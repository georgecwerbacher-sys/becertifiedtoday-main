#!/usr/bin/env python3
"""Monthly SY0-701 PBQ workflow: collect → compare → save (.md).

Parallel to secplus_monthly_question_hunt.py for performance-based items.
Compares against public/COMP_TIA_SEC+/SEC+_PBQ/ and SEC+_Sim_Hot_Spot/.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import date
from pathlib import Path

from secplus_competitor_poll import poll_all_pbq_sources
from secplus_monthly_question_hunt import (
    USER_AGENT,
    fetch_url,
    jaccard,
    normalize_text,
    token_set,
    write_csv,
    write_discovery_csv,
)

ROOT = Path(__file__).resolve().parent.parent
VAULT_RUNS = ROOT / "marketing-vault" / "11-question-sourcing" / "pbq" / "runs"
VAULT_CONFIG = ROOT / "marketing-vault" / "11-question-sourcing" / "pbq" / "config" / "secplus-pbq-sources.json"
PBQ_DIR = ROOT / "public" / "COMP_TIA_SEC+" / "SEC+_PBQ"
SIM_DIR = ROOT / "public" / "COMP_TIA_SEC+" / "SEC+_Sim_Hot_Spot"

CSV_FIELDS = [
    "discovered_at",
    "source_id",
    "source_url",
    "source_version",
    "source_question_id",
    "stem",
    "pbq_type",
    "interaction_notes",
    "tokens_or_items",
    "correct_mapping",
    "stated_answer",
    "screenshot_path",
    "topic_notes",
    "date_found",
]
COMPARE_EXTRA = ["bct_match_score", "bct_match_slug"]
NET_NEW_FIELDS = CSV_FIELDS + COMPARE_EXTRA


def load_source_config() -> dict:
    if not VAULT_CONFIG.is_file():
        return {"tier_a_fetch": [], "poll_registry": "marketing-vault/10-competitors/sites"}
    return json.loads(VAULT_CONFIG.read_text(encoding="utf-8"))


def read_import_csv(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(newline="", encoding="utf-8") as f:
        for raw in csv.DictReader(f):
            row = {k: (raw.get(k) or "").strip() for k in CSV_FIELDS if k != "discovered_at"}
            if not row.get("screenshot_path"):
                row["screenshot_path"] = (raw.get("capture_path") or "").strip()
            if row.get("stem"):
                rows.append(row)
    return rows


def find_latest_run() -> str | None:
    runs = sorted(VAULT_RUNS.glob("*-discovered.csv"), reverse=True)
    if not runs:
        return None
    return runs[0].stem.replace("-discovered", "")


def run_id_to_paths(run_id: str) -> dict[str, Path]:
    return {
        "discovered": VAULT_RUNS / f"{run_id}-discovered.csv",
        "meta": VAULT_RUNS / f"{run_id}-discovered.meta.json",
        "compare_md": VAULT_RUNS / f"{run_id}-compare.md",
        "net_new_csv": VAULT_RUNS / f"{run_id}-net-new.csv",
        "net_new_md": VAULT_RUNS / f"{run_id}-net-new.md",
    }


def load_discovered(run_id: str) -> list[dict]:
    path = run_id_to_paths(run_id)["discovered"]
    if not path.is_file():
        raise FileNotFoundError(f"Missing {path.relative_to(ROOT)} — run collect first.")
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _extract_page_text(path: Path) -> tuple[str, str]:
    page = path.read_text(encoding="utf-8", errors="replace")
    title = path.stem.replace("-", " ")
    tm = re.search(r"<title>(.*?)</title>", page, re.I | re.DOTALL)
    if tm:
        title = re.sub(r"\s+", " ", tm.group(1)).strip()
        title = re.sub(r"\s*\|\s*Be Certified Today.*$", "", title, flags=re.I)
        title = re.sub(r"^Security\+\s*(PBQ|Simulation|SY0-701 PBQ Practice)\s*[—\-]\s*", "", title, flags=re.I)
    hm = re.search(r"<h1[^>]*>(.*?)</h1>", page, re.I | re.DOTALL)
    h1 = ""
    if hm:
        h1 = re.sub(r"<[^>]+>", " ", hm.group(1))
        h1 = re.sub(r"\s+", " ", h1).strip()
    lead = ""
    lm = re.search(r'class="lead"[^>]*>(.*?)</p>', page, re.I | re.DOTALL)
    if lm:
        lead = re.sub(r"<[^>]+>", " ", lm.group(1))
        lead = re.sub(r"\s+", " ", lead).strip()
    stem = h1 or title
    if lead and lead not in stem:
        stem = f"{stem}. {lead}"
    return path.stem, stem.strip()


def load_bct_pbq_items() -> list[dict]:
    items: list[dict] = []
    pbq_paths = sorted(PBQ_DIR.glob("*.html"))
    sim_paths: list[Path] = []
    if SIM_DIR.is_dir():
        sim_paths = sorted(SIM_DIR.glob("*.html"))
        for sub in ("pending", "PBQ_Production"):
            extra = SIM_DIR / sub
            if extra.is_dir():
                sim_paths.extend(sorted(extra.rglob("*.html")))
    scan_dirs = [("pbq", pbq_paths), ("sim", sim_paths)])
    for _label, paths in scan_dirs:
        for path in paths:
            slug, stem = _extract_page_text(path)
            if stem:
                items.append(
                    {
                        "slug": slug,
                        "stem": stem,
                        "path": str(path.relative_to(ROOT)),
                    }
                )
    by_slug: dict[str, dict] = {}
    for it in items:
        by_slug[it["slug"]] = it
    return list(by_slug.values())


def pbq_match_text(row: dict) -> str:
    parts = [
        row.get("stem", ""),
        row.get("pbq_type", ""),
        row.get("interaction_notes", ""),
        row.get("tokens_or_items", ""),
        row.get("correct_mapping", ""),
    ]
    return " ".join(p for p in parts if p)


def best_bct_match(stem: str, bct_items: list[dict], threshold: float) -> tuple[float, str | None]:
    n_stem = normalize_text(stem)
    t_stem = token_set(stem)
    best_score = 0.0
    best_slug: str | None = None
    for it in bct_items:
        n_b = normalize_text(it["stem"])
        if n_stem and n_stem == n_b:
            return 1.0, it["slug"]
        if n_stem and len(n_stem) > 40 and (n_stem in n_b or n_b in n_stem):
            return 0.95, it["slug"]
        score = jaccard(t_stem, token_set(it["stem"]))
        if score > best_score:
            best_score = score
            best_slug = it["slug"]
    if best_score >= threshold:
        return best_score, best_slug
    return best_score, None


def compare_discovered(discovered: list[dict], threshold: float) -> tuple[list[dict], list[dict]]:
    bct = load_bct_pbq_items()
    net_new: list[dict] = []
    likely_dup: list[dict] = []
    for row in discovered:
        score, slug = best_bct_match(pbq_match_text(row), bct, threshold)
        out = dict(row)
        out["bct_match_score"] = f"{score:.2f}"
        out["bct_match_slug"] = slug or ""
        (likely_dup if slug else net_new).append(out)
    return net_new, likely_dup


def write_compare_report(
    run_id: str,
    discovered: list[dict],
    net_new: list[dict],
    likely_dup: list[dict],
    threshold: float,
) -> None:
    paths = run_id_to_paths(run_id)
    lines = [
        "---",
        "type: pbq-compare-report",
        f"run: {run_id}",
        "exam: SY0-701",
        "content_type: pbq",
        f"discovered_count: {len(discovered)}",
        f"net_new_count: {len(net_new)}",
        f"likely_duplicate_count: {len(likely_dup)}",
        f"match_threshold: {threshold}",
        f"bct_pbq_dir: public/COMP_TIA_SEC+/SEC+_PBQ/",
        f"bct_sim_dir: public/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/",
        f"net_new_csv: {paths['net_new_csv'].relative_to(ROOT)}",
        f"net_new_md: {paths['net_new_md'].relative_to(ROOT)}",
        "---",
        "",
        f"# SY0-701 PBQ compare — {run_id}",
        "",
        f"| Discovered | Likely in BCT | **Net-new** |",
        f"|-----------:|--------------:|------------:|",
        f"| {len(discovered)} | {len(likely_dup)} | **{len(net_new)}** |",
        "",
    ]
    paths["compare_md"].write_text("\n".join(lines) + "\n", encoding="utf-8")
    write_csv(paths["net_new_csv"], net_new, NET_NEW_FIELDS)


def write_net_new_md(
    net_new: list[dict],
    run_id: str,
    discovered_count: int,
    dup_count: int,
    out_path: Path,
) -> None:
    lines = [
        "---",
        "type: net-new-pbq",
        f"run: {run_id}",
        "exam: SY0-701",
        "content_type: pbq",
        f"discovered_count: {discovered_count}",
        f"net_new_count: {len(net_new)}",
        f"likely_duplicate_count: {dup_count}",
        "status: review",
        "---",
        "",
        f"# SY0-701 PBQ net-new candidates — {run_id}",
        "",
        "Collected from the web, compared to BCT PBQ/sim pages. **Verify on CompTIA Tier A** before building HTML under `public/COMP_TIA_SEC+/SEC+_PBQ/`.",
        "",
        f"- Discovered: **{discovered_count}**",
        f"- Likely already in BCT: **{dup_count}**",
        f"- Net-new below: **{len(net_new)}**",
        "",
        "Summary: [[" + run_id + "-compare|compare report]]",
        "",
    ]
    if not net_new:
        lines.append("_No net-new PBQ candidates at this threshold._")
    else:
        for i, r in enumerate(net_new, 1):
            lines.append(f"## PBQ {i}")
            if r.get("pbq_type"):
                lines.append(f"**Type:** {r['pbq_type']}")
            if r.get("topic_notes"):
                lines.append(f"**Topic:** {r['topic_notes']}")
            lines.append("")
            lines.append(r.get("stem", ""))
            lines.append("")
            if r.get("interaction_notes"):
                lines.append(f"**Interaction:** {r['interaction_notes']}")
                lines.append("")
            if r.get("tokens_or_items"):
                lines.append(f"**Items/tokens:** {r['tokens_or_items']}")
                lines.append("")
            if r.get("correct_mapping"):
                lines.append(f"**Correct mapping:** {r['correct_mapping']}")
                lines.append("")
            if r.get("stated_answer"):
                lines.append(f"**Stated answer (external):** {r['stated_answer']}")
                lines.append("")
            lines.append(
                f"**Source:** `{r.get('source_id', '')}` · v {r.get('source_version', '')} · "
                f"[link]({r.get('source_url', '')})"
            )
            lines.append("")
            lines.append(f"**BCT match score:** {r.get('bct_match_score', '—')}")
            if r.get("bct_match_slug"):
                lines.append(f"**Closest BCT slug:** `{r['bct_match_slug']}`")
            lines.append("")
            lines.append("- [ ] Verified vs CompTIA Tier A / official PBQ objectives")
            lines.append("- [ ] Draft original PBQ page in `public/COMP_TIA_SEC+/SEC+_PBQ/`")
            lines.append("")
            lines.append("---")
            lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def cmd_collect(args: argparse.Namespace) -> tuple[int, str]:
    run_id = args.date or date.today().isoformat()
    all_rows: list[dict] = []

    for src in load_source_config().get("tier_a_fetch", []):
        if not src.get("enabled", True):
            continue
        sid = src.get("id", "unknown")
        print(f"[collect] Tier A PBQ note: {sid} — manual catalog only (no auto parser)")
        if src.get("notes"):
            print(f"  {src['notes']}")

    polled = poll_all_pbq_sources()
    all_rows.extend(polled)

    if args.import_path:
        imp = Path(args.import_path)
        if not imp.is_file():
            print(f"Import not found: {imp}", file=sys.stderr)
            return 1, run_id
        manual = read_import_csv(imp)
        print(f"[collect] import: {len(manual)} rows from {imp.name}")
        all_rows.extend(manual)

    if not all_rows:
        print(
            "[collect] no PBQ candidates — enable pbq_poll in 10-competitors/sites, "
            "add --import, or paste into pbq/imports/.",
            file=sys.stderr,
        )
        return 1, run_id

    paths = run_id_to_paths(run_id)
    write_discovery_csv(paths["discovered"], all_rows, run_id)
    paths["meta"].write_text(
        json.dumps(
            {
                "exam": "SY0-701",
                "content_type": "pbq",
                "run_id": run_id,
                "phase": "collect",
                "count": len(all_rows),
                "deep_scan": True,
                "bct_read": False,
                "discovered_csv": str(paths["discovered"].relative_to(ROOT)),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"[collect] {len(all_rows)} rows -> {paths['discovered'].relative_to(ROOT)}")
    return 0, run_id


def cmd_compare(args: argparse.Namespace) -> tuple[int, str, list[dict], list[dict]]:
    run_id = args.date or find_latest_run()
    if not run_id:
        print("[compare] no run — run collect first.", file=sys.stderr)
        return 1, "", [], []

    try:
        discovered = load_discovered(run_id)
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 1, "", [], []

    threshold = args.threshold
    bct_count = len(load_bct_pbq_items())
    print(f"[compare] BCT PBQ index: {bct_count} pages · run {run_id} · threshold {threshold}")
    net_new, likely_dup = compare_discovered(discovered, threshold)
    write_compare_report(run_id, discovered, net_new, likely_dup, threshold)
    paths = run_id_to_paths(run_id)
    print(
        f"[compare] net-new {len(net_new)} | likely dup {len(likely_dup)} -> "
        f"{paths['net_new_csv'].relative_to(ROOT)}"
    )
    return 0, run_id, net_new, likely_dup


def cmd_save(args: argparse.Namespace) -> int:
    run_id = args.date or find_latest_run()
    if not run_id:
        print("[save] no run — run collect + compare first.", file=sys.stderr)
        return 1

    paths = run_id_to_paths(run_id)
    net_new: list[dict] = []
    likely_dup_count = 0
    discovered_count = 0

    if paths["net_new_csv"].is_file():
        with paths["net_new_csv"].open(newline="", encoding="utf-8") as f:
            net_new = list(csv.DictReader(f))
        try:
            discovered_count = len(load_discovered(run_id))
        except FileNotFoundError:
            discovered_count = len(net_new)
        likely_dup_count = max(0, discovered_count - len(net_new))
    else:
        print("[save] net-new CSV missing — running compare …")
        cmp_args = argparse.Namespace(date=run_id, threshold=args.threshold)
        code, run_id, net_new, likely_dup = cmd_compare(cmp_args)
        if code != 0:
            return code
        discovered_count = len(net_new) + len(likely_dup)
        likely_dup_count = len(likely_dup)

    write_net_new_md(net_new, run_id, discovered_count, likely_dup_count, paths["net_new_md"])
    print(f"[save] {len(net_new)} net-new -> {paths['net_new_md'].relative_to(ROOT)}")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    code, run_id = cmd_collect(args)
    if code != 0:
        return code
    cmp_args = argparse.Namespace(date=run_id, threshold=args.threshold)
    code, run_id, _, _ = cmd_compare(cmp_args)
    if code != 0:
        return code
    save_args = argparse.Namespace(date=run_id, threshold=args.threshold)
    return cmd_save(save_args)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="SY0-701 PBQ monthly: collect → compare → save (.md)",
    )
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument("--date", help="Run id YYYY-MM-DD (default: today)")
    parent.add_argument(
        "--import",
        dest="import_path",
        help="Manual PBQ import CSV (Tier B practice or Tier C research)",
    )
    parent.add_argument(
        "--threshold",
        type=float,
        default=0.68,
        help="BCT duplicate match threshold (PBQ stems are shorter)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    for name, help_text in (
        ("collect", "Step 1 — collect PBQ candidates (no BCT)"),
        ("discover", "Alias for collect"),
        ("compare", "Step 2 — compare to BCT PBQ/sim bank"),
        ("save", "Step 3 — save net-new as markdown"),
        ("pdf", "Alias for save"),
        ("run", "All three steps"),
    ):
        sub.add_parser(name, parents=[parent], help=help_text)

    args = parser.parse_args()
    cmd = args.command
    if cmd in ("collect", "discover"):
        code, _ = cmd_collect(args)
        return code
    if cmd == "compare":
        code, _, _, _ = cmd_compare(args)
        return code
    if cmd in ("save", "pdf"):
        return cmd_save(args)
    if cmd == "run":
        return cmd_run(args)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
