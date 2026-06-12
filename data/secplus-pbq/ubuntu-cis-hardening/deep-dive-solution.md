---
type: pbq-scenario-solution
exam: SY0-701
scenario: ubuntu-cis-hardening
last_updated: 2026-06-05
---

# Ubuntu CIS baseline hardening — deep dive solution

> Checklist + sshd_config + pwquality.conf for CIS-aligned baseline.

---

## Part 1 — Checklist (all eight)

| Task | Detail |
|------|--------|
| Disable unused services | telnet, rsh, rlogin, vsftpd |
| Enable auditd logging | Privilege escalation tracking |
| Set /etc/shadow permissions | chmod 640 |
| Enable UFW firewall | ufw enable + default deny |
| Install AIDE | File integrity monitoring |
| Configure NTP | chronyc tracking |
| Disable IPv6 if unused | net.ipv6.conf.all.disable_ipv6=1 |
| Remove default accounts | userdel -r ubuntu |

---

## Part 2 — sshd_config

| Setting | Secure value |
|---------|--------------|
| Port | 22 (fixed) |
| Protocol | 2 |
| PermitRootLogin | no |
| PasswordAuthentication | no |
| PermitEmptyPasswords | no |
| MaxAuthTries | 3 |
| X11Forwarding | no |
| LoginGraceTime | 60 |
| AllowUsers | webadmin svcuser (fixed) |

---

## Part 3 — pwquality.conf

| Setting | Secure value |
|---------|--------------|
| minlen | 14 |
| minclass | 4 |
| maxrepeat | 2 |
| dcredit | −1 (require ≥1 digit) |
| ucredit | −1 (require ≥1 uppercase) |
| ocredit | −1 (require ≥1 special char) |

---

## Common mistakes

| Mistake | Why wrong |
|---------|-----------|
| Protocol 1 or 1,2 | SSH v1 is deprecated/insecure |
| PermitRootLogin yes | Direct root login violates CIS |
| PasswordAuthentication yes | Baseline prefers key-based auth |
| minlen 8 on CIS L1 stem | Ubuntu CIS L1 commonly requires 14 |
| dcredit 0 | Does not enforce digit requirement |

---

## vs Ubuntu SSH breach lab

| Topic | Baseline (this lab) | Post-breach lab |
|-------|---------------------|-----------------|
| SSH Port | 22 | 4422 |
| fail2ban | Checklist only | Full jail config |
| UFW | Checklist only | Rule ordering sim |
| Focus | CIS audit failure | Active incident |

---

## Exam takeaway

**Baseline hardening** = disable weak protocols, enforce password policy, reduce attack surface — match each setting to the **named standard** in the stem (CIS).
