# Security+ PBQ — pending

Staged scenarios **not** in the `PBQ_Production` build chain (`scripts/build-pbq-production-suite.py`). Ship to production when ready; vault notes stay in `data/secplus-pbq/{slug}/`.

Legacy `SEC+_Sim_Hot_Spot/simulation-*.html` URLs redirect here for the four BCT standalone sims below.

## BCT standalone simulations

| Folder | Description | Preview |
|--------|-------------|---------|
| [`dark-web-account-protection/`](dark-web-account-protection/) | Dark web credential exposure IR | [Open](dark-web-account-protection/dark-web-account-protection.html) |
| [`malware-outbreak-classification/`](malware-outbreak-classification/) | AV log timeline — outbreak type | [Open](malware-outbreak-classification/malware-outbreak-classification.html) |
| [`secure-web-architecture-openssl/`](secure-web-architecture-openssl/) | TLS, ciphers, OpenSSL practices | [Open](secure-web-architecture-openssl/secure-web-architecture-openssl.html) |
| [`vpc-payment-architecture/`](vpc-payment-architecture/) | PCI VPC segmentation diagram | [Open](vpc-payment-architecture/vpc-payment-architecture.html) |

## WLAN router PBQs (2026-06-22)

| Folder | Description | Preview |
|--------|-------------|---------|
| [`home-wlan-director-config/`](home-wlan-director-config/) | Director home router — WPA2, MAC filter, admin password | [Open](home-wlan-director-config/home-wlan-director-config.html) |
| [`public-wlan-guest-config/`](public-wlan-guest-config/) | BCT lobby guest WLAN — open SSID, channel 11, admin username | [Open](public-wlan-guest-config/public-wlan-guest-config.html) |
| [`cloud-waf-setup/`](cloud-waf-setup/) | *(shipped — see [production](../PBQ_Production/cloud-waf-setup/))* | [Production](../PBQ_Production/cloud-waf-setup/cloud-waf-setup.html) |
| [`mdm-enrollment-config/`](mdm-enrollment-config/) | Acme MDM — iOS compliance, app restrictions, ADE | [Open](mdm-enrollment-config/mdm-enrollment-config.html) |
| [`siem-alert-settings-config/`](siem-alert-settings-config/) | SIEM failed-login alert — sliding window, email notify | [Open](siem-alert-settings-config/siem-alert-settings-config.html) |
| [`network-protocols-matching/`](network-protocols-matching/) | Match protocols to security functions (drag-and-drop) | [Open](network-protocols-matching/network-protocols-matching.html) |
| [`incident-response-matching/`](incident-response-matching/) | Match IR phases to actions (drag-and-drop) | [Open](incident-response-matching/incident-response-matching.html) |
| [`cryptographic-algorithms-matching/`](cryptographic-algorithms-matching/) | Match crypto algorithms to use cases (drag-and-drop) | [Open](cryptographic-algorithms-matching/cryptographic-algorithms-matching.html) |
| [`site-to-site-vpn-config/`](site-to-site-vpn-config/) | Site-to-site VPN Phase 1 &amp; 2 dual-gateway config | [Open](site-to-site-vpn-config/site-to-site-vpn-config.html) |
| [`malware-infection-log-analysis/`](malware-infection-log-analysis/) | Malware log triage — source / infected / clean | [Open](malware-infection-log-analysis/malware-infection-log-analysis.html) |
| [`web-app-subnet-zoning/`](web-app-subnet-zoning/) | Web app subnet zoning — drag-and-drop tiers | [Open](web-app-subnet-zoning/web-app-subnet-zoning.html) |

Pending chain: … → site-to-site VPN → malware log analysis → **web app subnet zoning**.

Production PBQ chain (22 labs) ends at [`../PBQ_Production/cloud-waf-setup/`](../PBQ_Production/cloud-waf-setup/cloud-waf-setup.html).

## Reference only

| File | Role |
|------|------|
| `TEMPLATE-dragdrop.html` | Copy skeleton for new drag-and-drop PBQs |

## Production preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/governance/governance.html
```
