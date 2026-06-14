---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v2.0
source_id: mastery-ccna-public
source_question_id: 9
bct_match_score: 0.19
blueprint: V2.0
status: review
---

# Question 95

**Topic:** Tier B — 24 on-page samples; verify answer on Cisco Tier A

A workstation on access port Gi1/0/12 in VLAN 30 cannot obtain an IPv4 address by DHCP. The DHCP server is reached through trunk Gi1/0/48 toward the distribution switch. You run simultaneous packet captures for 30 seconds. Exhibit: Packet-capture summary Capture point Observed traffic Gi1/0/12 client port DHCP Discover from client MAC every 4 seconds Gi1/0/48 trunk VLAN 10 and VLAN 20 traffic seen; no VLAN 30 frames from the client MAC What is the best interpretation?

- A. DHCP is failing because the client uses unicast requests.
- B. VLAN 30 traffic is not being forwarded on the trunk.
- C. The DHCP server is rejecting the client MAC address.
- D. The client is not sending DHCP Discover messages. Best answer: B Explanation: The capture evidence separates client behavior from forwarding behavior. The client is generating DHCP Discover broadcasts, so the workstation and DHCP protocol start are working. Because those same frames are absent on the trunk that should carry VLAN 30 toward the DHCP server, the likely fault is Layer 2 forwarding or filtering on the access switch path, such as VLAN 30 not being allowed, not active, or not properly carried on the trunk. The next practical check would be trunk and VLAN state, not DHCP server policy.

V2.0

**Source:** `mastery-ccna-public` · Q `9` · [link](https://masteryexamprep.com/exams/cisco/ccna/)

**BCT match score:** 0.19

- [ ] Verified vs Cisco Tier A
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]