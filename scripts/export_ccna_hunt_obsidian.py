#!/usr/bin/env python3
"""Export CCNA net-new hunt rows to Obsidian notes under Hunt/ccna/."""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "data" / "ccna-question-sourcing" / "runs"
OUT_BASE = ROOT / "Hunt" / "ccna"
CONFIG = ROOT / "data" / "ccna-question-sourcing" / "config" / "ccna-web-sources.json"

sys.path.insert(0, str(ROOT / "scripts"))
from net_new_markdown import version_line  # noqa: E402

V11_DIR = "v1.1"
V20_DIR = "v2.0"


def slugify(text: str, max_len: int = 48) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return s[:max_len].strip("-") or "item"


def load_blueprint_map() -> dict[str, str]:
    if not CONFIG.is_file():
        return {}
    import json

    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    return (data.get("net_new_markdown") or {}).get("blueprint_by_source") or {}


def question_filename(index: int, stem: str) -> str:
    return f"Q{index:03d}-{slugify(stem)}"


def version_subdir(revision: str | None) -> str:
    """Obsidian folder under each run: v1.1 (default) or v2.0."""
    if revision and revision.strip().upper().startswith("V2"):
        return V20_DIR
    return V11_DIR


def revision_for_row(row: dict, blueprint_by_source: dict[str, str]) -> str | None:
    return version_line(
        row.get("source_version", ""),
        row.get("source_id", ""),
        blueprint_by_source=blueprint_by_source,
    )


def write_question_note(
    path: Path,
    *,
    index: int,
    row: dict,
    run_id: str,
    blueprint_by_source: dict[str, str],
    version_dir: str,
) -> None:
    revision = revision_for_row(row, blueprint_by_source)
    lines = [
        "---",
        "type: hunt-candidate",
        "exam: CCNA-200-301",
        f"run: {run_id}",
        f"version_folder: {version_dir}",
        f"source_id: {row.get('source_id', '')}",
        f"source_question_id: {row.get('source_question_id', '')}",
        f"bct_match_score: {row.get('bct_match_score', '')}",
        f"blueprint: {revision or ''}",
        "status: review",
        "---",
        "",
        f"# Question {index}",
        "",
    ]
    if row.get("topic_notes"):
        lines.extend([f"**Topic:** {row['topic_notes']}", ""])
    lines.append(row.get("stem", ""))
    lines.append("")
    for letter in "abcdef":
        choice = row.get(f"choice_{letter}")
        if choice:
            lines.append(f"- {choice}")
    lines.append("")
    if row.get("stated_answer"):
        lines.append(f"**Stated answer (external):** {row['stated_answer']}")
        lines.append("")
    if revision:
        lines.append(revision)
        lines.append("")
    qid = (row.get("source_question_id") or "").strip()
    qid_bit = f" · Q `{qid}`" if qid else ""
    lines.append(
        f"**Source:** `{row.get('source_id', '')}`{qid_bit} · "
        f"[link]({row.get('source_url', '')})"
    )
    lines.append("")
    lines.append("**BCT match score:** " + str(row.get("bct_match_score", "—")))
    lines.append("")
    lines.extend(
        [
            "- [ ] Verified vs Cisco Tier A",
            "- [ ] Draft original stem in `gen_ccna_chain_pages.py`",
            "",
            f"[[{run_id}|Back to run index]]",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_index(
    path: Path,
    *,
    run_id: str,
    rows: list[dict],
    discovered: int,
    dup_count: int,
    blueprint_by_source: dict[str, str],
) -> None:
    v11_rows: list[tuple[int, dict, str | None]] = []
    v20_rows: list[tuple[int, dict, str | None]] = []
    for i, row in enumerate(rows, 1):
        rev = revision_for_row(row, blueprint_by_source)
        bucket = v20_rows if version_subdir(rev) == V20_DIR else v11_rows
        bucket.append((i, row, rev))

    lines = [
        "---",
        "type: hunt-index",
        "exam: CCNA-200-301",
        f"run: {run_id}",
        f"net_new_count: {len(rows)}",
        f"v11_count: {len(v11_rows)}",
        f"v20_count: {len(v20_rows)}",
        f"likely_duplicate_count: {dup_count}",
        f"discovered_count: {discovered}",
        "status: review",
        "---",
        "",
        f"# CCNA net-new hunt — {run_id}",
        "",
        "Collected from competitors, compared to BCT CCNA bank. "
        "**Verify answers on Cisco Tier A** before drafting original stems.",
        "",
        f"- Discovered: **{discovered}**",
        f"- Likely already in BCT: **{dup_count}**",
        f"- Net-new in this run: **{len(rows)}**",
        f"  - [[{run_id}/{V11_DIR}|Version 1.1]]: **{len(v11_rows)}**",
        f"  - [[{run_id}/{V20_DIR}|Version 2.0]]: **{len(v20_rows)}**",
        "",
        "Data: `data/ccna-question-sourcing/runs/" + run_id + "-net-new.csv`",
        "",
    ]

    def append_section(title: str, version_dir: str, section_rows: list[tuple[int, dict, str | None]]) -> None:
        lines.extend([f"## {title}", ""])
        for i, row, rev in section_rows:
            fname = question_filename(i, row.get("stem", ""))
            rev_bit = f" · {rev}" if rev else ""
            stem_preview = (row.get("stem") or "")[:72]
            if len(row.get("stem") or "") > 72:
                stem_preview += "…"
            lines.append(
                f"- [[{run_id}/{version_dir}/{fname}|Q{i:03d}]]{rev_bit} — {stem_preview} "
                f"(`{row.get('source_id', '')}`)"
            )
        lines.append("")

    append_section("Version 1.1", V11_DIR, v11_rows)
    append_section("Version 2.0", V20_DIR, v20_rows)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_version_readme(path: Path, *, run_id: str, version_dir: str, count: int) -> None:
    label = "Version 1.1" if version_dir == V11_DIR else "Version 2.0"
    path.write_text(
        "\n".join(
            [
                "---",
                "type: hunt-version-folder",
                "exam: CCNA-200-301",
                f"run: {run_id}",
                f"version: {label}",
                f"count: {count}",
                "---",
                "",
                f"# {label} — {run_id}",
                "",
                f"Net-new hunt candidates tagged **{label}** ({count} notes).",
                "",
                f"[[{run_id}|Back to run index]]",
                "",
            ]
        ),
        encoding="utf-8",
    )


def export_run(run_id: str) -> int:
    csv_path = RUNS / f"{run_id}-net-new.csv"
    if not csv_path.is_file():
        print(f"Missing {csv_path}", file=sys.stderr)
        return 1

    with csv_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    meta_path = RUNS / f"{run_id}-discovered.meta.json"
    discovered = len(rows)
    dup_count = 0
    if meta_path.is_file():
        import json

        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        discovered = int(meta.get("count", discovered))
        dup_count = max(0, discovered - len(rows))

    blueprint_by_source = load_blueprint_map()
    run_dir = OUT_BASE / run_id
    v11_dir = run_dir / V11_DIR
    v20_dir = run_dir / V20_DIR
    v11_dir.mkdir(parents=True, exist_ok=True)
    v20_dir.mkdir(parents=True, exist_ok=True)

    v11_count = 0
    v20_count = 0
    for i, row in enumerate(rows, 1):
        rev = revision_for_row(row, blueprint_by_source)
        version_dir = version_subdir(rev)
        if version_dir == V20_DIR:
            v20_count += 1
        else:
            v11_count += 1
        fname = question_filename(i, row.get("stem", ""))
        write_question_note(
            run_dir / version_dir / f"{fname}.md",
            index=i,
            row=row,
            run_id=run_id,
            blueprint_by_source=blueprint_by_source,
            version_dir=version_dir,
        )

    write_version_readme(v11_dir / "README.md", run_id=run_id, version_dir=V11_DIR, count=v11_count)
    write_version_readme(v20_dir / "README.md", run_id=run_id, version_dir=V20_DIR, count=v20_count)

    write_index(
        OUT_BASE / f"{run_id}.md",
        run_id=run_id,
        rows=rows,
        discovered=discovered,
        dup_count=dup_count,
        blueprint_by_source=blueprint_by_source,
    )

    readme = OUT_BASE / "README.md"
    link = f"- [[{run_id}|{run_id}]] — {len(rows)} net-new ({v11_count} v1.1, {v20_count} v2.0)"
    if not readme.is_file():
        readme.write_text(
            "\n".join(
                [
                    "---",
                    "type: hunt-folder",
                    "exam: CCNA-200-301",
                    "---",
                    "",
                    "# CCNA question hunt",
                    "",
                    "Net-new competitor candidates not yet in the BCT bank.",
                    "",
                    "## Runs",
                    "",
                    link,
                    "",
                ]
            ),
            encoding="utf-8",
        )
    else:
        text = readme.read_text(encoding="utf-8")
        if f"[[{run_id}|{run_id}]]" not in text:
            readme.write_text(text.rstrip() + "\n" + link + "\n", encoding="utf-8")
        else:
            text = re.sub(
                rf"- \[\[{re.escape(run_id)}\|{re.escape(run_id)}\]\].*",
                link,
                text,
                count=1,
            )
            readme.write_text(text, encoding="utf-8")

    parent = ROOT / "Hunt" / "README.md"
    if not parent.is_file():
        parent.write_text(
            "\n".join(
                [
                    "---",
                    "type: hunt-root",
                    "---",
                    "",
                    "# Hunt",
                    "",
                    "Competitor question sourcing — net-new candidates for review.",
                    "",
                    "## Exams",
                    "",
                    "- [[ccna/README|CCNA]]",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    print(
        f"Wrote {len(rows)} notes -> {run_dir.relative_to(ROOT)} "
        f"({v11_count} {V11_DIR}, {v20_count} {V20_DIR})"
    )
    print(f"Index -> {(OUT_BASE / f'{run_id}.md').relative_to(ROOT)}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Export CCNA net-new hunt to Obsidian Hunt/ccna/")
    ap.add_argument("--date", default="2026-06-14", help="Hunt run id YYYY-MM-DD")
    args = ap.parse_args()
    return export_run(args.date)


if __name__ == "__main__":
    raise SystemExit(main())
