"""Load SY0-701 question poll targets from marketing-vault/10-competitors/sites/*.md."""
from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMPETITOR_SITES = ROOT / "marketing-vault" / "10-competitors" / "sites"

USER_AGENT = "BCT-SY0-701-Monthly-Hunt/1.0 (+https://becertifiedtoday.com; research)"


def fetch_url(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def html_to_text(fragment: str) -> str:
    text = re.sub(r"<[^>]+>", " ", fragment)
    text = unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def parse_simple_yaml(block: str) -> dict:
    root: dict = {}
    stack: list[tuple[int, dict]] = [(-1, root)]
    for raw in block.splitlines():
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        key, _, val = raw.strip().partition(":")
        val = val.strip().strip('"').strip("'")
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if val == "":
            child: dict = {}
            parent[key] = child
            stack.append((indent, child))
        elif val.lower() == "true":
            parent[key] = True
        elif val.lower() == "false":
            parent[key] = False
        elif val.isdigit():
            parent[key] = int(val)
        else:
            parent[key] = val
    return root


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    return parse_simple_yaml(text[3:end])


def load_poll_sources() -> list[dict]:
    if not COMPETITOR_SITES.is_dir():
        return []
    sources: list[dict] = []
    for path in sorted(COMPETITOR_SITES.glob("*.md")):
        meta = parse_frontmatter(path)
        poll = meta.get("question_poll")
        if not isinstance(poll, dict) or not poll.get("enabled"):
            continue
        sample_url = poll.get("sample_url") or meta.get("url") or ""
        if not sample_url:
            print(f"[poll] skip {path.name}: no sample_url", file=sys.stderr)
            continue
        sources.append(
            {
                "file": path.name,
                "brand": meta.get("brand", path.stem),
                "id": poll.get("id") or path.stem,
                "sample_url": sample_url,
                "parser": poll.get("parser", "generic_mcq"),
                "version_note": poll.get("version_note") or meta.get("product", "SY0-701"),
                "tier": poll.get("tier", "b"),
                "max_pages": int(poll.get("max_pages", 1)),
                "max_questions": int(poll.get("max_questions", 0)),
                "topic_notes": poll.get("topic_notes")
                or _default_topic_notes(poll.get("tier", "b")),
            }
        )
    return sources


def _default_topic_notes(tier: str) -> str:
    if str(tier).lower() == "c":
        return "Tier C research — community recall; verify answer on CompTIA Tier A only"
    return "Tier B — verify answer on CompTIA Tier A"


def _base_row(src: dict, qid: str, stem: str) -> dict:
    return {
        "source_id": src["id"],
        "source_url": src["sample_url"],
        "source_version": src.get("version_note", ""),
        "source_question_id": qid,
        "stem": stem,
        "topic_notes": src.get("topic_notes", ""),
    }


def _attach_choices(row: dict, choices: list[str]) -> dict:
    for idx, ch in enumerate(choices[:6]):
        row[f"choice_{chr(ord('a') + idx)}"] = ch
    return row


def _dedupe_rows(rows: list[dict]) -> list[dict]:
    seen: set[str] = set()
    out: list[dict] = []
    for row in rows:
        key = re.sub(r"\s+", " ", (row.get("stem") or "").lower())[:120]
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


def parse_techexamlexicon(page_html: str, src: dict) -> list[dict]:
    rows: list[dict] = []
    parts = re.split(r'id="question-(\d+)"', page_html)
    for i in range(1, len(parts), 2):
        qnum = parts[i]
        block = parts[i + 1] if i + 1 < len(parts) else ""
        text = html_to_text(block)
        choice_start = re.search(r"\s+A\.\s+", text)
        if not choice_start:
            continue
        stem = text[: choice_start.start()].strip()
        stem = re.sub(r"^Topic:\s*.+?\s+", "", stem, flags=re.I).strip()
        if len(stem) < 20:
            continue
        choices = re.findall(r"([A-F])\.\s+(.+?)(?=\s+[A-F]\.\s+|Best answer:|$)", text)
        row = _base_row(src, qnum, stem)
        _attach_choices(row, [f"{letter}. {txt.strip()}" for letter, txt in choices])
        ans = re.search(r"Best answer:\s*([A-F])", text, re.I)
        if ans:
            row["stated_answer"] = ans.group(1).upper()
        rows.append(row)
    return _dedupe_rows(rows)


def parse_certblaster(page_html: str, src: dict) -> list[dict]:
    rows: list[dict] = []
    parts = re.split(
        r"<h2[^>]*>.*?QUESTION(?:&nbsp;|\s)+(\d+).*?</h2>",
        page_html,
        flags=re.I | re.DOTALL,
    )
    for i in range(1, len(parts), 2):
        qnum = parts[i]
        block = parts[i + 1] if i + 1 < len(parts) else ""
        plain = html_to_text(re.sub(r"<ul[^>]*>.*?</ul>", " CHOICES ", block, count=1, flags=re.I | re.DOTALL))
        ul = re.search(r"<ul[^>]*>(.*?)</ul>", block, re.I | re.DOTALL)
        choices: list[str] = []
        if ul:
            for li in re.findall(r"<li[^>]*>(.*?)</li>", ul.group(1), re.I | re.DOTALL):
                t = html_to_text(li)
                if t:
                    choices.append(t)
        stem_match = re.search(r"^(.+?\?)", plain)
        if not stem_match or len(choices) < 2:
            continue
        row = _base_row(src, qnum, stem_match.group(1).strip())
        letters = "abcdef"
        _attach_choices(row, [f"{letters[i].upper()}. {c}" for i, c in enumerate(choices[:6])])
        ans = re.search(r"Answer:\s*(.+?)(?:This question|$)", plain, re.I)
        if ans:
            row["stated_answer"] = ans.group(1).strip()[:120]
        rows.append(row)
    return _dedupe_rows(rows)


def parse_mastery(page_html: str, src: dict) -> list[dict]:
    rows: list[dict] = []
    parts = re.split(r"<h3[^>]*>\s*Question\s+(\d+)\s*</h3>", page_html, flags=re.I)
    for i in range(1, len(parts), 2):
        qnum = parts[i]
        block = parts[i + 1] if i + 1 < len(parts) else ""
        text = html_to_text(block)
        text = re.sub(r"^Topic:\s*.+?\s+", "", text, flags=re.I)
        text = re.sub(
            r"^Domain\s+\d+:\s*.+?\s+(?=Which|What|When|How|An |A |The )",
            "",
            text,
            flags=re.I,
        )
        stem_m = re.search(r"((?:Which|What|When|How|An |A |The ).+?\?)", text)
        if not stem_m:
            continue
        stem = stem_m.group(1).strip()
        choices = re.findall(r"([A-F])\.\s+(.+?)(?=\s+[A-F]\.\s+|Correct Answer|$)", text)
        if not choices:
            choices = re.findall(r"([A-F])\.\s+(.+?)(?=\s+[A-F]\.\s+|$)", text)
        row = _base_row(src, qnum, stem)
        _attach_choices(row, [f"{letter}. {txt.strip()}" for letter, txt in choices])
        ans = re.search(r"Correct Answer[s]?:\s*([A-F,\s]+)", text, re.I)
        if ans:
            row["stated_answer"] = ans.group(1).strip()
        rows.append(row)
    return _dedupe_rows(rows)


def _extract_openexamprep_questions(page_html: str) -> list[dict]:
    chunks = re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)', page_html)
    for raw in chunks:
        try:
            decoded = json.loads('"' + raw + '"')
        except json.JSONDecodeError:
            continue
        match = re.search(r"initialQuestions\":(\[)", decoded)
        if not match:
            continue
        start = match.start(1)
        depth = 0
        for i in range(start, len(decoded)):
            if decoded[i] == "[":
                depth += 1
            elif decoded[i] == "]":
                depth -= 1
                if depth == 0:
                    return json.loads(decoded[start : i + 1])
    return []


def parse_openexamprep(page_html: str, src: dict) -> list[dict]:
    items = _extract_openexamprep_questions(page_html)
    if not items:
        return []
    cap = int(src.get("max_questions", 0))
    if cap > 0:
        items = items[:cap]
    rows: list[dict] = []
    for item in items:
        stem = (item.get("question") or "").strip()
        options = item.get("options") or []
        if len(stem) < 20 or len(options) < 2:
            continue
        qid = item.get("id") or str(len(rows) + 1)
        qnum = re.sub(r"^qb-secplus-", "", qid)
        row = _base_row(src, qnum, stem)
        letters = "ABCDEF"
        _attach_choices(
            row,
            [f"{letters[i]}. {opt}" for i, opt in enumerate(options[:6])],
        )
        correct = item.get("correctAnswer")
        if isinstance(correct, int) and 0 <= correct < len(options):
            row["stated_answer"] = letters[correct]
        rows.append(row)
    return _dedupe_rows(rows)


def parse_examtopics(page_html: str, src: dict) -> list[dict]:
    rows: list[dict] = []
    cards = re.split(r'<div class="card exam-question-card', page_html)[1:]
    for card in cards:
        qm = re.search(r"Question\s+#(\d+)", card, re.I)
        if not qm:
            continue
        qnum = qm.group(1)
        stem_m = re.search(
            r"((?:Which|What|When|How|An |A |The )[^<]+?\?)",
            card,
            re.I | re.DOTALL,
        )
        if not stem_m:
            continue
        stem = html_to_text(stem_m.group(1))
        choices = re.findall(
            r'class="multi-choice-item[^"]*"[^>]*>(.*?)</li>',
            card,
            re.I | re.DOTALL,
        )
        choice_text = [html_to_text(c) for c in choices if html_to_text(c)]
        if len(choice_text) < 2:
            continue
        row = _base_row(src, qnum, stem)
        _attach_choices(row, choice_text[:6])
        vote = re.search(r'"voted_answers":\s*"([A-F])".*?"is_most_voted":\s*true', card)
        if vote:
            row["stated_answer"] = f"{vote.group(1)} (community vote — unverified)"
        rows.append(row)
    return _dedupe_rows(rows)


def parse_preptia(page_html: str, src: dict) -> list[dict]:
    rows: list[dict] = []
    parts = re.split(r"Question No\s*(\d+)", page_html, flags=re.I)
    for i in range(1, len(parts), 2):
        qnum = parts[i]
        block = parts[i + 1] if i + 1 < len(parts) else ""
        text = html_to_text(block)
        pre = text.split("Explanation:")[0]
        stem_m = re.search(r"(.+?\?)\s", pre)
        if not stem_m:
            continue
        stem = stem_m.group(1).strip()
        letters_found: dict[str, str] = {}
        for m in re.finditer(r"([A-D])\.\s+(.+?)(?=\s+[A-D]\.\s+|$)", pre):
            if m.group(1) not in letters_found:
                letters_found[m.group(1)] = m.group(2).strip()
        if len(letters_found) < 4:
            continue
        row = _base_row(src, qnum, stem)
        _attach_choices(
            row,
            [f"{letter}. {letters_found[letter]}" for letter in "ABCD"],
        )
        ans = re.search(r"Correct Option:\s*([A-D])\.", text, re.I)
        if ans:
            row["stated_answer"] = ans.group(1).upper()
        rows.append(row)
    return _dedupe_rows(rows)


def parse_certimaan(page_html: str, src: dict) -> list[dict]:
    rows: list[dict] = []
    h2_matches = list(
        re.finditer(r"<h2[^>]*>.*?(\d+)\.\s*([^<]*\?)", page_html, re.I | re.DOTALL)
    )
    for i, m in enumerate(h2_matches):
        qnum = int(m.group(1))
        if qnum < 1 or qnum > 40:
            continue
        stem = unescape(m.group(2)).strip()
        start = m.end()
        end = h2_matches[i + 1].start() if i + 1 < len(h2_matches) else start + 8000
        block = page_html[start:end]
        opts = re.findall(r"<p[^>]*>.*?<span>([^<]+)</span>", block, re.I | re.DOTALL)
        opts = [unescape(o.strip()) for o in opts if o.strip() and len(o.strip()) < 120]
        if len(opts) < 4:
            continue
        row = _base_row(src, str(qnum), stem)
        _attach_choices(
            row,
            [f"{idx}. {opt}" for idx, opt in enumerate(opts[:4], 1)],
        )
        rows.append(row)
    return _dedupe_rows(rows)


def parse_generic_mcq(page_html: str, src: dict) -> list[dict]:
    rows: list[dict] = []
    text = html_to_text(page_html)
    blocks = re.split(r"(?:Question\s+#?\d+|QUESTION\s+\d+)", text, flags=re.I)[1:]
    for i, block in enumerate(blocks, 1):
        stem_m = re.search(r"^(.+?\?)", block.strip())
        if not stem_m:
            continue
        choices = re.findall(r"([A-F])\.\s+(.+?)(?=\s+[A-F]\.\s+|$)", block)
        if len(choices) < 2:
            continue
        row = _base_row(src, str(i), stem_m.group(1).strip())
        _attach_choices(row, [f"{letter}. {txt.strip()}" for letter, txt in choices])
        rows.append(row)
    return _dedupe_rows(rows)


PARSERS = {
    "techexamlexicon": parse_techexamlexicon,
    "certblaster": parse_certblaster,
    "mastery": parse_mastery,
    "openexamprep": parse_openexamprep,
    "preptia": parse_preptia,
    "certimaan": parse_certimaan,
    "examtopics": parse_examtopics,
    "generic_mcq": parse_generic_mcq,
}


def poll_source(src: dict, fetcher=fetch_url) -> list[dict]:
    parser_name = src.get("parser", "generic_mcq")
    parser = PARSERS.get(parser_name, parse_generic_mcq)
    rows: list[dict] = []
    max_pages = max(1, int(src.get("max_pages", 1)))

    if parser_name == "examtopics":
        base = re.sub(r"/view/\d+/?$", "", src["sample_url"].rstrip("/"))
        for page in range(1, max_pages + 1):
            url = f"{base}/view/{page}/"
            try:
                html = fetcher(url)
            except (urllib.error.URLError, TimeoutError) as exc:
                print(f"  page {page} skip: {exc}", file=sys.stderr)
                break
            parsed = parser(html, src)
            if not parsed:
                break
            for r in parsed:
                r["source_url"] = url
            rows.extend(parsed)
        return _dedupe_rows(rows)

    try:
        html = fetcher(src["sample_url"])
    except (urllib.error.URLError, TimeoutError) as exc:
        raise exc
    return parser(html, src)


def poll_all_sources(sources: list[dict] | None = None, fetcher=fetch_url) -> list[dict]:
    sources = sources if sources is not None else load_poll_sources()
    all_rows: list[dict] = []
    for src in sources:
        sid = src.get("id", "?")
        print(f"[collect] poll: {sid} ({src.get('parser')}) …")
        try:
            parsed = poll_source(src, fetcher=fetcher)
        except (urllib.error.URLError, TimeoutError) as exc:
            print(f"  skip: {exc}", file=sys.stderr)
            continue
        print(f"  {len(parsed)} questions")
        all_rows.extend(parsed)
    return all_rows


if __name__ == "__main__":
    for s in load_poll_sources():
        print(json.dumps({k: s[k] for k in ("id", "parser", "sample_url", "tier")}, indent=2))
