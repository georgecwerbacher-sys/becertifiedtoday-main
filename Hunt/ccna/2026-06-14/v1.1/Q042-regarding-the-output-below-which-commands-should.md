---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v1.1
source_id: howtonetwork-ccna-walkthrough
source_question_id: 8649
bct_match_score: 0.20
blueprint: V1.1
exhibit: image
status: review
---

# Question 42

**Topic:** Tier B — WatuPro walkthrough; verify answer on Cisco Tier A

**Exhibit (diagram)**

![Exhibit diagram](images/howtonetwork-ccna-walkthrough-q8649.png)

`Hunt/ccna/2026-06-14/images/howtonetwork-ccna-walkthrough-q8649.png`

Regarding the output below, which commands should be used to redistribute routes between OSPF and EIGRP? RTR4 must receive the default route either.

- A. router eigrp 10 redistribute ospf 10 subnetsrouter ospf 10 redistribute eigrp 10 subnets
- B. router eigrp 10 redistribute ospf 10 default-information originaterouter ospf 10 redistribute eigrp 10 subnets
- C. router eigrp 10 redistribute ospf 10 metric 10000 100 255 1 1500router ospf 10 redistribute eigrp 10 subnets
- D. router eigrp 10 redistribute ospf 10 metric 10000 100 255 1 1500 default-information originaterouter ospf 10 redistribute eigrp 10 subnets

V1.1

**Source:** `howtonetwork-ccna-walkthrough` · Q `8649` · [link](https://www.howtonetwork.com/free/cisco-ccna-exam-walkthrough/)

**BCT match score:** 0.20

- [ ] Verified vs Cisco Tier A
- [ ] Exhibit captured (CLI transcript or diagram image)
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]