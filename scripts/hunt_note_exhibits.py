"""Shared exhibit / image helpers for Obsidian hunt note export."""
from __future__ import annotations

import re
import urllib.request
from html import unescape
from pathlib import Path

EXHIBIT_INLINE_RE = re.compile(r"\s+Exhibit:\s+", re.I)
BARE_EXHIBIT_RE = re.compile(r"^(?:the\s+)?exhibit\.?\s+", re.I)
REFER_BELOW_ONLY_RE = re.compile(
    r"^refer to (?:the )?(?:following )?(?:'[^']+' )?(?:command )?(?:outputs?|config|show)[^.]*(?:below)?\.?\s*$",
    re.I,
)
REFER_OUTPUT_INLINE_RE = re.compile(
    r"\b(?:refer to|regarding) (?:the )?(?:following |command )?(?:'[^']+' )?(?:outputs?|config|show)[^.]*(?:below)?\.?",
    re.I,
)
REFER_TOPOLOGY_RE = re.compile(
    r"\b(?:refer to |per |as per )(?:the )?following topology\b|\b(?:the )?topology below\b",
    re.I,
)
TABLE_BELOW_RE = re.compile(r"\bon the table below\b", re.I)
FOLLOWING_OUTPUT_RE = re.compile(
    r"\b(?:considering|regarding) the following (?:command )?outputs?\b",
    re.I,
)
REFER_EXHIBIT_RE = re.compile(r"\b(?:based on|review) the exhibit\b", re.I)
QUESTION_SENTENCE_RE = re.compile(
    r"((?:Which|What|When|Why|How|A developer|Package|On which)\b[^?]+\?)\s*$",
    re.I | re.DOTALL,
)
CLI_HINT_RE = re.compile(
    r"(?:#\s|show\s|interface\s|Gi\d|GigabitEthernet|ip\s|vlan\s|Device\s+Int\s|git\s+\w+)",
    re.I,
)
COMMAND_OUTCOME_RE = re.compile(
    r"\b(?:outcome of executing|result of (?:running|executing)|following command)\b",
    re.I,
)
REFER_TO_EXHIBIT_RE = re.compile(
    r"\b(?:refer to (?:the )?exhibit|see (?:the )?exhibit|per (?:the )?exhibit|"
    r"based on (?:the )?exhibit|review (?:the )?exhibit|using (?:the )?exhibit)\b",
    re.I,
)
HTTP_HEADERS = {"User-Agent": "BCT-Hunt-Export/1.0 (+https://becertifiedtoday.com)"}

_page_cache: dict[str, str] = {}


def normalize_cli_exhibit(text: str) -> str:
    lines = [ln.rstrip() for ln in text.strip().splitlines()]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


def fetch_page(url: str) -> str:
    if not url:
        return ""
    if url in _page_cache:
        return _page_cache[url]
    try:
        req = urllib.request.Request(url, headers=HTTP_HEADERS)
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except Exception:
        html = ""
    _page_cache[url] = html
    return html


def download_hunt_image(url: str, dest: Path) -> bool:
    if not url or url.startswith("data:"):
        return False
    if url.startswith("//"):
        url = "https:" + url
    elif url.startswith("/"):
        return False
    try:
        req = urllib.request.Request(url, headers=HTTP_HEADERS)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        if len(data) < 800:
            return False
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        return True
    except Exception:
        return False


def split_stem_and_exhibit(raw_stem: str) -> tuple[str, str | None, str]:
    stem = (raw_stem or "").strip()
    if not stem:
        return stem, None, "none"

    if EXHIBIT_INLINE_RE.search(stem):
        before, after = EXHIBIT_INLINE_RE.split(stem, maxsplit=1)
        before = before.strip()
        after = after.strip()
        qm = QUESTION_SENTENCE_RE.search(after)
        if qm:
            exhibit = after[: qm.start()].strip()
            question = qm.group(1).strip()
        else:
            exhibit = after
            question = before or "See exhibit."
        merged_stem = f"{before} {question}".strip() if before else question
        if exhibit and CLI_HINT_RE.search(exhibit):
            return merged_stem, normalize_cli_exhibit(exhibit), "cli"
        if exhibit:
            return merged_stem, normalize_cli_exhibit(exhibit), "cli"
        return merged_stem, None, "missing-cli"

    if BARE_EXHIBIT_RE.match(stem):
        return BARE_EXHIBIT_RE.sub("", stem).strip(), None, "missing-image"

    if REFER_BELOW_ONLY_RE.match(stem):
        return stem, None, "missing-cli"

    if REFER_OUTPUT_INLINE_RE.search(stem):
        return stem, None, "missing-cli"

    if REFER_TOPOLOGY_RE.search(stem):
        return stem, None, "missing-image"

    if TABLE_BELOW_RE.search(stem):
        return stem, None, "missing-cli"

    if FOLLOWING_OUTPUT_RE.search(stem):
        return stem, None, "missing-cli"

    if REFER_EXHIBIT_RE.search(stem) and not EXHIBIT_INLINE_RE.search(stem):
        return stem, None, "missing-image"

    if COMMAND_OUTCOME_RE.search(stem):
        return stem, None, "missing-cli"

    if re.search(r"\bexhibit\b", stem, re.I) and not EXHIBIT_INLINE_RE.search(stem):
        return stem, None, "missing-image"

    return stem, None, "none"


def stem_expects_exhibit_image(stem: str, exhibit_status: str) -> bool:
    """True only when the stem calls for a diagram/screenshot exhibit — not decorative page art."""
    if exhibit_status == "missing-image":
        return True
    if exhibit_status in {"cli", "missing-cli", "none"}:
        return False
    if exhibit_status == "image":
        return True
    return bool(
        REFER_TO_EXHIBIT_RE.search(stem)
        or REFER_EXHIBIT_RE.search(stem)
        or REFER_TOPOLOGY_RE.search(stem)
        or BARE_EXHIBIT_RE.match(stem)
        or (re.search(r"\bexhibit\b", stem, re.I) and not EXHIBIT_INLINE_RE.search(stem))
    )


def extract_certimaan_images(page_html: str, qid: str) -> list[str]:
    urls: list[str] = []
    try:
        qnum = int(qid)
    except ValueError:
        return urls
    h2_matches = list(
        re.finditer(r"<h2[^>]*>.*?" + str(qnum) + r"\.\s*", page_html, re.I | re.DOTALL)
    )
    if not h2_matches:
        return urls
    start = h2_matches[0].start()
    end = h2_matches[1].start() if len(h2_matches) > 1 else start + 12000
    block = page_html[start:end]
    # Prefer images near an exhibit label in the question block
    exhibit_region = block
    em = re.search(
        r"(?:<[^>]+>)?\s*(?:exhibit|figure|diagram)\s*(?:<[^>]+>)?",
        block,
        re.I,
    )
    if em:
        exhibit_region = block[em.start() :]
    urls.extend(_collect_img_urls(exhibit_region))
    if not urls:
        urls.extend(_collect_img_urls(block))
    return urls


def _collect_img_urls(fragment: str) -> list[str]:
    urls: list[str] = []
    for m in re.finditer(r'<img[^>]+src=["\']([^"\']+)["\']', fragment, re.I):
        src = unescape(m.group(1)).strip()
        lower = src.lower()
        if not src or any(skip in lower for skip in ("logo", "avatar", "icon", "badge", "emoji")):
            continue
        urls.append(src)
    return urls


def extract_generic_question_images(page_html: str, qid: str) -> list[str]:
    urls: list[str] = []
    for pattern in (
        rf'(?:question|q)[-_]?{re.escape(qid)}\b',
        rf'id="question-{re.escape(qid)}"',
        rf'data-question="{re.escape(qid)}"',
    ):
        m = re.search(pattern, page_html, re.I)
        if not m:
            continue
        start = max(0, m.start() - 200)
        end = min(len(page_html), m.end() + 8000)
        block = page_html[start:end]
        for im in re.finditer(r'<img[^>]+src=["\']([^"\']+)["\']', block, re.I):
            src = unescape(im.group(1)).strip()
            if src and "logo" not in src.lower():
                urls.append(src)
        if urls:
            break
    return urls


def auto_image_urls(row: dict) -> list[str]:
    source_id = str(row.get("source_id", ""))
    qid = str(row.get("source_question_id", "")).strip()
    if not qid:
        return []
    page = fetch_page(str(row.get("source_url", "")))
    if not page:
        return []
    if "certimaan" in source_id:
        return extract_certimaan_images(page, qid)
    return extract_generic_question_images(page, qid)


def hunt_image_paths(run_dir: Path, source_id: str, source_qid: str) -> list[Path]:
    if not source_qid or not run_dir:
        return []
    images_dir = run_dir / "images"
    if not images_dir.is_dir():
        return []
    patterns = [
        f"{source_id}-q{source_qid}.*",
        f"{source_id}-q{source_qid}-*.*",
        f"q{source_qid.zfill(2)}-*",
        f"q{source_qid.zfill(3)}-*",
    ]
    found: list[Path] = []
    seen: set[str] = set()
    for pattern in patterns:
        for path in sorted(images_dir.glob(pattern)):
            if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}:
                continue
            if path.name in seen:
                continue
            seen.add(path.name)
            found.append(path)
    return found


def auto_hunt_image_paths(
    run_dir: Path,
    source_id: str,
    source_qid: str,
    image_urls: list[str],
) -> list[Path]:
    if not image_urls or not source_qid:
        return []
    images_dir = run_dir / "images"
    paths: list[Path] = []
    for index, url in enumerate(image_urls, 1):
        ext = ".png"
        if ".jpg" in url.lower() or ".jpeg" in url.lower():
            ext = ".jpg"
        elif ".webp" in url.lower():
            ext = ".webp"
        name = (
            f"{source_id}-q{source_qid}{ext}"
            if len(image_urls) == 1
            else f"{source_id}-q{source_qid}-{index}{ext}"
        )
        dest = images_dir / name
        if dest.is_file() or download_hunt_image(url, dest):
            paths.append(dest)
    return paths


def resolve_exhibit(row: dict, run_dir: Path | None) -> tuple[str, str | None, str, list[Path]]:
    raw_stem = row.get("stem", "") or ""
    stem, exhibit_text, exhibit_status = split_stem_and_exhibit(raw_stem)
    wants_image = stem_expects_exhibit_image(stem, exhibit_status)

    manual_images: list[Path] = []
    if run_dir and wants_image:
        manual_images = hunt_image_paths(
            run_dir,
            str(row.get("source_id", "")),
            str(row.get("source_question_id", "")),
        )

    auto_images: list[Path] = []
    if run_dir and wants_image and not manual_images:
        urls = auto_image_urls(row)
        auto_images = auto_hunt_image_paths(
            run_dir,
            str(row.get("source_id", "")),
            str(row.get("source_question_id", "")),
            urls,
        )

    image_paths = manual_images or auto_images
    if image_paths and wants_image:
        exhibit_status = "image"
    elif wants_image and exhibit_status == "missing-image" and not image_paths:
        pass  # keep missing-image + warning
    elif not wants_image and exhibit_status not in ("cli", "missing-cli"):
        exhibit_status = "none" if exhibit_status == "missing-image" else exhibit_status

    return stem, exhibit_text, exhibit_status, image_paths if wants_image else []


def exhibit_warning(status: str, source_url: str, images_rel_prefix: str) -> list[str]:
    if status == "missing-image":
        return [
            "> [!warning] Exhibit not captured",
            "> Stem references an **exhibit** (diagram/screenshot). Save the exhibit image under "
            f"`{images_rel_prefix}/images/` and re-run export.",
            f"> [Source page]({source_url})",
            "",
        ]
    if status == "missing-cli":
        return [
            "> [!warning] Exhibit CLI / command not captured",
            "> Stem references output or a command that was not extracted by the poll.",
            f"> Open the [source page]({source_url}) and paste the transcript in **Exhibit** below.",
            "",
        ]
    return []


def format_exhibit_image_block(
    image_path: Path,
    *,
    image_rel: str,
    vault_path: str,
) -> list[str]:
    return [
        "**Exhibit**",
        "",
        f"![Exhibit]({image_rel})",
        "",
        f"`{vault_path}`",
        "",
    ]


def format_exhibit_cli_block(exhibit_text: str) -> list[str]:
    return [
        "**Exhibit (CLI / code transcript)**",
        "",
        "```text",
        exhibit_text,
        "```",
        "",
    ]
