#!/usr/bin/env python3
"""Replace question-bank version labels V_2025/V_2026 → V_2025/V_2026 across the repo."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Paths whose *content* should not get lowercase V_2025/V_2026 swaps (Cisco exam objective files, etc.)
SKIP_LOWERCASE_REPLACE = frozenset(
    {
        "public/CCNA-Study/data/ccna-exam-objectives-200-301-v1.1.json",
    }
)

# File extensions to scan (skip binaries, images, lockfiles)
TEXT_SUFFIXES = {
    ".html",
    ".js",
    ".json",
    ".md",
    ".py",
    ".csv",
    ".txt",
    ".mjs",
    ".mdc",
    ".canvas",
}

SKIP_DIR_NAMES = {
    ".git",
    "node_modules",
    ".obsidian",
}

# Longer phrases first.
EXACT_REPLACEMENTS = [
    ("V_2025 & V_2026", "V_2025 & V_2026"),
    ("V_2025 and V_2026", "V_2025 and V_2026"),
    ("V_2025 & V_2026", "V_2025 & V_2026"),
    ("V_2025 and V_2026", "V_2025 and V_2026"),
    ("V_2025", "V_2025"),
    ("V_2026", "V_2026"),
    ("V_2025", "V_2025"),
    ("V_2026", "V_2026"),
    ("V_2025 &amp; V_2026", "V_2025 &amp; V_2026"),
    ("V_2025 & V_2026", "V_2025 & V_2026"),
    ("V_2025 and V_2026", "V_2025 and V_2026"),
    ("V_2025 &amp; V_2026", "V_2025 &amp; V_2026"),  # duplicate-safe
    ("CCNA V_2025", "CCNA V_2025"),
    ("blueprint: V_2025", "blueprint: V_2025"),
    ("blueprint: V_2026", "blueprint: V_2026"),
    ("version_folder: V_2025", "version_folder: V_2025"),
    ("version_folder: V_2026", "version_folder: V_2026"),
    ("V_2025", "V_2025"),
    ("V_2026", "V_2026"),
    ('"V_2025"', '"V_2025"'),
    ('"V_2026"', '"V_2026"'),
    ("v2025", "v2025"),
    ("V_2025 & 2.0", "V_2025 & V_2026"),
    ("V_2025 &amp; 2.0", "V_2025 &amp; V_2026"),
    ("version 2026 slugs", "version 2026 slugs"),
    ("V_2026 slug", "V_2026 slug"),
    ("tagged V_2026", "tagged V_2026"),
    ("excludes tagged V_2026", "excludes tagged V_2026"),
    ("V_2025 (default bank set)", "V_2025 (default bank set)"),
    ("V_2026 (~70 tagged questions)", "V_2026 (~70 tagged questions)"),
    ("Current V_2025 MCQ preview", "Current V_2025 MCQ preview"),
    ("Latest V_2025 Questions", "Latest V_2025 Questions"),
    ("Full V_2025 question bank", "Full V_2025 question bank"),
    ("800+ Qs · V_2025 & V_2026", "800+ Qs · V_2025 & V_2026"),
    ("V_2025 & V_2026 · Verified", "V_2025 & V_2026 · Verified"),
    ("V_2025 & V_2026 Question Bank", "V_2025 & V_2026 Question Bank"),
    ("700+ CCNA questions V_2025 & V_2026", "700+ CCNA questions V_2025 & V_2026"),
    ("700+ Qs V_2025 & V_2026", "700+ Qs V_2025 & V_2026"),
    ("V_2025 & V_2026 Questions", "V_2025 & V_2026 Questions"),
    ("aligned to objectives <strong>V_2025</strong>", "aligned to objectives <strong>V_2025</strong>"),
    ("objectives (V_2025)", "objectives (V_2025)"),
    ("200-301 V_2025", "200-301 V_2025"),
    ("200-301 objectives (V_2025)", "200-301 objectives (V_2025)"),
    ("CCNA 200-301 V_2025", "CCNA 200-301 V_2025"),
    ("CCNA V_2025,", "CCNA V_2025,"),
    ("CCNA V_2025 exam", "CCNA V_2025 exam"),
    ("CCNA V_2025 emphasizes", "CCNA V_2025 emphasizes"),
    ("CCNA V_2025 replacement", "CCNA V_2025 replacement"),
    ("not the CCNA V_2025", "not the CCNA V_2025"),
    ("ccna-version-2026-slugs.json", "ccna-version-2026-slugs.json"),
]

# Standalone lowercase V_2025 / V_2026 in prose (after exact passes).
LOWERCASE_WORD_RE = re.compile(r"\bv1\.1\b|\bv2\.0\b")


def should_scan(path: Path) -> bool:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return False
    rel = path.relative_to(ROOT).as_posix()
    if rel in SKIP_LOWERCASE_REPLACE:
        return False
    for part in path.parts:
        if part in SKIP_DIR_NAMES:
            return False
    return True


def transform(text: str, rel_path: str) -> str:
    out = text
    for old, new in EXACT_REPLACEMENTS:
        if old == new:
            continue
        out = out.replace(old, new)

    if rel_path in SKIP_LOWERCASE_REPLACE:
        return out

    def lower_sub(m: re.Match[str]) -> str:
        return "V_2025" if m.group(0) == "V_2025" else "V_2026"

    out = LOWERCASE_WORD_RE.sub(lower_sub, out)
    return out


def iter_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if not should_scan(path):
            continue
        if any(part in SKIP_DIR_NAMES for part in path.parts):
            continue
        files.append(path)
    return files


def main() -> int:
    changed = 0
    for path in iter_files():
        rel = path.relative_to(ROOT).as_posix()
        original = path.read_text(encoding="utf-8")
        updated = transform(original, rel)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    print(f"Updated {changed} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
