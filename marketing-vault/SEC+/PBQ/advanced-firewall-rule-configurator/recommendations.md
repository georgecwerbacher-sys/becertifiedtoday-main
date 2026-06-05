---
type: pbq-scenario-recommendations
exam: SY0-701
scenario: advanced-firewall-rule-configurator
last_updated: 2026-06-05
---

# Advanced Firewall Rule Configurator — recommendations

## For learners

1. Rules **1–4** can be in any order; **deny-all must be last**.
2. Use **OUT** + **UDP 53** for DNS — a common miss is marking DNS as inbound.
3. SSH source must be **10.0.0.0/24**, not ANY.
4. Telnet deny can use **ANY** destination — it blocks port 23 from any source.

## For instructors

| Priority | Recommendation |
|----------|----------------|
| High | Contrast with [[../firewall-acl-secops/notes|Firewall ACL SecOps]] — dropdown-only vs free-text CIDR + direction. |
| Medium | Walk through activity log to reinforce evaluation order. |
| Low | Optional: ask what breaks if deny-all is rule 1. |

## For product

- Strong follow-on to SIEM scenario in the chain (detect → contain → harden perimeter).
- Ad keyword angle: “Security+ firewall PBQ ACL direction”.

## Maintenance

- Edit `sections/advanced-firewall-config.html` → `npm run build:pbq-suite`.
