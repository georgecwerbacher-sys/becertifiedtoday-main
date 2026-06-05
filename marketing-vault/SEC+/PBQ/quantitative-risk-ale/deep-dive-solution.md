---
type: pbq-scenario-solution
exam: SY0-701
scenario: quantitative-risk-ale
last_updated: 2026-06-05
---

# Quantitative Risk — ALE — deep dive solution

> ALE worksheet — justify $50,000 security awareness training with dollar-based ROI.

---

## Step 1 — Recall the formulas

| Term | Formula | Example (phishing row) |
|------|---------|------------------------|
| SLE | Asset Value × Exposure Factor | $100,000 × 30% = **$30,000** |
| ARO | Expected events per year | **5.0** |
| ALE | SLE × ARO | $30,000 × 5.0 = **$150,000** |

ALE annualizes risk; SLE alone is a single-event loss.

---

## Step 2 — Read the worksheet priorities

| Scenario | SLE | ARO | ALE | Note |
|----------|-----|-----|-----|------|
| Ransomware | $450,000 | 0.5 | $225,000 | Highest ALE |
| **Phishing** | $30,000 | 5.0 | **$150,000** | High frequency |
| DDoS | $40,000 | 2.0 | $80,000 | |
| Data breach PII | $200,000 | 0.3 | $60,000 | |
| Laptop theft | $2,500 | 3.0 | $7,500 | Low |

Training targets **phishing credential theft**, not ransomware directly.

---

## Step 3 — Build the business case (correct math)

**Correct: B**

1. Baseline phishing ALE = $150,000/year (ARO 5.0 × SLE $30,000).
2. After training, assume ARO drops from **5.0 → 1.0** (exhibit analyst note).
3. New ALE = $30,000 × 1.0 = **$30,000**.
4. Annual savings = $150,000 − $30,000 = **$120,000**.
5. One-time training cost = **$50,000**.
6. **Net benefit year one** = $120,000 − $50,000 = **$70,000**.

---

## Step 4 — Eliminate distractors

| Choice | Why wrong |
|--------|-----------|
| A — Use ransomware SLE only | Wrong risk; ignores frequency (ARO) |
| C — Fund only highest ALE | Budget justification must match the control's target risk |
| D — Transfer via insurance | Risk transfer strategy, not ROI math for awareness training |

---

## Exam takeaway

Tie control spend to the **ALE of the threat the control mitigates**, then show before/after ARO or SLE. Do not swap in unrelated highest-ALE scenarios.

**Objectives:** 5.3 risk quantification · ROI on security investments
