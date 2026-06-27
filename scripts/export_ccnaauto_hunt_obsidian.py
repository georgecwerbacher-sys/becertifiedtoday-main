#!/usr/bin/env python3
"""Export CCNAAUTO 200-901 hunt rows to Obsidian under CCNA-Auto/hunt-results/."""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MCQ_RUNS = ROOT / "data" / "ccnaauto-question-sourcing" / "runs"
LABS_RUNS = ROOT / "data" / "ccnaauto-question-sourcing" / "labs" / "runs"
OUT_BASE = ROOT / "CCNA-Auto" / "hunt-results"
CONFIG = ROOT / "data" / "ccnaauto-question-sourcing" / "config" / "ccnaauto-web-sources.json"
EXAM = "CCNAAUTO-200-901"
VERSION_DIR = "v1.1"
LABS_DIR = "labs"

sys.path.insert(0, str(ROOT / "scripts"))
from ccnaauto_exam_guard import EXAM as GUARD_EXAM, is_ccnaauto_hunt_row  # noqa: E402
from net_new_markdown import version_line  # noqa: E402


def slugify(text: str, max_len: int = 48) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return s[:max_len].strip("-") or "item"


def load_blueprint_map() -> dict[str, str]:
    if not CONFIG.is_file():
        return {}
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    return (data.get("net_new_markdown") or {}).get("blueprint_by_source") or {}


def latest_run_id(runs_dir: Path) -> str | None:
    for path in sorted(runs_dir.glob("*-net-new.csv"), reverse=True):
        run_id = path.stem.replace("-net-new", "")
        if run_id:
            return run_id
    return None


def load_net_new_rows(runs_dir: Path, run_id: str) -> list[dict]:
    path = runs_dir / f"{run_id}-net-new.csv"
    if not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return [row for row in csv.DictReader(f) if is_ccnaauto_hunt_row(row)]


def load_run_meta(runs_dir: Path, run_id: str, row_count: int) -> tuple[int, int]:
    meta_path = runs_dir / f"{run_id}-discovered.meta.json"
    discovered = row_count
    if meta_path.is_file():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        discovered = int(meta.get("count", row_count))
    return discovered, max(0, discovered - row_count)


def blueprint_label(row: dict, blueprint_by_source: dict[str, str]) -> str:
    raw = (row.get("source_version") or "").strip()
    if "200-901" in raw or "901" in raw:
        m = re.search(r"v(\d+\.\d+)", raw, re.I)
        return f"200-901 v{m.group(1)}" if m else "200-901 v1.1"
    rev = version_line(raw, row.get("source_id", ""), blueprint_by_source=blueprint_by_source)
    return rev or "200-901 v1.1"


def item_filename(prefix: str, index: int, stem: str) -> str:
    return f"{prefix}{index:03d}-{slugify(stem)}"


def write_mcq_note(path: Path, *, index: int, row: dict, run_id: str, blueprint_by_source: dict[str, str]) -> str:
    revision = blueprint_label(row, blueprint_by_source)
    source_url = row.get("source_url", "") or ""
    stem = (row.get("stem") or "").strip()
    fname = item_filename("Q", index, stem)
    rel = f"{run_id}/{VERSION_DIR}/{fname}"

    lines = [
        "---",
        "type: hunt-candidate",
        f"exam: {GUARD_EXAM}",
        f"run: {run_id}",
        f"version_folder: {VERSION_DIR}",
        f"source_id: {row.get('source_id', '')}",
        f"source_question_id: {row.get('source_question_id', '')}",
        f"bct_match_score: {row.get('bct_match_score', '')}",
        f"blueprint: {revision or 'v1.1'}",
        "status: review",
        "---",
        "",
        f"# Question {index}",
        "",
    ]
    if row.get("topic_notes"):
        lines.extend([f"**Topic:** {row['topic_notes']}", ""])
    lines.extend([stem, ""])
    for letter in "abcdef":
        choice = row.get(f"choice_{letter}")
        if choice:
            lines.append(f"- {choice}")
    lines.append("")
    if row.get("stated_answer"):
        lines.extend([f"**Stated answer (external):** {row['stated_answer']}", ""])
    if revision:
        lines.extend([revision, ""])
    qid = (row.get("source_question_id") or "").strip()
    qid_bit = f" · Q `{qid}`" if qid else ""
    lines.extend([
        f"**Source:** `{row.get('source_id', '')}`{qid_bit} · [link]({source_url})",
        "",
        f"**BCT match score:** {row.get('bct_match_score', '—')}",
        "",
        "- [ ] Verified vs Cisco Tier A / DevNet docs",
        "- [ ] Draft original stem in `public/CCNAAUTO-Study/` (planned)",
        "",
        f"[[../../{run_id}|Back to run index]] · [[../../README|All runs]]",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")
    return rel


def write_lab_note(path: Path, *, index: int, row: dict, run_id: str) -> str:
    stem = (row.get("stem") or "").strip()
    fname = item_filename("L", index, stem)
    rel = f"{run_id}/{LABS_DIR}/{fname}"
    source_url = row.get("source_url", "") or ""
    interaction = (row.get("interaction_notes") or row.get("pbq_type") or "").strip()
    blob = f"{interaction} {stem}"
    style = "drag-and-drop" if re.search(r"drag", blob, re.I) else "labs-sim"

    lines = [
        "---",
        "type: hunt-labs-candidate",
        f"exam: {GUARD_EXAM}",
        f"run: {run_id}",
        f"content_type: {style}",
        f"source_id: {row.get('source_id', '')}",
        f"source_question_id: {row.get('source_question_id', '')}",
        f"bct_match_score: {row.get('bct_match_score', '')}",
        "status: review",
        "---",
        "",
        f"# Labs / PBQ {index}",
        "",
    ]
    if row.get("topic_notes"):
        lines.extend([f"**Topic:** {row['topic_notes']}", ""])
    if interaction:
        lines.extend([f"**Interaction:** {interaction}", ""])
    lines.extend([stem, ""])
    lines.extend([
        f"**Source:** `{row.get('source_id', '')}` · [link]({source_url})",
        "",
        f"**BCT match score:** {row.get('bct_match_score', '—')}",
        "",
        "- [ ] Verified vs Cisco Tier A",
        "- [ ] Capture exhibit / script if competitor page has one",
        "- [ ] Draft lab or drag-and-drop in CCNAAUTO bank",
        "",
        f"[[../../{run_id}|Back to run index]] · [[../../README|All runs]]",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")
    return rel, style


def write_run_index(
    path: Path,
    *,
    run_id: str,
    mcq_rows: list[dict],
    mcq_links: list[tuple[str, str, str]],
    lab_rows: list[dict],
    lab_links: list[tuple[str, str, str, str]],
    mcq_discovered: int,
    mcq_dup: int,
    labs_discovered: int,
    labs_dup: int,
) -> None:
    dnd_count = sum(1 for _, _, _, style in lab_links if style == "drag-and-drop")
    lines = [
        "---",
        "type: hunt-index",
        f"exam: {GUARD_EXAM}",
        f"run: {run_id}",
        f"mcq_net_new_count: {len(mcq_rows)}",
        f"labs_net_new_count: {len(lab_rows)}",
        f"drag_drop_signals: {dnd_count}",
        f"mcq_discovered_count: {mcq_discovered}",
        f"mcq_likely_duplicate_count: {mcq_dup}",
        f"labs_discovered_count: {labs_discovered}",
        f"labs_likely_duplicate_count: {labs_dup}",
        "status: review",
        "---",
        "",
        f"# CCNAAUTO 200-901 hunt — {run_id}",
        "",
        "Competitor net-new vs interim BCT automation overlap. **Verify on Cisco Tier A** before bank draft.",
        "",
        f"- MCQ net-new: **{len(mcq_rows)}** (discovered {mcq_discovered}, likely dup {mcq_dup})",
        f"- Labs / PBQ net-new: **{len(lab_rows)}** (discovered {labs_discovered}, likely dup {labs_dup})",
        f"- Drag-and-drop signals: **{dnd_count}**",
        "",
        f"Data: `data/ccnaauto-question-sourcing/runs/{run_id}-net-new.csv` · "
        f"`data/ccnaauto-question-sourcing/labs/runs/{run_id}-net-new.csv`",
        "",
        f"## MCQ — [[{run_id}/{VERSION_DIR}|v1.1 folder]]",
        "",
    ]
    for rel, stem, source_id in mcq_links:
        note = rel.split("/")[-1]
        short = stem[:72] + ("…" if len(stem) > 72 else "")
        lines.append(f"- [[{rel}|{note}]] — {short} (`{source_id}`)")
    lines.extend(["", "## Labs / PBQ / D&D signals", ""])
    for rel, stem, source_id, style in lab_links:
        note = rel.split("/")[-1]
        short = stem[:72] + ("…" if len(stem) > 72 else "")
        tag = " · D&D" if style == "drag-and-drop" else ""
        lines.append(f"- [[{rel}|{note}]]{tag} — {short} (`{source_id}`)")
    lines.extend([
        "",
        "Back: [[../README|All runs]] · [[../hunt-inventory|Hunt inventory]]",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def update_readme(run_id: str, mcq_count: int, lab_count: int) -> None:
    readme = OUT_BASE / "README.md"
    link = f"- [[{run_id}|{run_id}]] — {mcq_count} MCQ · {lab_count} labs/PBQ"
    if not readme.is_file():
        readme.write_text(
            "\n".join([
                "---", "type: hunt-folder", f"exam: {GUARD_EXAM}", "---", "",
                "# CCNAAUTO 200-901 hunt results", "",
                "Full question text lives here (main Obsidian vault). Rerun: `npm run ccnaauto:hunt`", "",
                "## Runs", "", link, "",
            ]),
            encoding="utf-8",
        )
        return
    text = readme.read_text(encoding="utf-8")
    if f"[[{run_id}|{run_id}]]" not in text:
        if "## Runs" in text:
            text = text.replace("## Runs\n", f"## Runs\n\n{link}\n", 1)
        else:
            text = text.rstrip() + f"\n\n## Runs\n\n{link}\n"
    else:
        text = re.sub(
            rf"- \[\[{re.escape(run_id)}\|{re.escape(run_id)}\]\].*",
            link,
            text,
            count=1,
        )
    readme.write_text(text, encoding="utf-8")


def export_run(run_id: str | None = None) -> int:
    mcq_run = run_id or latest_run_id(MCQ_RUNS)
    if not mcq_run:
        print("[export_ccnaauto] no MCQ run — run npm run ccnaauto:monthly first", file=sys.stderr)
        return 1

    lab_run = run_id or latest_run_id(LABS_RUNS) or mcq_run
    mcq_rows = load_net_new_rows(MCQ_RUNS, mcq_run)
    lab_rows = load_net_new_rows(LABS_RUNS, lab_run)
    mcq_discovered, mcq_dup = load_run_meta(MCQ_RUNS, mcq_run, len(mcq_rows))
    labs_discovered, labs_dup = load_run_meta(LABS_RUNS, lab_run, len(lab_rows))
    blueprint_by_source = load_blueprint_map()

    run_dir = OUT_BASE / mcq_run
    mcq_dir = run_dir / VERSION_DIR
    labs_dir = run_dir / LABS_DIR
    mcq_dir.mkdir(parents=True, exist_ok=True)
    labs_dir.mkdir(parents=True, exist_ok=True)

    mcq_links: list[tuple[str, str, str]] = []
    for i, row in enumerate(mcq_rows, 1):
        rel = write_mcq_note(
            mcq_dir / f"{item_filename('Q', i, row.get('stem', ''))}.md",
            index=i,
            row=row,
            run_id=mcq_run,
            blueprint_by_source=blueprint_by_source,
        )
        mcq_links.append((rel, row.get("stem", ""), row.get("source_id", "")))

    lab_links: list[tuple[str, str, str, str]] = []
    for i, row in enumerate(lab_rows, 1):
        rel, style = write_lab_note(
            labs_dir / f"{item_filename('L', i, row.get('stem', ''))}.md",
            index=i,
            row=row,
            run_id=mcq_run,
        )
        lab_links.append((rel, row.get("stem", ""), row.get("source_id", ""), style))

    write_run_index(
        OUT_BASE / f"{mcq_run}.md",
        run_id=mcq_run,
        mcq_rows=mcq_rows,
        mcq_links=mcq_links,
        lab_rows=lab_rows,
        lab_links=lab_links,
        mcq_discovered=mcq_discovered,
        mcq_dup=mcq_dup,
        labs_discovered=labs_discovered,
        labs_dup=labs_dup,
    )
    update_readme(mcq_run, len(mcq_rows), len(lab_rows))

    print(
        f"[export_ccnaauto] {mcq_run}: {len(mcq_rows)} MCQ -> CCNA-Auto/hunt-results/{mcq_run}/{VERSION_DIR}/ · "
        f"{len(lab_rows)} labs -> CCNA-Auto/hunt-results/{mcq_run}/{LABS_DIR}/"
    )
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Export CCNAAUTO hunt CSV rows to Obsidian CCNA-Auto/hunt-results/")
    ap.add_argument("--date", help="Run id YYYY-MM-DD (default: latest net-new CSV)")
    args = ap.parse_args()
    return export_run(args.date)


if __name__ == "__main__":
    raise SystemExit(main())
