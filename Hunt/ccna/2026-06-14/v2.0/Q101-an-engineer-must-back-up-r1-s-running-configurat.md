---
type: hunt-candidate
exam: CCNA-200-301
run: 2026-06-14
version_folder: v2.0
source_id: mastery-ccna-public
source_question_id: 15
bct_match_score: 0.14
blueprint: V2.0
exhibit: cli
status: review
---

# Question 101

**Topic:** Tier B — 24 on-page samples; verify answer on Cisco Tier A

**Exhibit (CLI transcript)**

```text
R1# show ip ssh SSH Enabled - version 2.0 Authentication timeout: 120 secs; Authentication retries: 3
R1# ping 192.0.2.50 Success rate is 100 percent (5/5)
R1# copy running-config tftp://192.0.2.50/R1-running.cfg Destination filename [R1-running.cfg]?
```

An engineer must back up R1’s running configuration to a file server. The security requirement says the transfer must protect both credentials and file contents in transit. Review the exhibit and choose the best next action. An engineer must back up R1’s running configuration to a file server. The security requirement says the transfer must protect both credentials and file contents in transit. Review the exhibit and choose the best next action.

- A. Keep the completed TFTP backup
- B. Disable SSH and retry the transfer
- C. Repeat the backup using FTP to 192.0.2.50
- D. Repeat the backup using SCP to 192.0.2.50

**Stated answer (external):** D

**External explanation (unverified):**

SCP is the appropriate secure file transfer method when a device configuration or software file must be protected in transit. In the exhibit, the router successfully used TFTP, but TFTP does not encrypt credentials or file data. The same exhibit also shows SSH version 2 is enabled and the target server is reachable, which supports using SCP for the required secure copy behavior. FTP would still expose credentials and data, and disabling SSH would remove the transport SCP depends on. The key distinction is that a successful transfer is not enough when the requirement specifically calls for secure transfer.

V2.0

**Source:** `mastery-ccna-public` · Q `15` · [link](https://masteryexamprep.com/exams/cisco/ccna/)

**BCT match score:** 0.14

- [ ] Verified vs Cisco Tier A
- [ ] Exhibit captured (CLI transcript or diagram image)
- [ ] Draft original stem in `gen_ccna_chain_pages.py`

[[2026-06-14|Back to run index]]