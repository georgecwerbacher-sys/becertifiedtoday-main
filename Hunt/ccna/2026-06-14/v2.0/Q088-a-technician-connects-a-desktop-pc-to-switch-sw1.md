---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v2.0
source_id: mastery-ccna-public
source_question_id: 2
bct_match_score: 0.15
blueprint: V2.0
exhibit: cli
status: review
---

# Question 88

**Topic:** Tier B — 24 on-page samples; verify answer on Cisco Tier A

**Exhibit (CLI transcript)**

```text
SW1# show interfaces gi1/0/12 status
Port Name Status Vlan Duplex Speed Type Gi1/0/12 PC-7 notconnect 20 auto auto 10/100/1000BaseTX
Cable tag: RJ-45 rollover console cable
Tester pin map: 1->8 2->7 3->6 4->5 5->4 6->3 7->2 8->1
```

A technician connects a desktop PC to switch SW1 on Gi1/0/12 , but the PC reports that the network cable is unplugged. The switch port is enabled and assigned to the correct access VLAN. What is the best interpretation or next action?

- A. Configure PortFast on the switch port.
- B. Replace it with an Ethernet crossover cable.
- C. Replace it with a straight-through Ethernet patch cable.
- D. Manually set both ends to full duplex.

**Stated answer (external):** C

**External explanation (unverified):**

The exhibit points to a physical cabling problem, not a VLAN, spanning-tree, or duplex problem. The switch shows notconnect , and the cable tag plus tester pin map identify a rollover console cable, where pin 1 maps to pin 8, pin 2 to pin 7, and so on. A rollover cable is used for console connections, not for Ethernet data links. For a typical desktop PC connected to a switch access port, use a normal straight-through Ethernet patch cable. The key clue is the reversed pinout before the link ever establishes.

V2.0

**Source:** `mastery-ccna-public` · Q `2` · [link](https://masteryexamprep.com/exams/cisco/ccna/)

**BCT match score:** 0.15

- [ ] Verified vs Cisco Tier A
- [ ] Exhibit captured (CLI transcript or diagram image)
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]