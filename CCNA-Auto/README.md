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

## Hunt (Obsidian)

- [[competitor-list|Competitor list]] — sites to poll and URLs to scan manually
- **[[hunt-results/README|Hunt results]]** — one doc per run with full question text

## Checklist

- [[exam-objectives|Official exam objectives]] — v1.1 CCNAAUTO + v1.0 DEVASC PDFs
- [[blueprint-hunt-list|Blueprint hunt list — 200-901 v1.1]]

## Hunt workflow (Cursor)

```bash
npm run ccnaauto:hunt
```

Or step by step:

- MCQ: `npm run ccnaauto:monthly`
- Labs / PBQ / D&D signals: `npm run ccnaauto:labs-monthly`
- Export to `CCNA-Auto/hunt-results/`: `npm run ccnaauto:export`

Verify every answer on **Cisco Tier A** before bank draft.
