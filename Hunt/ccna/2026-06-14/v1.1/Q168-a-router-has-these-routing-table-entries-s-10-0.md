---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v1.1
source_id: openexamprep-ccna
source_question_id: ccna-059
bct_match_score: 0.38
blueprint: V1.1
status: review
---

# Question 168

**Topic:** Tier B — verify answer on Cisco Tier A; enable when CCNA monthly collect ships

A router has these routing table entries:

  S 10.0.0.0/8 via 192.168.1.1
  O 10.0.0.0/8 [110/20] via 192.168.2.1
  C 10.1.1.0/24 is directly connected, GigabitEthernet0/0

A packet arrives destined for 10.1.1.50. Which route will the router use?

- A. The static route via 192.168.1.1 because static routes are preferred
- B. The OSPF route via 192.168.2.1 because it has a lower metric
- C. The connected route on GigabitEthernet0/0 because it is the longest prefix match
- D. The router will load balance across all three routes

**Stated answer (external):** C

V1.1

**Source:** `openexamprep-ccna` · Q `ccna-059` · [link](https://open-exam-prep.com/practice/ccna)

**BCT match score:** 0.38

- [ ] Verified vs Cisco Tier A
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]