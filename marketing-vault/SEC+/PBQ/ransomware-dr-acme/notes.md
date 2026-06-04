---
type: pbq-scenario-notes
exam: SY0-701
scenario: ransomware-dr-acme
title: Ransomware DR — Acme Corp
status: production
last_updated: 2026-06-04
---

# Ransomware DR — notes

## Scenario

Ransomware encrypts Acme Corp primary DC. CISO invokes DR under:

- **RTO (SLA):** 4 hours
- **Current RPO:** 6 hours (last verified backup age)
- **Budget:** $2M annual IT
- **Attack:** Ransomware

## Sections

| ID | Part |
|----|------|
| `dr-overview` | Constraint metric cards |
| `dr-part1-order` | 8-step drag-and-drop activation order |
| `dr-part2-targets` | RTO/RPO/backup freq + warm site + why not hot |
| `dr-part3-tradeoffs` | Ransom / CDP / eradication MCQs |

**Previous:** [[../firewall-acl-secops/notes|Firewall ACL]]

## Preview

http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/ransomware-dr-acme/ransomware-dr-acme.html

→ [[recommendations]] · [[deep-dive-solution]]
