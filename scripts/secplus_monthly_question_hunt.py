#!/usr/bin/env python3
"""Monthly SY0-701 question workflow: collect → compare → save (.md).

  collect  — web + optional import CSV (Tier B or Tier C research; does NOT read BCT)
  compare  — match collected rows against BCT bank
  save     — write net-new candidates as Obsidian markdown
  run      — all three steps in order
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

from secplus_competitor_poll import load_poll_sources, poll_all_sources

ROOT = Path(__file__).resolve().parent.parent
VAULT_RUNS = ROOT / "marketing-vault" / "11-question-sourcing" / "runs"
VAULT_CONFIG = ROOT / "marketing-vault" / "11-question-sourcing" / "config" / "secplus-web-sources.json"
CHAIN_PY = ROOT / "scripts" / "gen_secplus_chain_pages.py"
QUESTIONS_DIR = ROOT / "public" / "COMP_TIA_SEC" / "SEC+_Questions"

CSV_FIELDS = [
    "discovered_at",
    "source_id",
    "source_url",
    "source_version",
    "source_question_id",
    "stem",
    "choice_a",
    "choice_b",
    "choice_c",
    "choice_d",
    "choice_e",
    "choice_f",
    "stated_answer",
    "topic_notes",
    "date_found",
]
COMPARE_EXTRA = ["bct_match_score", "bct_match_slug"]
NET_NEW_FIELDS = CSV_FIELDS + COMPARE_EXTRA

USER_AGENT = "BCT-SY0-701-Monthly-Hunt/1.0 (+https://becertifiedtoday.com; research)"


def normalize_text(text: str) -> str:
    t = (text or "").lower()
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"[^a-z0-9\s+]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def token_set(text: str) -> set[str]:
    return {w for w in normalize_text(text).split() if len(w) > 2}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def fetch_url(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _split_inline_choices(stem: str) -> tuple[str, list[str]]:
    m = re.search(r"\s+([A-F])\.\s", stem)
    if not m:
        return stem, []
    idx = m.start()
    head = stem[:idx].strip()
    tail = stem[idx:]
    choices = re.findall(r"([A-F])\.\s+(.+?)(?=\s+[A-F]\.\s+|$)", tail)
    return head, [f"{letter}. {text.strip()}" for letter, text in choices]


def parse_comptia_practice_questions(page_html: str) -> list[dict]:
    rows: list[dict] = []
    cut = re.split(
        r"Answer\s+key|##\s*Answer|Shop\s+About\s+Us|self\.__next_f",
        page_html,
        maxsplit=1,
        flags=re.I,
    )[0]
    blocks = re.findall(
        r"margin-bottom:\s*30px.*?padding-bottom:\s*20px;?\">(.*?)</div>\s*</div>",
        cut,
        re.I | re.DOTALL,
    )
    qnum = 0
    for block in blocks:
        text = re.sub(r"<[^>]+>", " ", block)
        text = re.sub(r"\s+", " ", text).strip()
        if len(text) < 40 or text.startswith(":"):
            continue
        qnum += 1
        stem, choices = _split_inline_choices(text)
        stem = re.sub(r"^Question\s+\d+\s*", "", stem, flags=re.I).strip()
        if len(stem) < 30:
            continue
        row = {
            "source_id": "comptia-practice-questions",
            "source_url": "https://www.comptia.org/en-us/certifications/security/practice-questions/",
            "source_version": "V7",
            "source_question_id": str(qnum),
            "stem": stem,
            "topic_notes": "Tier A — verify answer on CompTIA page",
        }
        for idx, ch in enumerate(choices[:6]):
            row[f"choice_{chr(ord('a') + idx)}"] = ch
        rows.append(row)
    seen: set[str] = set()
    unique: list[dict] = []
    for r in rows:
        key = normalize_text(r["stem"])[:120]
        if key in seen:
            continue
        seen.add(key)
        unique.append(r)
    return unique[:20]


def load_source_config() -> dict:
    if not VAULT_CONFIG.is_file():
        return {"tier_a_fetch": [], "poll_registry": "marketing-vault/10-competitors/sites"}
    return json.loads(VAULT_CONFIG.read_text(encoding="utf-8"))


def read_import_csv(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(newline="", encoding="utf-8") as f:
        for raw in csv.DictReader(f):
            row = {k: (raw.get(k) or "").strip() for k in CSV_FIELDS if k != "discovered_at"}
            if row.get("stem"):
                rows.append(row)
    return rows


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            out = {k: "" for k in fieldnames}
            out.update(row)
            w.writerow(out)


def write_discovery_csv(path: Path, rows: list[dict], discovered_at: str) -> None:
    enriched = []
    for row in rows:
        out = dict(row)
        out["discovered_at"] = discovered_at
        if not out.get("date_found"):
            out["date_found"] = discovered_at
        enriched.append(out)
    write_csv(path, enriched, CSV_FIELDS)


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


def load_bct_stems() -> list[dict]:
    items: list[dict] = []
    if CHAIN_PY.is_file():
        text = CHAIN_PY.read_text(encoding="utf-8")
        for m in re.finditer(
            r'"slug":\s*"([^"]+)".*?"stem":\s*\((.*?)\)\s*,\s*"name"',
            text,
            re.DOTALL,
        ):
            parts = re.findall(r'"([^"]*)"', m.group(2))
            stem = " ".join(parts).strip()
            if stem:
                items.append({"slug": m.group(1), "stem": stem})
    if QUESTIONS_DIR.is_dir():
        for path in sorted(QUESTIONS_DIR.glob("*.html")):
            page = path.read_text(encoding="utf-8", errors="replace")
            hm = re.search(r"<h1[^>]*>(.*?)</h1>", page, re.I | re.DOTALL)
            if hm:
                stem = re.sub(r"<[^>]+>", " ", hm.group(1))
                stem = re.sub(r"\s+", " ", stem).strip()
                if stem:
                    items.append({"slug": path.stem, "stem": stem})
    by_slug: dict[str, dict] = {}
    for it in items:
        by_slug[it["slug"]] = it
    return list(by_slug.values())


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
    bct = load_bct_stems()
    net_new: list[dict] = []
    likely_dup: list[dict] = []
    for row in discovered:
        score, slug = best_bct_match(row.get("stem", ""), bct, threshold)
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
        "type: question-compare-report",
        f"run: {run_id}",
        "exam: SY0-701",
        f"discovered_count: {len(discovered)}",
        f"net_new_count: {len(net_new)}",
        f"likely_duplicate_count: {len(likely_dup)}",
        f"match_threshold: {threshold}",
        f"net_new_csv: {paths['net_new_csv'].relative_to(ROOT)}",
        f"net_new_md: {paths['net_new_md'].relative_to(ROOT)}",
        "---",
        "",
        f"# SY0-701 compare — {run_id}",
        "",
        f"| Discovered | Likely in BCT | **Net-new** |",
        f"|-----------:|--------------:|------------:|",
        f"| {len(discovered)} | {len(likely_dup)} | **{len(net_new)}** |",
        "",
    ]
    paths["compare_md"].write_text("\n".join(lines) + "\n", encoding="utf-8")
    write_csv(paths["net_new_csv"], net_new, NET_NEW_FIELDS)


def write_net_new_md(net_new: list[dict], run_id: str, discovered_count: int, dup_count: int, out_path: Path) -> None:
    lines = [
        "---",
        "type: net-new-questions",
        f"run: {run_id}",
        "exam: SY0-701",
        f"discovered_count: {discovered_count}",
        f"net_new_count: {len(net_new)}",
        f"likely_duplicate_count: {dup_count}",
        "status: review",
        "---",
        "",
        f"# SY0-701 net-new candidates — {run_id}",
        "",
        "Collected from the web, compared to BCT. **Verify answers on CompTIA Tier A** before drafting original stems.",
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
        for i, r in enumerate(net_new, 1):
            lines.append(f"## Question {i}")
            if r.get("topic_notes"):
                lines.append(f"**Topic:** {r['topic_notes']}")
            lines.append("")
            lines.append(r.get("stem", ""))
            lines.append("")
            for letter in "abcdef":
                ch = r.get(f"choice_{letter}")
                if ch:
                    lines.append(f"- {ch}")
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
            lines.append("")
            lines.append("- [ ] Verified vs CompTIA Tier A")
            lines.append("- [ ] Draft original stem in `gen_secplus_chain_pages.py`")
            lines.append("")
            lines.append("---")
            lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def cmd_collect(args: argparse.Namespace) -> tuple[int, str]:
    """Phase 1: collect from web + import. Does not read BCT."""
    run_id = args.date or date.today().isoformat()
    all_rows: list[dict] = []

    for src in load_source_config().get("tier_a_fetch", []):
        if not src.get("enabled", True):
            continue
        sid = src.get("id", "unknown")
        print(f"[collect] Tier A: {sid} …")
        try:
            page = fetch_url(src["url"])
        except (urllib.error.URLError, TimeoutError) as exc:
            print(f"  skip: {exc}", file=sys.stderr)
            continue
        parsed = parse_comptia_practice_questions(page)
        for r in parsed:
            r.setdefault("source_version", src.get("version_note", ""))
        print(f"  {len(parsed)} questions")
        all_rows.extend(parsed)

    polled = poll_all_sources()
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
            "[collect] no questions — enable question_poll in 10-competitors/sites, "
            "add --import, or check Tier A fetch.",
            file=sys.stderr,
        )
        return 1, run_id

    paths = run_id_to_paths(run_id)
    write_discovery_csv(paths["discovered"], all_rows, run_id)
    paths["meta"].write_text(
        json.dumps(
            {
                "exam": "SY0-701",
                "run_id": run_id,
                "phase": "collect",
                "count": len(all_rows),
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
    """Phase 2: compare collected rows to BCT."""
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
    print(f"[compare] BCT index loaded · run {run_id} · threshold {threshold}")
    net_new, likely_dup = compare_discovered(discovered, threshold)
    write_compare_report(run_id, discovered, net_new, likely_dup, threshold)
    paths = run_id_to_paths(run_id)
    print(
        f"[compare] net-new {len(net_new)} | likely dup {len(likely_dup)} -> "
        f"{paths['net_new_csv'].relative_to(ROOT)}"
    )
    return 0, run_id, net_new, likely_dup


def cmd_save(args: argparse.Namespace) -> int:
    """Phase 3: Obsidian markdown for net-new candidates."""
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
    """Collect → compare → save markdown."""
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
        description="SY0-701 monthly: collect → compare → save (.md)",
    )
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument("--date", help="Run id YYYY-MM-DD (default: today)")
    parent.add_argument("--import", dest="import_path", help="Manual import CSV (Tier B practice or Tier C research)")
    parent.add_argument(
        "--threshold",
        type=float,
        default=0.72,
        help="BCT duplicate match threshold",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    for name, help_text in (
        ("collect", "Step 1 — collect from web/import (no BCT)"),
        ("discover", "Alias for collect"),
        ("compare", "Step 2 — compare to BCT bank"),
        ("save", "Step 3 — save net-new as Obsidian .md"),
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
