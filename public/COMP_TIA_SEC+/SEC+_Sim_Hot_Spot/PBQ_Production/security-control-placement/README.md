# Network Diagram — Security Control Placement

SY0-701 PBQ: drag security controls onto a three-zone network diagram (Internet, DMZ, Internal).

## Section

| ID | Content |
|----|---------|
| `sec-control-placement` | Control bank + labeled zone slots |

## Answer key

| Slot | Control | Token ID |
|------|---------|----------|
| Between Internet ↔ DMZ | Perimeter Firewall | `perimeter-firewall` |
| Protect Web Server (HTTP attacks) | WAF | `waf` |
| Detect intrusions in DMZ | Network IDS | `network-ids` |
| Decoy to lure attackers | Honeypot | `honeypot` |
| Between DMZ ↔ Internal | Internal Firewall | `internal-firewall` |
| Endpoint access control | NAC | `nac` |
| Log aggregation & alerting | SIEM | `siem` |

**Unused:** Proxy Server (optional — leave in bank).

## SY0-701 themes

- Network segmentation and defense in depth (3.3)
- Security control placement — firewall, WAF, IDS, NAC, SIEM (3.2, 4.1)

## Chain

**Previous:** [Advanced Firewall Rule Configurator](../advanced-firewall-rule-configurator/advanced-firewall-rule-configurator.html)

## Preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/security-control-placement/security-control-placement.html
```
