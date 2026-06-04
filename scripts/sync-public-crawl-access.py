#!/usr/bin/env python3
"""Align robots.txt, sitemap.xml, and HTML meta robots with public vs private pages.

Public pages (reachable without login or paid portal access) get index,follow.
Private flows (admin, magic links, checkout success, gated test runners) stay noindex.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
ROBOTS = PUBLIC / "robots.txt"
SITEMAP = PUBLIC / "sitemap.xml"
SITE_ORIGIN = "https://becertifiedtoday.com"

ROBOTS_TXT = """\
# Public study content is crawlable; block admin, API, and auth/checkout-only flows.
User-agent: *
Allow: /

Disallow: /admin
Disallow: /admin/
Disallow: /admin/analytics
Disallow: /admin/analytics.html
Disallow: /api/
Disallow: /choose-training-path.html
Disallow: /secplus-home.html
Disallow: /*Training_Portal.html
Disallow: /CCNP-ENCOR-Study/access-restricted.html
Disallow: /CCNP-ENCOR-Study/admin-renew.html
Disallow: /*portal-magic.html
Disallow: /*portal-restore-access.html
Disallow: /*portal-request-link.html
Disallow: /*portal-30d-checkout-success.html
Disallow: /*test-simulation-runner.html
Disallow: /*test-simulation-purchase.html

Sitemap: https://becertifiedtoday.com/sitemap.xml
"""

NOCRAWL_SUFFIXES = (
    "Training_Portal.html",
    "portal-magic.html",
    "portal-restore-access.html",
    "portal-request-link.html",
    "portal-30d-checkout-success.html",
    "test-simulation-runner.html",
    "test-simulation-purchase.html",
)

NOCRAWL_EXACT = {
    "choose-training-path.html",
    "secplus-home.html",
    "CCNP-ENCOR-Study/access-restricted.html",
    "CCNP-ENCOR-Study/admin-renew.html",
}

NOCRAWL_PREFIXES = (
    "admin/",
    "COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/pending/",
    "COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/",
)

# Guest-facing pages promoted in sitemap (unregistered users, no portal purchase).
SITEMAP_EXACT = {
    "index.html",
    "ccna-home.html",
    "ccnp-home.html",
    "comptia-sec+-home.html",
    "CCNA_Sim_EXAM/free-assessment.html",
    "CCNA_Sim_EXAM/test-simulation.html",
    "CCNA_Sim_EXAM/begin-test-simulation.html",
    "CCNP-ENCOR-Study/test-simulation.html",
    "CCNA-Study/CCNA_labs/cli-lab-trunk_lacp.html",
    "CCNA-Study/CCNA_labs/cli-lab-vlan-sim.html",
    "COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/simulation-secure-web-architecture-openssl.html",
}

SITEMAP_PREFIXES = (
    "CCNA-Study/CCNA_Samples/",
    "CCNP-ENCOR-Study/ENCOR_Samples/",
    "COMP_TIA_SEC+/SEC+_Samples/",
    "COMP_TIA_SEC+/SEC+_PBQ/",
)

# Vercel rewrite entry points (canonical path → source file for lastmod).
SITEMAP_ALIASES: dict[str, str] = {
    "sample": "CCNP-ENCOR-Study/ENCOR_Samples/sample.html",
    "secplus-sample": "COMP_TIA_SEC+/SEC+_Samples/sample.html",
    "ccna/practice-test": "ccna-home.html",
}

SITEMAP_SKIP_PREFIXES = (
    "COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/reports/",
)

ROBOTS_META_RE = re.compile(
    r'<meta\s+name="robots"\s+content="[^"]*"\s*/?\s*>',
    re.IGNORECASE,
)

INDEXABLE = '<meta name="robots" content="index, follow" />'
NOINDEX = '<meta name="robots" content="noindex, nofollow" />'


def rel_public(path: Path) -> str:
    return path.relative_to(PUBLIC).as_posix()


def should_noindex(rel: str) -> bool:
    if rel in NOCRAWL_EXACT:
        return True
    if any(rel.startswith(prefix) for prefix in NOCRAWL_PREFIXES):
        return True
    return any(rel.endswith(suffix) for suffix in NOCRAWL_SUFFIXES)


def is_indexable(rel: str) -> bool:
    return not should_noindex(rel)


def is_guest_sitemap_page(rel: str) -> bool:
    if not is_indexable(rel):
        return False
    if any(rel.startswith(skip) for skip in SITEMAP_SKIP_PREFIXES):
        return False
    if rel in SITEMAP_EXACT:
        return True
    return any(rel.startswith(prefix) for prefix in SITEMAP_PREFIXES)


def public_url(rel: str) -> str:
    if rel == "index.html":
        return f"{SITE_ORIGIN}/"
    return f"{SITE_ORIGIN}/{rel}"


def lastmod_for(path: Path) -> str:
    stamp = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    return stamp.strftime("%Y-%m-%d")


def alias_public_url(alias_path: str) -> str:
    return f"{SITE_ORIGIN}/{alias_path}"


def build_sitemap() -> int:
    entries: list[tuple[str, str]] = []
    seen_locs: set[str] = set()

    def add_entry(loc: str, path: Path) -> None:
        if loc in seen_locs:
            return
        seen_locs.add(loc)
        entries.append((loc, lastmod_for(path)))

    for path in sorted(PUBLIC.rglob("*.html")):
        rel = rel_public(path)
        if not is_guest_sitemap_page(rel):
            continue
        add_entry(public_url(rel), path)

    for alias_path, source_rel in sorted(SITEMAP_ALIASES.items()):
        source = PUBLIC / source_rel
        if not source.is_file():
            continue
        add_entry(alias_public_url(alias_path), source)

    entries.sort(key=lambda pair: pair[0])

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, lastmod in entries:
        lines.extend(
            [
                "  <url>",
                f"    <loc>{escape(loc)}</loc>",
                f"    <lastmod>{lastmod}</lastmod>",
                "  </url>",
            ]
        )
    lines.append("</urlset>")
    SITEMAP.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(entries)


def insert_robots_after_charset(html: str, robots_line: str) -> str:
    charset_match = re.search(
        r'(<meta\s+charset="[^"]*"\s*/?\s*>)',
        html,
        re.IGNORECASE,
    )
    if charset_match:
        insert_at = charset_match.end()
        return html[:insert_at] + "\n  " + robots_line + html[insert_at:]
    head_match = re.search(r"<head[^>]*>", html, re.IGNORECASE)
    if head_match:
        insert_at = head_match.end()
        return html[:insert_at] + "\n  " + robots_line + html[insert_at:]
    return robots_line + "\n" + html


def sync_html(path: Path) -> str | None:
    rel = rel_public(path)
    want_noindex = should_noindex(rel)
    want_line = NOINDEX if want_noindex else INDEXABLE

    original = path.read_text(encoding="utf-8")
    updated = original

    if ROBOTS_META_RE.search(updated):
        updated = ROBOTS_META_RE.sub(want_line, updated, count=1)
    else:
        updated = insert_robots_after_charset(updated, want_line)

    if updated == original:
        return None
    path.write_text(updated, encoding="utf-8")
    return "noindex" if want_noindex else "index"


def main() -> None:
    ROBOTS.write_text(ROBOTS_TXT, encoding="utf-8")
    url_count = build_sitemap()

    counts = {"index": 0, "noindex": 0, "unchanged": 0}
    for path in sorted(PUBLIC.rglob("*.html")):
        result = sync_html(path)
        if result is None:
            counts["unchanged"] += 1
        else:
            counts[result] += 1

    print(f"Wrote {ROBOTS.relative_to(ROOT)}")
    print(f"Wrote {SITEMAP.relative_to(ROOT)} ({url_count} URLs)")
    print(
        "HTML robots meta: "
        f"{counts['index']} indexable, "
        f"{counts['noindex']} noindex, "
        f"{counts['unchanged']} unchanged"
    )


if __name__ == "__main__":
    main()
