---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v2.0
source_id: mastery-ccna-public
source_question_id: 1
bct_match_score: 0.16
blueprint: V2.0
exhibit: none
status: review
---

# Question 87

**Topic:** Tier B — 24 on-page samples; verify answer on Cisco Tier A

A NOC engineer is creating a prompt template for an AI assistant that reviews Cisco IOS XE show output and syslog excerpts during troubleshooting. The team must be able to verify recommendations before making changes, and the assistant must not perform remediation. Which output-format instruction best meets this goal?

- A. Use sections for Evidence, Assumptions, Recommended next checks, and Confidence.
- B. Use one concise root-cause paragraph with the most likely fix first.
- C. Use a prioritized command checklist without confidence ratings or assumptions.
- D. Use a configuration patch showing commands to apply immediately.

**Stated answer (external):** A

**External explanation (unverified):**

For AI-assisted network troubleshooting, the prompt should require a verifiable structure. Evidence should contain facts from the provided outputs, assumptions should identify what the assistant inferred, recommended next checks should tell the engineer how to validate the conclusion, and confidence should show how strongly the evidence supports the recommendation. This keeps the AI from blending facts with guesses or jumping directly to configuration changes. The key is not just getting an answer quickly, but making the reasoning auditable before a network operator acts.

V2.0

**Source:** `mastery-ccna-public` · Q `1` · [link](https://masteryexamprep.com/exams/cisco/ccna/)

**BCT match score:** 0.16

- [ ] Verified vs Cisco Tier A
- [ ] Exhibit captured (CLI transcript or diagram image)
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]