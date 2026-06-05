---
type: pbq-scenario-notes
exam: SY0-701
scenario: advanced-firewall-rule-configurator
title: Advanced Firewall Rule Configurator
status: production
last_updated: 2026-06-05
---

# Advanced Firewall Rule Configurator — notes

## What this lab tests

Configure a **perimeter firewall** for Acme Corp with **inbound/outbound direction**, **CIDR notation**, dynamic rule rows, and an **implicit deny-all** last rule:

- HTTPS inbound to web server `192.168.1.10`
- SSH inbound from mgmt subnet `10.0.0.0/24` only
- Telnet denied inbound
- DNS outbound from `192.168.1.0/24`
- Explicit deny-all as final rule

## SY0-701 alignment

| Theme | Coverage |
|-------|----------|
| **3.3** Network security | ACL order, segmentation, least privilege |
| **4.1** Secure baselines | Explicit deny, service-specific permits |

## Page structure

| Section ID | Content |
|------------|---------|
| `advanced-firewall-config` | Policy checklist, topology, ACL table, activity log |

**Previous:** [[../siem-ransomware-mitre/notes|SIEM MITRE]] · **Next:** [[../security-control-placement/notes|Control placement]]

## Local preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/advanced-firewall-rule-configurator/advanced-firewall-rule-configurator.html
```

→ [[recommendations]] · [[deep-dive-solution]]
