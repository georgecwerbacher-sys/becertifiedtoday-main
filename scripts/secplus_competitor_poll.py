"""Load SY0-701 question poll targets from marketing-vault/10-competitors/sites/*.md."""
from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMPETITOR_SITES = ROOT / "marketing-vault" / "10-competitors" / "sites"

USER_AGENT = "BCT-SY0-701-Monthly-Hunt/1.0 (+https://becertifiedtoday.com; research)"
REDDIT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)


def fetch_url(url: str, timeout: int = 30, extra_headers: dict | None = None) -> str:
    headers = {"User-Agent": USER_AGENT}
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(url, headers=headers)
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


def load_poll_sources(product: str | None = None) -> list[dict]:
    if not COMPETITOR_SITES.is_dir():
        return []
    sources: list[dict] = []
    for path in sorted(COMPETITOR_SITES.glob("*.md")):
        meta = parse_frontmatter(path)
        if product and meta.get("product") != product:
            continue
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


def _decode_json_string(raw: str) -> str:
    return json.loads(f'"{raw}"')


def crucial_demo_url(sample_url: str) -> str:
    code_m = re.search(r"/(?:ccna|exams/cisco/ccna)/(\d{3}-\d{3})", sample_url, re.I)
    if not code_m:
        code_m = re.search(r"/(\d{3}-\d{3})/", sample_url)
    code = code_m.group(1) if code_m else "200-301"
    return f"https://crucialexams.com/study/tests/cisco/{code}/auto?DemoMode=True&ShowTest=True"


def howtonetwork_page_slug(sample_url: str) -> str:
    path = urllib.parse.urlparse(sample_url).path.strip("/")
    return path.split("/")[-1] if path else ""


def parse_crucialexams(page_html: str, src: dict) -> list[dict]:
    text = unescape(page_html)
    rows: list[dict] = []
    letters = "ABCDEF"
    for block in re.split(r'(?="questionHtml")', text)[1:]:
        qh = re.search(r'"questionHtml"\s*:\s*"((?:\\.|[^"\\])*)"', block)
        if not qh:
            continue
        stem = html_to_text(_decode_json_string(qh.group(1)))
        if len(stem) < 15:
            continue
        answers = re.findall(
            r'"html"\s*:\s*"((?:\\.|[^"\\])*)"\s*,\s*"isCorrect"\s*:\s*(true|false)',
            block,
            re.I,
        )
        opts: list[str] = []
        correct: list[str] = []
        for h, is_correct in answers[:6]:
            opt = html_to_text(_decode_json_string(h))
            if not opt:
                continue
            letter = letters[len(opts)]
            opts.append(f"{letter}. {opt}")
            if is_correct.lower() == "true":
                correct.append(letter)
        if len(opts) < 2:
            continue
        qurl = re.search(r'"questionUrl"\s*:\s*"([^"]+)"', block)
        qid = str(len(rows) + 1)
        if qurl:
            tail = re.search(r"/(\d+)/?$", qurl.group(1).rstrip("/"))
            if tail:
                qid = tail.group(1)
        row = _base_row(src, qid, stem)
        _attach_choices(row, opts)
        if correct:
            row["stated_answer"] = ",".join(correct)
        rows.append(row)
    cap = int(src.get("max_questions", 0))
    if cap > 0:
        rows = rows[:cap]
    return _dedupe_rows(rows)


def parse_howtonetwork(page_html: str, src: dict) -> list[dict]:
    rows: list[dict] = []
    parts = re.split(
        r"<div[^>]*class=['\"]watu-question\s*['\"][^>]*>",
        page_html,
        flags=re.I,
    )
    for part in parts[1:]:
        if "watupro-matrix" in part.lower():
            continue
        qid_m = re.search(r"watupro-question-id-(\d+)", part)
        qid = qid_m.group(1) if qid_m else str(len(rows) + 1)
        heading = re.search(r"<h[45][^>]*>(.*?)</h[45]>", part, re.I | re.S)
        if not heading:
            continue
        stem = re.sub(r"^\d+\.\s*", "", html_to_text(heading.group(1))).strip()
        if len(stem) < 15:
            continue
        choices: list[str] = []
        for m in re.finditer(
            r"<label[^>]*class=['\"][^'\"]*answer[^'\"]*['\"][^>]*>\s*<span>(.*?)</span>",
            part,
            re.I | re.S,
        ):
            choice = html_to_text(m.group(1)).strip()
            if choice:
                choices.append(choice)
        if len(choices) < 2:
            continue
        row = _base_row(src, qid, stem)
        _attach_choices(
            row,
            [f"{chr(ord('A') + i)}. {choice}" for i, choice in enumerate(choices[:6])],
        )
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


PBQ_SECTION_SPLIT = re.compile(
    r"(?:"
    r"performance[- ]based(?:\s+question[s]?)?"
    r"|PBQ[s]?"
    r"|simulation(?:\s+question[s]?)?"
    r"|hot[- ]?spot"
    r"|drag[- ]?(?:and|&)[- ]?drop"
    r"|drag[- ]drop"
    r"|click[- ]and[- ]drag"
    r")(?:\s*question[s]?)?\s*[:\-]?\s*",
    re.I,
)

PBQ_STEM_ACTION = re.compile(
    r"\b("
    r"map|place|drag|drop|reorder|sort|select|configure|identify|match|arrange|move|click"
    r")\b",
    re.I,
)

PBQ_STEM_TOPIC = re.compile(
    r"\b("
    r"security|network|firewall|waf|ssh|log|sudo|user|cron|vlan|dns|tls|ssl|certificate|"
    r"hash|malware|incident|access|control|risk|threat|encryption|auth|router|switch|"
    r"port|protocol|ipsec|vpn|siem|edr|ids|ips|dmz|perimeter|endpoint|cloud"
    r")\b",
    re.I,
)

PBQ_SIGNAL_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("pbq", re.compile(r"\bPBQs?\b", re.I)),
    ("performance-based", re.compile(r"performance[- ]based", re.I)),
    ("drag-and-drop", re.compile(r"drag[- ]?(?:and|&)[- ]?drop", re.I)),
    ("drag-drop", re.compile(r"drag[- ]drop", re.I)),
    ("hot-spot", re.compile(r"hot[- ]?spot", re.I)),
    ("simulation", re.compile(r"\bsimulation[s]?\b", re.I)),
    ("simulator", re.compile(r"\b(?:exam|testing)\s+simulator\b|\btesting\s+engine\b", re.I)),
    ("hands-on", re.compile(r"hands[- ]on\s+(?:exercise|question|lab|sim)", re.I)),
    ("interactive", re.compile(r"interactive\s+(?:pbq|question|sim|item)", re.I)),
    ("table-matching", re.compile(r"table\s+matching|match[- ]each", re.I)),
    ("reorder", re.compile(r"\b(?:reorder|correct order|put in order|chronolog)\b", re.I)),
    ("mini-game", re.compile(r"mini[- ]?games?", re.I)),
    ("security-plus-pbq", re.compile(r"security\+?\s*(?:sy0[- ]?701)?[^.]{0,60}(?:pbq|performance[- ]based|simulation)", re.I)),
]

PBQ_DEEP_SNIPPET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    (
        "stated-count",
        re.compile(
            r"(\d+)\s+(?:PBQs?|performance[- ]based questions?|simulations?|hot[- ]?spots?|"
            r"drag[- ]?(?:and|&)?[- ]?drops?|interactive questions?)",
            re.I,
        ),
    ),
    (
        "combo-count",
        re.compile(
            r"(\d+\s+\w+\s*\+\s*\d+\s+\w+|(?:\d+\s+){1,4}(?:MCQ|simulation|hotspot|drag)[^.]{0,40})",
            re.I,
        ),
    ),
    (
        "hands-on-sim",
        re.compile(
            r"hands[- ]on\s+(?:exercises?|mini[- ]?games?|simulations?)[^.]{0,120}",
            re.I,
        ),
    ),
    (
        "engine-type",
        re.compile(
            r"(?:drag[- ]?(?:and|&)?[- ]?drop|simulation|hot[- ]?spot|performance[- ]based)"
            r"[^.]{0,80}(?:engine|player|format|question type)",
            re.I,
        ),
    ),
    (
        "sy0-sim",
        re.compile(
            r"sy0[- ]?701[^.]{0,80}(?:pbq|simulation|performance[- ]based|drag[- ]drop)",
            re.I,
        ),
    ),
]


def html_to_pbq_text(page_html: str) -> str:
    """Strip scripts/styles before PBQ heuristics so JSON-LD does not become fake stems."""
    cleaned = re.sub(r"<script[^>]*>.*?</script>", " ", page_html, flags=re.I | re.S)
    cleaned = re.sub(r"<style[^>]*>.*?</style>", " ", cleaned, flags=re.I | re.S)
    cleaned = re.sub(r"<noscript[^>]*>.*?</noscript>", " ", cleaned, flags=re.I | re.S)
    return html_to_text(cleaned)


def scan_pbq_page_signals(text: str) -> dict:
    hits = [label for label, pat in PBQ_SIGNAL_PATTERNS if pat.search(text)]
    count_match = re.search(
        r"(\d+)\s+(?:PBQs?|performance[- ]based questions?)",
        text,
        re.I,
    )
    stated_counts: list[str] = []
    for pat in (
        r"\d+\s+PBQs?",
        r"\d+\s+performance[- ]based questions?",
        r"\d+\s+simulations?",
        r"\d+\s+hot[- ]?spots?",
        r"\d+\s+drag[- ]?(?:and|&)?[- ]?drops?",
        r"\d+\s+interactive questions?",
    ):
        for m in re.finditer(pat, text, re.I):
            snip = re.sub(r"\s+", " ", m.group(0)).strip()
            if snip not in stated_counts:
                stated_counts.append(snip)

    deep_snippets: list[dict] = []
    for label, pat in PBQ_DEEP_SNIPPET_PATTERNS:
        for m in pat.finditer(text):
            snip = re.sub(r"\s+", " ", m.group(0)).strip()
            if len(snip) < 20:
                continue
            deep_snippets.append({"label": label, "snippet": snip[:220]})
            if len(deep_snippets) >= 8:
                break
        if len(deep_snippets) >= 8:
            break

    return {
        "terms": hits,
        "stated_pbq_count": count_match.group(1) if count_match else "",
        "stated_counts": stated_counts[:6],
        "deep_snippets": deep_snippets,
    }


def _pbq_stem_is_noise(stem: str) -> bool:
    lower = stem.lower()
    if len(stem) < 30:
        return True
    if re.search(r"\b(sameas|schema\.org|@type|read article|save big|mini-games|flashcards)\b", lower):
        return True
    if stem.count("http") >= 2:
        return True
    if re.search(r'[{}[\]"]', stem):
        return True
    return False


def _pbq_stem_is_plausible(stem: str, *, require_pbq_signal: bool = True) -> bool:
    if _pbq_stem_is_noise(stem):
        return False
    has_signal = any(pat.search(stem) for _, pat in PBQ_SIGNAL_PATTERNS)
    has_action = PBQ_STEM_ACTION.search(stem) is not None
    has_topic = PBQ_STEM_TOPIC.search(stem) is not None
    if require_pbq_signal and not has_signal:
        return False
    if has_signal and (has_action or has_topic):
        return True
    if has_action and has_topic:
        return True
    return False


def _infer_pbq_type(text: str) -> str:
    lower = text.lower()
    if re.search(r"drag[- ]?(?:and|&)?[- ]?drop|drag[- ]drop|click[- ]and[- ]drag", lower):
        return "drag-drop"
    if "table matching" in lower:
        return "drag-drop"
    if "hot spot" in lower or "hotspot" in lower:
        return "hotspot"
    if re.search(r"\b(?:reorder|correct order|timeline|put in order|chronolog)\b", lower):
        return "ordered-sequence"
    if "fill" in lower and "blank" in lower:
        return "fill-in"
    if re.search(r"\b(?:simulation|performance[- ]based|pbq)\b", lower):
        return "simulation"
    return "pbq-other"


def _extract_pbq_catalog_rows(text: str, src: dict, signals: dict) -> list[dict]:
    rows: list[dict] = []
    count = signals.get("stated_pbq_count") or ""
    if count:
        stem = (
            f"Site advertises {count} performance-based question(s) (PBQ) for "
            f"{src.get('version_note', 'SY0-701')}"
        )
        styles: list[str] = []
        if any(t in signals["terms"] for t in ("drag-and-drop", "drag-drop", "table-matching")):
            styles.append("drag-and-drop")
        if "hot-spot" in signals["terms"]:
            styles.append("hot spot")
        if "simulation" in signals["terms"] or "simulator" in signals["terms"]:
            styles.append("simulation")
        if "reorder" in signals["terms"]:
            styles.append("ordered sequence")
        if "hands-on" in signals["terms"] or "mini-game" in signals["terms"]:
            styles.append("hands-on")
        style_note = f" Stated styles: {', '.join(styles)}." if styles else ""
        row = _base_row(src, "catalog", stem)
        row["pbq_type"] = _infer_pbq_type(f"{stem} {style_note}")
        row["interaction_notes"] = (
            "Landing-page PBQ catalog signal — individual stems not in public HTML; "
            "capture pbq-preview screenshot or import manually"
            + style_note
        )
        rows.append(row)
    elif signals.get("terms"):
        stem = (
            f"Page mentions Security+ PBQ / drag-and-drop / simulation practice "
            f"({', '.join(signals['terms'][:6])})"
        )
        row = _base_row(src, "catalog", stem)
        row["pbq_type"] = _infer_pbq_type(stem)
        row["interaction_notes"] = (
            "Deep scan catalog signal — marketing or FAQ copy; not an extractable PBQ stem"
        )
        rows.append(row)

    for i, snip in enumerate(signals.get("stated_counts") or [], 1):
        stem = f"Stated count on page: {snip} ({src.get('version_note', 'SY0-701')})"
        row = _base_row(src, f"count-{i}", stem)
        row["pbq_type"] = _infer_pbq_type(snip)
        row["interaction_notes"] = "Deep scan — numeric PBQ/sim/hotspot/drag-drop claim on landing page"
        rows.append(row)

    for i, hit in enumerate(signals.get("deep_snippets") or [], 1):
        stem = f"Deep scan ({hit['label']}): {hit['snippet']}"
        row = _base_row(src, f"deep-{i}", stem[:480])
        row["pbq_type"] = _infer_pbq_type(hit["snippet"])
        row["interaction_notes"] = "Deep scan snippet — verify interaction type; pbq-preview screenshot if possible"
        rows.append(row)

    return _dedupe_rows(rows)


def parse_generic_pbq(page_html: str, src: dict) -> list[dict]:
    rows: list[dict] = []
    text = html_to_pbq_text(page_html)
    signals = scan_pbq_page_signals(text)

    blocks = PBQ_SECTION_SPLIT.split(text)
    for i, block in enumerate(blocks[1:], 1):
        chunk = block.strip()
        if len(chunk) < 40:
            continue
        stem = chunk[:480].strip()
        if not _pbq_stem_is_plausible(stem):
            continue
        row = _base_row(src, str(i), stem)
        row["pbq_type"] = _infer_pbq_type(stem)
        row["interaction_notes"] = "Extracted from page — confirm interaction type manually"
        rows.append(row)
    if rows:
        return _dedupe_rows(rows)

    markers = re.findall(
        r"((?:drag|drop|place|reorder|sort|map|hot[- ]?spot|match each|put in order).{20,320}?)(?:\.|$)",
        text,
        re.I,
    )
    for i, stem in enumerate(markers[:12], 1):
        stem = stem.strip()
        if not _pbq_stem_is_plausible(stem):
            continue
        row = _base_row(src, str(i), stem)
        row["pbq_type"] = _infer_pbq_type(stem)
        row["interaction_notes"] = "Heuristic extract — review manually"
        rows.append(row)
    if rows:
        return _dedupe_rows(rows)

    catalog_rows = _extract_pbq_catalog_rows(text, src, signals)
    if catalog_rows:
        return catalog_rows
    return []


REDDIT_PBQ_SEARCHES: dict[str, list[str]] = {
    "reddit-comptia-pbq": [
        "SY0-701 PBQ",
        "SY0-701 performance based",
        "SY0-701 simulation",
        "SY0-701 drag drop",
        "security+ PBQ",
        "security+ performance based question",
    ],
    "reddit-securityplus-pbq": [
        "SY0-701 PBQ",
        "PBQ exam",
        "performance based",
        "simulation question",
        "drag and drop",
        "what PBQ",
    ],
}

REDDIT_PBQ_DEFAULT_QUERIES = [
    "SY0-701 PBQ",
    "SY0-701 performance based",
    "security+ simulation",
]


def _reddit_post_is_pbq_relevant(text: str) -> bool:
    lower = text.lower()
    exam_hit = re.search(r"sy0[- ]?701|security\+|sec\+", lower)
    pbq_hit = re.search(
        r"\b(?:pbq|performance[- ]based|simulation|simulated|drag[- ]?(?:and|&)?[- ]?drop|"
        r"hot[- ]?spot|interactive question|lab question|what pbq)\b",
        lower,
    )
    return bool(exam_hit and pbq_hit)


def _reddit_search_url(subreddit: str, query: str, limit: int = 25) -> str:
    q = urllib.parse.quote(query)
    sr = urllib.parse.quote(subreddit.strip("/"))
    return (
        f"https://www.reddit.com/r/{sr}/search.json"
        f"?q={q}&restrict_sr=on&sort=new&limit={limit}"
    )


def poll_reddit_pbq(src: dict, fetcher=fetch_url) -> list[dict]:
    subreddit = (src.get("subreddit") or "").strip()
    if not subreddit:
        m = re.search(r"/r/([^/]+)/", src.get("sample_url", ""))
        subreddit = m.group(1) if m else "CompTIA"
    queries = REDDIT_PBQ_SEARCHES.get(src.get("id", ""), REDDIT_PBQ_DEFAULT_QUERIES)
    limit = int(src.get("max_questions", 25) or 25)
    rows: list[dict] = []
    seen_ids: set[str] = set()

    for query in queries:
        url = _reddit_search_url(subreddit, query, limit=min(limit, 25))
        try:
            raw = fetcher(
                url,
                extra_headers={
                    "User-Agent": REDDIT_USER_AGENT,
                    "Accept": "application/json",
                },
            )
            data = json.loads(raw)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            print(f"  reddit search skip ({query!r}): {exc}", file=sys.stderr)
            continue
        for child in data.get("data", {}).get("children", []):
            post = child.get("data") or {}
            pid = post.get("id") or ""
            if not pid or pid in seen_ids:
                continue
            title = (post.get("title") or "").strip()
            body = (post.get("selftext") or "").strip()
            combined = f"{title}. {body[:500]}".strip().strip(".")
            if len(combined) < 25 or not _reddit_post_is_pbq_relevant(combined):
                continue
            seen_ids.add(pid)
            permalink = post.get("permalink") or ""
            post_url = f"https://www.reddit.com{permalink}" if permalink else url
            row = _base_row(src, pid, combined[:480])
            row["source_url"] = post_url
            row["pbq_type"] = _infer_pbq_type(combined)
            row["interaction_notes"] = (
                f"Reddit r/{subreddit} recall — search {query!r}; paraphrase only; verify Tier A"
            )
            row["date_found"] = src.get("version_note", "")
            rows.append(row)
    if not rows:
        print(
            "  Reddit returned no posts (often HTTP 403 from datacenter IPs). "
            "Paste PBQ recall threads into pbq/imports/ manually.",
            file=sys.stderr,
        )
    return _dedupe_rows(rows)


def parse_reddit_pbq(raw: str, src: dict) -> list[dict]:
    """Unused directly — poll_source calls poll_reddit_pbq instead."""
    return poll_reddit_pbq(src)


PARSERS = {
    "techexamlexicon": parse_techexamlexicon,
    "certblaster": parse_certblaster,
    "mastery": parse_mastery,
    "openexamprep": parse_openexamprep,
    "preptia": parse_preptia,
    "certimaan": parse_certimaan,
    "crucialexams": parse_crucialexams,
    "howtonetwork": parse_howtonetwork,
    "examtopics": parse_examtopics,
    "generic_mcq": parse_generic_mcq,
    "generic_pbq": parse_generic_pbq,
    "reddit_pbq": parse_reddit_pbq,
}


def load_pbq_poll_sources(product: str | None = None) -> list[dict]:
    if not COMPETITOR_SITES.is_dir():
        return []
    sources: list[dict] = []
    for path in sorted(COMPETITOR_SITES.glob("*.md")):
        meta = parse_frontmatter(path)
        if product and meta.get("product") != product:
            continue
        poll = meta.get("pbq_poll")
        if not isinstance(poll, dict) or not poll.get("enabled"):
            continue
        sample_url = poll.get("sample_url") or meta.get("url") or ""
        if not sample_url:
            print(f"[pbq-poll] skip {path.name}: no sample_url", file=sys.stderr)
            continue
        sources.append(
            {
                "file": path.name,
                "brand": meta.get("brand", path.stem),
                "id": poll.get("id") or f"{path.stem}-pbq",
                "sample_url": sample_url,
                "parser": poll.get("parser", "generic_pbq"),
                "version_note": poll.get("version_note") or meta.get("product", "SY0-701"),
                "tier": poll.get("tier", "b"),
                "max_pages": int(poll.get("max_pages", 1)),
                "max_questions": int(poll.get("max_questions", 0)),
                "subreddit": poll.get("subreddit", ""),
                "topic_notes": poll.get("topic_notes")
                or _default_topic_notes(poll.get("tier", "b")),
            }
        )
    return sources


def poll_all_pbq_sources(sources: list[dict] | None = None, fetcher=fetch_url) -> list[dict]:
    sources = sources if sources is not None else load_pbq_poll_sources()
    all_rows: list[dict] = []
    for src in sources:
        sid = src.get("id", "?")
        print(f"[collect] pbq poll: {sid} ({src.get('parser')}) …")
        try:
            parsed = poll_source(src, fetcher=fetcher)
        except (urllib.error.URLError, TimeoutError) as exc:
            print(f"  skip: {exc}", file=sys.stderr)
            continue
        for row in parsed:
            row.setdefault("pbq_type", _infer_pbq_type(row.get("stem", "")))
        if parsed:
            deep = sum(1 for r in parsed if str(r.get("source_question_id", "")).startswith(("deep-", "count-")))
            print(f"  {len(parsed)} PBQ candidate(s)" + (f" ({deep} deep-scan)" if deep else ""))
        else:
            try:
                page = fetcher(src["sample_url"])
                sig = scan_pbq_page_signals(html_to_pbq_text(page))
            except (urllib.error.URLError, TimeoutError):
                sig = {"terms": [], "stated_pbq_count": "", "stated_counts": [], "deep_snippets": []}
            if sig.get("terms") or sig.get("stated_pbq_count") or sig.get("deep_snippets"):
                bits = []
                if sig.get("stated_pbq_count"):
                    bits.append(f"{sig['stated_pbq_count']} PBQ(s) stated")
                if sig.get("stated_counts"):
                    bits.append("counts: " + "; ".join(sig["stated_counts"][:3]))
                if sig.get("terms"):
                    bits.append("signals: " + ", ".join(sig["terms"][:6]))
                if sig.get("deep_snippets"):
                    bits.append(f"{len(sig['deep_snippets'])} deep snippet(s)")
                print(f"  0 rows — page signals PBQ/sim/drag-drop ({'; '.join(bits)})")
            else:
                print("  0 PBQ candidates (no PBQ/drag-drop/sim signals on page)")
        all_rows.extend(parsed)
    return all_rows


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

    if parser_name == "reddit_pbq":
        return poll_reddit_pbq(src, fetcher=fetcher)

    if parser_name == "crucialexams":
        demo_url = src.get("poll_url") or crucial_demo_url(src["sample_url"])
        html = fetcher(demo_url)
        parsed = parser(html, src)
        for row in parsed:
            row["source_url"] = demo_url
        return _dedupe_rows(parsed)

    if parser_name == "howtonetwork":
        slug = howtonetwork_page_slug(src["sample_url"])
        rest_url = f"https://www.howtonetwork.com/wp-json/wp/v2/pages?slug={slug}"
        raw = fetcher(rest_url)
        pages = json.loads(raw)
        if not pages:
            return []
        html = pages[0].get("content", {}).get("rendered", "")
        parsed = parser(html, src)
        for row in parsed:
            row["source_url"] = src["sample_url"]
        return _dedupe_rows(parsed)

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
    import argparse

    ap = argparse.ArgumentParser(description="List enabled question poll sources")
    ap.add_argument("--pbq", action="store_true", help="List PBQ poll registry (pbq_poll.enabled)")
    ap.add_argument(
        "--product",
        default="SY0-701",
        help="Filter MCQ polls by frontmatter product (default: SY0-701; use CCNA-200-301 for CCNA)",
    )
    args = ap.parse_args()
    product = args.product if args.product not in ("", "all") else None
    if args.pbq:
        sources = load_pbq_poll_sources(product=product)
    else:
        sources = load_poll_sources(product=product)
    label = "PBQ" if args.pbq else "MCQ"
    print(f"[{label}] {len(sources)} enabled source(s)")
    for s in sources:
        print(json.dumps({k: s[k] for k in ("id", "parser", "sample_url", "tier")}, indent=2))
