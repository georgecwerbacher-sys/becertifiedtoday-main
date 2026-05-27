#!/usr/bin/env python3
"""Ensure cli-lab-container.js loads in <head> before inline lab scripts."""

from __future__ import annotations

import re
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCAN_DIRS = (ROOT / "public", ROOT / "templates")
CONTAINER_JS = '<script src="/js/cli-lab-container.js"></script>'
TAG_RE = re.compile(r'\s*<script src="/js/cli-lab-container\.js"></script>\s*')


def patch_file(path: pathlib.Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "cliLabContainer" not in text and "invalidInputMsgForNormalizedCmd" not in text:
        return False
    if "/js/cli-lab-container.js" not in text:
        return False

    original = text
    tags = TAG_RE.findall(text)
    if not tags:
        return False

    # Strip all existing tags; re-insert once in head.
    text = TAG_RE.sub("\n", text)

    css = '<link rel="stylesheet" href="/css/cli-lab-container.css" />'
    viewport = '<meta name="viewport" content="width=device-width, initial-scale=1.0" />'
    if css in text:
        text = text.replace(css, css + "\n  " + CONTAINER_JS, 1)
    elif viewport in text:
        text = text.replace(viewport, viewport + "\n  " + CONTAINER_JS, 1)
    else:
        head_end = text.find("</head>")
        if head_end == -1:
            return False
        text = text[:head_end] + "  " + CONTAINER_JS + "\n" + text[head_end:]

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = []
    for base in SCAN_DIRS:
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.html")):
            if patch_file(path):
                changed.append(str(path.relative_to(ROOT)))
    print(f"Fixed load order in {len(changed)} file(s)")
    for rel in changed:
        print(f"  {rel}")


if __name__ == "__main__":
    main()
