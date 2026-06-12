#!/usr/bin/env python3
"""Monthly CCNA 200-301 question workflow: collect → compare → save (.md).

  collect  — competitor poll + optional import CSV (does NOT read BCT)
  compare  — match collected rows against CCNA BCT bank
  save     — write net-new candidates as markdown
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

from net_new_markdown import write_net_new_md as write_net_new_review_md
from secplus_competitor_poll import load_poll_sources, poll_all_sources

ROOT = Path(__file__).resolve().parent.parent
SOURCING = ROOT / "data" / "ccna-question-sourcing"
RUNS_DIR = SOURCING / "runs"
CONFIG = SOURCING / "config" / "ccna-web-sources.json"
CHAIN_PY = ROOT / "scripts" / "gen_ccna_chain_pages.py"
QUESTIONS_DIR = ROOT / "public" / "CCNA-Study" / "CCNA_questions"
POLL_PRODUCT = "CCNA-200-301"

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

USER_AGENT = "BCT-CCNA-200-301-Monthly-Hunt/1.0 (+https://becertifiedtoday.com; research)"

EXHIBIT_PREFIX_RE = re.compile(
    r"^(?:refer\s+to\s+)?(?:the\s+)?exhibit\.?\s*",
    re.I,
)


def decode_py_string(value: str) -> str:
    if "\\" in value:
        return value.encode().decode("unicode_escape")
    return value


def strip_html_text(fragment: str) -> str:
    text = re.sub(r"<[^>]+>", " ", fragment or "")
    return re.sub(r"\s+", " ", text).strip()


def strip_exhibit_prefix(text: str) -> str:
    cleaned = strip_html_text(text) if "<" in (text or "") else (text or "").strip()
    return EXHIBIT_PREFIX_RE.sub("", cleaned).strip()


def is_bare_exhibit_label(text: str) -> bool:
    normalized = normalize_text(strip_exhibit_prefix(text))
    return not normalized or normalized in {"refer to the exhibit", "the exhibit", "exhibit"}


def effective_compare_stem(text: str) -> str:
    return strip_exhibit_prefix(text)


def extract_post_exhibit_stem_from_html(page: str) -> str:
    """Return the verify stem: text after exhibit blocks, not the exhibit label."""
    main_m = re.search(r"<main[^>]*>(.*)</main>", page, re.I | re.DOTALL)
    body = main_m.group(1) if main_m else page
    choice_m = re.search(r'<label\s+class="choice"', body, re.I)
    content = body[: choice_m.start()] if choice_m else body

    parts: list[str] = []
    for m in re.finditer(
        r'<p[^>]*class="[^"]*stem-after-exhibit[^"]*"[^>]*>(.*?)</p>',
        content,
        re.I | re.DOTALL,
    ):
        parts.append(strip_html_text(m.group(1)))
    for m in re.finditer(
        r'<ul[^>]*class="[^"]*stem-after-exhibit-list[^"]*"[^>]*>(.*?)</ul>',
        content,
        re.I | re.DOTALL,
    ):
        for li in re.finditer(r"<li[^>]*>(.*?)</li>", m.group(1), re.I | re.DOTALL):
            parts.append(strip_html_text(li.group(1)))
    if parts:
        return " ".join(part for part in parts if part).strip()

    hm = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.I | re.DOTALL)
    if hm:
        return strip_html_text(hm.group(1))
    return ""


def chain_block_to_stem(block: str) -> str:
    parts: list[str] = []
    sae_m = re.search(r'"stem_after_exhibit":\s*"((?:\\.|[^"\\])*)"', block)
    if sae_m:
        parts.append(decode_py_string(sae_m.group(1)).strip())
    bullets_m = re.search(r'"stem_after_exhibit_bullets":\s*\[(.*?)\]', block, re.DOTALL)
    if bullets_m:
        for bullet in re.findall(r'"((?:\\.|[^"\\])*)"', bullets_m.group(1)):
            parts.append(decode_py_string(bullet).strip())
    tail_m = re.search(r'"stem_after_exhibit_tail":\s*"((?:\\.|[^"\\])*)"', block)
    if tail_m:
        parts.append(decode_py_string(tail_m.group(1)).strip())
    if parts:
        return " ".join(part for part in parts if part).strip()

    tuple_m = re.search(r'"stem":\s*\((.*?)\)\s*,', block, re.DOTALL)
    if tuple_m:
        return " ".join(re.findall(r'"([^"]*)"', tuple_m.group(1))).strip()
    stem_m = re.search(r'"stem":\s*"((?:\\.|[^"\\])*)"', block)
    if stem_m:
        return decode_py_string(stem_m.group(1)).strip()
    return ""


def load_chain_stems(text: str) -> dict[str, str]:
    stems: dict[str, str] = {}
    slug_starts = list(re.finditer(r'\n\s+\{\s*\n\s+"slug":\s*"([^"]+)"', text))
    for idx, match in enumerate(slug_starts):
        start = match.start()
        end = slug_starts[idx + 1].start() if idx + 1 < len(slug_starts) else len(text)
        slug = match.group(1)
        stem = chain_block_to_stem(text[start:end])
        if stem:
            stems[slug] = stem
    return stems


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


def load_source_config() -> dict:
    if not CONFIG.is_file():
        return {"tier_a_fetch": [], "poll_product": POLL_PRODUCT}
    return json.loads(CONFIG.read_text(encoding="utf-8"))


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
    runs = sorted(RUNS_DIR.glob("*-discovered.csv"), reverse=True)
    if not runs:
        return None
    return runs[0].stem.replace("-discovered", "")


def run_id_to_paths(run_id: str) -> dict[str, Path]:
    return {
        "discovered": RUNS_DIR / f"{run_id}-discovered.csv",
        "meta": RUNS_DIR / f"{run_id}-discovered.meta.json",
        "compare_md": RUNS_DIR / f"{run_id}-compare.md",
        "net_new_csv": RUNS_DIR / f"{run_id}-net-new.csv",
        "net_new_md": RUNS_DIR / f"{run_id}-net-new.md",
    }


def load_discovered(run_id: str) -> list[dict]:
    path = run_id_to_paths(run_id)["discovered"]
    if not path.is_file():
        raise FileNotFoundError(f"Missing {path.relative_to(ROOT)} — run collect first.")
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_bct_stems() -> list[dict]:
    chain_stems = load_chain_stems(CHAIN_PY.read_text(encoding="utf-8")) if CHAIN_PY.is_file() else {}
    by_slug: dict[str, dict] = {}

    for slug, raw_stem in chain_stems.items():
        stem = effective_compare_stem(raw_stem)
        if stem and not is_bare_exhibit_label(raw_stem):
            by_slug[slug] = {"slug": slug, "stem": stem}

    if QUESTIONS_DIR.is_dir():
        for path in sorted(QUESTIONS_DIR.glob("*.html")):
            slug = path.stem
            page = path.read_text(encoding="utf-8", errors="replace")
            raw_stem = extract_post_exhibit_stem_from_html(page)
            stem = effective_compare_stem(raw_stem)
            if stem and not is_bare_exhibit_label(raw_stem):
                by_slug[slug] = {"slug": slug, "stem": stem}
                continue
            chain_raw = chain_stems.get(slug, "")
            chain_stem = effective_compare_stem(chain_raw)
            if chain_stem and not is_bare_exhibit_label(chain_raw):
                by_slug[slug] = {"slug": slug, "stem": chain_stem}

    return list(by_slug.values())


def best_bct_match(stem: str, bct_items: list[dict], threshold: float) -> tuple[float, str | None]:
    stem = effective_compare_stem(stem)
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
        "exam: CCNA-200-301",
        f"discovered_count: {len(discovered)}",
        f"net_new_count: {len(net_new)}",
        f"likely_duplicate_count: {len(likely_dup)}",
        f"match_threshold: {threshold}",
        f"net_new_csv: {paths['net_new_csv'].relative_to(ROOT)}",
        f"net_new_md: {paths['net_new_md'].relative_to(ROOT)}",
        "---",
        "",
        f"# CCNA 200-301 compare — {run_id}",
        "",
        f"| Discovered | Likely in BCT | **Net-new** |",
        f"|-----------:|--------------:|------------:|",
        f"| {len(discovered)} | {len(likely_dup)} | **{len(net_new)}** |",
        "",
    ]
    paths["compare_md"].write_text("\n".join(lines) + "\n", encoding="utf-8")
    write_csv(paths["net_new_csv"], net_new, NET_NEW_FIELDS)


def net_new_md_settings(cfg: dict | None = None) -> dict:
    product_cfg = cfg or load_source_config()
    md = dict(product_cfg.get("net_new_markdown") or {})
    return {
        "exam": product_cfg.get("exam", POLL_PRODUCT),
        "title": md.get("title", "CCNA 200-301 net-new candidates"),
        "intro": md.get(
            "intro",
            "Collected from competitors, compared to BCT CCNA bank. "
            "**Verify answers on Cisco Tier A** before drafting original stems.",
        ),
        "verify_tier": md.get("verify_tier", "Cisco Tier A"),
        "draft_target": md.get("draft_target", "gen_ccna_chain_pages.py"),
        "blueprint_by_source": md.get("blueprint_by_source") or {},
    }


def write_net_new_md(net_new: list[dict], run_id: str, discovered_count: int, dup_count: int, out_path: Path) -> None:
    settings = net_new_md_settings()
    write_net_new_review_md(
        net_new,
        run_id,
        discovered_count,
        dup_count,
        out_path,
        exam=settings["exam"],
        title=settings["title"],
        intro=settings["intro"],
        draft_target=settings["draft_target"],
        verify_tier=settings["verify_tier"],
        blueprint_by_source=settings["blueprint_by_source"],
    )


def cmd_collect(args: argparse.Namespace) -> tuple[int, str]:
    run_id = args.date or date.today().isoformat()
    all_rows: list[dict] = []

    cfg = load_source_config()
    product = cfg.get("poll_product", POLL_PRODUCT)
    sources = load_poll_sources(product=product)
    if not sources:
        print(
            f"[collect] no enabled polls for product={product} — set question_poll.enabled in sites/*-ccna.md",
            file=sys.stderr,
        )
    polled = poll_all_sources(sources=sources)
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
            "[collect] no questions — enable question_poll in 10-competitors/sites/*-ccna.md or add --import.",
            file=sys.stderr,
        )
        return 1, run_id

    paths = run_id_to_paths(run_id)
    write_discovery_csv(paths["discovered"], all_rows, run_id)
    paths["meta"].write_text(
        json.dumps(
            {
                "exam": "CCNA-200-301",
                "run_id": run_id,
                "phase": "collect",
                "count": len(all_rows),
                "bct_read": False,
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
    bct_count = len(load_bct_stems())
    print(f"[compare] BCT index: {bct_count} stems · run {run_id} · threshold {threshold}")
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
        description="CCNA 200-301 monthly: collect → compare → save (.md)",
    )
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument("--date", help="Run id YYYY-MM-DD (default: today)")
    parent.add_argument("--import", dest="import_path", help="Manual import CSV")
    parent.add_argument(
        "--threshold",
        type=float,
        default=0.72,
        help="BCT duplicate match threshold",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    for name, help_text in (
        ("collect", "Step 1 — collect from competitor polls (no BCT)"),
        ("discover", "Alias for collect"),
        ("compare", "Step 2 — compare to CCNA BCT bank"),
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
