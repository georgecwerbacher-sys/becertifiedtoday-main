---
type: pbq-scenario-notes
exam: SY0-701
scenario: ubuntu-ssh-breach-hardening
title: Ubuntu SSH breach hardening
status: production
last_updated: 2026-06-04
---

# Ubuntu SSH breach hardening — notes

## What this lab tests

Single-scenario **post-incident hardening** on Ubuntu 22.04 after:

- SSH brute-force on port 22
- Successful password login → **sudo** pivot
- **Cron** persistence as root

Candidate fixes **sshd_config**, **fail2ban jail.local**, **UFW** rules, then answers **consequence MCQs** (lockout, port mismatch, best control, eradication).

## SY0-701 alignment

| Theme | Coverage |
|-------|----------|
| **4.1** Secure baselines | SSH hardening, firewall defaults |
| **4.4** Host hardening | Non-default port (depth), key-based auth, fail2ban |
| **2.4** Incident response | Persistence removal (cron, authorized_keys) |
| **2.x** Threats | Brute force, lateral movement after compromise |

## Page structure (folder sections)

| Section ID | Points | Content |
|------------|--------|---------|
| `ubuntu-intro` | — | Scenario + score badges |
| `ubuntu-sshd` | 7 | Port, Protocol, root/password, MaxAuthTries, LoginGraceTime, X11 |
| `ubuntu-fail2ban` | 4 | enabled, port, maxretry, bantime |
| `ubuntu-ufw` | 3 | SSH from mgmt net, Nginx Full, default policies |
| `ubuntu-consequences` | 4 | MCQs — graded with **Submit All & Grade** |

**Critical interdependency:** `Port 4422` must match in **sshd**, **fail2ban**, and **UFW** rule #1.

**Previous:** [[../hybrid-pki-audit/notes|Hybrid PKI]] · End of production chain.

## Scenario constants

- Management subnet: `10.0.1.0/24`
- SSH port after hardening: `4422`
- Web: Nginx (HTTP/HTTPS profile)

## Preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/ubuntu-ssh-breach-hardening/ubuntu-ssh-breach-hardening.html
```

→ [[recommendations]] · [[deep-dive-solution]]
