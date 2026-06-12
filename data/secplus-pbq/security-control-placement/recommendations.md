---
type: pbq-scenario-recommendations
exam: SY0-701
scenario: security-control-placement
last_updated: 2026-06-05
---

# Security Control Placement — recommendations

## For learners

1. Match **control function to slot label** — “Protect Web Server (HTTP attacks)” → **WAF**, not perimeter firewall.
2. **Perimeter firewall** sits between Internet and DMZ; **internal firewall** between DMZ and trusted LAN.
3. **NAC** = endpoint admission; **SIEM** = log aggregation — don’t swap them.
4. **Proxy Server** is a distractor for this topology.

## For instructors

| Priority | Recommendation |
|----------|----------------|
| High | Compare to [[../zero-trust-zta-migration/notes|ZTA zone map]] — same drag pattern, different controls. |
| Medium | Draw blank three-zone diagram on whiteboard before the sim. |
| Low | Discuss where proxy *would* fit (egress filtering) vs why it’s unused here. |

## For product

- Good visual PBQ for mobile (tap-to-pick supported).
- Pair with firewall ACL scenarios for “architecture + rules” study path.

## Maintenance

- Edit `sections/sec-control-placement.html` → `npm run build:pbq-suite`.
