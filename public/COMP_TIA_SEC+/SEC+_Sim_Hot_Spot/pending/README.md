# Security+ PBQ — pending

Staged scenarios **not** on [`SEC+_Training_Portal.html`](../../SEC+_Training_Portal.html) yet — review here before portal + production promotion.

Registered chain labs live under [`../PBQ_Production/`](../PBQ_Production/) (`scripts/build-pbq-production-suite.py`). BCT standalone sims on the portal also live in `PBQ_Production/` as single-page HTML (not in the build chain).

Legacy `SEC+_Sim_Hot_Spot/simulation-*.html` URLs redirect to `PBQ_Production/` for shipped BCT sims.

## Review queue (not on portal)

| Folder | Description | Preview |
|--------|-------------|---------|
| [`home-wlan-director-config/`](home-wlan-director-config/) | Director home router — WPA2, MAC filter, admin password | [Open](home-wlan-director-config/home-wlan-director-config.html) |
| [`public-wlan-guest-config/`](public-wlan-guest-config/) | BCT lobby guest WLAN — open SSID, channel 11, admin username | [Open](public-wlan-guest-config/public-wlan-guest-config.html) |
| [`mdm-enrollment-config/`](mdm-enrollment-config/) | Acme MDM — iOS compliance, app restrictions, ADE | [Open](mdm-enrollment-config/mdm-enrollment-config.html) |
| [`siem-alert-settings-config/`](siem-alert-settings-config/) | SIEM failed-login alert — sliding window, email notify | [Open](siem-alert-settings-config/siem-alert-settings-config.html) |
| [`network-protocols-matching/`](network-protocols-matching/) | Match protocols to security functions (drag-and-drop) | [Open](network-protocols-matching/network-protocols-matching.html) |
| [`site-to-site-vpn-config/`](site-to-site-vpn-config/) | Site-to-site VPN Phase 1 &amp; 2 dual-gateway config | [Open](site-to-site-vpn-config/site-to-site-vpn-config.html) |
| [`web-app-subnet-zoning/`](web-app-subnet-zoning/) | Web app subnet zoning — drag-and-drop tiers | [Open](web-app-subnet-zoning/web-app-subnet-zoning.html) |

Pending chain: … → site-to-site VPN → **web app subnet zoning**.

Production PBQ chain (25 labs) ends at [`../PBQ_Production/malware-infection-log-analysis/`](../PBQ_Production/malware-infection-log-analysis/malware-infection-log-analysis.html).

## BCT standalone sims (on portal → `PBQ_Production/`)

| Folder | Preview |
|--------|---------|
| [`../PBQ_Production/dark-web-account-protection/`](../PBQ_Production/dark-web-account-protection/dark-web-account-protection.html) | Dark web credential IR |
| [`../PBQ_Production/malware-outbreak-classification/`](../PBQ_Production/malware-outbreak-classification/malware-outbreak-classification.html) | Malware outbreak classification |
| [`../PBQ_Production/secure-web-architecture-openssl/`](../PBQ_Production/secure-web-architecture-openssl/secure-web-architecture-openssl.html) | Secure web & OpenSSL |
| [`../PBQ_Production/vpc-payment-architecture/`](../PBQ_Production/vpc-payment-architecture/vpc-payment-architecture.html) | VPC payment network |

## Reference only

| File | Role |
|------|------|
| `TEMPLATE-dragdrop.html` | Copy skeleton for new drag-and-drop PBQs |

## Production preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/governance/governance.html
```
