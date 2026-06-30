#!/usr/bin/env bash
# End-to-end: service account → GA4 access → Vercel env → Cursor MCP (deep analytics).
#
# Recommended path for Cursor chat + /admin dashboard + weekly reports.
#
# Usage:
#   ./scripts/setup-ga-deep-analytics.sh
#   ./scripts/setup-ga-deep-analytics.sh /path/to/existing-key.json
#
# If gcloud auth is expired, the script stops with exact login commands.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
KEY_PATH="${1:-$HOME/.config/bcc-ga4-service-account.json}"
GA_PROPERTY_ID="${GA_PROPERTY_ID:-538156526}"
GCP_PROJECT_ID="${GCP_PROJECT_ID:-youtube-404901}"
PRIMARY_LANDING="${BCC_GA_PRIMARY_LANDING_PATH:-/comptia-sec+-home.html}"

export PATH="/opt/homebrew/bin:/opt/homebrew/share/google-cloud-sdk/bin:${PATH:-}"

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Missing: $1" >&2
    exit 1
  }
}

key_is_valid() {
  [[ -f "$1" && -s "$1" ]] && jq -e '.client_email and .private_key' "$1" >/dev/null 2>&1
}

try_vercel_key_extract() {
  need_cmd vercel
  if ! [[ -f "$ROOT/.vercel/project.json" ]]; then
    return 1
  fi
  echo "Trying Vercel production env for GA_SERVICE_ACCOUNT_JSON_B64…" >&2
  vercel env run -e production -- node -e "
    const fs = require('fs');
    const path = require('path');
    const b64 = (process.env.GA_SERVICE_ACCOUNT_JSON_B64 || '').trim();
    if (!b64) process.exit(2);
    const json = Buffer.from(b64, 'base64').toString('utf8');
    const out = process.argv[1];
    fs.mkdirSync(path.dirname(out), { recursive: true });
    fs.writeFileSync(out, json, { mode: 0o600 });
  " "$KEY_PATH" 2>/dev/null || return 1
  key_is_valid "$KEY_PATH"
}

ensure_key() {
  if [[ -n "${1:-}" ]]; then
    KEY_PATH="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
  fi

  if key_is_valid "$KEY_PATH"; then
    echo "Using service account key: $KEY_PATH"
    jq -r '"  " + .client_email' "$KEY_PATH"
    return 0
  fi

  if try_vercel_key_extract; then
    echo "Decoded key from Vercel → $KEY_PATH"
    return 0
  fi

  echo "No valid key at $KEY_PATH. Provisioning via gcloud…" >&2
  if ! "$ROOT/scripts/provision-ga-service-account-key.sh"; then
    echo "" >&2
    echo "=== Action required ===" >&2
    echo "1. In Terminal, log in (browser opens):" >&2
    echo "     gcloud auth login georgecwerbacher@gmail.com" >&2
    echo "     gcloud config set project $GCP_PROJECT_ID" >&2
    echo "2. Re-run:" >&2
    echo "     $0" >&2
    exit 1
  fi
}

grant_ga4_access() {
  echo ""
  echo "Granting GA4 Viewer on property ${GA_PROPERTY_ID} (skip if API already works)..."
  if "$ROOT/scripts/grant-ga4-service-account-access.sh" "$GA_PROPERTY_ID" "$KEY_PATH"; then
    return 0
  fi
  echo "Grant step skipped or failed — continuing if Data API smoke test passes." >&2
}

sync_vercel_env() {
  need_cmd vercel
  [[ -f "$ROOT/.vercel/project.json" ]] || {
    echo "Skip Vercel sync (not linked)." >&2
    return 0
  }

  local b64 compact
  compact="$(jq -c . "$KEY_PATH")"
  b64="$(printf '%s' "$compact" | base64 | tr -d '\n')"

  echo ""
  echo "Updating Vercel GA_SERVICE_ACCOUNT_JSON_B64 (production + preview)…"
  for env in production preview; do
    if vercel env ls "$env" 2>/dev/null | grep -q GA_SERVICE_ACCOUNT_JSON_B64; then
      printf '%s' "$b64" | vercel env update GA_SERVICE_ACCOUNT_JSON_B64 "$env" --yes
      echo "  updated GA_SERVICE_ACCOUNT_JSON_B64 ($env)"
    else
      printf '%s' "$b64" | vercel env add GA_SERVICE_ACCOUNT_JSON_B64 "$env" --yes
      echo "  added GA_SERVICE_ACCOUNT_JSON_B64 ($env)"
    fi
  done

  for env in production preview; do
    printf '%s' "$GA_PROPERTY_ID" | vercel env update GA_PROPERTY_ID "$env" --yes 2>/dev/null || \
      printf '%s' "$GA_PROPERTY_ID" | vercel env add GA_PROPERTY_ID "$env" --yes
    printf '%s' "G-YTT6KBHX7V" | vercel env update GA_MEASUREMENT_ID "$env" --yes 2>/dev/null || \
      printf '%s' "G-YTT6KBHX7V" | vercel env add GA_MEASUREMENT_ID "$env" --yes
    echo "  synced GA_PROPERTY_ID + GA_MEASUREMENT_ID ($env)"
  done

  echo "Verifying Vercel production GA env lengths…"
  vercel env run -e production -- node -e "
    const b=(process.env.GA_SERVICE_ACCOUNT_JSON_B64||'').length;
    const p=(process.env.GA_PROPERTY_ID||'').length;
    if (!b || !p) { console.error('Vercel GA env still empty (b64='+b+', property='+p+')'); process.exit(1); }
    console.log('Vercel GA env OK (b64 length '+b+', property '+process.env.GA_PROPERTY_ID+')');
  "
  echo "Vercel GA env synced. Redeploy for /admin to pick up changes."
}

smoke_test() {
  echo ""
  echo "Smoke test: GA4 Data API (${PRIMARY_LANDING} page views, 7d)…"
  GOOGLE_APPLICATION_CREDENTIALS="$KEY_PATH" BCC_GA_PRIMARY_LANDING_PATH="$PRIMARY_LANDING" node --input-type=module -e "
    import { readFileSync } from 'node:fs';
    import { BetaAnalyticsDataClient } from '@google-analytics/data';
    const landing = process.env.BCC_GA_PRIMARY_LANDING_PATH || '/comptia-sec+-home.html';
    const client = new BetaAnalyticsDataClient({
      credentials: JSON.parse(readFileSync(process.env.GOOGLE_APPLICATION_CREDENTIALS, 'utf8')),
    });
    const [r] = await client.runReport({
      property: 'properties/${GA_PROPERTY_ID}',
      dateRanges: [{ startDate: '7daysAgo', endDate: 'today' }],
      dimensions: [{ name: 'pagePath' }],
      metrics: [{ name: 'screenPageViews' }, { name: 'activeUsers' }],
      dimensionFilter: {
        filter: {
          fieldName: 'pagePath',
          stringFilter: { matchType: 'EXACT', value: landing },
        },
      },
    });
    const row = r.rows?.[0];
    console.log('  page:', landing);
    console.log('  screenPageViews (7d):', row?.metricValues?.[0]?.value ?? '0');
    console.log('  activeUsers (7d):', row?.metricValues?.[1]?.value ?? '0');
  " 2>&1
}

setup_mcp() {
  echo ""
  "$ROOT/scripts/setup-google-analytics-mcp.sh" "$KEY_PATH"
}

main() {
  need_cmd jq
  need_cmd brew

  if ! command -v python3.12 >/dev/null 2>&1 || ! command -v uv >/dev/null 2>&1; then
    echo "Installing Python 3.12 + uv…"
    brew install python@3.12 uv
  fi

  ensure_key "${1:-}"
  grant_ga4_access
  sync_vercel_env
  smoke_test
  setup_mcp

  cat <<EOF

=== Deep analytics ready ===

Cursor MCP:  $ROOT/.cursor/mcp.json  → restart Cursor → Settings → MCP
Admin UI:      https://becertifiedtoday.com/admin
Weekly report: npm run marketing:weekly-report

Ask in chat (examples):
  • Security+ home (/comptia-sec+-home.html): sessions by utm_campaign (secplus_portal) last 28d
  • begin_checkout for secplus_portal_30d on the home page
  • Funnel: home page_view → begin_checkout → purchase
  • Realtime users on /comptia-sec+-home.html right now

Local preview (tagged page): http://localhost:3000/comptia-sec+-home.html
Production: https://becertifiedtoday.com/comptia-sec+-home.html

EOF
}

main "$@"
