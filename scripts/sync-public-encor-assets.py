#!/usr/bin/env python3
"""Copy CCNP-ENCOR-Study assets into public/js and public/css.

The `serve` static server does not follow symlinks, so /js/cli-lab-container.js
and similar paths 404 unless these files are regular copies.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"

PAIRS = (
    ("js/cli-lab-container.js", "CCNP-ENCOR-Study/js/cli-lab-container.js"),
    ("js/cli-ios-mode.js", "CCNP-ENCOR-Study/js/cli-ios-mode.js"),
    ("js/lab-modal-drag.js", "CCNP-ENCOR-Study/js/lab-modal-drag.js"),
    ("js/practice-questions.js", "CCNP-ENCOR-Study/js/practice-questions.js"),
    ("css/cli-lab-container.css", "CCNP-ENCOR-Study/css/cli-lab-container.css"),
    ("css/lab-router-spoiler.css", "CCNP-ENCOR-Study/css/lab-router-spoiler.css"),
)


def main() -> None:
    for dest_rel, src_rel in PAIRS:
        src = PUBLIC / src_rel
        dest = PUBLIC / dest_rel
        if not src.is_file():
            raise SystemExit(f"missing source: {src}")
        data = src.read_bytes()
        if dest.is_symlink() or not dest.exists() or dest.read_bytes() != data:
            dest.unlink(missing_ok=True)
            dest.write_bytes(data)
            print(f"synced {dest_rel}")
        else:
            print(f"ok {dest_rel}")


if __name__ == "__main__":
    main()
