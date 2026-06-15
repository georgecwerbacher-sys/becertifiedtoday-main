#!/usr/bin/env python3
"""Sync router and switch IOS `?` help comment blocks."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    router = subprocess.run([sys.executable, str(ROOT / "scripts/patch-router-cli-help.py")], cwd=ROOT)
    switch = subprocess.run([sys.executable, str(ROOT / "scripts/patch-switch-cli-help.py")], cwd=ROOT)
    return router.returncode or switch.returncode


if __name__ == "__main__":
    sys.exit(main())
