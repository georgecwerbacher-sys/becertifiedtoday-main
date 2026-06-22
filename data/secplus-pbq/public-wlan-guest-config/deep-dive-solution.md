---
type: pbq-scenario-solution
exam: SY0-701
scenario: public-wlan-guest-config
last_updated: 2026-06-22
---

# Public WLAN guest — deep dive solution

Configure all three router tabs — **Wireless Settings**, **Router Security**, and **Network Security** — for BeCertifiedToday's lobby guest network.

> Original BCT scenario; verify against SY0-701 wireless objectives.

---

## Correct configuration

| Field | Value | Why |
|-------|-------|-----|
| Wireless Status | **Enable** | Guest network must be active |
| SSID | **Free BCT Guest WiFi** | Policy name for lobby guests |
| SSID Broadcast | **Enabled** | Anyone must see and join the network |
| Channel | **11** | In 2.4 GHz, channels 1/4/6 overlap each other; **11** is non-overlapping with 1 and 6 |
| WiFi Security | **Disable** | No password prompt for guests (open WLAN) |
| Passphrase | *(empty)* | Not used when security is disabled |
| Admin Username | **employeesonly** | Restrict router management |
| Admin Password | **nu2XAwGUmw4e0KaR8PmAh** | Strong admin credential (verify both fields) |
| MAC filtering | **Disabled** | Open guest access — no allow-list |

---

## Channel overlap (2.4 GHz)

| In-use channels | Overlap risk on |
|-----------------|-----------------|
| 1 | 1–5 |
| 4 | 2–8 |
| 6 | 4–8 |

**Channel 11** avoids overlap with 1, 4, and 6 — standard exam answer. Channels **9** or **12** may also work in some models, but **11** is the conventional choice.

---

## Distractor analysis

| Wrong choice | Why it fails |
|--------------|--------------|
| WPA/WPA2/WEP | Guests would need a passphrase |
| Hidden SSID (broadcast off) | Violates “anyone can connect” visibility |
| Channels 1, 4, 6 (or auto picking them) | Overlaps existing networks |
| MAC filtering enabled | Blocks open guest access model |
| Default admin credentials | Stem requires new username/password |

---

## Security note

Open guest WLANs are common in lobbies but carry risk (no over-the-air encryption). The PBQ tests **separation**: guest data plane open, **admin interface** protected with unique credentials.
