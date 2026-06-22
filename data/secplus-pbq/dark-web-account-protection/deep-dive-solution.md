---
type: pbq-deep-dive
exam: SY0-701
scenario: dark-web-account-protection
last_updated: 2026-06-22
---

# Dark web IR — solution walkthrough

**BeCertifiedToday.com** case **IR-2024-0847**: leaked directory index, compensation report, and credential audit on the dark web. Protect accounts without wiping kiosk forensic images.

## Step 1 — Review all three artifacts

Open **Directory contents**, **Compensation report**, and **User data** before answering.

- **Directory** — AD password policy shows 8-character minimum, weak complexity (letters OR numbers only), and **active 90-day expiration**.
- **User data** — credential audit export shows long-lived passwords, reuse across services, minimum length only, and weak patterns.
- **Compensation report** — HR payroll context; security findings are in directory and user-data artifacts.

## Step 2 — Weak password practices

Select **Age**, **Reuse**, **Length**, and **Complexity**.

Do **not** select **Expiration** — 90-day rotation is enforced; the breach drivers are age, reuse, short length, and weak complexity.

## Step 3 — Containment

Select **FIDO security key** — hardware-bound, phishing-resistant, and does not require typing secrets on a potentially compromised kiosk (preserves disk evidence).

PIN, SMS, and OTP are weaker and may leave traces on the host.
