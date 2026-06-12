---
type: pbq-scenario-notes
exam: SY0-701
scenario: ubuntu-cis-hardening
title: Ubuntu 22.04 baseline hardening
status: production
last_updated: 2026-06-05
---

# Ubuntu 22.04 baseline hardening — notes

## What this lab tests

Failed **security baseline audit** on a new Ubuntu 22.04 web server:

1. **Hardening checklist** — eight CIS-aligned tasks (services, auditd, shadow perms, UFW, AIDE, NTP, IPv6, default accounts)
2. **sshd_config** — seven dropdown settings (Port 22 fixed)
3. **pwquality.conf** — password complexity (minlen, minclass, credits)

Distinct from [[../ubuntu-ssh-breach-hardening/notes|Ubuntu SSH breach]] (post-incident: Port 4422, fail2ban, UFW ordering).

## SY0-701 alignment

| Theme | Coverage |
|-------|----------|
| **4.1** Secure baselines | CIS hardening, checklist |
| **4.4** Host hardening | SSH, PAM password policy |
| **1.4** Authentication | Password complexity |

## Page structure

| Section ID | Content |
|------------|---------|
| `harden-checklist` | Part 1 — task tiles |
| `harden-sshd` | Part 2 — sshd_config editor |
| `harden-pwquality` | Part 3 — pwquality.conf editor |

**Previous:** [[../subnetting-ip-addressing/notes|Subnetting]] · **Next:** [[../wap-secure-configuration/notes|WAP config]]

## Local preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/ubuntu-cis-hardening/ubuntu-cis-hardening.html
```

→ [[recommendations]] · [[deep-dive-solution]]
