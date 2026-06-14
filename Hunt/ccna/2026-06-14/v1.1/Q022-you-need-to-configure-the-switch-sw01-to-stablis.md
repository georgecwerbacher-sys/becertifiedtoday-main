---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v1.1
source_id: howtonetwork-ccna-walkthrough
source_question_id: 8622
bct_match_score: 0.28
blueprint: V1.1
status: review
---

# Question 22

**Topic:** Tier B — WatuPro walkthrough; verify answer on Cisco Tier A

You need to configure the switch SW01 to stablish a trunk connection to the SW02. On this configuration, SW01 must communicate through all the VLANs with SW02. All the untagged traffic must be tagged as VLAN 100. Which script you should use to accomplish this task?

- A. SW01(config)#interface GigabitEthernet1/0/1 SW01(config-if)#switchport mode trunkSW01(config-if)#switchport access vlan 100
- B. SW01(config)#interface GigabitEthernet1/0/1 SW01(config-if)#switchport mode trunkSW01(config-if)#switchport trunk native vlan 100
- C. SW01(config)#interface GigabitEthernet1/0/1 SW01(config-if)#switchport mode trunkSW01(config-if)#switchport trunk allowed vlan 100
- D. SW01(config)#interface GigabitEthernet1/0/1 SW01(config-if)#switchport mode accessSW01(config-if)#switchport access vlan 100

V1.1

**Source:** `howtonetwork-ccna-walkthrough` · Q `8622` · [link](https://www.howtonetwork.com/free/cisco-ccna-exam-walkthrough/)

**BCT match score:** 0.28

- [ ] Verified vs Cisco Tier A
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]