---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v2.0
source_id: mastery-ccna-public
source_question_id: 11
bct_match_score: 0.16
blueprint: V2.0
exhibit: cli
status: review
---

# Question 97

**Topic:** Tier B — 24 on-page samples; verify answer on Cisco Tier A

**Exhibit (CLI transcript)**

```text
SW1# show ip dhcp snooping
DHCP snooping is enabled
DHCP snooping VLANs: 20
Trusted interfaces: Gi1/0/48
SW1# show interfaces trunk
Port        Mode   Status    Allowed vlans
Gi1/0/48    on     trunking  10,30
```

A addresses. The DHCP server is reached through distribution switch DSW1 on uplink Gi1/0/48, and the VLAN 20 SVI on DSW1 already has the correct helper address. A digital network assistant recommends automatically disabling DHCP snooping for VLAN 20. What is the best next action supported by the evidence?

- A. Approve disabling DHCP snooping on VLAN 20
- B. Reload SW1 to clear DHCP snooping bindings
- C. Add VLAN 20 to the trunk after validation
- D. Configure a helper address on the VLAN 20 SVI

**Stated answer (external):** C

**External explanation (unverified):**

Agentic AI can assist troubleshooting, but its proposed configuration changes should be validated against network evidence before being applied. Here, DHCP snooping is enabled for VLAN 20, but the uplink to DSW1 is already trusted, so snooping is not the supported root cause. The trunk output shows Gi1/0/48 allows only VLANs 10 and 30, which prevents VLAN 20 DHCP traffic from reaching the distribution switch and its helper address. The evidence supports correcting the trunk allowed VLAN list through normal change control, not blindly accepting the assistant’s autonomous change.

V2.0

**Source:** `mastery-ccna-public` · Q `11` · [link](https://masteryexamprep.com/exams/cisco/ccna/)

**BCT match score:** 0.16

- [ ] Verified vs Cisco Tier A
- [ ] Exhibit captured (CLI transcript or diagram image)
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]