#!/usr/bin/env python3
"""Build one HTML page per PBQ scenario (folder sections + exhibit modals)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PBQ = ROOT / "public/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production"
BASE_URL = "/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production"

SCENARIOS = [
    {
        "slug": "acme-rag-hr-ai",
        "title": "HR RAG Assistant — AI Security Hardening",
        "body_class": "pbq-ai-rag",
        "objectives": "3.1 · 3.3 · 5.5",
        "suite_instructions": "Open <strong>Case exhibits</strong> first, then work through configuration, guardrails, attack mitigations, and the AI attack MCQs.",
        "description": "BeCertifiedToday rolled out a generative HR assistant backed by a policy vector store. Review the case exhibits, secure configuration and guardrails, then match each AI attack to the right mitigation.",
        "prev": None,
        "next": "zero-trust-zta-migration",
        "sections": [
            {"id": "acme-exhibits", "label": "Case exhibits", "path": "acme-rag-hr-ai/sections/acme-exhibits.html"},
            {"id": "acme-config", "label": "Task 1 — Configuration", "path": "acme-rag-hr-ai/sections/acme-config.html"},
            {"id": "acme-guardrails", "label": "Task 2 — Guardrails", "path": "acme-rag-hr-ai/sections/acme-guardrails.html"},
            {"id": "acme-attacks", "label": "Task 3 — Attack mitigations", "path": "acme-rag-hr-ai/sections/acme-attacks.html"},
            {"id": "acme-p2", "label": "Part 2 — AI attack MCQs", "path": "acme-rag-hr-ai/sections/acme-p2.html"},
        ],
    },
    {
        "slug": "zero-trust-zta-migration",
        "title": "Zero Trust Architecture: Zone Migration",
        "body_class": "pbq-zta-zone-map pbq-zero-trust dragdrop-exercise",
        "objectives": "1.2 · 3.3 · 3.4",
        "suite_instructions": "Open the <strong>reference exhibit</strong>, answer the core concept question, then pick the best control for each zone.",
        "description": "BeCertifiedToday replaces implicit perimeter trust with NIST SP 800-207 Zero Trust. Open the reference exhibit, answer the core concept question, then pick the best control for each zone slot.",
        "prev": "acme-rag-hr-ai",
        "next": "hybrid-pki-audit",
        "sections": [
            {"id": "zta-exhibit", "label": "Reference exhibit", "path": "zero-trust-zta-migration/sections/zta-exhibit.html"},
            {"id": "zta-concept", "label": "Core concept", "path": "zero-trust-zta-migration/sections/zta-concept.html"},
            {"id": "zta-p2", "label": "Zone control map", "path": "zero-trust-zta-migration/sections/zta-p2.html"},
            {"id": "zta-p3", "label": "Trade-off decisions", "path": "zero-trust-zta-migration/sections/zta-p3.html"},
        ],
    },
    {
        "slug": "hybrid-pki-audit",
        "title": "Hybrid PKI — Certificate Audit & Revocation",
        "body_class": "pbq-pki-audit dragdrop-exercise",
        "objectives": "1.4 · 4.6",
        "suite_instructions": "Complete each section in order: trust chain, algorithms, then revocation selection.",
        "description": "An audit of BeCertifiedToday's hybrid PKI flagged weak algorithms, stale CRLs, and an expired leaf. Build the TLS chain for api.becertifiedtoday.com, review crypto choices, and select certificates to revoke.",
        "prev": "zero-trust-zta-migration",
        "next": "ubuntu-ssh-breach-hardening",
        "sections": [
            {"id": "pki-p1", "label": "Part 1 — Trust chain", "path": "hybrid-pki-audit/sections/pki-p1.html"},
            {"id": "pki-p2", "label": "Part 2 — Algorithms", "path": "hybrid-pki-audit/sections/pki-p2.html"},
            {"id": "pki-p3", "label": "Part 3 — Revocation", "path": "hybrid-pki-audit/sections/pki-p3.html"},
        ],
    },
    {
        "slug": "ubuntu-ssh-breach-hardening",
        "title": "Linux Server Breach — SSH Hardening & IR",
        "body_class": "pbq-ssh-harden",
        "objectives": "2.4 · 4.1 · 4.4",
        "suite_instructions": "Work through each config section, then grade your answers on <strong>Consequence review</strong>.",
        "description": "After brute-forced SSH credentials and attacker persistence on a Ubuntu 22.04 web server, harden sshd_config, fail2ban, and UFW — then answer consequence questions about lockout and eradication.",
        "prev": "hybrid-pki-audit",
        "next": "firewall-acl-secops",
        "sections": [
            {"id": "ubuntu-intro", "label": "Case briefing", "path": "ubuntu-ssh-breach-hardening/sections/ubuntu-intro.html"},
            {"id": "ubuntu-sshd", "label": "sshd_config", "path": "ubuntu-ssh-breach-hardening/sections/ubuntu-sshd.html"},
            {"id": "ubuntu-fail2ban", "label": "fail2ban jail", "path": "ubuntu-ssh-breach-hardening/sections/ubuntu-fail2ban.html"},
            {"id": "ubuntu-ufw", "label": "UFW rules", "path": "ubuntu-ssh-breach-hardening/sections/ubuntu-ufw.html"},
            {"id": "ubuntu-consequences", "label": "Consequence review", "path": "ubuntu-ssh-breach-hardening/sections/ubuntu-consequences.html"},
        ],
    },
    {
        "slug": "firewall-acl-secops",
        "title": "Three-Tier Firewall — ACL Rule Builder",
        "body_class": "pbq-acl-secops",
        "objectives": "3.3 · 4.1",
        "suite_instructions": "Review the <strong>three-tier topology</strong>, then build ACL rules top-down with explicit deny-all last.",
        "description": "BeCertifiedToday needs inbound web access and database isolation between DMZ tiers. Write four top-down ACL rows: separate HTTP and HTTPS permits, scoped MySQL, then explicit deny-all.",
        "prev": "ubuntu-ssh-breach-hardening",
        "next": "ransomware-dr-acme",
        "sections": [
            {
                "id": "firewall-acl-config",
                "label": "ACL rule table",
                "path": "firewall-acl-secops/sections/firewall-acl-config.html",
            },
        ],
    },
    {
        "slug": "ransomware-dr-acme",
        "title": "Ransomware Crisis — Disaster Recovery Plan",
        "body_class": "pbq-dr-ransomware dragdrop-exercise",
        "objectives": "3.1 · 5.6",
        "suite_instructions": "Read the constraint cards, then complete activation order, recovery targets, and cost trade-offs.",
        "description": "Ransomware encrypted BeCertifiedToday's primary data center under a 4-hour RTO, 6-hour backup window, and $2M budget. Order DR activation steps, pick recovery targets, and justify cost trade-offs.",
        "prev": "firewall-acl-secops",
        "next": "siem-ransomware-mitre",
        "sections": [
            {"id": "dr-overview", "label": "Scenario constraints", "path": "ransomware-dr-acme/sections/dr-overview.html"},
            {"id": "dr-part1-order", "label": "Part 1 — DR activation", "path": "ransomware-dr-acme/sections/dr-part1-order.html"},
            {"id": "dr-part2-targets", "label": "Part 2 — RTO/RPO & site", "path": "ransomware-dr-acme/sections/dr-part2-targets.html"},
            {"id": "dr-part3-tradeoffs", "label": "Part 3 — Cost trade-offs", "path": "ransomware-dr-acme/sections/dr-part3-tradeoffs.html"},
        ],
    },
    {
        "slug": "siem-ransomware-mitre",
        "title": "Ransomware Attack — SIEM Triage & MITRE Mapping",
        "body_class": "pbq-siem-ransomware",
        "objectives": "2.4 · 4.4 · 4.7",
        "suite_instructions": "Review the attack timeline, then author the Sigma rule, map MITRE techniques, and choose containment actions.",
        "description": "Seven correlated SIEM alerts trace a Word-to-PowerShell stager through lateral movement. Author a Sigma detection rule, map events to MITRE ATT&CK, and decide containment actions.",
        "prev": "ransomware-dr-acme",
        "next": "advanced-firewall-rule-configurator",
        "sections": [
            {"id": "siem-overview", "label": "Attack timeline", "path": "siem-ransomware-mitre/sections/siem-overview.html"},
            {"id": "siem-part1-sigma", "label": "Part 1 — Sigma rule", "path": "siem-ransomware-mitre/sections/siem-part1-sigma.html"},
            {"id": "siem-part2-mitre", "label": "Part 2 — MITRE mapping", "path": "siem-ransomware-mitre/sections/siem-part2-mitre.html"},
            {"id": "siem-part3-containment", "label": "Part 3 — Containment", "path": "siem-ransomware-mitre/sections/siem-part3-containment.html"},
        ],
    },
    {
        "slug": "advanced-firewall-rule-configurator",
        "title": "Perimeter Firewall: Policy Rule Configurator",
        "body_class": "pbq-afw-config",
        "objectives": "3.3 · 4.1",
        "suite_instructions": "Review the <strong>network topology</strong> exhibit, then add ACL rules to satisfy each policy requirement.",
        "description": "Configure BeCertifiedToday's edge firewall with free-text CIDR and direction fields: permit inbound HTTPS and scoped SSH, deny Telnet, allow outbound DNS, and finish with implicit deny-all.",
        "prev": "siem-ransomware-mitre",
        "next": "security-control-placement",
        "sections": [
            {
                "id": "advanced-firewall-config",
                "label": "Rule builder",
                "path": "advanced-firewall-rule-configurator/sections/advanced-firewall-config.html",
            },
        ],
    },
    {
        "slug": "security-control-placement",
        "title": "Defense in Depth — Control Placement Map",
        "body_class": "pbq-sec-control-map dragdrop-exercise",
        "objectives": "3.2 · 3.3 · 4.1",
        "suite_instructions": "Drag each security control into the zone where it belongs on the architecture diagram.",
        "description": "BeCertifiedToday's Internet, DMZ, and internal diagram needs the right controls in each zone. Drag firewall, WAF, IDS, honeypot, NAC, and SIEM into the slots that match the architecture.",
        "prev": "advanced-firewall-rule-configurator",
        "next": "subnetting-ip-addressing",
        "sections": [
            {
                "id": "sec-control-placement",
                "label": "Zone placement map",
                "path": "security-control-placement/sections/sec-control-placement.html",
            },
        ],
    },
    {
        "slug": "subnetting-ip-addressing",
        "title": "Office Expansion — Subnet Design",
        "body_class": "pbq-subnet-ip",
        "objectives": "3.3 · 4.3",
        "suite_instructions": "Choose the prefix that yields at least six subnets, then assign the first three networks to Sales, HR, and IT.",
        "description": "A growing office must split 192.168.10.0/24 into at least six subnets while maximizing usable hosts. Choose the right prefix, then assign the first three /27 networks to Sales, HR, and IT.",
        "prev": "security-control-placement",
        "next": "ubuntu-cis-hardening",
        "sections": [
            {
                "id": "subnet-ip-config",
                "label": "Subnet calculator",
                "path": "subnetting-ip-addressing/sections/subnet-ip-config.html",
            },
        ],
    },
    {
        "slug": "ubuntu-cis-hardening",
        "title": "Baseline Audit Failure — CIS Hardening",
        "body_class": "pbq-cis-harden pbq-ssh-harden",
        "objectives": "1.4 · 4.1 · 4.4",
        "suite_instructions": "Complete the hardening checklist, <strong>sshd_config</strong>, and <strong>pwquality.conf</strong> sections in order.",
        "description": "A Ubuntu 22.04 host failed its CIS baseline audit. Complete the hardening checklist, fix sshd_config to CIS expectations, and set pwquality.conf password requirements.",
        "prev": "subnetting-ip-addressing",
        "next": "wap-secure-configuration",
        "sections": [
            {
                "id": "harden-checklist",
                "label": "Hardening checklist",
                "path": "ubuntu-cis-hardening/sections/harden-checklist.html",
            },
            {
                "id": "harden-sshd",
                "label": "sshd_config",
                "path": "ubuntu-cis-hardening/sections/harden-sshd.html",
            },
            {
                "id": "harden-pwquality",
                "label": "pwquality.conf",
                "path": "ubuntu-cis-hardening/sections/harden-pwquality.html",
            },
        ],
    },
    {
        "slug": "wap-secure-configuration",
        "title": "Corporate Wireless — Secure AP Configuration",
        "body_class": "pbq-wap-config",
        "objectives": "1.4 · 3.3 · 4.1",
        "suite_instructions": "Configure the access point to meet corporate wireless policy, then check your settings.",
        "description": "Bring a corporate access point in line with policy: WPA3-Enterprise with 802.1X, disable WPS, hide the SSID, enable guest isolation, and pick the least-congested 5 GHz channel.",
        "prev": "ubuntu-cis-hardening",
        "next": "log-timeline-forensics",
        "sections": [
            {
                "id": "wap-secure-config",
                "label": "WAP settings panel",
                "path": "wap-secure-configuration/sections/wap-secure-config.html",
            },
        ],
    },
    {
        "slug": "log-timeline-forensics",
        "title": "SSH Breach Timeline — Log Reconstruction",
        "body_class": "dragdrop-exercise",
        "objectives": "2.4 · 2.5",
        "suite_instructions": "Drag the log snippets into chronological order to reconstruct the SSH breach timeline.",
        "description": "Six out-of-order SSH authentication log snippets describe a brute-force intrusion through privilege escalation. Drag them into chronological order to reconstruct the attack path.",
        "prev": "wap-secure-configuration",
        "next": "pki-certificate-chain-browser-error",
        "sections": [
            {
                "id": "log-timeline",
                "label": "Log timeline",
                "path": "log-timeline-forensics/sections/log-timeline.html",
            },
        ],
    },
    {
        "slug": "pki-certificate-chain-browser-error",
        "title": "TLS Browser Error — Certificate Chain Fix",
        "body_class": "pbq-exhibit-mcq",
        "objectives": "1.4",
        "suite_instructions": "Review the <strong>certificate chain exhibit</strong>, then choose the fix that restores trust.",
        "description": "Users see NET::ERR_CERT_AUTHORITY_INVALID when connecting to an internal HTTPS service. Review the PKI chain exhibit and choose the fix that restores trust without weakening validation.",
        "prev": "log-timeline-forensics",
        "next": "phishing-email-analysis",
        "sections": [
            {
                "id": "pki-browser-error",
                "label": "Chain exhibit & MCQ",
                "path": "pki-certificate-chain-browser-error/sections/pki-browser-error.html",
            },
        ],
    },
    {
        "slug": "phishing-email-analysis",
        "title": "Suspicious Inbox — Phishing Email Analysis",
        "body_class": "pbq-phishing-analysis dragdrop-exercise",
        "objectives": "2.1 · 4.3",
        "suite_instructions": "Study the <strong>email exhibit</strong>, then drag each term into the matching analysis sentence.",
        "description": "A suspicious message impersonates Microsoft 365 support. Study the email exhibit and drag each social-engineering term into the analysis paragraph that matches the red flags.",
        "prev": "pki-certificate-chain-browser-error",
        "next": "vulnerability-management",
        "sections": [
            {
                "id": "phishing-analysis",
                "label": "Email analysis",
                "path": "phishing-email-analysis/sections/phishing-analysis.html",
            },
        ],
    },
    {
        "slug": "vulnerability-management",
        "title": "Critical CVE — Vulnerability Response",
        "body_class": "pbq-exhibit-mcq",
        "objectives": "4.1 · 4.2",
        "suite_instructions": "Review the <strong>scan exhibit</strong>, then pick the best compensating control during the change freeze.",
        "description": "A credentialed scan found Log4Shell (CVSS 10) on production Java services during a change freeze. Review the scan exhibit and pick the best compensating control until patching is allowed.",
        "prev": "phishing-email-analysis",
        "next": "incident-response",
        "sections": [
            {
                "id": "vuln-management",
                "label": "Scan exhibit & response",
                "path": "vulnerability-management/sections/vuln-management.html",
            },
        ],
    },
    {
        "slug": "incident-response",
        "title": "Active Ransomware — NIST Incident Response",
        "body_class": "pbq-incident-response dragdrop-exercise",
        "objectives": "2.5",
        "suite_instructions": "Use the <strong>NIST IR timeline exhibit</strong> and fill in the correct terms for each phase.",
        "description": "A ransomware incident is underway at BeCertifiedToday. Use the NIST SP 800-61 timeline exhibit and fill in the correct IR and forensics terms for each phase of the response.",
        "prev": "vulnerability-management",
        "next": "quantitative-risk-ale",
        "sections": [
            {
                "id": "incident-response",
                "label": "NIST IR timeline",
                "path": "incident-response/sections/incident-response.html",
            },
        ],
    },
    {
        "slug": "quantitative-risk-ale",
        "title": "Risk Register — ALE & Training ROI",
        "body_class": "pbq-exhibit-mcq pbq-risk-ale",
        "objectives": "1.2",
        "suite_instructions": "Work through the <strong>ALE worksheet</strong>, then select the calculation that supports the training investment.",
        "description": "The CISO needs quantitative justification for a $50,000 security awareness program. Work through the ALE worksheet (SLE × ARO) and select the calculation that supports the investment.",
        "prev": "incident-response",
        "next": "malware-ioc-analysis",
        "sections": [
            {
                "id": "risk-ale",
                "label": "ALE worksheet",
                "path": "quantitative-risk-ale/sections/risk-ale.html",
            },
        ],
    },
    {
        "slug": "malware-ioc-analysis",
        "title": "Endpoint Alert — Malware IOC Triage",
        "body_class": "pbq-exhibit-mcq pbq-malware-ioc",
        "objectives": "2.4 · 4.5",
        "suite_instructions": "Review the <strong>IOC exhibit</strong>, then classify the malware that best fits the evidence.",
        "description": "SOC analysts pulled process, network, and persistence indicators from an infected Windows endpoint. Review the IOC exhibit and classify the malware combination that best fits the evidence.",
        "prev": "quantitative-risk-ale",
        "next": "data-protection",
        "sections": [
            {
                "id": "malware-ioc",
                "label": "IOC exhibit & classification",
                "path": "malware-ioc-analysis/sections/malware-ioc.html",
            },
        ],
    },
    {
        "slug": "data-protection",
        "title": "PCI Test Environment — Data Protection Methods",
        "body_class": "pbq-exhibit-mcq pbq-data-protection",
        "objectives": "1.3 · 4.3",
        "suite_instructions": "Review the <strong>data protection exhibit</strong>, then choose the best approach for PCI test data.",
        "description": "Developers need realistic payment-card test data without exposing PANs. Review classification levels, data states, and protection methods, then choose the right approach for the sandbox.",
        "prev": "malware-ioc-analysis",
        "next": "governance",
        "sections": [
            {
                "id": "data-protection",
                "label": "Protection methods exhibit",
                "path": "data-protection/sections/data-protection.html",
            },
        ],
    },
    {
        "slug": "governance",
        "title": "Governance & Compliance: Breach Notification",
        "body_class": "pbq-exhibit-mcq pbq-governance",
        "objectives": "5.1 · 5.2 · 5.5",
        "suite_instructions": "Review the <strong>governance exhibit</strong>, then answer the breach notification question.",
        "description": "As the new CISO at BeCertifiedToday, align policy, vendor risk, and breach notification with frameworks and regulations. A breach exposes EU personal data and payment cards; identify which notification obligations apply.",
        "prev": "data-protection",
        "next": None,
        "sections": [
            {
                "id": "governance",
                "label": "Governance exhibit",
                "path": "governance/sections/governance.html",
            },
        ],
    },
]

CROSS_SECTION_IDS: set[str] = set()
for _sc in SCENARIOS:
    for _sec in _sc["sections"]:
        CROSS_SECTION_IDS.add(_sec["id"])

LEGACY_REDIRECTS: dict[str, tuple[str, str]] = {
    "acme-rag-hr-ai/acme-rag-hr-ai-part1.html": ("acme-rag-hr-ai/acme-rag-hr-ai.html", "acme-exhibits"),
    "acme-rag-hr-ai/acme-rag-hr-ai-part2.html": ("acme-rag-hr-ai/acme-rag-hr-ai.html", "acme-p2"),
    "zero-trust-zta-migration/zero-trust-zta-migration-part1.html": ("zero-trust-zta-migration/zero-trust-zta-migration.html", "zta-exhibit"),
    "zero-trust-zta-migration/zero-trust-zta-migration-part2.html": ("zero-trust-zta-migration/zero-trust-zta-migration.html", "zta-p2"),
    "zero-trust-zta-migration/zero-trust-zta-migration-part3.html": ("zero-trust-zta-migration/zero-trust-zta-migration.html", "zta-p3"),
    "hybrid-pki-audit/hybrid-pki-audit-part1.html": ("hybrid-pki-audit/hybrid-pki-audit.html", "pki-p1"),
    "hybrid-pki-audit/hybrid-pki-audit-part2.html": ("hybrid-pki-audit/hybrid-pki-audit.html", "pki-p2"),
    "hybrid-pki-audit/hybrid-pki-audit-part3.html": ("hybrid-pki-audit/hybrid-pki-audit.html", "pki-p3"),
}

REDIRECT_STUB = """<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta http-equiv="refresh" content="0;url={url}" />
  <script>location.replace("{url}");</script>
  <title>Redirect — PBQ</title>
</head>
<body>
  <p><a href="{url}">Continue</a></p>
</body>
</html>
"""


def collect_ids(html: str) -> set[str]:
    return {m.group(1) for m in re.finditer(r'\bid="([a-zA-Z][\w-]*)"', html)}


def apply_id_prefix(html: str, prefix: str, ids: set[str]) -> str:
    if not prefix:
        return html
    out = html
    for old_id in sorted(ids, key=len, reverse=True):
        if old_id.startswith(f"{prefix}-") or old_id in CROSS_SECTION_IDS:
            continue
        new_id = f"{prefix}-{old_id}"
        out = re.sub(rf'\bid="{re.escape(old_id)}"', f'id="{new_id}"', out)
        out = re.sub(
            rf"getElementById\(\s*['\"]{re.escape(old_id)}['\"]\s*\)",
            f'getElementById("{new_id}")',
            out,
        )
        out = re.sub(
            rf"querySelector\(\s*['\"]#{re.escape(old_id)}['\"]\s*\)",
            f'querySelector("#{new_id}")',
            out,
        )
        out = re.sub(
            rf"querySelectorAll\(\s*['\"]#{re.escape(old_id)}['\"]\s*\)",
            f'querySelectorAll("#{new_id}")',
            out,
        )
    return out


def prefix_section(html: str, prefix: str) -> str:
    return apply_id_prefix(html, prefix, collect_ids(html))


def prefix_script(script: str, prefix: str, inner_html: str) -> str:
    script = apply_id_prefix(script, prefix, collect_ids(inner_html))
    for sid in CROSS_SECTION_IDS:
        script = script.replace(f'"{prefix}-{sid}"', f'"{sid}"')
        script = script.replace(f"#{prefix}-{sid}", f"#{sid}")
    return script


def strip_duplicate_headers(inner: str, first: bool) -> str:
    if first:
        return inner
    inner = re.sub(r"<h1[^>]*>.*?</h1>\s*", "", inner, count=1, flags=re.DOTALL | re.IGNORECASE)
    inner = re.sub(r"<p\s+class=\"pbq-sub\"[^>]*>.*?</p>\s*", "", inner, count=1, flags=re.DOTALL | re.IGNORECASE)
    inner = re.sub(
        r"<p\s+class=\"pbq-instructions\"[^>]*>.*?</p>\s*",
        "",
        inner,
        count=1,
        flags=re.DOTALL | re.IGNORECASE,
    )
    return inner.strip()


def load_section_content(sec: dict) -> tuple[str, str]:
    path = PBQ / sec["path"]
    html = path.read_text(encoding="utf-8")
    script_re = re.compile(r"<script(?![^>]*src=)[^>]*>.*?</script>", re.DOTALL | re.IGNORECASE)
    scripts = ""
    for sm in script_re.finditer(html):
        scripts += sm.group(0) + "\n"
    m = re.search(r"<article[^>]*>(.*)</article>", html, re.DOTALL)
    inner = m.group(1).strip() if m else html.strip()
    inner = script_re.sub("", inner).strip()
    return inner, scripts.strip()


def build_folder_nav(scenario: dict) -> str:
    if len(scenario["sections"]) <= 1:
        return ""
    parts = [
        '<nav class="pbq-suite-folders pbq-suite-folders--flat" aria-label="Sections">',
        '<p class="pbq-suite-folders__label"><span aria-hidden="true">📁</span> Sections</p>',
        '<ul class="pbq-suite-folders__list">',
    ]
    for sec in scenario["sections"]:
        parts.append(
            f'<li><button type="button" class="pbq-suite-folder__item" '
            f'data-section="{sec["id"]}">{sec["label"]}</button></li>'
        )
    parts.append("</ul></nav>")
    return "\n".join(parts)


def build_scenario_sections(scenario: dict) -> tuple[str, str]:
    panels: list[str] = []
    scripts: list[str] = []
    first = True
    for sec in scenario["sections"]:
        inner, script = load_section_content(sec)
        inner = strip_duplicate_headers(inner, first)
        inner_for_script = inner
        inner = prefix_section(inner, sec["id"])
        panels.append(
            f'<article class="pbq-suite-section" id="{sec["id"]}" '
            f'data-scenario="{scenario["slug"]}" hidden>'
            f'<div class="pbq-suite-section__inner">{inner}</div>'
            f"</article>"
        )
        if script:
            scripts.append(f"<!-- {sec['id']} -->\n{prefix_script(script, sec['id'], inner_for_script)}")
        first = False
    return "\n".join(panels), "\n".join(scripts)


def nav_link(scenario: dict, which: str) -> str:
    slug = scenario.get(which)
    if not slug:
        pos = "nav-prev" if which == "prev" else "nav-next"
        label = "Back" if which == "prev" else "Next"
        return f'<span class="nav-link {pos} nav-link--disabled" aria-hidden="true">{label}</span>'
    label = "Back" if which == "prev" else "Next"
    cls = "nav-link nav-prev" if which == "prev" else "nav-link nav-next next-link"
    return f'<a class="{cls}" href="{BASE_URL}/{slug}/{slug}.html">{label}</a>'


def build_suite_instructions(scenario: dict) -> str:
    text = scenario.get("suite_instructions")
    if text:
        return text
    if len(scenario["sections"]) > 1:
        return (
            "Use the <strong>section list</strong> to work through each task in order. "
            "Complete every section before you move on."
        )
    return "Read the scenario, complete the task below, then use <strong>Check answer</strong>."


def build_objectives_block(scenario: dict) -> str:
    objs = scenario.get("objectives")
    if not objs:
        return ""
    return (
        f'        <p class="pbq-suite-objectives" aria-label="SY0-701 exam objectives covered">'
        f"Covers SY0-701 objectives: {objs}</p>\n"
    )


def build_question_nav(scenario: dict, *, footer: bool = False) -> str:
    modifier = " question-nav--footer" if footer else ""
    label = "Question navigation (footer)" if footer else "Question navigation"
    return f"""      <nav class="question-nav{modifier}" aria-label="{label}">
        <div class="question-nav-links">
          {nav_link(scenario, "prev")}
          <a class="nav-link nav-home" href="/COMP_TIA_SEC+/SEC+_Training_Portal.html">Home</a>
          {nav_link(scenario, "next")}
        </div>
      </nav>"""


def build_scenario_page(scenario: dict) -> str:
    slug = scenario["slug"]
    page_url = f"{BASE_URL}/{slug}/{slug}.html"
    panels, scripts = build_scenario_sections(scenario)
    nav = build_folder_nav(scenario)
    first_section = scenario["sections"][0]["id"]
    layout_class = "pbq-suite-layout"
    if len(scenario["sections"]) <= 1:
        layout_class += " pbq-suite-layout--single"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="robots" content="noindex, nofollow" />
  <meta name="description" content="CompTIA Security+ SY0-701 PBQ: {scenario['description']}" />
  <link rel="canonical" href="https://becertifiedtoday.com{page_url}" />
  <title>Security+ Simulation: {scenario['title']} | Be Certified Today</title>
  <link rel="stylesheet" href="/css/bcc-question-link-nav.css" />
  <link rel="stylesheet" href="/COMP_TIA_SEC+/SEC+_Samples/secplus-sample-touch.css" />
  <link rel="stylesheet" href="/COMP_TIA_SEC+/js/secplus-sim-page.css" />
  <link rel="stylesheet" href="/COMP_TIA_SEC+/js/secplus-sim-deep-dive.css" />
  <link rel="stylesheet" href="/COMP_TIA_SEC+/js/secplus-pbq-page.css" />
  <link rel="stylesheet" href="/COMP_TIA_SEC+/js/secplus-pbq-portal-chrome.css" />
</head>
<body class="secplus-question-ui secplus-sim-page secplus-pbq-ui pbq-bct-sim pbq-folder-suite {scenario['body_class']}">
  <script src="/js/sample-url-mask-apply.js"></script>
  <script src="/COMP_TIA_SEC+/js/secplus-pbq-portal-chrome.js"></script>
  <div class="page-logo-watermark" aria-hidden="true">
    <img src="/images/logo/becertifiedtoday_logo_image_trans.png" alt="" />
  </div>
  <div class="question-shell question-shell--suite">
    <a class="site-logo-corner" href="/COMP_TIA_SEC+/SEC+_Training_Portal.html" aria-label="Security+ practice portal">
      <img src="/images/logo/becertifiedtoday_logo_trans.png" width="52" height="52" alt="Be Certified Today" />
    </a>
    <main class="pbq-card pbq-card--suite">
      <header class="pbq-suite-header">
        <p class="pbq-suite-eyebrow">SY0-701 PBQ · BeCertifiedToday</p>
{build_objectives_block(scenario)}        <h1>Simulation: {scenario['title']}</h1>
        <p class="lead pbq-sub">{scenario['description']}</p>
        <p class="instructions pbq-instructions">
          {build_suite_instructions(scenario)}
        </p>
      </header>

      <div class="{layout_class}">
        {nav}
        <div class="pbq-suite-main" id="pbqSuiteMain">
          {panels}
        </div>
      </div>

      <div class="pbq-suite-footer">
        <div class="pbq-suite-footer__deep-dive">
          <button type="button" class="deep-dive-btn" id="pbqDeepDiveBtn" data-deep-dive-key="{slug}.html">Deep dive explanation</button>
        </div>
{build_question_nav(scenario, footer=True)}
      </div>
    </main>
  </div>

  <script src="/COMP_TIA_SEC+/js/pbq-folder-suite.js"></script>
  <script>window.PBQ_SUITE_DEFAULT_SECTION = "{first_section}"; window.PBQ_DEEP_DIVE_KEY = "{slug}.html";</script>
  {scripts}
  <script src="/COMP_TIA_SEC+/js/secplus-pbq-deep-dive-data.js"></script>
  <script src="/COMP_TIA_SEC+/js/secplus-deep-dive-modal.js"></script>
  <script src="/COMP_TIA_SEC+/js/secplus-pbq-deep-dive.js"></script>
</body>
</html>
"""


def write_redirects() -> None:
    for rel, (page, section_id) in LEGACY_REDIRECTS.items():
        url = f"{BASE_URL}/{page}#{section_id}"
        (PBQ / rel).write_text(REDIRECT_STUB.format(url=url), encoding="utf-8")


def main() -> None:
    import importlib.util
    import sys

    written: list[str] = []
    for scenario in SCENARIOS:
        slug = scenario["slug"]
        out = PBQ / slug / f"{slug}.html"
        out.write_text(build_scenario_page(scenario), encoding="utf-8")
        written.append(str(out.relative_to(ROOT)))
    write_redirects()
    print("wrote " + ", ".join(written))

    sys.path.insert(0, str(ROOT / "scripts"))
    from pbq_deep_dive_md import write_deep_dive_js

    dive_out = ROOT / "public/COMP_TIA_SEC+/js/secplus-pbq-deep-dive-data.js"
    dive_count = write_deep_dive_js([sc["slug"] for sc in SCENARIOS], dive_out)
    print(f"wrote {dive_out.relative_to(ROOT)} ({dive_count} scenarios)")


if __name__ == "__main__":
    main()
