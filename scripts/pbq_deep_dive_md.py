"""Convert marketing-vault SEC+ PBQ deep-dive-solution.md to HTML for modals."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VAULT_PBq = ROOT / "marketing-vault/SEC+/PBQ"


def _strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            return text[end + 3 :].lstrip()
    return text


def _inline_md(s: str) -> str:
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def _parse_table(lines: list[str]) -> str:
    rows: list[list[str]] = []
    for line in lines:
        line = line.strip()
        if not line.startswith("|"):
            break
        if re.match(r"^\|[\s\-:|]+\|$", line):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        rows.append(cells)
    if not rows:
        return ""
    head = rows[0]
    body = rows[1:]
    parts = ['<table class="deep-dive-table"><thead><tr>']
    for cell in head:
        parts.append(f"<th scope=\"col\">{_inline_md(cell)}</th>")
    parts.append("</tr></thead><tbody>")
    for row in body:
        parts.append("<tr>")
        for i, cell in enumerate(row):
            tag = "th" if i == 0 and len(row) > 1 else "td"
            scope = ' scope="row"' if tag == "th" else ""
            parts.append(f"<{tag}{scope}>{_inline_md(cell)}</{tag}>")
        parts.append("</tr>")
    parts.append("</tbody></table>")
    return "".join(parts)


def md_to_deep_dive_html(md: str) -> tuple[str, str]:
    """Return (title, html body) from vault markdown."""
    md = _strip_frontmatter(md)
    title = "Deep dive — solution walkthrough"
    m = re.search(r"^#\s+(.+)$", md, re.MULTILINE)
    if m:
        title = re.sub(r"\s*—\s*deep dive solution\s*$", "", m.group(1).strip(), flags=re.I)
        if not title.lower().startswith("deep dive"):
            title = f"Deep dive — {title}"

    lines = md.splitlines()
    i = 0
    while i < len(lines) and not lines[i].startswith("## "):
        i += 1

    steps: list[str] = []
    while i < len(lines):
        line = lines[i]
        if line.startswith("## "):
            heading = _inline_md(line[3:].strip())
            i += 1
            chunk: list[str] = []
            while i < len(lines) and not lines[i].startswith("## "):
                chunk.append(lines[i])
                i += 1
            body = _chunk_to_html(chunk)
            steps.append(f"<li><h3>{heading}</h3>{body}</li>")
        else:
            i += 1

    if not steps:
        body_html = _chunk_to_html(lines)
        return title, f'<div class="deep-dive-body">{body_html}</div>'

    return title, '<ol class="deep-dive-steps">' + "".join(steps) + "</ol>"


def _chunk_to_html(chunk: list[str]) -> str:
    parts: list[str] = []
    i = 0
    while i < len(chunk):
        line = chunk[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue
        if stripped == "---":
            i += 1
            continue
        if stripped.startswith("### "):
            parts.append(f"<h4>{_inline_md(stripped[4:].strip())}</h4>")
            i += 1
            continue
        if stripped.startswith(">"):
            quote_lines = []
            while i < len(chunk) and chunk[i].strip().startswith(">"):
                quote_lines.append(chunk[i].strip().lstrip(">").strip())
                i += 1
            parts.append(f'<p class="deep-dive-note">{_inline_md(" ".join(quote_lines))}</p>')
            continue
        if stripped.startswith("|"):
            table_lines = []
            while i < len(chunk) and chunk[i].strip().startswith("|"):
                table_lines.append(chunk[i])
                i += 1
            parts.append(_parse_table(table_lines))
            continue
        if stripped.startswith("```"):
            fence = stripped[3:].strip()
            i += 1
            code_lines = []
            while i < len(chunk) and not chunk[i].strip().startswith("```"):
                code_lines.append(chunk[i])
                i += 1
            if i < len(chunk):
                i += 1
            code = html.escape("\n".join(code_lines))
            lang = f' class="deep-dive-pre deep-dive-pre--{fence}"' if fence else ' class="deep-dive-pre"'
            parts.append(f"<pre{lang}><code>{code}</code></pre>")
            continue
        if re.match(r"^[-*]\s+", stripped):
            items = []
            while i < len(chunk) and re.match(r"^[-*]\s+", chunk[i].strip()):
                items.append(_inline_md(re.sub(r"^[-*]\s+", "", chunk[i].strip())))
                i += 1
            parts.append("<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>")
            continue
        if re.match(r"^\d+\.\s+", stripped):
            items = []
            while i < len(chunk) and re.match(r"^\d+\.\s+", chunk[i].strip()):
                items.append(_inline_md(re.sub(r"^\d+\.\s+", "", chunk[i].strip())))
                i += 1
            parts.append("<ol>" + "".join(f"<li>{item}</li>" for item in items) + "</ol>")
            continue

        para_lines = [stripped]
        i += 1
        while i < len(chunk):
            nxt = chunk[i].strip()
            if (
                not nxt
                or nxt == "---"
                or nxt.startswith(">")
                or nxt.startswith("|")
                or nxt.startswith("```")
                or re.match(r"^[-*]\s+", nxt)
                or re.match(r"^\d+\.\s+", nxt)
                or nxt.startswith("## ")
            ):
                break
            para_lines.append(nxt)
            i += 1
        parts.append(f"<p>{_inline_md(' '.join(para_lines))}</p>")

    return "".join(parts)


def build_deep_dive_data(slugs: list[str]) -> dict[str, dict[str, str]]:
    data: dict[str, dict[str, str]] = {}
    for slug in slugs:
        path = VAULT_PBq / slug / "deep-dive-solution.md"
        if not path.is_file():
            continue
        title, body_html = md_to_deep_dive_html(path.read_text(encoding="utf-8"))
        data[f"{slug}.html"] = {"title": title, "html": body_html}
    return data


def write_deep_dive_js(slugs: list[str], out_path: Path) -> int:
    data = build_deep_dive_data(slugs)
    js = (
        "/* Generated by scripts/build-pbq-deep-dive.py — do not hand-edit */\n"
        "window.SECPLUS_PBq_DEEP_DIVE = "
        + json.dumps(data, ensure_ascii=False, indent=2)
        + ";\n"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(js, encoding="utf-8")
    return len(data)
