#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OBJECTIVES_PATH = ROOT / "public" / "CCNA-Study" / "data" / "ccna-exam-objectives-200-301-v1.1.json"

CONTENT_TYPES = {
    "question": {
        "dir": ROOT / "public" / "CCNA-Study" / "CCNA_questions",
        "map": ROOT / "public" / "CCNA-Study" / "data" / "ccna-question-topic-map.json",
        "tracker": ROOT / "public" / "CCNA-Study" / "data" / "ccna-question-topic-tracker.json",
        "label": "questions",
    },
    "dnd": {
        "dir": ROOT / "public" / "CCNA-Study" / "CCNA_D_D",
        "map": ROOT / "public" / "CCNA-Study" / "data" / "ccna-dnd-topic-map.json",
        "tracker": ROOT / "public" / "CCNA-Study" / "data" / "ccna-dnd-topic-tracker.json",
        "label": "drag and drops",
    },
    "lab": {
        "dir": ROOT / "public" / "CCNA-Study" / "CCNA_labs",
        "map": ROOT / "public" / "CCNA-Study" / "data" / "ccna-lab-topic-map.json",
        "tracker": ROOT / "public" / "CCNA-Study" / "data" / "ccna-lab-topic-tracker.json",
        "label": "labs",
    },
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def sorted_html_files(directory: Path) -> list[str]:
    return sorted(p.name for p in directory.glob("*.html"))


def suggest_objectives_from_filename(file_name: str) -> list[str]:
    s = file_name.lower()

    rules: list[tuple[list[str], list[str]]] = [
        (["ospf", "route", "routing", "fhrp", "vrrp", "hsrp"], ["3.0"]),
        (["vlan", "trunk", "stp", "spanning", "etherchannel", "lacp", "lldp", "cdp"], ["2.0"]),
        (["nat", "ntp", "dhcp", "dns", "syslog", "snmp", "ssh", "ftp", "tftp", "qos"], ["4.0"]),
        (["acl", "ipsec", "wpa", "wireless-security", "8021x", "port-security", "snooping", "inspection"], ["5.0"]),
        (["rest", "json", "ansible", "terraform", "automation", "sdn", "controller", "api"], ["6.0"]),
        (["ipv4", "ipv6", "subnet", "tcp", "udp", "cable", "fiber", "wan", "soho", "topology", "switch", "router"], ["1.0"]),
        (["wireless", "wlan", "wlc", "ap", "ssid", "rf"], ["2.0"]),
    ]

    hits: list[str] = []
    for keywords, objective_ids in rules:
        if any(k in s for k in keywords):
            for oid in objective_ids:
                if oid not in hits:
                    hits.append(oid)

    return hits


def ensure_map(map_path: Path, files: list[str]) -> dict:
    if map_path.exists():
        mapping = load_json(map_path)
    else:
        mapping = {
            "schemaVersion": 1,
            "notes": "Assign CCNA question files to one or more objective IDs (e.g. 1.5, 4.8). New files receive a heuristic default domain ID (e.g. 4.0) that you can refine.",
            "assignments": {},
        }

    assignments = mapping.setdefault("assignments", {})
    for name in files:
        if name not in assignments or not isinstance(assignments[name], list):
            assignments[name] = suggest_objectives_from_filename(name)

    # Keep map clean: remove entries for files that no longer exist
    stale = [name for name in assignments.keys() if name not in files]
    for name in stale:
        assignments.pop(name, None)

    # Sort keys for stable diffs
    mapping["assignments"] = {name: assignments[name] for name in sorted(assignments.keys())}
    write_json(map_path, mapping)
    return mapping


def build_tracker(objectives: dict, mapping: dict, files: list[str], map_path: Path) -> dict:
    assignments: dict[str, list[str]] = mapping.get("assignments", {})
    domain_lookup: dict[str, dict] = {}
    objective_lookup: dict[str, dict] = {}
    domain_to_questions: dict[str, list[str]] = {}
    objective_to_questions: dict[str, list[str]] = {}

    for domain in objectives.get("domains", []):
        did = domain["id"]
        domain_lookup[did] = domain
        domain_to_questions[did] = []
        for obj in domain.get("objectives", []):
            oid = obj["id"]
            objective_lookup[oid] = obj
            objective_to_questions[oid] = []

    unassigned_files: list[str] = []
    unknown_objective_links: list[dict] = []

    for f in files:
        linked = assignments.get(f, [])
        if not linked:
            unassigned_files.append(f)
            continue
        matched_any = False
        for oid in linked:
            if oid in objective_to_questions:
                objective_to_questions[oid].append(f)
                matched_any = True
            elif oid in domain_to_questions:
                domain_to_questions[oid].append(f)
                matched_any = True
            else:
                unknown_objective_links.append({"file": f, "objectiveId": oid})
        if not matched_any:
            unassigned_files.append(f)

    domains_summary = []
    for domain in objectives.get("domains", []):
        objective_summaries = []
        covered = 0
        domain_files = set(domain_to_questions.get(domain["id"], []))
        for obj in domain.get("objectives", []):
            oid = obj["id"]
            obj_files = sorted(objective_to_questions.get(oid, []))
            if obj_files:
                covered += 1
            objective_summaries.append(
                {
                    "id": oid,
                    "text": obj["text"],
                    "questionCount": len(obj_files),
                    "questionFiles": obj_files,
                }
            )
        total = len(domain.get("objectives", []))
        domains_summary.append(
            {
                "id": domain["id"],
                "name": domain["name"],
                "weightPercent": domain["weight_percent"],
                "domainAssignedQuestionCount": len(domain_files),
                "objectiveCount": total,
                "coveredObjectiveCount": covered,
                "coveragePercent": round((covered / total) * 100, 1) if total else 0.0,
                "objectives": objective_summaries,
            }
        )

    assigned_questions = len(files) - len(unassigned_files)
    return {
        "schemaVersion": 1,
        "source": {
            "objectives": str(OBJECTIVES_PATH.relative_to(ROOT)),
            "map": str(map_path.relative_to(ROOT)),
        },
        "totals": {
            "questionCount": len(files),
            "assignedQuestionCount": assigned_questions,
            "unassignedQuestionCount": len(unassigned_files),
            "assignedPercent": round((assigned_questions / len(files)) * 100, 1) if files else 0.0,
        },
        "unassignedQuestionFiles": unassigned_files,
        "unknownObjectiveLinks": unknown_objective_links,
        "domains": domains_summary,
    }


def main() -> None:
    objectives = load_json(OBJECTIVES_PATH)
    for content_type, cfg in CONTENT_TYPES.items():
        files = sorted_html_files(cfg["dir"])
        mapping = ensure_map(cfg["map"], files)
        tracker = build_tracker(objectives, mapping, files, cfg["map"])
        write_json(cfg["tracker"], tracker)
        print(
            f"Wrote tracker for {tracker['totals']['questionCount']} {cfg['label']} "
            f"({tracker['totals']['assignedQuestionCount']} assigned) -> {cfg['tracker'].relative_to(ROOT)}"
        )


if __name__ == "__main__":
    main()

