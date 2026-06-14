---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v2.0
source_id: mastery-ccna-public
source_question_id: 13
bct_match_score: 0.19
blueprint: V2.0
exhibit: cli
status: review
---

# Question 99

**Topic:** Tier B — 24 on-page samples; verify answer on Cisco Tier A

**Exhibit (CLI transcript)**

```text
R1# show ip route | include 10.20|0.0.0.0
O    10.20.0.0/16 [110/20] via 192.0.2.2, GigabitEthernet0/0
S    10.20.30.0/24 [1/0] via 198.51.100.2, GigabitEthernet0/1
O    10.20.30.0/25 [110/30] via 192.0.2.6, GigabitEthernet0/2
S    10.20.30.64/26 [1/0] via 198.51.100.6, GigabitEthernet0/3
S*   0.0.0.0/0 [1/0] via 203.0.113.1, GigabitEthernet0/4
```

An engineer must apply an outbound policy only on the interface R1 will use to forward packets to destination 10.20.30.90 . Use only the routing table excerpt; do not assume any physical topology beyond what is shown. R1# show ip route | include 10.20|0.0.0.0 O 10.20.0.0/16 [110/20] via 192.0.2.2, GigabitEthernet0/0 S 10.20.30.0/24 [1/0] via 198.51.100.2, GigabitEthernet0/1 O 10.20.30.0/25 [110/30] via 192.0.2.6, GigabitEthernet0/2 S 10.20.30.64/26 [1/0] via 198.51.100.6, GigabitEthernet0/3 S* 0.0.0.0/0 [1/0] via 203.0.113.1, GigabitEthernet0/4 Which interface should be selected?

- A. GigabitEthernet0/4
- B. GigabitEthernet0/0
- C. GigabitEthernet0/1
- D. GigabitEthernet0/3

**Stated answer (external):** D

**External explanation (unverified):**

Routers choose the forwarding route by longest prefix match among routes installed in the routing table. The destination 10.20.30.90 falls within 10.20.30.64/26 , which covers addresses 10.20.30.64 through 10.20.30.127 . That prefix is more specific than the /25 , /24 , /16 , and default route entries, so R1 forwards the packet toward next hop 198.51.100.6 out GigabitEthernet0/3 . Administrative distance does not override a longer matching prefix when both routes are present in the table. The safest conclusion is the one directly supported by the route entry, not by assumed topology.

V2.0

**Source:** `mastery-ccna-public` · Q `13` · [link](https://masteryexamprep.com/exams/cisco/ccna/)

**BCT match score:** 0.19

- [ ] Verified vs Cisco Tier A
- [ ] Exhibit captured (CLI transcript or diagram image)
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]