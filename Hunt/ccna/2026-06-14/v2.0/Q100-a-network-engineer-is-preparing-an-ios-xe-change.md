---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v2.0
source_id: mastery-ccna-public
source_question_id: 14
bct_match_score: 0.26
blueprint: V2.0
status: review
---

# Question 100

**Topic:** Tier B — 24 on-page samples; verify answer on Cisco Tier A

A network engineer is preparing an IOS XE change to preserve the current Rapid PVST+ root bridge for VLAN 10 after maintenance. Based on the spanning-tree evidence, which configuration target is correct?

- A. Preserve SW-C as the VLAN 10 root bridge
- B. Preserve any switch with default priority
- C. Preserve SW-A as the VLAN 10 root bridge
- D. Preserve SW-B as the VLAN 10 root bridge Best answer: D Explanation: In Rapid PVST+, the root bridge is selected per VLAN by the lowest bridge ID, which combines bridge priority and MAC address. In the exhibit, the Root ID for VLAN 10 is priority 24586 and MAC address 0050.56aa.bbbb. SW-B’s Bridge ID has the same priority and MAC address, so SW-B is the current root bridge for VLAN 10. SW-A and SW-C show a root port and path cost toward that Root ID, which means they are non-root switches forwarding toward the root. The key evidence is the match between the Root ID and a switch’s local Bridge ID.

V2.0

**Source:** `mastery-ccna-public` · Q `14` · [link](https://masteryexamprep.com/exams/cisco/ccna/)

**BCT match score:** 0.26

- [ ] Verified vs Cisco Tier A
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]