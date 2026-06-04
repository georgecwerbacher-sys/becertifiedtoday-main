#!/usr/bin/env python3
"""Save PBQ / drag-and-drop / sim **screenshots** for the sourcing vault.

A screenshot PNG is the research artifact — no OCR or auto-parse. You paraphrase
stem + tokens from the image, verify on CompTIA Tier A, then build original BCT HTML.

Setup (optional automated browser shots):
  pip install playwright
  playwright install chromium

Usage:
  python3 scripts/secplus_pbq_capture.py list
  python3 scripts/secplus_pbq_capture.py screenshot
  python3 scripts/secplus_pbq_capture.py screenshot --source-id crucialexams-pbq
  python3 scripts/secplus_pbq_capture.py register --png path/to/shot.png --source-id manual-id
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


def load_capture_targets() -> list[dict]:
    targets: list[dict] = []
    if CONFIG.is_file():
        data = json.loads(CONFIG.read_text(encoding="utf-8"))
        targets.extend(data.get("targets", []))

    from secplus_competitor_poll import load_pbq_poll_sources

    seen = {t.get("id") for t in targets}
    for src in load_pbq_poll_sources():
        sid = src.get("id", "")
        if sid in seen:
            continue
        targets.append(
            {
                "id": sid,
                "url": src.get("sample_url", ""),
                "tier": src.get("tier", "b"),
                "notes": src.get("topic_notes", ""),
                "wait_ms": 2500,
                "full_page": True,
                "from_pbq_poll": True,
            }
        )
    return [t for t in targets if t.get("url")]


def capture_dir(run_id: str, source_id: str) -> Path:
    return CAPTURES / run_id / source_id


def write_sidecar(path: Path, meta: dict) -> None:
    path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")


def cmd_list(_: argparse.Namespace) -> int:
    targets = load_capture_targets()
    print(f"[capture] {len(targets)} target(s)")
    for t in targets:
        flags = []
        if t.get("login_required"):
            flags.append("login")
        if t.get("preview_path"):
            flags.append(f"preview:{t['preview_path']}")
        extra = f" ({', '.join(flags)})" if flags else ""
        print(f"  {t.get('id')}: {t.get('url')}{extra}")
    return 0


def _playwright_capture(target: dict, out_dir: Path, run_id: str) -> list[dict]:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "[capture] Playwright not installed.\n"
            "  pip install playwright\n"
            "  playwright install chromium",
            file=sys.stderr,
        )
        return []

    url = target["url"]
    source_id = target["id"]
    wait_ms = int(target.get("wait_ms", 2500))
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
            page.goto(url, wait_until="networkidle", timeout=60000)
        except Exception as exc:
            print(f"  skip {source_id}: {exc}", file=sys.stderr)
            browser.close()
            return []

        page.wait_for_timeout(wait_ms)

        preview_path = target.get("preview_path")
        if preview_path:
            try:
                page.click(preview_path, timeout=8000)
                page.wait_for_timeout(wait_ms)
            except Exception as exc:
                print(f"  preview click failed ({source_id}): {exc}", file=sys.stderr)

        shots = [
            ("landing", target.get("full_page", True)),
        ]
        if target.get("viewport_shot", True):
            shots.append(("viewport", False))

        for label, full_page in shots:
            png = out_dir / f"{label}.png"
            page.screenshot(path=str(png), full_page=full_page)
            rel = str(png.relative_to(ROOT))
            meta = {
                "run_id": run_id,
                "source_id": source_id,
                "url": url,
                "capture_label": label,
                "screenshot_path": rel,
                "capture_path": rel,
                "tier": target.get("tier", ""),
                "notes": target.get("notes", ""),
                "login_required": bool(target.get("login_required")),
                "pbq_type_hint": target.get("pbq_type_hint", ""),
                "next_step": "Paraphrase stem/tokens from screenshot; add row to pbq/imports/ — verify on CompTIA Tier A",
            }
            sidecar = out_dir / f"{label}.meta.json"
            write_sidecar(sidecar, meta)
            saved.append(meta)
            print(f"  saved {rel}")

        browser.close()
    return saved


def cmd_capture(args: argparse.Namespace) -> int:
    run_id = args.date or date.today().isoformat()
    targets = load_capture_targets()
    if args.source_id:
        targets = [t for t in targets if t.get("id") == args.source_id]
    if not targets:
        print("[capture] no targets — check pbq_poll registry or config/secplus-pbq-capture-targets.json", file=sys.stderr)
        return 1

    CAPTURES.mkdir(parents=True, exist_ok=True)
    manifest: list[dict] = []
    for target in targets:
        sid = target.get("id", "?")
        print(f"[capture] {sid} …")
        out_dir = capture_dir(run_id, sid)
        manifest.extend(_playwright_capture(target, out_dir, run_id))

    manifest_path = CAPTURES / run_id / "manifest.json"
    if manifest:
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        write_sidecar(
            manifest_path,
            {"run_id": run_id, "count": len(manifest), "captures": manifest},
        )
        print(f"[capture] manifest -> {manifest_path.relative_to(ROOT)}")
        return 0
    return 1


def cmd_register(args: argparse.Namespace) -> int:
    png = Path(args.png)
    if not png.is_file():
        print(f"PNG not found: {png}", file=sys.stderr)
        return 1
    run_id = args.date or date.today().isoformat()
    out_dir = capture_dir(run_id, args.source_id)
    out_dir.mkdir(parents=True, exist_ok=True)
    label = args.label or "manual"
    dest = out_dir / f"{label}.png"
    dest.write_bytes(png.read_bytes())
    rel = str(dest.relative_to(ROOT))
    meta = {
        "run_id": run_id,
        "source_id": args.source_id,
        "url": args.url or "",
        "capture_label": label,
        "screenshot_path": rel,
        "capture_path": rel,
        "manual_drop": True,
        "notes": args.notes or "",
        "next_step": "Paraphrase stem/tokens from screenshot; add row to pbq/imports/",
    }
    write_sidecar(out_dir / f"{label}.meta.json", meta)
    print(f"[capture] registered {rel}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="PBQ screen capture for sourcing workflow")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="List capture targets")
    p_list.set_defaults(func=cmd_list)

    p_cap = sub.add_parser("screenshot", help="Headless browser screenshots (requires Playwright)")
    p_cap.add_argument("--date", help="Run folder YYYY-MM-DD")
    p_cap.add_argument("--source-id", help="Screenshot one source only")
    p_cap.set_defaults(func=cmd_capture)

    p_cap_alias = sub.add_parser("capture", help="Alias for screenshot")
    p_cap_alias.add_argument("--date", help="Run folder YYYY-MM-DD")
    p_cap_alias.add_argument("--source-id", help="Screenshot one source only")
    p_cap_alias.set_defaults(func=cmd_capture)

    p_reg = sub.add_parser("register", help="Register a manual screenshot drop")
    p_reg.add_argument("--png", required=True, help="Path to screenshot PNG")
    p_reg.add_argument("--source-id", required=True, help="Source id for folder naming")
    p_reg.add_argument("--label", default="manual", help="Filename label")
    p_reg.add_argument("--url", default="", help="Optional source URL")
    p_reg.add_argument("--notes", default="", help="Optional notes")
    p_reg.add_argument("--date", help="Run folder YYYY-MM-DD")
    p_reg.set_defaults(func=cmd_register)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
