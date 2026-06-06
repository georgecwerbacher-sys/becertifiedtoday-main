#!/usr/bin/env python3
"""Monthly CCNA 200-301 labs / sim / PBQ workflow: collect → compare → save (.md).

Scans competitor pages for drag-and-drop, CLI lab, and simulation signals.
Compares against public/CCNA-Study/CCNA_D_D/, CCNA_labs/, and CCNA_Sim_EXAM/.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

from secplus_competitor_poll import load_pbq_poll_sources, poll_all_pbq_sources
from secplus_monthly_pbq_hunt import (
    CSV_FIELDS,
    COMPARE_EXTRA,
    NET_NEW_FIELDS,
    best_bct_match,
    compare_discovered,
    pbq_match_text,
    read_import_csv,
    write_csv,
    write_discovery_csv,
)
ROOT = Path(__file__).resolve().parent.parent
VAULT_RUNS = ROOT / "marketing-vault" / "11-question-sourcing" / "ccna" / "labs-sim" / "runs"
VAULT_CONFIG = (
    ROOT / "marketing-vault" / "11-question-sourcing" / "ccna" / "config" / "ccna-labs-sim-sources.json"
)
DND_DIR = ROOT / "public" / "CCNA-Study" / "CCNA_D_D"
LABS_DIR = ROOT / "public" / "CCNA-Study" / "CCNA_labs"
SIM_DIR = ROOT / "public" / "CCNA_Sim_EXAM"
POLL_PRODUCT = "CCNA-200-301"


def load_source_config() -> dict:
    if not VAULT_CONFIG.is_file():
        return {"poll_product": POLL_PRODUCT}
    return json.loads(VAULT_CONFIG.read_text(encoding="utf-8"))


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
    import csv

    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _extract_page_text(path: Path) -> tuple[str, str]:
    page = path.read_text(encoding="utf-8", errors="replace")
    title = path.stem.replace("-", " ")
    tm = re.search(r"<title>(.*?)</title>", page, re.I | re.DOTALL)
    if tm:
        title = re.sub(r"\s+", " ", tm.group(1)).strip()
        title = re.sub(r"\s*\|\s*Be Certified Today.*$", "", title, flags=re.I)
    hm = re.search(r"<h1[^>]*>(.*?)</h1>", page, re.I | re.DOTALL)
    h1 = ""
    if hm:
        h1 = re.sub(r"<[^>]+>", " ", hm.group(1))
        h1 = re.sub(r"\s+", " ", h1).strip()
    stem = h1 or title
    return path.stem, stem.strip()


def load_bct_labs_sim_items() -> list[dict]:
    items: list[dict] = []
    scans: list[tuple[str, list[Path]]] = []
    if DND_DIR.is_dir():
        scans.append(("dnd", sorted(DND_DIR.rglob("*.html"))))
    if LABS_DIR.is_dir():
        scans.append(("lab", sorted(LABS_DIR.rglob("*.html"))))
    if SIM_DIR.is_dir():
        scans.append(("sim", sorted(SIM_DIR.glob("*.html"))))
    for _label, paths in scans:
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


def compare_discovered_ccna(discovered: list[dict], threshold: float) -> tuple[list[dict], list[dict]]:
    bct = load_bct_labs_sim_items()
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
    bct_count = len(load_bct_labs_sim_items())
    lines = [
        "---",
        "type: labs-sim-compare-report",
        f"run: {run_id}",
        "exam: CCNA-200-301",
        "content_type: labs-sim",
        f"discovered_count: {len(discovered)}",
        f"net_new_count: {len(net_new)}",
        f"likely_duplicate_count: {len(likely_dup)}",
        f"match_threshold: {threshold}",
        f"bct_index_count: {bct_count}",
        f"net_new_csv: {paths['net_new_csv'].relative_to(ROOT)}",
        f"net_new_md: {paths['net_new_md'].relative_to(ROOT)}",
        "---",
        "",
        f"# CCNA 200-301 labs / sim compare — {run_id}",
        "",
        f"| Discovered | Likely in BCT | **Net-new** | BCT index |",
        f"|-----------:|--------------:|------------:|----------:|",
        f"| {len(discovered)} | {len(likely_dup)} | **{len(net_new)}** | {bct_count} |",
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
        "type: net-new-labs-sim",
        f"run: {run_id}",
        "exam: CCNA-200-301",
        "content_type: labs-sim",
        f"discovered_count: {discovered_count}",
        f"net_new_count: {len(net_new)}",
        f"likely_duplicate_count: {dup_count}",
        "status: review",
        "---",
        "",
        f"# CCNA 200-301 labs / sim net-new — {run_id}",
        "",
        "Compared to BCT `CCNA_D_D/`, `CCNA_labs/`, `CCNA_Sim_EXAM/`. **Verify on Cisco Tier A** before new HTML.",
        "",
        f"- Discovered: **{discovered_count}**",
        f"- Likely already in BCT: **{dup_count}**",
        f"- Net-new below: **{len(net_new)}**",
        "",
        "Summary: [[" + run_id + "-compare|compare report]]",
        "",
    ]
    if not net_new:
        lines.append("_No net-new labs/sim candidates at this threshold._")
    else:
        for i, r in enumerate(net_new, 1):
            lines.append(f"## Item {i}")
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
            lines.append(
                f"**Source:** `{r.get('source_id', '')}` · v {r.get('source_version', '')} · "
                f"[link]({r.get('source_url', '')})"
            )
            lines.append("")
            lines.append(f"**BCT match score:** {r.get('bct_match_score', '—')}")
            if r.get("bct_match_slug"):
                lines.append(f"**Closest BCT slug:** `{r['bct_match_slug']}`")
            lines.append("")
            lines.append("- [ ] Verified vs Cisco Tier A / IOS behavior")
            lines.append("- [ ] Draft D&D in `CCNA_D_D/` or CLI lab in `CCNA_labs/`")
            lines.append("")
            lines.append("---")
            lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def cmd_collect(args: argparse.Namespace) -> tuple[int, str]:
    run_id = args.date or date.today().isoformat()
    all_rows: list[dict] = []

    cfg = load_source_config()
    product = cfg.get("poll_product", POLL_PRODUCT)
    sources = load_pbq_poll_sources(product=product)
    if not sources:
        print(
            f"[collect] no enabled pbq_poll for product={product} — enable in sites/*-ccna.md",
            file=sys.stderr,
        )
    polled = poll_all_pbq_sources(sources=sources)
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
            "[collect] no labs/sim candidates — enable pbq_poll in sites/*-ccna.md or add --import.",
            file=sys.stderr,
        )
        return 1, run_id

    paths = run_id_to_paths(run_id)
    write_discovery_csv(paths["discovered"], all_rows, run_id)
    paths["meta"].write_text(
        json.dumps(
            {
                "exam": "CCNA-200-301",
                "content_type": "labs-sim",
                "run_id": run_id,
                "phase": "collect",
                "count": len(all_rows),
                "poll_product": product,
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
    bct_count = len(load_bct_labs_sim_items())
    print(f"[compare] BCT labs/sim index: {bct_count} pages · run {run_id} · threshold {threshold}")
    net_new, likely_dup = compare_discovered_ccna(discovered, threshold)
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
    import csv

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
        description="CCNA 200-301 labs/sim monthly: collect → compare → save (.md)",
    )
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument("--date", help="Run id YYYY-MM-DD (default: today)")
    parent.add_argument("--import", dest="import_path", help="Manual import CSV")
    parent.add_argument(
        "--threshold",
        type=float,
        default=0.68,
        help="BCT duplicate match threshold",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    for name, help_text in (
        ("collect", "Step 1 — collect labs/sim signals (no BCT)"),
        ("discover", "Alias for collect"),
        ("compare", "Step 2 — compare to BCT D&D / labs / sim"),
        ("save", "Step 3 — save net-new as markdown"),
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
    if cmd == "save":
        return cmd_save(args)
    if cmd == "run":
        return cmd_run(args)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
