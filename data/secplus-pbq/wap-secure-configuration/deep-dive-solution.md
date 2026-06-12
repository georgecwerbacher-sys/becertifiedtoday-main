---
type: pbq-scenario-solution
exam: SY0-701
scenario: wap-secure-configuration
last_updated: 2026-06-05
---

# WAP Secure Configuration — deep dive solution

> Corporate WAP — WPA3-Enterprise, hidden SSID, guest isolation, 5 GHz.

---

## Correct settings

| Setting | Value |
|---------|-------|
| Encryption | WPA3-Enterprise (SAE / 802.1X) |
| Authentication | 802.1X with RADIUS server *(EAP-TLS also accepted)* |
| SSID name | Any corporate name (≥3 characters), e.g. `BeCertifiedToday_WiFi` |
| Band / channel | 5 GHz — Channel 149 (non-overlapping) |
| Broadcast SSID | **OFF** (hidden) |
| WPS | **OFF** |
| Guest network | **ON** (isolated) |

**Show Answer also enables:** Rogue AP detection ON, Management VLAN isolation ON.

---

## Why each policy item

| Requirement | Setting |
|-------------|---------|
| Strongest encryption | WPA3-Enterprise — deprecates WEP/WPA/TKIP |
| Enterprise auth server | 802.1X + RADIUS (centralized identity) |
| No legacy insecure protocols | WPS off; no WEP/WPA-TKIP |
| Hidden corporate SSID | Broadcast SSID off |
| Isolated guest network | Guest network on |
| Least congested 5 GHz | Channel 149 (upper UNII-3; non-overlapping in sim) |

---

## Distractor analysis

| Option | Why wrong |
|--------|-----------|
| WEP / WPA (TKIP) | Legacy, broken crypto |
| WPA2-Personal (PSK) | No enterprise RADIUS; shared key |
| Open (no auth) | No authentication |
| 2.4 GHz channels | Stem asks for 5 GHz |
| Broadcast ON | Violates hidden SSID policy |
| WPS ON | PIN vulnerability; legacy pairing |
| Guest OFF | Policy requires isolated guest network |

---

## Common mistakes

| Mistake | Result |
|---------|--------|
| WPA2-Enterprise only | Not the **strongest available** in dropdown |
| PSK for corporate LAN | Not enterprise-grade |
| Channel 36 when stem says “least congested” | Either 5 GHz may work; grader keys **149** |
| Forgetting to toggle WPS off | Preview shows red “Enabled (ON)” |

---

## Exam takeaway

Wireless PBQs: **encryption generation** + **authentication model** + **operational hardening** (WPS, SSID broadcast, guest segmentation) — read the policy bullet list as a checklist.
