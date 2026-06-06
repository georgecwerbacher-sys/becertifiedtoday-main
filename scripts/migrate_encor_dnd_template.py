#!/usr/bin/env python3
"""Migrate ENCOR drag-and-drop pages to the light SEC+-style shell."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DND_DIR = ROOT / "public" / "CCNP-ENCOR-Study" / "CCNP-ENCOR-Drag-Drop"
SAMPLE_DND_FILES = (
    ROOT / "public" / "CCNP-ENCOR-Study" / "ENCOR_Samples" / "question-365.html",
)
LOGO_IMG = "/images/logo/becertifiedtoday_logo_image_trans.png"
PORTAL_HOME = "/CCNP-ENCOR-Study/ENCOR_Training_Portal.html"
SAMPLE_HOME = "/ccnp-home.html"

KEEP_CSS_KEYWORDS = (
    "exhibit",
    "cli-",
    "topology",
    "figure",
    "route-exhibit",
    "code-exhibit",
    "debug-exhibit",
    "image-wrap",
    "visually-hidden",
    "code-wrap",
    "exhibit-light",
    "exhibit-region",
    "exhibit-hint",
)

TOUCH_HINT = (
    '    <p class="dragdrop-touch-hint" aria-hidden="true">'
    "On a phone or tablet, tap a chip to pick it up, then tap a drop zone "
    "(or another chip to swap).</p>"
)

WATERMARK = f"""  <div class="page-logo-watermark" aria-hidden="true">
    <img src="{LOGO_IMG}" alt="" />
  </div>"""

REQUIRED_STYLESHEETS = (
    "/css/bcc-question-link-nav.css",
    "/CCNP-ENCOR-Study/ENCOR_Samples/encor-sample-touch.css",
    "/CCNP-ENCOR-Study/js/encor-dnd-page.css",
)

BUTTON_BY_ID_RE = {
    "checkBtn": re.compile(r'<button id="checkBtn"[^>]*>.*?</button>', re.I | re.S),
    "resetBtn": re.compile(r'<button id="resetBtn"[^>]*>.*?</button>', re.I | re.S),
    "showBtn": re.compile(r'<button id="showBtn"[^>]*>.*?</button>', re.I | re.S),
}


def is_broken_layout_wrap(text: str) -> bool:
    return bool(
        re.search(
            r'<div id="bank"[^>]*>\s*<div class="token"[^>]*>[\s\S]*?</div>\s*</div>\s*<div class="token"',
            text,
            re.I,
        )
    )


def needs_migration(text: str) -> bool:
    if "encor-dnd-page.css" not in text or "question-shell" not in text:
        return True
    if "home-key" in text:
        return True
    if re.search(r"background:\s*#0b1020", text, re.I):
        return True
    return is_broken_layout_wrap(text)


def extract_head_extras(text: str) -> str:
    bits: list[str] = []
    for pat in (
        r'<link rel="canonical"[^>]+>',
        r'<meta name="description"[^>]+>',
    ):
        m = re.search(pat, text, re.I)
        if m:
            bits.append("  " + m.group(0))
    return "\n".join(bits)


def extract_title(text: str) -> str:
    m = re.search(r"<title>(.*?)</title>", text, re.S | re.I)
    return m.group(1).strip() if m else "ENCOR drag and drop"


def extract_first_style(text: str) -> str:
    m = re.search(r"<style>(.*?)</style>", text, re.S | re.I)
    return m.group(1) if m else ""


def extract_exhibit_css(style_text: str) -> str:
    if not style_text.strip():
        return ""
    kept: list[str] = []
    for sel, body in re.findall(r"([^{]+)\{([^}]*)\}", style_text, re.S):
        sl = sel.lower()
        if not any(k in sl for k in KEEP_CSS_KEYWORDS):
            continue
        kept.append(f"    {sel.strip()} {{\n{body.strip()}\n    }}")
    if not kept:
        return ""
    return "  <style>\n" + "\n".join(kept) + "\n  </style>"


def extract_main_inner(text: str) -> str:
    m = re.search(r'<main class="card">(.*?)</main>', text, re.S | re.I)
    if not m:
        raise ValueError("missing main.card")
    return m.group(1).strip()


def find_matching_div_close(text: str, open_start: int) -> int:
    gt = text.find(">", open_start)
    if gt < 0:
        return -1
    i = gt + 1
    depth = 1
    while i < len(text) and depth > 0:
        next_open = text.find("<div", i)
        next_close = text.find("</div>", i)
        if next_close < 0:
            return -1
        if next_open >= 0 and next_open < next_close:
            depth += 1
            i = next_open + 4
            continue
        depth -= 1
        end = next_close + len("</div>")
        if depth == 0:
            return end
        i = end
    return -1


def unwrap_sim_frame(main: str) -> str:
    if 'class="sim-frame"' not in main:
        return main
    main = re.sub(r'<div class="sim-frame">\s*', "", main, count=1, flags=re.I)
    main = re.sub(
        r"</div>\s*(?=<div class=\"actions\")",
        "",
        main,
        count=1,
        flags=re.I,
    )
    return main


def wrap_layout_in_sim_frame(main: str) -> str:
    main = unwrap_sim_frame(main)
    m = re.search(r'<div class="layout"[^>]*>', main, re.I)
    if not m:
        return main
    end = find_matching_div_close(main, m.start())
    if end < 0:
        return main
    layout = main[m.start() : end]
    if "dnd-split" not in layout:
        layout = re.sub(r'<div class="layout"', '<div class="layout dnd-split"', layout, count=1, flags=re.I)
    return main[: m.start()] + f'<div class="sim-frame">\n{layout}\n</div>' + main[end:]


def collect_row_blocks(main: str) -> tuple[int, int, list[str]] | None:
    pos = 0
    rows: list[str] = []
    first_start = -1
    last_end = 0
    while pos < len(main):
        m = re.search(r'<div class="row">', main[pos:], re.I)
        if not m:
            break
        start = pos + m.start()
        end = find_matching_div_close(main, start)
        if end < 0:
            break
        if first_start < 0:
            first_start = start
        rows.append(main[start:end])
        last_end = end
        pos = end
    if not rows or first_start < 0:
        return None
    return first_start, last_end, rows


def extract_bank_block(main: str, start_pos: int) -> tuple[str, int] | None:
    tail = main[start_pos:]
    wrap_m = re.search(r'<div class="bank-wrap">\s*<div id="bank"', tail, re.I)
    if wrap_m:
        wrap_start = start_pos + wrap_m.start()
        wrap_end = find_matching_div_close(main, wrap_start)
        if wrap_end < 0:
            return None
        bank_start = main.find('<div id="bank"', wrap_start)
        bank_end = find_matching_div_close(main, bank_start)
        if bank_end < 0:
            return None
        return main[bank_start:bank_end], wrap_end
    bank_m = re.search(r'<div id="bank"', tail, re.I)
    if not bank_m:
        return None
    bank_start = start_pos + bank_m.start()
    bank_end = find_matching_div_close(main, bank_start)
    if bank_end < 0:
        return None
    return main[bank_start:bank_end], bank_end


def build_split_block(*, solution_html: str, bank_html: str) -> str:
    return (
        '<div class="sim-frame">\n'
        '<div class="layout dnd-split">\n'
        '      <div class="panel panel--solution">\n'
        f"{solution_html}\n"
        '      </div>\n'
        '      <div class="panel panel--choices">\n'
        '        <h2>Choices</h2>\n'
        f"        {bank_html}\n"
        '      </div>\n'
        '</div>\n'
        '</div>'
    )


def wrap_row_bank_split(main: str) -> str:
    """Side-by-side: match rows (solution) left, token bank right."""
    if 'class="row-list"' in main and "drop-slot" in main:
        return main
    collected = collect_row_blocks(main)
    if not collected:
        return main
    first_start, last_end, rows = collected
    bank_result = extract_bank_block(main, last_end)
    if not bank_result:
        return main
    bank_html, bank_end = bank_result
    rows_inner = "\n".join(f"          {row.strip()}" for row in rows)
    solution_html = f"        <div class=\"row-list\">\n{rows_inner}\n        </div>"
    block = build_split_block(solution_html=solution_html, bank_html=bank_html.strip())
    return main[:first_start] + block + main[bank_end:]


def wrap_code_bank_split(main: str) -> str:
    """Side-by-side: code/script panel left, token bank right."""
    if re.search(r'class="layout"', main, re.I) and "panel--solution" in main:
        return main
    code_m = re.search(r'<div class="code-wrap">', main, re.I)
    if not code_m:
        return main
    code_end = find_matching_div_close(main, code_m.start())
    if code_end < 0:
        return main
    bank_result = extract_bank_block(main, code_end)
    if not bank_result:
        return main
    bank_html, bank_end = bank_result
    solution_html = f"        {main[code_m.start():code_end].strip()}"
    block = build_split_block(solution_html=solution_html, bank_html=bank_html.strip())
    return main[: code_m.start()] + block + main[bank_end:]


def add_touch_hint(main: str) -> str:
    if "dragdrop-touch-hint" in main:
        return main
    m = re.search(r"(<h1[^>]*>)", main, re.I)
    if not m:
        return TOUCH_HINT + "\n" + main
    return main[: m.start()] + TOUCH_HINT + "\n\n" + main[m.start() :]


def extract_tail(text: str) -> str:
    m = re.search(r"</main>([\s\S]*)</body>", text, re.I)
    return m.group(1).strip() if m else ""


def strip_home_key(tail: str) -> str:
    tail = re.sub(r"<style>[\s\S]*?\.home-key[\s\S]*?</style>\s*", "", tail, flags=re.I)
    tail = re.sub(r'<a class="home-key"[^>]*>.*?</a>\s*', "", tail, flags=re.I)
    return tail.strip()


def normalize_actions(text: str) -> str:
    """Template order: Check Answer · Reset · Show Answer (optional) · result · nextWrap."""

    m = re.search(r'<div class="actions">(.*?)</div>', text, re.I | re.S)
    if not m:
        return text
    block = m.group(1)
    check = BUTTON_BY_ID_RE["checkBtn"].search(block)
    reset = BUTTON_BY_ID_RE["resetBtn"].search(block)
    show = BUTTON_BY_ID_RE["showBtn"].search(block)
    result = re.search(r'<span id="result"[^>]*></span>', block, re.I | re.S)
    next_wrap = re.search(r'<span id="nextWrap"[^>]*>[\s\S]*?</span>', block, re.I | re.S)
    if not check:
        return text
    parts = ["<div class=\"actions\">", f"      {check.group(0).strip()}"]
    if reset:
        parts.append(f"      {reset.group(0).strip()}")
    if show:
        parts.append(f"      {show.group(0).strip()}")
    if result:
        parts.append(f"      {result.group(0).strip()}")
    if next_wrap:
        parts.append(f"      {next_wrap.group(0).strip()}")
    parts.append("    </div>")
    replacement = "\n".join(parts)
    return text[: m.start()] + replacement + text[m.end() :]


def ensure_stylesheets(text: str) -> str:
    for href in REQUIRED_STYLESHEETS:
        if href not in text:
            text = text.replace("</head>", f'  <link rel="stylesheet" href="{href}" />\n</head>', 1)
    return text


def ensure_body_classes(text: str, *, is_sample: bool) -> str:
    expected = (
        "encor-static-sample encor-dnd-ui dragdrop-exercise"
        if is_sample
        else "encor-question-ui encor-dnd-ui dragdrop-exercise"
    )
    if re.search(rf'<body class="[^"]*encor-dnd-ui[^"]*"', text, re.I):
        return re.sub(r'<body class="[^"]*"', f'<body class="{expected}"', text, count=1, flags=re.I)
    return re.sub(r"<body>", f'<body class="{expected}">', text, count=1, flags=re.I)


def build_sim_nav(*, is_sample: bool) -> str:
    home = SAMPLE_HOME if is_sample else PORTAL_HOME
    return (
        f'  <nav class="sim-nav encor-sample-sim-nav" aria-label="Question navigation">\n'
        f'    <a class="sim-nav-btn sim-nav-home" href="{home}">Home</a>\n'
        f"  </nav>"
    )


def normalize_sim_nav(tail: str, *, is_sample: bool) -> str:
    tail = strip_home_key(tail)
    tail = re.sub(
        r'<a class="site-logo-corner"[\s\S]*?</a>\s*',
        "",
        tail,
        flags=re.I,
    )
    if "encor-sample-sim-nav" not in tail and 'class="sim-nav"' not in tail:
        nav = build_sim_nav(is_sample=is_sample)
        practice = '<script src="/js/practice-questions.js"></script>'
        if practice in tail:
            tail = tail.replace(practice, nav + "\n  " + practice)
        else:
            tail = (tail + "\n\n" + nav).strip()
    else:
        tail = re.sub(
            r'<nav class="sim-nav"',
            '<nav class="sim-nav encor-sample-sim-nav"',
            tail,
            count=1,
            flags=re.I,
        )
    for home_href in (SAMPLE_HOME, PORTAL_HOME):
        if home_href not in tail or "sim-nav-home" in tail:
            continue
        tail = re.sub(
            rf'(<a class="sim-nav-btn)(?!\s+sim-nav-home)(" href="{re.escape(home_href)}")',
            r"\1 sim-nav-home\2",
            tail,
            count=1,
            flags=re.I,
        )
    tail = re.sub(
        r'class="sim-nav-btn"\s+class="sim-nav-btn sim-nav-home"',
        'class="sim-nav-btn sim-nav-home"',
        tail,
    )
    return tail.strip()


def build_head(*, title: str, extras: str, exhibit_css: str) -> str:
    lines = [
        "<head>",
        '  <meta charset="UTF-8" />',
    ]
    if extras:
        lines.append(extras)
    lines.extend(
        [
            '  <meta name="robots" content="index, follow" />',
            '  <meta name="viewport" content="width=device-width, initial-scale=1.0" />',
            f"  <title>{title}</title>",
        ]
    )
    for href in REQUIRED_STYLESHEETS:
        lines.append(f'  <link rel="stylesheet" href="{href}" />')
    if exhibit_css:
        lines.append(exhibit_css)
    lines.append("</head>")
    return "\n".join(lines)


def build_body_shell(
    main_inner: str,
    tail: str,
    *,
    is_sample: bool,
) -> str:
    home = SAMPLE_HOME if is_sample else PORTAL_HOME
    body_class = (
        "encor-static-sample encor-dnd-ui dragdrop-exercise"
        if is_sample
        else "encor-question-ui encor-dnd-ui dragdrop-exercise"
    )
    if is_sample:
        logo_corner = (
            '    <span class="site-logo-corner" aria-hidden="true">\n'
            f'      <img src="{LOGO_IMG}" width="52" height="52" alt="" />\n'
            "    </span>"
        )
    else:
        logo_corner = (
            f'    <a class="site-logo-corner" href="{home}" '
            f'aria-label="ENCOR practice portal">\n'
            f'      <img src="{LOGO_IMG}" width="52" height="52" alt="Be Certified Today" />\n'
            "    </a>"
        )
    return f"""<body class="{body_class}">
  <script src="/js/sample-url-mask-apply.js"></script>
{WATERMARK}
  <div class="question-shell">
{logo_corner}
    <main class="card">
{main_inner}
    </main>
  </div>

{tail}
</body>"""


def repair_broken_bank(main: str) -> str:
    m = re.search(r'(<div id="bank" class="bank">)([\s\S]*?)(</div>)', main, re.I)
    if not m or not is_broken_layout_wrap(main):
        return main
    bank_open, bank_body, bank_close = m.group(1), m.group(2), m.group(3)
    tokens = re.findall(r'<div class="token"[\s\S]*?</div>', bank_body, re.I)
    if len(tokens) <= 1:
        return main
    first = tokens[0]
    rest = "".join(tokens[1:])
    if rest not in main[m.end() : m.end() + len(rest) + 40]:
        return main
    repaired_bank = bank_open + "\n          " + first + "\n" + rest + "\n        " + bank_close
    main = main[: m.start()] + repaired_bank + main[m.end() :]
    main = re.sub(
        r"</div>\s*<div class=\"token\"",
        '<div class="token"',
        main,
        flags=re.I,
    )
    return main


def apply_template(text: str, *, is_sample: bool) -> str:
    text = ensure_stylesheets(text)
    text = ensure_body_classes(text, is_sample=is_sample)
    if "dragdrop-touch-hint" not in text:
        text = re.sub(
            r'(<main class="card">)',
            r"\1\n" + TOUCH_HINT,
            text,
            count=1,
            flags=re.I,
        )
    m = re.search(r'<main class="card">(.*?)</main>', text, re.I | re.S)
    if m:
        main_inner = m.group(1)
        repaired = repair_broken_bank(main_inner)
        repaired = wrap_row_bank_split(repaired)
        repaired = wrap_code_bank_split(repaired)
        repaired = wrap_layout_in_sim_frame(repaired)
        repaired = normalize_actions(repaired)
        if repaired != main_inner:
            text = text[: m.start(1)] + repaired + text[m.end(1) :]
    text = normalize_actions(text)
    tail_m = re.search(r"</main>([\s\S]*)</body>", text, re.I)
    if tail_m:
        tail = normalize_sim_nav(tail_m.group(1), is_sample=is_sample)
        if tail != tail_m.group(1).strip():
            text = text[: tail_m.start(1)] + "\n" + tail + "\n" + text[tail_m.end(1) :]
    return text


def migrate_text(text: str, *, is_sample: bool) -> str:
    if not needs_migration(text):
        return text

    title = extract_title(text)
    extras = extract_head_extras(text)
    exhibit_css = extract_exhibit_css(extract_first_style(text))
    main_inner = extract_main_inner(text)
    main_inner = repair_broken_bank(main_inner)
    main_inner = wrap_row_bank_split(main_inner)
    main_inner = wrap_code_bank_split(main_inner)
    main_inner = wrap_layout_in_sim_frame(main_inner)
    main_inner = add_touch_hint(main_inner)
    main_inner = normalize_actions(main_inner)
    tail = normalize_sim_nav(extract_tail(text), is_sample=is_sample)

    head = build_head(title=title, extras=extras, exhibit_css=exhibit_css)
    body = build_body_shell(main_inner, tail, is_sample=is_sample)
    return f'<!doctype html>\n<html lang="en">\n{head}\n{body}\n</html>\n'


def migrate_file(path: Path, *, is_sample: bool = False) -> bool:
    text = path.read_text(encoding="utf-8")
    if not needs_migration(text):
        return False
    path.write_text(migrate_text(text, is_sample=is_sample), encoding="utf-8")
    return True


def apply_template_file(path: Path, *, is_sample: bool = False) -> bool:
    text = path.read_text(encoding="utf-8")
    updated = apply_template(text, is_sample=is_sample)
    if updated == text:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def is_broken_row_split(main: str) -> bool:
    if 'class="row-list"' not in main:
        return False
    before_actions = main.split('<div class="actions"', 1)[0]
    return "drop-slot" not in before_actions and 'class="slot"' not in before_actions


def is_broken_split(main: str) -> bool:
    if is_broken_row_split(main):
        return True
    before_actions = main.split('<div class="actions"', 1)[0]
    token_total = len(re.findall(r'class="token"', before_actions, re.I))
    bank_m = re.search(r'<div id="bank"', before_actions, re.I)
    if not bank_m:
        return False
    bank_end = find_matching_div_close(before_actions, bank_m.start())
    if bank_end < 0:
        return False
    bank_body = before_actions[bank_m.start() : bank_end]
    token_in_bank = len(re.findall(r'class="token"', bank_body, re.I))
    return token_total > token_in_bank


def extract_work_region(main: str) -> tuple[str, str] | None:
    start_m = re.search(
        r"(?=<div class=\"(?:layout|row|sim-frame|code-wrap)\")",
        main,
        re.I,
    )
    end_m = re.search(r"<div class=\"actions\">", main, re.I)
    if not start_m or not end_m or start_m.start() >= end_m.start():
        return None
    prefix = main[: start_m.start()]
    suffix = main[end_m.start() :]
    body = main[start_m.start() : end_m.start()]
    return prefix + "%%WORK%%" + suffix, body


def repair_broken_split(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    try:
        main_inner = extract_main_inner(text)
    except ValueError:
        return False
    if not is_broken_split(main_inner):
        return False
    rel = path.relative_to(ROOT).as_posix()
    try:
        head_text = subprocess.check_output(
            ["git", "show", f"HEAD:{rel}"],
            cwd=ROOT,
            text=True,
        )
    except subprocess.CalledProcessError:
        return False
    head_main = extract_main_inner(head_text)
    shell = extract_work_region(main_inner)
    if not shell:
        return False
    prefix_suffix, _ = shell
    work = head_main
    work = wrap_row_bank_split(work)
    work = wrap_code_bank_split(work)
    work = wrap_layout_in_sim_frame(work)
    work_region = extract_work_region(work)
    if not work_region:
        return False
    _, work_body = work_region
    repaired_main = prefix_suffix.replace("%%WORK%%", work_body)
    text = re.sub(
        r"<main class=\"card\">.*?</main>",
        f"<main class=\"card\">\n{repaired_main}\n    </main>",
        text,
        count=1,
        flags=re.I | re.S,
    )
    path.write_text(text, encoding="utf-8")
    return True


def main() -> int:
    apply_all = "--apply-template" in sys.argv or "--all" in sys.argv
    repair_only = "--repair" in sys.argv
    changed = 0
    targets = sorted(DND_DIR.rglob("*.html"))
    for sample_path in SAMPLE_DND_FILES:
        if sample_path.exists():
            targets.append(sample_path)
    for html_path in targets:
        is_sample = "ENCOR_Samples" in str(html_path)
        if repair_only:
            if repair_broken_split(html_path):
                changed += 1
                print(f"repaired: {html_path.relative_to(ROOT)}")
            continue
        if apply_all:
            if apply_template_file(html_path, is_sample=is_sample):
                changed += 1
                print(f"template: {html_path.relative_to(ROOT)}")
        elif migrate_file(html_path, is_sample=is_sample):
            changed += 1
            print(f"migrated: {html_path.relative_to(ROOT)}")
    print(f"done — {changed} file(s) updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
