---
type: pbq-scenario-recommendations
exam: SY0-701
scenario: zero-trust-zta-migration
last_updated: 2026-06-04
---

# Zero Trust migration — recommendations

## For learners

1. Memorize **control plane vs data plane**: decisions (policy engine, IdP, adaptive identity) vs enforcement (PEP, micro-segments).
2. For zone map: ask *“where is the user or asset before trust is established?”* → Internet gets **ZTNA**; *“where do we authenticate at the edge?”* → DMZ gets **IdP + continuous auth**.
3. **PAM Vault** belongs with assets it protects (internal), not where admins find it convenient (cloud) — exam trade-off framing.
4. ZTNA vs VPN: VPN grants **network**; ZTNA grants **application** with ongoing verification.

## For instructors

| Priority | Recommendation |
|----------|----------------|
| High | After Part 2, show one east-west flow diagram (workstation → micro-segment → DB) to reinforce Q3. |
| Medium | Clarify in exhibit that ZTA does **not** mean “remove all firewalls” (distractor D on Part 1). |
| Low | Add optional slot hint on first attempt only (e.g. “Internet has one slot”) for accessibility. |

## For product

- Part 2 is the highest cognitive load — consider **reset bank** button label “Shuffle controls” (already shuffled on load).
- YouTube clip candidate: 90s “8 controls, 4 zones” walkthrough linking to Professor Messer–style SY0-701 1.2 objectives.
- Ad landing message match: “Zero Trust PBQ — zone map + NIST SP 800-207” ([[../../07-keywords/landing-maps/security-plus-portal|Security+ portal map]]).

## Competitive / vault

- Logged in [[../../11-question-sourcing/pbq/secplus-pbq-not-in-bct|net-new PBQ log]] (2026-06-04).
- Compare monthly against competitor ZT drag-drop captures in `11-question-sourcing/pbq/captures/`.

## Maintenance

- NIST 800-207 errata or CompTIA objective wording changes → refresh [[deep-dive-solution|deep dive]].
