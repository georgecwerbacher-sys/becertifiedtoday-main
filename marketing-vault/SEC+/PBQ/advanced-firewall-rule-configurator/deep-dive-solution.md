---
type: pbq-scenario-solution
exam: SY0-701
scenario: advanced-firewall-rule-configurator
last_updated: 2026-06-08
---

# Advanced Firewall Rule Configurator: deep dive solution

> Perimeter ACL with inbound/outbound rules, CIDR notation, and explicit deny-all (SY0-701 3.3, 4.1).

---

## Step-by-step: complete the scenario

Work top to bottom on this single-page lab. Use **Check answer** when all rule fields are filled. Open **Deep dive explanation** in the footer anytime for this walkthrough.

1. **Read the stem:** You configure BeCertifiedToday's **perimeter firewall**. Traffic is evaluated **top-down; first match wins**.

2. **Reference exhibit: network topology:** Note three assets:
   - **Internet** (ANY) reaches the web server through the firewall.
   - **Web server** at **192.168.1.10** on internal LAN **192.168.1.0/24**.
   - **Mgmt workstations** at **10.0.0.0/24** are the only allowed SSH source.

3. **Policy requirements:** Five outcomes must appear as ACL rows (checklist turns green on pass):
   - Inbound **HTTPS** TCP **443** to **192.168.1.10** from any source.
   - Inbound **SSH** TCP **22** to **192.168.1.10** from **10.0.0.0/24** only.
   - Inbound **Telnet** TCP **23** **deny** from any source.
   - Outbound **DNS** UDP **53** from **192.168.1.0/24**.
   - **Implicit deny-all** as the **last** rule.

4. **Build the ACL table:** Click **+ Add Rule** until you have **five rows**. Fill direction, protocol, source, destination, port, and action. Use **ANY** for wildcards. CIDR is accepted (e.g. `10.0.0.0/24`).

   **Order tip:** Rules 1 through 4 can be in any order among themselves. **Deny-all must be rule 5.**

5. **Check answer:** Every field must be complete. The activity log records adds, deletes, and pass/fail. Use **Show answer** if stuck, then **Reset** to retry from scratch.

6. **Finish:** Use **Next** for the control-placement scenario or **Home** for the Security+ practice portal.

### Common mistakes

- You set SSH source to **ANY** instead of **10.0.0.0/24**.
- You mark DNS as **IN** instead of **OUT** (clients query resolvers outbound).
- You place **deny-all** above a permit rule (later permits would still match first).
- You skip an explicit **Telnet deny** (policy asks for it even though deny-all would block unknown traffic eventually).

---

## Correct rule set

| # | Dir | Proto | Source | Destination | Port | Action |
|---|-----|-------|--------|-------------|------|--------|
| 1 | IN | TCP | ANY | 192.168.1.10 | 443 | ALLOW |
| 2 | IN | TCP | 10.0.0.0/24 | 192.168.1.10 | 22 | ALLOW |
| 3 | IN | TCP | ANY | ANY | 23 | DENY |
| 4 | OUT | UDP | 192.168.1.0/24 | ANY | 53 | ALLOW |
| 5 | ANY | ANY | ANY | ANY | ANY | DENY |

Rules 1 through 4 may appear in any order. **Rule 5 must be last.**

---

## Why each rule exists

1. **HTTPS permit:** Public web service on the internal web host. TCP 443 from any source to the specific server IP.
2. **SSH permit:** Administrative access restricted to the management subnet only.
3. **Telnet deny:** Legacy cleartext protocol blocked inbound before a broad permit could allow it.
4. **DNS outbound:** Internal clients resolve names. UDP 53 from the internal LAN segment.
5. **Deny-all:** Default-deny catch-all. Must be evaluated after all explicit permits and denies.

---

## Contrast with Firewall ACL SecOps

The [[../firewall-acl-secops/notes|Firewall ACL SecOps]] lab uses **dropdown rows** for a three-tier DMZ table. This scenario adds **free-text CIDR**, **IN/OUT direction**, and an **activity log** to mirror exam-style firewall PBQs.

---

## Exam takeaway

**First match wins.** Place specific permits and explicit denies before the catch-all. Use **direction** (IN/OUT) correctly for asymmetric flows.

---

## Quick reference

```
ALLOW  IN  TCP  ANY           → 192.168.1.10     443
ALLOW  IN  TCP  10.0.0.0/24   → 192.168.1.10     22
DENY   IN  TCP  ANY           → ANY              23
ALLOW  OUT UDP  192.168.1.0/24 → ANY             53
DENY   ANY ANY  ANY           → ANY              ANY   (last)
```
