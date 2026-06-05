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
        "title": "BeCertifiedToday RAG HR AI",
        "body_class": "pbq-ai-rag",
        "description": "Secure BeCertifiedToday HR RAG — exhibits, configuration, guardrails, attack mitigations, and AI attack MCQs.",
        "prev": None,
        "next": "zero-trust-zta-migration",
        "sections": [
            {"id": "acme-exhibits", "label": "Exhibits & architecture", "path": "acme-rag-hr-ai/sections/acme-exhibits.html"},
            {"id": "acme-config", "label": "System configuration", "path": "acme-rag-hr-ai/sections/acme-config.html"},
            {"id": "acme-guardrails", "label": "Guardrails", "path": "acme-rag-hr-ai/sections/acme-guardrails.html"},
            {"id": "acme-attacks", "label": "Attack mitigations", "path": "acme-rag-hr-ai/sections/acme-attacks.html"},
            {"id": "acme-p2", "label": "AI attack MCQs (Part 2)", "path": "acme-rag-hr-ai/sections/acme-p2.html"},
        ],
    },
    {
        "slug": "zero-trust-zta-migration",
        "title": "Zero Trust migration",
        "body_class": "pbq-zta-zone-map pbq-zero-trust dragdrop-exercise",
        "description": "BeCertifiedToday ZTA migration — exhibit, core concept, zone control map, and trade-off questions.",
        "prev": "acme-rag-hr-ai",
        "next": "hybrid-pki-audit",
        "sections": [
            {"id": "zta-exhibit", "label": "Reference exhibit", "path": "zero-trust-zta-migration/sections/zta-exhibit.html"},
            {"id": "zta-concept", "label": "Core concept (MCQ)", "path": "zero-trust-zta-migration/sections/zta-concept.html"},
            {"id": "zta-p2", "label": "Zone control map", "path": "zero-trust-zta-migration/sections/zta-p2.html"},
            {"id": "zta-p3", "label": "Trade-off questions", "path": "zero-trust-zta-migration/sections/zta-p3.html"},
        ],
    },
    {
        "slug": "hybrid-pki-audit",
        "title": "Hybrid PKI audit",
        "body_class": "pbq-pki-audit dragdrop-exercise",
        "description": "Hybrid PKI audit for api.becertifiedtoday.com — chain order, algorithms, and revocation.",
        "prev": "zero-trust-zta-migration",
        "next": "ubuntu-ssh-breach-hardening",
        "sections": [
            {"id": "pki-p1", "label": "Certificate chain order", "path": "hybrid-pki-audit/sections/pki-p1.html"},
            {"id": "pki-p2", "label": "Algorithm review", "path": "hybrid-pki-audit/sections/pki-p2.html"},
            {"id": "pki-p3", "label": "Revocation scope", "path": "hybrid-pki-audit/sections/pki-p3.html"},
        ],
    },
    {
        "slug": "ubuntu-ssh-breach-hardening",
        "title": "Ubuntu SSH breach hardening",
        "body_class": "pbq-ssh-harden",
        "description": "Ubuntu 22.04 post-breach hardening — sshd, fail2ban, UFW, and consequence questions.",
        "prev": "hybrid-pki-audit",
        "next": "firewall-acl-secops",
        "sections": [
            {"id": "ubuntu-intro", "label": "Overview & scores", "path": "ubuntu-ssh-breach-hardening/sections/ubuntu-intro.html"},
            {"id": "ubuntu-sshd", "label": "sshd_config", "path": "ubuntu-ssh-breach-hardening/sections/ubuntu-sshd.html"},
            {"id": "ubuntu-fail2ban", "label": "jail.local (fail2ban)", "path": "ubuntu-ssh-breach-hardening/sections/ubuntu-fail2ban.html"},
            {"id": "ubuntu-ufw", "label": "UFW rules", "path": "ubuntu-ssh-breach-hardening/sections/ubuntu-ufw.html"},
            {"id": "ubuntu-consequences", "label": "Consequence Qs & grade", "path": "ubuntu-ssh-breach-hardening/sections/ubuntu-consequences.html"},
        ],
    },
    {
        "slug": "firewall-acl-secops",
        "title": "Firewall ACL Configuration — Security Operations",
        "body_class": "pbq-acl-secops",
        "description": "Acme Corp firewall ACL — permit web and database tiers, explicit deny catch-all (top-down evaluation).",
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
        "title": "Ransomware DR — Acme Corp",
        "body_class": "pbq-dr-ransomware dragdrop-exercise",
        "description": "Ransomware DR activation — order 8 steps, RTO/RPO and warm site tier, cost vs. recovery trade-offs.",
        "prev": "firewall-acl-secops",
        "next": "siem-ransomware-mitre",
        "sections": [
            {"id": "dr-overview", "label": "Scenario constraints", "path": "ransomware-dr-acme/sections/dr-overview.html"},
            {"id": "dr-part1-order", "label": "Part 1 — DR step order", "path": "ransomware-dr-acme/sections/dr-part1-order.html"},
            {"id": "dr-part2-targets", "label": "Part 2 — RTO/RPO & site", "path": "ransomware-dr-acme/sections/dr-part2-targets.html"},
            {"id": "dr-part3-tradeoffs", "label": "Part 3 — Trade-offs", "path": "ransomware-dr-acme/sections/dr-part3-tradeoffs.html"},
        ],
    },
    {
        "slug": "siem-ransomware-mitre",
        "title": "SIEM ransomware — Sigma & MITRE",
        "body_class": "pbq-siem-ransomware",
        "description": "7 SIEM alerts — Sigma rule for Word/PowerShell stager, MITRE ATT&CK classification, containment decisions.",
        "prev": "ransomware-dr-acme",
        "next": "advanced-firewall-rule-configurator",
        "sections": [
            {"id": "siem-overview", "label": "Attack timeline", "path": "siem-ransomware-mitre/sections/siem-overview.html"},
            {"id": "siem-part1-sigma", "label": "Part 1 — Sigma rule", "path": "siem-ransomware-mitre/sections/siem-part1-sigma.html"},
            {"id": "siem-part2-mitre", "label": "Part 2 — MITRE stages", "path": "siem-ransomware-mitre/sections/siem-part2-mitre.html"},
            {"id": "siem-part3-containment", "label": "Part 3 — Containment", "path": "siem-ransomware-mitre/sections/siem-part3-containment.html"},
        ],
    },
    {
        "slug": "advanced-firewall-rule-configurator",
        "title": "Advanced Firewall Rule Configurator",
        "body_class": "pbq-afw-config",
        "description": "Acme Corp perimeter firewall — inbound HTTPS/SSH, deny Telnet, outbound DNS, implicit deny-all (top-down ACL).",
        "prev": "siem-ransomware-mitre",
        "next": "security-control-placement",
        "sections": [
            {
                "id": "advanced-firewall-config",
                "label": "ACL rule configurator",
                "path": "advanced-firewall-rule-configurator/sections/advanced-firewall-config.html",
            },
        ],
    },
    {
        "slug": "security-control-placement",
        "title": "Network Diagram — Security Control Placement",
        "body_class": "pbq-sec-control-map dragdrop-exercise",
        "description": "Acme Corp three-zone diagram — place firewall, WAF, IDS, honeypot, NAC, and SIEM in labeled slots.",
        "prev": "advanced-firewall-rule-configurator",
        "next": "subnetting-ip-addressing",
        "sections": [
            {
                "id": "sec-control-placement",
                "label": "Control placement map",
                "path": "security-control-placement/sections/sec-control-placement.html",
            },
        ],
    },
    {
        "slug": "subnetting-ip-addressing",
        "title": "Subnetting & IP Addressing Configuration",
        "body_class": "pbq-subnet-ip",
        "description": "Subnet 192.168.10.0/24 for ≥6 networks (maximize hosts), assign first three /27 subnets to Sales, HR, IT.",
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
        "title": "Ubuntu 22.04 baseline hardening",
        "body_class": "pbq-cis-harden pbq-ssh-harden",
        "description": "Failed baseline audit — hardening checklist, CIS sshd_config, and pwquality.conf password policy.",
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
        "title": "Wireless Access Point — Secure Configuration",
        "body_class": "pbq-wap-config",
        "description": "Corporate WAP — WPA3-Enterprise, 802.1X, hidden SSID, guest isolation, 5 GHz channel 149.",
        "prev": "ubuntu-cis-hardening",
        "next": "log-timeline-forensics",
        "sections": [
            {
                "id": "wap-secure-config",
                "label": "WAP settings",
                "path": "wap-secure-configuration/sections/wap-secure-config.html",
            },
        ],
    },
    {
        "slug": "log-timeline-forensics",
        "title": "Log Timeline Forensics",
        "body_class": "dragdrop-exercise",
        "description": "Reorder SSH auth log snippets to reconstruct a brute-force attack ending in privilege escalation.",
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
        "title": "PKI Certificate Chain — Browser Error",
        "body_class": "pbq-exhibit-mcq",
        "description": "PKI certificate chain exhibit and NET::ERR_CERT_AUTHORITY_INVALID troubleshooting.",
        "prev": "log-timeline-forensics",
        "next": "phishing-email-analysis",
        "sections": [
            {
                "id": "pki-browser-error",
                "label": "Browser cert error",
                "path": "pki-certificate-chain-browser-error/sections/pki-browser-error.html",
            },
        ],
    },
    {
        "slug": "phishing-email-analysis",
        "title": "Phishing Email Analysis",
        "body_class": "pbq-phishing-analysis dragdrop-exercise",
        "description": "Phishing email exhibit and drag-and-drop social engineering term matching.",
        "prev": "pki-certificate-chain-browser-error",
        "next": "vulnerability-management",
        "sections": [
            {
                "id": "phishing-analysis",
                "label": "Phishing analysis",
                "path": "phishing-email-analysis/sections/phishing-analysis.html",
            },
        ],
    },
    {
        "slug": "vulnerability-management",
        "title": "Vulnerability Management",
        "body_class": "pbq-exhibit-mcq",
        "description": "Vulnerability scanner exhibit and Log4Shell compensating controls during a change freeze.",
        "prev": "phishing-email-analysis",
        "next": "incident-response",
        "sections": [
            {
                "id": "vuln-management",
                "label": "Vulnerability scan",
                "path": "vulnerability-management/sections/vuln-management.html",
            },
        ],
    },
    {
        "slug": "incident-response",
        "title": "Incident Response — Ransomware IR",
        "body_class": "pbq-incident-response dragdrop-exercise",
        "description": "NIST SP 800-61 ransomware incident timeline and IR process fill-in drag-and-drop.",
        "prev": "vulnerability-management",
        "next": "quantitative-risk-ale",
        "sections": [
            {
                "id": "incident-response",
                "label": "NIST IR fill-in",
                "path": "incident-response/sections/incident-response.html",
            },
        ],
    },
    {
        "slug": "quantitative-risk-ale",
        "title": "Quantitative Risk — ALE",
        "body_class": "pbq-exhibit-mcq pbq-risk-ale",
        "description": "Quantitative risk analysis exhibit (SLE, ARO, ALE) and security awareness training ROI.",
        "prev": "incident-response",
        "next": "malware-ioc-analysis",
        "sections": [
            {
                "id": "risk-ale",
                "label": "Risk & ALE",
                "path": "quantitative-risk-ale/sections/risk-ale.html",
            },
        ],
    },
    {
        "slug": "malware-ioc-analysis",
        "title": "Malware IOC Analysis",
        "body_class": "pbq-exhibit-mcq pbq-malware-ioc",
        "description": "Endpoint malware IOC exhibit (process, network, persistence) and malware classification.",
        "prev": "quantitative-risk-ale",
        "next": "data-protection",
        "sections": [
            {
                "id": "malware-ioc",
                "label": "Malware IOCs",
                "path": "malware-ioc-analysis/sections/malware-ioc.html",
            },
        ],
    },
    {
        "slug": "data-protection",
        "title": "Data Protection",
        "body_class": "pbq-exhibit-mcq pbq-data-protection",
        "description": "Data classification, states, and protection methods exhibit plus PCI test-data tokenization.",
        "prev": "malware-ioc-analysis",
        "next": "governance",
        "sections": [
            {
                "id": "data-protection",
                "label": "Data protection",
                "path": "data-protection/sections/data-protection.html",
            },
        ],
    },
    {
        "slug": "governance",
        "title": "Governance",
        "body_class": "pbq-exhibit-mcq pbq-governance",
        "description": "Security governance frameworks, policies, vendor agreements, and breach notification obligations.",
        "prev": "data-protection",
        "next": None,
        "sections": [
            {
                "id": "governance",
                "label": "Governance",
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
    scripts = ""
    for sm in re.finditer(r"<script(?![^>]*src=)[^>]*>.*?</script>", html, re.DOTALL | re.IGNORECASE):
        scripts += sm.group(0) + "\n"
    m = re.search(r"<article[^>]*>(.*)</article>", html, re.DOTALL)
    inner = m.group(1).strip() if m else html.strip()
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
        inner = prefix_section(inner, sec["id"])
        panels.append(
            f'<article class="pbq-suite-section" id="{sec["id"]}" '
            f'data-scenario="{scenario["slug"]}" hidden>'
            f'<div class="pbq-suite-section__inner">{inner}</div>'
            f"</article>"
        )
        if script:
            scripts.append(f"<!-- {sec['id']} -->\n{prefix_script(script, sec['id'], inner)}")
        first = False
    return "\n".join(panels), "\n".join(scripts)


def nav_link(scenario: dict, which: str) -> str:
    slug = scenario.get(which)
    if not slug:
        return '<span class="nav-link nav-link--disabled" aria-hidden="true">' + ("Back" if which == "prev" else "Next") + "</span>"
    label = "Back" if which == "prev" else "Next"
    cls = "nav-link nav-prev" if which == "prev" else "nav-link nav-next next-link"
    return f'<a class="{cls}" href="{BASE_URL}/{slug}/{slug}.html">{label}</a>'


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
  <meta name="description" content="CompTIA Security+ SY0-701 PBQ — {scenario['description']}" />
  <link rel="canonical" href="https://becertifiedtoday.com{page_url}" />
  <title>Security+ PBQ — {scenario['title']} | Be Certified Today</title>
  <link rel="stylesheet" href="/css/bcc-question-link-nav.css" />
  <link rel="stylesheet" href="/COMP_TIA_SEC+/SEC+_Samples/secplus-sample-touch.css" />
  <link rel="stylesheet" href="/COMP_TIA_SEC+/js/secplus-pbq-page.css" />
</head>
<body class="secplus-question-ui secplus-pbq-ui pbq-folder-suite {scenario['body_class']}">
  <script src="/js/sample-url-mask-apply.js"></script>
  <div class="page-logo-watermark" aria-hidden="true">
    <img src="/images/logo/becertifiedtoday_logo_image_trans.png" alt="" />
  </div>
  <div class="question-shell question-shell--suite">
    <a class="site-logo-corner" href="/COMP_TIA_SEC+/SEC+_Training_Portal.html" aria-label="Security+ practice portal">
      <img src="/images/logo/becertifiedtoday_logo_trans.png" width="52" height="52" alt="Be Certified Today" />
    </a>
    <main class="pbq-card pbq-card--suite">
      <nav class="question-nav" aria-label="Question navigation">
        <div class="question-nav-links">
          {nav_link(scenario, "prev")}
          <a class="nav-link nav-home" href="/COMP_TIA_SEC+/SEC+_Training_Portal.html">Home</a>
          {nav_link(scenario, "next")}
        </div>
      </nav>

      <header class="pbq-suite-header">
        <h1>{scenario['title']}</h1>
        <p class="pbq-sub">{scenario['description']}</p>
        <p class="pbq-instructions">
          Use the <strong>folder sidebar</strong> to switch sections on this page. Open <strong>exhibits</strong> in
          popups where available.
        </p>
      </header>

      <div class="{layout_class}">
        {nav}
        <div class="pbq-suite-main" id="pbqSuiteMain">
          {panels}
        </div>
      </div>

      <p class="pbq-suite-footer">
        <a class="btn btn-secondary" href="{BASE_URL}/index.html">All PBQ Labs</a>
      </p>
    </main>
  </div>

  <script src="/COMP_TIA_SEC+/js/pbq-folder-suite.js"></script>
  <script>window.PBQ_SUITE_DEFAULT_SECTION = "{first_section}";</script>
  {scripts}
</body>
</html>
"""


def build_hub_index() -> str:
    items = []
    for sc in SCENARIOS:
        slug = sc["slug"]
        url = f"{BASE_URL}/{slug}/{slug}.html"
        items.append(
            f'<li><a class="pbq-hub-card" href="{url}">'
            f'<strong>{sc["title"]}</strong>'
            f'<span>{len(sc["sections"])} sections — {sc["description"][:80]}…</span>'
            f"</a></li>"
        )
    first = SCENARIOS[0]["slug"]
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="robots" content="noindex, nofollow" />
  <meta name="description" content="CompTIA Security+ PBQ production labs — pick a scenario." />
  <link rel="canonical" href="https://becertifiedtoday.com{BASE_URL}/index.html" />
  <title>Security+ PBQ Production Labs | Be Certified Today</title>
  <link rel="stylesheet" href="/css/bcc-question-link-nav.css" />
  <link rel="stylesheet" href="/COMP_TIA_SEC+/SEC+_Samples/secplus-sample-touch.css" />
  <link rel="stylesheet" href="/COMP_TIA_SEC+/js/secplus-pbq-page.css" />
</head>
<body class="secplus-question-ui secplus-pbq-ui pbq-hub">
  <script src="/js/sample-url-mask-apply.js"></script>
  <div class="question-shell">
    <main class="pbq-card">
      <nav class="question-nav" aria-label="Question navigation">
        <div class="question-nav-links">
          <span class="nav-link nav-link--disabled nav-prev" aria-hidden="true">Back</span>
          <a class="nav-link nav-home" href="/COMP_TIA_SEC+/SEC+_Training_Portal.html">Home</a>
          <a class="nav-link nav-next next-link" href="{BASE_URL}/{first}/{first}.html">Next</a>
        </div>
      </nav>
      <h1>Security+ PBQ production labs</h1>
      <p class="pbq-sub">Each scenario is one page with folder sections. Legacy part URLs redirect into the matching scenario.</p>
      <ul class="pbq-hub-list">
        {"".join(items)}
      </ul>
    </main>
  </div>
</body>
</html>
"""


def write_redirects() -> None:
    for rel, (page, section_id) in LEGACY_REDIRECTS.items():
        url = f"{BASE_URL}/{page}#{section_id}"
        (PBQ / rel).write_text(REDIRECT_STUB.format(url=url), encoding="utf-8")


def main() -> None:
    written: list[str] = []
    for scenario in SCENARIOS:
        slug = scenario["slug"]
        out = PBQ / slug / f"{slug}.html"
        out.write_text(build_scenario_page(scenario), encoding="utf-8")
        written.append(str(out.relative_to(ROOT)))
    hub = PBQ / "index.html"
    hub.write_text(build_hub_index(), encoding="utf-8")
    write_redirects()
    print("wrote " + ", ".join(written))
    print(f"wrote {hub.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
