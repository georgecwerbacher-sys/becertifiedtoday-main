---
type: pbq-scenario-recommendations
exam: SY0-701
scenario: siem-ransomware-mitre
last_updated: 2026-06-04
---

# SIEM ransomware — recommendations

- Part 1: parent **and** child process in Sigma — `-enc` alone is FP-heavy.
- Part 2: DCSync is still **Credential Access**, not Lateral Movement.
- Part 3: distinguish **two early alerts** (A001+A002) from **earliest CRITICAL** for auto-isolate (A002 only).

Pairs well with `pending/log-timeline-forensics.html` and `malware-ioc-analysis.html` in the public bank.
