---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v1.1
source_id: howtonetwork-ccna-walkthrough
source_question_id: 8655
bct_match_score: 0.23
blueprint: V1.1
status: review
---

# Question 48

**Topic:** Tier B — WatuPro walkthrough; verify answer on Cisco Tier A

Which command can be used to allow internal IP addresses from the corporate network 10.0.0.0/24 to access any public IP, using the interface Gi0/0/0 as translated source?

- A. ip access-list extended WWW-HOST-NAT permit ip 10.0.0.0 0.0.0.255 anyip nat inside source list WWW-HOST-NAT interface GigabitEthernet0/0/0 overloadinterface GigabitEthernet0/0/0 ip nat outsideinterface GigabitEthernet0/0/1 ip nat inside
- B. ip access-list extended WWW-HOST-NAT permit ip 10.0.0.0 255.255.255.0 anyip nat inside source list WWW-HOST-NAT interface GigabitEthernet0/0/0 overloadinterface GigabitEthernet0/0/0 ip nat outsideinterface GigabitEthernet0/0/1 ip nat inside
- C. ip access-list extended WWW-HOST-NAT permit ip 10.0.0.0 0.0.0.255 anyip nat inside source list WWW-HOST-NAT interface GigabitEthernet0/0/0 overloadinterface GigabitEthernet0/0/1 ip nat outsideinterface GigabitEthernet0/0/0 ip nat inside
- D. ip access-list extended WWW-HOST-NAT permit ip 10.0.0.0 0.0.0.255 anyip nat inside source list WWW-HOST-NAT interface GigabitEthernet0/0/1 overload
- E. ip access-list extended WWW-HOST-NAT permit ip 10.0.0.0 0.0.0.255 anyip nat inside source list WWW-HOST-NAT interface GigabitEthernet0/0/1 overloadinterface GigabitEthernet0/0/0 ip nat outsideinterface GigabitEthernet0/0/1 ip nat inside

V1.1

**Source:** `howtonetwork-ccna-walkthrough` · Q `8655` · [link](https://www.howtonetwork.com/free/cisco-ccna-exam-walkthrough/)

**BCT match score:** 0.23

- [ ] Verified vs Cisco Tier A
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]