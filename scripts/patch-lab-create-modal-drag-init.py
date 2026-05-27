#!/usr/bin/env python3
"""After createModal appends overlay, call bccInitLabModalDrag for local/dynamic binding."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LABS = ROOT / "public" / "CCNP-ENCOR-Study" / "CCNP-ENCOR-Labs"
MARKER = "if (window.bccInitLabModalDrag) window.bccInitLabModalDrag();"
APPEND_RE = re.compile(
    r"(document\.body\.appendChild\(overlay\);\s*\n)(?!\s*if \(window\.bccInitLabModalDrag\))"
)


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "function createModal" not in text:
        return False
    if MARKER in text:
        return False
    new_text, n = APPEND_RE.subn(r"\1    " + MARKER + "\n", text)
    if n:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main() -> int:
    changed = []
    for path in sorted(LABS.rglob("*.html")):
        if patch_file(path):
            changed.append(str(path.relative_to(ROOT)))
    print(f"Patched {len(changed)} file(s)")
    for name in changed:
        print(f"  {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
