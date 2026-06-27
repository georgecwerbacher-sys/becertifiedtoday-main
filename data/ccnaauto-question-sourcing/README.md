# CCNAAUTO 200-901 question sourcing

Competitor polls use the **master registry**: `data/competitor-sites/` (`*-ccnaauto.md`, `product: CCNAAUTO-200-901`).

Obsidian: [[../../marketing-research/competitor-sites/README|competitor-sites]] · checklist [[../../CCNA-Auto/competitor-list|CCNA-Auto competitor list]]

| Workflow | npm | Poll key |
|----------|-----|----------|
| MCQ hunt | `npm run ccnaauto:monthly` | `question_poll.enabled` |
| Labs / sim / PBQ hunt | `npm run ccnaauto:labs-monthly` | `pbq_poll.enabled` |

Runs: `data/ccnaauto-question-sourcing/runs/` · full hunt: `npm run ccnaauto:hunt`
