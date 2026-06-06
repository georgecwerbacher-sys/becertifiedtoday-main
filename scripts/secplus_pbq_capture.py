#!/usr/bin/env python3
"""Capture Security+ PBQ / drag-and-drop / sim screenshots into marketing-vault.

For each registered site: try pbq-preview screenshot → landing fallback → link-only entry.
Writes PNG + meta.json per source and generates captures/YYYY-MM-DD/INDEX.md.

Setup:
  pip install playwright
  python3 -m playwright install chromium

Usage:
  npm run serve   # required for localhost BCT pages
  npm run secplus:pbq-capture

  python3 scripts/secplus_pbq_capture.py list
  python3 scripts/secplus_pbq_capture.py register --png … --source-id … --url …
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

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

STATUS_PBq = "captured-pbq"
STATUS_LANDING = "captured-landing"
STATUS_LINK = "link-only"
STATUS_FAILED = "failed"

REDDIT_LINKS = {
    "reddit-comptia-pbq": "https://www.reddit.com/r/CompTIA/search/?q=SY0-701+PBQ&restrict_sr=1",
    "reddit-securityplus-pbq": "https://www.reddit.com/r/SecurityPlus/search/?q=SY0-701+PBQ&restrict_sr=1",
}


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _target_defaults(raw: dict) -> dict:
    t = dict(raw)
    t.setdefault("url", "")
    t.setdefault("link_url", t.get("url", ""))
    t.setdefault("preview_url", "")
    t.setdefault("wait_ms", 3500)
    t.setdefault("full_page", False)
    t.setdefault("viewport_shot", True)
    t.setdefault("try_preview", t.get("capture_mode") != "link-only")
    t.setdefault("try_landing", t.get("capture_mode") != "link-only")
    t.setdefault("pbq_type_hint", "pbq")
    t.setdefault("tier", "b")
    t.setdefault("notes", "")
    t.setdefault("login_required", False)
    if t.get("id") in REDDIT_LINKS:
        t["capture_mode"] = "link-only"
        t["link_url"] = REDDIT_LINKS[t["id"]]
        t["try_preview"] = False
        t["try_landing"] = False
        t["notes"] = (t.get("notes") or "") + " Reddit blocks bots — use search link; paste recall manually."
    if t.get("from_pbq_poll") and not (t.get("preview_url") or t.get("preview_selector")):
        t.setdefault("try_preview", False)
        t.setdefault("try_landing", True)
    return t


def _is_pbq_ui_target(target: dict) -> bool:
    if target.get("force_pbq_preview"):
        return True
    if target.get("id", "").startswith("bct-"):
        return True
    if target.get("preview_url") or target.get("preview_selector") or target.get("preview_steps"):
        return True
    return False


def load_all_targets() -> list[dict]:
    targets: dict[str, dict] = {}
    if CONFIG.is_file():
        data = json.loads(CONFIG.read_text(encoding="utf-8"))
        for raw in data.get("targets", []):
            if raw.get("enabled") is False:
                continue
            t = _target_defaults(raw)
            if t.get("id") and t.get("url") or t.get("link_url"):
                targets[t["id"]] = t

    from secplus_competitor_poll import load_pbq_poll_sources

    for src in load_pbq_poll_sources():
        sid = src.get("id", "")
        if not sid or sid in targets:
            continue
        url = src.get("sample_url", "")
        targets[sid] = _target_defaults(
            {
                "id": sid,
                "url": url,
                "link_url": url,
                "tier": src.get("tier", "b"),
                "notes": src.get("topic_notes", ""),
                "from_pbq_poll": True,
            }
        )
    return list(targets.values())


def source_dir(run_id: str, source_id: str) -> Path:
    return CAPTURES / run_id / source_id


def _entry_base(target: dict, run_id: str) -> dict:
    return {
        "run_id": run_id,
        "source_id": target["id"],
        "url": target.get("url") or target.get("link_url", ""),
        "link_url": target.get("link_url") or target.get("url", ""),
        "preview_url": target.get("preview_url") or "",
        "tier": target.get("tier", ""),
        "pbq_type_hint": target.get("pbq_type_hint", "pbq"),
        "notes": target.get("notes", ""),
        "login_required": bool(target.get("login_required")),
    }


def _playwright_shot(target: dict, out_dir: Path, label: str, url: str, full_page: bool) -> str | None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "[capture] Playwright not installed — pip install playwright && "
            "python3 -m playwright install chromium",
            file=sys.stderr,
        )
        return None

    wait_ms = int(target.get("wait_ms", 3500))
    out_dir.mkdir(parents=True, exist_ok=True)
    png = out_dir / f"{label}.png"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_context(
            user_agent=USER_AGENT,
            viewport={"width": 1440, "height": 900},
        ).new_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=90000)
        except Exception as exc:
            print(f"    goto failed: {exc}", file=sys.stderr)
            browser.close()
            return None

        page.wait_for_timeout(wait_ms)

        for step in target.get("preview_steps") or []:
            sel = step.get("selector", "")
            if not sel:
                continue
            try:
                if step.get("action") == "wait":
                    page.wait_for_selector(sel, timeout=12000)
                else:
                    page.click(sel, timeout=12000)
                page.wait_for_timeout(int(step.get("wait_ms", wait_ms)))
            except Exception as exc:
                print(f"    preview step failed: {exc}", file=sys.stderr)

        sel = target.get("preview_selector")
        if sel and label == "pbq-preview":
            try:
                page.click(sel, timeout=12000)
                page.wait_for_timeout(wait_ms)
            except Exception as exc:
                print(f"    preview click failed: {exc}", file=sys.stderr)

        try:
            page.screenshot(path=str(png), full_page=full_page)
        except Exception as exc:
            print(f"    screenshot failed: {exc}", file=sys.stderr)
            browser.close()
            return None
        browser.close()

    if png.is_file() and png.stat().st_size > 8000:
        return str(png.relative_to(ROOT))
    if png.is_file():
        png.unlink(missing_ok=True)
    return None


def _image_markdown(sid: str, filename: str) -> str:
    return f"![{sid} {filename}]({sid}/{filename})"


def capture_one_target(target: dict, run_id: str) -> dict:
    sid = target["id"]
    out_dir = source_dir(run_id, sid)
    entry = _entry_base(target, run_id)
    entry["screenshot_path"] = ""
    entry["landing_screenshot_path"] = ""
    entry["capture_status"] = STATUS_LINK
    entry["image_markdown"] = ""

    if target.get("capture_mode") == "link-only" or (
        not target.get("try_preview") and not target.get("try_landing")
    ):
        out_dir.mkdir(parents=True, exist_ok=True)
        entry["capture_status"] = STATUS_LINK
        entry["status_note"] = "Link-only — open in browser for PBQ recall or preview"
        write_json(out_dir / "meta.json", entry)
        print(f"  [{STATUS_LINK}] {sid} -> {entry['link_url']}")
        return entry

    # Try PBQ preview only for BCT pages or targets with explicit preview URL/selector
    if _is_pbq_ui_target(target) and target.get("try_preview"):
        preview_url = target.get("preview_url") or target.get("url")
        rel = _playwright_shot(target, out_dir, "pbq-preview", preview_url, full_page=False)
        if rel:
            entry["screenshot_path"] = rel
            entry["capture_status"] = STATUS_PBq
            entry["image_markdown"] = _image_markdown(sid, "pbq-preview.png")
            entry["status_note"] = "PBQ / sim UI screenshot — paraphrase for BCT; verify Tier A"
            write_json(out_dir / "meta.json", entry)
            print(f"  [{STATUS_PBq}] {sid} -> {rel}")
            return entry

    # Landing / catalog fallback (still save reachable link)
    if target.get("try_landing") and target.get("url"):
        rel = _playwright_shot(
            target,
            out_dir,
            "landing",
            target["url"],
            full_page=bool(target.get("full_page", True)),
        )
        if rel:
            entry["landing_screenshot_path"] = rel
            entry["screenshot_path"] = rel
            entry["capture_status"] = STATUS_LANDING
            entry["image_markdown"] = _image_markdown(sid, "landing.png")
            entry["status_note"] = (
                "Marketing/landing page only — not PBQ UI. "
                "Open link for preview or manual pbq-preview register."
            )
            write_json(out_dir / "meta.json", entry)
            print(f"  [{STATUS_LANDING}] {sid} -> {rel}")
            return entry

    entry["capture_status"] = STATUS_FAILED if not entry.get("link_url") else STATUS_LINK
    entry["status_note"] = "No screenshot — use link to open site manually"
    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "meta.json", entry)
    print(f"  [{entry['capture_status']}] {sid} -> {entry.get('link_url', 'no url')}")
    return entry


def build_capture_index(run_id: str, entries: list[dict]) -> Path:
    run_dir = CAPTURES / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "---",
        "type: pbq-capture-index",
        f"run: {run_id}",
        "exam: SY0-701",
        "content_type: pbq",
        "---",
        "",
        f"# PBQ captures — {run_id}",
        "",
        "Security+ **SY0-701** drag-and-drop, PBQ, and simulation references. "
        "Expand `config/secplus-pbq-capture-targets.json` and `pbq_poll` sites as you add sources.",
        "",
        f"Regenerate: `npm run secplus:pbq-capture` · Text scan: `npm run secplus:pbq-monthly`",
        "",
        "---",
        "",
    ]

    by_status = {STATUS_PBq: [], STATUS_LANDING: [], STATUS_LINK: [], STATUS_FAILED: []}
    for e in entries:
        by_status.setdefault(e.get("capture_status", STATUS_LINK), []).append(e)

    def section(title: str, items: list[dict]) -> None:
        if not items:
            return
        lines.append(f"## {title}")
        lines.append("")
        for e in sorted(items, key=lambda x: x.get("source_id", "")):
            sid = e["source_id"]
            hint = e.get("pbq_type_hint", "pbq")
            tier = e.get("tier", "?")
            link = e.get("link_url") or e.get("url", "")
            lines.append(f"### {sid} · {hint} · Tier {tier}")
            lines.append("")
            lines.append(f"**Status:** {e.get('capture_status')} — {e.get('status_note', '')}")
            lines.append("")
            if link:
                lines.append(f"**Open:** [{link}]({link})")
                lines.append("")
            embed = e.get("image_markdown") or e.get("obsidian_embed")
            if embed:
                lines.append(embed)
                lines.append("")
            elif e.get("screenshot_path"):
                rel = Path(e["screenshot_path"]).relative_to(run_dir)
                sid = e.get("source_id", rel.parts[0] if rel.parts else "screenshot")
                lines.append(_image_markdown(sid, rel.name))
                lines.append("")
            lines.append(f"Folder: `captures/{run_id}/{sid}/`")
            lines.append("")
            lines.append("---")
            lines.append("")

    section("PBQ / sim UI captured", by_status[STATUS_PBq])
    section("Landing fallback (open link for preview)", by_status[STATUS_LANDING])
    section("Link only (manual screenshot or recall)", by_status[STATUS_LINK] + by_status[STATUS_FAILED])

    path = run_dir / "INDEX.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def cmd_run(args: argparse.Namespace) -> int:
    run_id = args.date or date.today().isoformat()
    targets = load_all_targets()
    if args.source_id:
        targets = [t for t in targets if t.get("id") == args.source_id]
    if not targets:
        print("[capture] no targets — enable pbq_poll or add config/secplus-pbq-capture-targets.json", file=sys.stderr)
        return 1

    CAPTURES.mkdir(parents=True, exist_ok=True)
    print(f"[capture] run {run_id} · {len(targets)} source(s)")
    manifest_path = CAPTURES / run_id / "manifest.json"
    entries_by_id: dict[str, dict] = {}
    if args.source_id and manifest_path.is_file():
        for e in json.loads(manifest_path.read_text(encoding="utf-8")).get("entries", []):
            sid = e.get("source_id")
            if sid:
                entries_by_id[sid] = e

    for target in targets:
        print(f"[capture] {target['id']} …")
        entries_by_id[target["id"]] = capture_one_target(target, run_id)

    entries = sorted(entries_by_id.values(), key=lambda x: x.get("source_id", ""))

    index_path = build_capture_index(run_id, entries)
    write_json(
        manifest_path,
        {
            "run_id": run_id,
            "count": len(entries),
            "captured_pbq": sum(1 for e in entries if e.get("capture_status") == STATUS_PBq),
            "captured_landing": sum(1 for e in entries if e.get("capture_status") == STATUS_LANDING),
            "link_only": sum(
                1 for e in entries if e.get("capture_status") in (STATUS_LINK, STATUS_FAILED)
            ),
            "entries": entries,
            "capture_index": str(index_path.relative_to(ROOT)),
        },
    )
    print(f"[capture] index -> {index_path.relative_to(ROOT)}")
    print(f"[capture] manifest -> {manifest_path.relative_to(ROOT)}")
    return 0


def cmd_list(_: argparse.Namespace) -> int:
    targets = load_all_targets()
    print(f"[capture] {len(targets)} target(s) — npm run secplus:pbq-capture")
    for t in targets:
        mode = t.get("capture_mode", "auto")
        flags = [mode]
        if t.get("preview_url"):
            flags.append("preview_url")
        if t.get("preview_selector"):
            flags.append("selector")
        print(f"  {t['id']}: {t.get('link_url') or t.get('url')} ({', '.join(flags)})")
    return 0


def cmd_register(args: argparse.Namespace) -> int:
    png = Path(args.png)
    if not png.is_file():
        print(f"PNG not found: {png}", file=sys.stderr)
        return 1
    run_id = args.date or date.today().isoformat()
    out_dir = source_dir(run_id, args.source_id)
    out_dir.mkdir(parents=True, exist_ok=True)
    label = args.label or "pbq-preview"
    dest = out_dir / f"{label}.png"
    dest.write_bytes(png.read_bytes())
    rel = str(dest.relative_to(ROOT))
    entry = _entry_base(
        {
            "id": args.source_id,
            "url": args.url,
            "link_url": args.url,
            "tier": args.tier,
            "notes": args.notes,
            "pbq_type_hint": args.pbq_type or "pbq",
        },
        run_id,
    )
    entry["screenshot_path"] = rel
    entry["capture_status"] = STATUS_PBq
    entry["image_markdown"] = _image_markdown(args.source_id, f"{label}.png")
    entry["status_note"] = "Manual pbq-preview register"
    entry["manual_drop"] = True
    write_json(out_dir / "meta.json", entry)
    print(f"[capture] registered {rel}")

    manifest_path = CAPTURES / run_id / "manifest.json"
    entries: list[dict] = []
    if manifest_path.is_file():
        entries = json.loads(manifest_path.read_text(encoding="utf-8")).get("entries", [])
    entries = [e for e in entries if e.get("source_id") != args.source_id] + [entry]
    build_capture_index(run_id, entries)
    write_json(manifest_path, {"run_id": run_id, "entries": entries})
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Security+ PBQ screenshot capture for marketing-vault")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser("run", help="Capture all targets → PNG or link + INDEX.md")
    p_run.add_argument("--date", help="Run folder YYYY-MM-DD")
    p_run.add_argument("--source-id", help="One source only")
    p_run.set_defaults(func=cmd_run)

    p_list = sub.add_parser("list", help="List capture targets")
    p_list.set_defaults(func=cmd_list)

    for alias in ("screenshot", "capture", "landing-catalog"):
        p = sub.add_parser(alias, help="Alias for run")
        p.add_argument("--date", help="Run folder YYYY-MM-DD")
        p.add_argument("--source-id", help="One source only")
        p.set_defaults(func=cmd_run)

    p_reg = sub.add_parser("register", help="Manual pbq-preview PNG")
    p_reg.add_argument("--png", required=True)
    p_reg.add_argument("--source-id", required=True)
    p_reg.add_argument("--label", default="pbq-preview")
    p_reg.add_argument("--url", default="")
    p_reg.add_argument("--notes", default="")
    p_reg.add_argument("--pbq-type", default="pbq", dest="pbq_type")
    p_reg.add_argument("--tier", default="b")
    p_reg.add_argument("--date", help="Run folder YYYY-MM-DD")
    p_reg.set_defaults(func=cmd_register)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
