---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v2.0
source_id: mastery-ccna-public
source_question_id: 8
bct_match_score: 0.24
blueprint: V2.0
exhibit: none
status: review
---

# Question 94

**Topic:** Tier B — 24 on-page samples; verify answer on Cisco Tier A

Which device is currently forwarding traffic sent to the virtual gateway?

- A. R1, because it has priority 110
- B. Both routers, because HSRP load-balances by default
- C. R1, because it is local
- D. R2, because 10.10.10.3 is Active

**Stated answer (external):** D

**External explanation (unverified):**

HSRP uses one Active router to forward traffic for the virtual IP address and one Standby router to take over if the Active router fails. The show standby brief output is from R1, but R1’s state is Standby . The Active column lists 10.10.10.3, which the stem identifies as R2. Therefore, R2 is the device currently forwarding traffic sent to 10.10.10.1. Priority matters during election, but the current operational state in the output is the deciding evidence.

V2.0

**Source:** `mastery-ccna-public` · Q `8` · [link](https://masteryexamprep.com/exams/cisco/ccna/)

**BCT match score:** 0.24

- [ ] Verified vs Cisco Tier A
- [ ] Exhibit captured (CLI transcript or diagram image)
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]