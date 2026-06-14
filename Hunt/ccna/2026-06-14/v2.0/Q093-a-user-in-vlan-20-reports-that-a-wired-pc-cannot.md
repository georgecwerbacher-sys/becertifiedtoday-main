---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v2.0
source_id: mastery-ccna-public
source_question_id: 7
bct_match_score: 0.22
blueprint: V2.0
exhibit: cli
status: review
---

# Question 93

**Topic:** Tier B — 24 on-page samples; verify answer on Cisco Tier A

**Exhibit (CLI transcript)**

```text
Expected VLAN 20 prefix: 2001:db8:20:10::/64 R1 Gi0/0.20 IPv6: 2001:db8:20:10::1/64 PC IPv6 address: 2001:db8:20:1::25/64 PC default gateway: 2001:db8:20:10::1
```

A user in VLAN 20 reports that a wired PC cannot ping its IPv6 default gateway. The switchport is up/up in VLAN 20, and other VLAN 20 users can reach the gateway. Which root cause is best supported by the facts?

- A. The PC address is outside the VLAN 20 prefix.
- B. The switchport is assigned to the wrong VLAN.
- C. The PC default gateway is not reachable by other users.
- D. The router subinterface has the wrong prefix length.

**Stated answer (external):** A

**External explanation (unverified):**

IPv6 prefix membership is determined by comparing the network portion defined by the prefix length. For a /64 unicast prefix, the first four hextets identify the subnet. VLAN 20 expects 2001:db8:20:10::/64 , and the router interface is correctly addressed inside that subnet as 2001:db8:20:10::1/64 . The PC address 2001:db8:20:1::25/64 belongs to 2001:db8:20:1::/64 , not 2001:db8:20:10::/64 . Because the PC is configured in a different /64, it will not treat the gateway’s global address as on-link for the expected VLAN 20 subnet. The closest trap is the switchport VLAN, but the stem says the port is up/up in VLAN 20 and other users work.

V2.0

**Source:** `mastery-ccna-public` · Q `7` · [link](https://masteryexamprep.com/exams/cisco/ccna/)

**BCT match score:** 0.22

- [ ] Verified vs Cisco Tier A
- [ ] Exhibit captured (CLI transcript or diagram image)
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]