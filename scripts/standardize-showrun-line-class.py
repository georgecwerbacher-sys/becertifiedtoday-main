#!/usr/bin/env python3
"""Use line-showrun (shared blue) for initial / show running-config output in ENCOR labs."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LABS = ROOT / "public" / "CCNP-ENCOR-Study" / "CCNP-ENCOR-Labs"

SHOWRUN_VARS = (
    r"R10_INITIAL_CONFIG|R20_INITIAL_CONFIG|R30_INITIAL_CONFIG|"
    r"R1_INITIAL_CONFIG|SW1_INITIAL_CONFIG|SW10_INITIAL_CONFIG|"
    r"R2_SHOW_RUN_INITIAL|R1_SHOW_RUN_TEXT|R2_SHOW_RUN_TEXT|R3_SHOW_RUN_TEXT|"
    r"R10_SHOW_RUN|R20_SHOW_RUN|R22_SHOW_RUN|SW22_SHOW_RUN|"
    r"SHOW_RUNNING_SNAPSHOT|SW10_SHOW_RUN"
)

APPEND_RE = re.compile(
    rf'append(Block|Line)\(([^,]+),\s*"(line-sys|line-out)",\s*({SHOWRUN_VARS})\)'
)
APPEND_CLASS_FIRST_RE = re.compile(
    rf'appendBlock\("(line-sys|line-out)",\s*({SHOWRUN_VARS})\)'
)


def strip_local_line_showrun_css(text: str) -> str:
    return re.sub(
        r"\n\s*\.line-showrun\s*\{[^}]+\}\n",
        "\n",
        text,
        count=1,
    )


def ensure_container_css(text: str) -> str:
    link = '<link rel="stylesheet" href="/css/cli-lab-container.css" />'
    if link in text:
        return text
    if 'href="/css/lab-router-spoiler.css"' in text:
        return text.replace(
            '<link rel="stylesheet" href="/css/lab-router-spoiler.css" />',
            '<link rel="stylesheet" href="/css/lab-router-spoiler.css" />\n  ' + link,
            1,
        )
    return text.replace("</head>", f"  {link}\n</head>", 1)


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    text = APPEND_RE.sub(r'append\1(\2, "line-showrun", \4)', text)
    text = APPEND_CLASS_FIRST_RE.sub(r'appendBlock("line-showrun", \2)', text)

    # Etherchannel summary is not running-config — keep neutral sys styling.
    text = text.replace(
        'appendLine("line-showrun", SHOW_ETHERCHANNEL_SUMMARY)',
        'appendLine("line-sys", SHOW_ETHERCHANNEL_SUMMARY)',
    )

    if "line-showrun" in text and "cli-lab-container.css" in text:
        text = strip_local_line_showrun_css(text)

    text = ensure_container_css(text)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    changed: list[str] = []
    for path in sorted(LABS.rglob("*.html")):
        if patch_file(path):
            changed.append(str(path.relative_to(ROOT)))
    print(f"Updated {len(changed)} file(s):")
    for name in changed:
        print(f"  {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
