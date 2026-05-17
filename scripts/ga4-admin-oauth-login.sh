#!/usr/bin/env bash
# Log in for GA4 Admin API (grant service account access) using YOUR OAuth client.
# Google's default gcloud OAuth app is often blocked for analytics.manage.users.
#
# One-time setup (project youtube-404901):
#   1. Enable Google Analytics Admin API
#   2. APIs & Services → OAuth consent screen → add scope "analytics.manage.users"
#      → Test users → add georgecwerbacher@gmail.com (GA4 Administrator)
#   3. Credentials → Create OAuth client ID → Desktop app → Download JSON
#   4. Save as: ~/.config/bcc-ga4-oauth-client.json  (do not commit)
#
# Usage:
#   ./scripts/ga4-admin-oauth-login.sh
#   BCC_GA4_OAUTH_CLIENT_JSON=/path/to/client.json ./scripts/ga4-admin-oauth-login.sh

set -euo pipefail

export PATH="/opt/homebrew/share/google-cloud-sdk/bin:/opt/homebrew/bin:${PATH:-}"

CLIENT_JSON="${BCC_GA4_OAUTH_CLIENT_JSON:-$HOME/.config/bcc-ga4-oauth-client.json}"
SCOPES="https://www.googleapis.com/auth/analytics.manage.users,https://www.googleapis.com/auth/analytics.edit,https://www.googleapis.com/auth/cloud-platform,openid,https://www.googleapis.com/auth/userinfo.email"

if [[ ! -f "$CLIENT_JSON" ]]; then
  echo "Missing OAuth client JSON: $CLIENT_JSON" >&2
  echo "" >&2
  echo "Create a Desktop OAuth client in project youtube-404901, then:" >&2
  echo "  mkdir -p ~/.config" >&2
  echo "  mv ~/Downloads/client_secret_*.json ~/.config/bcc-ga4-oauth-client.json" >&2
  echo "" >&2
  echo "Consent screen (Testing): add georgecwerbacher@gmail.com as a test user." >&2
  echo "Add scope: .../auth/analytics.manage.users" >&2
  exit 1
fi

CLIENT_ID="$(jq -r '.installed.client_id // .web.client_id // .client_id // empty' "$CLIENT_JSON")"

if [[ -z "$CLIENT_ID" ]]; then
  echo "Could not read client_id from: $CLIENT_JSON" >&2
  exit 1
fi

echo "Using OAuth client: $CLIENT_ID"
echo "Browser will open — sign in as georgecwerbacher@gmail.com (GA4 Admin)."
echo ""

gcloud config set account georgecwerbacher@gmail.com 2>/dev/null || true
gcloud auth application-default login \
  --client-id-file="$CLIENT_JSON" \
  --scopes="$SCOPES"

echo ""
echo "ADC saved. Run:"
echo "  ./scripts/grant-ga4-service-account-access.sh 538156526 /Users/werby/Downloads/youtube-404901-e307f982ad9e.json"
