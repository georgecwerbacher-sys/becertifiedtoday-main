---
type: pbq-deep-dive
exam: SY0-701
scenario: cloud-waf-setup
last_updated: 2026-06-22
---

# Cloud WAF setup — solution walkthrough

## General Settings

**Domain:** `example.com` scopes the policy to the protected web application.

**Protocol:** HTTPS — the ticket requires encrypted traffic only. HTTP would expose cleartext sessions outside the WAF policy scope.

**WAF Policy Name:** `ProductionPolicy` — exact name from the ticket.

## Security Rules

**Baseline Rule Set:** OWASP Top 10 — industry-standard default ruleset for common web application vulnerabilities (injection, XSS, broken access control, etc.).

## Custom Rule

**Rule Name:** `CrossSiteScripting` — ticket-specified identifier.

**Match Condition:** XSS — Cross-Site Scripting; blocks script injection in user input reflected or stored by the app.

**Action:** Block — prevent XSS rather than allow or log-only during initial rollout.

## Logging & Monitoring

**Logging Level:** Verbose — maximum detail while tuning new rules; minimal or off would not meet “as much information as possible.”
