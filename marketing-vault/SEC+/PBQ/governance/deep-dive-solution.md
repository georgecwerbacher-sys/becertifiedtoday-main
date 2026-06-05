---
type: pbq-scenario-solution
exam: SY0-701
scenario: governance
last_updated: 2026-06-05
---

# Governance — deep dive solution

> Breach exposing EU personal data and payment card data — identify parallel notification obligations.

---

## Step 1 — Classify the data in the breach

| Data type | Framework | Why it matters |
|-----------|-----------|----------------|
| EU customer PII | **GDPR** | Personal data of EU subjects |
| Payment card numbers | **PCI DSS** | Cardholder data environment |

Both regimes can apply **at the same time** to one incident.

---

## Step 2 — List GDPR obligations

When personal data is breached under GDPR:

1. Notify the **supervisory authority** within **72 hours** when feasible.
2. Notify **affected individuals** when the breach is likely to result in **high risk** to their rights and freedoms.
3. Document the breach (records of processing / incident documentation).

Encryption may reduce risk but does **not** automatically eliminate notification duties.

---

## Step 3 — List PCI DSS obligations

When cardholder data is exposed:

1. Notify the **acquiring bank** promptly.
2. Notify **payment card brands** per scheme rules.
3. Follow incident response and forensic requirements defined by the acquirer/brand.

PCI compliance does **not** satisfy GDPR, and GDPR does **not** satisfy PCI.

---

## Step 4 — Select the answer

**Correct: D** — Both GDPR and PCI DSS apply simultaneously with **separate** notification paths.

---

## Eliminate distractors

| Choice | Why wrong |
|--------|-----------|
| A — Only PCI | Ignores GDPR for EU personal data |
| B — No notice if encrypted | Encryption helps but does not auto-waive GDPR/PCI duties |
| C — Customers only, no regulators | GDPR requires supervisory authority notice; PCI requires acquirer/brand notice |

---

## Exam takeaway

Governance questions often test **parallel compliance**: one breach, multiple frameworks, independent notification clocks.

**Objectives:** 5.1 governance · 5.5 privacy · PCI DSS incident reporting
