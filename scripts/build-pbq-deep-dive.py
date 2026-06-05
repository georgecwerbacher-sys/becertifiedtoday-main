#!/usr/bin/env python3
"""Generate secplus-pbq-deep-dive-data.js from marketing-vault deep-dive-solution.md files."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

_spec = importlib.util.spec_from_file_location(
    "build_pbq_production_suite",
    ROOT / "scripts/build-pbq-production-suite.py",
)
_mod = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_mod)
SCENARIOS = _mod.SCENARIOS

from pbq_deep_dive_md import write_deep_dive_js  # noqa: E402

OUT = ROOT / "public/COMP_TIA_SEC+/js/secplus-pbq-deep-dive-data.js"


def main() -> None:
    slugs = [sc["slug"] for sc in SCENARIOS]
    count = write_deep_dive_js(slugs, OUT)
    print(f"wrote {OUT.relative_to(ROOT)} ({count} scenarios)")


if __name__ == "__main__":
    main()
