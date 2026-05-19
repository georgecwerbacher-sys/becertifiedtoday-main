#!/usr/bin/env python3
"""Move Back/Home/Next to top nav on hand-maintained CCNA prefix question pages."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public/CCNA-Study/CCNA_questions"
HUB_JS = ROOT / "public/CCNA-Study/js/ccna-practice-100-hub.js"
ANCHOR = "vty-access-list-ssh-secure"

NAV_CSS = """
    .question-nav {
      margin: 0 0 20px;
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      justify-content: space-between;
    }
    .question-nav-links {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
    }
    .question-nav .nav-link,
    .question-nav .nav-check {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      text-decoration: none;
      color: #e6edf3;
      background: #254b8a;
      border: 1px solid #3d6dbb;
      border-radius: 10px;
      padding: 10px 16px;
      font-weight: 700;
      font-size: 0.95rem;
      font-family: inherit;
      cursor: pointer;
    }
    .question-nav .nav-link--disabled {
      opacity: 0.35;
      pointer-events: none;
      cursor: default;
    }
    .question-nav .nav-check {
      margin-left: auto;
    }
    .question-nav .nav-link:hover,
    .question-nav .nav-check:hover {
      filter: brightness(1.08);
    }
"""

ACTIONS_RE = re.compile(r'\s*<div class="actions">.*?</div>\s*', re.DOTALL)
NEXT_WRAP_RE = re.compile(r'\s*<div class="next-wrap">.*?</div>\s*', re.DOTALL)
PREV_RE = re.compile(
    r'<a class="next-link" href="/CCNA-Study/CCNA_questions/([^"]+)\.html">(?:Previous question|Back)</a>'
)
NEXT_RE = re.compile(
    r'<a class="next-link" href="/CCNA-Study/CCNA_questions/([^"]+)\.html">(?:Next question|Next)</a>'
)


def prefix_slugs() -> list[str]:
    text = HUB_JS.read_text(encoding="utf-8")
    m = re.search(r"ALL_SLUGS\s*=\s*\[(.*?)\];", text, re.S)
    if not m:
        raise ValueError("ALL_SLUGS not found")
    slugs = re.findall(r'"([^"]+)"', m.group(1))
    try:
        end = slugs.index(ANCHOR) + 1
    except ValueError:
        end = 11
    return slugs[:end]


def build_nav(prev_slug: str | None, next_slug: str | None, *, show_check: bool) -> str:
    parts: list[str] = []
    if prev_slug:
        parts.append(
            f'      <a class="nav-link nav-prev" href="/CCNA-Study/CCNA_questions/{html.escape(prev_slug)}.html">Back</a>'
        )
    else:
        parts.append(
            '      <span class="nav-link nav-prev nav-link--disabled" aria-hidden="true">Back</span>'
        )
    parts.append('      <a class="nav-link nav-home" href="/index.html">Home</a>')
    if next_slug:
        parts.append(
            f'      <a class="nav-link nav-next next-link" href="/CCNA-Study/CCNA_questions/{html.escape(next_slug)}.html">Next</a>'
        )
    else:
        parts.append(
            '      <span class="nav-link nav-next nav-link--disabled" aria-hidden="true">Next</span>'
        )
    check = ""
    if show_check:
        check = '\n      <button id="checkBtn" type="button" class="nav-check">Check answer</button>'
    return (
        '    <nav class="question-nav" aria-label="Question navigation">\n'
        '      <div class="question-nav-links">\n'
        + "\n".join(parts)
        + "\n      </div>"
        + check
        + "\n    </nav>\n"
    )


def migrate_one(raw: str) -> str:
    text = raw.replace("**", "")
    if 'class="question-nav"' in text:
        return text

    prev_m = PREV_RE.search(text)
    next_m = NEXT_RE.search(text)
    prev_slug = prev_m.group(1) if prev_m else None
    next_slug = next_m.group(1) if next_m else None
    show_check = 'id="checkBtn"' in text

    text = ACTIONS_RE.sub("\n", text)
    text = NEXT_WRAP_RE.sub("\n", text)

    if ".question-nav" not in text:
        text = text.replace("  </style>", NAV_CSS + "  </style>", 1)

    nav = build_nav(prev_slug, next_slug, show_check=show_check)
    text = text.replace('<main class="card">\n', '<main class="card">\n' + nav, 1)
    return text


def main() -> None:
    changed = 0
    for slug in prefix_slugs():
        path = OUT / f"{slug}.html"
        if not path.is_file():
            continue
        raw = path.read_text(encoding="utf-8")
        new = migrate_one(raw)
        if new != raw:
            path.write_text(new, encoding="utf-8")
            changed += 1
            print("updated", path.name)
    print(f"Done. {changed} prefix file(s) updated.")


if __name__ == "__main__":
    main()
