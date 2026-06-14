---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v1.1
source_id: howtonetwork-ccna-walkthrough
source_question_id: 8687
bct_match_score: 0.20
blueprint: V1.1
status: review
---

# Question 74

**Topic:** Tier B — WatuPro walkthrough; verify answer on Cisco Tier A

You already configure voice and access VLAN to all users ports on a switch. Which of the following commands are necessary to enable port security and limit the number of mac addresses per port to 1 on each voice and access vlan? Make sure the ports will not disable when a violation occurs. Just drop the unknown source address packets and generates a SNMP trap to the syslog.

- A. SW01(config-if)#switchport port-security
- B. SW01(config-if)#switchport port-security maximum 1 vlan access
- C. SW01(config-if)#switchport port-security maximum 1 vlan voice
- D. SW01(config-if)#switchport port-security maximum 1
- E. SW01(config-if)# switchport port-security violation restrict
- F. SW01(config-if)# switchport port-security violation shutdown

V1.1

**Source:** `howtonetwork-ccna-walkthrough` · Q `8687` · [link](https://www.howtonetwork.com/free/cisco-ccna-exam-walkthrough/)

**BCT match score:** 0.20

- [ ] Verified vs Cisco Tier A
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]