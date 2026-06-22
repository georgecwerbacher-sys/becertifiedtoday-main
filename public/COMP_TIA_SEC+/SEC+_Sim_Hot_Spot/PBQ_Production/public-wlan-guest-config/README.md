# SEC+ Public WLAN Guest Configuration

**SY0-701 PBQ · BCT lobby guest router**

Three-tab consumer router UI (same family as Director WLAN, with **Admin Username** on Router Security). Open guest SSID for lobby visitors; admin interface hardened separately.

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

**Status:** Production — chain #27, linked on `SEC+_Training_Portal.html` (PKI, TLS & Wireless).

## Chain

- **Previous:** [`../home-wlan-director-config/`](../home-wlan-director-config/home-wlan-director-config.html)
- **Next:** [`../mdm-enrollment-config/`](../mdm-enrollment-config/mdm-enrollment-config.html)

## Preview

http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/public-wlan-guest-config/public-wlan-guest-config.html

Rebuild after section edits: `npm run build:pbq-suite`
