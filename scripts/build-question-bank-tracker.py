#!/usr/bin/env python3
"""Build question-bank tracker JSON: actual vs blueprint domain targets."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent.parent

TRACKS: dict[str, dict[str, Path | bool]] = {
    "ccnaauto": {
        "blueprint": ROOT / "public/CCNAAUTO-Study/data/ccnaauto-practice-bank-blueprint.json",
        "map": ROOT / "public/CCNAAUTO-Study/data/ccnaauto-question-topic-map.json",
        "questions_dir": ROOT / "public/CCNAAUTO-Study/CCNAAUTO_Questions",
        "tracker": ROOT / "public/CCNAAUTO-Study/data/ccnaauto-question-topic-tracker.json",
        "recursive": False,
    },
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def sorted_html_files(directory: Path, *, recursive: bool = False) -> list[str]:
    if not directory.is_dir():
        return []
    if recursive:
        return sorted(p.relative_to(directory).as_posix() for p in directory.rglob("*.html"))
    return sorted(p.name for p in directory.glob("*.html"))


def normalize_entry(entry: object) -> tuple[list[str], list[str], dict | None]:
    """Return (objectives, sub_objectives, verification_or_none)."""
    if isinstance(entry, list):
        return [str(x) for x in entry], [], None
    if isinstance(entry, dict):
        objs = [str(x) for x in entry.get("objectives") or []]
        subs = [str(x) for x in entry.get("subObjectives") or []]
        ver = entry.get("verification")
        return objs, subs, ver if isinstance(ver, dict) else None
    return [], [], None


def domain_major(objective_id: str) -> str:
    m = re.match(r"^(\d+)\.", str(objective_id))
    return m.group(1) if m else ""


def url_allowed(url: str, suffixes: list[str]) -> bool:
    try:
        host = (urlparse(url).hostname or "").lower()
    except Exception:
        return False
    for suffix in suffixes:
        s = suffix.lower().lstrip(".")
        if host == s or host.endswith("." + s):
            return True
    return False


def build_tracker(track_key: str) -> dict:
    cfg = TRACKS[track_key]
    blueprint = load_json(cfg["blueprint"])  # type: ignore[arg-type]
    topic_map = load_json(cfg["map"])  # type: ignore[arg-type]
    questions_dir: Path = cfg["questions_dir"]  # type: ignore[assignment]
    recursive = bool(cfg.get("recursive", False))

    files = sorted_html_files(questions_dir, recursive=recursive)
    assignments: dict = topic_map.get("assignments") or {}
    domains_cfg = blueprint.get("domains") or []
    bank_size = int(blueprint.get("bankSize") or 100)
    allowed_suffixes = (blueprint.get("verificationPolicy") or {}).get("allowedHostSuffixes") or [
        "cisco.com",
        "developer.cisco.com",
        "learningnetwork.cisco.com",
    ]

    domain_targets = {d["id"]: int(d.get("questionsPerBank") or 0) for d in domains_cfg}
    domain_names = {d["id"]: d.get("name") or d["id"] for d in domains_cfg}
    domain_counts: dict[str, int] = {did: 0 for did in domain_targets}
    objective_counts: dict[str, int] = {}
    unassigned: list[str] = []
    missing_verification: list[str] = []
    invalid_verification_url: list[str] = []
    unknown_objectives: list[str] = []

    known_objective_ids: set[str] = set()
    for d in domains_cfg:
        known_objective_ids.add(d["id"])
        # objectives live in separate blueprint file for ccnaauto; accept major ids only here

    for file_name in files:
        entry = assignments.get(file_name)
        if entry is None:
            unassigned.append(file_name)
            continue
        objs, subs, verification = normalize_entry(entry)
        all_ids = objs + subs
        if not all_ids:
            unassigned.append(file_name)
            continue

        if topic_map.get("schemaVersion") == 2:
            if not verification or not verification.get("sources"):
                missing_verification.append(file_name)
            else:
                for src in verification.get("sources") or []:
                    url = str((src or {}).get("url") or "")
                    if url and not url_allowed(url, allowed_suffixes):
                        invalid_verification_url.append(file_name)

        majors_seen: set[str] = set()
        for oid in all_ids:
            objective_counts[oid] = objective_counts.get(oid, 0) + 1
            maj = domain_major(oid)
            if maj:
                major_id = f"{maj}.0"
                if major_id in domain_counts:
                    if major_id not in majors_seen:
                        domain_counts[major_id] += 1
                        majors_seen.add(major_id)
                elif oid not in known_objective_ids:
                    unknown_objectives.append(f"{file_name} → {oid}")

    assigned_count = len(files) - len(unassigned)
    domains_summary = []
    for d in domains_cfg:
        did = d["id"]
        target = domain_targets.get(did, 0)
        count = domain_counts.get(did, 0)
        pct = round((count / assigned_count) * 100, 1) if assigned_count else 0.0
        target_pct = float(d.get("weightPercent") or 0)
        domains_summary.append(
            {
                "id": did,
                "name": domain_names.get(did, did),
                "weightPercent": target_pct,
                "questionsPerBankTarget": target,
                "assignedQuestionCount": count,
                "assignedPercent": pct,
                "gapToTarget": target - count,
            }
        )

    n_banks = max(1, (len(files) + bank_size - 1) // bank_size) if files else 1
    return {
        "schemaVersion": 1,
        "track": track_key,
        "exam": blueprint.get("exam"),
        "blueprintVersion": blueprint.get("blueprintVersion"),
        "sourcePdf": blueprint.get("sourcePdf"),
        "bankSize": bank_size,
        "source": {
            "blueprint": str(cfg["blueprint"].relative_to(ROOT)),  # type: ignore[union-attr]
            "map": str(cfg["map"].relative_to(ROOT)),  # type: ignore[union-attr]
        },
        "totals": {
            "questionFileCount": len(files),
            "assignedQuestionCount": assigned_count,
            "unassignedQuestionCount": len(unassigned),
            "assignedPercent": round((assigned_count / len(files)) * 100, 1) if files else 0.0,
            "bankCount": n_banks,
            "questionsInCurrentBank": len(files) % bank_size or (bank_size if files else 0),
        },
        "unassignedQuestionFiles": unassigned,
        "missingVerificationFiles": sorted(set(missing_verification)),
        "invalidVerificationUrlFiles": sorted(set(invalid_verification_url)),
        "unknownObjectiveLinks": sorted(set(unknown_objectives)),
        "domains": domains_summary,
        "objectiveCounts": dict(sorted(objective_counts.items())),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Build question bank domain tracker")
    ap.add_argument(
        "--track",
        choices=sorted(TRACKS.keys()),
        default="ccnaauto",
        help="Track key (default: ccnaauto)",
    )
    args = ap.parse_args()
    cfg = TRACKS[args.track]
    tracker = build_tracker(args.track)
    out: Path = cfg["tracker"]  # type: ignore[assignment]
    write_json(out, tracker)
    t = tracker["totals"]
    print(
        f"[build-question-bank-tracker] {args.track}: "
        f"{t['questionFileCount']} files · {t['assignedQuestionCount']} assigned · "
        f"bank {t['bankCount']} → {out.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
