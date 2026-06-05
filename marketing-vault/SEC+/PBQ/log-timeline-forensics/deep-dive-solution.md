---
type: pbq-scenario-solution
exam: SY0-701
scenario: log-timeline-forensics
last_updated: 2026-06-05
---

# Log Timeline Forensics — deep dive solution

> Reorder six SSH auth log snippets from brute-force attempts through privilege escalation and persistence.

---

## Step 1 — Read every snippet before you drag

Open each token in the bank and note the **actor**, **action**, and **artifact**:

| Token | Log line (summary) | What it tells you |
|-------|-------------------|-------------------|
| failed-login | First `Failed password for root` from 203.0.113.45 | Attack starts |
| multiple-retries | `message repeated 47 times` for root failures | Brute force escalates |
| successful-login | `Accepted password for deploy` from same IP | Initial compromise |
| sudo-escalation | `deploy` runs `sudo /bin/bash` as root | Privilege escalation |
| new-user | `useradd` creates `svc-backup` | Persistence account |
| cron-job | `svc-backup` cron curls beacon to attacker IP | Long-term access |

---

## Step 2 — Place events in chronological order

| Step | Slot | Token | IR phase |
|------|------|-------|----------|
| 1 | First Event | failed-login | Recon / first attempt |
| 2 | Second Event | multiple-retries | Brute force volume |
| 3 | Third Event | successful-login | Initial access |
| 4 | Fourth Event | sudo-escalation | Privilege escalation |
| 5 | Fifth Event | new-user | Persistence (local account) |
| 6 | Sixth Event | cron-job | Persistence (scheduled callback) |

**Answer order:** failed-login → multiple-retries → successful-login → sudo-escalation → new-user → cron-job

---

## Step 3 — Why this sequence is fixed

1. You cannot get **47 repeated failures** before the **first** failed attempt.
2. **Successful login** must follow brute force, not precede it.
3. **sudo** requires an authenticated session (`deploy` already logged in).
4. **useradd** and **cron** are post-compromise persistence; cron for `svc-backup` requires the account to exist first.

---

## Common mistakes

| Mistake | Why wrong |
|---------|-----------|
| successful-login before multiple-retries | Ignores repeated failure message |
| new-user before sudo-escalation | Attacker often escalates before creating backup accounts |
| cron-job before new-user | Cron entry references `svc-backup` user |
| Treating deploy sudo as first event | No auth success yet |

---

## Exam takeaway

Log timeline PBQs test **cause before effect**: authentication failures → success → escalation → persistence. Map each line to the kill-chain phase, then sort.

---

## Related lab

Pair with [[../ubuntu-ssh-breach-hardening/notes|Ubuntu SSH breach]]: same attack narrative; that lab focuses on hardening instead of ordering.
