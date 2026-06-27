#!/usr/bin/env python3
"""Regenerate CCNA-Auto Obsidian hunt views from CCNA-Auto/hunt-results/ export."""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from ccnaauto_exam_guard import EXAM

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "CCNA-Auto"
HUNT = ROOT / "CCNA-Auto" / "hunt-results"
VERSION_DIR = "v1.1"
LABS_DIR = "labs"


def md_table(headers: list[str], rows: list[tuple]) -> list[str]:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for row in rows:
        cells = []
        for cell in row:
            text = str(cell)
            if text.startswith("[[") and "]]" in text:
                cells.append(text)
            else:
                cells.append(text.replace("|", "/"))
        out.append("| " + " | ".join(cells) + " |")
    return out


def latest_run_dir() -> Path | None:
    runs = sorted(HUNT.glob("20*"), key=lambda p: p.name, reverse=True)
    for run in runs:
        if run.is_dir() and run.name.count("-") == 2:
            return run
    return None


def latest_run_id() -> str | None:
    run_dir = latest_run_dir()
    return run_dir.name if run_dir else None


def parse_note_meta(path: Path) -> dict[str, str]:
    meta: dict[str, str] = {}
    if not path.is_file():
        return meta
    in_fm = False
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.strip() == "---":
            in_fm = not in_fm
            if not in_fm:
                break
            continue
        if in_fm and ":" in line:
            key, val = line.split(":", 1)
            meta[key.strip()] = val.strip()
    return meta


def note_stem(path: Path) -> str:
    body = path.read_text(encoding="utf-8", errors="replace")
    past = False
    fm = 0
    for line in body.splitlines():
        if line.strip() == "---":
            fm += 1
            if fm == 2:
                past = True
            continue
        if not past or line.startswith("#") or line.startswith("**"):
            continue
        s = line.strip()
        if s:
            return s[:120]
    return path.stem.replace("-", " ")


def wikilink(run_id: str, subpath: str) -> str:
    base = subpath.split("/")[-1]
    return f"[[hunt-results/{run_id}/{subpath}|{base}]]"


def collect_mcq(run_dir: Path) -> list[tuple[str, str, str, str]]:
    mcq_root = run_dir / VERSION_DIR
    if not mcq_root.is_dir():
        return []
    rows: list[tuple[str, str, str, str]] = []
    for path in sorted(mcq_root.glob("Q*.md")):
        meta = parse_note_meta(path)
        rel = f"{VERSION_DIR}/{path.stem}"
        rows.append((
            wikilink(run_dir.name, rel),
            note_stem(path),
            meta.get("source_id", ""),
            meta.get("source_question_id", ""),
        ))
    return rows


def collect_labs(run_dir: Path, drag_only: bool = False) -> list[tuple[str, str, str, str]]:
    labs_root = run_dir / LABS_DIR
    if not labs_root.is_dir():
        return []
    rows: list[tuple[str, str, str, str]] = []
    for path in sorted(labs_root.glob("L*.md")):
        meta = parse_note_meta(path)
        content_type = meta.get("content_type", "")
        if drag_only and content_type != "drag-and-drop":
            continue
        if not drag_only and content_type == "drag-and-drop":
            continue
        rel = f"{LABS_DIR}/{path.stem}"
        rows.append((
            wikilink(run_dir.name, rel),
            note_stem(path),
            meta.get("source_id", ""),
            content_type or "labs-sim",
        ))
    return rows


def collect_dnd(run_dir: Path) -> list[tuple[str, str, str, str]]:
    return collect_labs(run_dir, drag_only=True)


def write_bct_overlap_reference() -> None:
    """Interim dedupe list — not hunt findings."""
    import json

    qdir = ROOT / "public" / "CCNA-Study" / "CCNA_questions"
    topic_map = json.loads(
        (ROOT / "public" / "CCNA-Study" / "data" / "ccna-question-topic-map.json").read_text(encoding="utf-8")
    )
    prefixes = ("6.",)
    keywords = (
        "ansible", "terraform", "rest-api", "json-", "sdn", "automation", "programmability", "dna-center",
    )
    slugs: list[str] = []
    for fn, objs in sorted(topic_map.get("assignments", {}).items()):
        obj_ids = [str(o) for o in objs]
        if any(o.startswith(prefixes) for o in obj_ids) or any(kw in fn for kw in keywords):
            slugs.append(fn.replace(".html", ""))

    lines = [
        "---", "type: hunt-reference", f"exam: {EXAM}", f"generated: {date.today().isoformat()}", "---", "",
        "# BCT overlap reference (interim dedupe)", "",
        f"**{len(slugs)}** CCNA 200-301 bank pages used to dedupe CCNAAUTO hunt rows — not hunt findings.", "",
        "Preview: `http://localhost:3000/CCNA-Study/CCNA_questions/{{slug}}.html`", "",
        "Back: [[hunt-inventory|Hunt results]]", "", "---", "",
    ]
    for slug in slugs:
        lines.append(f"- `{slug}` — [open](http://localhost:3000/CCNA-Study/CCNA_questions/{slug}.html)")
    (OUT / "bct-overlap-reference.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    run_dir = latest_run_dir()
    run_id = run_dir.name if run_dir else "none"
    mcq = collect_mcq(run_dir) if run_dir else []
    labs = collect_labs(run_dir) if run_dir else []
    dnd = collect_dnd(run_dir) if run_dir else []

    run_index = f"[[hunt-results/{run_id}|Run {run_id}]]" if run_dir else "_no export yet — run `npm run ccnaauto:hunt`_"

    (OUT / "hunt-inventory.md").write_text(
        "\n".join([
            "---", "type: hunt-inventory", f"exam: {EXAM}", f"generated: {date.today().isoformat()}", "---", "",
            "# CCNAAUTO 200-901 hunt results", "",
            f"Latest run: {run_index} · **Open questions:** [[hunt-results/{run_id}/{VERSION_DIR}|MCQ folder]] · "
            f"[[hunt-results/{run_id}|run index]]" if run_dir else
            f"Latest run: {run_index}",
            "",
            "Rerun: `npm run ccnaauto:hunt`", "",
            "| Category | Hunt net-new |",
            "|----------|-------------:|",
            f"| MCQ questions | {len(mcq)} |",
            f"| Labs / PBQ | {len(labs)} |",
            f"| Drag-and-drop signals | {len(dnd)} |", "",
            "[[hunt-inventory-questions|Questions]] · [[hunt-inventory-labs|Labs & PBQ]] · "
            "[[hunt-inventory-drag-drop|Drag-and-drop]] · [[competitor-list|Competitor list]]", "",
            "BCT overlap dedupe reference (CCNA 200-301 automation slugs): [[bct-overlap-reference|BCT overlap]]", "",
            "Back: [[README|CCNA-Auto]]", "",
        ]) + "\n",
        encoding="utf-8",
    )

    (OUT / "hunt-inventory-questions.md").write_text(
        "\n".join([
            "---", "type: hunt-inventory", f"exam: {EXAM}", "category: mcq",
            f"generated: {date.today().isoformat()}", "---", "",
            "# CCNAAUTO 200-901 — hunt MCQs", "",
            f"Run: {run_index} · **{len(mcq)}** questions", "",
            "Back: [[hunt-inventory|Inventory]] · [[blueprint-hunt-list|Blueprint]]", "", "---", "",
        ] + (md_table(["Note", "Stem", "Source", "Q ID"], mcq) if mcq else [
            "_No MCQ export yet. Run `npm run ccnaauto:hunt`._",
        ])) + "\n",
        encoding="utf-8",
    )

    (OUT / "hunt-inventory-labs.md").write_text(
        "\n".join([
            "---", "type: hunt-inventory", f"exam: {EXAM}", "category: labs",
            f"generated: {date.today().isoformat()}", "---", "",
            "# CCNAAUTO 200-901 — hunt labs / PBQ", "",
            f"Run: {run_index} · **{len(labs)}** items (excludes drag-and-drop signals)", "",
            "Back: [[hunt-inventory|Inventory]] · [[hunt-inventory-drag-drop|Drag-and-drop]]", "", "---", "",
        ] + (md_table(["Note", "Stem", "Source", "Type"], labs) if labs else [
            "_No labs/PBQ export yet. Run `npm run ccnaauto:hunt`._",
        ])) + "\n",
        encoding="utf-8",
    )

    (OUT / "hunt-inventory-drag-drop.md").write_text(
        "\n".join([
            "---", "type: hunt-inventory", f"exam: {EXAM}", "category: drag-drop",
            f"generated: {date.today().isoformat()}", "---", "",
            "# CCNAAUTO 200-901 — hunt drag-and-drop signals", "",
            f"Run: {run_index} · **{len(dnd)}** competitor page signals (verify + capture before draft)", "",
            "Back: [[hunt-inventory|Inventory]]", "", "---", "",
        ] + (md_table(["Note", "Stem", "Source", "Type"], dnd) if dnd else [
            "_No drag-and-drop signals in latest labs export._",
        ])) + "\n",
        encoding="utf-8",
    )

    write_bct_overlap_reference()

    print(
        f"[gen_ccnaauto_hunt_inventory] run {run_id} · MCQ {len(mcq)} · "
        f"labs {len(labs)} · D&D {len(dnd)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
