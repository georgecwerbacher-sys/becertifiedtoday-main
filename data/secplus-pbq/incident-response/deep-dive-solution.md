---
type: pbq-scenario-solution
exam: SY0-701
scenario: incident-response
last_updated: 2026-06-05
---

# Incident Response — Ransomware IR — deep dive solution

> NIST SP 800-61 ransomware timeline exhibit with eight IR/forensics term blanks.

---

## Step 1 — Map the exhibit timeline to NIST phases

| Exhibit section | NIST phase | Key actions in scenario |
|-----------------|------------|-------------------------|
| Preparation | Preparation | IR plan, backups, tabletop exercise Q1 2026 |
| Detection & Analysis | Detection / Analysis | EDR + SIEM alerts, RCA begins 06:16 |
| Containment | Containment | Isolate WS-042, block C2, legal hold 06:40 |
| Footer flow | Eradication → Recovery → Lessons Learned | Post-containment steps |

---

## Step 2 — Fill each blank in the paragraph

| # | Blank | Correct term | Why |
|---|-------|--------------|-----|
| 1 | After Detection | **Analysis** | Scope and root-cause work (06:16 RCA) |
| 2 | Next phase | **Containment** | Isolate host, block C2 (section 3) |
| 3 | Final lifecycle step | **Lessons Learned** | Improve posture after recovery |
| 4 | Before isolation | **image** | Forensic disk image before changes |
| 5 | Evidence handling record | **chain of custody** | Who touched evidence and when |
| 6 | Preserve data | **legal hold** | Prevent destruction of relevant data |
| 7 | Plan test without real incident | **tabletop exercise** | Q1 2026 prep activity |
| 8 | Remove malware | **eradication** | Defined in footer flow after containment |

**Full answer string:** analysis · containment · lessons learned · image · chain of custody · legal hold · tabletop exercise · eradication

---

## Step 3 — Tie terms to exhibit evidence

- **Image before isolate:** Containment bullet says "preserve forensic image first" before WS-042 isolation.
- **Chain of custody / legal hold:** Containment section 06:40 explicitly references both.
- **Tabletop exercise:** Listed under Preparation, not during active containment.
- **Eradication vs Recovery:** Footer separates malware removal (eradication) from restore (recovery).

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Swap Analysis and Containment | RCA in exhibit is still in Detection & Analysis before isolation |
| Use "acquisition" instead of image | Blank expects the forensic **image** artifact |
| Put Lessons Learned before Recovery | NIST order: eradicate → recover → lessons learned |

---

## Exam takeaway

NIST SP 800-61 fill-ins reward **phase vocabulary** plus **forensics hygiene** (image, chain of custody, legal hold) before disruptive containment.

**Related labs:** [[../siem-ransomware-mitre/notes|SIEM MITRE]] (live triage) · [[../ransomware-dr-acme/notes|Ransomware DR]] (DR activation order)
