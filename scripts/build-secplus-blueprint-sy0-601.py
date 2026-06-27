#!/usr/bin/env python3
"""Build secplus-blueprint-sy0-601.json from the official CompTIA objectives PDF."""
from __future__ import annotations

import argparse
import json
import re
import string
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PDF = Path.home() / "Desktop/comptia-security-sy0-601-exam-objectives-(2-0).pdf"
OUT = ROOT / "public/COMP_TIA_SEC+/data/secplus-blueprint-sy0-601.json"
LEGACY_OUT = ROOT / "public/COMP_TIA_SEC+/data/secplus-exam-objectives-sy0-601.json"

DOMAINS = [
    {"id": "1.0", "title": "Attacks, Threats, and Vulnerabilities", "weight": "24%"},
    {"id": "2.0", "title": "Architecture and Design", "weight": "21%"},
    {"id": "3.0", "title": "Implementation", "weight": "25%"},
    {"id": "4.0", "title": "Operations and Incident Response", "weight": "16%"},
    {"id": "5.0", "title": "Governance, Risk, and Compliance", "weight": "14%"},
]

# Objective statements from CompTIA SY0-601 exam objectives PDF (v2.0 file / v3.0 document body).
OBJECTIVE_TEXT: dict[str, str] = {
    "1.1": "Compare and contrast different types of social engineering techniques.",
    "1.2": "Given a scenario, analyze potential indicators to determine the type of attack.",
    "1.3": "Given a scenario, analyze potential indicators associated with application attacks.",
    "1.4": "Given a scenario, analyze potential indicators associated with network attacks.",
    "1.5": "Explain different threat actors, vectors, and intelligence sources.",
    "1.6": "Explain the security concerns associated with various types of vulnerabilities.",
    "1.7": "Summarize the techniques used in security assessments.",
    "1.8": "Explain the techniques used in penetration testing.",
    "2.1": "Explain the importance of security concepts in an enterprise environment.",
    "2.2": "Summarize virtualization and cloud computing concepts.",
    "2.3": "Summarize secure application development, deployment, and automation concepts.",
    "2.4": "Summarize authentication and authorization design concepts.",
    "2.5": "Given a scenario, implement cybersecurity resilience.",
    "2.6": "Explain the security implications of embedded and specialized systems.",
    "2.7": "Explain the importance of physical security controls.",
    "2.8": "Summarize the basics of cryptographic concepts.",
    "3.1": "Given a scenario, implement secure protocols.",
    "3.2": "Given a scenario, implement host or application security solutions.",
    "3.3": "Given a scenario, implement secure network designs.",
    "3.4": "Given a scenario, install and configure wireless security settings.",
    "3.5": "Given a scenario, implement secure mobile solutions.",
    "3.6": "Given a scenario, apply cybersecurity solutions to the cloud.",
    "3.7": "Given a scenario, implement identity and account management controls.",
    "3.8": "Given a scenario, implement authentication and authorization solutions.",
    "3.9": "Given a scenario, implement public key infrastructure.",
    "4.1": "Given a scenario, use the appropriate tool to assess organizational security.",
    "4.2": "Summarize the importance of policies, processes, and procedures for incident response.",
    "4.3": "Given an incident, utilize appropriate data sources to support an investigation.",
    "4.4": "Given an incident, apply mitigation techniques or controls to secure an environment.",
    "4.5": "Explain the key aspects of digital forensics.",
    "5.1": "Compare and contrast various types of controls.",
    "5.2": "Explain the importance of applicable regulations, standards, or frameworks that impact organizational security posture.",
    "5.3": "Explain the importance of policies to organizational security.",
    "5.4": "Summarize risk management processes and concepts.",
    "5.5": "Explain privacy and sensitive data concepts in relation to security.",
}

# Per PDF page (1-based): objective id, optional start marker, optional end_before marker.
PAGE_SECTIONS: dict[int, list[tuple[str, str | None, str | None]]] = {
    4: [
        ("1.1", "• Phishing", "• Malware"),
        ("1.2", "• Malware", None),
    ],
    5: [
        ("1.3", "• Privilege escalation", "• Wireless"),
        ("1.4", "• Wireless", None),
    ],
    6: [
        ("1.6", "• Cloud-based", "• Actors and threats"),
        ("1.5", "• Actors and threats", None),
    ],
    7: [
        ("1.8", "• Penetration testing", "• Vulnerability scans"),
        ("1.7", "• Vulnerability scans", None),
    ],
    8: [
        ("2.1", "• Configuration management", "• Cloud models"),
        ("2.2", "• Cloud models", None),
    ],
    9: [
        ("2.3", "• Environment", "• Authentication methods"),
        ("2.4", "• Authentication methods", None),
    ],
    10: [
        ("2.5", "• Redundancy", "• Embedded systems"),
        ("2.6", "• Embedded systems", None),
    ],
    11: [
        ("2.7", "• Bollards/barricades", "• Digital signatures"),
        ("2.8", "• Digital signatures", None),
    ],
    12: [
        ("3.1", "• Protocols", "• Endpoint protection"),
        ("3.2", "• Endpoint protection", None),
    ],
    13: [
        ("3.3", "• Load balancing", "• Cryptographic protocols"),
        ("3.4", "• Cryptographic protocols", None),
    ],
    14: [
        ("3.5", "• Connection methods and receivers", "• Cloud security controls"),
        ("3.6", "• Cloud security controls", None),
    ],
    15: [
        ("3.7", "• Identity", "• Authentication/authorization"),
        ("3.8", "• Authentication/authorization", "• Public key infrastructure (PKI)"),
        ("3.9", "• Public key infrastructure (PKI)", None),
    ],
    16: [
        ("4.1", "• Network reconnaissance and discovery", "• Incident response plans"),
        ("4.2", "• Incident response plans", None),
    ],
    17: [
        ("4.3", "• Vulnerability scan output", "• Reconfigure endpoint security solutions"),
        ("4.4", "• Reconfigure endpoint security solutions", "• Documentation/evidence"),
        ("4.5", "• Documentation/evidence", None),
    ],
    18: [
        ("5.1", "• Category", "• Regulations, standards, and legislation"),
        ("5.2", "• Regulations, standards, and legislation", "• Personnel"),
        ("5.3", "• Personnel", None),
    ],
    19: [
        ("5.4", "• Risk types", "• Organizational consequences"),
        ("5.5", "• Organizational consequences", None),
    ],
}


def normalize(text: str) -> str:
    text = text.replace("\u2022", "•").replace("\uf0b7", "•")
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
    # Drop footer noise
    text = re.split(r"CompTIA Security\+ Certification Exam Objectives", text)[0]
    text = re.sub(r"^\d\.\d+\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\d\.0 .+$", "", text, flags=re.MULTILINE)
    return text.strip()


def parse_bullet_tree(section: str) -> list[dict]:
    root: list[dict] = []
    stack: list[tuple[int, dict]] = []

    def level_for(line: str) -> tuple[int, str]:
        if line.startswith("• "):
            return 0, line[2:].strip()
        m = re.match(r"^(\s*)-\s+(.*)$", line)
        if m:
            indent = len(m.group(1).replace("\t", "    "))
            depth = indent // 2 + 1
            return depth, m.group(2).strip()
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
                {"text": c["text"], **({"children": [{"text": g["text"]} for g in c.get("children", [])]} if c.get("children") else {})}
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
    by_domain: dict[str, list[dict]] = {d["id"]: [] for d in DOMAINS}

    for page_num, sections in sorted(PAGE_SECTIONS.items()):
        page_text = pages.get(page_num, "")
        if not page_text:
            raise ValueError(f"Missing PDF page {page_num}")
        for obj_id, start, end_before in sections:
            major = obj_id.split(".")[0] + ".0"
            section_text = slice_section(page_text, start, end_before)
            bullets = parse_bullet_tree(section_text)
            by_domain[major].append(
                {
                    "id": obj_id,
                    "text": OBJECTIVE_TEXT[obj_id],
                    "children": attach_ids(bullets, obj_id),
                }
            )

    domains_out = []
    for d in DOMAINS:
        objs = sorted(by_domain[d["id"]], key=lambda o: o["id"])
        domains_out.append(
            {
                "id": d["id"],
                "title": d["title"],
                "weight": d["weight"],
                "objectives": objs,
            }
        )

    return {
        "exam": "SY0-601",
        "version": "v2.0",
        "document_version_note": "PDF body lists Exam Objectives Version 3.0; filename is (2-0).",
        "title": "CompTIA Security+",
        "certification": "Security+",
        "source_pdf": pdf_path.name,
        "source_pdf_url": "https://comptiacdn.azureedge.net/webcontent/docs/default-source/exam-objectives/comptia-security-sy0-601-exam-objectives-(2-0).pdf",
        "retired": "2024-07-31",
        "successor_exam": "SY0-701",
        "domains": domains_out,
    }


def build_legacy_flat(blueprint: dict) -> dict:
    return {
        "exam": {
            "name": "CompTIA Security+",
            "code": "SY0-601",
            "version": "2.0",
            "retired": "2024-07-31",
            "duration_minutes": 90,
            "source_document": blueprint["source_pdf"],
            "source_url": blueprint.get("source_pdf_url"),
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
    ap = argparse.ArgumentParser(description="Build SY0-601 blueprint outline JSON from official PDF")
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
        f"[build-secplus-blueprint-sy0-601] {obj_count} objectives · "
        f"{child_count} top-level examples → {args.out.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
