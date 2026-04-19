#!/usr/bin/env python3
"""Normalize CLI modal/terminal CSS in public/cli-lab-*.html to match cli-lab-ebgp-neighbor-2."""

from __future__ import annotations

import re
from pathlib import Path

PUBLIC = Path(__file__).resolve().parent.parent / "public"

TERMINAL_STD = """    .terminal {
      font-family: "SF Mono", ui-monospace, Consolas, monospace;
      font-size: 0.88rem;
      background: #0a0d12;
      border: 1px solid #2a3344;
      border-radius: 10px;
      padding: 12px 12px 10px;
      min-height: 240px;
      display: flex;
      flex-direction: column;
      margin-top: 0;
    }"""

TERMINAL_HEAD = re.compile(
    r"    \.terminal \{\n"
    r"      font-family: \"SF Mono\", ui-monospace, Consolas, monospace;\n"
    r"      font-size: [^;\n]+;\n"
    r"      background: #0a0d12;\n"
    r"      border: 1px solid #2a3344;\n"
    r"      border-radius: 10px;\n"
    r"      padding: [^;\n]+;\n"
    r"      min-height: \d+px;\n"
    r"      display: flex;\n"
    r"      flex-direction: column;\n"
    r"(?:      margin-top: 0;\n)?"
    r"    \}\n"
    r"    ((?:#scrollback)|(?:\.console-scroll)) \{",
    re.MULTILINE,
)

SCROLL_MAIN = re.compile(
    r"(    (?:#scrollback|\.console-scroll) \{\n"
    r"      flex: 1;\n"
    r"      overflow-y: auto;\n"
    r"      )max-height: [^;\n]+;",
    re.MULTILINE,
)

RAPID_MODAL_SHRINK = """    .cli-modal-body .terminal {
      min-height: 0;
    }
    .cli-modal-body #scrollback {
      max-height: min(220px, 38vh);
    }
"""

OSPF_DR_BDR_LINE_OUT_OLD = """    .line-out {
      color: #cbd5e1;
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 0.88em;
      white-space: pre-wrap;
    }"""

OSPF_DR_BDR_LINE_OUT_NEW = """    .line-out {
      color: #cbd5e1;
      font-size: 0.9em;
      line-height: 1.45;
    }"""


def main() -> None:
    for path in sorted(PUBLIC.glob("cli-lab-*.html")):
        text = path.read_text(encoding="utf-8")
        orig = text

        text = text.replace(
            "max-height: min(85vh, 680px)", "max-height: min(85vh, 720px)"
        )
        text = text.replace(
            "max-height: min(85vh, 640px)", "max-height: min(85vh, 720px)"
        )
        text = text.replace(
            "width: min(460px, calc(100vw - 24px))",
            "width: min(520px, calc(100vw - 24px))",
        )
        text = text.replace(
            "width: min(440px, calc(100vw - 24px))",
            "width: min(520px, calc(100vw - 24px))",
        )

        if path.name == "cli-lab-rapid-pvst-lacp.html":
            text = text.replace(RAPID_MODAL_SHRINK, "")
            text = re.sub(
                r"    \.cli-modal-body #pc3Scrollback \{\n      max-height: min\(220px, 38vh\);\n    \}",
                "    .cli-modal-body #pc3Scrollback {\n      max-height: 360px;\n    }",
                text,
            )

        def _term_repl(m: re.Match[str]) -> str:
            return TERMINAL_STD + "\n    " + m.group(1) + " {"

        text, n_term = TERMINAL_HEAD.subn(_term_repl, text, count=1)
        text, n_scroll = SCROLL_MAIN.subn(r"\1max-height: 360px;", text)

        if path.name == "cli-lab-ospf-dr-bdr.html":
            text = text.replace(OSPF_DR_BDR_LINE_OUT_OLD, OSPF_DR_BDR_LINE_OUT_NEW)

        if text != orig:
            path.write_text(text, encoding="utf-8")
            print(f"{path.name}: wrote (terminal={n_term}, scroll_blocks={n_scroll})")
        else:
            print(f"{path.name}: unchanged")

        if n_term == 0:
            print(f"  WARNING: no main .terminal block matched in {path.name}")


if __name__ == "__main__":
    main()
