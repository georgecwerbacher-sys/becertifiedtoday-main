---
type: pbq-deep-dive
exam: SY0-701
scenario: mdm-enrollment-config
last_updated: 2026-06-22
---

# MDM enrollment — solution walkthrough

## HTTPS Certificate Settings

**HTTPS Certificate:** Enabled — MDM console and device communication must use TLS.

**Domain/Hostname:** `mdm.acmecorp.com` — `mdm` subdomain on `acmecorp.com`.

**Certificate File:** `/mnt/certs/AcmeMDMCertificate.pfx` — path given in the stem.

## iOS Compliance Policies

**Minimum iOS Version:** `17` — corporate standard is iOS 18; at most one major version behind.

**Password Requirement:** Enabled — users must set a passcode.

**Minimum Password Length:** `6` — meets “>= 6 characters.”

**Password Reuse:** Disabled — passcodes must never be reused.

**Auto-lock:** Enabled with **60** seconds — one minute of inactivity.

**Jailbreak alerts:** Enabled; email `alerts@mdm.acmecorp.com` — alerts@ the MDM hostname.

## Application Restrictions

Enable restrictions; **disable** App Store and unmanaged installs so only ACME-managed apps run; **enable** forced automatic updates.

## Enrollment Settings

**Enrollment Method:** Automated Device Enrollment (ADE) — Apple Device Enrollment Program / automatic enrollment.

**ADE token:** `/mnt/certs/AdeServerToken.p7m`

**Device Supervision:** Enabled — maximum management control.

**Allow Profile Removal:** Disabled — strictest enrollment; users cannot remove the MDM profile.
