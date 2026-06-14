---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v2.0
source_id: mastery-ccna-public
source_question_id: 4
bct_match_score: 0.18
blueprint: V2.0
exhibit: cli
status: review
---

# Question 90

**Topic:** Tier B — 24 on-page samples; verify answer on Cisco Tier A

**Exhibit (CLI transcript)**

```text
SW1# show interfaces gigabitEthernet1/0/18
GigabitEthernet1/0/18 is up, line protocol is up
Hardware is Gigabit Ethernet, address is 0c9e.6a11.1212
MTU 1500 bytes, BW 1000000 Kbit/sec
Full-duplex, 1000Mb/s, media type is 10/100/1000BaseTX
5 minute input rate 81000 bits/sec, 70 packets/sec
5 minute output rate 76000 bits/sec, 65 packets/sec
186,240 packets input, 0 giants, 0 throttles
4,912 input errors, 4,887 CRC, 0 frame, 0 overrun
0 collisions, 0 late collision
```

A user reports intermittent connectivity from a wired desktop connected to SW1. The VLAN assignment is correct, and the port remains up. Based on the exhibit, what is the best interpretation?

- A. The access VLAN is missing from the switch
- B. Spanning Tree is blocking the desktop port
- C. A physical cabling or connector problem is likely
- D. The port is administratively shut down

**Stated answer (external):** C

**External explanation (unverified):**

CRC errors are received frames that fail the frame check sequence, commonly caused by physical-layer problems such as a damaged patch cable, bad connector, excessive interference, or a failing NIC/transceiver. In the exhibit, the interface is up/up at 1000 Mb/s full duplex, so the port is operational and passing traffic. The large number of input errors that are almost entirely CRC errors makes the physical medium the best place to investigate first. A reasonable next action would be to replace or test the cable and check the desktop NIC and switchport connection. VLAN or STP issues can cause reachability failures, but they do not explain this specific error pattern.

V2.0

**Source:** `mastery-ccna-public` · Q `4` · [link](https://masteryexamprep.com/exams/cisco/ccna/)

**BCT match score:** 0.18

- [ ] Verified vs Cisco Tier A
- [ ] Exhibit captured (CLI transcript or diagram image)
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]