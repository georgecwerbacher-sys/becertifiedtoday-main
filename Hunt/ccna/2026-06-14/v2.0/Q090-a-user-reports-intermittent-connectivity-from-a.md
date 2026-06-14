---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v2.0
source_id: mastery-ccna-public
source_question_id: 4
bct_match_score: 0.18
blueprint: V2.0
status: review
---

# Question 90

**Topic:** Tier B — 24 on-page samples; verify answer on Cisco Tier A

A user reports intermittent connectivity from a wired desktop connected to SW1. The VLAN assignment is correct, and the port remains up. Based on the exhibit, what is the best interpretation?

- A. The access VLAN is missing from the switch
- B. Spanning Tree is blocking the desktop port
- C. A physical cabling or connector problem is likely
- D. The port is administratively shut down Best answer: C Explanation: CRC errors are received frames that fail the frame check sequence, commonly caused by physical-layer problems such as a damaged patch cable, bad connector, excessive interference, or a failing NIC/transceiver. In the exhibit, the interface is up/up at 1000 Mb/s full duplex, so the port is operational and passing traffic. The large number of input errors that are almost entirely CRC errors makes the physical medium the best place to investigate first. A reasonable next action would be to replace or test the cable and check the desktop NIC and switchport connection. VLAN or STP issues can cause reachability failures, but they do not explain this specific error pattern.

V2.0

**Source:** `mastery-ccna-public` · Q `4` · [link](https://masteryexamprep.com/exams/cisco/ccna/)

**BCT match score:** 0.18

- [ ] Verified vs Cisco Tier A
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]