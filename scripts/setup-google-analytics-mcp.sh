#!/usr/bin/env bash
# Wire Cursor to Google Analytics via the official analytics-mcp server.
# Read-only: run reports, list properties, realtime — same GA4 property as /admin.
#
# Prereqs (one-time):
#   1. GA4 property 538156526 (becertifiedtoday.com) — already tagged G-YTT6KBHX7V
#   2. GCP project youtube-404901 with Analytics Admin + Data APIs enabled
#   3. Service account JSON with Viewer on the GA4 property, OR OAuth ADC login
#
# Service account path (recommended — matches Vercel /admin):
#   ./scripts/setup-google-analytics-mcp.sh /path/to/service-account-key.json
#
# OAuth (your Google user, read-only):
#   gcloud auth application-default login \
#     --scopes https://www.googleapis.com/auth/analytics.readonly,https://www.googleapis.com/auth/cloud-platform \
#     --client-id-file="$HOME/.config/bcc-ga4-oauth-client.json"
#   ./scripts/setup-google-analytics-mcp.sh
#
# After running: restart Cursor → Settings → MCP → analytics-mcp should be Connected.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MCP_JSON="$ROOT/.cursor/mcp.json"
GA_PROPERTY_ID="${GA_PROPERTY_ID:-538156526}"
GCP_PROJECT_ID="${GCP_PROJECT_ID:-youtube-404901}"
PRIMARY_LANDING="${BCC_GA_PRIMARY_LANDING_PATH:-/comptia-sec+-home.html}"
KEY_ARG="${1:-}"

export PATH="/opt/homebrew/bin:/opt/homebrew/share/google-cloud-sdk/bin:${PATH:-}"

need_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

ANALYTICS_MCP_VENV="${BCC_ANALYTICS_MCP_VENV:-$HOME/.local/analytics-mcp-venv}"
ANALYTICS_MCP_BIN="$ANALYTICS_MCP_VENV/bin/analytics-mcp"

ensure_analytics_mcp() {
  if [[ -x "$ANALYTICS_MCP_BIN" ]]; then
    return 0
  fi
  need_cmd uv
  if ! command -v python3.12 >/dev/null 2>&1; then
    echo "Installing Python 3.12 for analytics-mcp…" >&2
    brew install python@3.12
  fi
  echo "Installing analytics-mcp into $ANALYTICS_MCP_VENV …" >&2
  uv venv "$ANALYTICS_MCP_VENV" --python python3.12
  uv pip install --python "$ANALYTICS_MCP_VENV/bin/python" analytics-mcp
  [[ -x "$ANALYTICS_MCP_BIN" ]] || {
    echo "analytics-mcp install failed: $ANALYTICS_MCP_BIN missing" >&2
    exit 1
  }
}

resolve_credentials() {
  local default_key="$HOME/.config/bcc-ga4-service-account.json"

  if [[ -n "$KEY_ARG" ]]; then
    if [[ ! -f "$KEY_ARG" ]]; then
      echo "Service account key not found: $KEY_ARG" >&2
      exit 1
    fi
    CREDS="$(cd "$(dirname "$KEY_ARG")" && pwd)/$(basename "$KEY_ARG")"
  elif [[ -f "$default_key" ]] && jq -e '.client_email and .private_key' "$default_key" >/dev/null 2>&1; then
    CREDS="$default_key"
  else
    CREDS=""
  fi

  if [[ -n "$CREDS" ]]; then
    PROJECT_ID="$(jq -r .project_id "$CREDS")"
    SA_EMAIL="$(jq -r .client_email "$CREDS")"
    echo "Using service account: $SA_EMAIL"
    echo "Grant Viewer on GA4 property $GA_PROPERTY_ID if needed:"
    echo "  ./scripts/grant-ga4-service-account-access.sh $GA_PROPERTY_ID \"$CREDS\""
    return 0
  fi

  ADC="$HOME/.config/gcloud/application_default_credentials.json"
  if [[ -f "$ADC" ]]; then
    CREDS="$ADC"
    PROJECT_ID="$GCP_PROJECT_ID"
    echo "Using Application Default Credentials: $ADC"
    return 0
  fi

  echo "No credentials found." >&2
  echo "" >&2
  echo "Recommended — full setup (service account + MCP + Vercel):" >&2
  echo "  ./scripts/setup-ga-deep-analytics.sh" >&2
  echo "" >&2
  echo "Or pass a key path:" >&2
  echo "  $0 /path/to/service-account-key.json" >&2
  exit 1
}

write_mcp_json() {
  need_cmd jq
  mkdir -p "$(dirname "$MCP_JSON")"
  jq -n \
    --arg cmd "$ANALYTICS_MCP_BIN" \
    --arg creds "$CREDS" \
    --arg project "${PROJECT_ID:-$GCP_PROJECT_ID}" \
    --arg landing "$PRIMARY_LANDING" \
    '{
      mcpServers: {
        "analytics-mcp": {
          command: $cmd,
          args: [],
          env: {
            GOOGLE_APPLICATION_CREDENTIALS: $creds,
            GOOGLE_PROJECT_ID: $project,
            BCC_GA_PRIMARY_LANDING_PATH: $landing
          }
        }
      }
    }' >"$MCP_JSON"
}

prefetch_mcp() {
  echo "Verifying analytics-mcp binary…" >&2
  test -x "$ANALYTICS_MCP_BIN"
}

main() {
  need_cmd jq
  if ! command -v uv >/dev/null 2>&1; then
    echo "Installing uv…" >&2
    brew install uv
  fi
  ensure_analytics_mcp
  resolve_credentials
  write_mcp_json
  prefetch_mcp

  cat <<EOF

Wrote $MCP_JSON

Next:
  1. Restart Cursor (or reload MCP servers in Settings → MCP).
  2. Confirm "analytics-mcp" shows Connected with tools like run_report.
  3. Ask in chat, e.g.:
     "Sessions and begin_checkout on $PRIMARY_LANDING (secplus_portal) last 28 days"

GA4 property ID: $GA_PROPERTY_ID
Primary landing:   $PRIMARY_LANDING
Measurement ID:  G-YTT6KBHX7V (site tagging — separate from MCP property queries)
Local preview:   http://localhost:3000/comptia-sec+-home.html

EOF
}

main
