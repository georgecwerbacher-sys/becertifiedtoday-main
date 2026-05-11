#!/usr/bin/env python3
"""Build ccna-practice-questions-manifest.json from ccna-practice-100-hub.js + question HTML titles."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HUB = ROOT / "public/CCNA-Study/js/ccna-practice-100-hub.js"
QUESTIONS = ROOT / "public/CCNA-Study/CCNA_questions"
OUT = ROOT / "public/CCNA-Study/data/ccna-practice-questions-manifest.json"

TITLE_RE = re.compile(r"<title>([^<]*)</title>", re.I)


def slugs_from_hub() -> list[str]:
    text = HUB.read_text(encoding="utf-8")
    m = re.search(r"ALL_SLUGS\s*=\s*\[(.*?)\];", text, re.S)
    if not m:
        raise SystemExit("Could not find ALL_SLUGS in ccna-practice-100-hub.js")
    return re.findall(r'"([^"]+)"', m.group(1))


def title_from_html(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    m = TITLE_RE.search(raw)
    if m:
        return m.group(1).strip()
    return path.stem.replace("-", " ").title()


def main() -> None:
    slugs = slugs_from_hub()
    items: list[dict[str, str]] = []
    missing: list[str] = []
    for slug in slugs:
        p = QUESTIONS / f"{slug}.html"
        if not p.is_file():
            missing.append(slug)
            continue
        items.append({"slug": slug, "title": title_from_html(p)})
    payload = {
        "schemaVersion": 1,
        "source": "public/CCNA-Study/js/ccna-practice-100-hub.js",
        "count": len(items),
        "items": items,
    }
    if missing:
        payload["missingHtml"] = missing
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("Wrote", len(items), "entries to", OUT.relative_to(ROOT))
    if missing:
        print("WARNING: missing HTML for", len(missing), "slug(s):", ", ".join(missing[:12]), "..." if len(missing) > 12 else "")


if __name__ == "__main__":
    main()
