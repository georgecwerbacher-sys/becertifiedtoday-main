---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v2.0
source_id: mastery-ccna-public
source_question_id: 22
bct_match_score: 0.19
blueprint: V2.0
status: review
---

# Question 108

**Topic:** Tier B — 24 on-page samples; verify answer on Cisco Tier A

A branch office has one access switch port connected to a lightweight AP. Wired clients in VLAN 20 receive DHCP addresses and reach the default gateway. Wireless clients can associate to SSID Employees , which is configured to tag client traffic for VLAN 20, but they receive 169.254.x.x addresses. The AP management interface must remain untagged in VLAN 10. Current switch port role for the AP: access port in VLAN 10. Which configuration action should be taken?

- A. Enable PortFast on all wired client access ports.
- B. Configure the AP switch port as an 802.1Q trunk with native VLAN 10 and allow VLAN 20.
- C. Add a DHCP relay address to the VLAN 20 SVI.
- D. Change the SSID VLAN mapping from VLAN 20 to VLAN 10. Best answer: B Explanation: An AP that carries multiple VLANs to a switch normally needs an 802.1Q trunk. In this scenario, AP management must stay untagged in VLAN 10, while the Employees SSID tags client frames for VLAN 20. An access port in VLAN 10 drops or fails to carry the tagged VLAN 20 client traffic correctly, so wireless clients cannot reach DHCP even though wired VLAN 20 clients can. The focused fix is to make the AP-facing switch port a trunk, set VLAN 10 as the native VLAN, and permit VLAN 20. The working wired clients prove that VLAN 20 DHCP and gateway services are already functioning.

V2.0

**Source:** `mastery-ccna-public` · Q `22` · [link](https://masteryexamprep.com/exams/cisco/ccna/)

**BCT match score:** 0.19

- [ ] Verified vs Cisco Tier A
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]