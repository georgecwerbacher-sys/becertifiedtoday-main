#!/usr/bin/env bash
# Create a new JSON key for the GA4 Data API service account (recommended path).
# Requires: gcloud logged in as a user who can create keys on the SA.
#
# Usage:
#   ./scripts/provision-ga-service-account-key.sh
#   GA_SERVICE_ACCOUNT_EMAIL=other@project.iam.gserviceaccount.com ./scripts/provision-ga-service-account-key.sh

set -euo pipefail

export PATH="/opt/homebrew/share/google-cloud-sdk/bin:/opt/homebrew/bin:${PATH:-}"

GCP_PROJECT_ID="${GCP_PROJECT_ID:-youtube-404901}"
SA_EMAIL="${GA_SERVICE_ACCOUNT_EMAIL:-becertifiedtoday@${GCP_PROJECT_ID}.iam.gserviceaccount.com}"
OUT="${BCC_GA_SERVICE_ACCOUNT_KEY:-$HOME/.config/bcc-ga4-service-account.json}"

if ! command -v gcloud >/dev/null 2>&1; then
  echo "Install Google Cloud SDK first: brew install --cask google-cloud-sdk" >&2
  exit 1
fi

if ! gcloud auth list --filter=status:ACTIVE --format='value(account)' 2>/dev/null | grep -q .; then
  echo "No active gcloud account. Run in Terminal (browser will open):" >&2
  echo "  gcloud auth login georgecwerbacher@gmail.com" >&2
  echo "  gcloud config set project $GCP_PROJECT_ID" >&2
  exit 1
fi

mkdir -p "$(dirname "$OUT")"
if [[ -f "$OUT" && -s "$OUT" ]]; then
  EXISTING_EMAIL="$(jq -r .client_email "$OUT" 2>/dev/null || true)"
  if [[ "$EXISTING_EMAIL" == "$SA_EMAIL" ]]; then
    echo "Key already exists: $OUT ($EXISTING_EMAIL)"
    exit 0
  fi
  BACKUP="${OUT}.bak.$(date +%Y%m%d%H%M%S)"
  echo "Backing up existing key to $BACKUP"
  mv "$OUT" "$BACKUP"
fi

echo "Creating key for $SA_EMAIL (project $GCP_PROJECT_ID)…"
gcloud iam service-accounts keys create "$OUT" \
  --iam-account="$SA_EMAIL" \
  --project="$GCP_PROJECT_ID"
chmod 600 "$OUT"

echo ""
echo "Wrote $OUT"
echo "Grant GA4 Viewer if needed:"
echo "  ./scripts/grant-ga4-service-account-access.sh 538156526 \"$OUT\""
