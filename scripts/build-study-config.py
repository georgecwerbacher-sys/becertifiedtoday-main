#!/usr/bin/env python3
"""Build public/js/study-config.json: question IDs grouped into studies of 50."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
OUT = PUBLIC / "js" / "study-config.json"
GROUP_SIZE = 50
QUESTION_RE = re.compile(r"^question-(\d+)\.html$", re.I)


def main() -> None:
    ids: list[int] = []
    for path in PUBLIC.glob("question-*.html"):
        m = QUESTION_RE.match(path.name)
        if m:
            ids.append(int(m.group(1)))
    ids.sort()

    studies: list[dict] = []
    for i in range(0, len(ids), GROUP_SIZE):
        chunk = ids[i : i + GROUP_SIZE]
        n = len(studies) + 1
        studies.append({"index": n, "name": f"Study {n}", "ids": chunk})

    payload = {
        "groupSize": GROUP_SIZE,
        "studies": studies,
        "allIds": ids,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(studies)} studies, {len(ids)} questions -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
