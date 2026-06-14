---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v2.0
source_id: mastery-ccna-public
source_question_id: 10
bct_match_score: 0.23
blueprint: V2.0
exhibit: missing-image
status: review
---

# Question 96

**Topic:** Tier B — 24 on-page samples; verify answer on Cisco Tier A

> [!warning] Exhibit image not captured
> Hunt poll saved the stem only. The source page likely has a **topology or diagram**.
> Open the [source page](https://masteryexamprep.com/exams/cisco/ccna/) and save a PNG under `Hunt/ccna/<run>/images/` or transcribe CLI if shown.

Which interpretation is best based on the exhibit?

- A. Move PAT overload to G0/1 instead of G0/0.
- B. Swap the NAT roles on G0/0 and G0/1.
- C. Permit 203.0.113.0/30 in ACL 10.
- D. Keep the roles because inside means the ISP-facing source.

**Stated answer (external):** B

**External explanation (unverified):**

In IOS XE NAT, ip nat inside identifies the interface facing the original inside local addresses, usually the LAN. ip nat outside identifies the interface facing the outside network, usually the ISP. Here, G0/1 is the LAN default gateway for 192.168.10.0/24, so it should be inside. G0/0 connects to the ISP and is the interface whose address should be used for PAT overload, so it should be outside. The ACL is already matching the inside local subnet that needs translation. The issue is the reversed interface roles, not the overload interface or ACL source network.

V2.0

**Source:** `mastery-ccna-public` · Q `10` · [link](https://masteryexamprep.com/exams/cisco/ccna/)

**BCT match score:** 0.23

- [ ] Verified vs Cisco Tier A
- [ ] Exhibit captured (CLI transcript or diagram image)
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]