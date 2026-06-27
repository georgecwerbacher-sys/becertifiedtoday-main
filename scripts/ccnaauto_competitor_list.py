"""Parse CCNA-Auto/competitor-list.md and load hunt metadata from competitor site notes."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMPETITOR_LIST = ROOT / "CCNA-Auto" / "competitor-list.md"
COMPETITOR_SITES = ROOT / "data" / "competitor-sites"
PRODUCT = "CCNAAUTO-200-901"

sys_path = str(ROOT / "scripts")
if sys_path not in __import__("sys").path:
    __import__("sys").path.insert(0, sys_path)

from secplus_competitor_poll import parse_frontmatter  # noqa: E402

URL_RE = re.compile(r"\((https?://[^)]+)\)")
LOGIN_HINT_RE = re.compile(r"\$|paid|checkout|sign[- ]?in|login|account required", re.I)


def parse_markdown_table(lines: list[str], start: int) -> tuple[list[dict[str, str]], int]:
    rows: list[dict[str, str]] = []
    if start >= len(lines) or not lines[start].strip().startswith("|"):
        return rows, start
    headers = [h.strip().lower() for h in lines[start].strip().strip("|").split("|")]
    i = start + 2
    while i < len(lines):
        line = lines[i].strip()
        if not line.startswith("|"):
            break
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < len(headers):
            cells.extend([""] * (len(headers) - len(cells)))
        rows.append(dict(zip(headers, cells)))
        i += 1
    return rows, i


def parse_competitor_list(path: Path | None = None) -> dict:
    path = path or COMPETITOR_LIST
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    lines = text.splitlines()

    result: dict = {
        "path": str(path),
        "active": [],
        "backlog": [],
        "places_free": [],
        "places_dumps": [],
        "places_other": [],
    }

    section = ""
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("## Active"):
            section = "active"
        elif line.startswith("## Backlog"):
            section = "backlog"
        elif line.startswith("### Free practice"):
            section = "places_free"
        elif line.startswith("### Dumps"):
            section = "places_dumps"
        elif line.startswith("### Other"):
            section = "places_other"
        elif line.strip().startswith("|") and section:
            table_rows, next_i = parse_markdown_table(lines, i)
            key = section
            if key in result:
                for row in table_rows:
                    urls = URL_RE.findall(" ".join(row.values()))
                    row["_url"] = urls[0] if urls else ""
                    row["_login_hint"] = bool(
                        LOGIN_HINT_RE.search(" ".join(row.values()))
                    )
                result[key].extend(table_rows)
            i = next_i
            continue
        i += 1
    return result


def load_competitor_site_meta(product: str = PRODUCT) -> dict[str, dict]:
    """Map poll id -> frontmatter dict for CCNAAUTO competitor notes."""
    meta_by_id: dict[str, dict] = {}
    if not COMPETITOR_SITES.is_dir():
        return meta_by_id
    for path in sorted(COMPETITOR_SITES.glob("*-ccnaauto.md")):
        meta = parse_frontmatter(path)
        if meta.get("product") != product:
            continue
        entry = {
            "file": path.name,
            "brand": meta.get("brand", path.stem),
            "url": meta.get("url", ""),
            "login_required": bool(meta.get("login_required", False)),
            "sign_on_notes": str(meta.get("sign_on_notes", "") or "").strip(),
        }
        for poll_key in ("question_poll", "pbq_poll"):
            poll = meta.get(poll_key)
            if isinstance(poll, dict) and poll.get("id"):
                pid = str(poll["id"])
                meta_by_id[pid] = {
                    **entry,
                    "poll_tier": poll.get("tier", ""),
                    "sample_url": poll.get("sample_url") or meta.get("url", ""),
                    "login_required": bool(
                        poll.get("login_required", entry["login_required"])
                    ),
                    "sign_on_notes": str(
                        poll.get("sign_on_notes") or entry["sign_on_notes"] or ""
                    ).strip(),
                }
    return meta_by_id


def login_required_for_source(source_id: str, meta_by_id: dict[str, dict]) -> tuple[bool, str]:
    info = meta_by_id.get(source_id, {})
    if info.get("login_required"):
        note = info.get("sign_on_notes") or "Source requires sign-on or paid access before full capture."
        return True, note
    return False, ""


def slugify_site(name: str, max_len: int = 40) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (name or "").lower()).strip("-")
    return s[:max_len].strip("-") or "site"
