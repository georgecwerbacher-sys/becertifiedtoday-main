---
type: pbq-scenario-notes
exam: SY0-701
scenario: siem-ransomware-mitre
title: SIEM ransomware — Sigma & MITRE
status: production
last_updated: 2026-06-08
---

# SIEM ransomware — notes

7 alerts over 4 hours; forensics confirms ransomware + lateral movement via stolen creds.

## Parts

1. **Sigma** — Word → `powershell.exe -enc` (09:15)
2. **MITRE** — classify #A001–#A007
3. **Containment** — two earliest alerts (A001+A002), CRITICAL isolation (A002), SOAR playbook

**Previous:** [[../ransomware-dr-acme/notes|Ransomware DR]]

→ [[deep-dive-solution]]
