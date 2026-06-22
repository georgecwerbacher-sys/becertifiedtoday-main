---
type: pbq-scenario-notes
exam: SY0-701
scenario: public-wlan-guest-config
last_updated: 2026-06-22
---

# Public WLAN — Guest Wi‑Fi (BCT lobby)

BCT adaptation of common Security+ **public/guest WLAN** PBQs (airport terminal pattern). Open SSID for visitors; admin plane hardened separately.

**Status:** Production — chain #27, portal (PKI, TLS & Wireless).

## SY0-701 mapping

- **1.2** — wireless security modes (open vs WPA2)
- **3.3** — 2.4 GHz channel overlap (avoid 1, 4, 6 → channel 11)
- **4.6** — router admin credentials; MAC filtering off for open guest access
