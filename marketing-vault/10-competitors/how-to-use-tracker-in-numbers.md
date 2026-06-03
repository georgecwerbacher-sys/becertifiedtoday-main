---
type: playbook
status: active
---

# Open the competitor tracker in Apple Numbers

1. In Finder, go to `marketing-vault/10-competitors/`.
2. Double-click **`competitors-pdf-dumps-tracker.csv`** — Numbers opens it as a new spreadsheet.
3. Optional: **File → Export To → Numbers…** and save as `competitors-pdf-dumps-tracker.numbers` beside the CSV so formatting (filters, freeze header) persists.
4. Link the Numbers file in Obsidian with `[[competitors-pdf-dumps-tracker.csv]]` or attach the `.numbers` file to this note once exported.

## Suggested Numbers columns to format

- **popup_aggressiveness**, **outdated_risk**, **pbq_fidelity** — data validation lists (Low / Medium / High)
- **price_pdf_usd**, **price_bundle_usd** — currency
- **research_date** — date
- Freeze row 1; turn on filters for `category` and `syndicated_bundle`

## Sync with Obsidian

- Edit narrative in [[pdf-dump-market-analysis]] when strategy shifts.
- Add a row to the CSV when you discover a new dump site; add a matching `sites/<brand>.md` if you need screenshots or ad screenshots archived.
