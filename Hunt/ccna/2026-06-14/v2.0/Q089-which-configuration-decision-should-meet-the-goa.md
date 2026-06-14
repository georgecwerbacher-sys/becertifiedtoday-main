---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v2.0
source_id: mastery-ccna-public
source_question_id: 3
bct_match_score: 0.21
blueprint: V2.0
exhibit: cli
status: review
---

# Question 89

**Topic:** Tier B — 24 on-page samples; verify answer on Cisco Tier A

**Exhibit (CLI transcript)**

```text
R1# show ip ospf neighbor
Neighbor ID     Pri   State     Address       Interface
2.2.2.2           1   FULL/DR   10.0.12.2     Gi0/0
R1# show ip route 192.168.20.0
% Network not in table
R2# show ip route connected
C 10.0.12.0/30 is directly connected, GigabitEthernet0/0
C 192.168.20.0/24 is directly connected, GigabitEthernet0/1
```

Which configuration decision should meet the goal?

- F. No route filtering is configured. Exhibit: R1# show ip ospf neighbor Neighbor ID Pri State Address Interface 2.2.2.2 1 FULL/DR 10.0.12.2 Gi0/0 R1# show ip route 192.168.20.0 % Network not in table R2# show ip route connected C 10.0.12.0/30 is directly connected, GigabitEthernet0/0 C 192.168.20.0/24 is directly connected, GigabitEthernet0/1 Which configuration decision should meet the goal?
- A. Enable OSPF on R2 G0/1 in area 0.
- B. Change R2’s OSPF router ID and restart OSPF.
- C. Enable OSPF for 192.168.20.0/24 on R1.
- D. Configure a default static route on R1 toward R2.

**Stated answer (external):** A

**External explanation (unverified):**

The neighbor output shows that R1 and R2 already have a working OSPF adjacency, so the transit link is not the problem. R1 has no route for 192.168.20.0/24, while R2 shows that subnet as directly connected. In OSPF, a connected network is advertised only when the matching interface or subnet is enabled for OSPF in the correct area. The correct operational fix is on R2, for the LAN-facing interface or its subnet in area 0. If no OSPF neighbors should form on that LAN, making the interface passive is also common, but it still must be included in OSPF.

V2.0

**Source:** `mastery-ccna-public` · Q `3` · [link](https://masteryexamprep.com/exams/cisco/ccna/)

**BCT match score:** 0.21

- [ ] Verified vs Cisco Tier A
- [ ] Exhibit captured (CLI transcript or diagram image)
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]