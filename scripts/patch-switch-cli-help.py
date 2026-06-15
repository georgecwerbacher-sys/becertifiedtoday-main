#!/usr/bin/env python3
"""Sync switch IOS `?` help comment blocks from scripts/lib/cli-lab-switch-help.mjs."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HELP_LIB = ROOT / "scripts" / "lib" / "cli-lab-switch-help.mjs"

SKIP_PARTS = {"Unused_Labs", "ENCOR_Samples"}

COMMENT_RE = re.compile(r"<!--([\s\S]*?)-->", re.MULTILINE)
SWITCH_LEGACY_RE = re.compile(
    r"\n  Shared defaults \(/js/cli-lab-container\.js\) when SWITCH_CLI_HELP = null:[\s\S]*?"
    r"(?=\n\n  (?:CCNA |CLI shell|Patterns:|IOS `|CLI lab —|For a fourth|Includes:))",
)


def chains_comment() -> str:
    out = subprocess.run(
        ["node", str(HELP_LIB), "comment-chains"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    lines = []
    for line in out.stdout.rstrip("\n").splitlines():
        lines.append(f"  {line}" if line else "")
    return "\n".join(lines)


def patch_list() -> list[str]:
    out = subprocess.run(
        ["node", str(HELP_LIB), "patch-list"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return [line.strip() for line in out.stdout.splitlines() if line.strip()]


def find_lab_path(basename: str) -> Path | None:
    for path in PUBLIC.rglob(basename):
        if should_skip(path):
            continue
        return path
    return None


def should_skip(path: Path) -> bool:
    return any(part in SKIP_PARTS for part in path.parts)


def strip_switch_help_from_comment(comment: str) -> str:
    updated = SWITCH_LEGACY_RE.sub("", comment, count=1)
    if updated != comment:
        return updated.rstrip()
    match = re.search(r"\n(?:  )?IOS `\?` help — SWITCH_CLI_HELP", comment)
    if match:
        return comment[: match.start()].rstrip()
    return comment


def patch_file(path: Path, new_block: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if 'iosHelpOpts("switch"' not in text:
        return False
    m = COMMENT_RE.search(text)
    if not m:
        return False
    comment = m.group(1)
    if SWITCH_LEGACY_RE.search(comment) or "SWITCH_CLI_HELP" in comment:
        cleaned = strip_switch_help_from_comment(comment)
    elif 'iosHelpOpts("switch"' in text:
        cleaned = comment.rstrip()
    else:
        return False
    updated_comment = cleaned.rstrip() + "\n\n" + new_block + "\n"
    updated = text[: m.start(1)] + updated_comment + text[m.end(1) :]
    if updated == text:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    new_block = chains_comment()
    patched: list[str] = []
    missing: list[str] = []

    for basename in patch_list():
        path = find_lab_path(basename)
        if not path:
            missing.append(basename)
            continue
        if patch_file(path, new_block):
            patched.append(str(path.relative_to(ROOT)))

    print(f"Synced switch help block in {len(patched)} file(s):")
    for line in patched:
        print(f"  {line}")
    if missing:
        print(f"Skipped {len(missing)} profile(s) with no HTML under public/:")
        for line in missing:
            print(f"  {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
