# Public WLAN — Guest Wi‑Fi configuration

**SY0-701 PBQ · Scenario #23**

Open guest WLAN for BeCertifiedToday lobby visitors. Same three-tab router UI as `home-wlan-director-config`, with **Admin Username** on Router Security.

## Answer key

| Tab | Setting | Correct value |
|-----|---------|---------------|
| Wireless | Wireless Status | Enable |
| Wireless | SSID | `Free BCT Guest WiFi` |
| Wireless | SSID Broadcast | Enabled |
| Wireless | Channel | **11** (non-overlapping with 1, 4, 6) |
| Wireless | WiFi Security | Disable (open — no guest password) |
| Wireless | WiFi Passphrase | *(leave empty)* |
| Router Security | Admin Username | `employeesonly` |
| Router Security | Admin / Verify password | `nu2XAwGUmw4e0KaR8PmAh` |
| Network Security | MAC filtering | Disabled |

**Status:** Pending — not in `PBQ_Production` build chain.

## Pending chain

- **Previous:** `../home-wlan-director-config/`
- **Next:** *(none)*

## Preview

http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/pending/public-wlan-guest-config/public-wlan-guest-config.html
