#!/usr/bin/env python3
"""Align guest-facing HTML pages with marketing-vault/01-strategy positioning.

Guest pages = public sitemap URLs (no login / paid portal). Applies exam-prep
copy, landing-page home links, meta descriptions, and disclaimer language.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
SITE_ORIGIN = "https://becertifiedtoday.com"

# Re-use crawl/sitemap guest detection from sync-public-crawl-access.py
import importlib.util

_crawl_spec = importlib.util.spec_from_file_location(
    "sync_public_crawl_access",
    ROOT / "scripts" / "sync-public-crawl-access.py",
)
_crawl = importlib.util.module_from_spec(_crawl_spec)
assert _crawl_spec and _crawl_spec.loader
_crawl_spec.loader.exec_module(_crawl)
is_guest_sitemap_page = _crawl.is_guest_sitemap_page
rel_public = _crawl.rel_public

META_DESC_RE = re.compile(
    r'<meta\s+name="description"\s+content="[^"]*"\s*/?\s*>',
    re.IGNORECASE,
)
CANONICAL_RE = re.compile(
    r'<link\s+rel="canonical"\s+href="[^"]*"\s*/?\s*>',
    re.IGNORECASE,
)
TITLE_RE = re.compile(r"<title>([^<]*)</title>", re.IGNORECASE)

# Customer-facing: exam prep landing pages, not gated Training Portal URLs.
LINK_REPLACEMENTS: list[tuple[str, str]] = [
    ('href="/CCNA-Study/CCNA_Training_Portal.html"', 'href="/ccna-home.html"'),
    ('href="/CCNP-ENCOR-Study/ENCOR_Training_Portal.html"', 'href="/ccnp-home.html"'),
    ('href="/COMP_TIA_SEC+/SEC+_Training_Portal.html"', 'href="/comptia-sec+-home.html"'),
    (">CCNA Study<", ">CCNA exam prep<"),
    (">Security+ Study<", ">Security+ exam prep<"),
    ("independent training resource", "independent exam prep resource"),
    ("CCNA Training Portal banks", "CCNA practice question bank"),
    ("Security+ Training Portal banks", "Security+ practice question bank"),
]

# Visible copy on guest pages only (avoid changing internal portal-only strings in JS comments).
GUEST_COPY_REPLACEMENTS: list[tuple[str, str]] = [
    ("CCNA Training Portal</a>", "CCNA exam prep</a>"),
    ("ENCOR Training Portal</a>", "ENCOR exam prep</a>"),
    (
        "return to the CCNA Training Portal; otherwise",
        "return to CCNA exam prep; otherwise",
    ),
    (
        "start the timed test from the CCNA Training Portal on this browser.",
        "start the timed test from CCNA exam prep on this browser.",
    ),
    ("From the training portal, use", "From CCNP exam prep, use"),
    ("Back to ENCOR training portal", "Back to ENCOR exam prep"),
    (
        "Be Certified Today — ENCOR training portal",
        "Be Certified Today — ENCOR exam prep",
    ),
    (
        "full practice library and training portal.",
        "full practice library and practice portal.",
    ),
    ("training portal modes, and timed", "practice portal modes, and timed"),
    (">CCNP ENCOR Training Portal<", ">CCNP ENCOR exam prep<"),
    (
        "CCNP ENCOR training portal — requires active access",
        "CCNP ENCOR exam prep — requires active access",
    ),
    (
        "CCNP ENCOR training portal — open when you have active access",
        "CCNP ENCOR exam prep — open when you have active access",
    ),
    ("the CCNP ENCOR training portal</a>", "CCNP ENCOR exam prep</a>"),
    (
        "The CCNP ENCOR Training Portal is for learners",
        "The CCNP ENCOR practice portal is for learners",
    ),
    (
        "The CCNA Training Portal is for learners",
        "The CCNA practice portal is for learners",
    ),
    (">CCNA Training Portal<", ">CCNA practice portal<"),
    (">CCNP ENCOR Training Portal<", ">CCNP ENCOR practice portal<"),
    (
        'content="CCNA Timed Test Simulation hub — preparation, purchase, and runner (becertifiedtoday.com)."',
        'content="CCNA 200-301 timed exam simulation — one-time purchase, browser-based exam prep. Realistic question mix before test day."',
    ),
]

TITLE_LAUNCHER_FIXES: dict[str, str] = {
    "Sample practice": "Free exam prep sample — Be Certified Today",
    "Security+ sample practice": "Security+ SY0-701 free practice sample | Be Certified Today",
    "Starting sample…": "Starting free exam prep sample…",
}

DEFAULT_META: list[tuple[str, str]] = [
    (
        "CCNA-Study/CCNA_Samples/",
        "Free CCNA 200-301 exam prep sample — interactive practice in your browser with verified explanations. No PDFs or third-party software.",
    ),
    (
        "CCNA-Study/CCNA_labs/cli-lab-trunk_lacp.html",
        "Free CCNA 200-301 CLI lab sample — trunk and LACP practice in your browser. Exam prep, not a training course. No GNS3 required.",
    ),
    (
        "CCNA-Study/CCNA_labs/cli-lab-vlan-sim.html",
        "Free CCNA 200-301 VLAN CLI lab sample — browser exam prep with simulated IOS. No Packet Tracer or GNS3 install.",
    ),
    (
        "CCNP-ENCOR-Study/ENCOR_Samples/",
        "Free CCNP ENCOR 350-401 exam prep sample — interactive practice questions and labs in your browser. Verified explanations, no PDF dumps.",
    ),
    (
        "COMP_TIA_SEC+/SEC+_Samples/",
        "Free CompTIA Security+ SY0-701 exam prep sample — interactive practice with verified explanations in your browser. Not a training course.",
    ),
    (
        "CCNA_Sim_EXAM/free-assessment.html",
        "Free CCNA 200-301 assessment — timed practice test with domain scorecard. Browser exam prep from Be Certified Today. No subscription.",
    ),
    (
        "CCNA_Sim_EXAM/test-simulation.html",
        "CCNA 200-301 timed exam simulation — one-time purchase, browser-based exam prep. Realistic question mix before test day.",
    ),
    (
        "CCNA_Sim_EXAM/begin-test-simulation.html",
        "CCNA 200-301 timed test simulation — purchase one-time exam prep access. 120-minute browser run with detailed review.",
    ),
    (
        "CCNP-ENCOR-Study/test-simulation.html",
        "CCNP ENCOR 350-401 timed exam simulation — browser exam prep. One-time purchase for a realistic timed dry run.",
    ),
]


def meta_for(rel: str) -> str | None:
    for prefix, text in DEFAULT_META:
        if rel == prefix or rel.startswith(prefix):
            return text
    return None


def insert_after_charset(html: str, line: str) -> str:
    charset_match = re.search(
        r'(<meta\s+charset="[^"]*"\s*/?\s*>)',
        html,
        re.IGNORECASE,
    )
    if charset_match:
        pos = charset_match.end()
        return html[:pos] + "\n  " + line + html[pos:]
    head_match = re.search(r"<head[^>]*>", html, re.IGNORECASE)
    if head_match:
        pos = head_match.end()
        return html[:pos] + "\n  " + line + html[pos:]
    return line + "\n" + html


def ensure_meta_description(html: str, description: str) -> str:
    tag = f'<meta name="description" content="{description}" />'
    if META_DESC_RE.search(html):
        return META_DESC_RE.sub(tag, html, count=1)
    return insert_after_charset(html, tag)


def ensure_canonical(html: str, rel: str) -> str:
    if rel == "index.html":
        href = f"{SITE_ORIGIN}/"
    else:
        href = f"{SITE_ORIGIN}/{rel}"
    tag = f'<link rel="canonical" href="{href}" />'
    if CANONICAL_RE.search(html):
        return CANONICAL_RE.sub(tag, html, count=1)
    return insert_after_charset(html, tag)


def fix_title(html: str, rel: str) -> str:
    m = TITLE_RE.search(html)
    if not m:
        return html
    title = m.group(1).strip()
    new_title = TITLE_LAUNCHER_FIXES.get(title)
    if not new_title:
        if title == "OSPF Sample Question":
            new_title = "ENCOR 350-401 sample — OSPF DR (exam prep)"
        elif title.startswith("CCNA sample —") and "Be Certified Today" not in title:
            new_title = title.replace("CCNA sample —", "CCNA 200-301 exam prep sample —")
        elif title.startswith("Security+ sample —") and "Be Certified Today" not in title:
            new_title = title.replace(
                "Security+ sample —", "Security+ SY0-701 exam prep sample —"
            )
    if not new_title or new_title == title:
        return html
    return TITLE_RE.sub(f"<title>{new_title}</title>", html, count=1)


def apply_replacements(html: str, pairs: list[tuple[str, str]]) -> str:
    for old, new in pairs:
        html = html.replace(old, new)
    return html


def ensure_analytics(html: str) -> str:
    if "install-google-tag.js" in html or "campaign-attribution.js" in html:
        return html
    snippet = (
        '<script src="/js/install-google-tag.js"></script>\n'
        '  <script src="/js/install-vercel-analytics.js"></script>'
    )
    return insert_after_charset(html, snippet)


def sync_file(path: Path) -> bool:
    rel = rel_public(path)
    original = path.read_text(encoding="utf-8")
    updated = original

    updated = apply_replacements(updated, LINK_REPLACEMENTS)
    updated = apply_replacements(updated, GUEST_COPY_REPLACEMENTS)

    desc = meta_for(rel)
    if desc:
        updated = ensure_meta_description(updated, desc)
        updated = ensure_canonical(updated, rel)

    updated = fix_title(updated, rel)

    if rel.endswith("/sample.html") or rel.endswith("begin-landing-sample.html"):
        updated = ensure_analytics(updated)

    if updated == original:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    changed: list[str] = []
    for path in sorted(PUBLIC.rglob("*.html")):
        rel = rel_public(path)
        if not is_guest_sitemap_page(rel):
            continue
        if sync_file(path):
            changed.append(rel)

    print(f"Guest page marketing sync: {len(changed)} file(s) updated")
    for rel in changed:
        print(f"  - {rel}")


if __name__ == "__main__":
    main()
