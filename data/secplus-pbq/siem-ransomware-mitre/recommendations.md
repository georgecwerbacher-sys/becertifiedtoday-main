---
type: pbq-scenario-recommendations
exam: SY0-701
scenario: siem-ransomware-mitre
last_updated: 2026-06-08
---

# SIEM ransomware — recommendations

## For learners

1. **Part 1:** Parent **and** child process in Sigma. `-enc` alone is FP-heavy.
2. **Part 2:** DCSync is **Credential Access**, not Lateral Movement.
3. **Part 3:** Distinguish **two early alerts** (A001+A002) from **earliest CRITICAL** for auto-isolate (A002 only; A001 is HIGH).

## For instructors

| Priority | Recommendation |
|----------|----------------|
| High | Whiteboard the 09:14–09:22 window: what changes if you stop at A001 vs A002 vs A003. |
| Medium | Contrast HIGH vs CRITICAL for SOAR playbooks (Part 3 question 2). |
| Low | Pair with `log-timeline-forensics` and `malware-ioc-analysis` in the public bank. |

## For product

| Item | Status |
|------|--------|
| Neutral Sigma choice notes (field labels only) | Done |
| Timeline exhibit without MITRE stage tags | Done |
| Part 1 process-creation exhibit (Sysmon) | Done |
| Part 3 read-only alert index table | Done |
| Part 3 dropdown without CRITICAL arrows | Done |
| Expanded step-by-step deep dive | Done |

## Vault / ops

- Grading keys live in section scripts (`siem-part1-sigma.html`, `siem-part2-mitre.html`, `siem-part3-containment.html`).
- Rebuild: `python3 scripts/build-pbq-production-suite.py` after section edits.
