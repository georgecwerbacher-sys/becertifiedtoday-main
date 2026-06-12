---
type: pbq-scenario-solution
exam: SY0-701
scenario: phishing-email-analysis
last_updated: 2026-06-05
---

# Phishing Email Analysis — deep dive solution

> Suspicious Microsoft 365 impersonation email — drag eight social-engineering terms into the analysis paragraph.

---

## Step 1 — Review the exhibit red flags

| Red flag | Evidence in email |
|----------|-------------------|
| Typosquatting | `micros0ft-support.com` (zero instead of letter O) |
| Urgency / fear | SUSPENDED in 24 hours, permanent deletion |
| Suspicious link | `micros0ft-login.ru` (untrusted TLD) |
| Generic greeting | "Dear Valued Customer" |
| Credential request | Password verification via email link |

---

## Step 2 — Match each blank to the correct term

| Blank | Correct term | Mapping |
|-------|--------------|---------|
| 1 | **typosquatting** | micros0ft domain typo |
| 2 | **pretexting** | Urgency story to pressure action |
| 3 | **phishing** | Email-based social engineering attack |
| 4 | **spear phishing** | *Definition slot:* targeted executive attack (contrast with this mass email) |
| 5 | **smishing** | SMS-based phishing (definition) |
| 6 | **vishing** | Voice/phone phishing (definition) |
| 7 | **brand impersonation** | Fake Microsoft Security Team |
| 8 | **report** | Safe response: report to security, do not click |

---

## Step 3 — How to solve quickly

1. Read the **fill-in sentence** — later blanks are **definitions** (spear phishing, smishing, vishing), not properties of this specific email.
2. Match blank 1–3 and 7–8 directly to red-flag list order in the exhibit.
3. Use process of elimination on the bank: only one token fits each `data-target`.

---

## Common mistakes

| Mistake | Why wrong |
|---------|-----------|
| spear phishing for blank 1 | This email is mass/generic, not executive-targeted |
| phishing for blank 2 | Urgency fabricates a scenario = **pretexting** |
| clicking the link to verify | Correct employee action is **report** |

---

## Exam takeaway

Phishing PBQs separate **attack delivery** (phishing), **manipulation tactic** (pretexting), **brand abuse** (impersonation), and **channel variants** (smishing/vishing). Always end with safe reporting.

**Objectives:** 2.2 social engineering · 2.4 user awareness
