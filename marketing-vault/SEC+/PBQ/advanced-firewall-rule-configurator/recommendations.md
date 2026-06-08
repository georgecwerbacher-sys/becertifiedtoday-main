---
type: pbq-scenario-recommendations
exam: SY0-701
scenario: advanced-firewall-rule-configurator
last_updated: 2026-06-08
---

# Advanced Firewall Rule Configurator: recommendations

## Implementation status (2026-06-08)

| Item | Status |
|------|--------|
| SY0-701 objective badge (3.3 · 4.1) | Done |
| Topology exhibit first, centered layout | Done |
| Suite instructions (no blue-tile exhibit wording) | Done |
| Step-by-step deep dive | Done |
| Security+ practice portal listing | Done (Simulation bank 2) |
| Writing rules pass (no em/en dashes in guest copy) | Done |
| First-attempt rule-order hint | Done |

## For learners

1. Rules **1 through 4** can be in any order. **Deny-all must be last**.
2. Use **OUT** + **UDP 53** for DNS. A common miss is marking DNS as inbound.
3. SSH source must be **10.0.0.0/24**, not ANY.
4. Telnet deny can use **ANY** destination. It blocks port 23 from any source.

## For instructors

| Priority | Recommendation |
|----------|----------------|
| High | Contrast with [[../firewall-acl-secops/notes|Firewall ACL SecOps]]: dropdown-only vs free-text CIDR + direction. |
| Medium | Walk through the activity log to reinforce evaluation order. |
| Low | Ask what breaks if deny-all is rule 1. |

## For product

- Strong follow-on to SIEM scenario in the chain (detect, contain, harden perimeter).
- Ad keyword angle: "Security+ firewall PBQ ACL direction".
- Portal: listed under **Simulation bank 2** with Zero Trust and Attack ID Remediation.

## Maintenance

- Edit `sections/advanced-firewall-config.html` → `python3 scripts/build-pbq-production-suite.py`.
- Refresh [[deep-dive-solution|deep dive]] after rule-key or topology changes.
