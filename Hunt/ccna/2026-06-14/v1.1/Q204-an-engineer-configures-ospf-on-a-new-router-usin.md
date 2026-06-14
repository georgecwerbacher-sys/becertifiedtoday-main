---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v1.1
source_id: openexamprep-ccna
source_question_id: ccna-095
bct_match_score: 0.21
blueprint: V1.1
exhibit: none
status: review
---

# Question 204

**Topic:** Tier B — verify answer on Cisco Tier A; enable when CCNA monthly collect ships

An engineer configures OSPF on a new router using the following commands:

  router ospf 10
   router-id 5.5.5.5
   network 10.0.0.0 0.0.0.255 area 0
   network 172.16.0.0 0.0.255.255 area 0
   passive-interface GigabitEthernet0/2

What is the effect of the "passive-interface GigabitEthernet0/2" command?

- A. OSPF will not advertise the network connected to GigabitEthernet0/2
- B. OSPF will advertise the network connected to GigabitEthernet0/2 but will not send or process OSPF hello packets on that interface
- C. GigabitEthernet0/2 will be shut down
- D. OSPF packets on GigabitEthernet0/2 will be encrypted

**Stated answer (external):** B

V1.1

**Source:** `openexamprep-ccna` · Q `ccna-095` · [link](https://open-exam-prep.com/practice/ccna)

**BCT match score:** 0.21

- [ ] Verified vs Cisco Tier A
- [ ] Exhibit captured (CLI transcript or diagram image)
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]