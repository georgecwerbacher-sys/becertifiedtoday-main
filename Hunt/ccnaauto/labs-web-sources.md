---
type: hunt-source-catalog
exam: CCNAAUTO-200-901
poll_key: pbq_poll
---

# CCNAAUTO labs / sim / PBQ web sources

Target formats for CCNAAUTO v1.1 performance-based items:

- Python script completion or interpretation
- Ansible playbook workflow
- REST API request/response troubleshooting
- JSON / YANG drag-and-drop
- Bash script workflow
- Unified diff / sequence diagram interpretation

Enable `pbq_poll.enabled: true`, then run `npm run ccnaauto:labs-monthly`.

| Site | File | Tier | Poll id | Status |
|------|------|:----:|---------|--------|
| CertiMaan | `data/ccnaauto-question-sourcing/competitor-sites/certimaan-ccnaauto.md` | C | `certimaan-ccnaauto-pbq` | disabled |
| Dion Training | `data/ccnaauto-question-sourcing/competitor-sites/diontraining-ccnaauto.md` | B | `diontraining-ccnaauto-pbq` | disabled — watch for PBQ/lab packs |
| HowToNetwork | `data/ccnaauto-question-sourcing/competitor-sites/howtonetwork-ccnaauto.md` | B | `howtonetwork-ccnaauto-pbq` | disabled |

## BCT compare baseline

Until a dedicated CCNAAUTO lab bank exists, compare uses:

- `public/CCNA-Study/CCNA_D_D/` (JSON/automation drag-and-drop)
- `public/CCNA-Study/CCNA_labs/` (CLI labs with automation themes)
- `public/CCNA_Sim_EXAM/`

Track gaps against [[../../CCNA-Auto/blueprint-hunt-list#Hunt priorities (first pass)|hunt priorities]].

Back: [[README|CCNAAUTO hunt index]]
