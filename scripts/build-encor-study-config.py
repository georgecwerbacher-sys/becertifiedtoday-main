#!/usr/bin/env python3
"""Build public/CCNP-ENCOR-Study/js/study-config.json from ENCOR_Questions HTML.

Practice banks slice ``allIds`` (MCQ only, drag-and-drop excluded) in hub order —
one file per ``public/CCNP-ENCOR-Study/ENCOR_Questions/question-NNN.html``.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUESTIONS_DIR = ROOT / "public" / "CCNP-ENCOR-Study" / "ENCOR_Questions"
OUT = ROOT / "public" / "CCNP-ENCOR-Study" / "js" / "study-config.json"
GROUP_SIZE = 50
QUESTION_RE = re.compile(r"^question-(\d+)\.html$", re.I)
DROP_SLOT_CLASS_RE = re.compile(r'class="[^"]*\bdrop-slot\b[^"]*"', re.I)
JSON_DRAGDROP_EXCLUDE_IDS = {271, 309, 405}
JSON_DRAGDROP_INCLUDE_IDS = {18, 33, 363}


def main() -> None:
    ids: list[int] = []
    drag_drop_ids: list[int] = []
    drag_drop_json_ids: list[int] = []

    for path in sorted(QUESTIONS_DIR.glob("question-*.html")):
        m = QUESTION_RE.match(path.name)
        if not m:
            continue
        qid = int(m.group(1))
        try:
            html = path.read_text(encoding="utf-8")
        except OSError:
            html = ""
        is_drag_drop = bool(DROP_SLOT_CLASS_RE.search(html)) and 'draggable="true"' in html
        if is_drag_drop:
            drag_drop_ids.append(qid)
            if qid in JSON_DRAGDROP_INCLUDE_IDS or (
                qid not in JSON_DRAGDROP_EXCLUDE_IDS and "json" in html.lower()
            ):
                drag_drop_json_ids.append(qid)
        else:
            ids.append(qid)

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
            if chunk:
                studies.append(
                    {"index": study_idx, "name": f"Study {study_idx}", "ids": chunk}
                )

    payload = {
        "sourceDirectory": "CCNP-ENCOR-Study/ENCOR_Questions",
        "groupSize": GROUP_SIZE,
        "studies": studies,
        "allIds": ids,
        "dragDropIds": drag_drop_standard_ids,
        "dragDropJsonIds": drag_drop_json_ids,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        f"Wrote {len(studies)} studies, {len(ids)} MCQ ids, "
        f"{len(drag_drop_standard_ids)} standard D&D, {len(drag_drop_json_ids)} JSON D&D "
        f"-> {OUT.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
