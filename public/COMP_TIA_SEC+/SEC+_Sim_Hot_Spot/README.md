# Security+ simulations and PBQ workspace

| Path | Purpose |
|------|---------|
| `simulation-*.html`, `hotspot-*.html` | Legacy redirects → `pending/` or production labs |
| `reports/` | In-sim report pages (noindex) |
| `images/` | Shared exhibit assets |
| **`PBQ_Production/`** | **Production** PBQ suite — 21 scenarios from `scripts/build-pbq-production-suite.py` |
| `pending/` | Staged sims and PBQs not yet in the build chain (noindex) |

Published PBQ pages: `../SEC+_PBQ/`

**Production preview:** `PBQ_Production/{slug}/{slug}.html` (e.g. `http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/acme-rag-hr-ai/acme-rag-hr-ai.html#acme-config`).

**Pending preview:** `pending/{slug}/{slug}.html` — four BCT standalone sims plus WLAN router PBQs; legacy `simulation-*.html` at this folder root redirect to `pending/`. Labs are linked from `SEC+_Training_Portal.html`.
