---
type: pbq-scenario-recommendations
exam: SY0-701
scenario: wap-secure-configuration
last_updated: 2026-06-05
---

# WAP Secure Configuration — recommendations

## For learners

1. **WPA3-Enterprise** beats WPA2-Personal/Enterprise and all legacy options (WEP, WPA/TKIP).
2. **802.1X with RADIUS** satisfies “enterprise-grade auth server”; EAP-TLS also accepted in grader.
3. **WPS defaults ON** in the sim — policy requires **OFF** (PIN brute-force risk).
4. **Broadcast SSID OFF** = hidden network; guest network **ON** = separate isolated VLAN/SSID.

## For instructors

| Priority | Recommendation |
|----------|----------------|
| High | Use live preview red/green to discuss why WPS + visible SSID fail policy. |
| Medium | Explain why 5 GHz Ch 149 vs 2.4 GHz for “least congested” stem. |
| Low | Note rogue AP + mgmt VLAN toggles (Show Answer enables; not required to pass). |

## For product

- End of current PBQ chain — good “wireless PBQ” landing for ads.
- Preview panel is clip-friendly for YouTube shorts.

## Maintenance

- Edit `sections/wap-secure-config.html` → `npm run build:pbq-suite`.
