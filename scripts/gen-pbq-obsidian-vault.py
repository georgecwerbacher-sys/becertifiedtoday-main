#!/usr/bin/env python3
"""Generate marketing-vault/SEC+/PBQ/{slug}/ notes for ported pending scenarios."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "marketing-vault/SEC+/PBQ"

SCENARIOS = [
    {
        "slug": "log-timeline-forensics",
        "title": "Log Timeline Forensics",
        "section": "log-timeline",
        "summary": "Reorder six SSH auth log snippets from brute-force attempts through privilege escalation and persistence.",
        "sy0": "**2.4** log analysis · **2.5** incident response timeline",
        "key": "Chronological order: failed-login → multiple-retries → successful-login → sudo-escalation → new-user → cron-job",
        "prev": "wap-secure-configuration",
        "next": "pki-certificate-chain-browser-error",
        "tips": "Pair with [[../ubuntu-ssh-breach-hardening/notes|Ubuntu SSH breach]] — same narrative, different skill (ordering vs hardening).",
    },
    {
        "slug": "pki-certificate-chain-browser-error",
        "title": "PKI Certificate Chain — Browser Error",
        "section": "pki-browser-error",
        "summary": "PKI chain exhibit plus MCQ on NET::ERR_CERT_AUTHORITY_INVALID troubleshooting.",
        "sy0": "**1.4** PKI/TLS trust paths",
        "key": "MCQ **B** — missing intermediate CA; serve full chain or distribute enterprise root via GPO",
        "prev": "log-timeline-forensics",
        "next": "phishing-email-analysis",
        "tips": "Contrast with [[../hybrid-pki-audit/notes|Hybrid PKI audit]] (chain order, algorithms, revocation).",
    },
    {
        "slug": "phishing-email-analysis",
        "title": "Phishing Email Analysis",
        "section": "phishing-analysis",
        "summary": "Suspicious email exhibit with eight-blank social-engineering term fill-in.",
        "sy0": "**2.1** social engineering · **4.3** security awareness",
        "key": "typosquatting · pretexting · phishing · spear phishing · smishing · vishing · brand impersonation · report",
        "prev": "pki-certificate-chain-browser-error",
        "next": "vulnerability-management",
        "tips": "Red-flag list in exhibit maps directly to blanks — good teaching walkthrough.",
    },
    {
        "slug": "vulnerability-management",
        "title": "Vulnerability Management",
        "section": "vuln-management",
        "summary": "Credentialed scan exhibit (Log4Shell CVSS 10) — choose compensating control during change freeze.",
        "sy0": "**4.2** vulnerability management · **4.1** compensating controls",
        "key": "MCQ **A** — WAF/IPS block JNDI patterns + restrict outbound LDAP",
        "prev": "phishing-email-analysis",
        "next": "incident-response",
        "tips": "Emphasize patch-first vs compensating control when deployment is blocked.",
    },
    {
        "slug": "incident-response",
        "title": "Incident Response — Ransomware IR",
        "section": "incident-response",
        "summary": "NIST SP 800-61 ransomware timeline exhibit with eight IR/forensics term blanks.",
        "sy0": "**2.5** incident response · NIST SP 800-61",
        "key": "analysis · containment · lessons learned · image · chain of custody · legal hold · tabletop exercise · eradication",
        "prev": "vulnerability-management",
        "next": "quantitative-risk-ale",
        "tips": "Complements [[../siem-ransomware-mitre/notes|SIEM MITRE]] and [[../ransomware-dr-acme/notes|Ransomware DR]] — vocabulary vs live triage vs DR steps.",
    },
    {
        "slug": "quantitative-risk-ale",
        "title": "Quantitative Risk — ALE",
        "section": "risk-ale",
        "summary": "SLE/ARO/ALE worksheet exhibit plus security awareness training ROI MCQ.",
        "sy0": "**1.2** risk management · quantitative analysis",
        "key": "MCQ **B** — training ROI (ALE reduction vs program cost)",
        "prev": "incident-response",
        "next": "malware-ioc-analysis",
        "tips": "Walk through SLE × ARO = ALE before answering ROI question.",
    },
    {
        "slug": "malware-ioc-analysis",
        "title": "Malware IOC Analysis",
        "section": "malware-ioc",
        "summary": "Endpoint IOC console (process, network, persistence) plus malware classification MCQ.",
        "sy0": "**2.4** malware analysis · **4.5** endpoint detection",
        "key": "MCQ **C** — see exhibit IOC patterns (process injection, C2, Run key persistence)",
        "prev": "quantitative-risk-ale",
        "next": "data-protection",
        "tips": "Map each IOC column to ATT&CK tactics when teaching.",
    },
    {
        "slug": "data-protection",
        "title": "Data Protection",
        "section": "data-protection",
        "summary": "Data classification/states exhibit plus PCI test-data tokenization MCQ.",
        "sy0": "**1.3** data sensitivity · **4.3** protection methods",
        "key": "MCQ **C** — tokenization for PCI test environments",
        "prev": "malware-ioc-analysis",
        "next": "governance",
        "tips": "Contrast tokenization vs encryption vs masking in exhibit.",
    },
    {
        "slug": "governance",
        "title": "Governance",
        "section": "governance",
        "summary": "Frameworks, policy types, vendor agreements, and parallel GDPR/PCI breach notification MCQ.",
        "sy0": "**5.1** governance · **5.2** compliance · **5.5** policies",
        "key": "MCQ **D** — GDPR and PCI DSS both apply; parallel notification obligations",
        "prev": "data-protection",
        "next": None,
        "tips": "End of PBQ chain — good capstone for compliance overlap scenarios.",
    },
]


def notes(sc: dict) -> str:
    chain = f"**Previous:** [[../{sc['prev']}/notes|{sc['prev']}]]"
    if sc["next"]:
        chain += f" · **Next:** [[../{sc['next']}/notes|{sc['next']}]]"
    else:
        chain += " · End of chain."
    return f"""---
type: pbq-scenario-notes
exam: SY0-701
scenario: {sc['slug']}
title: {sc['title']}
status: production
last_updated: 2026-06-05
---

# {sc['title']} — notes

## What this lab tests

{sc['summary']}

## SY0-701 alignment

{sc['sy0']}

## Page structure

| Section ID | Content |
|------------|---------|
| `{sc['section']}` | Single-section scenario (ported from `pending/`) |

{chain}

## Answer key (summary)

{sc['key']}

## Local preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/{sc['slug']}/{sc['slug']}.html
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/{sc['slug']}/{sc['slug']}.html#{sc['section']}
```

→ [[recommendations]] · [[deep-dive-solution]]
"""


def recommendations(sc: dict) -> str:
    return f"""---
type: pbq-scenario-recommendations
exam: SY0-701
scenario: {sc['slug']}
last_updated: 2026-06-05
---

# {sc['title']} — recommendations

## For learners

{sc['tips']}

## For instructors

| Priority | Recommendation |
|----------|----------------|
| High | Use Show Answer, then walk exhibit → key mapping aloud. |
| Medium | Tie stem to SY0-701 objective wording in {sc['sy0']}. |
| Low | Clip folder-sidebar navigation for short-form video. |

## Maintenance

- Edit `sections/{sc['section']}.html` → `npm run build:pbq-suite`
- Answer audit: `PBQ_Production/VERIFICATION.md` § scenario row for `{sc['slug']}`
"""


def deep_dive(sc: dict) -> str:
    return f"""---
type: pbq-scenario-solution
exam: SY0-701
scenario: {sc['slug']}
last_updated: 2026-06-05
---

# {sc['title']} — deep dive solution

> {sc['summary']}

---

## Correct answer

{sc['key']}

---

## Why it matters (exam lens)

{sc['sy0']}

---

## Distractor patterns

Review wrong choices in the live page — each MCQ/fill-in distractor targets a common SY0-701 misconception (wrong control order, wrong framework scope, or wrong IR phase).

---

## Related labs

{sc['tips']}

---

## Source

Ported from `public/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/pending/{sc['slug']}.html` (2026-06-05).
"""


def main() -> None:
    for sc in SCENARIOS:
        d = VAULT / sc["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "notes.md").write_text(notes(sc), encoding="utf-8")
        (d / "recommendations.md").write_text(recommendations(sc), encoding="utf-8")
        (d / "deep-dive-solution.md").write_text(deep_dive(sc), encoding="utf-8")
        print(f"vault {sc['slug']}")


if __name__ == "__main__":
    main()
