#!/usr/bin/env python3
"""Build SY0-601 → SY0-701 blueprint diff JSON from official objectives files."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEGACY = ROOT / "public/COMP_TIA_SEC+/data/secplus-exam-objectives-sy0-601.json"
CURRENT = ROOT / "public/COMP_TIA_SEC+/data/secplus-exam-objectives-sy0-701.json"
OUT = ROOT / "public/COMP_TIA_SEC+/data/secplus-blueprint-sy0-601-to-701-changes.json"
ARCHIVE = ROOT / "public/COMP_TIA_SEC+/data/secplus-obsolete-question-archive.json"
MAP = ROOT / "public/COMP_TIA_SEC+/data/secplus-question-topic-map.json"
BLUEPRINT_601 = ROOT / "public/COMP_TIA_SEC+/data/secplus-blueprint-sy0-601.json"

COMPTIA_601_VS_701_BLOG = "https://www.comptia.org/en-us/blog/comptia-security-601-vs-701-whats-the-difference/"

# Summarized from CompTIA official blog (Dec 2024) — Tier A cross-check for domain remap narrative.
COMPTIA_BLOG_SUMMARY = {
    "url": COMPTIA_601_VS_701_BLOG,
    "title": "CompTIA Security+ 601 vs. 701: What's the Difference?",
    "published": "2024-12-18",
    "highlights": [
        "SY0-701 has five domains (same count as SY0-601) but 28 objectives vs. 35 on SY0-601.",
        "About 20% of exam objectives were updated for current trends (automation, zero trust, hybrid/cloud, IoT, OT).",
        "Security Operations grows from 16% to 28%; Program Management/Oversight grows from 14% to 20%.",
        "New domain 1.0 General Security Concepts (12%) pulls controls, fundamentals, change management, and crypto basics out of the old 601 mix.",
    ],
    "domain_table": [
        {
            "sy0_601": "Attacks, Threats and Vulnerabilities (24%)",
            "sy0_701": "Threats, Vulnerabilities and Mitigations (22%)",
        },
        {
            "sy0_601": "Architecture and Design (21%)",
            "sy0_701": "Security Architecture (18%)",
        },
        {
            "sy0_601": "Implementation (25%)",
            "sy0_701": "Security Operations (28%)",
        },
        {
            "sy0_601": "Operations and Incident Response (16%)",
            "sy0_701": "Security Operations (28%)",
        },
        {
            "sy0_601": "Governance, Risk and Compliance (14%)",
            "sy0_701": "Security Program Management and Oversight (20%)",
        },
        {
            "sy0_601": "(not a separate 601 domain)",
            "sy0_701": "General Security Concepts (12%)",
        },
    ],
    "sy0_701_domain_focus": [
        {
            "id": "1.0",
            "name": "General Security Concepts",
            "summary": "Security controls, fundamental concepts, change management, cryptographic solutions.",
        },
        {
            "id": "2.0",
            "name": "Threats, Vulnerabilities, and Mitigations",
            "summary": "Threat actors, vectors, attack surfaces, vulnerabilities, mitigation, malicious-activity indicators.",
        },
        {
            "id": "3.0",
            "name": "Security Architecture",
            "summary": "Architecture models, data protection strategies, enterprise infrastructure principles, resilience and recovery.",
        },
        {
            "id": "4.0",
            "name": "Security Operations",
            "summary": "Day-to-day ops: monitoring, vulnerability management, asset management, IAM, automation/orchestration, incident response.",
        },
        {
            "id": "5.0",
            "name": "Security Program Management and Oversight",
            "summary": "Governance, risk management, third-party risk, audits/assessments, security awareness, compliance.",
        },
    ],
}


def load_objectives(path: Path) -> dict[str, dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    out: dict[str, dict] = {}
    for domain in data.get("domains") or []:
        for obj in domain.get("objectives") or []:
            oid = str(obj["id"])
            out[oid] = {
                "id": oid,
                "domain": domain["id"],
                "domainName": domain.get("name"),
                "text": obj.get("text", ""),
            }
    return out


def domain_rows(data: dict) -> list[dict]:
    return [
        {
            "id": d["id"],
            "name": d.get("name"),
            "weightPercent": d.get("weight_percent"),
        }
        for d in data.get("domains") or []
    ]


# Curated crosswalk: retired 601 objective → closest 701 successor (or null if dropped).
SUCCESSOR_MAP: dict[str, str | None] = {
    "1.1": "2.2",
    "1.2": "2.4",
    "1.3": "2.4",
    "1.4": "2.4",
    "1.5": "2.1",
    "1.6": "2.3",
    "1.7": "4.3",
    "1.8": "4.3",
    "2.1": "3.2",
    "2.2": "3.1",
    "2.3": "3.2",
    "2.4": "4.5",
    "2.5": "3.4",
    "2.6": "3.2",
    "2.7": "1.2",
    "2.8": "1.4",
    "3.1": "4.6",
    "3.2": "4.1",
    "3.3": "4.6",
    "3.4": "4.1",
    "3.5": "4.1",
    "3.6": "3.1",
    "3.7": "4.5",
    "3.8": "4.5",
    "3.9": "1.4",
    "4.1": "4.4",
    "4.2": "4.8",
    "4.3": "4.9",
    "4.4": "4.8",
    "4.5": "4.9",
    "5.1": "1.1",
    "5.2": "5.4",
    "5.3": "5.1",
    "5.4": "5.2",
    "5.5": "5.4",
}


def build_changes() -> dict:
    legacy_data = json.loads(LEGACY.read_text(encoding="utf-8"))
    current_data = json.loads(CURRENT.read_text(encoding="utf-8"))
    blueprint_601 = json.loads(BLUEPRINT_601.read_text(encoding="utf-8")) if BLUEPRINT_601.is_file() else {}
    legacy = load_objectives(LEGACY)
    current = load_objectives(CURRENT)

    changes: list[dict] = []

    for did, row in zip(
        [d["id"] for d in legacy_data["domains"]],
        domain_rows(legacy_data),
    ):
        cur = next((d for d in domain_rows(current_data) if d["id"] == did), None)
        if not cur:
            for cd in domain_rows(current_data):
                if cd["name"] != row["name"]:
                    continue
            changes.append(
                {
                    "id": did,
                    "domain": did,
                    "type": "domain_restructure",
                    "sy0_601": f"{row['name']} ({row['weightPercent']}%)",
                    "sy0_701": "See domain_renames table",
                    "hunt": "601 domain retired or renamed in SY0-701.",
                }
            )

    domain_renames = [
        {
            "sy0_601": "1.0 Attacks, Threats, and Vulnerabilities (24%)",
            "sy0_701": "2.0 Threats, Vulnerabilities, and Mitigations (22%)",
            "type": "domain_remap",
        },
        {
            "sy0_601": "2.0 Architecture and Design (21%)",
            "sy0_701": "3.0 Security Architecture (18%)",
            "type": "domain_remap",
        },
        {
            "sy0_601": "3.0 Implementation (25%)",
            "sy0_701": "4.0 Security Operations (28%)",
            "type": "domain_remap",
        },
        {
            "sy0_601": "4.0 Operations and Incident Response (16%)",
            "sy0_701": "4.0 Security Operations (28%)",
            "type": "domain_merge",
        },
        {
            "sy0_601": "5.0 Governance, Risk, and Compliance (14%)",
            "sy0_701": "5.0 Security Program Management and Oversight (20%)",
            "type": "domain_remap",
        },
        {
            "sy0_601": "(none)",
            "sy0_701": "1.0 General Security Concepts (12%)",
            "type": "domain_new",
        },
    ]

    for oid, meta in sorted(legacy.items()):
        successor = SUCCESSOR_MAP.get(oid)
        if successor is None:
            changes.append(
                {
                    "id": oid,
                    "domain": meta["domain"],
                    "type": "removed",
                    "sy0_601": meta["text"],
                    "sy0_701": None,
                    "hunt": "601-only objective with no direct 701 ID. Archive stems that test only this wording.",
                }
            )
        elif legacy[oid]["text"] == current.get(successor, {}).get("text"):
            changes.append(
                {
                    "id": oid,
                    "domain": meta["domain"],
                    "type": "renumbered",
                    "sy0_601": meta["text"],
                    "sy0_701": f"{successor}: {current[successor]['text']}",
                    "successor701": successor,
                    "hunt": "Concept retained; map legacy 601 tags to 701 successor during verification.",
                }
            )
        else:
            changes.append(
                {
                    "id": oid,
                    "domain": meta["domain"],
                    "type": "consolidated",
                    "sy0_601": meta["text"],
                    "sy0_701": f"{successor}: {current[successor]['text']}",
                    "successor701": successor,
                    "hunt": "601 objective folded into broader 701 objective. Re-verify key on Tier A sources.",
                }
            )

    new_701 = sorted(set(current) - set(SUCCESSOR_MAP.values()) - {None})
    for oid in new_701:
        if oid not in [c.get("successor701") for c in changes if c.get("successor701")]:
            pass
    for oid in sorted(current):
        if oid not in set(SUCCESSOR_MAP.values()):
            changes.append(
                {
                    "id": oid,
                    "domain": current[oid]["domain"],
                    "type": "new",
                    "sy0_601": None,
                    "sy0_701": current[oid]["text"],
                    "hunt": "701-only objective (not in SY0-601 PDF). Prioritize new stems and verification.",
                }
            )

    return {
        "from_version": "SY0-601",
        "from_label": "CompTIA Security+ SY0-601 (retired 2024-07-31)",
        "to_version": "SY0-701",
        "to_label": "CompTIA Security+ SY0-701",
        "source_legacy_pdf": legacy_data["exam"]["source_document"],
        "source_legacy_url": legacy_data["exam"].get("source_url")
        or blueprint_601.get("source_pdf_url"),
        "source_current_pdf": current_data["exam"]["source_document"],
        "tier_a_sources": [
            {
                "type": "comptia-pdf",
                "title": "SY0-601 exam objectives PDF",
                "url": legacy_data["exam"].get("source_url") or blueprint_601.get("source_pdf_url"),
            },
            {
                "type": "comptia-pdf",
                "title": "SY0-701 exam objectives PDF",
                "url": "https://www.comptia.org/en-us/resources/security-plus-sy0-701-exam-objectives/",
            },
            {
                "type": "comptia-blog",
                "title": COMPTIA_BLOG_SUMMARY["title"],
                "url": COMPTIA_601_VS_701_BLOG,
            },
        ],
        "comptia_official_comparison": COMPTIA_BLOG_SUMMARY,
        "intro": (
            "Structured diff between official CompTIA SY0-601 and SY0-701 exam objectives PDFs, "
            "cross-checked against CompTIA's public 601 vs. 701 domain comparison. "
            "Use successor701 when triaging legacy-tagged items. Default SY0-701 pools exclude "
            "secplus-obsolete-question-archive.json entries."
        ),
        "domain_renames": domain_renames,
        "weight_changes": [
            {"domain": "1.0", "sy0_601_percent": 24, "sy0_701_percent": 12, "note": "Split: threats → 2.0; controls/crypto → new 1.0"},
            {"domain": "2.0", "sy0_601_percent": 21, "sy0_701_percent": 18, "note": "Architecture and Design → Security Architecture"},
            {"domain": "3.0", "sy0_601_percent": 25, "sy0_701_percent": 28, "note": "Implementation absorbed into Security Operations"},
            {"domain": "4.0", "sy0_601_percent": 16, "sy0_701_percent": 28, "note": "Operations weight doubled; merged with implementation tasks"},
            {"domain": "5.0", "sy0_601_percent": 14, "sy0_701_percent": 20, "note": "GRC expanded to Program Management and Oversight"},
        ],
        "objective_counts": {
            "sy0_601": len(legacy),
            "sy0_701": len(current),
            "sy0_601_with_examples": sum(len(d.get("objectives") or []) for d in blueprint_601.get("domains") or []),
            "sy0_601_top_level_examples": sum(
                len(o.get("children") or [])
                for d in blueprint_601.get("domains") or []
                for o in d.get("objectives") or []
            ),
        },
        "successor_map_601_to_701": SUCCESSOR_MAP,
        "changes": changes,
    }


def build_obsolete_archive(changes_payload: dict) -> dict:
    topic_map = json.loads(MAP.read_text(encoding="utf-8"))
    assignments = topic_map.get("assignments") or {}
    valid_701 = set(load_objectives(CURRENT))

    removed_successors: set[str] = set()
    for c in changes_payload["changes"]:
        if c.get("type") == "removed":
            removed_successors.add(c["id"])

    archived: list[dict] = []
    review: list[dict] = []

    for file_name, entry in sorted(assignments.items()):
        if isinstance(entry, list):
            objs = [str(x) for x in entry]
        else:
            objs = [str(x) for x in (entry.get("objectives") or [])]

        unknown = [o for o in objs if o not in valid_701]
        if unknown:
            review.append(
                {
                    "file": file_name,
                    "reason": "non_pdf_objective_id_remap_needed",
                    "objectives": unknown,
                    "note": "Legacy v1 extended IDs (e.g. 3.8, 3.10). Remap to SY0-701 PDF IDs before excluding from pools.",
                }
            )

    hub = (ROOT / "public/COMP_TIA_SEC+/js/secplus-practice-hub.js").read_text(encoding="utf-8")
    import re

    slugs = re.findall(r'"([^"]+)"', re.search(r"SLUGS = \[([\s\S]*?)\];", hub).group(1))
    for slug in slugs:
        key = slug + ".html"
        if key not in assignments:
            review.append({"file": key, "reason": "hub_slug_missing_from_map"})

    return {
        "schemaVersion": 1,
        "blueprintVersion": "701",
        "exam": "SY0-701",
        "source_diff": str(OUT.relative_to(ROOT)),
        "notes": (
            "Default practice pools exclude files listed in archived. "
            "candidateReview lists hub/map sync issues, not auto-archived."
        ),
        "archived": archived,
        "candidateReview": review,
        "dropped601ObjectiveIds": sorted(removed_successors),
    }


def main() -> None:
    payload = build_changes()
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    archive = build_obsolete_archive(payload)
    ARCHIVE.write_text(json.dumps(archive, indent=2) + "\n", encoding="utf-8")

    import subprocess

    sync = ROOT / "scripts/sync-secplus-question-exam-version.py"
    if sync.is_file():
        subprocess.run([sys.executable, str(sync)], check=False, cwd=ROOT)

    print(f"[build-secplus-blueprint-diff] changes → {OUT.relative_to(ROOT)}")
    print(
        f"[build-secplus-blueprint-diff] archive: {len(archive['archived'])} archived, "
        f"{len(archive['candidateReview'])} review"
    )


if __name__ == "__main__":
    main()
