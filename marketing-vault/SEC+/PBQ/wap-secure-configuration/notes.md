---
type: pbq-scenario-notes
exam: SY0-701
scenario: wap-secure-configuration
title: Wireless Access Point — Secure Configuration
status: production
last_updated: 2026-06-05
---

# WAP Secure Configuration — notes

## What this lab tests

Configure a **corporate wireless access point** per security policy:

- Strongest encryption (**WPA3-Enterprise**) and **enterprise auth** (802.1X/RADIUS)
- No legacy protocols (**WPS off**)
- **Hidden SSID** (broadcast off)
- **Isolated guest network**
- **5 GHz channel 149** (least congested non-overlapping option in sim)

## SY0-701 alignment

| Theme | Coverage |
|-------|----------|
| **1.4** Wireless crypto | WPA3, 802.1X, WPS risks |
| **3.3** Segmentation | Guest network isolation |
| **4.1** Secure configuration | SSID broadcast, channel selection |

## Page structure

| Section ID | Content |
|------------|---------|
| `wap-secure-config` | Security/auth fields, feature toggles, live preview |

**Previous:** [[../ubuntu-cis-hardening/notes|Ubuntu CIS]] · End of chain.

## Local preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/wap-secure-configuration/wap-secure-configuration.html
```

→ [[recommendations]] · [[deep-dive-solution]]
