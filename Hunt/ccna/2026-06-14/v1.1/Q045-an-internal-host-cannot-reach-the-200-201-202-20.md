---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v1.1
source_id: howtonetwork-ccna-walkthrough
source_question_id: 8652
bct_match_score: 0.12
blueprint: V1.1
exhibit: none
status: review
---

# Question 45

**Topic:** Tier B — WatuPro walkthrough; verify answer on Cisco Tier A

An internal host cannot reach the 200.201.202.203 server on the internet. You were asked to fix this. Which commands you need to issue on RTR01 to accomplish this? BTW, the host already reaches RTR1, so don´t need to worry about routing issues. You need to allow the communication to any tcp port.

- A. ip access-list extended NAT-HOST-WWW permit tcp host 10.0.0.10 host 200.201.202.203ip nat inside source list NAT-HOST-WWW interface GigabitEthernet0/0/0 overloadinterface GigabitEthernet0/0/1 ip nat insideinterface GigabitEthernet0/0/0 ip nat outside
- B. ip access-list extended NAT-HOST-WWW permit ip 10.0.0.10 255.255.255.255 host 200.201.202.203ip nat inside source list NAT-HOST-WWW interface GigabitEthernet0/0/0 overloadinterface GigabitEthernet0/0/1 ip nat insideinterface GigabitEthernet0/0/0 ip nat outside
- C. ip access-list extended NAT-HOST-WWW permit ip 10.0.0.0 0.0.0.255 host 200.201.202.203ip nat inside source list NAT-HOST-WWW interface GigabitEthernet0/0/0 overloadinterface GigabitEthernet0/0/1 ip nat insideinterface GigabitEthernet0/0/0 ip nat outside
- D. ip access-list extended NAT-HOST-WWW permit ip host 10.0.0.10 host 200.201.202.203ip nat inside source list NAT-HOST-WWW interface GigabitEthernet0/0/0 overloadinterface GigabitEthernet0/0/1 ip nat outsideinterface GigabitEthernet0/0/0 ip nat inside

V1.1

**Source:** `howtonetwork-ccna-walkthrough` · Q `8652` · [link](https://www.howtonetwork.com/free/cisco-ccna-exam-walkthrough/)

**BCT match score:** 0.12

- [ ] Verified vs Cisco Tier A
- [ ] Exhibit captured (CLI transcript or diagram image)
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]