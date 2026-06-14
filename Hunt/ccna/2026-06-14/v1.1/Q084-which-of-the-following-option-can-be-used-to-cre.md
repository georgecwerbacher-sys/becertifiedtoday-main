---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v1.1
source_id: howtonetwork-ccna-walkthrough
source_question_id: 8699
bct_match_score: 0.31
blueprint: V1.1
exhibit: none
status: review
---

# Question 84

**Topic:** Tier B — WatuPro walkthrough; verify answer on Cisco Tier A

Which of the following option can be used to create the following DHCP scope:

- A. Router(config)#ip dhcp excluded-address 10.10.1.1 10.10.1.19Router(config)#ip dhcp excluded-address 10.10.1.201 10.10.1.254Router(config)#ip dhcp pool POOLRouter(dhcp-config)#default-router 10.10.1.1Router(dhcp-config)#dns-server 10.10.10.10 10.10.10.11Router(dhcp-config)#option 150 ip 192.168.10.10Router(dhcp-config)#network 10.10.1.0 255.255.255.0
- B. Router(config)#ip dhcp excluded-address 10.10.1.1 10.10.1.20Router(config)#ip dhcp excluded-address 10.10.1.200 10.10.1.254Router(config)#ip dhcp pool POOLRouter(dhcp-config)#default-gateway 10.10.1.1Router(dhcp-config)#dns-server 10.10.10.10 10.10.10.11Router(dhcp-config)#option 53 ip 192.168.10.10Router(dhcp-config)#network 10.10.1.0 255.255.255.0
- C. Router(config)#ip dhcp excluded-address 10.10.1.20 10.10.1.200Router(config)#ip dhcp pool POOLRouter(dhcp-config)#default-router 10.10.1.1Router(dhcp-config)#dns-server 10.10.10.10 10.10.10.11Router(dhcp-config)#option 69 ip 192.168.10.10Router(dhcp-config)#network 10.10.1.0 255.255.255.0
- D. Router(config)#ip dhcp excluded-address 10.10.1.1 10.10.1.20Router(config)#ip dhcp excluded-address 10.10.1.200 10.10.1.254Router(config)#ip dhcp pool POOLRouter(dhcp-config)#default-gateway 10.10.1.1Router(dhcp-config)#dns-server 10.10.10.10 10.10.10.11Router(dhcp-config)#option 69 ip 192.168.10.10Router(dhcp-config)#network 10.10.1.0 255.255.255.0

V1.1

**Source:** `howtonetwork-ccna-walkthrough` · Q `8699` · [link](https://www.howtonetwork.com/free/cisco-ccna-exam-walkthrough/)

**BCT match score:** 0.31

- [ ] Verified vs Cisco Tier A
- [ ] Exhibit captured (CLI transcript or diagram image)
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]