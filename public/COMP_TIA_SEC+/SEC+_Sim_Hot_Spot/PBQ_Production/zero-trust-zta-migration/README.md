# BeCertifiedToday Zero Trust Architecture migration (PBQ)

SY0-701 performance-based practice: perimeter vs ZTA concepts, zone control map, and trade-off MCQs. Merged from former `pending/zero-trust.html` plus zone-map and trade-off parts.

## Chain

| File | Part |
|------|------|
| `zero-trust-zta-migration-part1.html` | Exhibit (perimeter vs NIST SP 800-207) + fundamental change MCQ |
| `zero-trust-zta-migration-part2.html` | Drag-and-drop — 8 controls → 4 zones (1+2+3+2 slots) |
| `zero-trust-zta-migration-part3.html` | ZTNA vs VPN, PAM placement, east-west verification (MCQ) |

**Previous scenario:** [acme-rag-hr-ai](../acme-rag-hr-ai/) Part 2 → Part 1 here. **Next:** [hybrid-pki-audit](../hybrid-pki-audit/) Part 1.

## Correct answers

**Part 1 MCQ:** B (never trust, always verify; PEP + adaptive identity)

**Part 2 zone map**

| Zone | Controls |
|------|----------|
| Internet | ZTNA Gateway |
| DMZ / Edge | Identity Provider, Continuous Auth |
| Internal | Micro-segmentation, PAM Vault, JIT Access |
| Cloud | CASB, DLP Proxy |

**Part 3 MCQs:** all B

## Preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/zero-trust-zta-migration/zero-trust-zta-migration-part1.html
```
