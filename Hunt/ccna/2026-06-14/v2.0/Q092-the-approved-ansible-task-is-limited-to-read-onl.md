---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v2.0
source_id: mastery-ccna-public
source_question_id: 6
bct_match_score: 0.14
blueprint: V2.0
exhibit: cli
status: review
---

# Question 92

**Topic:** Tier B — 24 on-page samples; verify answer on Cisco Tier A

**Exhibit (CLI transcript)**

```text
Proposed plan inventory : access_bldg2 : [ ASW21, ASW22] distribution : [ DSW1, DSW2] play : hosts : all tasks : - cisco.ios.ios_command : commands : - show vlan brief - show interfaces trunk - configure terminal - interface Gi1/0/24 - shutdown
```

The approved Ansible task is limited to read-only validation commands on Building 2 access switches only . Which action best keeps the Ansible command execution plan within the approved operational scope?

- A. Use ios_config to shut and re-enable Gi1/0/24
- B. Limit hosts to access_bldg2 and remove configuration commands
- C. Keep hosts: all to compare access and distribution trunks
- D. Run the plan because ios_command is read-only by design

**Stated answer (external):** B

**External explanation (unverified):**

The key issue is operational scope control for Ansible command execution. The approval permits read-only validation commands and only on the Building 2 access switches. The proposed plan violates both limits: hosts: all includes distribution switches, and the command list includes configuration-mode commands that would shut an interface. A safe validation plan would target the access_bldg2 inventory group and include only nonchanging commands such as show vlan brief and show interfaces trunk . The tool module name does not replace scope review; the host pattern and command list must both match the approved task.

V2.0

**Source:** `mastery-ccna-public` · Q `6` · [link](https://masteryexamprep.com/exams/cisco/ccna/)

**BCT match score:** 0.14

- [ ] Verified vs Cisco Tier A
- [ ] Exhibit captured (CLI transcript or diagram image)
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]