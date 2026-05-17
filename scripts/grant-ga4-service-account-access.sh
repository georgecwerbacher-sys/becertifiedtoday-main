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
  echo "Run first: gcloud auth application-default login" >&2
  exit 1
fi

AUTH="Authorization: Bearer $TOKEN"
BASE="https://analyticsadmin.googleapis.com/v1beta"
USER="serviceAccount:${SA_EMAIL}"

echo "Property ID: $PROPERTY_ID"
echo "Service account: $SA_EMAIL"
echo ""

echo "Checking property..."
curl -sS -H "$AUTH" "$BASE/properties/$PROPERTY_ID" | jq '{name, displayName, parent}' || true
echo ""

echo "Existing access bindings on property..."
curl -sS -H "$AUTH" "$BASE/properties/$PROPERTY_ID/accessBindings" | jq '.accessBindings[]? | {name, user, roles}' || true
echo ""

PARENT="$(curl -sS -H "$AUTH" "$BASE/properties/$PROPERTY_ID" | jq -r '.parent // empty')"

echo "Creating property access binding (Viewer)..."
RESP="$(curl -sS -X POST \
  -H "$AUTH" \
  -H "Content-Type: application/json" \
  "$BASE/properties/$PROPERTY_ID/accessBindings" \
  -d "{\"user\":\"$USER\",\"roles\":[\"predefinedRoles/viewer\"]}")"

echo "$RESP" | jq .

if echo "$RESP" | jq -e '.error' >/dev/null 2>&1; then
  echo ""
  echo "Property-level grant failed. Trying account-level..."
  if [[ -n "$PARENT" && "$PARENT" == accounts/* ]]; then
    echo "Account: $PARENT"
    RESP2="$(curl -sS -X POST \
      -H "$AUTH" \
      -H "Content-Type: application/json" \
      "$BASE/${PARENT}/accessBindings" \
      -d "{\"user\":\"$USER\",\"roles\":[\"predefinedRoles/viewer\"]}")"
    echo "$RESP2" | jq .
  else
    echo "Could not resolve account parent for property $PROPERTY_ID" >&2
  fi
fi

echo ""
echo "Done. Wait 2–5 minutes, set GA_PROPERTY_ID=$PROPERTY_ID on Vercel, then refresh /admin/analytics"
