#!/usr/bin/env python3
"""Wire tryAppendIosHelp into lab submit handlers that lack IOS ? help."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"

SKIP_PARTS = {"Unused_Labs", "CCNA_Samples", "ENCOR_Samples"}

ROUTER_HELP_DOC = """
  IOS `?` help — ROUTER_CLI_HELP = null → DEFAULT_ROUTER_CLI_HELP (/js/cli-lab-container.js):
  tryAppendIosHelp(..., iosHelpOpts("router", promptText, ROUTER_CLI_HELP)) in every router submit handler.
  Help is read-only — using ? does not change config, advance steps, or affect completion.
  OSPF chain: router ?, router ospf ?, (config-router)# ?, router-id ?,
    (config-if)# ip ospf ?, ip ospf <pid> ?, ip ospf <pid> area ?, ip ospf priority ?"""

ROUTER_HELP_MARKER = "OSPF chain:"

ROUTER_VARS = """      /** null = DEFAULT_ROUTER_CLI_HELP (baseline for all routers). */
      var ROUTER_CLI_HELP = null;"""

SWITCH_VARS = """      /** null = DEFAULT_SWITCH_CLI_HELP (baseline for all switches). */
      var SWITCH_CLI_HELP = null;"""

# (path fragment, submit fn) -> device type
DEVICE_OVERRIDES: dict[tuple[str, str], str] = {
    ("cli-lab-named-acl-snoopimg.html", "submitSw2"): "router",
    ("cli-lab-nat-dhcp-sim.html", "submitSw"): "router",
    ("cli-lab-static-routing.html", "submitSw"): "router",
    ("cli-lab-static-routing.html", "submitSw2"): "router",
    ("cli-lab-static-routing.html", "submitSw3"): "router",
    ("ipv4_ipv6_assign.html", "submitSw"): "router",
    ("ipv4_ipv6_assign.html", "submitSw2"): "router",
    ("cli-lab-ip-services-sim-v2.html", "submitSw"): "router",
    ("cli-lab-ip-services-sim-v2.html", "submitR1"): "router",
    ("cli-lab-ip-services-sim-v2.html", "submitR3"): "router",
    ("cli-lab-ospf_config_sim_v3.html", "submitSw2"): "router",
}

SUBMIT_FN_RE = re.compile(r"function\s+(submit\w+)\s*\(\)\s*\{")


def should_skip(path: Path) -> bool:
    return any(part in SKIP_PARTS for part in path.parts)


def infer_device_type(rel: str, func_name: str) -> str | None:
    if "Pc" in func_name or func_name.lower() == "submitpc":
        return None
    key = (Path(rel).name, func_name)
    if key in DEVICE_OVERRIDES:
        return DEVICE_OVERRIDES[key]
    if re.match(r"submitR\d*$", func_name):
        return "router"
    return "switch"


def find_matching_brace(text: str, open_idx: int) -> int:
    depth = 0
    for i in range(open_idx, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return i
    return -1


def infer_scroll(func_name: str, file_text: str) -> str | None:
    m = re.match(r"submit(R|Sw)(\d+)$", func_name)
    if not m:
        return None
    kind, num = m.group(1), m.group(2)
    scroll = f"scroll{kind}{num}"
    if scroll in file_text:
        return scroll
    if kind == "Sw" and f"sw{num}Scrollback" in file_text:
        return f"sw{num}Scrollback"
    return None


def infer_append_fn(file_text: str, func_body: str, func_name: str) -> str | None:
    m = re.search(r"\b(append(?:Sw\d*|Sw\d+|R\d+|Sw))\(", func_body)
    if m:
        name = m.group(1)
        if re.search(rf"function\s+{re.escape(name)}\s*\(", file_text):
            return name
    for name in ("appendR1", "appendR3", "appendR2", "appendR10", "appendR20"):
        if re.search(rf"\b{re.escape(name)}\(", func_body):
            if re.search(rf"function\s+{re.escape(name)}\s*\(", file_text):
                return name
    scroll = infer_scroll(func_name, file_text)
    if not scroll:
        return None
    if "appendBlock" in file_text:
        return f"function (cls, text) {{ appendBlock({scroll}, cls, text); }}"
    if "appendLine" in file_text:
        return f"function (cls, text) {{ appendLine({scroll}, cls, text); }}"
    return None


def infer_prompt(func_body: str, func_name: str, file_text: str) -> str:
    if re.search(r"\bpromptText\b", func_body):
        return "promptText"
    m = re.search(r"const prompt = ([^;]+);", func_body)
    if m:
        return m.group(1).strip()
    m = re.match(r"submit(R|Sw)(\d+)$", func_name)
    if m:
        kind, num = m.group(1), m.group(2)
        pn = f"prompt{kind}{num}"
        if pn in file_text:
            return f"{pn}.textContent"
    if "sw10PromptEl" in func_body or "sw10PromptEl" in file_text:
        return "sw10PromptEl.textContent"
    return "promptText"


def find_insert_pos(func_body: str) -> int | None:
    patterns = [
        r"if\s*\(\s*!line\.trim\(\)\s*\)\s*\{\s*\n\s*\w+\.value\s*=\s*[\"'][^\"']*[\"'];\s*\n\s*return;\s*\n\s*\}",
        r"if\s*\(\s*!line\.trim\(\)\s*\)\s*return;",
        r"if\s*\(\s*!trimmed\s*\)\s*return;",
        r"if\s*\(\s*!lineSave\.trim\(\)\s*\)\s*return;",
    ]
    for pat in patterns:
        m = re.search(pat, func_body)
        if m:
            return m.end()
    # Only fall back to first `var line =` at the start of a line (avoid mid-string matches).
    m = re.search(r"(?:^|\n)\s*(?:const|var)\s+line\s*=[^;]+;", func_body)
    if m:
        tail = func_body[m.end() :]
        if re.match(r"\s*\n", tail):
            return m.end()
    return None


def ensure_help_vars(text: str, need_router: bool, need_switch: bool) -> str:
    if need_router and "ROUTER_CLI_HELP" not in text:
        anchor = "cliLabContainer.CLI_HELP_UNAVAILABLE_MSG"
        if anchor in text:
            text = text.replace(
                anchor,
                anchor + "\n" + ROUTER_VARS,
                1,
            )
        elif "cli-lab-container.js" in text and "<script>" in text:
            text = text.replace(
                "<script>",
                "<script>\n" + ROUTER_VARS + "\n",
                1,
            )
    if need_switch and "SWITCH_CLI_HELP" not in text:
        if "ROUTER_CLI_HELP" in text and "SWITCH_CLI_HELP" not in text:
            text = text.replace(ROUTER_VARS, ROUTER_VARS + "\n" + SWITCH_VARS, 1)
        elif "SWITCH_CLI_HELP" not in text:
            anchor = "cliLabContainer.CLI_HELP_UNAVAILABLE_MSG"
            if anchor in text:
                text = text.replace(anchor, anchor + "\n" + SWITCH_VARS, 1)
    return text


def patch_router_help_doc(path: Path) -> bool:
    """Add OSPF router help doc block to lab HTML header when missing."""
    text = path.read_text(encoding="utf-8")
    if 'iosHelpOpts("router"' not in text:
        return False
    if ROUTER_HELP_MARKER in text:
        return False
    m = re.search(r"<!--([\s\S]*?)-->", text)
    if not m:
        return False
    insert = ROUTER_HELP_DOC + "\n"
    new_text = text[: m.end(1)] + insert + text[m.end(1) :]
    path.write_text(new_text, encoding="utf-8")
    return True


def patch_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if "cli-lab-container.js" not in text:
        return []
    if "tryAppendIosHelp" in text and not re.search(
        r"function\s+submit\w+\s*\(\)\s*\{[^}]*\}(?!.*tryAppendIosHelp)", text, re.S
    ):
        # Still patch individual submit fns missing help
        pass

    rel = str(path.relative_to(ROOT))
    changes: list[str] = []
    need_router = False
    need_switch = False
    offset = 0
    original = text

    for m in SUBMIT_FN_RE.finditer(text):
        func_name = m.group(1)
        device = infer_device_type(rel, func_name)
        if not device:
            continue
        open_brace = m.end() - 1
        close_brace = find_matching_brace(text, open_brace)
        if close_brace < 0:
            continue
        func_body = text[open_brace : close_brace + 1]
        if "tryAppendIosHelp" in func_body:
            continue

        append_fn = infer_append_fn(text, func_body, func_name)
        if not append_fn:
            continue
        insert_at = find_insert_pos(func_body)
        if insert_at is None:
            continue

        prompt = infer_prompt(func_body, func_name, text)
        help_var = "ROUTER_CLI_HELP" if device == "router" else "SWITCH_CLI_HELP"
        snippet = (
            f'\n        if (cliLabContainer.tryAppendIosHelp(line, {append_fn}, '
            f'cliLabContainer.iosHelpOpts("{device}", {prompt}, {help_var}))) return;'
        )

        abs_insert = open_brace + insert_at + offset
        text = text[:abs_insert] + snippet + text[abs_insert:]
        offset += len(snippet)
        changes.append(func_name)
        if device == "router":
            need_router = True
        else:
            need_switch = True

    if changes:
        text = ensure_help_vars(text, need_router, need_switch)
        path.write_text(text, encoding="utf-8")

    return changes


def main() -> int:
    patched: list[str] = []
    doc_patched: list[str] = []
    for path in sorted(PUBLIC.rglob("*.html")):
        if should_skip(path):
            continue
        funcs = patch_file(path)
        if funcs:
            rel = path.relative_to(ROOT)
            patched.append(f"{rel}: {', '.join(funcs)}")
        if patch_router_help_doc(path):
            doc_patched.append(str(path.relative_to(ROOT)))
    print(f"Patched {len(patched)} lab file(s) with tryAppendIosHelp:")
    for line in patched:
        print(f"  {line}")
    print(f"Added router OSPF help docs to {len(doc_patched)} file(s):")
    for line in doc_patched:
        print(f"  {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
