---
type: question-sourcing
exam: CCNA-200-301
content_type: labs-sim
---

# CCNA 200-301 — labs, drag-and-drop & simulation sourcing

**Catalog:** [[../ccna-labs-sim-web-sources|ccna-labs-sim-web-sources.md]]  
**Tracker:** [[../competitors-ccna-labs-sim-tracker.csv|competitors-ccna-labs-sim-tracker.csv]]

```bash
npm run ccna:labs-monthly       # collect + compare + save
npm run ccna:labs-collect
npm run ccna:labs-compare
npm run ccna:labs-save
npm run ccna:labs-poll-sources  # list enabled pbq_poll sites
```

**Poll registry:** `marketing-vault/10-competitors/sites/*-ccna.md` with `pbq_poll.enabled: true` and `product: CCNA-200-301`.

**Compare vs:** `CCNA_D_D/`, `CCNA_labs/`, `CCNA_Sim_EXAM/`

**Policy:** Paraphrase only; verify on Cisco Tier A before new HTML.

**MCQ pipeline:** [[../README|ccna/README]] · `npm run ccna:monthly`
