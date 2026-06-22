---
type: pbq-scenario-solution
exam: SY0-701
scenario: home-wlan-director-config
last_updated: 2026-06-22
---

# Home WLAN — Director router — deep dive solution

> Consumer home-router PBQ. Original BCT scenario; verify against CompTIA SY0-701 wireless objectives — not exam dumps.

---

## Correct configuration

| Tab | Field | Value | Why |
|-----|-------|-------|-----|
| Wireless | Status | **Enable** | Stem requires an active WLAN |
| Wireless | SSID | **No Illegal Downloads** | Policy message; visible naming |
| Wireless | SSID Broadcast | **Enabled** | Must be visible to devices |
| Wireless | Channel | **auto** | Router selects channel — avoid fixed manual overlap |
| Wireless | Security | **WPA2** | Strongest option on this UI (WEP/WPA are legacy) |
| Wireless | Passphrase | **becertified2day_2026** | Assigned key — length/complexity |
| Router | Admin password | **BCT_1234** (both fields) | Protects management plane |
| Network | MAC filtering | **Enabled** | Allow-list only the Director phone |
| Network | MAC | **28-ED-57-FD-A0-FE** | Director smartphone OUI |

---

## Distractor analysis

| Wrong choice | Why it fails |
|--------------|--------------|
| Disable wireless | Violates “Wi‑Fi enabled” |
| WEP / WPA / Disable security | Weak or open — not “best possible” on this router |
| Fixed channel 1–12 | Stem requires auto |
| SSID broadcast Disabled | Hidden SSID — not visible to devices |
| MAC filtering Disabled | Any client could associate |
| Wrong MAC | Opens network to other devices |
| Mismatched admin verify | Router rejects or leaves weak config |

---

## Exam tips

- On consumer-router PBQs, **WPA2** (or WPA3 when offered) beats WPA/WEP.
- **MAC filtering** is a supplement — not a substitute for WPA2, but stems often require it for a single known device.
- **Auto channel** avoids manual interference mistakes; fixed channels are traps when the stem says “chosen by the router.”
