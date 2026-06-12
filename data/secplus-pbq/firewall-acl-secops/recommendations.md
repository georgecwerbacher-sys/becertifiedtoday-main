---
type: pbq-scenario-recommendations
exam: SY0-701
scenario: firewall-acl-secops
last_updated: 2026-06-04
---

# Firewall ACL — recommendations

## For learners

1. **Most specific permits first**, then **explicit deny** — matches “first match wins.”
2. Web tier: two rules (80 and 443) or one rule with port object — this lab uses **separate rows** for HTTP and HTTPS.
3. DB rule: source must be **10.0.0.10**, not ANY — only the web tier may query MySQL.
4. Row 4 is the **implicit deny** — DENY + ANY/ANY/ANY/ANY.

## For instructors

| Priority | Recommendation |
|----------|----------------|
| High | Draw three-tier diagram (Internet → Web → DB) before opening dropdowns. |
| Medium | Contrast with stateful firewall “established” — stem is static ACL focus. |
| Low | Optional follow-up MCQ: “What happens if rule 4 is ALLOW ANY?” |

## For product

- Single-section scenario — sidebar has one item; consider hiding sidebar when `sections.length === 1` (future build tweak).
- Good lead-magnet snippet for “Security+ firewall PBQ” ad groups.

## Maintenance

- Edit `sections/firewall-acl-config.html` → `npm run build:pbq-suite`.
