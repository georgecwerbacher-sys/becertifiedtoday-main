---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v1.1
source_id: howtonetwork-ccna-walkthrough
source_question_id: 8664
bct_match_score: 0.29
blueprint: V1.1
exhibit: none
status: review
---

# Question 56

**Topic:** Tier B — WatuPro walkthrough; verify answer on Cisco Tier A

Which of the following access-list should be used to deny the following specific inbound traffic in the interface Gi0/0? SOURCE: 192.168.0.10 DESTINATION: 200.200.200.200 PROTOCOL: IP

- A. ip access-list extended block-specific deny ip host 192.168.0.10 host 200.200.200.200 permit ip any anyinterface GigabitEthernet0/0 ip access-group block-specific in
- B. ip access-list extended block-specific deny ip host 192.168.0.10 host 200.200.200.200interface GigabitEthernet0/0 ip access-group block-specific in
- C. ip access-list extended block-specific deny ip 192.168.0.10 255.255.255.255 200.200.200.200 255.255.255.255 permit ip any anyinterface GigabitEthernet0/0 ip access-group block-specific in
- D. ip access-list extended block-specific deny tcp host 192.168.0.10 host 200.200.200.200interface GigabitEthernet0/0 ip access-group block-specific in
- E. ip access-list extended block-specific permit tcp host 192.168.0.10 host 200.200.200.200interface GigabitEthernet0/0 ip access-group block-specific in

V1.1

**Source:** `howtonetwork-ccna-walkthrough` · Q `8664` · [link](https://www.howtonetwork.com/free/cisco-ccna-exam-walkthrough/)

**BCT match score:** 0.29

- [ ] Verified vs Cisco Tier A
- [ ] Exhibit captured (CLI transcript or diagram image)
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]