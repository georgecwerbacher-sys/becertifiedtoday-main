# SY0-701 PBQ sourcing

Performance-based question (PBQ) research — drag-and-drop, hot spot, ordered log timelines, multi-step sims — for gap analysis vs the BCT PBQ bank.

**Policy:** Same tiers as MCQ sourcing ([[../secplus-sy0-701-web-sources|SY0-701 web sources]]). **Uncredited sources (Tier C)** are discovery only. **Verify on CompTIA Tier A / objectives v5.0** before shipping HTML.

**BCT bank:**

| Path | Content |
|------|---------|
| `public/COMP_TIA_SEC+/SEC+_PBQ/README.md` | Drag-and-drop template doc + checklist |
| `public/COMP_TIA_SEC+/SEC+_PBQ/TEMPLATE-dragdrop.html` | Copy skeleton for new drag-and-drop PBQs |
| `public/COMP_TIA_SEC+/js/secplus-pbq-page.css` | Shared PBQ layout (14% logo, purple blocks, blue drop slots, nav buttons) |
| `public/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/` | Full simulations and hot spots |

**Poll registry:** `marketing-vault/10-competitors/sites/*.md` with **`pbq_poll.enabled: true`** (separate from `question_poll` for MCQ).

**Monthly process:**

```bash
npm run secplus:pbq-monthly
```

Playbook: [[../05-playbooks/secplus-monthly-pbq-sourcing|secplus-monthly-pbq-sourcing]]

---

## Folder map

| Path | Purpose |
|------|---------|
| [[secplus-pbq-web-sources\|PBQ web source catalog]] | Tier A/B/C PBQ-heavy sources |
| [[secplus-pbq-not-in-bct\|PBQ net-new log]] | Accepted candidates after compare |
| `config/secplus-pbq-sources.json` | Tier A notes + poll registry pointer |
| `templates/discovered-pbq-import.csv` | Manual paste format |
| `imports/` | Your paste CSVs |
| `runs/` | `YYYY-MM-DD-discovered.csv`, compare, net-new `.md` |

---

## MCQ vs PBQ pipeline

| | MCQ (`11-question-sourcing/`) | PBQ (`11-question-sourcing/pbq/`) |
|--|-------------------------------|-----------------------------------|
| Script | `secplus_monthly_question_hunt.py` | `secplus_monthly_pbq_hunt.py` |
| npm | `secplus:monthly` | `secplus:pbq-monthly` |
| Poll key | `question_poll` | `pbq_poll` |
| Compare vs | `SEC+_Questions/` | `SEC+_PBQ/` + `SEC+_Sim_Hot_Spot/` |
| Ship to | `gen_secplus_chain_pages.py` | `public/COMP_TIA_SEC+/SEC+_PBQ/*.html` |

Related: [[../secplus-sy0-701-web-sources|MCQ source catalog]] · [[../10-competitors/practice-samples-competitors|Practice competitors]]
