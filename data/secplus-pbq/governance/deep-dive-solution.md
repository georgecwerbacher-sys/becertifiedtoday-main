---
type: pbq-scenario-solution
exam: SY0-701
scenario: governance
last_updated: 2026-06-08
---

# Governance & Compliance: deep dive solution

> Parallel GDPR and PCI DSS breach notification when EU personal data and cardholder data are exposed (SY0-701 5.1, 5.2, 5.5).

---

## Step-by-step: complete the scenario

Work top to bottom on this single-page lab. Use **Check answer** after you select a choice. Open **Deep dive explanation** in the footer anytime for this walkthrough.

1. **Read the stem:** You are the new CISO at **BeCertifiedToday**. A breach exposes **EU personal data** and **payment card data**. The question asks which **notification obligations** apply, not which policy document to write first.

2. **Reference exhibit: governance frameworks:** Scan three columns:
   - **Compliance frameworks:** Note **GDPR** (72-hour supervisory authority notice) and **PCI DSS** (cardholder data environment).
   - **Vendor agreement types:** Context for third-party risk (SLA, NDA, MSA). Not the graded answer, but supports governance objective **5.1**.
   - **Security policy types:** Incident response and business continuity tie to how you execute notifications after classification.

3. **Classify the data in the breach:**

| Data type | Framework | Why it matters |
|-----------|-----------|----------------|
| EU customer PII | **GDPR** | Personal data of EU subjects |
| Payment card numbers | **PCI DSS** | Cardholder data environment |

Both regimes can apply **at the same time** to one incident.

4. **List GDPR obligations:** When personal data is breached under GDPR:
   1. Notify the **supervisory authority** within **72 hours** when feasible.
   2. Notify **affected individuals** when the breach is likely to result in **high risk** to their rights and freedoms.
   3. Document the breach (records of processing / incident documentation).

   Encryption may reduce risk but does **not** automatically eliminate notification duties.

5. **List PCI DSS obligations:** When cardholder data is exposed:
   1. Notify the **acquiring bank** promptly.
   2. Notify **payment card brands** per scheme rules.
   3. Follow incident response and forensic requirements defined by the acquirer/brand.

   PCI compliance does **not** satisfy GDPR, and GDPR does **not** satisfy PCI.

6. **Select the answer:** **Correct: D** — Both GDPR and PCI DSS apply simultaneously with **separate** notification paths.

7. **Finish:** This is the end of the PBQ production chain. Use **Home** for the Security+ practice portal.

### Common mistakes

- You pick **A** because card data feels "more sensitive." GDPR still applies to EU personal data in the same breach.
- You pick **B** because encryption was mentioned in training. Encryption can reduce harm; it does not automatically waive all notice duties.
- You pick **C** because you focus on customer email only. GDPR requires supervisory authority notice; PCI requires acquirer and brand notice.

---

## Eliminate distractors

| Choice | Why wrong |
|--------|-----------|
| A — Only PCI | Ignores GDPR for EU personal data |
| B — No notice if encrypted | Encryption helps but does not auto-waive GDPR/PCI duties |
| C — Customers only, no regulators | GDPR requires supervisory authority notice; PCI requires acquirer/brand notice |

---

## Exhibit quick map (what each column is for)

| Column | Exam use |
|--------|----------|
| Frameworks | Match data type to regulation (GDPR + PCI here) |
| Vendor agreements | SLA vs MOU vs MSA for third-party governance |
| Policy types | IR/BC/DR documents that operationalize compliance |

---

## Exam takeaway

Governance questions often test **parallel compliance**: one breach, multiple frameworks, independent notification clocks.

**Objectives:** 5.1 governance · 5.2 compliance · 5.5 policies · PCI DSS incident reporting
