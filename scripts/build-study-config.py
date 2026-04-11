#!/usr/bin/env python3
"""Build public/js/study-config.json: group question IDs into studies by number range.

Study 1: question IDs 1–50, Study 2: 51–100, Study 3: 101–150, and so on (50 per study).
Only IDs that exist as public/question-NNN.html are listed in each study's ``ids``.
Studies are emitted through the last range that contains at least one question (no
trailing empty studies).
"""
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
    if ids:
        max_id = max(ids)
        num_studies = (max_id - 1) // GROUP_SIZE + 1
        for study_idx in range(1, num_studies + 1):
            lo = (study_idx - 1) * GROUP_SIZE + 1
            hi = study_idx * GROUP_SIZE
            chunk = [i for i in ids if lo <= i <= hi]
            studies.append(
                {"index": study_idx, "name": f"Study {study_idx}", "ids": chunk}
            )

    payload = {
        "groupSize": GROUP_SIZE,
        "studies": studies,
        "allIds": ids,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        f"Wrote {len(studies)} studies (ranges of {GROUP_SIZE} by question #), "
        f"{len(ids)} questions -> {OUT.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
