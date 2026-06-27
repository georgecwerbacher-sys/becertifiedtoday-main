#!/usr/bin/env python3
"""Set question-page exam version badges (601 vs 701) from topic-map objective IDs."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAP = ROOT / "public/COMP_TIA_SEC+/data/secplus-question-topic-map.json"
BLUEPRINT_701 = ROOT / "public/COMP_TIA_SEC+/data/secplus-blueprint-sy0-701.json"
QUESTIONS_DIR = ROOT / "public/COMP_TIA_SEC+/SEC+_Questions"
LEGACY_JSON = ROOT / "public/COMP_TIA_SEC+/data/secplus-legacy-601-questions.json"

VERSION_RE = re.compile(
    r'(<span class="question-topic-meta__version">)(701|601)(</span>)',
    re.MULTILINE,
)


def load_valid_701_objectives() -> set[str]:
    data = json.loads(BLUEPRINT_701.read_text(encoding="utf-8"))
    valid: set[str] = set()

    def walk(nodes: list | None) -> None:
        for node in nodes or []:
            oid = node.get("id")
            if isinstance(oid, str) and re.fullmatch(r"\d+\.\d+", oid):
                valid.add(oid)
            walk(node.get("children"))

    for domain in data.get("domains") or []:
        walk(domain.get("objectives"))

    return valid


def objectives_for_entry(entry: object) -> list[str]:
    if isinstance(entry, list):
        return [str(x) for x in entry]
    if isinstance(entry, dict):
        return [str(x) for x in (entry.get("objectives") or [])]
    return []


def classify_outdated(assignments: dict, valid_701: set[str]) -> dict[str, dict]:
    outdated: dict[str, dict] = {}
    for file_name, entry in sorted(assignments.items()):
        objs = objectives_for_entry(entry)
        unknown = [o for o in objs if o not in valid_701]
        if unknown:
            outdated[file_name] = {
                "examVersion": "601",
                "legacyObjectives": unknown,
                "reason": "non_pdf_objective_id_remap_needed",
            }
    return outdated


def patch_html_version(path: Path, version: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if 'class="question-topic-meta__version"' not in text:
        return False

    def repl(match: re.Match[str]) -> str:
        return match.group(1) + version + match.group(3)

    new_text, count = VERSION_RE.subn(repl, text, count=1)
    if count == 0:
        return False
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    topic_map = json.loads(MAP.read_text(encoding="utf-8"))
    assignments = topic_map.get("assignments") or {}
    valid_701 = load_valid_701_objectives()
    outdated = classify_outdated(assignments, valid_701)

    legacy_files = sorted(outdated.keys())
    legacy_slugs = [f.replace(".html", "") for f in legacy_files]
    LEGACY_JSON.write_text(
        json.dumps(
            {
                "exam": "SY0-601",
                "bankTitle": "SY0-601 Outdated",
                "auditNote": (
                    "Audit archive: items carry legacy SY0-601 objective tags not on the official "
                    "SY0-701 study path. Banked for future remap or retirement—not mixed into "
                    "SY0-701 Random/Review pools."
                ),
                "notes": (
                    "Practice items tagged with legacy objective IDs not on the official "
                    "SY0-701 PDF. Shown as 601 until remapped or retired."
                ),
                "slugs": legacy_slugs,
                "files": legacy_files,
                "byFile": outdated,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    updated_601 = 0
    updated_701 = 0
    missing_html = 0

    for file_name in assignments:
        path = QUESTIONS_DIR / file_name
        target = "601" if file_name in outdated else "701"
        if not path.is_file():
            if file_name in outdated:
                missing_html += 1
            continue
        if patch_html_version(path, target):
            if target == "601":
                updated_601 += 1
            else:
                updated_701 += 1

    print(
        f"[sync-secplus-question-exam-version] legacy 601: {len(legacy_files)} · "
        f"html patched → 601: {updated_601}, reaffirmed 701: {updated_701}"
    )
    if missing_html:
        print(f"[sync-secplus-question-exam-version] warning: {missing_html} legacy file(s) missing HTML")
    print(f"[sync-secplus-question-exam-version] wrote {LEGACY_JSON.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
