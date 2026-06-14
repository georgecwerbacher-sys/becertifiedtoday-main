---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v2.0
source_id: mastery-ccna-public
source_question_id: 23
bct_match_score: 0.43
blueprint: V2.0
status: review
---

# Question 109

**Topic:** Tier B — 24 on-page samples; verify answer on Cisco Tier A

A packet arrives with destination IP address 10.10.8.77 . Which next hop will IOS XE select for this packet?

- A. 172.16.1.1
- B. 172.16.2.1
- C. 172.16.4.1
- D. 172.16.3.1 Best answer: C Explanation: IOS XE selects a route using longest prefix match first. The destination 10.10.8.77 falls within 10.10.8.72/29 , whose usable range includes addresses from 10.10.8.73 through 10.10.8.78 . Even though other routes also match the destination, the /29 is more specific than the /26 , /24 , and /16 routes. Administrative distance is used to choose between competing routes to the same prefix length, not to override a longer matching prefix already in the routing table. The key takeaway is that the most specific matching route determines the forwarding next hop.

V2.0

**Source:** `mastery-ccna-public` · Q `23` · [link](https://masteryexamprep.com/exams/cisco/ccna/)

**BCT match score:** 0.43

- [ ] Verified vs Cisco Tier A
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]