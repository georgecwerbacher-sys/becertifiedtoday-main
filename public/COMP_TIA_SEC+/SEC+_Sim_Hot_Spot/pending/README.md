# Security+ PBQ — pending

Staged scenarios **not** on [`SEC+_Training_Portal.html`](../../SEC+_Training_Portal.html) yet — review here before portal + production promotion.

Registered chain labs live under [`../PBQ_Production/`](../PBQ_Production/) (`scripts/build-pbq-production-suite.py`). BCT standalone sims on the portal also live in `PBQ_Production/` as single-page HTML (not in the build chain).

Legacy `SEC+_Sim_Hot_Spot/simulation-*.html` URLs redirect to `PBQ_Production/` for shipped BCT sims.

## Review queue (not on portal)

| Folder | Description | Preview |
|--------|-------------|---------|
| [`siem-alert-settings-config/`](siem-alert-settings-config/) | SIEM failed-login alert — sliding window, email notify | [Open](siem-alert-settings-config/siem-alert-settings-config.html) |

Production PBQ chain (34 labs) ends at [`../PBQ_Production/vpc-payment-architecture/`](../PBQ_Production/vpc-payment-architecture/vpc-payment-architecture.html).

## BCT standalone sims (on portal → `PBQ_Production/`)

| Folder | Preview |
|--------|---------|
| [`../PBQ_Production/secure-web-architecture-openssl/`](../PBQ_Production/secure-web-architecture-openssl/secure-web-architecture-openssl.html) | Secure web & OpenSSL |

## Reference only

| File | Role |
|------|------|
| `TEMPLATE-dragdrop.html` | Copy skeleton for new drag-and-drop PBQs |

## Production preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/governance/governance.html
```
