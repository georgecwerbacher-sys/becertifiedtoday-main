#!/usr/bin/env python3
"""Sync ENCOR guest pool → home/free blueprints, free-simulation queue.json, and build JS embed."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POOL_PATH = ROOT / "public/CCNP-ENCOR-Study/data/encor-guest-sample-pool.json"
HOME_BP = ROOT / "public/CCNP-ENCOR-Study/data/encor-home-sample-blueprint.json"
FREE_BP = ROOT / "public/CCNP-ENCOR-Study/data/encor-free-simulation-blueprint.json"
QUEUE_PATH = ROOT / "public/CCNP-ENCOR-Study/data/free-simulation/queue.json"
BUILD_JS = ROOT / "public/CCNP-ENCOR-Study/js/encor-test-sim-build.js"


def main() -> None:
    pool = json.loads(POOL_PATH.read_text(encoding="utf-8"))
    mcq_ids = pool["mcqIds"]
    drag_ids = pool["dragDropIds"]
    drag_paths = pool["dragDropPaths"]
    lab_files = pool["labFiles"]
    lab_base = "/CCNP-ENCOR-Study/CCNP-ENCOR-Labs/"

    home = json.loads(HOME_BP.read_text(encoding="utf-8"))
    home["mcqIds"] = mcq_ids
    home["dragDropIds"] = drag_ids
    home["dragDropPaths"] = drag_paths
    home["lab"] = {
        "type": "lab",
        "path": pool["labPath"],
        "title": home.get("lab", {}).get("title", "ACL and CoPP CLI lab"),
    }
    home["notes"] = (
        "Homepage tracks: 2 shuffled MCQ from encor-guest-sample-pool.json, two D&D items, ACL/CoPP lab. "
        "Free timed simulation uses the same guest pool."
    )
    HOME_BP.write_text(json.dumps(home, indent=2) + "\n", encoding="utf-8")

    free = json.loads(FREE_BP.read_text(encoding="utf-8"))
    free["multipleChoiceCount"] = len(mcq_ids)
    free["multipleChoiceIds"] = mcq_ids
    free["dragDropIds"] = drag_ids
    free["dragDropPaths"] = drag_paths
    free["labFiles"] = lab_files
    free["totalItems"] = len(mcq_ids) + len(drag_ids) + len(lab_files)
    free["guestPoolUrl"] = "/CCNP-ENCOR-Study/data/encor-guest-sample-pool.json"
    free["notes"] = (
        "Email-unlocked ENCOR guest sample uses encor-guest-sample-pool.json — "
        "same MCQ/D&D/lab files as homepage previews."
    )
    FREE_BP.write_text(json.dumps(free, indent=2) + "\n", encoding="utf-8")

    queue_items = []
    for qid in mcq_ids:
        queue_items.append(
            {
                "kind": "question",
                "url": f"/CCNP-ENCOR-Study/ENCOR_Questions/question-{qid}.html",
                "id": qid,
            }
        )
    for qid in drag_ids:
        queue_items.append(
            {
                "kind": "dragdrop",
                "url": drag_paths[str(qid)],
                "id": qid,
            }
        )
    for fn in lab_files:
        queue_items.append(
            {
                "kind": "sim",
                "url": lab_base + fn,
                "file": fn,
            }
        )

    queue_doc = {
        "schemaVersion": 1,
        "productId": "encor-free-simulation",
        "durationMinutes": free.get("durationMinutes", 45),
        "title": free.get("title", "Free ENCOR timed simulation sample"),
        "guestPoolUrl": "/CCNP-ENCOR-Study/data/encor-guest-sample-pool.json",
        "notes": f"Fixed lead-magnet exam queue ({len(mcq_ids)} MCQ + {len(drag_ids)} D&D + {len(lab_files)} lab). Synced from encor-guest-sample-pool.json.",
        "queue": queue_items,
    }
    QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
    QUEUE_PATH.write_text(json.dumps(queue_doc, indent=2) + "\n", encoding="utf-8")

    js_lines = []
    for item in queue_items:
        js_lines.append(f'    {{ kind: "{item["kind"]}", url: "{item["url"]}" }},')

    build_src = BUILD_JS.read_text(encoding="utf-8")
    pattern = re.compile(
        r"/\*\* Mirror of data/free-simulation/queue\.json — sync start, no fetch at exam launch\. \*/\n"
        r"  var FREE_SIM_QUEUE_ITEMS = \[\n.*?\n  \];",
        re.S,
    )
    replacement = (
        "/** Mirror of data/free-simulation/queue.json — sync via scripts/sync-encor-guest-free-sim.py */\n"
        "  var FREE_SIM_QUEUE_ITEMS = [\n"
        + "\n".join(js_lines)
        + "\n  ];"
    )
    if not pattern.search(build_src):
        raise SystemExit("Could not find FREE_SIM_QUEUE_ITEMS block in encor-test-sim-build.js")
    BUILD_JS.write_text(pattern.sub(replacement, build_src), encoding="utf-8")

    missing = []
    pub = ROOT / "public"
    for item in queue_items:
        if not (pub / item["url"].lstrip("/")).exists():
            missing.append(item["url"])
    if missing:
        raise SystemExit("Missing files:\n" + "\n".join(missing))

    print(f"Synced {len(queue_items)} items from {POOL_PATH.name}")


if __name__ == "__main__":
    main()
