#!/usr/bin/env python3
"""Add cli-container-template classes and script/css links to ENCOR lab pages."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LABS_DIR = ROOT / "public" / "CCNP-ENCOR-Study" / "CCNP-ENCOR-Labs"

CONTAINER_CSS = '<link rel="stylesheet" href="/css/cli-lab-container.css" />'
CONTAINER_JS = '<script src="/js/cli-lab-container.js"></script>'

SKIP_DIRS = {"Unused_Labs"}


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def add_class(existing: str | None, token: str) -> str:
    classes = (existing or "").split()
    if token not in classes:
        classes.append(token)
    return " ".join(classes)


def patch_scroll_div(match: re.Match[str]) -> str:
    tag = match.group(0)
    if "scrollback-area" in tag:
        return tag
    id_m = re.search(r'\bid="([^"]+)"', tag)
    if not id_m:
        return tag
    scroll_id = id_m.group(1)
    is_scroll = (
        scroll_id == "scrollback"
        or scroll_id.startswith("scroll")
        or scroll_id.endswith("Scrollback")
    )
    if not is_scroll:
        return tag
    cls_m = re.search(r'\bclass="([^"]*)"', tag)
    if cls_m:
        new_cls = add_class(cls_m.group(1), "scrollback-area")
        return tag.replace(f'class="{cls_m.group(1)}"', f'class="{new_cls}"', 1)
    return tag.replace(f'id="{scroll_id}"', f'id="{scroll_id}" class="scrollback-area"', 1)


def patch_prompt_span(match: re.Match[str]) -> str:
    tag = match.group(0)
    if "prompt-el" in tag:
        return tag
    cls_m = re.search(r'\bclass="([^"]*)"', tag)
    if cls_m:
        new_cls = add_class(cls_m.group(1), "prompt-el")
        return tag.replace(f'class="{cls_m.group(1)}"', f'class="{new_cls}"', 1)
    return tag.replace("<span ", '<span class="prompt-el" ', 1)


def patch_cmdline_input(match: re.Match[str]) -> str:
    tag = match.group(0)
    if "cmdline-input" in tag:
        return tag
    cls_m = re.search(r'\bclass="([^"]*)"', tag)
    if cls_m:
        new_cls = add_class(cls_m.group(1), "cmdline-input")
        return tag.replace(f'class="{cls_m.group(1)}"', f'class="{new_cls}"', 1)
    return tag.replace("<input ", '<input class="cmdline-input" ', 1)


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    text = text.replace(
        "scroll.className = 'console-scroll';",
        "scroll.className = 'console-scroll scrollback-area';",
    )
    text = text.replace(
        'scroll.className = "console-scroll";',
        'scroll.className = "console-scroll scrollback-area";',
    )

    text = re.sub(
        r'<div\b[^>]*\bid="scroll[^"]*"[^>]*>',
        patch_scroll_div,
        text,
    )
    text = re.sub(
        r'<div\b[^>]*\bid="scrollback[^"]*"[^>]*>',
        patch_scroll_div,
        text,
    )

    text = re.sub(
        r'<div\b[^>]*\bid="[^"]*Scrollback[^"]*"[^>]*>',
        patch_scroll_div,
        text,
    )

    text = re.sub(
        r'<span\b[^>]*\bid="(?:prompt[^"]*|[^"]*Prompt)"[^>]*>',
        patch_prompt_span,
        text,
    )

    text = re.sub(
        r'<input\b(?=[^>]*\b(?:id="cmd[^"]*"|id="cmdline[^"]*"|id="[^"]*Cmdline"))[^>]*>',
        patch_cmdline_input,
        text,
        flags=re.IGNORECASE,
    )

    if CONTAINER_CSS not in text:
        if 'href="/css/lab-router-spoiler.css"' in text:
            text = text.replace(
                '<link rel="stylesheet" href="/css/lab-router-spoiler.css" />',
                '<link rel="stylesheet" href="/css/lab-router-spoiler.css" />\n  '
                + CONTAINER_CSS,
                1,
            )
        elif "</head>" in text:
            text = text.replace("</head>", f"  {CONTAINER_CSS}\n</head>", 1)

    if CONTAINER_JS not in text and "lab-modal-drag.js" in text:
        text = text.replace(
            '<script src="/js/lab-modal-drag.js"></script>',
            CONTAINER_JS + "\n  " + '<script src="/js/lab-modal-drag.js"></script>',
            1,
        )
    elif CONTAINER_JS not in text and "</body>" in text:
        text = text.replace("</body>", f"  {CONTAINER_JS}\n</body>", 1)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    changed: list[str] = []
    for path in sorted(LABS_DIR.rglob("*.html")):
        if should_skip(path):
            continue
        if patch_file(path):
            changed.append(str(path.relative_to(ROOT)))
    print(f"Patched {len(changed)} lab file(s):")
    for name in changed:
        print(f"  {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
