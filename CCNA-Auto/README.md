---
type: hunt-blueprint-folder
exam: CCNAAUTO-200-901
aliases:
  - CCNA Automation
  - DevNet Associate
  - 200-901
---

# CCNA-Auto

Blueprint checklist and objective tracking for **200-901 CCNAAUTO v1.1** (CCNA Automation).

**Hunt scope:** CCNAAUTO **200-901** competitor polls only — not CCNA 200-301.

## Hunt results (Obsidian)

- [[hunt-inventory|Hunt inventory]] — summary counts
- **[[hunt-results/README|Scraped questions (full text)]]** — per-question notes with stems and choices
- [[hunt-inventory-questions|Questions index]] · [[hunt-inventory-labs|Labs & PBQ]] · [[hunt-inventory-drag-drop|Drag-and-drop]]
- Dedupe reference only: [[bct-overlap-reference|BCT overlap (CCNA bank)]]

## Competitors (edit me)

Same master list as Sec+, CCNA 200-301, and ENCOR: **`marketing-research/competitor-sites/`** (`data/competitor-sites/`).

- [[competitor-list|CCNAAUTO 200-901 rows]] — active + backlog table for this exam
- [[../competitor-sites/README|Full competitor registry]] (`data/competitor-sites/`)

## Checklist

- [[exam-objectives|Official exam objectives]] — v1.1 CCNAAUTO + v1.0 DEVASC PDFs
- [[blueprint-hunt-list|Blueprint hunt list — 200-901 v1.1]]

## Hunt workflow

Rerun everything (poll → compare → Obsidian export → inventory):

```bash
npm run ccnaauto:hunt
```

Or step by step:

- MCQ: `npm run ccnaauto:monthly`
- Labs / PBQ / D&D signals: `npm run ccnaauto:labs-monthly`
- Export to `Hunt/ccnaauto/`: `npm run ccnaauto:export`
- Refresh `CCNA-Auto/hunt-inventory*.md`: `npm run ccnaauto:inventory`

Verify every answer on **Cisco Tier A** before bank draft.
