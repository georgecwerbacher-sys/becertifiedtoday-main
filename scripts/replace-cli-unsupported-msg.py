#!/usr/bin/env python3
"""Replace legacy CLI invalid-input strings with the lab simulation message."""
from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCAN_DIRS = (
    ROOT / "public",
    ROOT / "templates",
)

NEW_BASE = "% command not supported in this lab simulation"
NEW_NUMERIC_HINT = (
    "% command not supported in this lab simulation — "
    "check the lab Tasks and Verification sections for the exact values."
)
NEW_VERIFY_HINT = (
    "% command not supported in this lab simulation. "
    "Verify the lab instructions (Tasks and Helper) for the required values."
)

# Longest / most specific replacements first.
REPLACEMENTS = [
    (
        "% Invalid input — check the lab Tasks and Verification sections for the exact values.",
        NEW_NUMERIC_HINT,
    ),
    (
        "% Invalid input. Verify the lab instructions (Tasks and Helper) for the required values.",
        NEW_VERIFY_HINT,
    ),
    ("% Invalid — check task order and syntax.", f"{NEW_BASE} — check task order and syntax."),
    ("Not supported in this simulation", NEW_BASE),
    ("% Invalid input", NEW_BASE),
]

EXTENSIONS = {".html", ".js", ".py", ".md", ".mdc"}


def patch_file(path: pathlib.Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed: list[str] = []
    for base in SCAN_DIRS:
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix not in EXTENSIONS:
                continue
            if patch_file(path):
                changed.append(str(path.relative_to(ROOT)))
    print(f"Updated {len(changed)} file(s)")
    for rel in sorted(changed):
        print(f"  {rel}")


if __name__ == "__main__":
    main()
