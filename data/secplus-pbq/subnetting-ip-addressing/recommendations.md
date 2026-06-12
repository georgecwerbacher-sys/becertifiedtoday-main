---
type: pbq-scenario-recommendations
exam: SY0-701
scenario: subnetting-ip-addressing
last_updated: 2026-06-05
---

# Subnetting & IP Addressing — recommendations

## For learners

1. **Maximize hosts** = choose the **smallest prefix extension** that still yields ≥6 subnets (/27, not /28).
2. /28 gives 14 usable hosts — **insufficient for Sales (25)**.
3. Magic number for /27 = **32**; subnets increment by 32 in the last octet.
4. First three subnets: `.0`, `.32`, `.64` — not `.1`, `.2`, `.3`.

## For instructors

| Priority | Recommendation |
|----------|----------------|
| High | Have learners write borrowed-bits math: ⌈log₂(6)⌉ = 3 → /27. |
| Medium | Use binary visualizer to tie mask 224 to three network bits in last octet. |
| Low | Contrast with CCNA chain subnet items in `public/CCNA-Study/`. |

## For product

- Calculator + magic table mirrors exam PBQ tooling; good standalone demo clip.
- Cross-link from Security+ “network implementation” study mode when available.

## Maintenance

- Edit `sections/subnet-ip-config.html` → `npm run build:pbq-suite`.
