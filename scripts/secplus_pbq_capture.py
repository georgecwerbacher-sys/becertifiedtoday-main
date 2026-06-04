#!/usr/bin/env python3
"""Save PBQ preview **screenshots** for the sourcing vault.

Two capture kinds:
  pbq-preview     — actual drag-and-drop / hot-spot / sim UI (manual register or config preview URL)
  landing-catalog — competitor marketing pages only (NOT importable as PBQ stems)

Setup (optional Playwright for config targets):
  pip install playwright
  playwright install chromium

Usage:
  python3 scripts/secplus_pbq_capture.py list
  python3 scripts/secplus_pbq_capture.py screenshot              # pbq-preview targets only
  python3 scripts/secplus_pbq_capture.py landing-catalog           # optional intel shots
  python3 scripts/secplus_pbq_capture.py register --png … --kind pbq-preview
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAPTURES = ROOT / "marketing-vault" / "11-question-sourcing" / "pbq" / "captures"
CONFIG = ROOT / "marketing-vault" / "11-question-sourcing" / "pbq" / "config" / "secplus-pbq-capture-targets.json"

USER_AGENT = "BCT-SY0-701-PBQ-Capture/1.0 (+https://becertifiedtoday.com; research)"

KIND_PBq_PREVIEW = "pbq-preview"
KIND_LANDING = "landing-catalog"
KIND_BCT_REF = "bct-reference"


def _poll_as_landing(src: dict) -> dict:
    return {
        "id": src.get("id", ""),
        "url": src.get("sample_url", ""),
        "tier": src.get("tier", "b"),
        "notes": src.get("topic_notes", ""),
        "wait_ms": 2500,
        "full_page": True,
        "viewport_shot": True,
        "capture_kind": KIND_LANDING,
        "from_pbq_poll": True,
    }


def load_capture_targets(*, kind: str) -> list[dict]:
    targets: list[dict] = []
    if CONFIG.is_file():
        data = json.loads(CONFIG.read_text(encoding="utf-8"))
        for raw in data.get("targets", []):
            t = dict(raw)
            if t.get("enabled") is False:
                continue
            t.setdefault("capture_kind", KIND_PBq_PREVIEW)
            if t.get("capture_kind") == kind:
                targets.append(t)

    if kind == KIND_LANDING:
        from secplus_competitor_poll import load_pbq_poll_sources

        seen = {t.get("id") for t in targets}
        for src in load_pbq_poll_sources():
            sid = src.get("id", "")
            if sid in seen:
                continue
            targets.append(_poll_as_landing(src))
    return [t for t in targets if t.get("url")]


def capture_dir(run_id: str, source_id: str, *, kind: str) -> Path:
    base = CAPTURES / run_id
    if kind == KIND_LANDING:
        return base / "landing-catalog" / source_id
    if kind == KIND_BCT_REF:
        return base / "bct-reference" / source_id
    return base / source_id


def write_sidecar(path: Path, meta: dict) -> None:
    path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")


def _sidecar_base(target: dict, run_id: str, source_id: str, url: str, label: str, rel: str) -> dict:
    kind = target.get("capture_kind", KIND_PBq_PREVIEW)
    if kind == KIND_LANDING:
        next_step = "Catalog intel only — NOT a PBQ stem. For imports, register a pbq-preview screenshot."
    elif kind == KIND_BCT_REF:
        next_step = "BCT template QA — not competitor research."
    else:
        next_step = "Paraphrase stem/tokens from screenshot; add row to pbq/imports/ — verify on CompTIA Tier A"
    return {
        "run_id": run_id,
        "source_id": source_id,
        "url": url,
        "capture_kind": kind,
        "capture_label": label,
        "screenshot_path": rel,
        "capture_path": rel,
        "tier": target.get("tier", ""),
        "notes": target.get("notes", ""),
        "login_required": bool(target.get("login_required")),
        "pbq_type_hint": target.get("pbq_type_hint", ""),
        "is_pbq_question_ui": kind == KIND_PBq_PREVIEW,
        "next_step": next_step,
    }


def cmd_list(args: argparse.Namespace) -> int:
    preview = load_capture_targets(kind=KIND_PBq_PREVIEW)
    landing = load_capture_targets(kind=KIND_LANDING)
    print(f"[pbq-preview] {len(preview)} target(s) — npm run secplus:pbq-screenshot")
    for t in preview:
        flags = []
        if t.get("login_required"):
            flags.append("login")
        if t.get("preview_url"):
            flags.append(f"preview_url")
        if t.get("preview_selector"):
            flags.append(f"click:{t['preview_selector']}")
        extra = f" ({', '.join(flags)})" if flags else ""
        print(f"  {t.get('id')}: {t.get('url') or t.get('preview_url')}{extra}")
    print(f"[landing-catalog] {len(landing)} target(s) — npm run secplus:pbq-screenshot-landing")
    for t in landing[:5]:
        print(f"  {t.get('id')}: {t.get('url')}")
    if len(landing) > 5:
        print(f"  … +{len(landing) - 5} more")
    return 0


def _playwright_capture(target: dict, out_dir: Path, run_id: str) -> list[dict]:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "[capture] Playwright not installed.\n"
            "  pip install playwright\n"
            "  python3 -m playwright install chromium",
            file=sys.stderr,
        )
        return []

    url = target.get("preview_url") or target["url"]
    source_id = target["id"]
    wait_ms = int(target.get("wait_ms", 2500))
    kind = target.get("capture_kind", KIND_PBq_PREVIEW)
    out_dir.mkdir(parents=True, exist_ok=True)
    saved: list[dict] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=USER_AGENT,
            viewport={"width": 1440, "height": 900},
        )
        page = context.new_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=90000)
        except Exception as exc:
            print(f"  skip {source_id}: {exc}", file=sys.stderr)
            browser.close()
            return []

        page.wait_for_timeout(wait_ms)

        for step in target.get("preview_steps") or []:
            action = step.get("action", "click")
            sel = step.get("selector", "")
            if not sel:
                continue
            try:
                if action == "click":
                    page.click(sel, timeout=12000)
                elif action == "wait":
                    page.wait_for_selector(sel, timeout=12000)
                page.wait_for_timeout(int(step.get("wait_ms", wait_ms)))
            except Exception as exc:
                print(f"  preview step failed ({source_id}): {exc}", file=sys.stderr)

        preview_selector = target.get("preview_selector")
        if preview_selector:
            try:
                page.click(preview_selector, timeout=12000)
                page.wait_for_timeout(wait_ms)
            except Exception as exc:
                print(f"  preview click failed ({source_id}): {exc}", file=sys.stderr)

        if kind == KIND_PBq_PREVIEW:
            labels = [("pbq-preview", False)]
        elif kind == KIND_BCT_REF:
            labels = [("bct-reference", False)]
        else:
            labels = [("landing", target.get("full_page", True))]
            if target.get("viewport_shot", True):
                labels.append(("viewport", False))

        for label, full_page in labels:
            png = out_dir / f"{label}.png"
            page.screenshot(path=str(png), full_page=full_page)
            rel = str(png.relative_to(ROOT))
            meta = _sidecar_base(target, run_id, source_id, url, label, rel)
            write_sidecar(out_dir / f"{label}.meta.json", meta)
            saved.append(meta)
            print(f"  saved [{kind}] {rel}")

        browser.close()
    return saved


def _run_capture(args: argparse.Namespace, kind: str) -> int:
    run_id = args.date or date.today().isoformat()
    targets = load_capture_targets(kind=kind)
    if args.source_id:
        targets = [t for t in targets if t.get("id") == args.source_id]
    if not targets:
        if kind == KIND_PBq_PREVIEW:
            print(
                "[capture] no pbq-preview targets — add preview_url / preview_selector in "
                "config/secplus-pbq-capture-targets.json, or use register for manual PNGs.",
                file=sys.stderr,
            )
        else:
            print("[capture] no landing-catalog targets.", file=sys.stderr)
        return 1

    CAPTURES.mkdir(parents=True, exist_ok=True)
    manifest: list[dict] = []
    for target in targets:
        sid = target.get("id", "?")
        print(f"[capture] {sid} ({kind}) …")
        out_dir = capture_dir(run_id, sid, kind=kind)
        manifest.extend(_playwright_capture(target, out_dir, run_id))

    manifest_path = CAPTURES / run_id / f"manifest-{kind.replace('-', '_')}.json"
    if manifest:
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        write_sidecar(
            manifest_path,
            {"run_id": run_id, "capture_kind": kind, "count": len(manifest), "captures": manifest},
        )
        print(f"[capture] manifest -> {manifest_path.relative_to(ROOT)}")
        return 0
    return 1


def cmd_capture_preview(args: argparse.Namespace) -> int:
    return _run_capture(args, KIND_PBq_PREVIEW)


def cmd_capture_landing(args: argparse.Namespace) -> int:
    return _run_capture(args, KIND_LANDING)


def cmd_register(args: argparse.Namespace) -> int:
    png = Path(args.png)
    if not png.is_file():
        print(f"PNG not found: {png}", file=sys.stderr)
        return 1
    kind = args.kind or KIND_PBq_PREVIEW
    if kind not in (KIND_PBq_PREVIEW, KIND_LANDING, KIND_BCT_REF):
        print(f"Unknown kind: {kind}", file=sys.stderr)
        return 1
    run_id = args.date or date.today().isoformat()
    out_dir = capture_dir(run_id, args.source_id, kind=kind)
    out_dir.mkdir(parents=True, exist_ok=True)
    label = args.label or ("pbq-preview" if kind == KIND_PBq_PREVIEW else "manual")
    dest = out_dir / f"{label}.png"
    dest.write_bytes(png.read_bytes())
    rel = str(dest.relative_to(ROOT))
    target = {
        "capture_kind": kind,
        "tier": args.tier or "",
        "notes": args.notes or "",
        "pbq_type_hint": args.pbq_type or "",
        "login_required": False,
    }
    meta = _sidecar_base(target, run_id, args.source_id, args.url or "", label, rel)
    meta["manual_drop"] = True
    write_sidecar(out_dir / f"{label}.meta.json", meta)
    print(f"[capture] registered [{kind}] {rel}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="PBQ screenshot vault — preview UI vs landing catalog")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="List pbq-preview and landing-catalog targets")
    p_list.set_defaults(func=cmd_list)

    for name, func in (
        ("screenshot", cmd_capture_preview),
        ("capture", cmd_capture_preview),
        ("landing-catalog", cmd_capture_landing),
    ):
        p = sub.add_parser(name, help="PBQ preview shots" if name != "landing-catalog" else "Marketing landing pages only")
        p.add_argument("--date", help="Run folder YYYY-MM-DD")
        p.add_argument("--source-id", help="One source only")
        p.set_defaults(func=func)

    p_reg = sub.add_parser("register", help="Register a manual screenshot (default: pbq-preview)")
    p_reg.add_argument("--png", required=True)
    p_reg.add_argument("--source-id", required=True)
    p_reg.add_argument("--label", default="", help="Filename label (default pbq-preview)")
    p_reg.add_argument("--kind", default=KIND_PBq_PREVIEW, choices=[KIND_PBq_PREVIEW, KIND_LANDING, KIND_BCT_REF])
    p_reg.add_argument("--url", default="")
    p_reg.add_argument("--notes", default="")
    p_reg.add_argument("--pbq-type", default="", dest="pbq_type")
    p_reg.add_argument("--tier", default="b")
    p_reg.add_argument("--date", help="Run folder YYYY-MM-DD")
    p_reg.set_defaults(func=cmd_register)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
