---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v1.1
source_id: howtonetwork-ccna-walkthrough
source_question_id: 8601
bct_match_score: 0.56
blueprint: V1.1
exhibit: image
status: review
---

# Question 6

**Topic:** Tier B — WatuPro walkthrough; verify answer on Cisco Tier A

**Exhibit (diagram)**

![Exhibit diagram](images/howtonetwork-ccna-walkthrough-q8601.jpg)

`Hunt/ccna/2026-06-14/images/howtonetwork-ccna-walkthrough-q8601.jpg`

You have the following topology in your network and a Frame Flooding attack just ended. Just after the attack you connect a new host on the network (host C) and start sending traffic to host A, what happens and what you can do to prevent your environment from this to happening again?

- A. The switch 1 will forward the traffic just to host A. The best way to prevent the network from this attack is using access-list on all switch ports.
- B. The switch 1 will forward the traffic to hosts A and B. The best way to prevent the network from this attack is using spanning-tree portfast on all switch ports.
- C. The switch 1 will forward the traffic to hosts A, B and C. The best way to prevent the network from this attack is using port security on all switch ports.
- D. The switch 1 will forward the traffic to all the ports, including hosts A, B and the uplink port. The best way to prevent the network from this attack is using port security on all switch ports, except the uplink port.
- E. No packet will be forwarded until the switch is reloaded. The best way to prevent the network from this attack is using spanning-tree BPDU Guard enabled on all switch ports, except the uplink port.

V1.1

**Source:** `howtonetwork-ccna-walkthrough` · Q `8601` · [link](https://www.howtonetwork.com/free/cisco-ccna-exam-walkthrough/)

**BCT match score:** 0.56

- [ ] Verified vs Cisco Tier A
- [ ] Exhibit captured (CLI transcript or diagram image)
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]