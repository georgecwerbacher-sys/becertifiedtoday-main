# Security+ simulations and PBQ workspace

| Path | Purpose |
|------|---------|
| `simulation-*.html`, `hotspot-*.html` | Published simulations / hot spots |
| `reports/` | In-sim report pages (noindex) |
| `images/` | Shared exhibit assets |
| **`PBQ_Production/`** | **New** PBQ scenarios in development (noindex) |
| `pending/` | Legacy staged PBQ bank for reference (noindex) |

Published PBQ pages: `../SEC+_PBQ/`

Preview: each scenario is `PBQ_Production/{slug}/{slug}.html` (e.g. `http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/acme-rag-hr-ai/acme-rag-hr-ai.html#acme-config`). Four published sims live in the same tree (`dark-web-account-protection`, `malware-outbreak-classification`, `secure-web-architecture-openssl`, `vpc-payment-architecture`); legacy `simulation-*.html` at this folder root redirect there. Labs are linked from `SEC+_Training_Portal.html`.
