---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v1.1
source_id: howtonetwork-ccna-walkthrough
source_question_id: 8662
bct_match_score: 0.21
blueprint: V1.1
status: review
---

# Question 54

**Topic:** Tier B — WatuPro walkthrough; verify answer on Cisco Tier A

You need to implement HSRP as per the following topology. When the primary router fails, the secondary needs to be activated. Once the primary becomes online again, it needs to be the active again. Which of the presented script can be used to accomplish the task?

- A. R1:interface GigabitEthernet0/0 standby 1 ip 192.168.200.1 standby 1 preemptR2:interface GigabitEthernet0/0 standby 1 ip 192.168.200.1 standby 1 prio 90 standby 1 preemptR3:interface GigabitEthernet0/0 standby 254 ip 192.168.200.254 standby 254 preemptR4:interface GigabitEthernet0/0 standby 254 ip 192.168.200.254 standby 254 prio 90 standby 254 preempt
- B. R1:interface GigabitEthernet0/0 standby 1 ip 192.168.200.1 standby 1 prio 100 standby 1 preemptR2:interface GigabitEthernet0/0 standby 1 ip 192.168.200.1 standby 1 prio 90 standby 1 preemptR3:interface GigabitEthernet0/0 standby 1 ip 192.168.200.254 standby 1 prio 100 standby 1 preemptR4:interface GigabitEthernet0/0 standby 1 ip 192.168.200.254 standby 1 prio 90 standby 1 preempt
- C. R1:interface GigabitEthernet0/0 standby 1 ip 192.168.200.1 standby 1 prio 100R2:interface GigabitEthernet0/0 standby 1 ip 192.168.200.1 standby 1 prio 90R3:interface GigabitEthernet0/0 standby 1 ip 192.168.200.254 standby 1 prio 100R4:interface GigabitEthernet0/0 standby 1 ip 192.168.200.254 standby 1 prio 90
- D. R1:interface GigabitEthernet0/0 standby 1 ip 192.168.200.1R2:interface GigabitEthernet0/0 standby 1 ip 192.168.200.1 standby 1 prio 90R3:interface GigabitEthernet0/0 standby 254 ip 192.168.200.254R4:interface GigabitEthernet0/0 standby 254 ip 192.168.200.254 standby 254 prio 90

V1.1

**Source:** `howtonetwork-ccna-walkthrough` · Q `8662` · [link](https://www.howtonetwork.com/free/cisco-ccna-exam-walkthrough/)

**BCT match score:** 0.21

- [ ] Verified vs Cisco Tier A
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]