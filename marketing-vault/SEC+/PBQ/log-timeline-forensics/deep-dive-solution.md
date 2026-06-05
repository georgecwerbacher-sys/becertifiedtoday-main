---
type: pbq-scenario-solution
exam: SY0-701
scenario: log-timeline-forensics
last_updated: 2026-06-05
---

# Log Timeline Forensics — deep dive solution

> Reorder six SSH auth log snippets from brute-force attempts through privilege escalation and persistence.

---

## Correct answer

Chronological order: failed-login → multiple-retries → successful-login → sudo-escalation → new-user → cron-job

---

## Why it matters (exam lens)

**2.4** log analysis · **2.5** incident response timeline

---

## Distractor patterns

Review wrong choices in the live page — each MCQ/fill-in distractor targets a common SY0-701 misconception (wrong control order, wrong framework scope, or wrong IR phase).

---

## Related labs

Pair with [[../ubuntu-ssh-breach-hardening/notes|Ubuntu SSH breach]] — same narrative, different skill (ordering vs hardening).

---

## Source

Ported from `public/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/pending/log-timeline-forensics.html` (2026-06-05).
