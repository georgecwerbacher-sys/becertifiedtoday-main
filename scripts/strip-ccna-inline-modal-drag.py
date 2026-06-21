#!/usr/bin/env python3
"""Remove duplicate inline wireFloatingModal from CCNA labs (shared /js/lab-modal-drag.js handles drag+resize)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LABS = ROOT / "public" / "CCNA-Study" / "CCNA_labs"

FUNC_RE = re.compile(
    r"\n      function wireFloatingModal\(dialogEl, overlayEl\) \{.*?\n      \}\n",
    re.DOTALL,
)
CALL_RE = re.compile(r"\n      wireFloatingModal\([^\n]+\);\n")


def main() -> None:
    for path in sorted(LABS.glob("*.html")):
        text = path.read_text(encoding="utf-8")
        if "function wireFloatingModal" not in text:
            continue
        updated = FUNC_RE.sub("\n", text)
        updated = CALL_RE.sub("\n", updated)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            print(f"stripped {path.name}")


if __name__ == "__main__":
    main()
