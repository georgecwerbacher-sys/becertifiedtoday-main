---
type: pbq-deep-dive
exam: SY0-701
scenario: cloud-waf-setup
last_updated: 2026-06-22
---

# Cloud WAF setup — deep dive solution

> Sample ticket **#bct2026** — configure the cloud WAF console tab by tab.

---

## Step-by-step: complete the scenario

Work through sample ticket **#bct2026** on the left. Each timestamped **task note** maps to one **console tab** on the right. Fill every field on all four tabs, then click **Check Answer**.

1. **Read the ticket header** — subject, requester, and summary confirm you are protecting **BeCertifiedToday.com** with a new production WAF policy.
2. **General Settings tab** — set domain, protocol, and policy name (encrypted traffic only).
3. **Security Rules tab** — enable the OWASP Top 10 baseline ruleset.
4. **Custom Rule tab** — create the CrossSiteScripting rule to block XSS.
5. **Logging & Monitoring tab** — choose verbose logging while rules are validated.
6. **Submit** — all eight fields must be correct. Use **Show Answer** if you are stuck, then re-read the **Why** column below for each setting.

---

## Step 1 — General Settings tab

| Setting | Correct value | Why |
|---------|---------------|-----|
| Domain Name | `BeCertifiedToday.com` | Scopes the WAF policy to the protected web application named in the ticket. |
| Protocol | **HTTPS** | Task note requires **encrypted traffic only**. HTTP would leave cleartext sessions outside the WAF policy scope. |
| WAF Policy Name | `ProductionPolicy` | Exact policy name from ticket note — must match character-for-character. |

**Wrong picks:** HTTP (violates encrypted-traffic requirement); a different domain or policy name (policy would not attach to the intended app).

---

## Step 2 — Security Rules tab

| Setting | Correct value | Why |
|---------|---------------|-----|
| Baseline Rule Set | **OWASP Top 10** | Industry-standard default ruleset for common web application flaws (injection, XSS, broken access control, misconfiguration, etc.). |

**Wrong picks:** Common Threats or CVE Patches alone do not satisfy the ticket’s explicit **OWASP Top 10** requirement.

---

## Step 3 — Custom Rule tab

| Setting | Correct value | Why |
|---------|---------------|-----|
| Rule Name | `CrossSiteScripting` | Ticket-specified identifier for the custom rule. |
| Match Condition | **XSS** | Cross-Site Scripting — blocks script injection in user input reflected or stored by the application. |
| Action | **Block** | Prevents XSS payloads from reaching the origin; Allow would pass attacks through; log-only is weaker during initial rollout. |

**Wrong picks:** SQL Injection or Directory Traversal (wrong attack class); Allow (does not stop XSS).

---

## Step 4 — Logging & Monitoring tab

| Setting | Correct value | Why |
|---------|---------------|-----|
| Logging Level | **Verbose** | Ticket asks for **as much detail as possible** while new rules are monitored. Minimal or Off would not support tuning and incident review. |

**Wrong picks:** Minimal (insufficient detail); Off (no visibility during validation window).

---

## Common mistakes

| Mistake | Result |
|---------|--------|
| HTTPS domain correct but HTTP selected | Policy does not match “encrypted traffic only.” |
| OWASP enabled but custom XSS rule set to Allow | Baseline helps; named XSS rule must still **block**. |
| Verbose logging on wrong tab only | Every tab field is graded — complete all four. |
| `example.com` or old ticket number | Use **BeCertifiedToday.com** and ticket **#bct2026**. |

---

## Quick reference

```text
General:  BeCertifiedToday.com | HTTPS | ProductionPolicy
Security: OWASP Top 10
Custom:   CrossSiteScripting | XSS | Block
Logging:  Verbose
```

**Exam takeaway:** WAF PBQs test **layer-7 filtering** — scope (domain + HTTPS), baseline rulesets (OWASP), explicit custom rules (XSS + block), and visibility (verbose logging during rollout).
