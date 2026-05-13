#!/usr/bin/env python3
"""Guardrail for published practice questions: fail on non-Cisco http(s) URLs.

Primary project policy: **verify answers** (stems, keys, explanations) against
**official Cisco sources** only—documentation, configuration/command references,
Cisco Learning Network, DevNet where relevant—not exam dumps or unvetted sites.

This script only checks that question HTML and the CCNA chain generator do not
embed disallowed URL hosts; it does not fetch or validate doc content.

Scanned paths:
  - public/CCNA-Study/CCNA_questions/*.html (CCNA extra chain)
  - public/question-*.html (CCNP numbered practice pages)
  - scripts/gen_ccna_chain_pages.py (CCNA chain source strings)

Allowed hostnames: cisco.com and any *.cisco.com (e.g. learningnetwork.cisco.com,
developer.cisco.com, www.cisco.com).

Relative paths (/CCNA-Study/..., /question-1.html) are fine.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CCNA_QUESTIONS = ROOT / "public/CCNA-Study/CCNA_questions"
PUBLIC = ROOT / "public"
CHAIN_GENERATOR = ROOT / "scripts" / "gen_ccna_chain_pages.py"

URL_RE = re.compile(r"https?://([^/\s\"'<>]+)", re.IGNORECASE)
TOOL = "lint-practice-question-urls"


def _hostname(url_match_group1: str) -> str:
    host = url_match_group1.split("@")[-1]
    host = host.split(":")[0]
    return host.lower().rstrip(".")


def _host_allowed(host: str) -> bool:
    return host == "cisco.com" or host.endswith(".cisco.com")


def violations_in_text(rel_path: str, text: str) -> list[str]:
    out: list[str] = []
    for m in URL_RE.finditer(text):
        raw = m.group(1)
        host = _hostname(raw)
        if not _host_allowed(host):
            out.append(f"{rel_path}: disallowed URL {m.group(0)!r} (host {host!r})")
    return out


def main() -> int:
    errors: list[str] = []
    if CCNA_QUESTIONS.is_dir():
        for path in sorted(CCNA_QUESTIONS.glob("*.html")):
            text = path.read_text(encoding="utf-8", errors="replace")
            rel = str(path.relative_to(ROOT))
            errors.extend(violations_in_text(rel, text))
    if PUBLIC.is_dir():
        for path in sorted(PUBLIC.glob("question-*.html")):
            text = path.read_text(encoding="utf-8", errors="replace")
            rel = str(path.relative_to(ROOT))
            errors.extend(violations_in_text(rel, text))
    if CHAIN_GENERATOR.is_file():
        text = CHAIN_GENERATOR.read_text(encoding="utf-8", errors="replace")
        rel = str(CHAIN_GENERATOR.relative_to(ROOT))
        errors.extend(violations_in_text(rel, text))

    if errors:
        print(f"{TOOL}: FAILED\n", file=sys.stderr)
        for line in errors:
            print(f"  {line}", file=sys.stderr)
        print(
            "\nOnly https?://*.cisco.com URLs may appear in these files. "
            "Omit links or use official Cisco documentation.",
            file=sys.stderr,
        )
        return 1
    print(
        f"{TOOL}: OK (no disallowed URLs in "
        f"{CCNA_QUESTIONS.relative_to(ROOT)}/*.html, "
        f"{PUBLIC.relative_to(ROOT)}/question-*.html, "
        f"{CHAIN_GENERATOR.relative_to(ROOT)})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
