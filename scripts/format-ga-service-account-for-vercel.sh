#!/usr/bin/env bash
# Print Vercel-ready values for GA4 Data API service account credentials.
# Usage: ./scripts/format-ga-service-account-for-vercel.sh /path/to/key.json
set -euo pipefail

KEY="${1:?Usage: $0 /path/to/service-account-key.json}"

if ! command -v jq >/dev/null 2>&1; then
  echo "Install jq first (brew install jq)." >&2
  exit 1
fi

COMPACT="$(jq -c . "$KEY")"
B64="$(printf '%s' "$COMPACT" | base64 | tr -d '\n')"
EMAIL="$(jq -r .client_email "$KEY")"
PROJECT="$(jq -r .project_id "$KEY")"

echo "GA4 property (Vercel): GA_PROPERTY_ID=538156526"
echo ""
echo "=== Recommended: GA_SERVICE_ACCOUNT_JSON_B64 ==="
echo "In Vercel, add env var GA_SERVICE_ACCOUNT_JSON_B64 and paste this entire line (no quotes):"
echo ""
echo "$B64"
echo ""
echo "You can delete or clear GA_SERVICE_ACCOUNT_JSON if you use B64 instead."
echo ""
echo "=== Alternative: GA_SERVICE_ACCOUNT_JSON (single line) ==="
echo "$COMPACT"
echo ""
echo "=== Alternative: split vars (if JSON keeps failing) ==="
echo "GA_SERVICE_ACCOUNT_CLIENT_EMAIL=$EMAIL"
echo "GA_SERVICE_ACCOUNT_PROJECT_ID=$PROJECT"
echo "GA_SERVICE_ACCOUNT_PRIVATE_KEY=<paste private_key from key.json; keep \\n or real line breaks>"
echo ""
echo "Then: vercel --prod"
echo "Grant access: ./scripts/grant-ga4-service-account-access.sh 538156526 \"$KEY\""
