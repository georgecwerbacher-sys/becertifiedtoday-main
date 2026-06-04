# Firewall ACL Configuration — Security Operations

SY0-701 PBQ: top-down firewall ACL rules for web (10.0.0.10) and database (10.0.0.20) tier.

## Section

| ID | Content |
|----|---------|
| `firewall-acl-config` | Policy scenario + 4-rule ACL table |

## Answer key

| # | Action | Protocol | Source | Destination | Port |
|---|--------|----------|--------|-------------|------|
| 1 | ALLOW | TCP | ANY | 10.0.0.10 (Web) | 80 |
| 2 | ALLOW | TCP | ANY | 10.0.0.10 (Web) | 443 |
| 3 | ALLOW | TCP | 10.0.0.10 (Web) | 10.0.0.20 (DB) | 3306 |
| 4 | DENY | ANY | ANY | ANY | ANY |

## Chain

**Previous:** [Ubuntu SSH breach hardening](../ubuntu-ssh-breach-hardening/ubuntu-ssh-breach-hardening.html)

## Preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/firewall-acl-secops/firewall-acl-secops.html
```
