---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v1.1
source_id: openexamprep-ccna
source_question_id: ccna-100
bct_match_score: 0.35
blueprint: V1.1
status: review
---

# Question 209

**Topic:** Tier B — verify answer on Cisco Tier A; enable when CCNA monthly collect ships

A network has two routers configured with HSRP. The virtual IP is 10.1.1.1, Router A (active) has interface IP 10.1.1.2, and Router B (standby) has interface IP 10.1.1.3. A host on the LAN has its default gateway set to 10.1.1.1. Router A fails. What happens?

- A. The host loses connectivity until an administrator manually reconfigures the gateway to 10.1.1.3
- B. Router B becomes the active router and begins responding to traffic sent to 10.1.1.1; the host maintains connectivity without any configuration change
- C. The host automatically discovers Router B through DHCP and updates its gateway
- D. Router B sends a gratuitous ARP claiming Router A's physical IP address 10.1.1.2

**Stated answer (external):** B

V1.1

**Source:** `openexamprep-ccna` · Q `ccna-100` · [link](https://open-exam-prep.com/practice/ccna)

**BCT match score:** 0.35

- [ ] Verified vs Cisco Tier A
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]