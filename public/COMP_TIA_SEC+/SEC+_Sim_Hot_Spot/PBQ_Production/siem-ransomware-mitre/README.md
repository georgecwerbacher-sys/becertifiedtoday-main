# SIEM ransomware — Sigma & MITRE ATT&CK

SY0-701 PBQ: triage 7 SIEM alerts from a multi-stage ransomware attack.

## Parts

| Section | Task |
|---------|------|
| `siem-overview` | Read-only attack timeline |
| `siem-part1-sigma` | Pick Sigma rule for Word → encoded PowerShell |
| `siem-part2-mitre` | Classify alerts #A001–#A007 |
| `siem-part3-containment` | Two early alerts + CRITICAL isolation + SOAR on A002 |

## Answer key

**Part 1:** **B** — ParentImage `winword.exe`, `powershell.exe`, `-enc`

**Part 2**

| Alert | Stage |
|-------|--------|
| A001 | Initial Access (T1566) |
| A002 | Execution (T1059) |
| A003 | Credential Access (T1003) |
| A004 | Lateral Movement (T1570) |
| A005 | Credential Access (T1003) |
| A006 | Impact (T1486) |
| A007 | Impact (T1486) |

**Part 3**

- Two earliest containment alerts: **#A001** + **#A002**
- Earliest CRITICAL for WS-JDOE isolation: **#A002**
- SOAR on A002: **Isolate** host (VLAN/NAC), kill process, memory snapshot, P1 ticket

## Chain

**Previous:** [Ransomware DR](../ransomware-dr-acme/ransomware-dr-acme.html)

## Preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/siem-ransomware-mitre/siem-ransomware-mitre.html
```
