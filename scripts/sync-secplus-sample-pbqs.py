#!/usr/bin/env python3
"""Copy Security+ homepage sample PBQs into SEC+_Samples/pbq/ (public, not portal-gated).

Source: PBQ_Production. Strips portal chrome, fixes Home/logo → comptia-sec+-home.html,
removes production footer nav (sample nav handles Next/Back).
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
PRODUCTION = PUBLIC / "COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production"
DEST_ROOT = PUBLIC / "COMP_TIA_SEC+/SEC+_Samples/pbq"
PUBLIC_HOME = "/comptia-sec+-home.html"
PORTAL_HOME = "/COMP_TIA_SEC+/SEC+_Training_Portal.html"

SAMPLE_PBQS = (
    {
        "slug": "dark-web-account-protection",
        "canonical": "https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Samples/pbq/dark-web-account-protection/dark-web-account-protection.html",
    },
    {
        "slug": "home-wlan-director-config",
        "canonical": "https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Samples/pbq/home-wlan-director-config/home-wlan-director-config.html",
    },
    {
        "slug": "firewall-acl-secops",
        "canonical": "https://becertifiedtoday.com/COMP_TIA_SEC+/SEC+_Samples/pbq/firewall-acl-secops/firewall-acl-secops.html",
    },
)

FOOTER_NAV_RE = re.compile(
    r"\s*<nav class=\"question-nav question-nav--footer\"[\s\S]*?</nav>\s*",
    re.MULTILINE,
)

def transform_html(html: str, *, canonical: str) -> str:
    html = html.replace(PORTAL_HOME, PUBLIC_HOME)
    html = html.replace(
        'aria-label="Security+ practice portal"',
        'aria-label="Return to Security+ home"',
    )
    html = html.replace(
        'aria-label="Security+ training portal"',
        'aria-label="Return to Security+ home"',
    )
    html = re.sub(
        r'<link rel="canonical" href="[^"]+" />',
        f'<link rel="canonical" href="{canonical}" />',
        html,
        count=1,
    )
    html = html.replace(
        '<meta name="robots" content="noindex, nofollow" />',
        '<meta name="robots" content="index, follow" />',
    )
    html = html.replace(
        '  <link rel="stylesheet" href="/COMP_TIA_SEC+/js/secplus-pbq-portal-chrome.css" />\n',
        "",
    )
    html = html.replace(
        '  <script src="/COMP_TIA_SEC+/js/secplus-pbq-portal-chrome.js"></script>\n',
        "",
    )
    html = FOOTER_NAV_RE.sub("\n", html)
    html = re.sub(
        r'<article class="pbq-suite-section"',
        '<article class="pbq-suite-section is-active"',
        html,
        count=1,
    )
    html = re.sub(
        r'(<article class="pbq-suite-section is-active[^>]*)\shidden>',
        r"\1>",
        html,
        count=1,
    )
    if "secplus-sample-pbq" not in html:
        html = html.replace(
            "<body class=\"",
            '<body class="secplus-sample-pbq ',
            1,
        )
    return html


def main() -> None:
    DEST_ROOT.mkdir(parents=True, exist_ok=True)
    for entry in SAMPLE_PBQS:
        slug = entry["slug"]
        src = PRODUCTION / slug / f"{slug}.html"
        if not src.is_file():
            raise SystemExit(f"missing source PBQ: {src}")
        dest_dir = DEST_ROOT / slug
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / f"{slug}.html"
        out = transform_html(src.read_text(encoding="utf-8"), canonical=entry["canonical"])
        if not dest.exists() or dest.read_text(encoding="utf-8") != out:
            dest.write_text(out, encoding="utf-8")
            print(f"synced {dest.relative_to(ROOT)}")
        else:
            print(f"ok {dest.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
