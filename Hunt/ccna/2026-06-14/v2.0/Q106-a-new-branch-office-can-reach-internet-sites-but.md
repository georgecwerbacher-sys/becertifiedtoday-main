---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v2.0
source_id: mastery-ccna-public
source_question_id: 20
bct_match_score: 0.14
blueprint: V2.0
exhibit: none
status: review
---

# Question 106

**Topic:** Tier B — 24 on-page samples; verify answer on Cisco Tier A

A new branch office can reach Internet sites, but users cannot reach the HQ file server at 10.10.20.50 . The branch has printers, VoIP phones, and PCs that all need access to HQ resources. Clues: Item Evidence Branch LAN 10.30.10.0/24 , DHCP working Branch WAN Public IP, interface up/up Routing Default route points to ISP Current workaround Only laptops with remote-access VPN clients can reach HQ What is the best corrective action?

- A. Configure an IPsec site-to-site VPN between the edge routers.
- B. Configure PAT only on the branch edge router.
- C. Add a CNAME record for the HQ file server.
- D. Install remote-access VPN software on every branch device.

**Stated answer (external):** A

**External explanation (unverified):**

An IPsec site-to-site VPN is appropriate when two locations need secure network-to-network connectivity over an untrusted network such as the Internet. In this case, the branch LAN has working DHCP, an up WAN link, and a default route for Internet access, but many device types need private access to HQ resources. Remote-access VPN works only for endpoints that can run a client, which does not fit printers, phones, and other shared devices. A site-to-site tunnel between the branch and HQ edge devices can protect traffic between the two private subnets transparently to the hosts.

V2.0

**Source:** `mastery-ccna-public` · Q `20` · [link](https://masteryexamprep.com/exams/cisco/ccna/)

**BCT match score:** 0.14

- [ ] Verified vs Cisco Tier A
- [ ] Exhibit captured (CLI transcript or diagram image)
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]