---
type: question-sourcing
exam: CCNA-200-301
---

# CCNA 200-301 — monthly question sourcing

**MCQ catalog:** [[ccna-200-301-web-sources|ccna-200-301-web-sources.md]] · tracker [[../../10-competitors/competitors-ccna-practice-samples-tracker.csv|MCQ tracker]]  
**Labs / sim catalog:** [[ccna-labs-sim-web-sources|ccna-labs-sim-web-sources.md]] · tracker [[competitors-ccna-labs-sim-tracker.csv|labs-sim tracker]] · [[labs-sim/README|labs-sim workflow]]

**Workflow:** collect competitor polls → compare vs BCT CCNA bank → save net-new markdown for review.

```bash
npm run ccna:monthly      # collect + compare + save
npm run ccna:collect      # step 1 only
npm run ccna:compare      # step 2 only
npm run ccna:save         # step 3 only
npm run ccna:poll-sources # list enabled CCNA MCQ poll sites
npm run ccna:labs-monthly  # labs / D&D / sim collect → compare → save
npm run ccna:labs-poll-sources
```

**Poll registry:** `marketing-vault/10-competitors/sites/*-ccna.md` with `question_poll.enabled: true` and `product: CCNA-200-301`.

**Config:** `config/ccna-web-sources.json` (product) · `config/net-new-markdown.json` (shared review layout)

**ENCOR (planned):** [[../encor/README|encor/README]] — same markdown settings; hunt not wired yet.

**Runs:** `runs/YYYY-MM-DD-discovered.csv`, `-compare.md`, `-net-new.md`

**Policy:** Tier B/C discovery only. Verify every key on **Cisco Tier A** (official docs / Learning Network) before adding originals to `gen_ccna_chain_pages.py`.

**Competitors:** [[../../10-competitors/practice-samples-ccna-competitors|practice-samples-ccna-competitors]]
