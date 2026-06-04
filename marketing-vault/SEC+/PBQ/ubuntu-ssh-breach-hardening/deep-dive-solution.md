---
type: pbq-scenario-solution
exam: SY0-701
scenario: ubuntu-ssh-breach-hardening
last_updated: 2026-06-04
---

# Ubuntu SSH breach hardening — deep dive solution

> Sources: OpenSSH `sshd_config`, fail2ban wiki, Ubuntu Server UFW docs, NIST SP 800-61 (eradication).

---

## sshd_config (7 points)

| Setting | Correct | Why |
|---------|---------|-----|
| `Port` | **4422** | Non-default port adds defense-in-depth; must align with fail2ban and UFW. |
| `Protocol` | **2** | SSH protocol 1 is obsolete/insecure. |
| `PermitRootLogin` | **no** | Blocks direct root login; forces individual accountability. |
| `PasswordAuthentication` | **no** | Stops password brute force — primary attack vector in scenario. |
| `MaxAuthTries` | **3** | Limits guesses per connection (pairs with fail2ban `maxretry`). |
| `LoginGraceTime` | **30** | Shortens window for incomplete handshakes. |
| `X11Forwarding` | **no** | Reduces attack surface on a server role. |

**Order of operations in real life:** Deploy SSH keys **before** disabling password auth.

---

## fail2ban `jail.local` (4 points)

| Setting | Correct | Why |
|---------|---------|-----|
| `[sshd]` `enabled` | **true** | Jail must be active. |
| `port` | **4422** | Must match `sshd_config Port` or jail watches wrong service/log. |
| `maxretry` | **3** | Aligns with `MaxAuthTries` policy. |
| `bantime` | **24h** | Long ban slows persistent brute force (lab key). |

---

## UFW (3 points)

| # | Requirement | Correct rule |
|---|-------------|----------------|
| 1 | SSH on 4422 from management only | `ufw allow from 10.0.1.0/24 to any port 4422 proto tcp` |
| 2 | HTTP + HTTPS from anywhere | `ufw allow 'Nginx Full'` |
| 3 | Default policies | `ufw default deny incoming && ufw default allow outgoing` |

**Why not the distractors**

| Wrong rule | Problem |
|------------|---------|
| `ufw allow 22/tcp` | Wrong port after migration. |
| `ufw allow 4422/tcp` | Allows SSH from **any** source, not only mgmt subnet. |
| `ufw allow from any to any port 4422` | Overly broad source. |
| Default allow incoming | Violates least exposure post-breach. |

---

## Consequence MCQs

### Q1 — `PasswordAuthentication no` without user’s public key

**Answer: b** — Admin is **locked out** until their public key is in `authorized_keys`.

| Choice | Why wrong |
|--------|-----------|
| a, c, d | OpenSSH does not fall back to password when password auth is disabled. |

### Q2 — sshd on 4422, fail2ban still on port 22

**Answer: b** — fail2ban monitors **22** where no SSH listens; brute force on **4422** is **not** banned.

| Choice | Why wrong |
|--------|-----------|
| a | No effective protection on actual SSH port. |
| c | fail2ban does not auto-detect port changes without config. |
| d | SSH starts independently of fail2ban port setting. |

### Q3 — Most effective **single** change vs original brute force

**Answer: c** — **Disable password authentication; require SSH key pairs.**

| Choice | Why weaker as *single* fix |
|--------|---------------------------|
| a | Port change — security through obscurity; scanners still find SSH. |
| b | MaxAuthTries alone — passwords can still be guessed over many connections. |
| d | fail2ban helps but does not remove password attack surface. |

### Q4 — Remove cron persistence after SSH hardening

**Answer: b** — Audit `crontab -l` (root/users), `/etc/cron.*`, remove malicious entries; check **authorized_keys**, startup scripts.

| Choice | Why wrong |
|--------|-----------|
| a | Restarting sshd does not remove cron or backdoors. |
| c | Password change does not clear scheduled jobs or keys. |
| d | UFW does not block local cron execution. |

---

## Full pass checklist

```
sshd:     4422, 2, no root, no password, MaxAuthTries 3, Grace 30, no X11
fail2ban: enabled, port 4422, maxretry 3, bantime 24h
ufw:      allow 10.0.1.0/24→4422 | Nginx Full | default deny in / allow out
MCQ:      b | b | c | b
```

**IR sequence:** Contain (firewall) → Harden (SSH) → Eradicate (cron/keys) → Validate (monitor auth logs).
