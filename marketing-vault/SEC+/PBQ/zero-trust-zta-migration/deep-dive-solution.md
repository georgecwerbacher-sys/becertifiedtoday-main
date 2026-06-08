---
type: pbq-scenario-solution
exam: SY0-701
scenario: zero-trust-zta-migration
last_updated: 2026-06-08
---

# Zero Trust migration: deep dive solution

> Sources: NIST SP 800-207, CISA Zero Trust microsegmentation guidance, CompTIA SY0-701 1.2 ZTA themes.

---

## Step-by-step: complete the scenario

Work through the **four sidebar sections** in order. Each graded part has a **Check answer** button. Open **Deep dive explanation** in the footer anytime for this walkthrough.

1. **Reference exhibit:** Open the blue **Open exhibit** tile. Compare **Traditional Perimeter** (implicit trust inside the firewall) with **Zero Trust** (never trust, always verify). Note five components: Policy Engine, Policy Administrator, Policy Enforcement Point (PEP), **adaptive identity** (MFA, device health, location risk), and **micro-segmentation**. You do not submit an answer here. The exhibit sets up Part 1.

2. **Core concept:** Read the stem. BeCertifiedToday moves from perimeter trust to ZTA. Drop choices that treat ZTA as cloud-only, always-on VPN, or firewall removal.
   - **A:** ZTA is not cloud-only. It applies on-prem, remote, and cloud.
   - **C:** VPN can carry traffic but does not define ZTA. One login is not continuous verification.
   - **D:** ZTA reframes trust. It does not remove enforcement points.
   - Select **B**, then **Check answer**. Every request is authenticated and authorized through a PEP with adaptive identity. **Never trust, always verify.**

3. **Zone control map:** Eight slots, each with **two related controls**. Pick the **best** option per row. Use the slot hint: Internet **1**, DMZ **2**, Internal **3**, Cloud **2**.

   **Mnemonic: I-D-I-C (1-2-3-2)**
   - **Internet:** **ZTNA Gateway** (not Identity Provider; IdP sits at the DMZ PEP).
   - **DMZ:** **Identity Provider** + **Continuous Auth** (not ZTNA or JIT; north-south PEP, not remote gateway or internal JIT).
   - **Internal:** **Micro-segmentation** + **PAM Vault** + **JIT Access** (not CASB, DLP, or Continuous Auth).
   - **Cloud:** **CASB** + **DLP Proxy** (not Micro-segmentation or PAM; those protect internal assets).

   Select one radio per slot. **All eight** must be correct to pass. Use **Check answer**, then **Show answer** if you are stuck.

4. **Trade-off decisions:** Three multiple-choice items. Each correct choice is **B**. Work Q1 through Q3 and **Check answer** on each.
   - **Q1:** ZTNA grants per-application access with continuous verification. VPN often grants full network access after one auth.
   - **Q2:** PAM Vault belongs with internal systems it protects. Cloud placement widens attack surface and recovery dependency.
   - **Q3:** Internal east-west traffic is also verified. Micro-segmentation and continuous auth apply; internal IPs are not implicitly trusted.

5. **Finish:** When all parts pass, use **Next** for the next PBQ or **Home** for the Security+ practice portal. Review the **Quick reference** below before test day.

### Common mistakes on the zone map

- You pick **PAM Vault** for Cloud because admins work remotely. This item places the vault with **internal** privileged systems.
- You put **ZTNA** in DMZ. Here ZTNA serves **external** subjects on the Internet zone.
- You swap **CASB** and **DLP**. CASB governs SaaS apps. DLP inspects sensitive data egress to cloud workflows.
- You leave **Continuous Auth** in Internal. Continuous verification belongs at the **DMZ PEP**, not deep inside the trust zone.

---

## Part 1: fundamental change

**Answer: B**

Traditional perimeter models grant **implicit trust** to traffic inside the firewall. One compromise enables **lateral movement**. Zero Trust removes location-based trust. **Every request** is authenticated and authorized through a **Policy Enforcement Point (PEP)**, with **adaptive identity** (MFA, device health, risk signals) and continuous evaluation. **Never trust, always verify.**

| Choice | Why wrong |
|--------|-----------|
| A: ZTA only in cloud | ZTA applies on-prem, remote, and cloud. Assets are not only in the enterprise LAN. |
| C: Always-on VPN | VPN is often a **carrier**. ZTA is a policy model. Mandatory VPN is not ZTA. |
| D: Remove all firewalls | ZTA uses segmentation and PEPs. It reframes trust; it does not remove enforcement. |

**Components to name on exam:** Policy Engine, Policy Administrator, PEP, adaptive identity, micro-segmentation.

---

## Part 2: zone control map

Each slot shows **two related controls**. Select the **best** one for that zone under ZTA.

| Slot | Pick (best) | Distractor (related, wrong zone) | Rationale |
|------|-------------|----------------------------------|-----------|
| Internet, remote access | **ZTNA Gateway** | Identity Provider | ZTNA replaces broad VPN for external/remote subjects. IdP belongs at the DMZ PEP. |
| DMZ, authentication | **Identity Provider** | ZTNA Gateway | Central auth at north-south boundary. ZTNA serves Internet remote access. |
| DMZ, session risk | **Continuous Auth** | JIT Access | Re-verify every session at PEP. JIT is time-bound **internal** privileged access. |
| Internal, east-west | **Micro-segmentation** | CASB | Limits lateral movement inside the LAN. CASB governs SaaS in Cloud. |
| Internal, credentials | **PAM Vault** | DLP Proxy | Vault for internal privileged systems. DLP inspects cloud/SaaS egress. |
| Internal, privileged access | **JIT Access** | Continuous Auth | Time-bound internal admin access. Continuous auth sits at DMZ PEP. |
| Cloud, SaaS governance | **CASB** | Micro-segmentation | Shadow IT and app policy in Azure/SaaS. Microseg is internal east-west. |
| Cloud, data egress | **DLP Proxy** | PAM Vault | Sensitive data leaving to cloud apps. PAM stores internal credentials. |

**Why DMZ gets two controls:** The DMZ is the **north-south policy enforcement boundary**. The **Identity Provider** authenticates subjects before they cross into protected resources. **Continuous Auth** re-evaluates risk throughout the session at that same boundary. ZTA does not trust once at VPN login and then allow free movement.

**Common mistakes**

- You place **PAM** in Cloud because admins work from home. Convenience does not override security placement in this item.
- You place **ZTNA** in DMZ. ZTNA serves **external** subjects on the Internet zone in this topology.
- You swap **CASB** and **DLP**. Both are cloud-adjacent. CASB is app governance. DLP is data exfiltration control.

---

## Part 3: trade-offs (all **B**)

### Q1: ZTNA vs VPN

**B:** ZTNA grants **per-application** access with **continuous verification**. VPN typically grants **full network** access after one authentication. That violates least privilege.

| Choice | Why wrong |
|--------|-----------|
| A | ZTNA still encrypts. Speed is not the defining security difference. |
| C | ZTNA deployments commonly **require** strong auth/MFA. |
| D | Cost and appliance choices vary. Not the conceptual ZTA answer. |

### Q2: PAM Vault in cloud vs internal

**B:** The senior engineer is right. PAM secures credentials **to internal systems**. Cloud placement increases attack surface and **dependency on external connectivity** for critical internal recovery.

| Choice | Why wrong |
|--------|-----------|
| A | Availability alone ignores blast radius and trust boundary. |
| C | Placement has clear security impact for root-of-trust systems. |
| D | Cloud ToS rarely prohibit PAM. The argument is architectural, not legal. |

*Real world:* cloud-hosted PAM exists. This question tests the **best trade-off among four exam answers**.

### Q3: never trust, always verify for internal traffic

**B:** Internal (east-west) traffic is **also verified**. Micro-segmentation and continuous authentication limit lateral movement. Internal IPs are not implicitly trusted.

| Choice | Why wrong |
|--------|-----------|
| A | Opposite of ZTA core tenet. |
| C | Re-auth on a fixed 24h timer is not continuous verification. |
| D | Internal firewalls/PEPs still exist in ZTA. |

---

## Quick reference

```
Part 1:  B
Zones:   Internet=ZTNA | DMZ=IdP+Continuous Auth | Internal=Microseg+PAM+JIT | Cloud=CASB+DLP
Part 3:  B | B | B
Mnemonic: I-D-I-C (1-2-3-2 slots)
```
