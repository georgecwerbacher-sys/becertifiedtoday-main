---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v2.0
source_id: mastery-ccna-public
source_question_id: 19
bct_match_score: 0.55
blueprint: V2.0
exhibit: cli
status: review
---

# Question 105

**Topic:** Tier B — 24 on-page samples; verify answer on Cisco Tier A

**Exhibit (CLI transcript)**

```text
SW1# show spanning-tree vlan 20
Root ID    Priority 24596
Address 001e.7a11.2222
Cost 4
Port Gi1/0/1
Bridge ID  Priority 32788
Address 001e.7a11.1111
SW2# show spanning-tree vlan 20
Root ID    Priority 24596
Address 001e.7a11.2222
Bridge ID  Priority 24596
Address 001e.7a11.2222
This bridge is the root
```

Which switch is the root bridge for VLAN 20?

- A. The new access switch
- B. SW1
- C. SW2
- D. Cannot be determined from this output

**Stated answer (external):** C

**External explanation (unverified):**

In Rapid PVST+, each VLAN elects one root bridge based on the lowest bridge ID, which includes bridge priority and MAC address. The decisive evidence is the Root ID. On SW1, the Root ID is 001e.7a11.2222 , while SW1’s own Bridge ID is 001e.7a11.1111 , so SW1 is not the root and has a root port toward the root. On SW2, the Bridge ID matches the Root ID, and the output explicitly says This bridge is the root . A non-root switch has a root port; the root bridge does not need one for that VLAN.

V2.0

**Source:** `mastery-ccna-public` · Q `19` · [link](https://masteryexamprep.com/exams/cisco/ccna/)

**BCT match score:** 0.55

- [ ] Verified vs Cisco Tier A
- [ ] Exhibit captured (CLI transcript or diagram image)
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]