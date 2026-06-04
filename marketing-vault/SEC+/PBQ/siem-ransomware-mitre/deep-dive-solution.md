---
type: pbq-scenario-solution
exam: SY0-701
scenario: siem-ransomware-mitre
last_updated: 2026-06-04
---

# SIEM ransomware — deep dive solution

## Part 1 — Sigma (**B**)

```yaml
ParentImage|endswith: '\winword.exe'
Image|endswith: '\powershell.exe'
CommandLine|contains: '-enc'
```

Matches parent-child chain for the 09:15 stager; avoids broad `-enc` only or keyword noise.

## Part 2 — MITRE

| Alert | Answer |
|-------|--------|
| A001 | Initial Access (T1566) — macro .docm |
| A002 | Execution (T1059) — encoded PowerShell |
| A003 | Credential Access (T1003) — LSASS |
| A004 | Lateral Movement (T1570) — PsExec |
| A005 | Credential Access (T1003) — DCSync |
| A006 | Impact (T1486) — mass rename |
| A007 | Impact (T1486) — ransom note |

## Part 3 — Containment

1. **Two earliest stops:** #A001 + #A002 (before cred dump at 09:22)
2. **Earliest CRITICAL isolation on WS-JDOE:** #A002 (09:15) — prevents stager → cred → lateral → ransomware
3. **SOAR on A002:** Network isolate WS-JDOE, kill process, memory snapshot, P1 ticket

**Not:** email-only approval, AD block only, or kill-and-resume without isolation.
