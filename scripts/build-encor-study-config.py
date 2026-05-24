#!/usr/bin/env python3
"""Build public/CCNP-ENCOR-Study/js/study-config.json from ENCOR question HTML.

MCQ pages live under ``public/CCNP-ENCOR-Study/ENCOR_Questions/``.
Drag-and-drop pages live under ``public/CCNP-ENCOR-Study/CCNP-ENCOR-Drag-Drop/``.
Practice banks slice ``allIds`` (MCQ only) in hub order — up to 100 per bank.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MCQ_DIR = ROOT / "public" / "CCNP-ENCOR-Study" / "ENCOR_Questions"
DRAG_DROP_DIR = ROOT / "public" / "CCNP-ENCOR-Study" / "CCNP-ENCOR-Drag-Drop"
OUT = ROOT / "public" / "CCNP-ENCOR-Study" / "js" / "study-config.json"
GROUP_SIZE = 50
QUESTION_RE = re.compile(r"^question-(\d+)\.html$", re.I)
DROP_SLOT_CLASS_RE = re.compile(r'class="[^"]*\bdrop-slot\b[^"]*"', re.I)
JSON_DRAGDROP_EXCLUDE_IDS = {271, 309, 405}
JSON_DRAGDROP_INCLUDE_IDS = {18, 33, 363}


def is_drag_drop_html(html: str) -> bool:
    return bool(DROP_SLOT_CLASS_RE.search(html)) and 'draggable="true"' in html


def classify_drag_drop(qid: int, html: str) -> tuple[bool, bool]:
    if not is_drag_drop_html(html):
        return False, False
    is_json = qid in JSON_DRAGDROP_INCLUDE_IDS or (
        qid not in JSON_DRAGDROP_EXCLUDE_IDS and "json" in html.lower()
    )
    return True, is_json


def main() -> None:
    ids: list[int] = []
    drag_drop_ids: list[int] = []
    drag_drop_json_ids: list[int] = []

    for path in sorted(MCQ_DIR.glob("question-*.html")):
        m = QUESTION_RE.match(path.name)
        if not m:
            continue
        qid = int(m.group(1))
        try:
            html = path.read_text(encoding="utf-8")
        except OSError:
            html = ""
        is_dd, _ = classify_drag_drop(qid, html)
        if is_dd:
            print(f"Warning: drag-and-drop page still in ENCOR_Questions: {path.name}")
        else:
            ids.append(qid)

    DRAG_DROP_DIR.mkdir(parents=True, exist_ok=True)
    for path in sorted(DRAG_DROP_DIR.glob("question-*.html")):
        m = QUESTION_RE.match(path.name)
        if not m:
            continue
        qid = int(m.group(1))
        try:
            html = path.read_text(encoding="utf-8")
        except OSError:
            html = ""
        is_dd, is_json = classify_drag_drop(qid, html)
        if is_dd:
            drag_drop_ids.append(qid)
            if is_json:
                drag_drop_json_ids.append(qid)
        else:
            print(f"Warning: non drag-and-drop page in CCNP-ENCOR-Drag-Drop: {path.name}")

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
        "dragDropDirectory": "CCNP-ENCOR-Study/CCNP-ENCOR-Drag-Drop",
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
