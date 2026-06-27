#!/usr/bin/env python3
"""Pilot: migrate Security+ Bank 1 slugs to topic-map schema v2 with Tier A verification."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAP_PATH = ROOT / "public/COMP_TIA_SEC+/data/secplus-question-topic-map.json"
HUB_PATH = ROOT / "public/COMP_TIA_SEC+/js/secplus-practice-hub.js"
VERIFIED_AT = "2026-06-27"

TIER_A_BY_OBJECTIVE: dict[str, list[dict]] = {
    "1.1": [
        {
            "type": "comptia-objectives",
            "title": "SY0-701 objective 1.1 security control categories",
            "url": "https://www.comptia.org/en-us/resources/security-plus-sy0-701-exam-objectives/",
        },
        {
            "type": "nist-publication",
            "title": "NIST SP 800-53 Rev. 5 control families",
            "url": "https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final",
        },
    ],
    "1.2": [
        {
            "type": "comptia-objectives",
            "title": "SY0-701 objective 1.2 CIA and AAA fundamentals",
            "url": "https://www.comptia.org/en-us/resources/security-plus-sy0-701-exam-objectives/",
        }
    ],
    "1.3": [
        {
            "type": "comptia-objectives",
            "title": "SY0-701 objective 1.3 change management",
            "url": "https://www.comptia.org/en-us/resources/security-plus-sy0-701-exam-objectives/",
        }
    ],
    "1.4": [
        {
            "type": "nist-publication",
            "title": "NIST cryptographic standards overview",
            "url": "https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines",
        },
        {
            "type": "comptia-objectives",
            "title": "SY0-701 objective 1.4 cryptographic solutions",
            "url": "https://www.comptia.org/en-us/resources/security-plus-sy0-701-exam-objectives/",
        },
    ],
}

DEFAULT_TIER_A = [
    {
        "type": "comptia-objectives",
        "title": "CompTIA Security+ SY0-701 exam objectives",
        "url": "https://www.comptia.org/en-us/resources/security-plus-sy0-701-exam-objectives/",
    }
]


def hub_slugs() -> list[str]:
    text = HUB_PATH.read_text(encoding="utf-8")
    m = re.search(r"SLUGS = \[([\s\S]*?)\];", text)
    if not m:
        return []
    return re.findall(r'"([^"]+)"', m.group(1))


def sources_for_objectives(objectives: list[str]) -> list[dict]:
    seen: set[str] = set()
    out: list[dict] = []
    for oid in objectives:
        maj = oid.split(".")[0] + "." + oid.split(".")[1] if "." in oid else oid
        key = maj if maj in TIER_A_BY_OBJECTIVE else oid.split(".")[0] + "." + oid.split(".")[1]
        if not re.match(r"^\d+\.\d+$", key):
            key = objectives[0].rsplit(".", 1)[0] if objectives else "1.1"
        for src in TIER_A_BY_OBJECTIVE.get(key, DEFAULT_TIER_A):
            url = src["url"]
            if url in seen:
                continue
            seen.add(url)
            out.append(src)
    return out or DEFAULT_TIER_A


def main() -> None:
    data = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    assignments: dict = data.get("assignments") or {}
    bank1 = set(hub_slugs()[:100])

    migrated = 0
    verified = 0

    for file_name, entry in list(assignments.items()):
        slug = file_name.replace(".html", "")
        if slug not in bank1:
            continue
        if isinstance(entry, dict) and entry.get("objectives"):
            objectives = [str(x) for x in entry["objectives"]]
            if entry.get("verification"):
                continue
        elif isinstance(entry, list):
            objectives = [str(x) for x in entry]
        else:
            continue

        if not objectives:
            continue

        is_domain1 = any(o.startswith("1.") for o in objectives)
        new_entry: dict = {
            "objectives": objectives,
            "subObjectives": [],
        }
        if is_domain1:
            new_entry["verification"] = {
                "verifiedAt": VERIFIED_AT,
                "sources": sources_for_objectives(objectives),
            }
            verified += 1

        assignments[file_name] = new_entry
        migrated += 1

    data["schemaVersion"] = 2
    data["blueprintVersion"] = "701"
    data["sourcePdf"] = "CompTIA-Security-Plus-SY0-701-Exam-Objectives.pdf"
    data["notes"] = (
        "Schema v2 migration in progress. Bank 1 domain 1.x items include Tier A verification; "
        "remaining Bank 1 entries are v2 structure pending verification batches."
    )
    data["assignments"] = assignments
    MAP_PATH.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(
        f"[migrate-secplus-topic-map-v2-pilot] bank1 migrated={migrated} "
        f"domain1_verified={verified} → {MAP_PATH.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
