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

## Checklist

- [[blueprint-hunt-list|Blueprint hunt list — 200-901 v1.1]]

## Hunt inventory

- [[hunt-inventory|Inventory index]] — MCQ, drag-and-drop, labs from BCT bank + competitor hunt
- [[hunt-inventory-questions|Questions]] · [[hunt-inventory-drag-drop|Drag-and-drop]] · [[hunt-inventory-labs|Labs & sim]]

## Competitor sources

- [[competitor-hunt-sources|Competitor hunt list]] — Dion Training, HowToNetwork, CertiMaan (poll registry)

Mark **MCQ** and **Lab** columns as you find competitor samples or draft BCT items. Verify every answer on Cisco Tier A before bank draft.

## Hunt workflow

Monthly collect/compare lives in [[Hunt/ccnaauto/README|ccnaauto hunt index]] (runs, source catalogs, npm commands).

- MCQ: `npm run ccnaauto:monthly`
- Labs / sim: `npm run ccnaauto:labs-monthly`
- Regenerate Obsidian inventory: `npm run ccnaauto:inventory`
