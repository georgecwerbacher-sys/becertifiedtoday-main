#!/usr/bin/env bash
# Map a file under public/ to http://localhost:3000/... and open in the default browser.
set -euo pipefail

file="${1:-}"
if [[ -z "$file" ]]; then
  echo "Usage: open-localhost.sh <path-to-file-under-public>" >&2
  exit 1
fi

root="$(cd "$(dirname "$0")/.." && pwd)"
public="$root/public"

if [[ "$file" != /* ]]; then
  file="$root/$file"
fi

case "$file" in
  "$public"/*) ;;
  *)
    echo "File must be under public/: $file" >&2
    exit 1
    ;;
esac

rel="${file#$public/}"
url="http://localhost:3000/$rel"

if ! curl -sf -o /dev/null --max-time 2 "$url" 2>/dev/null; then
  echo "Warning: nothing responded at $url — run \"npm run serve\" first." >&2
fi

open "$url"
