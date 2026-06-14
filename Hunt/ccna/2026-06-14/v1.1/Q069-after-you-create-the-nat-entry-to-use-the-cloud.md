---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v1.1
source_id: howtonetwork-ccna-walkthrough
source_question_id: 8681
bct_match_score: 0.17
blueprint: V1.1
status: review
---

# Question 69

**Topic:** Tier B — WatuPro walkthrough; verify answer on Cisco Tier A

After you create the NAT entry to use the cloud proxy internally in your network, you need to evolve this architecture changing the IP based proxy to a DNS name-based implementation. As you don´t have any DNS server locally (since this is a small office), you need to configure DNS service on the router and create an entry for the proxy server. The name will be proxy.secureit.net and the IP address is 192.168.100.100. As per the corporate policy, no public access is allowed directly from hosts, just through the proxy. So, make sure public hosts will not be translated. Which configuration must be used to accomplish this task?

- A. R1(config)# ip dns serverR1(config)# ip domain-lookupR1(config)# ip name-server 8.8.8.8 1.1.1.1R1(config)# ip host proxy.secureit.net 192.168.100.100
- B. R1(config)# ip name-server 8.8.8.8 1.1.1.1R1(config)# ip host proxy.secureit.net 192.168.100.100
- C. R1(config)# ip domain-lookupR1(config)# ip name-server 8.8.8.8 1.1.1.1R1(config)# ip host proxy.secureit.net 192.168.100.100
- D. R1(config)# ip domain-lookupR1(config)# ip host proxy.secureit.net 192.168.100.100
- E. R1(config)# ip dns serverR1(config)# ip host proxy.secureit.net 192.168.100.100

V1.1

**Source:** `howtonetwork-ccna-walkthrough` · Q `8681` · [link](https://www.howtonetwork.com/free/cisco-ccna-exam-walkthrough/)

**BCT match score:** 0.17

- [ ] Verified vs Cisco Tier A
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]