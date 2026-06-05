# Ubuntu 22.04 baseline hardening (CIS)

SY0-701 PBQ: checklist + sshd_config + pwquality.conf for a failed baseline audit.

## Sections

| ID | Content |
|----|---------|
| `harden-checklist` | Part 1 — eight required hardening tasks |
| `harden-sshd` | Part 2 — `/etc/ssh/sshd_config` |
| `harden-pwquality` | Part 3 — `/etc/security/pwquality.conf` |

## Answer keys

### Checklist (all eight required)

Disable unused services · auditd · `/etc/shadow` 640 · UFW · AIDE · NTP · disable IPv6 · remove default accounts

### sshd_config

| Setting | Value |
|---------|-------|
| Protocol | 2 |
| PermitRootLogin | no |
| PasswordAuthentication | no |
| PermitEmptyPasswords | no |
| MaxAuthTries | 3 |
| X11Forwarding | no |
| LoginGraceTime | 60 |

Port 22 and `AllowUsers webadmin svcuser` are fixed (already compliant).

### pwquality.conf

| Setting | Value |
|---------|-------|
| minlen | 14 |
| minclass | 4 |
| maxrepeat | 2 |
| dcredit | −1 |
| ucredit | −1 |
| ocredit | −1 |

## Chain

**Previous:** [Subnetting & IP Addressing](../subnetting-ip-addressing/subnetting-ip-addressing.html)

## Preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/ubuntu-cis-hardening/ubuntu-cis-hardening.html
```
