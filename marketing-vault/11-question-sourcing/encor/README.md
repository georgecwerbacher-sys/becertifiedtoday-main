---
type: question-sourcing
exam: ENCOR-350-401
status: planned
---

# ENCOR 350-401 — monthly question sourcing (planned)

**Not wired yet** — no collect / compare / save scripts or `npm run encor:*` commands.

When the hunt ships, it will reuse the same **net-new review markdown** settings as CCNA:

| Setting | Location |
|---------|----------|
| Shared layout (double gap, version-only line, Source format) | `config/net-new-markdown.json` |
| ENCOR copy + per-source blueprint map | `config/encor-web-sources.json` → `net_new_markdown` |
| Writer module | `scripts/net_new_markdown.py` |

**CCNA reference:** [[../ccna/README|ccna/README]] · `npm run ccna:monthly`

**BCT bank (compare target):** `public/CCNP-ENCOR-Study/` practice questions (hunt will index when implemented).

**Next steps (when ready):**

1. Add `encor-350-401-web-sources.md` catalog + competitor `*-encor.md` poll notes
2. Add `scripts/encor_monthly_question_hunt.py` mirroring CCNA (import `net_new_markdown.write_net_new_md`)
3. Register `encor:monthly` in `package.json`
