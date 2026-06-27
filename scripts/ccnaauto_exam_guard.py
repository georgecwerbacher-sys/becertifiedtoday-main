"""CCNAAUTO 200-901 hunt scope — reject CCNA 200-301 bleed-through."""
from __future__ import annotations

EXAM = "CCNAAUTO-200-901"
REJECT_MARKERS = ("200-301", "ccna-hunt-import", "ccna-200-301")


def row_exam_blob(row: dict) -> str:
    return " ".join(
        (row.get(k) or "") for k in ("source_id", "source_version", "source_url", "topic_notes")
    ).lower()


def is_ccnaauto_hunt_row(row: dict) -> bool:
    blob = row_exam_blob(row)
    return not any(marker in blob for marker in REJECT_MARKERS)


def filter_ccnaauto_rows(rows: list[dict], label: str = "collect") -> list[dict]:
    kept = [row for row in rows if is_ccnaauto_hunt_row(row)]
    skipped = len(rows) - len(kept)
    if skipped:
        print(
            f"[{label}] rejected {skipped} row(s) — CCNAAUTO 200-901 only "
            "(not CCNA 200-301 / ccna-hunt-import)",
            flush=True,
        )
    return kept
