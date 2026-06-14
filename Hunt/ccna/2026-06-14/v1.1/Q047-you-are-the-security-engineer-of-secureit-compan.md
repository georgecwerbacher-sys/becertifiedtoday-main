---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v1.1
source_id: howtonetwork-ccna-walkthrough
source_question_id: 8654
bct_match_score: 0.15
blueprint: V1.1
status: review
---

# Question 47

**Topic:** Tier B — WatuPro walkthrough; verify answer on Cisco Tier A

You are the security engineer of SecureIT company. You need to implement a cloud proxy solution, where your local hosts will need to reach the proxy server to access any external website. Currently, all the hosts are using static proxy configuration pointing to the IP address 192.168.100.100 and port TCP/3080. Which configuration can be used to make this migration with low impact? The new proxy IP is 200.201.202.203 and the new TCP port is TCP/9400.

- A. ip access-list extended WWW-HOST-NAT permit tcp 10.0.0.0 0.0.0.255 host 192.168.100.100 eq 3080ip nat inside source list WWW-HOST-NAT interface GigabitEthernet0/0/0 overloadip nat outside source static tcp 200.201.202.203 9400 192.168.100.100 3080 ip route 192.168.100.100 255.255.255.255 GigabitEthernet0/0/0 interface GigabitEthernet0/0/1 ip nat outsideinterface GigabitEthernet0/0/0 ip nat inside
- B. ip access-list extended WWW-HOST-NAT permit tcp 10.0.0.0 0.0.0.255 host 192.168.100.100 eq 3080ip nat inside source list WWW-HOST-NAT interface GigabitEthernet0/0/0 overloadip nat outside source static tcp 200.201.202.203 9400 192.168.100.100 3080 interface GigabitEthernet0/0/1 ip nat outsideinterface GigabitEthernet0/0/0 ip nat inside
- C. ip access-list extended WWW-HOST-NAT permit tcp 10.0.0.0 0.0.0.255 host 192.168.100.100 eq 3080ip nat inside source list WWW-HOST-NAT interface GigabitEthernet0/0/0 overloadip nat outside source static 200.201.202.203 192.168.100.100 interface GigabitEthernet0/0/1 ip nat outsideinterface GigabitEthernet0/0/0 ip nat inside
- D. ip access-list extended WWW-HOST-NAT permit tcp 10.0.0.0 0.0.0.255 eq 3080 host 192.168.100.100ip nat inside source list WWW-HOST-NAT interface GigabitEthernet0/0/0 overloadip nat outside source static 200.201.202.203 192.168.100.100 interface GigabitEthernet0/0/1 ip nat outsideinterface GigabitEthernet0/0/0 ip nat inside

V1.1

**Source:** `howtonetwork-ccna-walkthrough` · Q `8654` · [link](https://www.howtonetwork.com/free/cisco-ccna-exam-walkthrough/)

**BCT match score:** 0.15

- [ ] Verified vs Cisco Tier A
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]