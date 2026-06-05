#!/usr/bin/env python3
"""One-time port: pending PBQ HTML → PBQ_Production section fragments."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PENDING = ROOT / "public/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/pending"
PBQ = ROOT / "public/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production"

# Duplicates — do not port (superseded in production).
SKIP = {"security-control-map", "siem-security-alerts-dashboard", "TEMPLATE-dragdrop"}

SCENARIOS = [
    {
        "slug": "log-timeline-forensics",
        "section_id": "log-timeline",
        "label": "Log timeline",
        "title": "Log Timeline Forensics",
        "body_class": "dragdrop-exercise",
        "description": "Reorder SSH auth log snippets to reconstruct a brute-force attack ending in privilege escalation.",
        "dragdrop": True,
    },
    {
        "slug": "pki-certificate-chain-browser-error",
        "section_id": "pki-browser-error",
        "label": "Browser cert error",
        "title": "PKI Certificate Chain — Browser Error",
        "body_class": "pbq-exhibit-mcq",
        "description": "PKI certificate chain exhibit and NET::ERR_CERT_AUTHORITY_INVALID troubleshooting.",
        "dragdrop": False,
    },
    {
        "slug": "phishing-email-analysis",
        "section_id": "phishing-analysis",
        "label": "Phishing analysis",
        "title": "Phishing Email Analysis",
        "body_class": "pbq-phishing-analysis dragdrop-exercise",
        "description": "Phishing email exhibit and drag-and-drop social engineering term matching.",
        "dragdrop": True,
    },
    {
        "slug": "vulnerability-management",
        "section_id": "vuln-management",
        "label": "Vulnerability scan",
        "title": "Vulnerability Management",
        "body_class": "pbq-exhibit-mcq",
        "description": "Vulnerability scanner exhibit and Log4Shell compensating controls during a change freeze.",
        "dragdrop": False,
    },
    {
        "slug": "incident-response",
        "section_id": "incident-response",
        "label": "NIST IR fill-in",
        "title": "Incident Response — Ransomware IR",
        "body_class": "pbq-incident-response dragdrop-exercise",
        "description": "NIST SP 800-61 ransomware incident timeline and IR process fill-in drag-and-drop.",
        "dragdrop": True,
    },
    {
        "slug": "quantitative-risk-ale",
        "section_id": "risk-ale",
        "label": "Risk & ALE",
        "title": "Quantitative Risk — ALE",
        "body_class": "pbq-exhibit-mcq pbq-risk-ale",
        "description": "Quantitative risk analysis exhibit (SLE, ARO, ALE) and security awareness training ROI.",
        "dragdrop": False,
    },
    {
        "slug": "malware-ioc-analysis",
        "section_id": "malware-ioc",
        "label": "Malware IOCs",
        "title": "Malware IOC Analysis",
        "body_class": "pbq-exhibit-mcq pbq-malware-ioc",
        "description": "Endpoint malware IOC exhibit (process, network, persistence) and malware classification.",
        "dragdrop": False,
    },
    {
        "slug": "data-protection",
        "section_id": "data-protection",
        "label": "Data protection",
        "title": "Data Protection",
        "body_class": "pbq-exhibit-mcq pbq-data-protection",
        "description": "Data classification, states, and protection methods exhibit plus PCI test-data tokenization.",
        "dragdrop": False,
    },
    {
        "slug": "governance",
        "section_id": "governance",
        "label": "Governance",
        "title": "Governance",
        "body_class": "pbq-exhibit-mcq pbq-governance",
        "description": "Security governance frameworks, policies, vendor agreements, and breach notification obligations.",
        "dragdrop": False,
    },
]


def extract_main_body(html: str) -> str:
    m = re.search(
        r"<main\s+class=\"pbq-card\"[^>]*>.*?<nav[^>]*>.*?</nav>\s*(.*?)\s*</main>",
        html,
        re.DOTALL | re.IGNORECASE,
    )
    if not m:
        raise ValueError("Could not find main body")
    return m.group(1).strip()


def extract_script(html: str) -> str:
    m = re.search(r"<script(?![^>]*src=)[^>]*>(.*?)</script>", html, re.DOTALL | re.IGNORECASE)
    if not m:
        raise ValueError("Could not find inline script")
    return m.group(1).strip()


def transform_script(script: str, section_id: str, dragdrop: bool) -> str:
    inner = script
    inner = re.sub(r"^\(function\s*\(\)\s*\{\s*", "", inner)
    inner = re.sub(r"\s*\}\)\(\);\s*$", "", inner)

    inner = re.sub(r"\s*var bank = document\.getElementById\(\"bank\"\);\s*", "\n", inner)
    inner = re.sub(r"\s*var checkBtn = document\.getElementById\(\"checkBtn\"\);\s*", "", inner)
    inner = re.sub(r"\s*var showBtn = document\.getElementById\(\"showBtn\"\);\s*", "", inner)
    inner = re.sub(r"\s*var resetBtn = document\.getElementById\(\"resetBtn\"\);\s*", "", inner)
    inner = re.sub(r"\s*var result = document\.getElementById\(\"result\"\);\s*", "", inner)

    inner = inner.replace("document.querySelectorAll(", "root.querySelectorAll(")
    inner = inner.replace("document.querySelector(", "root.querySelector(")
    inner = inner.replace('root.querySelector(".pbq-card")', "root")

    root_lines = [
        f'  var root = document.getElementById("{section_id}");',
        "  if (!root) return;",
        "",
    ]
    if dragdrop:
        root_lines.extend(
            [
                '  var bank = root.querySelector(".bank");',
                '  var actionBtns = root.querySelectorAll(".actions button");',
                "  var checkBtn = actionBtns[0];",
                "  var showBtn = actionBtns[1];",
                "  var resetBtn = actionBtns[2];",
                '  var result = root.querySelector(".actions [role=\'status\']");',
                "",
            ]
        )
    else:
        root_lines.extend(
            [
                '  var actionBtns = root.querySelectorAll(".actions button");',
                "  var checkBtn = actionBtns[0];",
                "  var showBtn = actionBtns[1];",
                "  var resetBtn = actionBtns[2];",
                '  var result = root.querySelector(".actions [role=\'status\']");',
                "",
            ]
        )

    return (
        "<script>\n(function () {\n"
        + "\n".join(root_lines)
        + inner.strip()
        + "\n})();\n</script>"
    )


def port_scenario(sc: dict) -> None:
    src = PENDING / f"{sc['slug']}.html"
    if not src.exists():
        raise FileNotFoundError(src)

    html = src.read_text(encoding="utf-8")
    body = extract_main_body(html)
    script = transform_script(extract_script(html), sc["section_id"], sc["dragdrop"])

    out_dir = PBQ / sc["slug"] / "sections"
    out_dir.mkdir(parents=True, exist_ok=True)

    fragment = (
        f'<article class="pbq-section-fragment" data-id="{sc["section_id"]}">\n'
        f"{body}\n"
        f"{script}\n"
        f"</article>\n"
    )
    (out_dir / f"{sc['section_id']}.html").write_text(fragment, encoding="utf-8")

    readme = f"""# {sc['title']} (PBQ)

SY0-701 performance-based practice — ported from `pending/{sc['slug']}.html`.

## Section

| File | Part |
|------|------|
| `sections/{sc['section_id']}.html` | {sc['label']} |

## Preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/{sc['slug']}/{sc['slug']}.html
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/{sc['slug']}/{sc['slug']}.html#{sc['section_id']}
```

See `../VERIFICATION.md` for answer keys.
"""
    (PBQ / sc["slug"] / "README.md").write_text(readme, encoding="utf-8")
    print(f"ported {sc['slug']}")


def main() -> None:
    for sc in SCENARIOS:
        port_scenario(sc)
    print(f"skipped duplicates: {', '.join(sorted(SKIP))}")


if __name__ == "__main__":
    main()
