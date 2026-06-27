#!/usr/bin/env python3
"""Build secplus-blueprint-sy0-701.json from the official CompTIA SY0-701 objectives PDF."""
from __future__ import annotations

import argparse
import json
import re
import string
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PDF = ROOT / "public/COMP_TIA_SEC+/misc/CompTIA-Security-Plus-SY0-701-Exam-Objectives.pdf"
OUT = ROOT / "public/COMP_TIA_SEC+/data/secplus-blueprint-sy0-701.json"
LEGACY_OUT = ROOT / "public/COMP_TIA_SEC+/data/secplus-exam-objectives-sy0-701.json"

DOMAINS = [
    {"id": "1.0", "title": "General Security Concepts", "weight": "12%"},
    {"id": "2.0", "title": "Threats, Vulnerabilities, and Mitigations", "weight": "22%"},
    {"id": "3.0", "title": "Security Architecture", "weight": "18%"},
    {"id": "4.0", "title": "Security Operations", "weight": "28%"},
    {"id": "5.0", "title": "Security Program Management and Oversight", "weight": "20%"},
]

OBJECTIVE_TEXT: dict[str, str] = {
    "1.1": "Compare and contrast various types of security controls.",
    "1.2": "Summarize fundamental security concepts.",
    "1.3": "Explain the importance of change management processes and the impact to security.",
    "1.4": "Explain the importance of using appropriate cryptographic solutions.",
    "2.1": "Compare and contrast common threat actors and motivations.",
    "2.2": "Explain common threat vectors and attack surfaces.",
    "2.3": "Explain various types of vulnerabilities.",
    "2.4": "Given a scenario, analyze indicators of malicious activity.",
    "2.5": "Explain the purpose of mitigation techniques used to secure the enterprise.",
    "3.1": "Compare and contrast security implications of different architecture models.",
    "3.2": "Given a scenario, apply security principles to secure enterprise infrastructure.",
    "3.3": "Compare and contrast concepts and strategies to protect data.",
    "3.4": "Explain the importance of resilience and recovery in security architecture.",
    "4.1": "Given a scenario, apply common security techniques to computing resources.",
    "4.2": "Explain the security implications of proper hardware, software, and data asset management.",
    "4.3": "Explain various activities associated with vulnerability management.",
    "4.4": "Explain security alerting and monitoring concepts and tools.",
    "4.5": "Given a scenario, implement and maintain identity and access management.",
    "4.6": "Given a scenario, modify enterprise capabilities to enhance security.",
    "4.7": "Explain the importance of automation and orchestration related to secure operations.",
    "4.8": "Explain appropriate incident response activities.",
    "4.9": "Given a scenario, use data sources to support an investigation.",
    "5.1": "Summarize elements of effective security governance.",
    "5.2": "Explain elements of the risk management process.",
    "5.3": "Explain the processes associated with third-party risk assessment and management.",
    "5.4": "Summarize elements of effective security compliance.",
    "5.5": "Explain types and purposes of audits and assessments.",
    "5.6": "Given a scenario, implement security awareness practices.",
}

PAGE_SECTIONS: dict[int, list[tuple[str, str | None, str | None]]] = {
    4: [
        ("1.1", "• Categories", "Summarize fundamental security concepts."),
        ("1.2", "• Confidentiality, Integrity", None),
    ],
    5: [
        ("1.4", "• Public key infrastructure (PKI)", "1.3 Explain the importance of change management"),
        ("1.3", "• Business processes impacting", None),
    ],
    6: [
        ("2.1", "• Threat actors", "Explain common threat vectors"),
        ("2.2", "• Message-based", None),
    ],
    7: [
        ("2.3", "• Application", "Given a scenario, analyze indicators"),
        ("2.5", "• Malware attacks", None),
    ],
    8: [
        ("3.1", "• Architecture and infrastructure", "Given a scenario, apply security principles"),
        ("3.2", "• Infrastructure considerations", None),
    ],
    9: [
        ("3.3", "• Data types", "• High availability"),
        ("3.4", "• High availability", None),
    ],
    10: [
        ("4.1", "• Secure baselines", "Explain the security implications of proper hardware"),
        ("4.2", "• Acquisition/procurement process", None),
    ],
    11: [
        ("4.4", "• Monitoring computing resources", "4.3 Explain various activities"),
        ("4.3", "• Identification methods", None),
    ],
    12: [
        ("4.5", "• Firewall", "Given a scenario, modify enterprise capabilities"),
    ],
    13: [
        ("4.7", "• Use cases of automation", "• Process"),
        ("4.8", "• Process", "• Log data"),
        ("4.9", "• Log data", None),
    ],
    14: [
        ("5.1", "• Guidelines", "Explain elements of the risk management process."),
        ("5.2", "• Risk identification", None),
    ],
    15: [
        ("5.3", "• Vendor assessment", "• Compliance reporting"),
        ("5.4", "• Compliance reporting", "• Attestation"),
        ("5.5", "• Attestation", None),
    ],
    16: [
        ("5.6", "• Phishing", None),
    ],
}


def normalize(text: str) -> str:
    text = text.replace("\u2022", "•").replace("\uf0b7", "•").replace("\t", "    ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def slice_section(page_text: str, start: str | None, end_before: str | None) -> str:
    text = normalize(page_text)
    if start:
        idx = text.find(start)
        if idx == -1:
            raise ValueError(f"Start marker not found: {start!r}")
        text = text[idx:]
    if end_before:
        end_idx = text.find(end_before)
        if end_idx == -1:
            raise ValueError(f"End marker not found: {end_before!r}")
        text = text[:end_idx]
    text = re.split(r"CompTIA Security\+ SY0-701 Certification Exam", text)[0]
    text = re.split(r"CompTIA Security\+ Certification Exam Objectives", text)[0]
    text = re.sub(r"^\d\.\d+\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\d\.0 .+$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\d\.0\s+\|\s+.+$", "", text, flags=re.MULTILINE)
    return text.strip()


def parse_bullet_tree(section: str) -> list[dict]:
    root: list[dict] = []
    stack: list[tuple[int, dict]] = []

    def level_for(line: str) -> tuple[int, str]:
        if line.startswith("• ") or line.startswith("o "):
            return 0, line[2:].strip()
        m = re.match(r"^(\s*)-\s+(.*)$", line)
        if m:
            indent = len(m.group(1).replace("\t", "    "))
            depth = indent // 2 + 1
            return depth, m.group(2).strip()
        m2 = re.match(r"^(\s+)°\s+(.*)$", line)
        if m2:
            indent = len(m2.group(1).replace("\t", "    "))
            depth = indent // 2 + 2
            return depth, m2.group(2).strip()
        return -1, line

    for raw in section.splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        lvl, text = level_for(line)
        if lvl < 0:
            continue
        node = {"text": re.sub(r"\s+", " ", text)}
        while stack and stack[-1][0] >= lvl:
            stack.pop()
        if not stack:
            root.append(node)
        else:
            parent = stack[-1][1]
            parent.setdefault("children", []).append(node)
        stack.append((lvl, node))
    return root


def letter_suffix(index: int) -> str:
    letters = string.ascii_lowercase
    if index < len(letters):
        return letters[index]
    return letters[index // len(letters) - 1] + letters[index % len(letters)]


def attach_ids(nodes: list[dict], prefix: str) -> list[dict]:
    out: list[dict] = []
    for i, node in enumerate(nodes):
        oid = f"{prefix}.{letter_suffix(i)}"
        entry: dict = {"id": oid, "text": node["text"]}
        if node.get("children"):
            entry["children"] = [
                {
                    "text": c["text"],
                    **(
                        {"children": [{"text": g["text"]} for g in c.get("children", [])]}
                        if c.get("children")
                        else {}
                    ),
                }
                for c in node["children"]
            ]
        out.append(entry)
    return out


def load_pages(pdf_path: Path) -> dict[int, str]:
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    return {i + 1: normalize(page.extract_text() or "") for i, page in enumerate(reader.pages)}


def build_blueprint(pdf_path: Path) -> dict:
    pages = load_pages(pdf_path)
    parsed: dict[str, dict] = {}

    for page_num, sections in sorted(PAGE_SECTIONS.items()):
        page_text = pages.get(page_num, "")
        if not page_text:
            raise ValueError(f"Missing PDF page {page_num}")
        for obj_id, start, end_before in sections:
            section_text = slice_section(page_text, start, end_before)
            bullets = parse_bullet_tree(section_text)
            parsed[obj_id] = {
                "id": obj_id,
                "text": OBJECTIVE_TEXT[obj_id],
                "children": attach_ids(bullets, obj_id),
            }

    for obj_id, text in OBJECTIVE_TEXT.items():
        if obj_id not in parsed:
            parsed[obj_id] = {"id": obj_id, "text": text, "children": []}

    domains_out = []
    for d in DOMAINS:
        major = d["id"].split(".")[0]
        objs = sorted(
            (parsed[oid] for oid in parsed if oid.startswith(major + ".")),
            key=lambda o: o["id"],
        )
        domains_out.append(
            {
                "id": d["id"],
                "title": d["title"],
                "weight": d["weight"],
                "objectives": objs,
            }
        )

    return {
        "exam": "SY0-701",
        "version": "701",
        "document_version_note": "CompTIA Security+ SY0-701 Certification Exam Objectives Version 5.0",
        "title": "CompTIA Security+",
        "certification": "Security+",
        "source_pdf": pdf_path.name,
        "source_pdf_url": "https://www.comptia.org/en-us/resources/security-plus-sy0-701-exam-objectives/",
        "domains": domains_out,
    }


def build_legacy_flat(blueprint: dict) -> dict:
    return {
        "exam": {
            "name": "CompTIA Security+",
            "code": "SY0-701",
            "version": "5.0",
            "duration_minutes": 90,
            "source_document": blueprint["source_pdf"],
        },
        "domains": [
            {
                "id": d["id"],
                "name": d["title"],
                "weight_percent": int(d["weight"].rstrip("%")),
                "objectives": [{"id": o["id"], "text": o["text"]} for o in d["objectives"]],
            }
            for d in blueprint["domains"]
        ],
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Build SY0-701 blueprint outline JSON from official PDF")
    ap.add_argument("--pdf", type=Path, default=DEFAULT_PDF, help="Path to official objectives PDF")
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--legacy-out", type=Path, default=LEGACY_OUT)
    args = ap.parse_args()

    if not args.pdf.is_file():
        raise SystemExit(f"PDF not found: {args.pdf}")

    blueprint = build_blueprint(args.pdf)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(blueprint, indent=2) + "\n", encoding="utf-8")
    args.legacy_out.write_text(json.dumps(build_legacy_flat(blueprint), indent=2) + "\n", encoding="utf-8")

    obj_count = sum(len(d["objectives"]) for d in blueprint["domains"])
    child_count = sum(
        len(o.get("children") or [])
        for d in blueprint["domains"]
        for o in d["objectives"]
    )
    print(
        f"[build-secplus-blueprint-sy0-701] {obj_count} objectives · "
        f"{child_count} top-level examples → {args.out.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
