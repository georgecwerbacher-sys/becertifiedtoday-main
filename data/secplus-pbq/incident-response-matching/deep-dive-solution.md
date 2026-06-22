---
type: pbq-deep-dive
exam: SY0-701
scenario: incident-response-matching
last_updated: 2026-06-22
---

# SEC+ Incident Response and Phase Matching — solution walkthrough

Drag-and-drop PBQ: place **two actions** in each **NIST SP 800-61** incident response phase bucket.

## Answer key

| Phase | Actions (both correct) |
|-------|------------------------|
| **Preparation** | Develop incident response plan · Establish and train response team roles and responsibilities |
| **Identification** | Analyze logs and alerts to detect anomalies · Validate and categorize security incidents |
| **Containment** | Apply short-term fixes or network segmentation · Isolate affected systems to prevent spread |
| **Eradication** | Remove malware and malicious artifacts · Disable compromised user accounts and credentials |
| **Recovery** | Restore systems and data from clean backups · Monitor systems and validate normal operations |
| **Lessons Learned** | Update incident response plan and security controls · Conduct post-incident review and root cause analysis |

## Phase-by-phase reasoning

### Preparation

Before an incident: document the **IR plan** and **train the team** on roles so response is coordinated instead of improvised.

### Identification

When events occur: use **log and alert analysis** to spot anomalies, then **validate and categorize** whether the activity is a true security incident.

### Containment

Limit blast radius: **segment the network** or apply short-term fixes and **isolate affected systems** so malware or an attacker cannot spread.

### Eradication

Remove the threat: **delete malware and artifacts** and **disable compromised accounts** so attacker persistence is eliminated.

### Recovery

Return to normal operations: **restore from clean backups** and **monitor/validate** that systems behave normally again.

### Lessons Learned

After closure: **update the IR plan and controls** and run a **post-incident review** with root-cause analysis to improve future response.

## Common mistakes

| Mistake | Why it is wrong |
|---------|-----------------|
| Putting isolation in eradication | Isolation limits spread — that is **containment**, not removal of the threat. |
| Putting log analysis in preparation | Analyzing logs happens when an event is suspected — **identification**. |
| Putting restore in eradication | Restoration returns business function — **recovery** after the threat is removed. |
| Mixing plan updates | **Develop** the plan in preparation; **update** it after lessons learned. |

## Quick reference

NIST lifecycle order: **Preparation → Identification → Containment → Eradication → Recovery → Lessons Learned**.

Each bucket holds exactly **two** tokens. Use **Show Answer** to verify placement, then **Reset** to practice again from a shuffled bank.
