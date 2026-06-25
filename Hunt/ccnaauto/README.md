---
type: hunt-folder
exam: CCNAAUTO-200-901
aliases:
  - CCNA Automation
  - DevNet Associate
  - DEVASC
---

# CCNAAUTO question hunt

Net-new competitor candidates for **Automating Networks Using Cisco Platforms (200-901 CCNAAUTO) v1.1** — questions, labs, and performance-based samples not yet in the BCT bank.

## Hunt checklist

Primary objective list (track MCQ + lab coverage per row):

- [[../../CCNA-Auto/blueprint-hunt-list|Blueprint hunt list — 200-901 v1.1]]

## Source catalogs

- [[web-sources|MCQ web sources]]
- [[labs-web-sources|Labs / sim / PBQ web sources]]

## Workflow

| Step | MCQ | Labs / sim |
|------|-----|------------|
| Poll registry | `npm run ccnaauto:poll-sources` | `npm run ccnaauto:labs-poll-sources` |
| Full hunt | `npm run ccnaauto:monthly` | `npm run ccnaauto:labs-monthly` |
| Collect only | `npm run ccnaauto:collect` | `npm run ccnaauto:labs-collect` |
| Compare | `npm run ccnaauto:compare` | `npm run ccnaauto:labs-compare` |
| Save markdown | `npm run ccnaauto:save` | `npm run ccnaauto:labs-save` |

Data runs: `data/ccnaauto-question-sourcing/runs/` · competitor notes: `data/ccnaauto-question-sourcing/competitor-sites/`

Compare dedupes against **CCNA automation overlap** (CCNA 200-301 domain 6.x + Ansible/REST/JSON slugs) until a dedicated CCNAAUTO bank exists.

## Runs

- **2026-06-25** — 6 automation MCQs imported from [[../ccna/2026-06-25|CCNA hunt 2026-06-25]] (`data/ccnaauto-question-sourcing/runs/2026-06-25-net-new.md`)

## Related

- CCNA 200-301 hunt: [[../ccna/README|Hunt/ccna]]
- CCNA domain 6.0 tracker: `public/CCNA-Study/data/ccna-lab-topic-tracker.json`
