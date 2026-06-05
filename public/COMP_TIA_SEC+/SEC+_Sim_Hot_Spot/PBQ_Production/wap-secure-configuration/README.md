# Wireless Access Point — Secure Configuration

SY0-701 PBQ: corporate WAP — WPA3-Enterprise, 802.1X, hidden SSID, guest isolation, 5 GHz channel.

## Section

| ID | Content |
|----|---------|
| `wap-secure-config` | Security/auth dropdowns, feature toggles, live preview |

## Answer key

| Setting | Value |
|---------|-------|
| Encryption | WPA3-Enterprise (SAE / 802.1X) |
| Authentication | 802.1X with RADIUS server (EAP-TLS also accepted) |
| SSID | Any corporate name (≥3 characters) |
| Band / channel | 5 GHz — Channel 149 (non-overlapping) |
| Broadcast SSID | OFF (hidden) |
| WPS | OFF |
| Guest network | ON (isolated) |

Rogue AP detection and management VLAN isolation: ON (shown in Show Answer; not required to pass Check).

## SY0-701 themes

- Wireless security — WPA3, 802.1X/RADIUS, WPS risks (1.4, 3.3)
- Guest network isolation and SSID broadcast control

## Chain

**Previous:** [Ubuntu 22.04 baseline hardening](../ubuntu-cis-hardening/ubuntu-cis-hardening.html) · **Next:** [Log Timeline Forensics](../log-timeline-forensics/log-timeline-forensics.html)

## Preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/wap-secure-configuration/wap-secure-configuration.html
```
