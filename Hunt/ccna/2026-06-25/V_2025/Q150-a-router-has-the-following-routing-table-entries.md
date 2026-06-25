---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-25
version_folder: V_2025
source_id: openexamprep-ccna
source_question_id: ccna-065
bct_match_score: 0.29
blueprint: 
exhibit: none
status: review
---

# Question 150

**Topic:** Tier B — verify answer on Cisco Tier A; enable when CCNA monthly collect ships

A router has the following routing table entries:

  O    10.10.10.0/24 [110/20] via 192.168.1.1, GigabitEthernet0/0
  O    10.10.10.0/24 [110/20] via 192.168.2.1, GigabitEthernet0/1

What will the router do when it receives a packet destined for 10.10.10.50?

- A. Forward the packet only via 192.168.1.1 because it appears first
- B. Forward the packet only via 192.168.2.1 because it was learned more recently
- C. Perform equal-cost load balancing across both paths
- D. Drop the packet because there are duplicate routes

**Stated answer (external):** C

**Source:** `openexamprep-ccna` · Q `ccna-065` · [link](https://open-exam-prep.com/practice/ccna)

**BCT match score:** 0.29

- [ ] Verified vs Cisco Tier A
- [ ] Exhibit captured (CLI transcript or diagram image)
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-25|Back to run index]]