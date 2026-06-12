---
type: pbq-scenario-recommendations
exam: SY0-701
scenario: ubuntu-cis-hardening
last_updated: 2026-06-05
---

# Ubuntu CIS baseline hardening — recommendations

## For learners

1. Complete **all eight checklist items** before treating the server as hardened.
2. **LoginGraceTime 60** (this lab) vs **30** in breach scenario — both CIS-valid; know your stem.
3. **pwquality** negative credits (−1) **require** character classes; zero = no requirement.
4. Port stays **22** here — do not change to 4422 (that’s the breach lab).

## For instructors

| Priority | Recommendation |
|----------|----------------|
| High | Side-by-side with [[../ubuntu-ssh-breach-hardening/notes|Ubuntu SSH breach]] to contrast baseline vs incident response. |
| Medium | Map checklist items to CIS Ubuntu 22.04 L1 section numbers. |
| Low | Demo `pam_pwquality` on a VM after the sim. |

## For product

- Three-section sidebar mirrors real audit workbook (checklist → SSH → passwords).
- Strong “Linux hardening PBQ” SEO alongside existing Ubuntu breach lab.

## Maintenance

- Edit `sections/*.html` → `npm run build:pbq-suite`.
