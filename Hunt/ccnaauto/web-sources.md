---
type: hunt-source-catalog
exam: CCNAAUTO-200-901
poll_key: question_poll
---

# CCNAAUTO MCQ web sources

Tier B = credited practice samples · Tier C = community recall (discovery only).

Enable `question_poll.enabled: true` in a site note after parser smoke test, then run `npm run ccnaauto:monthly`.

| Site | File | Tier | Poll id | Status |
|------|------|:----:|---------|--------|
| CertiMaan | `data/ccnaauto-question-sourcing/competitor-sites/certimaan-ccnaauto.md` | C | `certimaan-ccnaauto-samples` | disabled — enable after parser test |
| Dion Training | `data/ccnaauto-question-sourcing/competitor-sites/diontraining-ccnaauto.md` | B | `diontraining-ccnaauto-practice` | disabled — no CCNAAUTO SKU yet (2026-06-25) |
| HowToNetwork | `data/ccnaauto-question-sourcing/competitor-sites/howtonetwork-ccnaauto.md` | B | `howtonetwork-ccnaauto-quiz` | disabled — research quiz hub |

## Add a site

1. Copy [[../../data/competitor-sites/README#Add a new site|competitor-sites README]] frontmatter block
2. Set `product: CCNAAUTO-200-901` and filename `*-ccnaauto.md` under `data/ccnaauto-question-sourcing/competitor-sites/`
3. Set `version_note: 200-901 v1.1`
4. Map parser in `scripts/secplus_competitor_poll.py` if new site type

## Manual import

```bash
npm run ccnaauto:collect -- --import path/to/manual.csv
```

CSV columns match other hunt scripts (`stem`, `choice_a`…`choice_f`, `stated_answer`, `source_id`, etc.).

Back: [[README|CCNAAUTO hunt index]] · checklist: [[../../CCNA-Auto/blueprint-hunt-list|Blueprint hunt list]]
