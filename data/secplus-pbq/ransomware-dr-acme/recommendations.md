---
type: pbq-scenario-recommendations
exam: SY0-701
scenario: ransomware-dr-acme
last_updated: 2026-06-04
---

# Ransomware DR — recommendations

## Learners

- Map **RTO** to SLA downtime and **RPO** to backup age — do not pick zero RPO when the stem says 6-hour backup.
- Warm site is the exam sweet spot between 4-hour RTO and $2M budget.
- Part 3 Q3 aligns with NIST IR **eradication before recovery**.

## Product

- Keep constraint cards visible when switching sections (consider sticky metrics bar in a future build).
- Pair with `pending/incident-response.html` for NIST phase vocabulary.

## Maintenance

`sections/*.html` → `npm run build:pbq-suite`
