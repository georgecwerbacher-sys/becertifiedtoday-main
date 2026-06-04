---
type: pbq-scenario-solution
exam: SY0-701
scenario: zero-trust-zta-migration
last_updated: 2026-06-04
---

# Zero Trust migration — deep dive solution

> Sources: NIST SP 800-207, CISA Zero Trust microsegmentation guidance, CompTIA SY0-701 1.2 ZTA themes.

---

## Part 1 — Fundamental change

**Answer: B**

Traditional perimeter models grant **implicit trust** to traffic inside the firewall. One compromise enables **lateral movement**. Zero Trust removes location-based trust: **every request** is authenticated and authorized through a **Policy Enforcement Point (PEP)**, with **adaptive identity** (MFA, device health, risk signals) and continuous evaluation — **never trust, always verify**.

| Choice | Why wrong |
|--------|-----------|
| A — ZTA only in cloud | ZTA applies on-prem, remote, and cloud; assets are not only in enterprise LAN. |
| C — Always-on VPN | VPN is often a **carrier**; ZTA is a policy model. Mandatory VPN ≠ ZTA. |
| D — Remove all firewalls | ZTA uses segmentation and PEPs; it reframes trust, not elimination of enforcement. |

**Components to name on exam:** Policy Engine, Policy Administrator, PEP, adaptive identity, micro-segmentation.

---

## Part 2 — Zone control map

Drag each token to the slot whose `data-target` matches the token `data-value`.

| Token | Zone | Rationale |
|-------|------|-----------|
| **ZTNA Gateway** | Internet | Remote/BYOD/partner access terminates at ZTNA instead of broad VPN to internal network. |
| **Identity Provider** | DMZ / edge | Central authentication at policy boundary; pairs with public-facing edge services. |
| **Continuous Auth** | DMZ / edge | Re-verify session risk at enforcement boundary (not “trust once” at VPN login). |
| **Micro-segmentation** | Internal | Limits east-west lateral movement between workloads/VLANs. |
| **PAM Vault** | Internal | Stores credentials for **internal** privileged systems; keeps vault off SaaS attack surface. |
| **JIT Access** | Internal | Time-bound privileged access to internal resources. |
| **CASB** | Cloud | Governs SaaS/shadow IT in Azure/SaaS. |
| **DLP Proxy** | Cloud | Inspects sensitive data leaving to cloud apps / egress paths. |

**Common mistakes**

- Putting **PAM** in Cloud because “admins work from home” — convenience ≠ security placement in this item.
- Putting **ZTNA** in DMZ — ZTNA serves **external** subjects on the Internet zone in this topology.
- Swapping **CASB** and **DLP** — both cloud-adjacent; CASB is app governance, DLP is data exfiltration control.

---

## Part 3 — Trade-offs (all **B**)

### Q1 — ZTNA vs VPN

**B:** ZTNA grants **per-application** access with **continuous verification**; VPN typically grants **full network** access after one authentication — violates least privilege.

| Choice | Why wrong |
|--------|-----------|
| A | ZTNA still encrypts; speed is not the defining security difference. |
| C | ZTNA deployments commonly **require** strong auth/MFA. |
| D | Cost/appliance varies; not the conceptual ZTA answer. |

### Q2 — PAM Vault in cloud vs internal

**B:** Senior engineer — PAM secures credentials **to internal systems**; cloud placement increases attack surface and **dependency on external connectivity** for critical internal recovery.

| Choice | Why wrong |
|--------|-----------|
| A | Availability alone ignores blast radius and trust boundary. |
| C | Placement has clear security impact for root-of-trust systems. |
| D | Cloud ToS rarely “prohibit PAM”; argument is architectural, not legal fiction. |

*Real world:* cloud-hosted PAM exists; this question tests **best trade-off among four exam answers**.

### Q3 — “Never trust, always verify” for internal traffic

**B:** Internal (east-west) traffic is **also verified** — micro-segmentation and continuous authentication limit lateral movement; internal IPs are not implicitly trusted.

| Choice | Why wrong |
|--------|-----------|
| A | Opposite of ZTA core tenet. |
| C | Re-auth on a fixed 24h timer is not the definition of continuous verification. |
| D | Internal firewalls/PEPs still exist in ZTA. |

---

## Quick reference

```
Part 1:  B
Zones:   Internet=ZTNA | DMZ=IdP+Continuous Auth | Internal=Microseg+PAM+JIT | Cloud=CASB+DLP
Part 3:  B | B | B
```
