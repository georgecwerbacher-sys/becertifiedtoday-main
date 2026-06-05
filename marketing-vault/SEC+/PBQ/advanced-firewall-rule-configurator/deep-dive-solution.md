---
type: pbq-scenario-solution
exam: SY0-701
scenario: advanced-firewall-rule-configurator
last_updated: 2026-06-05
---

# Advanced Firewall Rule Configurator — deep dive solution

> Perimeter ACL with inbound/outbound rules and explicit deny-all.

---

## Correct rule set

| # | Dir | Proto | Source | Destination | Port | Action |
|---|-----|-------|--------|-------------|------|--------|
| 1 | IN | TCP | ANY | 192.168.1.10 | 443 | ALLOW |
| 2 | IN | TCP | 10.0.0.0/24 | 192.168.1.10 | 22 | ALLOW |
| 3 | IN | TCP | ANY | ANY | 23 | DENY |
| 4 | OUT | UDP | 192.168.1.0/24 | ANY | 53 | ALLOW |
| 5 | ANY | ANY | ANY | ANY | ANY | DENY |

Rules 1–4 may appear in any order; **rule 5 must be last**.

---

## Why each rule exists

1. **HTTPS permit** — public web service on the internal web host; TCP 443 from any source to the specific server IP.
2. **SSH permit** — administrative access restricted to the management subnet only.
3. **Telnet deny** — legacy cleartext protocol blocked inbound before a broad permit could allow it.
4. **DNS outbound** — internal clients resolve names; UDP 53 from the internal LAN segment.
5. **Deny-all** — default-deny catch-all; must be evaluated after all explicit permits/denies.

---

## Common mistakes

| Mistake | Result |
|---------|--------|
| SSH from ANY | Violates mgmt-subnet-only policy |
| DNS rule set to IN | Wrong direction for client DNS queries leaving the LAN |
| Deny-all not last | Later permits could override the catch-all intent |
| Forgetting Telnet deny | Port 23 might fall through to deny-all only (still blocked) but policy asks for explicit deny |
| Using /32 instead of host IP | Accept CIDR `192.168.1.10/32` only if grader allows — key uses host address |

---

## Exam takeaway

**First match wins** — place specific permits and explicit denies before the catch-all; use **direction** (IN/OUT) correctly for asymmetric flows.

---

## Quick reference

```
ALLOW  IN  TCP  ANY           → 192.168.1.10     443
ALLOW  IN  TCP  10.0.0.0/24   → 192.168.1.10     22
DENY   IN  TCP  ANY           → ANY              23
ALLOW  OUT UDP  192.168.1.0/24 → ANY             53
DENY   ANY ANY  ANY           → ANY              ANY   (last)
```
