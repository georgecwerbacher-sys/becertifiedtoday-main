# Sec+ Director and Administrator WLAN Setup

**SY0-701 PBQ · consumer router configuration**

Simulated router with three tabs (Wireless Settings, Router Security, Network Security). Configure WPA2, SSID, passphrase, admin login, and MAC filtering for the Director's phone.

## Answer key

| Tab | Setting | Correct value |
|-----|---------|---------------|
| Wireless | Wireless Status | Enable |
| Wireless | SSID | `No Illegal Downloads` (or equivalent naming illegal downloads) |
| Wireless | SSID Broadcast | Enabled |
| Wireless | Channel | auto |
| Wireless | WiFi Security | WPA2 |
| Wireless | WiFi Passphrase | `becertified2day_2026` |
| Router Security | Admin / Verify | `BCT_1234` |
| Network Security | MAC filtering | Enabled |
| Network Security | MAC Address | `28-ED-57-FD-A0-FE` |

**Status:** Production — chain #26, linked on `SEC+_Training_Portal.html` (PKI, TLS & Wireless).

## Chain

- **Previous:** [`../malware-infection-log-analysis/`](../malware-infection-log-analysis/malware-infection-log-analysis.html)
- **Next:** [`../public-wlan-guest-config/`](../public-wlan-guest-config/public-wlan-guest-config.html)

## Preview

http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/home-wlan-director-config/home-wlan-director-config.html

Rebuild after section edits: `npm run build:pbq-suite`
