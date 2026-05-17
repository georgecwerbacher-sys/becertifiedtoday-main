#!/usr/bin/env bash
# Grant a GCP service account Viewer access to a GA4 property (Admin API).
# Run as a Google user who is Administrator on the GA4 property.
#
# Usage:
#   ./scripts/grant-ga4-service-account-access.sh 538156526 path/to/key.json
#   ./scripts/grant-ga4-service-account-access.sh 538156526 becertifiedtoday@youtube-404901.iam.gserviceaccount.com
#
# Requires: gcloud (for access token), curl, jq

set -euo pipefail

PROPERTY_ID="${1:-}"
SA_INPUT="${2:-}"

if [[ -z "$PROPERTY_ID" || -z "$SA_INPUT" ]]; then
  echo "Usage: $0 <GA4_PROPERTY_ID> <service-account-email OR path-to-key.json>" >&2
  exit 1
fi

if [[ -f "$SA_INPUT" ]]; then
  SA_EMAIL="$(jq -r '.client_email' "$SA_INPUT")"
else
  SA_EMAIL="$SA_INPUT"
fi

if [[ -z "$SA_EMAIL" || "$SA_EMAIL" == "null" ]]; then
  echo "Could not read client_email from: $SA_INPUT" >&2
  exit 1
fi

TOKEN="$(gcloud auth application-default print-access-token 2>/dev/null || true)"
if [[ -z "$TOKEN" ]]; then
  TOKEN="$(gcloud auth print-access-token 2>/dev/null || true)"
fi
if [[ -z "$TOKEN" ]]; then
  echo "Run first (in Terminal — do not copy OAuth URLs from chat):" >&2
  echo "  gcloud auth login YOUR_GA4_ADMIN@gmail.com" >&2
  echo "  gcloud auth application-default login --scopes=https://www.googleapis.com/auth/analytics.manage.users,https://www.googleapis.com/auth/cloud-platform,openid,https://www.googleapis.com/auth/userinfo.email" >&2
  exit 1
fi

SCOPE_INFO="$(curl -sS "https://oauth2.googleapis.com/tokeninfo?access_token=${TOKEN}" 2>/dev/null || true)"
if ! echo "$SCOPE_INFO" | grep -q analytics.manage.users; then
  echo "Your token is missing analytics.manage.users." >&2
  echo "Run: ./scripts/ga4-admin-oauth-login.sh" >&2
  exit 1
fi

AUTH="Authorization: Bearer $TOKEN"
BASE="https://analyticsadmin.googleapis.com/v1alpha"
QUOTA_HDR="x-goog-user-project: youtube-404901"

echo "Property ID: $PROPERTY_ID"
echo "Service account: $SA_EMAIL"
echo ""

echo "Checking property..."
curl -sS -H "$AUTH" -H "$QUOTA_HDR" \
  "https://analyticsadmin.googleapis.com/v1beta/properties/$PROPERTY_ID" | jq '{name, displayName, parent}' || true
echo ""

echo "Existing access bindings on property..."
curl -sS -H "$AUTH" -H "$QUOTA_HDR" \
  "$BASE/properties/$PROPERTY_ID/accessBindings" | jq '.accessBindings[]? | {name, user, roles}' || true
echo ""

PARENT="$(curl -sS -H "$AUTH" -H "$QUOTA_HDR" \
  "https://analyticsadmin.googleapis.com/v1beta/properties/$PROPERTY_ID" | jq -r '.parent // empty')"

echo "Creating property access binding (Viewer)..."
RESP="$(curl -sS -X POST \
  -H "$AUTH" \
  -H "$QUOTA_HDR" \
  -H "Content-Type: application/json" \
  "$BASE/properties/$PROPERTY_ID/accessBindings" \
  -d "{\"user\":\"${SA_EMAIL}\",\"roles\":[\"predefinedRoles/viewer\"]}")"

echo "$RESP" | jq .

if echo "$RESP" | jq -e '.error' >/dev/null 2>&1; then
  echo ""
  echo "Property-level grant failed. Trying account-level..."
  if [[ -n "$PARENT" && "$PARENT" == accounts/* ]]; then
    echo "Account: $PARENT"
    RESP2="$(curl -sS -X POST \
      -H "$AUTH" \
      -H "$QUOTA_HDR" \
      -H "Content-Type: application/json" \
      "$BASE/${PARENT}/accessBindings" \
      -d "{\"user\":\"${SA_EMAIL}\",\"roles\":[\"predefinedRoles/viewer\"]}")"
    echo "$RESP2" | jq .
  else
    echo "Could not resolve account parent for property $PROPERTY_ID" >&2
  fi
fi

echo ""
echo "Done. Wait 2–5 minutes, set GA_PROPERTY_ID=$PROPERTY_ID on Vercel, then refresh /admin/analytics"
