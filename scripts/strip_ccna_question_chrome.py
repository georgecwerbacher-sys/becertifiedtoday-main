#!/usr/bin/env python3
"""Remove stem-note line, .stem-note CSS, Reset button, and resetBtn JS from CCNA question HTML."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

STEM_P = re.compile(r"\s*<p class=\"stem-note\">.*?</p>\s*", re.DOTALL)
STEM_CSS = re.compile(r"\s*\.stem-note\s*\{[^}]*\}\s*")
RESET_BTN = re.compile(r"\s*<button id=\"resetBtn\"[^>]*>Reset</button>\s*")
VAR_RESET = re.compile(r"\s*var resetBtn = document\.getElementById\(\"resetBtn\"\);\s*")


def strip_reset_listener(lines: list[str]) -> list[str]:
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if "resetBtn.addEventListener" in line:
            depth = 0
            started = False
            while i < len(lines):
                cur = lines[i]
                for ch in cur:
                    if ch == "{":
                        depth += 1
                        started = True
                    elif ch == "}" and started:
                        depth -= 1
                i += 1
                if started and depth == 0:
                    break
            continue
        out.append(line)
        i += 1
    return out


def strip_one(html: str) -> str:
    t = STEM_CSS.sub("\n", html)
    t = STEM_P.sub("\n", t)
    t = RESET_BTN.sub("\n", t)
    t = VAR_RESET.sub("\n", t)
    lines = t.splitlines(keepends=True)
    lines = strip_reset_listener(lines)
    return "".join(lines)


def main(paths: list[Path]) -> None:
    changed = 0
    for path in paths:
        if not path.is_file():
            continue
        raw = path.read_text(encoding="utf-8")
        new = strip_one(raw)
        if new != raw:
            path.write_text(new, encoding="utf-8")
            changed += 1
    print(f"Updated {changed} file(s).")


if __name__ == "__main__":
    dirs = [
        ROOT / "public/CCNA-Study/CCNA_questions",
        ROOT / "public/CCNA-Study/CCNA_Samples",
    ]
    files: list[Path] = []
    for d in dirs:
        if not d.is_dir():
            continue
        if d.name == "CCNA_Samples":
            files.extend(sorted(d.glob("sample-question-*.html")))
        else:
            files.extend(sorted(d.glob("*.html")))
    main(files)
