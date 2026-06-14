---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v1.1
source_id: howtonetwork-ccna-walkthrough
source_question_id: 8653
bct_match_score: 0.16
blueprint: V1.1
status: review
---

# Question 46

**Topic:** Tier B — WatuPro walkthrough; verify answer on Cisco Tier A

An internal HTTP service must be published to the internet using the standard HTTP port, as per the topology below. You were asked to publish only HTTP service (using the standard port) using the public IP 100.101.102.103. Which commands you need to issue on RTR01 to accomplish this? BTW, the server already reaches RTR1, so don´t need to worry about routing issues.

- A. ip nat inside source static tcp 10.0.0.10 8080 100.101.102.103 80interface GigabitEthernet0/0/0 ip nat outsideinterface GigabitEthernet0/0/1 ip nat inside
- B. ip access-list extended NAT-SERVER-WWW permit tcp any host 10.0.0.10 eq 8080ip nat inside source list NAT-HOST-WWW interface GigabitEthernet0/0/0 overloadinterface GigabitEthernet0/0/1 ip nat outsideinterface GigabitEthernet0/0/0 ip nat inside
- C. ip nat inside source static ip 10.0.0.10 100.101.102.103interface GigabitEthernet0/0/1 ip nat outsideinterface GigabitEthernet0/0/0 ip nat inside
- D. ip nat inside source static tcp 100.101.102.103 80 10.0.0.10 8080interface GigabitEthernet0/0/1 ip nat outsideinterface GigabitEthernet0/0/0 ip nat inside

V1.1

**Source:** `howtonetwork-ccna-walkthrough` · Q `8653` · [link](https://www.howtonetwork.com/free/cisco-ccna-exam-walkthrough/)

**BCT match score:** 0.16

- [ ] Verified vs Cisco Tier A
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]