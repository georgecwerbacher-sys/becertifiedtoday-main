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

WLAN pair chain: home WLAN → public WLAN.

Production PBQ chain (21 labs) ends at [`../PBQ_Production/governance/`](../PBQ_Production/governance/governance.html).

## Reference only

| File | Role |
|------|------|
| `TEMPLATE-dragdrop.html` | Copy skeleton for new drag-and-drop PBQs |

## Production preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/governance/governance.html
```
