#!/usr/bin/env python3
"""Sync router IOS `?` help comment blocks from scripts/lib/cli-lab-router-help.mjs."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HELP_LIB = ROOT / "scripts" / "lib" / "cli-lab-router-help.mjs"

SKIP_PARTS = {"Unused_Labs", "ENCOR_Samples"}

COMMENT_RE = re.compile(r"<!--([\s\S]*?)-->", re.MULTILINE)
HELP_START_RE = re.compile(r"\n(?:  )?IOS `\?` help — ROUTER_CLI_HELP")


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
    if "/" in basename:
        candidate = PUBLIC / basename.replace("CCNA_Samples/", "CCNA-Study/CCNA_Samples/")
        if candidate.is_file():
            return candidate
    for path in PUBLIC.rglob(basename):
        if should_skip(path):
            continue
        return path
    return None


def should_skip(path: Path) -> bool:
    return any(part in SKIP_PARTS for part in path.parts)


def strip_router_help_from_comment(comment: str) -> str:
    match = HELP_START_RE.search(comment)
    if not match:
        return comment
    return comment[: match.start()].rstrip()


def patch_file(path: Path, new_block: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if 'iosHelpOpts("router"' not in text:
        return False
    m = COMMENT_RE.search(text)
    if not m:
        return False
    comment = m.group(1)
    if not HELP_START_RE.search(comment) and "Shared defaults (/js/cli-lab-container.js)" in comment:
        # static-routing style — replace legacy shared-defaults router help intro
        comment = re.sub(
            r"\n\n  Shared defaults \(/js/cli-lab-container\.js\):[\s\S]*?"
            r"(?=\n\n  CLI lab baseline|\n\n  Includes:|\n-->)",
            "",
            comment,
            count=1,
        )
    cleaned = strip_router_help_from_comment(comment)
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

    print(f"Synced router help block in {len(patched)} file(s):")
    for line in patched:
        print(f"  {line}")
    if missing:
        print(f"Skipped {len(missing)} profile(s) with no HTML under public/:")
        for line in missing:
            print(f"  {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
