# Question sourcing

Research catalog for **where practice questions appear on the web** — for coverage gaps, objective mapping, and competitor sizing.

## CCNA 200-301

**MCQ catalog:** [[ccna/ccna-200-301-web-sources|CCNA web sources]] · `npm run ccna:monthly` · `ccna/runs/`  
**Labs / sim catalog:** [[ccna/ccna-labs-sim-web-sources|CCNA labs & sim]] · `npm run ccna:labs-monthly` · `ccna/labs-sim/runs/`  
**Net-new markdown layout:** `config/net-new-markdown.json` (shared) + `config/ccna-web-sources.json` → `net_new_markdown`

## ENCOR 350-401 (planned)

**Stub:** [[encor/README|encor/README]] · `config/encor-web-sources.json` — same net-new markdown settings as CCNA; monthly hunt **not** wired yet.

## Security+ SY0-701

**Policy:** **Uncredited sites** (Tier C — Reddit, forums, recall threads, dump indexes) feed **discovery only**: collect → compare vs BCT → review in Obsidian → **optionally add** original questions to the database. **Verify correctness only on Tier A** (CompTIA official).

**Poll registry:** add sites under [[../10-competitors/sites/README|10-competitors/sites]] with `question_poll.enabled: true` — monthly collect polls them automatically.

Workflow when you find a new source:

1. Add a row to [[secplus-sy0-701-web-sources|SY0-701 web sources]] only if the source is **SY0-701** and stated refresh is **2026+** (Tier A blueprint PDF is the exception).
2. Set `date_added` (vault) and **published version/date** the site states — **remove** rows when you later find the product is pre-2026.
3. Map stems to `public/COMP_TIA_SEC+/data/secplus-exam-objectives-sy0-701.json` objective IDs when you adopt a question.

Related: [[../10-competitors/practice-samples-competitors|Practice competitors]] · [[../10-competitors/pdf-dump-market-analysis|PDF dump market]] · [[../10-competitors/sites/examtopics|ExamTopics]] · in-repo bank `public/COMP_TIA_SEC+/SEC+_Questions/`.

**Monthly process (MCQ):** `npm run secplus:monthly` — collect → compare → save (Obsidian `.md`). Playbook: [[../05-playbooks/secplus-monthly-question-sourcing|secplus-monthly-question-sourcing]].

**Monthly process (PBQ):** `npm run secplus:pbq-monthly` — same three steps for performance-based items. Folder: [[pbq/README|pbq/]] · Playbook: [[../05-playbooks/secplus-monthly-pbq-sourcing|secplus-monthly-pbq-sourcing]].
