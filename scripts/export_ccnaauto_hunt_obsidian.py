#!/usr/bin/env python3
"""Export CCNAAUTO 200-901 hunt rows to one Obsidian doc per run under CCNA-Auto/hunt-results/."""
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
VAULT_PREFIX = "CCNA-Auto/hunt-results"
EXAM = "CCNAAUTO-200-901"
VERSION_DIR = "v1.1"
LABS_DIR = "labs"

sys.path.insert(0, str(ROOT / "scripts"))
from ccnaauto_competitor_list import load_competitor_site_meta, login_required_for_source  # noqa: E402
from ccnaauto_exam_guard import EXAM as GUARD_EXAM, is_ccnaauto_hunt_row  # noqa: E402
from hunt_note_exhibits import (  # noqa: E402
    exhibit_warning,
    format_exhibit_cli_block,
    format_exhibit_image_block,
    resolve_exhibit,
)
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


def review_checklist(*, login_required: bool, sign_on_notes: str, exhibit_status: str) -> list[str]:
    lines: list[str] = []
    if login_required:
        hint = f" — {sign_on_notes}" if sign_on_notes else ""
        lines.append(f"- [ ] Sign-on completed (required for this source{hint})")
    lines.append("- [ ] Verified vs Cisco Tier A / DevNet docs")
    if exhibit_status == "missing-image":
        lines.append("- [ ] Exhibit image captured above")
    elif exhibit_status == "missing-cli":
        lines.append("- [ ] Exhibit (CLI / code transcript) captured above")
    elif exhibit_status in {"cli", "image"}:
        lines.append("- [ ] Exhibit verified above")
    lines.append("- [ ] Draft original stem in `public/CCNAAUTO-Study/` (planned)")
    return lines


def render_mcq_section(
    *,
    index: int,
    row: dict,
    run_id: str,
    blueprint_by_source: dict[str, str],
    site_meta: dict[str, dict],
    run_dir: Path,
) -> tuple[list[str], str, str, str, list[Path]]:
    revision = blueprint_label(row, blueprint_by_source)
    source_url = row.get("source_url", "") or ""
    stem, exhibit_text, exhibit_status, image_paths = resolve_exhibit(row, run_dir)
    login_required, sign_on_notes = login_required_for_source(
        str(row.get("source_id", "")), site_meta
    )
    lines = [
        f"### Question {index}",
        "",
    ]
    if row.get("topic_notes"):
        lines.extend([f"**Topic:** {row['topic_notes']}", ""])
    if login_required:
        note = sign_on_notes or "Sign-on or paid access required on competitor site."
        lines.extend([f"> [!note] Sign-on required — {note}", ""])

    lines.extend(exhibit_warning(exhibit_status, source_url, f"{VAULT_PREFIX}/{run_id}"))

    for image_path in image_paths:
        image_rel = f"{run_id}/images/{image_path.name}"
        lines.extend(format_exhibit_image_block(
            image_path,
            image_rel=image_rel,
            vault_path=f"{VAULT_PREFIX}/{image_rel}",
        ))

    if exhibit_text:
        lines.extend(format_exhibit_cli_block(exhibit_text))

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
    ])
    lines.extend(review_checklist(
        login_required=login_required,
        sign_on_notes=sign_on_notes,
        exhibit_status=exhibit_status,
    ))
    lines.extend(["", "---", ""])

    ex_flag = "login" if login_required else exhibit_status
    return lines, stem or row.get("stem", ""), row.get("source_id", ""), ex_flag, image_paths


def render_lab_section(
    *,
    index: int,
    row: dict,
    run_id: str,
    site_meta: dict[str, dict],
) -> tuple[list[str], str, str]:
    stem = (row.get("stem") or "").strip()
    source_url = row.get("source_url", "") or ""
    interaction = (row.get("interaction_notes") or row.get("pbq_type") or "").strip()
    blob = f"{interaction} {stem}"
    style = "drag-and-drop" if re.search(r"drag", blob, re.I) else "labs-sim"
    login_required, sign_on_notes = login_required_for_source(
        str(row.get("source_id", "")), site_meta
    )
    lines = [
        f"### Labs / PBQ {index}",
        "",
    ]
    if login_required:
        note = sign_on_notes or "Sign-on or paid access required on competitor site."
        lines.extend([f"> [!note] Sign-on required — {note}", ""])
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
    ])
    if login_required:
        lines.append(
            f"- [ ] Sign-on completed (required for this source"
            f"{(' — ' + sign_on_notes) if sign_on_notes else ''})"
        )
    lines.extend([
        "- [ ] Verified vs Cisco Tier A",
        "- [ ] Exhibit / script captured above (screenshot or transcript)",
        "- [ ] Draft lab or drag-and-drop in CCNAAUTO bank",
        "",
        "---",
        "",
    ])
    return lines, stem, style


def write_consolidated_run_doc(
    path: Path,
    *,
    run_id: str,
    mcq_rows: list[dict],
    mcq_meta: list[tuple[str, str, str]],
    lab_rows: list[dict],
    lab_meta: list[tuple[str, str]],
    mcq_discovered: int,
    mcq_dup: int,
    labs_discovered: int,
    labs_dup: int,
    mcq_sections: list[list[str]],
    lab_sections: list[list[str]],
) -> None:
    dnd_count = sum(1 for _, style in lab_meta if style == "drag-and-drop")
    login_count = sum(1 for _, _, ex in mcq_meta if ex == "login")
    exhibit_counts: dict[str, int] = {}
    for _, _, ex in mcq_meta:
        exhibit_counts[ex] = exhibit_counts.get(ex, 0) + 1

    lines = [
        "---",
        "type: hunt-results",
        f"exam: {GUARD_EXAM}",
        f"run: {run_id}",
        f"mcq_net_new_count: {len(mcq_rows)}",
        f"labs_net_new_count: {len(lab_rows)}",
        f"drag_drop_signals: {dnd_count}",
        f"login_required_count: {login_count}",
        f"mcq_discovered_count: {mcq_discovered}",
        f"mcq_likely_duplicate_count: {mcq_dup}",
        f"labs_discovered_count: {labs_discovered}",
        f"labs_likely_duplicate_count: {labs_dup}",
        "status: review",
        "---",
        "",
        f"# CCNAAUTO 200-901 hunt — {run_id}",
        "",
        "All net-new MCQ and labs/PBQ signals in **this file**. **Verify on Cisco Tier A** before bank draft.",
        "Sources: [[../competitor-list|competitor-list]]",
        "",
        f"- MCQ net-new: **{len(mcq_rows)}** (discovered {mcq_discovered}, likely dup {mcq_dup})",
        f"- Labs / PBQ net-new: **{len(lab_rows)}** (discovered {labs_discovered}, likely dup {labs_dup})",
        f"- Drag-and-drop signals: **{dnd_count}**",
        f"- Sign-on required: **{login_count}** MCQ sources",
        "",
        "**Exhibits:** " + ", ".join(f"{k} **{v}**" for k, v in sorted(exhibit_counts.items())),
        "",
        f"Data: `data/ccnaauto-question-sourcing/runs/{run_id}-net-new.csv` · "
        f"`data/ccnaauto-question-sourcing/labs/runs/{run_id}-net-new.csv`",
        "",
        "## MCQ table of contents",
        "",
    ]
    for i, (stem, source_id, ex_status) in enumerate(mcq_meta, 1):
        short = stem[:72] + ("…" if len(stem) > 72 else "")
        ex_bit = f" · exhibit:{ex_status}" if ex_status not in ("none", "") else ""
        lines.append(f"- [[#Question {i}|Q{i:03d}]]{ex_bit} — {short} (`{source_id}`)")
    lines.extend(["", "## MCQ questions", ""])
    for section in mcq_sections:
        lines.extend(section)

    lines.extend(["", "## Labs / PBQ table of contents", ""])
    for i, (stem, style) in enumerate(lab_meta, 1):
        short = stem[:72] + ("…" if len(stem) > 72 else "")
        tag = " · D&D" if style == "drag-and-drop" else ""
        lines.append(f"- [[#Labs / PBQ {i}|L{i:03d}]]{tag} — {short}")
    lines.extend(["", "## Labs / PBQ / D&D signals", ""])
    for section in lab_sections:
        lines.extend(section)

    lines.extend([
        "",
        "Back: [[README|All runs]] · [[../competitor-list|Competitor list]]",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def cleanup_legacy_per_question_files(run_dir: Path) -> None:
    for sub in (VERSION_DIR, LABS_DIR):
        folder = run_dir / sub
        if not folder.is_dir():
            continue
        for md in folder.glob("*.md"):
            md.unlink(missing_ok=True)
        if folder.is_dir() and not any(folder.iterdir()):
            folder.rmdir()


def update_readme(run_id: str, mcq_count: int, lab_count: int) -> None:
    readme = OUT_BASE / "README.md"
    link = f"- [[{run_id}|{run_id}]] — {mcq_count} MCQ · {lab_count} labs/PBQ (single doc)"
    if not readme.is_file():
        readme.write_text(
            "\n".join([
                "---", "type: hunt-folder", f"exam: {GUARD_EXAM}", "---", "",
                "# CCNAAUTO 200-901 hunt results", "",
                "One **results doc per run** — all questions, choices, and exhibits in `YYYY-MM-DD.md`.",
                "Sources: [[../competitor-list|competitor-list]]. Rerun: `npm run ccnaauto:hunt`", "",
                "## Runs", "", link, "",
            ]),
            encoding="utf-8",
        )
        return
    text = readme.read_text(encoding="utf-8")
    text = re.sub(
        r"One note per question[^\n]*\n",
        "One **results doc per run** — all questions, choices, and exhibits in `YYYY-MM-DD.md`.\n",
        text,
        count=1,
    )
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


def cleanup_stale_exhibit_images(run_dir: Path, kept: set[Path]) -> None:
    images_dir = run_dir / "images"
    if not images_dir.is_dir():
        return
    for path in images_dir.iterdir():
        if path.is_file() and path.resolve() not in kept:
            path.unlink(missing_ok=True)


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
    site_meta = load_competitor_site_meta()

    run_dir = OUT_BASE / mcq_run
    run_dir.mkdir(parents=True, exist_ok=True)

    mcq_sections: list[list[str]] = []
    mcq_meta: list[tuple[str, str, str]] = []
    kept_images: set[Path] = set()
    for i, row in enumerate(mcq_rows, 1):
        section, stem, source_id, ex_flag, image_paths = render_mcq_section(
            index=i,
            row=row,
            run_id=mcq_run,
            blueprint_by_source=blueprint_by_source,
            site_meta=site_meta,
            run_dir=run_dir,
        )
        mcq_sections.append(section)
        mcq_meta.append((stem, source_id, ex_flag))
        kept_images.update(p.resolve() for p in image_paths)

    lab_sections: list[list[str]] = []
    lab_meta: list[tuple[str, str]] = []
    for i, row in enumerate(lab_rows, 1):
        section, stem, style = render_lab_section(
            index=i,
            row=row,
            run_id=mcq_run,
            site_meta=site_meta,
        )
        lab_sections.append(section)
        lab_meta.append((stem, style))

    cleanup_stale_exhibit_images(run_dir, kept_images)
    out_path = OUT_BASE / f"{mcq_run}.md"
    write_consolidated_run_doc(
        out_path,
        run_id=mcq_run,
        mcq_rows=mcq_rows,
        mcq_meta=mcq_meta,
        lab_rows=lab_rows,
        lab_meta=lab_meta,
        mcq_discovered=mcq_discovered,
        mcq_dup=mcq_dup,
        labs_discovered=labs_discovered,
        labs_dup=labs_dup,
        mcq_sections=mcq_sections,
        lab_sections=lab_sections,
    )
    cleanup_legacy_per_question_files(run_dir)
    update_readme(mcq_run, len(mcq_rows), len(lab_rows))

    print(
        f"[export_ccnaauto] {mcq_run}: {len(mcq_rows)} MCQ + {len(lab_rows)} labs -> "
        f"{VAULT_PREFIX}/{mcq_run}.md"
    )
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Export CCNAAUTO hunt CSV rows to one Obsidian doc per run")
    ap.add_argument("--date", help="Run id YYYY-MM-DD (default: latest net-new CSV)")
    args = ap.parse_args()
    return export_run(args.date)


if __name__ == "__main__":
    raise SystemExit(main())
