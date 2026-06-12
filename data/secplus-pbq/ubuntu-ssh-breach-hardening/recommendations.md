---
type: pbq-scenario-recommendations
exam: SY0-701
scenario: ubuntu-ssh-breach-hardening
last_updated: 2026-06-04
---

# Ubuntu SSH breach hardening — recommendations

## For learners

1. Configure **sshd + fail2ban + UFW** before consequence questions — badges show partial credit.
2. **Disable password authentication** is the strongest single control against the original brute-force vector (Q3), not port change alone.
3. Before `PasswordAuthentication no`, ensure **SSH public keys** are in `authorized_keys` (Q1 lockout).
4. After SSH hardening, **eradication** still requires cron and backdoor hunt (Q4) — NIST IR phase.

## For instructors

| Priority | Recommendation |
|----------|----------------|
| High | Demo fail2ban log line on wrong port vs 4422 when teaching Q2. |
| Medium | Mention `ufw allow 4422/tcp` vs scoped rule — explain why management subnet rule is correct. |
| Low | Add exhibit panel: attacker cron line from IR ticket (flavor only). |

## For product

- **Submit All & Grade** is correct UX for cross-section scoring; ensure mobile tap targets on UFW dropdowns.
- Pair with free sim funnel ([[../../05-playbooks/secplus-free-sim-funnel|Sec+ free sim funnel]]) as “Linux hardening PBQ sample.”
- Negative keywords: avoid “OpenSSL PBQ” confusion — see [[../../07-keywords/negatives/secplus-openssl-pbq|openssl negative list]].

## Technical accuracy

- OpenSSH **Protocol 2** only (Protocol 1 removed in modern OpenSSH).
- `LoginGraceTime 30` — reasonable hardening; not the primary anti-brute control.
- **24h bantime** — strong; acceptable for lab; note exam may use shorter windows.

## Maintenance

- Ubuntu/OpenSSH doc URL changes → update [[deep-dive-solution|deep dive]] references only (no dump links in public HTML).
