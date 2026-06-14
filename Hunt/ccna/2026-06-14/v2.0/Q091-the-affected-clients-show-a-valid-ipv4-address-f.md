---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v2.0
source_id: mastery-ccna-public
source_question_id: 5
bct_match_score: 0.20
blueprint: V2.0
exhibit: none
status: review
---

# Question 91

**Topic:** Tier B — 24 on-page samples; verify answer on Cisco Tier A

The affected clients show a valid IPv4 address from the DHCP server and an IPv6 default gateway learned from an unknown link-local address. The access switch log shows the link-local address arriving on a user-facing port connected to a small unmanaged router. What is the best corrective action?

- A. Enable Dynamic ARP Inspection for VLAN 30
- B. Configure storm control on the user-facing port
- C. Enable DHCP snooping for VLAN 30
- D. Enable RA guard on the user-facing port

**Stated answer (external):** D

**External explanation (unverified):**

The symptom points to a rogue IPv6 Router Advertisement, not an IPv4 DHCP, ARP, or broadcast-rate problem. IPv6 hosts can learn their default gateway from RA messages sent by routers on the local link. Because the unknown link-local gateway is being advertised from a user-facing port connected to an unmanaged router, RA guard is the Layer 2 control that should block those unauthorized RA messages at the access edge. DHCP snooping protects DHCP message trust boundaries, DAI validates ARP, and storm control limits excessive Layer 2 traffic rates. The key is matching the control to the specific Layer 2 threat.

V2.0

**Source:** `mastery-ccna-public` · Q `5` · [link](https://masteryexamprep.com/exams/cisco/ccna/)

**BCT match score:** 0.20

- [ ] Verified vs Cisco Tier A
- [ ] Exhibit captured (CLI transcript or diagram image)
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]