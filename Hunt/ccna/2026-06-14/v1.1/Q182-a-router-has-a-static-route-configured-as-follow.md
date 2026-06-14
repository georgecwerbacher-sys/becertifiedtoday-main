---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v1.1
source_id: openexamprep-ccna
source_question_id: ccna-073
bct_match_score: 0.26
blueprint: V1.1
status: review
---

# Question 182

**Topic:** Tier B — verify answer on Cisco Tier A; enable when CCNA monthly collect ships

A router has a static route configured as follows:

  ip route 10.10.10.0 255.255.255.0 192.168.1.1

The next-hop 192.168.1.1 is reachable via a route learned from OSPF. What happens if the OSPF route to 192.168.1.1 is withdrawn?

- A. The static route remains in the routing table but packets are dropped
- B. The static route is automatically removed from the routing table
- C. The static route remains active and the router sends ARP requests for 192.168.1.1
- D. The router generates a syslog warning but keeps forwarding packets

**Stated answer (external):** B

V1.1

**Source:** `openexamprep-ccna` · Q `ccna-073` · [link](https://open-exam-prep.com/practice/ccna)

**BCT match score:** 0.26

- [ ] Verified vs Cisco Tier A
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]