#!/usr/bin/env python3
"""Create -test.html sandbox copies of CCNA labs with free-order Submit Lab UI (not production)."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LABS = ROOT / "public" / "CCNA-Study" / "CCNA_labs"

LAB_CHECK_CSS = """
    .lab-check-result {
      display: none;
      margin-top: 14px;
      padding: 14px 16px;
      border-radius: 10px;
      line-height: 1.5;
      font-size: 0.9rem;
      text-align: left;
    }
    .lab-check-result.visible {
      display: block;
    }
    .lab-check-result.is-pass {
      background: #113e2d;
      border: 1px solid #1f7a58;
      color: #d1fae5;
    }
    .lab-check-result.is-fail {
      background: #3a1f24;
      border: 1px solid #7a2f3d;
      color: #fecdd3;
    }
    .lab-check-result ul {
      margin: 8px 0 0;
      padding-left: 1.25rem;
    }
    .lab-check-result li {
      margin: 4px 0;
      font-family: "SF Mono", ui-monospace, Consolas, monospace;
      font-size: 0.82rem;
    }
    .freeorder-test-banner {
      margin: 0 0 14px;
      padding: 10px 14px;
      border-radius: 8px;
      background: #2a2414;
      border: 1px solid #8a6d2f;
      color: #fde68a;
      font-size: 0.9rem;
      line-height: 1.45;
    }
"""

ENGINE_SCRIPTS = """
  <script src="/CCNA-Study/js/cli-lab-freeorder-shared.js"></script>
  <script src="/CCNA-Study/js/cli-lab-freeorder-engines.js"></script>
"""

SUBMIT_BTN = """
          <button type="button" class="device-link" id="checkLabBtn">Submit Lab</button>
"""

LAB_CHECK_DIV = """
        <div id="labCheckResult" class="lab-check-result" role="status" aria-live="polite"></div>
"""

TEST_BANNER = """
        <p class="freeorder-test-banner" role="note">
          <strong>TEST sandbox</strong> — free-order config + Submit Lab grading. Production lab unchanged until you promote this build.
        </p>
"""

SOURCES = [
    "cli-lab-ospf_config_sim_v3.html",
    "cli-lab-static-routing.html",
    "ipv4_ipv6_assign.html",
    "cli-lab-native_vlan_lacp.html",
    "cli-lab-named-acl-snoopimg.html",
    "cli-lab-ip-services-sim-v2.html",
    "cli-lab-trunk_lacp.html",
]


def dest_name(src: str) -> str:
    if src.endswith(".html"):
        return src[:-5] + "-test.html"
    return src + "-test.html"


def patch_html(text: str, src: str) -> str:
    prod = src
    test = dest_name(src)

    text = re.sub(
        r"^<!doctype html>\n<!--",
        "<!doctype html>\n<!--\n  TEST COPY — sandbox for free-order + Submit Lab. Production: "
        + prod
        + "\n  -->\n<!--",
        text,
        count=1,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r'<meta name="robots" content="[^"]*"\s*/>',
        '<meta name="robots" content="noindex, nofollow" />',
        text,
        count=1,
    )
    if 'name="robots"' not in text:
        text = text.replace(
            "<meta charset",
            '<meta name="robots" content="noindex, nofollow" />\n  <meta charset',
            1,
        )

    text = re.sub(r"(<title>)([^<]+)(</title>)", r"\1[TEST] \2\3", text, count=1)
    text = re.sub(r"(<h1>)([^<]+)(</h1>)", r"\1[TEST] \2\3", text, count=1)

    if ".lab-check-result" not in text:
        text = text.replace("  </style>", LAB_CHECK_CSS + "  </style>", 1)

    if 'cli-lab-freeorder-shared.js' not in text:
        text = text.replace(
            '<script src="/js/cli-lab-container.js"></script>',
            '<script src="/js/cli-lab-container.js"></script>' + ENGINE_SCRIPTS,
            1,
        )

    if "freeorder-test-banner" not in text:
        text = text.replace("<main class=\"card\">", "<main class=\"card\">" + TEST_BANNER, 1)

    if 'id="checkLabBtn"' not in text:
        text = re.sub(
            r'(<button type="button" class="device-link" id="openSpoilerBtn">Spoiler</button>)',
            SUBMIT_BTN + r"\n          \1",
            text,
            count=1,
        )

    if 'id="labCheckResult"' not in text:
        text = re.sub(
            r'(<div id="passBanner" class="pass-banner"[^>]*>)',
            LAB_CHECK_DIV + r"\n        \1",
            text,
            count=1,
        )

    return text


def main() -> None:
    for src in SOURCES:
        src_path = LABS / src
        if not src_path.is_file():
            print(f"skip missing {src_path}")
            continue
        dest_path = LABS / dest_name(src)
        shutil.copy2(src_path, dest_path)
        content = dest_path.read_text(encoding="utf-8")
        dest_path.write_text(patch_html(content, src), encoding="utf-8")
        print(f"wrote {dest_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
