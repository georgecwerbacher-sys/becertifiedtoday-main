---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v1.1
source_id: howtonetwork-ccna-walkthrough
source_question_id: 8619
bct_match_score: 0.21
blueprint: V1.1
exhibit: none
status: review
---

# Question 19

**Topic:** Tier B — WatuPro walkthrough; verify answer on Cisco Tier A

You are the network analyst of FloodIT company and you need to restrict the management access to the RTR01 router, where just the IP 192.168.10.100 will be able to access it through SSH. No other host or protocol should be allowed. Which commands should be used to accomplish this task?

- A. ip access-list standard SSH permit 192.168.10.100line vty 0 15 access-class SSH in transport input ssh
- B. ip access-list standard SSH permit 192.168.10.100line vty 0 15 transport input ssh
- C. ip access-list standard SSH permit 192.168.10.100line vty 0 15 access-class SSH in
- D. ip access-list standard SSH permit tcp host 192.168.0.100 any eq 22line vty 0 15 access-class SSH in transport input ssh

V1.1

**Source:** `howtonetwork-ccna-walkthrough` · Q `8619` · [link](https://www.howtonetwork.com/free/cisco-ccna-exam-walkthrough/)

**BCT match score:** 0.21

- [ ] Verified vs Cisco Tier A
- [ ] Exhibit captured (CLI transcript or diagram image)
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]