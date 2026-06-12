---
type: pbq-scenario-recommendations
exam: SY0-701
scenario: governance
last_updated: 2026-06-08
---

# Governance & Compliance: recommendations

## Implementation status (2026-06-08)

| Item | Status |
|------|--------|
| SY0-701 objective badge (5.1 · 5.2 · 5.5) | Done |
| Governance exhibit first, sectioned layout | Done |
| Suite instructions (no blue-tile exhibit wording) | Done |
| Step-by-step deep dive | Done |
| Security+ practice portal listing | Done (Simulation bank 2) |
| Writing rules pass (no em/en dashes in guest copy) | Done |
| Parallel-compliance hint before choices | Done |
| Script outside article (no duplicate listeners) | Done |

## For learners

1. Classify **what data** was breached before you pick a framework.
2. GDPR and PCI can both apply to **one incident**. Compliance with one does not satisfy the other.
3. Encryption reduces risk; it does not automatically remove all notification duties.

## For instructors

| Priority | Recommendation |
|----------|----------------|
| High | Walk exhibit column 1 (frameworks) aloud, then map stem data types to GDPR and PCI clocks. |
| Medium | Contrast with [[../data-protection/notes|Data Protection]]: tokenization vs breach notification overlap. |
| Low | Ask which vendor agreement (NDA vs SLA) fits a cloud processor under review. |

## For product

- Strong capstone for the PBQ chain (governance + compliance overlap).
- Ad keyword angle: "Security+ GDPR PCI breach notification PBQ".
- Portal: listed under **Simulation bank 2** with Zero Trust, Firewall ACL, and Attack ID Remediation.

## Maintenance

- Edit `sections/governance.html` → `python3 scripts/build-pbq-production-suite.py`.
- Refresh [[deep-dive-solution|deep dive]] after stem or exhibit changes.
