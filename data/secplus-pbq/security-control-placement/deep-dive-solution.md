---
type: pbq-scenario-solution
exam: SY0-701
scenario: security-control-placement
last_updated: 2026-06-05
---

# Security Control Placement — deep dive solution

> Three-zone network diagram — place controls by function.

---

## Correct placements

| Slot | Control |
|------|---------|
| Between Internet ↔ DMZ | Perimeter Firewall |
| Protect Web Server (HTTP attacks) | WAF |
| Detect intrusions in DMZ | Network IDS |
| Decoy to lure attackers | Honeypot |
| Between DMZ ↔ Internal | Internal Firewall |
| Endpoint access control | NAC |
| Log aggregation & alerting | SIEM |

**Unused:** Proxy Server

---

## Zone logic

- **Internet (untrusted)** → perimeter firewall is the first enforcement point.
- **DMZ** hosts public services — WAF filters HTTP attacks; IDS monitors; honeypot decoys attackers.
- **Internal** — internal firewall segments DMZ from trusted LAN; NAC controls endpoint admission; SIEM centralizes alerts.

---

## Common mistakes

| Mistake | Why wrong |
|---------|-----------|
| WAF at Internet edge | WAF is application-layer for web server HTTP/S |
| Perimeter firewall between DMZ and Internal | That slot is the **internal** firewall role |
| SIEM in DMZ for “detection” | SIEM aggregates logs; IDS detects intrusions in DMZ |
| NAC on Internet boundary | NAC authenticates/admits **endpoints** on the internal network |
| Using all eight controls | Proxy is not required for this design |

---

## Exam takeaway

Know **what each control does** and **which network boundary** it typically protects — not just acronym recognition.
