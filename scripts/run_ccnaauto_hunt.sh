#!/usr/bin/env bash
# CCNAAUTO 200-901 full hunt: poll competitors → compare → Obsidian export → inventory.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== CCNAAUTO 200-901 MCQ hunt =="
npm run ccnaauto:monthly

echo "== CCNAAUTO 200-901 labs / PBQ / D&D hunt =="
npm run ccnaauto:labs-monthly

echo "== Obsidian export (Hunt/ccnaauto/) =="
python3 scripts/export_ccnaauto_hunt_obsidian.py

echo "== CCNA-Auto inventory =="
python3 scripts/gen_ccnaauto_hunt_inventory.py

echo ""
echo "Done."
echo "  Questions:   CCNA-Auto/hunt-results/"
echo "  Inventory:   CCNA-Auto/hunt-inventory.md"
echo "  Competitors: CCNA-Auto/competitor-list.md"
