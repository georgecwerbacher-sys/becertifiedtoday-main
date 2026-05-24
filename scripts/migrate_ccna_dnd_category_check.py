#!/usr/bin/env python3
"""Migrate CCNA_D_D CORRECT_GROUP pages to CcnaDndCategoryCheck.check/show."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DND_DIR = ROOT / "public" / "CCNA-Study" / "CCNA_D_D"

CHECK_START = re.compile(r'(\s*)checkBtn\.addEventListener\("click", function \(\) \{')
SHOW_START = re.compile(r'(\s*)showBtn\.addEventListener\("click", function \(\) \{')


def extract_js_string_literal(source: str, start: int) -> tuple[str, int] | None:
    if start >= len(source) or source[start] != '"':
        return None
    out: list[str] = []
    i = start + 1
    while i < len(source):
        ch = source[i]
        if ch == "\\" and i + 1 < len(source):
            out.append(source[i + 1])
            i += 2
            continue
        if ch == '"':
            return "".join(out), i + 1
        out.append(ch)
        i += 1
    return None


def handler_body(text: str, start_re: re.Pattern[str]) -> tuple[int, int, str, str] | None:
    m = start_re.search(text)
    if not m:
        return None
    indent = m.group(1)
    open_brace = text.find("{", m.end() - 1)
    if open_brace < 0:
        return None
    depth = 0
    i = open_brace
    while i < len(text):
        ch = text[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                if text[end : end + 2] == ");":
                    end += 2
                body = text[open_brace + 1 : i]
                return m.start(), end, indent, body
        i += 1
    return None


def parse_check_messages(body: str) -> tuple[str, str]:
    ternary = re.search(r"result\.textContent\s*=\s*(?:allOk|ok)\s*\?\s*", body)
    if ternary:
        pos = ternary.end()
        while pos < len(body) and body[pos].isspace():
            pos += 1
        ok_pair = extract_js_string_literal(body, pos)
        if not ok_pair:
            raise ValueError("could not parse ok message")
        ok_msg, after_ok = ok_pair
        colon = body.find(":", after_ok)
        if colon < 0:
            raise ValueError("could not parse fail message")
        pos = colon + 1
        while pos < len(body) and body[pos].isspace():
            pos += 1
        fail_pair = extract_js_string_literal(body, pos)
        if not fail_pair:
            raise ValueError("could not parse fail message")
        return ok_msg, fail_pair[0]

    early = re.search(
        r"if\s*\(\s*!allOk\s*\)\s*\{\s*result\.textContent\s*=\s*",
        body,
    )
    if early:
        fail_pair = extract_js_string_literal(body, early.end())
        if not fail_pair:
            raise ValueError("could not parse early fail message")
        fail_msg = fail_pair[0]
        ok_match = re.search(r"result\.textContent\s*=\s*", body[fail_pair[1] :])
        if not ok_match:
            raise ValueError("could not parse ok message after early fail")
        ok_start = fail_pair[1] + ok_match.end()
        ok_pair = extract_js_string_literal(body, ok_start)
        if not ok_pair:
            raise ValueError("could not parse ok message")
        return ok_pair[0], fail_msg

    raise ValueError("could not parse check messages")


def js_string(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def check_options(body: str) -> str:
    ok, fail = parse_check_messages(body)

    lines = [
        "CcnaDndCategoryCheck.check({",
        "    bank: bank,",
        "    allSlots: allSlots,",
        "    correctGroup: CORRECT_GROUP,",
        "    result: result,",
    ]

    if "MUST_BANK" in body:
        lines.extend(
            [
                "    requireEmptyBank: false,",
                "    mustBank: MUST_BANK,",
                "    tokenInBank: tokenInBank,",
            ]
        )
    elif "tokenInBank(UNUSED)" in body or "v === UNUSED" in body:
        lines.extend(
            [
                "    requireEmptyBank: false,",
                "    mustBank: [UNUSED],",
                "    tokenInBank: tokenInBank,",
            ]
        )

    lines.extend(
        [
            "    messages: {",
            f"      ok: {js_string(ok)},",
            f"      fail: {js_string(fail)}",
            "    }",
            "  });",
        ]
    )
    return "\n".join(lines)


def show_options(body: str) -> str:
    assigns = list(re.finditer(r"result\.textContent\s*=\s*", body))
    show_msg = "Answer shown."
    if assigns:
        parsed = extract_js_string_literal(body, assigns[-1].end())
        if parsed:
            show_msg = parsed[0]

    lines = [
        "clearPick();",
        "CcnaDndCategoryCheck.show({",
        "    bank: bank,",
        "    allSlots: allSlots,",
        "    correctGroup: CORRECT_GROUP,",
        "    takeFromBank: takeFromBank,",
        "    result: result,",
        f"    showMessage: {js_string(show_msg)}",
        "  });",
    ]
    return "\n".join(lines)


def remove_fill_order_var(text: str) -> str:
    text = re.sub(r"\n\s*var FILL_ORDER = \[[^\]]*\];", "", text)
    text = re.sub(r"\n\s*var fillOrder = \[[^\]]*\];", "", text)
    return text


def migrate_file(path: Path) -> bool:
    text = path.read_text()
    if "CORRECT_GROUP" not in text:
        return False
    if "CcnaDndCategoryCheck.check" in text:
        return False

    check = handler_body(text, CHECK_START)
    show = handler_body(text, SHOW_START)
    if not check or not show:
        raise ValueError(f"{path}: missing check/show handler")

    c_start, c_end, c_indent, c_body = check
    s_start, s_end, s_indent, s_body = show

    check_inner = check_options(c_body).replace("\n", "\n" + c_indent + "  ")
    show_inner = show_options(s_body).replace("\n", "\n" + s_indent + "  ")

    new_check = (
        f'{c_indent}checkBtn.addEventListener("click", function () {{\n'
        f"{c_indent}  {check_inner}\n"
        f"{c_indent}}});"
    )
    new_show = (
        f'{s_indent}showBtn.addEventListener("click", function () {{\n'
        f"{s_indent}  {show_inner}\n"
        f"{s_indent}}});"
    )

    text = text[:c_start] + new_check + text[c_end:s_start] + new_show + text[s_end:]
    text = remove_fill_order_var(text)
    path.write_text(text)
    return True


def main() -> None:
    changed = 0
    for path in sorted(DND_DIR.rglob("*.html")):
        if migrate_file(path):
            changed += 1
            print("migrated", path.relative_to(ROOT))
    print(f"done: {changed} files")


if __name__ == "__main__":
    main()
