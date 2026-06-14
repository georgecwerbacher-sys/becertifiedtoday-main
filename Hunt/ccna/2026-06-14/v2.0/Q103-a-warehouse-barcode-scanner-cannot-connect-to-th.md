---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v2.0
source_id: mastery-ccna-public
source_question_id: 17
bct_match_score: 0.13
blueprint: V2.0
exhibit: cli
status: review
---

# Question 103

**Topic:** Tier B — 24 on-page samples; verify answer on Cisco Tier A

**Exhibit (CLI transcript)**

```text
Clue Value Scanner RSSI -46 dBm AP channel/noise Channel 6, normal noise floor DHCP lease on scanner None assigned WLAN security WPA2-Personal AES/CCMP Scanner saved profile WPA2-Personal TKIP
```

A warehouse barcode scanner cannot connect to the Inventory WLAN after the WLAN security profile was updated. Other scanners using the same AP are connected and passing traffic. Which root cause is best supported by these facts?

- A. Weak wireless signal
- B. Incorrect AP channel selection
- C. DHCP scope exhaustion
- D. Wireless encryption mismatch

**Stated answer (external):** D

**External explanation (unverified):**

The key distinction is whether the client is failing at the wireless association/security stage or after joining the WLAN. Here, the scanner sees the SSID with strong signal strength, and the AP channel/noise information does not indicate an RF problem. The decisive clue is the security mismatch: the WLAN requires WPA2-Personal with AES/CCMP, but the scanner profile is saved for WPA2-Personal with TKIP. Because the client cannot complete the required wireless security negotiation, it never reaches the point where DHCP can assign an address. A missing DHCP lease is therefore a symptom, not the root cause.

V2.0

**Source:** `mastery-ccna-public` · Q `17` · [link](https://masteryexamprep.com/exams/cisco/ccna/)

**BCT match score:** 0.13

- [ ] Verified vs Cisco Tier A
- [ ] Exhibit captured (CLI transcript or diagram image)
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]