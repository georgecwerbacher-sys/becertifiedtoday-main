---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v2.0
source_id: mastery-ccna-public
source_question_id: 16
bct_match_score: 0.12
blueprint: V2.0
exhibit: none
status: review
---

# Question 102

**Topic:** Tier B — 24 on-page samples; verify answer on Cisco Tier A

A network team uses Ansible to verify port status before a cabling change. The approved scope is read-only command execution on Site-A access switches only . The inventory contains these groups: [site_a_access] SW-A1 SW-A2 [site_a_distribution] DSW-A1 DSW-A2 [all_switches:children] site_a_access site_a_distribution Which Ansible plan best stays within the approved operational scope?

- A. Run ios_command against site_a_access for show interfaces status .
- B. Run ios_command against site_a_distribution for show interfaces status .
- C. Run ios_command against all_switches for show interfaces status .
- D. Run ios_config against site_a_access to set interface descriptions.

**Stated answer (external):** A

**External explanation (unverified):**

An Ansible command execution plan must match both the target scope and the allowed operation type. In this case, the approved scope is limited to Site-A access switches and read-only verification. The site_a_access inventory group contains only SW-A1 and SW-A2 , so it matches the device boundary. The ios_command module is appropriate for operational show commands such as show interfaces status ; it does not express an intent to change the running configuration. Targeting a broader or different group violates the device scope, and using a configuration module changes the type of operation. The key validation is: correct inventory group plus read-only command module.

V2.0

**Source:** `mastery-ccna-public` · Q `16` · [link](https://masteryexamprep.com/exams/cisco/ccna/)

**BCT match score:** 0.12

- [ ] Verified vs Cisco Tier A
- [ ] Exhibit captured (CLI transcript or diagram image)
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]