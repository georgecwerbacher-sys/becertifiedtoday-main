#!/usr/bin/env python3
"""Copy templates/lab-build HTML to public/lab-build/ for localhost preview."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "templates" / "lab-build"
DST = ROOT / "public" / "lab-build"


def main() -> None:
    DST.mkdir(parents=True, exist_ok=True)
    copied = 0
    for path in sorted(SRC.glob("*.html")):
        shutil.copy2(path, DST / path.name)
        copied += 1
    print(f"sync-lab-build-preview: copied {copied} file(s) → public/lab-build/")


if __name__ == "__main__":
    main()
