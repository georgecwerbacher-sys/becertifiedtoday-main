"""Shared net-new review markdown writer for Cisco monthly question hunts."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORMAT_CONFIG = ROOT / "marketing-vault" / "11-question-sourcing" / "config" / "net-new-markdown.json"


def load_format_config() -> dict:
    if not FORMAT_CONFIG.is_file():
        return {"format": {}}
    return json.loads(FORMAT_CONFIG.read_text(encoding="utf-8"))


def _md_gap(lines: list[str], count: int) -> None:
    lines.extend([""] * max(0, count))


def _format_revision(revision: str) -> str | None:
    m = re.search(r"v?(\d+)\.(\d+)", (revision or "").strip(), re.I)
    if not m:
        return None
    return f"V{m.group(1)}.{m.group(2)}"


def version_line(
    source_version: str,
    source_id: str,
    *,
    blueprint_by_source: dict[str, str] | None = None,
    fmt: dict | None = None,
) -> str | None:
    fmt = fmt or load_format_config().get("format", {})
    raw = (source_version or "").strip()
    community_text = fmt.get("community_recall_text", "community recall")
    omit = set(fmt.get("omit_version_when_note", ["", "200-301", "2026", "350-401"]))

    if raw.lower() == "community":
        return community_text

    rev = re.search(r"v(\d+)\.(\d+)", raw, re.I)
    if rev:
        return f"V{rev.group(1)}.{rev.group(2)}"

    fallback = (blueprint_by_source or {}).get((source_id or "").strip())
    if fallback:
        return _format_revision(fallback)

    if raw in omit:
        return None

    return _format_revision(raw) or raw


def write_net_new_md(
    net_new: list[dict],
    run_id: str,
    discovered_count: int,
    dup_count: int,
    out_path: Path,
    *,
    exam: str,
    title: str,
    intro: str,
    draft_target: str,
    verify_tier: str = "Cisco Tier A",
    blueprint_by_source: dict[str, str] | None = None,
    format_cfg: dict | None = None,
) -> None:
    cfg = format_cfg or load_format_config()
    fmt = cfg.get("format", {})
    gap_before_version = int(fmt.get("blank_lines_before_version", 2))
    gap_before_source = int(fmt.get("blank_lines_before_source", 2))
    stated_label = fmt.get("stated_answer_label", "**Stated answer (external):**")
    show_score = bool(fmt.get("show_bct_match_score", True))
    raw_checklist = fmt.get(
        "checklist",
        ["Verified vs {verify_tier}", "Draft original stem in `{draft_target}`"],
    )
    checklist = [
        item.format(draft_target=draft_target, verify_tier=verify_tier) for item in raw_checklist
    ]

    lines = [
        "---",
        "type: net-new-questions",
        f"run: {run_id}",
        f"exam: {exam}",
        f"discovered_count: {discovered_count}",
        f"net_new_count: {len(net_new)}",
        f"likely_duplicate_count: {dup_count}",
        "status: review",
        "---",
        "",
        f"# {title} — {run_id}",
        "",
        intro,
        "",
        f"- Discovered: **{discovered_count}**",
        f"- Likely already in BCT: **{dup_count}**",
        f"- Net-new below: **{len(net_new)}**",
        "",
        "Summary: [[" + run_id + "-compare|compare report]]",
        "",
    ]

    if not net_new:
        lines.append("_No net-new questions at this threshold._")
    else:
        for i, row in enumerate(net_new, 1):
            lines.append(f"## Question {i}")
            if row.get("topic_notes"):
                lines.append(f"**Topic:** {row['topic_notes']}")
            lines.append("")
            lines.append(row.get("stem", ""))
            lines.append("")
            for letter in "abcdef":
                choice = row.get(f"choice_{letter}")
                if choice:
                    lines.append(f"- {choice}")
            lines.append("")
            if row.get("stated_answer"):
                lines.append(f"{stated_label} {row['stated_answer']}")

            revision = version_line(
                row.get("source_version", ""),
                row.get("source_id", ""),
                blueprint_by_source=blueprint_by_source,
                fmt=fmt,
            )
            if revision:
                _md_gap(lines, gap_before_version)
                lines.append(revision)

            _md_gap(lines, gap_before_source)
            qid = (row.get("source_question_id") or "").strip()
            qid_bit = f" · Q `{qid}`" if fmt.get("source_include_question_id", True) and qid else ""
            version_bit = ""
            if fmt.get("source_include_version") and row.get("source_version"):
                version_bit = f" · {row['source_version']}"
            lines.append(
                f"**Source:** `{row.get('source_id', '')}`{qid_bit}{version_bit} · "
                f"[link]({row.get('source_url', '')})"
            )
            lines.append("")
            if show_score:
                lines.append(f"**BCT match score:** {row.get('bct_match_score', '—')}")
                lines.append("")
            for item in checklist:
                lines.append(f"- [ ] {item}")
            lines.append("")
            lines.append("---")
            lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")
