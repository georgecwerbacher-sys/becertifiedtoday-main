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
DROP_SLOT_CLASS_RE = re.compile(r'class="[^"]*\bdrop-slot\b[^"]*"', re.I)
JSON_DRAGDROP_EXCLUDE_IDS = {271, 309, 405}


def main() -> None:
    ids: list[int] = []
    drag_drop_ids: list[int] = []
    drag_drop_json_ids: list[int] = []
    for path in PUBLIC.glob("question-*.html"):
        m = QUESTION_RE.match(path.name)
        if m:
            qid = int(m.group(1))
            ids.append(qid)
            try:
                html = path.read_text(encoding="utf-8")
            except OSError:
                html = ""
            is_drag_drop = bool(DROP_SLOT_CLASS_RE.search(html)) and 'draggable="true"' in html
            if is_drag_drop:
                drag_drop_ids.append(qid)
                if qid not in JSON_DRAGDROP_EXCLUDE_IDS and "json" in html.lower():
                    drag_drop_json_ids.append(qid)
    ids.sort()
    drag_drop_ids.sort()
    drag_drop_json_ids.sort()
    drag_drop_standard_ids = [i for i in drag_drop_ids if i not in set(drag_drop_json_ids)]

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
        "dragDropIds": drag_drop_standard_ids,
        "dragDropJsonIds": drag_drop_json_ids,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        f"Wrote {len(studies)} studies (ranges of {GROUP_SIZE} by question #), "
        f"{len(ids)} questions -> {OUT.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
