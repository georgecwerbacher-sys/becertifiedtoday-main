---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v1.1
source_id: howtonetwork-ccna-walkthrough
source_question_id: 8665
bct_match_score: 0.25
blueprint: V1.1
status: review
---

# Question 57

**Topic:** Tier B — WatuPro walkthrough; verify answer on Cisco Tier A

You need to create an access-list where: - SSH traffic with destination 192.168.10.10 must be blocked just from subnet 192.168.0.0/24; - NTP traffic with destination 1.2.3.4 must be allowed just from subnet 192.168.0.0/24; - All the remaining traffic must be allowed.

- A. ip access-list extended acl deny tcp 192.168.0.0 0.0.0.255 host 192.168.10.10 eq 22 permit udp 192.168.0.0 0.0.0.255 host 1.2.3.4 eq 123 deny udp any host 1.2.3.4 eq 123 permit ip any any
- B. ip access-list extended acl deny tcp 192.168.0.0 0.0.0.255 host 192.168.10.10 eq 22 permit udp 192.168.0.0 0.0.0.255 host 1.2.3.4 eq 123 permit ip any any
- C. ip access-list extended acl deny tcp 192.168.0.0 0.0.0.255 host 192.168.10.10 eq 22 permit udp 192.168.0.0 0.0.0.255 host 1.2.3.4 eq 123 deny udp any host 1.2.3.4 eq 123
- D. ip access-list extended acl deny tcp 192.168.0.0 0.0.0.255 host 192.168.10.10 eq 22 permit tcp 192.168.0.0 0.0.0.255 host 1.2.3.4 eq 123 deny udp any host 1.2.3.4 eq 123 permit ip any any
- E. ip access-list extended acl deny tcp 192.168.0.0 0.0.0.255 host 192.168.10.10 eq 22 permit tcp 192.168.0.0 0.0.0.255 host 1.2.3.4 eq 123 deny udp any host 1.2.3.4 eq 123

V1.1

**Source:** `howtonetwork-ccna-walkthrough` · Q `8665` · [link](https://www.howtonetwork.com/free/cisco-ccna-exam-walkthrough/)

**BCT match score:** 0.25

- [ ] Verified vs Cisco Tier A
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]