# Advanced Firewall Rule Configurator

SY0-701 PBQ: perimeter firewall ACL rules with inbound/outbound direction, CIDR notation, and explicit deny-all.

## Section

| ID | Content |
|----|---------|
| `advanced-firewall-config` | Policy checklist, topology, dynamic ACL table, activity log |

## Answer key

| # | Direction | Protocol | Source | Destination | Port | Action |
|---|-----------|----------|--------|-------------|------|--------|
| 1 | IN | TCP | ANY | 192.168.1.10 | 443 | ALLOW |
| 2 | IN | TCP | 10.0.0.0/24 | 192.168.1.10 | 22 | ALLOW |
| 3 | IN | TCP | ANY | ANY | 23 | DENY |
| 4 | OUT | UDP | 192.168.1.0/24 | ANY | 53 | ALLOW |
| 5 | ANY | ANY | ANY | ANY | ANY | DENY |

Rules 1–4 may appear in any order; rule 5 (implicit deny-all) must be last.

## SY0-701 themes

- Network segmentation and firewall rule design (3.3)
- Secure configuration and least privilege (4.1)
- ACL evaluation order — top-down, first match wins

## Chain

**Previous:** [SIEM ransomware — Sigma & MITRE](../siem-ransomware-mitre/siem-ransomware-mitre.html)

## Preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/advanced-firewall-rule-configurator/advanced-firewall-rule-configurator.html
```
