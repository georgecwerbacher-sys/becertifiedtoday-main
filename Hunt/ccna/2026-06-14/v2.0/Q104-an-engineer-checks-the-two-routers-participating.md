---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v2.0
source_id: mastery-ccna-public
source_question_id: 18
bct_match_score: 0.13
blueprint: V2.0
exhibit: cli
status: review
---

# Question 104

**Topic:** Tier B — 24 on-page samples; verify answer on Cisco Tier A

**Exhibit (CLI transcript)**

```text
R1 Gi0/0 address: 192.0.2.2/24
R2 Gi0/0 address: 192.0.2.3/24
Device  Int    Grp  Pri  State   Master addr  Group addr
R1      Gi0/0  10   110  Master  192.0.2.2    192.0.2.1
R2      Gi0/0  10   100  Backup  192.0.2.2    192.0.2.1
```

An engineer checks the two routers participating in VRRP group 10. What is the best interpretation of the VRRP status?

- A. R1 is forwarding for the virtual gateway.
- B. Both routers are active because they share the group address.
- C. R2 is forwarding because it has the lower priority.
- D. The group is down because the virtual IP is not physical.

**Stated answer (external):** A

**External explanation (unverified):**

In VRRP, the router in the Master state owns forwarding responsibility for the shared virtual IP address. The exhibit shows both routers agree that 192.0.2.2 is the master address and that the group address is 192.0.2.1 , which is the default gateway used by clients. R1 has priority 110 and is listed as Master ; R2 has priority 100 and is listed as Backup . The higher-priority router normally becomes master when preemption and normal election behavior allow it. The key takeaway is that clients use the virtual IP, but the current master router performs the forwarding.

V2.0

**Source:** `mastery-ccna-public` · Q `18` · [link](https://masteryexamprep.com/exams/cisco/ccna/)

**BCT match score:** 0.13

- [ ] Verified vs Cisco Tier A
- [ ] Exhibit captured (CLI transcript or diagram image)
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]