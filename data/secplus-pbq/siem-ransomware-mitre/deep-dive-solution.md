---
type: pbq-scenario-solution
exam: SY0-701
scenario: siem-ransomware-mitre
last_updated: 2026-06-08
---

# SIEM ransomware — deep dive solution

> Seven correlated alerts from macro phish through ransomware impact. Author Sigma detection, map MITRE ATT&CK, then choose containment (SY0-701 2.4, 4.4, 4.7).

---

## Step 1 — Read the attack timeline exhibit

Open **Attack timeline** first. Note facts only (no MITRE labels in the exhibit):

| Time | Host | Event |
|------|------|-------|
| 09:14 | MAIL-SRV | Phishing .docm opened |
| 09:15 | WS-JDOE | Word → PowerShell `-enc` stager |
| 09:22 | WS-JDOE | LSASS / Mimikatz cred dump |
| 09:38 | WS-JDOE | PsExec to 10.0.0.31–33 |
| 09:55 | DC-01 | DCSync from WS-JDOE |
| 11:02 | FILE-SRV | Mass rename to `.locked` |
| 11:04 | FILE-SRV | Ransom note dropped |

Credential theft starts at **09:22**. Containment before that window is the exam focus in Part 3.

---

## Step 2 — Part 1 Sigma rule (**B**)

Use the **process creation exhibit** (Sysmon Event ID 1). The graded event is the child process, not the email server:

```yaml
ParentImage|endswith: '\winword.exe'
Image|endswith: '\powershell.exe'
CommandLine|contains: '-enc'
```

| Rule | Why wrong or right |
|------|-------------------|
| A | `-enc` on any PowerShell — no parent filter, high false positives |
| **B** | Parent Word + child PowerShell + `-enc` — matches 09:15 stager |
| C | Stops at Word → cmd.exe; misses PowerShell execution |
| D | Keyword noise — not field-based parent-child logic |

---

## Step 3 — Part 2 MITRE mapping (all seven required)

| Alert | Answer | Trap to avoid |
|-------|--------|---------------|
| A001 | Initial Access (T1566) | Macro/phish delivery |
| A002 | Execution (T1059) | Encoded PowerShell stager, not Initial Access |
| A003 | Credential Access (T1003) | LSASS read |
| A004 | Lateral Movement (T1570) | PsExec remote service |
| A005 | Credential Access (T1003) | **DCSync is cred access, not lateral movement** |
| A006 | Impact (T1486) | Mass encryption rename |
| A007 | Impact (T1486) | Ransom note |

---

## Step 4 — Part 3 containment (three distinct decisions)

Use the **SIEM alert index** in Part 3 for IDs, times, hosts, and severity.

1. **Two earliest chain stoppers (before 09:22):** **#A001 + #A002**
   - A001 stops macro/phish delivery; A002 stops the stager before cred dump.

2. **Earliest CRITICAL alert for WS-JDOE auto-isolation:** **#A002 only**
   - A001 is **HIGH**, not CRITICAL. First CRITICAL on WS-JDOE is the 09:15 stager.

3. **SOAR on #A002:** Network isolate WS-JDOE, kill process, memory snapshot, open P1 ticket.
   - Not email-only approval, AD block only, or kill-and-resume without isolation.

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Map A002 as Initial Access | Phish is A001; PowerShell execution is Execution |
| Map A005 as Lateral Movement | DCSync dumps credentials (Credential Access) |
| Pick A003 for earliest two | Cred dump is after the stager window |
| Pick A001 for CRITICAL auto-isolate | A001 is HIGH; question asks for earliest **CRITICAL** on WS-JDOE |

---

## Exam takeaway

SIEM PBQs test **detection precision** (Sigma parent-child), **ATT&CK taxonomy** (stage vs technique family), and **containment timing** (earliest stop vs severity-gated automation).

**Related labs:** [[../incident-response/notes|Incident Response]] (NIST phases) · [[../ransomware-dr-acme/notes|Ransomware DR]] (recovery order)

**Objectives:** 2.4 automation · 4.4 SIEM analysis · 4.7 incident response
