---
type: pbq-scenario-solution
exam: SY0-701
scenario: data-protection
last_updated: 2026-06-05
---

# Data Protection — deep dive solution

> PCI card data in a **non-production test** environment — pick the right protection method.

---

## Step 1 — Classify the data

Payment card numbers (PANs) are **restricted** data under PCI DSS. The developer wants values that **behave like production** in test without exposing real PANs.

---

## Step 2 — Compare protection methods from the exhibit

| Method | Reversible? | Test usability | PCI fit |
|--------|-------------|----------------|---------|
| **Tokenization** | Token maps to PAN in vault | Full test values, no real PAN in test DB | **Preferred for card data** |
| Encryption | Yes, with key | Real PAN recoverable if dev holds key | PAN still in test if decrypted |
| Hashing (SHA-256) | No | Cannot reproduce PAN-like behavior | Integrity only |
| Masking (last 4) | N/A | Partial display | Not full test data |

---

## Step 3 — Apply the stem requirement

Developer needs **realistic card numbers** for functional testing **without** keeping production PANs in the test environment.

**Correct: C — Tokenization**

- Replace PANs with **format-preserving tokens** unrelated mathematically to the original.
- Real PANs remain in a **PCI-compliant vault**.
- Test apps use tokens that pass validation rules without exposing CHD in non-production.

---

## Step 4 — Eliminate distractors

| Choice | Why wrong |
|--------|-----------|
| A — Hashing | One-way; cannot support full card-number test scenarios |
| B — Encryption + dev key | Recoverable PANs still exist in test; key sprawl risk |
| D — Masking last 4 | Does not provide complete test PANs |

---

## Exam takeaway

**Tokenization** for PAN substitution in lower environments. **Masking** for display. **Hashing** for integrity. **Encryption** when authorized parties must recover the value under key management.

**Objectives:** 3.2 data protection · PCI DSS tokenization guidance
