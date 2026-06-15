#!/usr/bin/env python3
"""Scaffold a new router CLI lab from templates/labs/cli-lab-router-baseline.html."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "labs" / "cli-lab-router-baseline.html"
HELP_LIB = ROOT / "scripts" / "lib" / "cli-lab-router-help.mjs"
DEFAULT_OUT_DIR = ROOT / "public" / "CCNA-Study" / "CCNA_labs"


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    if not slug.startswith("cli-lab-"):
        slug = f"cli-lab-{slug}"
    if not slug.endswith(".html"):
        slug = f"{slug}-sim.html" if not slug.endswith("-sim") else f"{slug}.html"
    return slug


def build_help_comment(title: str) -> str:
    intro = [
        f"CCNA CLI lab — {title}.",
        "Scaffolded from templates/labs/cli-lab-router-baseline.html.",
    ]
    script = f"""
import {{ buildRouterHelpComment }} from './scripts/lib/cli-lab-router-help.mjs';
const intro = {json.dumps(intro)};
process.stdout.write(buildRouterHelpComment('new-lab', intro));
"""
    out = subprocess.run(
        ["node", "--input-type=module", "-e", script],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return out.stdout.rstrip("\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a router CLI lab HTML scaffold.")
    parser.add_argument("title", help='Lab title, e.g. "BGP Neighbor Sim"')
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT_DIR,
        help="Output directory (default: public/CCNA-Study/CCNA_labs)",
    )
    parser.add_argument("--slug", help="Output filename (default: cli-lab-<slug>-sim.html)")
    args = parser.parse_args()

    if not TEMPLATE.is_file():
        print(f"Missing template: {TEMPLATE}", file=sys.stderr)
        return 1

    slug = args.slug or slugify(args.title)
    if not slug.endswith(".html"):
        slug += ".html"
    out_path = args.out / slug
    if out_path.exists():
        print(f"Refusing to overwrite existing file: {out_path}", file=sys.stderr)
        return 1

    help_comment = build_help_comment(args.title)
    text = TEMPLATE.read_text(encoding="utf-8")
    text = text.replace("REPLACE: Lab title", args.title)
    text = text.replace("REPLACE: cli-lab-router-baseline.html", slug)
    text = re.sub(
        r"<!--\s*ROUTER_HELP_COMMENT\s*-->",
        f"<!--\n{help_comment}\n-->",
        text,
        count=1,
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    print(f"Created {out_path.relative_to(ROOT)}")
    print("Next steps:")
    print(f"  1. Add profile cases to scripts/lib/cli-lab-router-help.mjs")
    print(f"  2. node scripts/test-cli-lab-help.mjs {slug}")
    print(f"  3. python3 scripts/patch-lab-ios-help.py  # wire tryAppendIosHelp if needed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
