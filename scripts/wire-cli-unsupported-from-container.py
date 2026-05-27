#!/usr/bin/env python3
"""Wire lab pages to cli-lab-container.js for unsupported-command messages."""

from __future__ import annotations

import re
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCAN_DIRS = (ROOT / "public", ROOT / "templates")
CONTAINER_JS = '<script src="/js/cli-lab-container.js"></script>'
MSG = "% command not supported in this lab simulation"
VERIFY_MSG = (
    "% command not supported in this lab simulation. "
    "Verify the lab instructions (Tasks and Helper) for the required values."
)
NUMERIC_MSG = (
    "% command not supported in this lab simulation — "
    "check the lab Tasks and Verification sections for the exact values."
)

LOCAL_BLOCK_RE = re.compile(
    r"\n[ \t]*var INVALID_INPUT_MSG = .*?"
    r"\n[ \t]*function invalidInputMsgForNormalizedCmd\(u\) \{.*?\n[ \t]*\}\n",
    re.DOTALL,
)

OSPF_VERIFY_RE = re.compile(
    r"(var OSPF_LAB_VERIFY_INSTRUCTIONS_MSG\s*=\s*)"
    r'"% command not supported in this lab simulation";',
)


def has_container_js(text: str) -> bool:
    return "/js/cli-lab-container.js" in text


def insert_container_js(text: str) -> str:
    if has_container_js(text):
        return text
    # Prefer after cli-lab-container.css link
    css = '<link rel="stylesheet" href="/css/cli-lab-container.css" />'
    if css in text:
        return text.replace(css, css + "\n  " + CONTAINER_JS, 1)
    # After viewport meta in head
    viewport = '<meta name="viewport" content="width=device-width, initial-scale=1.0" />'
    if viewport in text:
        return text.replace(viewport, viewport + "\n  " + CONTAINER_JS, 1)
    return text


def patch_file(path: pathlib.Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    if MSG not in text and VERIFY_MSG not in text and "INVALID_INPUT_MSG" not in text:
        return False

    text = insert_container_js(text)
    text = LOCAL_BLOCK_RE.sub(
        "\n      // invalidInputMsgForNormalizedCmd + cliLabContainer.* — from /js/cli-lab-container.js.\n",
        text,
    )
    text = text.replace(f'"{MSG}"', "cliLabContainer.INVALID_INPUT_MSG")
    text = text.replace(f'"{VERIFY_MSG}"', "cliLabContainer.CLI_VERIFY_INSTRUCTIONS_MSG")
    text = text.replace(f'"{NUMERIC_MSG}"', "cliLabContainer.CLI_UNSUPPORTED_NUMERIC_HINT_MSG")
    text = OSPF_VERIFY_RE.sub(
        r"\1cliLabContainer.CLI_VERIFY_INSTRUCTIONS_MSG;",
        text,
    )

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed: list[str] = []
    for base in SCAN_DIRS:
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.html")):
            if patch_file(path):
                changed.append(str(path.relative_to(ROOT)))
    print(f"Updated {len(changed)} file(s)")
    for rel in changed:
        print(f"  {rel}")


if __name__ == "__main__":
    main()
