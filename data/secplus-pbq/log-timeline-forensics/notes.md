---
type: pbq-scenario-notes
exam: SY0-701
scenario: log-timeline-forensics
title: Log Timeline Forensics
status: production
last_updated: 2026-06-05
---

# Log Timeline Forensics — notes

## What this lab tests

Reorder six SSH auth log snippets from brute-force attempts through privilege escalation and persistence.

## SY0-701 alignment

**2.4** log analysis · **2.5** incident response timeline

## Page structure

| Section ID | Content |
|------------|---------|
| `log-timeline` | Single-section scenario (ported from `pending/`) |

**Previous:** [[../wap-secure-configuration/notes|wap-secure-configuration]] · **Next:** [[../pki-certificate-chain-browser-error/notes|pki-certificate-chain-browser-error]]

## Answer key (summary)

Chronological order: failed-login → multiple-retries → successful-login → sudo-escalation → new-user → cron-job

## Local preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/log-timeline-forensics/log-timeline-forensics.html
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/log-timeline-forensics/log-timeline-forensics.html#log-timeline
```

→ [[recommendations]] · [[deep-dive-solution]]
