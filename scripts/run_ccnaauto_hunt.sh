#!/usr/bin/env bash
# CCNAAUTO 200-901 full hunt: poll competitors → compare → Obsidian export.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== CCNAAUTO 200-901 MCQ hunt =="
npm run ccnaauto:monthly

echo "== CCNAAUTO 200-901 labs / PBQ / D&D hunt =="
npm run ccnaauto:labs-monthly

echo "== Obsidian export (CCNA-Auto/hunt-results/) =="
python3 scripts/export_ccnaauto_hunt_obsidian.py

echo ""
echo "Done."
echo "  Results:     CCNA-Auto/hunt-results/"
echo "  Competitors: CCNA-Auto/competitor-list.md"
