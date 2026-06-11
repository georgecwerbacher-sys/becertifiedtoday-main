#!/usr/bin/env python3
"""Interactive physical-layer questionnaire for CLI lab authoring.

Usage:
  python3 scripts/cli_lab_build_wizard.py
  python3 scripts/cli_lab_build_wizard.py --slug cli-lab-my-lab

Writes: data/lab-builds/{slug}-physical.json
Question source: templates/lab-build/lab-build-questionnaire-physical.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONNAIRE = ROOT / "templates" / "lab-build" / "lab-build-questionnaire-physical.json"
OUTPUT_DIR = ROOT / "data" / "lab-builds"

ROUTER_IFACES = ["Ethernet0/0", "Ethernet0/1", "Ethernet0/2", "Ethernet0/3", "Serial0/0/0", "Serial0/0/1"]
SWITCH_IFACES = ["Ethernet0/0", "Ethernet0/1", "Ethernet0/2", "Ethernet0/3"]


def load_questionnaire() -> dict:
    with QUESTIONNAIRE.open(encoding="utf-8") as f:
        return json.load(f)


def prompt_text(label: str, required: bool = True, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    while True:
        raw = input(f"{label}{suffix}: ").strip()
        if not raw and default is not None:
            return default
        if raw or not required:
            return raw
        print("  (required)")


def prompt_choice(label: str, options: list[str], default: str | None = None) -> str:
    print(f"\n{label}")
    for i, opt in enumerate(options, 1):
        mark = " (default)" if opt == default else ""
        print(f"  {i}. {opt}{mark}")
    while True:
        raw = input("Choice (number or text): ").strip()
        if not raw and default:
            return default
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(options):
                return options[idx]
        if raw in options:
            return raw
        print("  Invalid choice — try again.")


def prompt_number(label: str, minimum: int = 0, default: int | None = None) -> int:
    while True:
        raw = input(f"{label} [{default}]: " if default is not None else f"{label}: ").strip()
        if not raw and default is not None:
            return default
        try:
            val = int(raw)
            if val >= minimum:
                return val
        except ValueError:
            pass
        print(f"  Enter an integer >= {minimum}")


def collect_devices(count: int) -> list[dict]:
    roles = ["router", "switch", "wlc", "ap", "pc", "server"]
    devices: list[dict] = []
    print(f"\n--- Device inventory ({count} IOS/network devices) ---")
    for i in range(count):
        print(f"\nDevice {i + 1}/{count}")
        hostname = prompt_text("  Hostname")
        print("  Role:", ", ".join(f"{j+1}={r}" for j, r in enumerate(roles)))
        role = prompt_choice("  Select role", roles)
        notes = prompt_text("  Notes (optional)", required=False)
        devices.append({"hostname": hostname, "role": role, "notes": notes or None})
    return devices


def collect_links() -> list[dict]:
    links: list[dict] = []
    cable_types = [
        "straight-through",
        "crossover",
        "serial_dce",
        "serial_dte",
        "fiber",
        "wireless",
        "console",
    ]
    print("\n--- Physical links (empty hostname to finish) ---")
    while True:
        from_dev = prompt_text("  From device (blank to done)", required=False)
        if not from_dev:
            break
        from_if = prompt_text("  From interface")
        to_dev = prompt_text("  To device")
        to_if = prompt_text("  To interface")
        cable = prompt_choice("  Cable type", cable_types)
        links.append(
            {
                "from": {"device": from_dev, "interface": from_if},
                "to": {"device": to_dev, "interface": to_if},
                "cableType": cable,
            }
        )
    if not links:
        print("  Warning: no links entered.")
    return links


def collect_interface_states(devices: list[dict], links: list[dict]) -> list[dict]:
    used: set[tuple[str, str]] = set()
    for link in links:
        used.add((link["from"]["device"], link["from"]["interface"]))
        used.add((link["to"]["device"], link["to"]["interface"]))

    hostnames = {d["hostname"] for d in devices}
    missing = [(d, i) for d, i in sorted(used) if d in hostnames]
    if not missing:
        print("\n--- Interface states (no links listed; enter manually) ---")
        while True:
            dev = prompt_text("  Device (blank to done)", required=False)
            if not dev:
                break
            iface = prompt_text("  Interface")
            missing.append((dev, iface))

    states: list[dict] = []
    print("\n--- Initial interface status for used ports ---")
    for dev, iface in missing:
        print(f"\n  {dev} {iface}")
        admin = prompt_choice("    Admin status", ["up", "down"], default="up")
        protocol = prompt_choice("    Line protocol", ["up", "down"], default="up")
        notes = prompt_text("    Notes (optional)", required=False)
        states.append(
            {
                "device": dev,
                "interface": iface,
                "adminStatus": admin,
                "protocolStatus": protocol,
                "notes": notes or None,
            }
        )
    return states


def interface_inventory(devices: list[dict], router_tpl: str, switch_tpl: str) -> dict[str, list[str]]:
    inv: dict[str, list[str]] = {}
    for d in devices:
        role = d["role"]
        if role == "router":
            inv[d["hostname"]] = list(ROUTER_IFACES) if router_tpl == "standard_4eth_2serial" else []
        elif role == "switch":
            inv[d["hostname"]] = list(SWITCH_IFACES) if switch_tpl == "standard_4eth" else []
        else:
            inv[d["hostname"]] = []
    return inv


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s or "cli-lab-untitled"


def run_wizard(preset_slug: str | None = None) -> Path:
    q = load_questionnaire()
    print("=" * 72)
    print(q["title"])
    print(q["description"])
    print("=" * 72)

    track = prompt_choice("Track", q["sections"][0]["questions"][0]["options"])
    slug = preset_slug or prompt_text("Lab slug (cli-lab-...)")
    if not slug.startswith("cli-lab-"):
        slug = f"cli-lab-{slugify(slug)}"
    title = prompt_text("Lab display title")
    objective = prompt_text("One-sentence objective")

    device_count = prompt_number("Number of routers/switches/WLC/AP in topology", minimum=1)
    devices = collect_devices(device_count)
    pc_count = prompt_number("Number of PC/server CLI hosts", minimum=0, default=0)

    router_tpl = prompt_choice(
        "Router interface template",
        ["standard_4eth_2serial", "custom"],
        default="standard_4eth_2serial",
    )
    switch_tpl = prompt_choice(
        "Switch interface template",
        ["standard_4eth", "custom"],
        default="standard_4eth",
    )
    custom_ifaces = prompt_text("Custom interface notes (if any)", required=False)

    links = collect_links()
    topo = prompt_choice(
        "Topology diagram",
        ["new_image_needed", "reuse_existing", "text_only_no_diagram"],
    )
    topo_path = ""
    if topo == "reuse_existing":
        topo_path = prompt_text("Existing image path under public/")

    iface_states = collect_interface_states(devices, links)
    speed_duplex = prompt_text("Speed/duplex notes (optional)", required=False)
    physical_faults = prompt_text("Physical faults in scenario (optional)", required=False)

    spec = {
        "schemaVersion": q["schemaVersion"],
        "phase": q["phase"],
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "meta": {
            "track": track,
            "slug": slug,
            "title": title,
            "objective": objective,
            "outputHtml": {
                "CCNA": f"public/CCNA-Study/CCNA_labs/{slug}.html",
                "ENCOR": f"public/CCNP-ENCOR-Study/CCNP-ENCOR-Labs/{slug}.html",
            }[track],
        },
        "inventory": {
            "devices": devices,
            "pcCount": pc_count,
            "interfaceInventory": interface_inventory(devices, router_tpl, switch_tpl),
            "routerInterfaceTemplate": router_tpl,
            "switchInterfaceTemplate": switch_tpl,
            "customInterfaceNotes": custom_ifaces or None,
        },
        "cabling": {
            "links": links,
            "topologyDiagram": topo,
            "topologyImagePath": topo_path or None,
        },
        "physicalState": {
            "interfaceStates": iface_states,
            "speedDuplex": speed_duplex or None,
            "physicalFaults": physical_faults or None,
        },
        "nextPhase": "L2/L3 tasks and LAB_STEPS grading (not collected in Phase 1)",
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUTPUT_DIR / f"{slug}-physical.json"
    with out.open("w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)
        f.write("\n")

    print("\n" + "=" * 72)
    print(f"Saved physical-layer spec: {out.relative_to(ROOT)}")
    print(f"Devices: {', '.join(d['hostname'] for d in devices)}")
    print(f"Links: {len(links)}")
    print("Next: Phase 2 — VLANs, IP addressing, lab tasks, and grading steps.")
    print("=" * 72)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="CLI lab physical-layer build wizard")
    parser.add_argument("--slug", help="Preset lab slug (cli-lab-...)")
    args = parser.parse_args()
    try:
        run_wizard(args.slug)
    except (KeyboardInterrupt, EOFError):
        print("\nCancelled.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
