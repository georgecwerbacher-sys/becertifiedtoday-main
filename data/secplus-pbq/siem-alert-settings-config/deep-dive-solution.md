---
type: pbq-deep-dive
exam: SY0-701
scenario: siem-alert-settings-config
last_updated: 2026-06-22
---

# SIEM alert settings — solution walkthrough

## Rule Settings

**Maximum Failed Login Attempts:** `5` — matches corporate policy.

**Timeframe:** `15` minutes — same policy window.

**Window Type:** **Sliding** — marked recommended in the console; continuously evaluates the last 15 minutes for burst brute-force attempts (more accurate than fixed clock windows).

## Action Preferences

**Action:** **Notify** — SIEM is not integrated with firewalls yet; alert only, no block.

**Notification Method:** **Email** — ticket requires security team email notification.

**Notification Address:** `security@example.com` — address specified in the ticket.
