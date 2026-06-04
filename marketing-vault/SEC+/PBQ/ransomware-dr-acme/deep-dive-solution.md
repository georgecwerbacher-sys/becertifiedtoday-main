---
type: pbq-scenario-solution
exam: SY0-701
scenario: ransomware-dr-acme
last_updated: 2026-06-04
---

# Ransomware DR — deep dive solution

## Part 1 — DR activation order

| Step | Action |
|------|--------|
| 1 | Activate DR team |
| 2 | Isolate affected systems |
| 3 | Assess scope |
| 4 | Declare disaster |
| 5 | Verify backup integrity |
| 6 | Failover to warm DR site |
| 7 | Restore from verified backup |
| 8 | Validate systems & lessons learned |

**Logic:** Contain before restore; verify backups are clean; failover infrastructure before data load; validate last.

## Part 2 — Targets

| Field | Answer |
|-------|--------|
| RTO | **4 hours** (match SLA) |
| RPO | **6 hours** (matches backup age) |
| Backup frequency | **Every 4 hours or less** (tighten RPO forward) |
| DR site | **Warm** (2–4 hr RTO, fits budget) |
| Why not hot | **Both** — $1.5M+/yr consumes budget; 4-hr RTO does not need real-time mirror |

## Part 3 — MCQs (all **B**)

**Q1:** Paying ransom funds criminals, no key guarantee, invites repeat attacks.

**Q2:** **CDP / synchronous replication** → near-zero RPO.

**Q3:** **Isolate, re-image, close attack vector**, then restore clean backup — prevents immediate reinfection.

## Quick reference

```
Order: team → isolate → assess → declare → verify backup → failover → restore → validate
Part2: 4h | 6h | 4h backups | warm | both
Part3: B | B | B
```
