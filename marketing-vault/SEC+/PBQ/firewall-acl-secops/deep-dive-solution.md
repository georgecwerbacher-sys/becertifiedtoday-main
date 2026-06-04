---
type: pbq-scenario-solution
exam: SY0-701
scenario: firewall-acl-secops
last_updated: 2026-06-04
---

# Firewall ACL — deep dive solution

> Tiered ACL / least privilege — CompTIA Security+ operations and network hardening themes.

---

## Correct rule set

| # | Action | Protocol | Source | Destination | Port |
|---|--------|----------|--------|-------------|------|
| **1** | ALLOW | TCP | ANY | 10.0.0.10 (Web) | 80 (HTTP) |
| **2** | ALLOW | TCP | ANY | 10.0.0.10 (Web) | 443 (HTTPS) |
| **3** | ALLOW | TCP | 10.0.0.10 (Web) | 10.0.0.20 (DB) | 3306 (MySQL) |
| **4** | DENY | ANY | ANY | ANY | ANY |

---

## Why this order works

1. **Rules 1–2** satisfy “web server may accept HTTP/HTTPS from any source.” TCP is required for HTTP/S. Destination must be the web host, not ANY.
2. **Rule 3** restricts database access to the application tier only — prevents direct inbound MySQL from the Internet or other internal hosts.
3. **Rule 4** implements **default deny** for all other inbound flows. Without it, unmatched traffic might be handled by an implicit permit depending on platform — the policy requires explicit denial.

**First match wins:** If rule 4 (DENY ANY) were placed at the top, legitimate web traffic would never be evaluated against permit rules.

---

## Common mistakes

| Mistake | Result |
|---------|--------|
| ALLOW 3306 from ANY to DB | Violates “only from web server” |
| Single rule “ALLOW TCP ANY → 10.0.0.10 ANY ports” | Over-permissive if ANY port is offered |
| DENY before permits | Blocks required services |
| Row 4 ALLOW | Leaves inbound path open |
| UDP/ICMP on web rules | Policy specifies HTTP/HTTPS (TCP 80/443) |

---

## Exam takeaway

**Explicit permit → explicit deny**, most specific sources and destinations first, align **protocol and port** with the service named in the stem.

---

## Quick reference

```
1: ALLOW  TCP  ANY         → 10.0.0.10  80
2: ALLOW  TCP  ANY         → 10.0.0.10  443
3: ALLOW  TCP  10.0.0.10   → 10.0.0.20  3306
4: DENY   ANY  ANY         → ANY        ANY
```
