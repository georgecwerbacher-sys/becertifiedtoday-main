#!/usr/bin/env python3
"""Generate Security+ practice question HTML under public/COMP_TIA_SEC+/SEC+_Questions/."""
from __future__ import annotations

import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "public/COMP_TIA_SEC+/SEC+_Questions"
HUB_JS = ROOT / "public/COMP_TIA_SEC+/js/secplus-practice-hub.js"
TOPIC_MAP = ROOT / "public/COMP_TIA_SEC+/data/secplus-question-topic-map.json"
OBJECTIVES_JSON = ROOT / "public/COMP_TIA_SEC+/data/secplus-exam-objectives-sy0-701.json"
PORTAL_HOME = "/COMP_TIA_SEC+/SEC+_Training_Portal.html"
QUESTIONS_BASE = "/COMP_TIA_SEC+/SEC+_Questions/"
SECPLUS_BANK_VERSION_LABEL = "Version: 1.1 2026"

STYLE = r"""  <style>
    :root {
      color-scheme: light dark;
      font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
    }
    body {
      margin: 0;
      min-height: 100vh;
      display: grid;
      place-items: center;
      background: #ffffff;
      color: #e6edf3;
      padding: 16px 16px calc(80px + env(safe-area-inset-bottom, 0px));
      box-sizing: border-box;
    }
    .card {
      width: min(900px, 100%);
      background: #121a2b;
      border: 1px solid #2d3b5a;
      border-radius: 14px;
      padding: 28px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
      display: flex;
      flex-direction: column;
    }
    .secplus-objective-tag {
      margin-top: 18px;
      align-self: flex-start;
      max-width: 100%;
      padding: 10px 12px;
      border-radius: 10px;
      border: 1px solid #2d3b5a;
      background: #0f1729;
      color: #b8c3d6;
      font-size: 0.65rem;
      line-height: 1.45;
      text-align: left;
    }
    .secplus-objective-tag__version {
      margin-bottom: 6px;
      color: #9fb0cc;
      font-size: 0.62rem;
    }
    .secplus-objective-tag__title {
      font-weight: 700;
      color: #e6edf3;
      margin-bottom: 4px;
    }
    .secplus-objective-tag__row {
      margin: 2px 0;
    }
    .secplus-exhibit {
      margin: 0 0 18px;
      overflow-x: auto;
    }
    .secplus-exhibit-lead {
      margin: 0 0 12px;
      color: #b8c3d6;
      font-size: 1rem;
      line-height: 1.45;
    }
    .secplus-exhibit-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.92rem;
    }
    .secplus-exhibit-table th,
    .secplus-exhibit-table td {
      border: 1px solid #2d3b5a;
      padding: 10px 12px;
      text-align: left;
      vertical-align: top;
    }
    .secplus-exhibit-table th {
      background: #1a253b;
      color: #e6edf3;
      font-weight: 700;
    }
    .secplus-exhibit-table td {
      background: #0f1729;
      color: #d4dce8;
    }
    .secplus-exhibit-table td.hash-cell,
    .secplus-exhibit-table td.mono-cell {
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.84rem;
      word-break: break-all;
    }
    .secplus-exhibit-question {
      margin: 16px 0 0;
      font-size: clamp(1.05rem, 2vw, 1.45rem);
      font-weight: 700;
      line-height: 1.35;
      color: #e6edf3;
    }
    .secplus-exhibit-log pre {
      margin: 0;
      padding: 14px 16px;
      border-radius: 10px;
      border: 1px solid #2d3b5a;
      background: #0a0e14;
      color: #e6edf3;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.88rem;
      line-height: 1.5;
      white-space: pre;
      overflow-x: auto;
    }
    h1 {
      margin: 0 0 8px;
      font-size: clamp(1.05rem, 2vw, 1.45rem);
      line-height: 1.35;
    }
    .choice {
      display: block;
      margin: 10px 0;
      padding: 12px 14px;
      border-radius: 10px;
      background: #1a253b;
      border: 1px solid #2c3f62;
      font-size: 1.02rem;
      cursor: pointer;
    }
    .choice input {
      margin-right: 10px;
      transform: translateY(1px);
    }
    .question-nav {
      margin: 0 0 20px;
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      justify-content: space-between;
    }
    .question-nav-links {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
    }
    .question-nav .nav-link {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      text-decoration: none;
      color: #f3e8ff;
      background: #5b21b6;
      border: 1px solid #7c3aed;
      border-radius: 10px;
      padding: 10px 16px;
      font-weight: 700;
      font-size: 0.95rem;
      font-family: inherit;
      cursor: pointer;
    }
    .question-nav .nav-link--disabled {
      opacity: 0.35;
      pointer-events: none;
      cursor: default;
    }
    .question-nav .nav-link:hover {
      filter: brightness(1.08);
    }
    .answer {
      margin-top: 18px;
      padding: 14px;
      border-radius: 10px;
      font-weight: 700;
      display: none;
      line-height: 1.45;
    }
    .answer.correct {
      background: #113e2d;
      border: 1px solid #1f7a58;
    }
    .answer.incorrect {
      background: #442020;
      border: 1px solid #8c3434;
    }
    .answer-actions {
      margin-top: 14px;
    }
    .nav-check {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 10px 16px;
      border-radius: 10px;
      border: 1px solid #7c3aed;
      background: #5b21b6;
      color: #f3e8ff;
      font-weight: 700;
      font-size: 0.95rem;
      font-family: inherit;
      cursor: pointer;
    }
    .nav-check:hover {
      filter: brightness(1.08);
    }
    h1.choose-two-stem {
      margin: 0 0 8px;
      font-size: clamp(1.05rem, 2vw, 1.45rem);
      line-height: 1.35;
    }
  </style>"""


def build_endpoint_audit_report_exhibit() -> str:
    rows = [
        ("10.18.04.42", "BE-AC-11-F1-E4-44", "PC-NY", "user1"),
        ("10.18.04.38", "EB-AC-11-82-42-F3", "PC-CA", "user3"),
        ("10.18.04.59", "28-BB-5A-11-52-29", "PC-PA", "user2"),
        ("10.18.04.58", "28-BB-5A-F0-E9-D1", "PC-TX", "user4"),
        ("10.18.04.22", "EB-AC-11-82-42-F3", "WIN10", "user3"),
        ("10.18.04.26", "BB-28-11-21-A2-73", "PC-NJ", "admin"),
    ]
    body_rows = "\n".join(
        "          <tr>"
        f'<td class="mono-cell">{html.escape(ip)}</td>'
        f'<td class="mono-cell">{html.escape(mac)}</td>'
        f"<td>{html.escape(host)}</td>"
        f"<td>{html.escape(acct)}</td>"
        "</tr>"
        for ip, mac, host, acct in rows
    )
    return (
        '    <div class="secplus-exhibit" role="region" aria-label="Endpoint audit report">\n'
        '      <p class="secplus-exhibit-lead">'
        "A security analyst finds a rogue device during a monthly audit of current endpoint assets that are "
        "connected to the network. The corporate network utilizes 802.1X for access control. To be allowed "
        "on the network, a device must have a known hardware address, and a valid user name and password "
        "must be entered in a captive portal. The following is the audit report:"
        "</p>\n"
        '      <table class="secplus-exhibit-table">\n'
        "        <thead>\n"
        "          <tr><th scope=\"col\">IP address</th><th scope=\"col\">MAC</th>"
        "<th scope=\"col\">Host</th><th scope=\"col\">Account</th></tr>\n"
        "        </thead>\n"
        "        <tbody>\n"
        f"{body_rows}\n"
        "        </tbody>\n"
        "      </table>\n"
        '      <p class="secplus-exhibit-question">'
        "Which of the following is the most likely way a rogue device was allowed to connect?"
        "</p>\n"
        "    </div>"
    )


def build_failed_auth_event_log_exhibit() -> str:
    log = (
        "184.168.131.241 - userA - failed authentication\n"
        "184.168.131.241 - userA - failed authentication\n"
        "184.168.131.241 - userB - failed authentication\n"
        "184.168.131.241 - userB - failed authentication\n"
        "184.168.131.241 - userC - failed authentication\n"
        "184.168.131.241 - userC - failed authentication"
    )
    return (
        '    <div class="secplus-exhibit secplus-exhibit-log" role="region" aria-label="Authentication event log">\n'
        '      <p class="secplus-exhibit-lead">'
        "The security operations center is researching an event concerning a suspicious IP address. "
        "A security analyst looks at the following event logs and discovers that a significant portion "
        "of the user accounts have experienced failed log-in attempts when authenticating from the same "
        "IP address:"
        "</p>\n"
        f"      <pre>{html.escape(log)}</pre>\n"
        '      <p class="secplus-exhibit-question">'
        "Which of the following most likely describes the attack that took place?"
        "</p>\n"
        "    </div>"
    )


def build_xss_script_tag_log_exhibit() -> str:
    snippet = "<script>function(send_info)</script>"
    return (
        '    <div class="secplus-exhibit secplus-exhibit-log" role="region" '
        'aria-label="Suspicious script in logs">\n'
        '      <p class="secplus-exhibit-lead">'
        "While reviewing logs, a security administrator identifies the following code:"
        "</p>\n"
        f"      <pre>{html.escape(snippet)}</pre>\n"
        '      <p class="secplus-exhibit-question">'
        "Which of the following best describes the vulnerability being exploited?"
        "</p>\n"
        "    </div>"
    )


def build_login_rejected_spring2023_spraying_exhibit() -> str:
    log = (
        "[10:00:00 AM] Login rejected - username administrator - password Spring2023\n"
        "[10:00:01 AM] Login rejected - username jsmith - password Spring2023\n"
        "[10:00:01 AM] Login rejected - username guest - password Spring2023\n"
        "[10:00:02 AM] Login rejected - username cpolk - password Spring2023\n"
        "[10:00:03 AM] Login rejected - username fmartin - password Spring2023"
    )
    return (
        '    <div class="secplus-exhibit secplus-exhibit-log" role="region" '
        'aria-label="Server login rejection log">\n'
        '      <p class="secplus-exhibit-lead">'
        "A security analyst is reviewing the following logs:"
        "</p>\n"
        f"      <pre>{html.escape(log)}</pre>\n"
        '      <p class="secplus-exhibit-question">'
        "Which of the following attacks is most likely occurring?"
        "</p>\n"
        "    </div>"
    )


def build_windows_4625_bruteforce_exhibit() -> str:
    entry = (
        "Event ID: 4625 — An account failed to log on.\n"
        "  Account Name: Administrator\n"
        "  Failure Reason: Unknown user name or bad password.\n"
        "  Status: 0xC000006D    Sub Status: 0xC000006A\n"
        "  Source Network Address: 203.0.113.44"
    )
    log = "\n\n".join(
        f"{entry}\n  Date/Time: 2024-06-12T14:02:{sec:02d}"
        for sec in (11, 14, 17, 20, 23)
    )
    return (
        '    <div class="secplus-exhibit secplus-exhibit-log" role="region" '
        'aria-label="Windows Security log excerpt">\n'
        '      <p class="secplus-exhibit-lead">'
        "An administrator is reviewing a single server's security logs and discovers the "
        "following:"
        "</p>\n"
        f"      <pre>{html.escape(log)}</pre>\n"
        '      <p class="secplus-exhibit-question">'
        "Which of the following best describes the action captured in this log file?"
        "</p>\n"
        "    </div>"
    )


def build_jsmith_domain_mfa_log_exhibit() -> str:
    log = (
        "Date/Time              User    Event                       Result\n"
        "2024-06-12 14:02:11   jsmith  Password authentication     Success\n"
        "2024-06-12 14:02:12   jsmith  MFA authentication          Failed — Invalid code\n"
        "2024-06-12 14:02:15   jsmith  Password authentication     Success\n"
        "2024-06-12 14:02:16   jsmith  MFA authentication          Failed — Invalid code\n"
        "2024-06-12 14:02:19   jsmith  Password authentication     Success\n"
        "2024-06-12 14:02:20   jsmith  MFA authentication          Failed — Invalid code\n"
        "2024-06-12 14:02:23   jsmith  Password authentication     Success\n"
        "2024-06-12 14:02:24   jsmith  MFA authentication          Failed — Invalid code"
    )
    return (
        '    <div class="secplus-exhibit secplus-exhibit-log" role="region" '
        'aria-label="Domain activity log excerpt">\n'
        '      <p class="secplus-exhibit-lead">'
        "A security analyst reviews domain activity logs and notices the following:"
        "</p>\n"
        f"      <pre>{html.escape(log)}</pre>\n"
        "    </div>"
    )


def build_ids_database_credential_replay_exhibit() -> str:
    lines = [
        "2025-04-10 14:22:01.4532 — Source IP: 192.168.15.101 — Status: Failed — User: JDoe — Action: Login Attempt",
        "2025-04-10 14:22:02.1122 — Source IP: 192.168.15.102 — Status: Failed — User: JDoe — Action: Login Attempt",
        "2025-04-10 14:22:02.7835 — Source IP: 192.168.15.103 — Status: Failed — User: JDoe — Action: Login Attempt",
        "2025-04-10 14:22:03.5637 — Source IP: 192.168.15.104 — Status: Failed — User: JDoe — Action: Login Attempt",
        "2025-04-10 14:22:04.9474 — Source IP: 192.168.15.105 — Status: Failed — User: JDoe — Action: Login Attempt",
        "2025-04-10 14:22:05.5673 — Source IP: 192.168.15.106 — Status: Failed — User: JDoe — Action: Login Attempt",
        "2025-04-10 14:22:06.1573 — Source IP: 192.168.15.107 — Status: Failed — User: JDoe — Action: Login Attempt",
        "2025-04-10 14:22:07.7462 — Source IP: 192.168.15.108 — Status: Failed — User: JDoe — Action: Login Attempt",
    ]
    log = "\n".join(lines)
    return (
        '    <div class="secplus-exhibit secplus-exhibit-log" role="region" '
        'aria-label="IDS database login attempt log">\n'
        '      <p class="secplus-exhibit-lead">Based on the following log output:</p>\n'
        f"      <pre>{html.escape(log)}</pre>\n"
        '      <p class="secplus-exhibit-question">'
        "Which of the following types of network attacks is most likely occurring?"
        "</p>\n"
        "    </div>"
    )


def build_vpn_impossible_travel_log_exhibit() -> str:
    log = (
        "09:12:03  jsmith  VPN login SUCCESS  Chicago, IL\n"
        "09:18:41  jsmith  VPN login SUCCESS  Chicago, IL\n"
        "09:22:15  jsmith  VPN login SUCCESS  Chicago, IL\n"
        "09:24:02  jsmith  VPN login SUCCESS  Rome, Italy\n"
        "09:31:47  jsmith  VPN login SUCCESS  Chicago, IL\n"
        "09:38:22  jsmith  VPN login SUCCESS  Chicago, IL"
    )
    return (
        '    <div class="secplus-exhibit secplus-exhibit-log" role="region" '
        'aria-label="VPN login log summary">\n'
        '      <p class="secplus-exhibit-lead">'
        "A security analyst is reviewing the following logs about a suspicious activity alert for a "
        "user's VPN log-ins:"
        "</p>\n"
        f"      <pre>{html.escape(log)}</pre>\n"
        '      <p class="secplus-exhibit-question">'
        "Which of the following malicious activity indicators triggered the alert?"
        "</p>\n"
        "    </div>"
    )


def build_visitor_badge_concurrent_session_exhibit() -> str:
    log = (
        "Alert: Concurrent session usage\n"
        "Application: Visitor Badge Management\n"
        "User: receptionist01\n"
        "Session 1: VMS-RECEPTION-01 — Active since 10:14:22\n"
        "Session 2: VMS-RECEPTION-02 — Active since 10:14:25\n"
        "Status: Two active sessions for the same account"
    )
    return (
        '    <div class="secplus-exhibit secplus-exhibit-log" role="region" '
        'aria-label="Visitor badge system alert details">\n'
        '      <p class="secplus-exhibit-lead">'
        "A security analyst receives an alert from a corporate endpoint used by employees to issue "
        "visitor badges. The alert contains the following details:"
        "</p>\n"
        f"      <pre>{html.escape(log)}</pre>\n"
        '      <p class="secplus-exhibit-question">'
        "Which of the following best describes the indicator that triggered the alert?"
        "</p>\n"
        "    </div>"
    )


def build_web_server_command_injection_useragent_exhibit() -> str:
    log = (
        '149.34.228.10 - - [28/Jan/2023:16:32:45 -0300] "GET / HTTP/1.0" '
        "User-Agent: $(/bin/sh id) 200 397"
    )
    return (
        '    <div class="secplus-exhibit secplus-exhibit-log" role="region" '
        'aria-label="Web server access log">\n'
        '      <p class="secplus-exhibit-lead">'
        "A security analyst is reviewing logs and discovers the following:"
        "</p>\n"
        f"      <pre>{html.escape(log)}</pre>\n"
        '      <p class="secplus-exhibit-question">'
        "Which of the following should be used to best mitigate this type of attack?"
        "</p>\n"
        "    </div>"
    )


def build_web_server_directory_traversal_log_exhibit() -> str:
    log = (
        "GET /image?filename=../../../etc/passwd\n"
        "Host: AcmeInc.web.net useragent: python-request/2.27.1\n"
        "GET /image?filename=../../../etc/shadow\n"
        "Host: AcmeInc.web.net useragent: python-request/2.27.1"
    )
    return (
        '    <div class="secplus-exhibit secplus-exhibit-log" role="region" aria-label="Web server logs">\n'
        '      <p class="secplus-exhibit-lead">'
        "A security analyst receives an alert from a web server that contains the following logs:"
        "</p>\n"
        f"      <pre>{html.escape(log)}</pre>\n"
        '      <p class="secplus-exhibit-question">'
        "Which of the following attacks is being attempted?"
        "</p>\n"
        "    </div>"
    )


def build_file_server_resource_exhibit() -> str:
    return (
        '    <div class="secplus-exhibit" role="region" aria-label="Server management metrics">\n'
        '      <p class="secplus-exhibit-lead">'
        "A systems administrator receives an alert that a company's internal file server is very slow and "
        "is only working intermittently. The systems administrator reviews the server management software "
        "and finds the following information about the server:"
        "</p>\n"
        '      <table class="secplus-exhibit-table">\n'
        "        <thead>\n"
        "          <tr>"
        '<th scope="col">ServerName</th>'
        '<th scope="col">#Connections</th>'
        '<th scope="col">CPU%</th>'
        '<th scope="col">MEM%</th>'
        '<th scope="col">Read/s</th>'
        '<th scope="col">Writes/s</th>'
        "</tr>\n"
        "        </thead>\n"
        "        <tbody>\n"
        "          <tr>"
        "<td>FileSev01</td>"
        "<td>12</td>"
        '<td class="mono-cell">99.6%</td>'
        '<td class="mono-cell">97%</td>'
        "<td>50KB/s</td>"
        "<td>100KB/s</td>"
        "</tr>\n"
        "        </tbody>\n"
        "      </table>\n"
        '      <p class="secplus-exhibit-question">'
        "Which of the following indicators most likely triggered this alert?"
        "</p>\n"
        "    </div>"
    )


def build_md5_local_password_exhibit() -> str:
    rows = [
        ("ACCT-PC-1", "admin", "f1bdf5ed1d7ad7ede4e3809bd35644b0"),
        ("HR-PC-1", "admin", "d706ab8258fe67c131ebc57a6e28184"),
        ("IT-PC-2", "admin", "f8ddb9cbb321d7dfbf6cb059736f0b3d"),
        ("FILE-SRV-1", "admin", "f054bbd2f5ebab9cb5571000b2c60c02"),
        ("DB-SRV-1", "admin", "8638f732ba7cf2d95b16979e2725da78"),
    ]
    body_rows = "\n".join(
        "          <tr>"
        f"<td>{html.escape(host)}</td>"
        f"<td>{html.escape(acct)}</td>"
        f'<td class="hash-cell">{html.escape(digest)}</td>'
        "</tr>"
        for host, acct, digest in rows
    )
    return (
        '    <div class="secplus-exhibit" role="region" aria-label="Recorded password hashes">\n'
        '      <p class="secplus-exhibit-lead">'
        "A security administrator recently reset local passwords and the following values "
        "were recorded in the system:</p>\n"
        '      <table class="secplus-exhibit-table">\n'
        "        <thead>\n"
        "          <tr><th scope=\"col\">Host</th><th scope=\"col\">Account</th>"
        "<th scope=\"col\">MD5 password values</th></tr>\n"
        "        </thead>\n"
        "        <tbody>\n"
        f"{body_rows}\n"
        "        </tbody>\n"
        "      </table>\n"
        '      <p class="secplus-exhibit-question">'
        "Which of the following is the security administrator most likely protecting against?"
        "</p>\n"
        "    </div>"
    )


def build_question_nav(prev_slug: str | None, next_slug: str | None) -> str:
    parts: list[str] = []
    if prev_slug:
        parts.append(
            f'      <a class="nav-link nav-prev" href="{QUESTIONS_BASE}{html.escape(prev_slug)}.html">Back</a>'
        )
    else:
        parts.append(
            '      <span class="nav-link nav-prev nav-link--disabled" aria-hidden="true">Back</span>'
        )
    parts.append(f'      <a class="nav-link nav-home" href="{PORTAL_HOME}">Home</a>')
    if next_slug:
        parts.append(
            f'      <a class="nav-link nav-next next-link" href="{QUESTIONS_BASE}{html.escape(next_slug)}.html">Next</a>'
        )
    else:
        parts.append(
            '      <span class="nav-link nav-next nav-link--disabled" aria-hidden="true">Next</span>'
        )
    links = "\n".join(parts)
    return (
        '    <nav class="question-nav" aria-label="Question navigation">\n'
        '      <div class="question-nav-links">\n'
        f"{links}\n"
        "      </div>\n"
        "    </nav>"
    )


def choice_line(name: str, letter: str, text: str) -> str:
    t = html.escape(text, quote=False)
    return f'    <label class="choice"><input type="radio" name="{name}" value="{letter}" />{letter}. {t}</label>'


def checkbox_choice_line(name: str, letter: str, text: str) -> str:
    t = html.escape(text, quote=False)
    return f'    <label class="choice"><input type="checkbox" name="{name}" value="{letter}" />{letter}. {t}</label>'


def _load_objective_lookups() -> tuple[dict[str, str], dict[str, tuple[str, str]]]:
    domain_lookup: dict[str, str] = {}
    objective_lookup: dict[str, tuple[str, str]] = {}
    if not OBJECTIVES_JSON.is_file():
        return domain_lookup, objective_lookup
    data = json.loads(OBJECTIVES_JSON.read_text(encoding="utf-8"))
    for domain in data.get("domains") or []:
        did = domain.get("id")
        dname = domain.get("name") or ""
        if did:
            domain_lookup[str(did)] = str(dname)
        for obj in domain.get("objectives") or []:
            oid = obj.get("id")
            if oid:
                objective_lookup[str(oid)] = (dname, str(obj.get("text") or ""))
    return domain_lookup, objective_lookup


def objective_label(
    oid: str,
    domain_lookup: dict[str, str],
    objective_lookup: dict[str, tuple[str, str]],
) -> str:
    if oid in domain_lookup:
        return f"{oid} ({domain_lookup[oid]})"
    if oid in objective_lookup:
        dname, text = objective_lookup[oid]
        return f"{oid} ({dname}): {text}"
    return oid


def build_objective_footer(
    objective_ids: list[str],
    domain_lookup: dict[str, str],
    objective_lookup: dict[str, tuple[str, str]],
) -> str:
    if not objective_ids:
        return ""
    rows = [
        f'      <div class="secplus-objective-tag__row">• {html.escape(objective_label(oid, domain_lookup, objective_lookup))}</div>'
        for oid in objective_ids
    ]
    body = "\n".join(rows)
    version = html.escape(SECPLUS_BANK_VERSION_LABEL)
    return (
        '    <div class="secplus-objective-tag ccna-objective-tag" aria-label="Security+ objective section">\n'
        f'      <div class="secplus-objective-tag__version">{version}</div>\n'
        '      <div class="secplus-objective-tag__title">Security+ objective section</div>\n'
        f"{body}\n"
        "    </div>"
    )


def render_page(
    *,
    title: str,
    slug: str,
    stem: str,
    choices: list[str],
    name: str,
    correct: str,
    explain: str,
    prev_slug: str | None,
    next_slug: str | None,
    prepend_html: str = "",
    objective_ids: list[str] | None = None,
    domain_lookup: dict[str, str] | None = None,
    objective_lookup: dict[str, tuple[str, str]] | None = None,
) -> str:
    nav = build_question_nav(prev_slug, next_slug)
    objective_footer = build_objective_footer(
        objective_ids or [],
        domain_lookup or {},
        objective_lookup or {},
    )
    choices_html = "\n".join(
        choice_line(name, chr(ord("A") + i), text) for i, text in enumerate(choices)
    )
    msg_json = json.dumps(explain)
    stem_h = html.escape(stem.strip()) if stem.strip() else ""
    stem_block = f"    <h1>{stem_h}</h1>\n\n" if stem_h else ""
    prepend = f"{prepend_html.rstrip()}\n" if prepend_html else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="robots" content="index, follow" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(title)}</title>
{STYLE}
  <link rel="stylesheet" href="/COMP_TIA_SEC+/SEC+_Samples/secplus-sample-touch.css" />
</head>
<body>
  <script src="/js/sample-url-mask-apply.js"></script>
  <script src="/COMP_TIA_SEC+/js/secplus-practice-nav.js" defer></script>
  <main class="card">
{nav}
{prepend}{stem_block}{choices_html}

    <div id="answerBox" class="answer" aria-live="polite"></div>
{objective_footer}
  </main>

  <script>
    (function () {{
      var CORRECT = {json.dumps(correct)};
      var CORRECT_MSG = {msg_json};
      var answerBox = document.getElementById("answerBox");

      function applyFeedback(value) {{
        answerBox.style.display = "block";
        if (value === CORRECT) {{
          answerBox.className = "answer correct";
          answerBox.textContent = CORRECT_MSG;
        }} else {{
          answerBox.className = "answer incorrect";
          answerBox.textContent = "Incorrect.";
        }}
      }}

      document.querySelectorAll('input[name="{name}"]').forEach(function (el) {{
        el.addEventListener("change", function () {{
          if (el.checked) {{
            applyFeedback(el.value);
          }}
        }});
      }});
    }})();
  </script>
</body>
</html>
"""


def render_page_choose_two(
    *,
    title: str,
    choices: list[str],
    name: str,
    correct: list[str],
    explain: str,
    stem: str,
    prev_slug: str | None,
    next_slug: str | None,
    prepend_html: str = "",
    objective_ids: list[str] | None = None,
    domain_lookup: dict[str, str] | None = None,
    objective_lookup: dict[str, tuple[str, str]] | None = None,
) -> str:
    nav = build_question_nav(prev_slug, next_slug)
    objective_footer = build_objective_footer(
        objective_ids or [],
        domain_lookup or {},
        objective_lookup or {},
    )
    choices_html = "\n".join(
        checkbox_choice_line(name, chr(ord("A") + i), text) for i, text in enumerate(choices)
    )
    cor_json = json.dumps(sorted(correct))
    msg_json = json.dumps(explain)
    stem_h = html.escape(stem.strip())
    prepend = f"{prepend_html.rstrip()}\n" if prepend_html else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="robots" content="index, follow" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(title)}</title>
{STYLE}
  <link rel="stylesheet" href="/COMP_TIA_SEC+/SEC+_Samples/secplus-sample-touch.css" />
</head>
<body>
  <script src="/js/sample-url-mask-apply.js"></script>
  <script src="/COMP_TIA_SEC+/js/secplus-practice-nav.js" defer></script>
  <main class="card">
{nav}
{prepend}    <h1 class="choose-two-stem">{stem_h}</h1>

{choices_html}

    <div class="answer-actions">
      <button id="checkBtn" type="button" class="nav-check">Check answer</button>
    </div>
    <div id="answerBox" class="answer" aria-live="polite"></div>
{objective_footer}
  </main>

  <script>
    (function () {{
      var CORRECT = {cor_json};
      var CORRECT_MSG = {msg_json};
      var checkBtn = document.getElementById("checkBtn");
      var answerBox = document.getElementById("answerBox");

      function selectedValues() {{
        return []
          .slice.call(document.querySelectorAll('input[name="{name}"]:checked'))
          .map(function (el) {{ return el.value; }})
          .sort();
      }}

      function arraysEqual(a, b) {{
        if (a.length !== b.length) return false;
        return a.every(function (v, i) {{ return v === b[i]; }});
      }}

      checkBtn.addEventListener("click", function () {{
        var sel = selectedValues();
        answerBox.style.display = "block";
        if (sel.length !== 2) {{
          answerBox.className = "answer incorrect";
          answerBox.textContent = "Choose exactly two answers.";
          return;
        }}
        if (arraysEqual(sel, CORRECT)) {{
          answerBox.className = "answer correct";
          answerBox.textContent = CORRECT_MSG;
        }} else {{
          answerBox.className = "answer incorrect";
          answerBox.textContent = "Incorrect.";
        }}
      }});
    }})();
  </script>
</body>
</html>
"""


# Extend this list for new questions (same shape as CCNA gen_ccna_chain_pages.py entries).
CHAIN: list[dict] = [
    {
        "slug": "pentest-hypervisor-vm-escape",
        "title": "Security+ — VM escape (hypervisor pentest)",
        "stem": (
            "During a penetration test in a hypervisor, the security engineer is able to use a script "
            "to inject a malicious payload and access the host filesystem. Which of the following "
            "best describes this vulnerability?"
        ),
        "name": "secplus_q1",
        "correct": "A",
        "explain": (
            "Correct. A — VM escape is when guest code breaks out of the virtual machine boundary "
            "to reach the hypervisor or host OS (for example, accessing the host filesystem). "
            "Cross-site scripting affects browsers, malicious update describes tampered software "
            "distribution, and SQL injection targets database queries."
        ),
        "choices": [
            "VM escape",
            "Cross-site scripting",
            "Malicious update",
            "SQL injection",
        ],
        "objectives": ["2.3", "3.1"],
    },
    {
        "slug": "public-download-code-signing-integrity",
        "title": "Security+ — Code signing (downloaded software integrity)",
        "stem": (
            "A customer reports that software the customer downloaded from a public website has malware "
            "in it. However, the company that created the software denies any malware in its software at "
            "delivery time. Which of the following techniques will address this concern?"
        ),
        "name": "secplus_q2",
        "correct": "D",
        "explain": (
            "Correct. D — Code signing applies a publisher digital signature so customers can verify the "
            "vendor and detect tampering after release. That supports integrity from delivery through "
            "download. Secure storage protects data at rest, static code analysis finds flaws in source "
            "but does not prove the binary you received is authentic, and input validation guards "
            "application input—not software distribution trust."
        ),
        "choices": [
            "Secure storage",
            "Static code analysis",
            "Input validation",
            "Code signing",
        ],
        "objectives": ["1.4", "2.2"],
    },
    {
        "slug": "mdm-mitigate-jailbreaking-mobile",
        "title": "Security+ — MDM and jailbreaking",
        "stem": (
            "Which of the following vulnerabilities would likely be mitigated by setting up an MDM platform?"
        ),
        "name": "secplus_q3",
        "correct": "C",
        "explain": (
            "Correct. C — Mobile device management (MDM) enforces compliance policies on smartphones "
            "and tablets, including detecting jailbroken or rooted devices and blocking or remediating "
            "them. A TPM is hardware root-of-trust, not an MDM substitute. Buffer overflows and SQL "
            "injection are application flaws addressed through secure development, patching, and input "
            "controls—not mobile fleet policy tools."
        ),
        "choices": [
            "TPM",
            "Buffer overflow",
            "Jailbreaking",
            "SQL injection",
        ],
        "objectives": ["2.3", "4.2"],
    },
    {
        "slug": "authorized-before-authenticated-tailgating",
        "title": "Security+ — Authorization before authentication (tailgating)",
        "stem": (
            "Which of the following describes a situation where a user is authorized before being authenticated?"
        ),
        "name": "secplus_q4",
        "correct": "C",
        "explain": (
            "Correct. C — Tailgating (piggybacking) is when someone enters a restricted area using another "
            "person's successful authentication—gaining physical access (authorization to the space) without "
            "authenticating themselves. Normal AAA order is authenticate first, then authorize. Privilege "
            "escalation raises rights after access, race conditions are timing flaws in software, and "
            "impersonation is falsifying identity—not entering solely on someone else's credential event."
        ),
        "choices": [
            "Privilege escalation",
            "Race condition",
            "Tailgating",
            "Impersonation",
        ],
        "objectives": ["1.2", "2.2"],
    },
    {
        "slug": "kiosk-dns-poisoning-hourly-credentials",
        "title": "Security+ — DNS poisoning and kiosk credential theft",
        "stem": (
            "A security analyst discovers that a large number of employee credentials had been stolen and were "
            "being sold on the dark web. The analyst investigates and discovers that some hourly employee credentials "
            "were compromised, but salaried employee credentials were not affected. "
            "Most employees clocked in and out while they were inside the building using one of the kiosks connected to "
            "the network. However, some clocked out and recorded their time after leaving to go home. Only those who "
            "clocked in and out while inside the building had credentials stolen. Each of the kiosks are on different floors, "
            "and there are multiple routers, since the business segments environments for certain business functions. "
            "Hourly employees are required to use a website called acmetimekeeping.com to clock in and out. This "
            "website is accessible from the internet. Which of the following is the most likely reason for this compromise?"
        ),
        "name": "secplus_q5",
        "correct": "C",
        "explain": (
            "Correct. C — Poisoned internal DNS can redirect acmetimekeeping.com to a look-alike site that "
            "captures credentials and forwards users to the real service. Kiosks inside the building rely on "
            "corporate DNS, so only on-site clock-ins were affected; employees who clocked out from home used "
            "other resolvers and were not redirected. A site-wide brute-force or compromised web app would likely "
            "hit remote users too. ARP poisoning is usually limited to a local segment and does not explain why "
            "only internal kiosk traffic to one hostname was stolen across segmented floors."
        ),
        "choices": [
            "A brute-force attack was used against the time-keeping website to scan for common passwords.",
            (
                "A malicious actor compromised the time-keeping website with malicious code using an unpatched "
                "vulnerability on the site, stealing the credentials."
            ),
            (
                "The internal DNS servers were poisoned and were redirecting acmetimekeeping.com to a malicious domain "
                "that intercepted the credentials and then passed them through to the real site"
            ),
            (
                "ARP poisoning affected the machines in the building and caused the kiosks to send a copy of all the "
                "submitted credentials to a malicious machine."
            ),
        ],
        "objectives": ["2.2", "2.4"],
    },
    {
        "slug": "cloud-international-data-protection-regulations",
        "title": "Security+ — International cloud expansion (data protection)",
        "stem": (
            "A U.S.-based cloud-hosting provider wants to expand its data centers to new international "
            "locations. Which of the following should the hosting provider consider first?"
        ),
        "name": "secplus_q6",
        "correct": "A",
        "explain": (
            "Correct. A — Before building in a new country, a provider must understand local data protection "
            "and privacy laws (residency, cross-border transfer, breach notification, and sector rules). "
            "Noncompliance can block operations or trigger fines. Threat actors abroad, existing contracts, "
            "and time-zone log correlation all matter later in planning, but legal and regulatory requirements "
            "define whether and how the expansion can proceed."
        ),
        "choices": [
            "Local data protection regulations",
            "Risks from hackers residing in other countries",
            "Impacts to existing contractual obligations",
            "Time zone differences in log correlation",
        ],
        "objectives": ["5.4", "5.1"],
    },
    {
        "slug": "reset-local-passwords-pass-the-hash",
        "title": "Security+ — Pass-the-hash (MD5 local password reset)",
        "prepend_html": build_md5_local_password_exhibit(),
        "stem": "",
        "name": "secplus_q7",
        "correct": "C",
        "explain": (
            "Correct. C — The table lists MD5 password hashes after a reset. New hashes invalidate "
            "hashes an attacker may have stolen from memory or credential stores, which blocks "
            "pass-the-hash reuse without cracking plaintext. Account sharing and weak complexity are "
            "policy issues not solved by rotating hashes alone. Password compromise is broader; "
            "resetting hashes specifically targets replay of captured hash material."
        ),
        "choices": [
            "Account sharing",
            "Weak password complexity",
            "Pass-the-hash attacks",
            "Password compromise",
        ],
        "objectives": ["2.5", "4.5"],
    },
    {
        "slug": "credential-harvesting-social-engineering",
        "title": "Security+ — Credential harvesting (social engineering)",
        "stem": (
            "Which of the following would most likely be used by attackers to perform credential harvesting?"
        ),
        "name": "secplus_q8",
        "correct": "A",
        "explain": (
            "Correct. A — Credential harvesting collects usernames and passwords (or session tokens) "
            "from victims, most often through social engineering such as phishing, vishing, or fake "
            "login pages that trick users into entering credentials. Supply chain and trojanized "
            "third-party software can also steal credentials but are not the primary technique named "
            "for harvesting in the SY0-701 threat landscape. Rainbow tables are precomputed hash "
            "lookups used to crack stolen password hashes offline, not to harvest credentials from users."
        ),
        "choices": [
            "Social engineering",
            "Supply chain compromise",
            "Third-party software",
            "Rainbow table",
        ],
        "objectives": ["2.2", "2.5"],
    },
    {
        "slug": "network-segmentation-security-zones-advantage",
        "title": "Security+ — Network segmentation (security zones)",
        "stem": (
            "Which of the following is the greatest advantage that network segmentation provides?"
        ),
        "name": "secplus_q9",
        "correct": "E",
        "explain": (
            "Correct. E — Segmentation divides the network into security zones (for example guest, "
            "internal, DMZ, and management) so policy and trust levels differ by zone and lateral "
            "movement is limited. Encryption protects data in transit but is not the main outcome of "
            "segmentation. Lower resource use or endpoint agents are side benefits, not the greatest "
            "security advantage. Configuration enforcement can follow segmentation but zones are what "
            "segmentation creates."
        ),
        "choices": [
            "End-to-end encryption",
            "Decreased resource utilization",
            "Enhanced endpoint protection",
            "Configuration enforcement",
            "Security zones",
        ],
        "objectives": ["3.2", "2.5"],
    },
    {
        "slug": "dlp-classify-data-before-policies",
        "title": "Security+ — DLP deployment (classify data first)",
        "stem": (
            "A security administrator is deploying a DLP solution to prevent the exfiltration of sensitive customer data. "
            "Which of the following should the administrator do first?"
        ),
        "name": "secplus_q10",
        "correct": "C",
        "explain": (
            "Correct. C — DLP rules need to know what to protect. Classifying or labeling sensitive customer data "
            "(discovery and data categories) comes before writing block rules for email, cloud uploads, or shares. "
            "Blocking cloud sites or stripping share permissions without classification risks blocking legitimate "
            "work or missing unlabeled data paths. Attachment rules alone cannot cover all exfiltration channels until "
            "the sensitive data is identified and tagged."
        ),
        "choices": [
            "Block access to cloud storage websites.",
            "Create a rule to block outgoing email attachments.",
            "Apply classifications to the data.",
            "Remove all user permissions from shares on the file server.",
        ],
        "objectives": ["3.3", "4.2"],
    },
    {
        "slug": "iot-exploit-firewall-logs-first",
        "title": "Security+ — IoT exploit (firewall logs first)",
        "stem": (
            "A security analyst learns that an attack vector, which was used as a part of a recent incident, was a "
            "well-known IoT device exploit. The analyst needs to review logs to identify the time of initial exploit. "
            "Which of the following logs should the analyst review first?"
        ),
        "name": "secplus_q11",
        "correct": "C",
        "explain": (
            "Correct. C — IoT devices often lack rich endpoint logging, but the first network-based exploit attempt "
            "usually appears at a perimeter or zone firewall as allowed or denied connections to the vulnerable "
            "device. Firewall logs help pinpoint when external or lateral traffic first targeted the IoT host. "
            "Wireless AP logs show association and wireless events, not full exploit timing for all IoT paths. "
            "Switch logs are mostly Layer 2 forwarding. NAC logs show admission and posture, not exploit payloads."
        ),
        "choices": [
            "Wireless access point",
            "Switch",
            "Firewall",
            "NAC",
        ],
        "objectives": ["4.4", "3.1"],
    },
    {
        "slug": "ai-ticketing-tool-intellectual-property",
        "title": "Security+ — AI ticketing tool (intellectual property)",
        "stem": (
            "Which of the following data types best describes an AI tool developed by a company to automate the "
            "ticketing system under a specific contract?"
        ),
        "name": "secplus_q12",
        "correct": "D",
        "explain": (
            "Correct. D — A custom AI automation built for a contracted ticketing workflow is proprietary "
            "intellectual property: company-owned software, models, and processes. Classified data is "
            "government-labeled sensitive information, not a label for commercial tooling. Regulated "
            "information describes data governed by law (for example PHI or PCI), which may flow through "
            "the tickets but does not define the tool itself. Open source is publicly licensed code the "
            "company does not own exclusively."
        ),
        "choices": [
            "Classified",
            "Regulated information",
            "Open source",
            "Intellectual property",
        ],
        "objectives": ["3.3", "5.4"],
    },
    {
        "slug": "aaa-accounting-login-time-tracking",
        "title": "Security+ — AAA accounting (login time tracking)",
        "stem": (
            "Which of the following is the primary purpose of a service that tracks log-ins and time spent using "
            "the service?"
        ),
        "name": "secplus_q13",
        "correct": "B",
        "explain": (
            "Correct. B — Accounting in the AAA framework records who accessed a resource, when they logged in, "
            "and how long the session lasted for billing, auditing, and compliance. Authentication proves "
            "identity, authorization decides what you may do, and availability is about uptime and resilience, "
            "not usage metering."
        ),
        "choices": [
            "Availability",
            "Accounting",
            "Authentication",
            "Authorization",
        ],
        "objectives": ["1.2"],
    },
    {
        "slug": "low-cost-standby-warm-site-hardware",
        "title": "Security+ — Warm site (low-cost standby with hardware)",
        "stem": (
            "Which of the following would be the best solution to deploy a low-cost standby site that includes "
            "hardware and internet access?"
        ),
        "name": "secplus_q14",
        "correct": "D",
        "explain": (
            "Correct. D — A warm site balances cost and readiness: space, power, network connectivity, and "
            "partially installed hardware, without the expense of a fully mirrored hot site. A cold site is "
            "cheaper but usually lacks pre-staged servers and active internet. A hot site includes hardware "
            "and connectivity but is the highest-cost option. Recovery site is a general term, not a specific "
            "tier with defined hardware and access."
        ),
        "choices": [
            "Recovery site",
            "Cold site",
            "Hot site",
            "Warm site",
        ],
        "objectives": ["3.4"],
    },
    {
        "slug": "right-to-be-forgotten-remove-data",
        "title": "Security+ — Right to be forgotten (data removal)",
        "stem": (
            "Which of the following actions must an organization take to comply with a person's request for "
            "the right to be forgotten?"
        ),
        "name": "secplus_q15",
        "correct": "C",
        "explain": (
            "Correct. C — The right to be forgotten (data erasure) requires deleting the individual's personal "
            "data from systems when the request is valid, subject to legal exceptions. Encryption or "
            "obfuscation still retains the data and does not satisfy erasure. Purging every PII attribute "
            "organization-wide is not the requirement—the obligation targets that person's records."
        ),
        "choices": [
            "Purge all personally identifiable attributes.",
            "Encrypt all of the data.",
            "Remove all of the person's data.",
            "Obfuscate all of the person's data.",
        ],
        "objectives": ["5.4", "5.1"],
    },
    {
        "slug": "unpatched-app-segmentation-mitigation",
        "title": "Security+ — Unpatched app (segmentation mitigation)",
        "stem": (
            "A security technician determines that no additional patches can be applied to an application and the "
            "risks of operating as such must be accepted. Additionally, only a limited number of network services "
            "should utilize the application. Which of the following best describes this type of mitigation?"
        ),
        "name": "secplus_q16",
        "correct": "B",
        "explain": (
            "Correct. B — When patching is not possible, network segmentation limits which systems and services "
            "can reach the vulnerable application, shrinking blast radius while risk is accepted. Patching is "
            "ruled out by the scenario. Isolation can contain a host but segmentation specifically controls "
            "allowed network paths and which services may use the app. Monitoring observes activity but does "
            "not by itself restrict which services connect."
        ),
        "choices": [
            "Patching",
            "Segmentation",
            "Isolation",
            "Monitoring",
        ],
        "objectives": ["2.5", "3.2"],
    },
    {
        "slug": "wifi-iot-sensors-vlan-segmentation",
        "title": "Security+ — Wi-Fi IoT sensors (VLAN)",
        "stem": (
            "A company wants to use new Wi-Fi-enabled environmental sensors to automatically collect metrics. "
            "Which of the following will the security team most likely do?"
        ),
        "name": "secplus_q17",
        "correct": "B",
        "explain": (
            "Correct. B — IoT and environmental sensors are commonly placed on a dedicated VLAN (or IoT segment) "
            "so they are separated from corporate user and server networks, limiting lateral movement if a "
            "sensor is compromised. Risk-register entries document risk but are not the primary technical "
            "control for deployment. Air gapping conflicts with Wi-Fi cloud/metrics collection. TLS protects "
            "data in transit and should be enabled, but segmentation is the typical first network control."
        ),
        "choices": [
            "Add the sensor software to the risk register.",
            "Create a VLAN for the sensors.",
            "Physically air gap the sensors.",
            "Configure TLS 1.2 on all sensors.",
        ],
        "objectives": ["3.2", "3.1"],
    },
    {
        "slug": "compensating-controls-alternative-measure",
        "title": "Security+ — Compensating controls (definition)",
        "stem": (
            "Which of the following best explains the role of compensating controls?"
        ),
        "name": "secplus_q18",
        "correct": "B",
        "explain": (
            "Correct. B — Compensating controls are alternate safeguards used when the primary or "
            "preferred control (such as patching or upgrading) cannot be applied because of technical, "
            "operational, or business limits. Segmentation that isolates vulnerable components is one "
            "example of a compensating control, not the definition of the concept. Delaying work to a "
            "maintenance window is scheduling, not compensation. Modifying source code is direct "
            "remediation, not a substitute control."
        ),
        "choices": [
            (
                "Reducing the attack surface by isolating vulnerable components within a "
                "segmented environment"
            ),
            "Providing an alternative security measure when standard remediation is not feasible",
            "Delaying remediation timelines by replacing affected systems in a maintenance window",
            "Remediating software flaws by modifying source code to remove insecure functions",
        ],
        "objectives": ["2.5", "1.1"],
    },
    {
        "slug": "download-integrity-verify-hashes",
        "title": "Security+ — File download integrity (hashes)",
        "stem": (
            "A software developer released a new application and is distributing application files via the "
            "developer's website. Which of the following should the developer post on the website to allow "
            "users to verify the integrity of the downloaded files?"
        ),
        "name": "secplus_q19",
        "correct": "A",
        "explain": (
            "Correct. A — Publishing cryptographic hashes (for example SHA-256) lets users compare a hash of "
            "the file they downloaded with the posted value to detect tampering or corruption. Certificates "
            "prove identity or enable TLS or code signing but are not the usual checksum users run locally "
            "on the installer file. Algorithms name the math used; salting adds randomness to passwords before "
            "hashing and does not verify download integrity."
        ),
        "choices": [
            "Hashes",
            "Certificates",
            "Algorithms",
            "Salting",
        ],
        "objectives": ["1.4"],
    },
    {
        "slug": "data-lifecycle-retention-regulations",
        "title": "Security+ — Data retention and regulations",
        "stem": (
            "Which of the following aspects of the data management life cycle is most directly impacted by "
            "local and international regulations?"
        ),
        "name": "secplus_q20",
        "correct": "C",
        "explain": (
            "Correct. C — Privacy and sector laws set how long data may or must be kept, when it must be "
            "deleted, and how retention supports legal holds and audits. Destruction and sanitization are "
            "related end-of-life steps but are often driven by retention policy once legal periods expire. "
            "Certification attests to controls; it is not itself a lifecycle phase shaped chiefly by "
            "retention rules in GDPR, HIPAA, and similar frameworks."
        ),
        "choices": [
            "Destruction",
            "Certification",
            "Retention",
            "Sanitization",
        ],
        "objectives": ["5.4", "4.2"],
    },
    {
        "slug": "decommission-device-encryption-updates",
        "title": "Security+ — Decommission network device (choose two)",
        "stem": (
            "Which of the following are cases in which an engineer should recommend the decommissioning "
            "of a network device? (Select two)."
        ),
        "name": "secplus_q21",
        "choose_two": True,
        "correct": ["E", "F"],
        "explain": (
            "Correct. E and F — Retire gear that cannot meet required encryption and cannot receive "
            "authorized updates; both leave the device unmaintainable or noncompliant. Moving to test or "
            "another site, isolating a segment, or using cleartext passwords are operational or "
            "compensating paths, not the usual reasons to remove a device from service entirely."
        ),
        "choices": [
            "The device has been moved from a production environment to a test environment.",
            "The device is configured to use cleartext passwords.",
            "The device is moved to an isolated segment on the enterprise network.",
            "The device is moved to a different location in the enterprise.",
            "The device's encryption level cannot meet organizational standards.",
            "The device is unable to receive authorized updates.",
        ],
        "objectives": ["4.2", "2.5"],
    },
    {
        "slug": "uat-production-data-masking",
        "title": "Security+ — UAT data (masking)",
        "stem": (
            "An analyst wants to move data from production to the UAT server to test the latest release. "
            "Which of the following strategies should the analyst use to protect sensitive data from being "
            "viewed by the testing team?"
        ),
        "name": "secplus_q22",
        "correct": "A",
        "explain": (
            "Correct. A — Data masking replaces sensitive values with realistic substitutes before data "
            "reaches UAT, so testers can exercise the release without seeing real PII or secrets. "
            "Tokenization swaps values for tokens and is geared toward production payment and lookup "
            "workflows, not typical test-data copies. Obfuscation hides meaning but is less precise than "
            "structured masking for regulated test datasets. Encryption protects confidentiality in transit "
            "or at rest; testers with keys or application access can still decrypt and view the data."
        ),
        "choices": [
            "Data masking",
            "Data tokenization",
            "Data obfuscation",
            "Data encryption",
        ],
        "objectives": ["3.3", "5.4"],
    },
    {
        "slug": "equipment-aro-ten-incidents-five-years",
        "title": "Security+ — ARO (equipment incidents)",
        "stem": (
            "A company performs risk analysis on its equipment and estimates it will experience about ten "
            "incidents over a five-year period. Which of the following is the correct ARO for the equipment?"
        ),
        "name": "secplus_q23",
        "correct": "A",
        "explain": (
            "Correct. A — Annualized rate of occurrence (ARO) is the expected number of times the event "
            "happens in one year: 10 incidents ÷ 5 years = 2 per year. Five and ten are the period length "
            "and total count, not the annualized rate. Fifty would imply an implausible rate for this scenario."
        ),
        "choices": ["2", "5", "10", "50"],
        "objectives": ["5.2"],
    },
    {
        "slug": "multicloud-iaas-vm-resilience",
        "title": "Security+ — Multicloud IaaS resilience",
        "stem": (
            "Which of the following provides resilience by hosting critical VMs within different IaaS providers "
            "while being maintained by internal application owners?"
        ),
        "name": "secplus_q24",
        "correct": "A",
        "explain": (
            "Correct. A — Multicloud spreads critical VMs across more than one infrastructure-as-a-service "
            "provider so an outage at one vendor does not take down every workload; internal teams still own "
            "and maintain the applications on those VMs. SaaS diversity addresses software services, not "
            "customer-managed VMs in IaaS. On-premises load balancing does not use multiple public IaaS "
            "providers. Corporate-owned off-site sites are private facilities, not the multicloud IaaS model "
            "described in the stem."
        ),
        "choices": [
            "Multicloud architectures",
            "SaaS provider diversity",
            "On-premises server load balancing",
            "Corporate-owned, off-site locations",
        ],
        "objectives": ["3.1", "3.4"],
    },
    {
        "slug": "soc-failed-logins-password-spraying",
        "title": "Security+ — Password spraying (auth event log)",
        "stem": "",
        "name": "secplus_q25",
        "correct": "A",
        "explain": (
            "Correct. A — Password spraying uses one or a few common passwords against many accounts "
            "from the same source, with only a couple of failures per user to avoid lockouts. The log "
            "shows one IP (184.168.131.241) and multiple users (userA, userB, userC) each with failed "
            "authentication attempts. Brute-force and dictionary attacks typically hammer one account "
            "with many passwords. Rainbow tables are used offline against stolen password hashes, not "
            "for live authentication log patterns like these."
        ),
        "choices": [
            "Spraying",
            "Brute-force",
            "Dictionary",
            "Rainbow table",
        ],
        "prepend_html": build_failed_auth_event_log_exhibit(),
        "objectives": ["2.4", "4.9"],
    },
    {
        "slug": "os-image-baseline-configuration-first",
        "title": "Security+ — OS image baseline (standardize first)",
        "stem": (
            "An organization has too many variations of a single operating system and needs to standardize "
            "the arrangement prior to pushing the system image to users. Which of the following should the "
            "organization implement first?"
        ),
        "name": "secplus_q26",
        "correct": "D",
        "explain": (
            "Correct. D — A baseline configuration documents the approved secure settings and services for "
            "the OS so every deployed image matches one standard before rollout. Naming conventions help "
            "inventory but do not define how the system is built. Mashing is not a standard step for "
            "defining or deploying a standardized OS image. Network diagrams document topology; they do "
            "not establish the OS build standard itself."
        ),
        "choices": [
            "Standard naming convention",
            "Mashing",
            "Network diagrams",
            "Baseline configuration",
        ],
        "objectives": ["4.2", "3.2"],
    },
    {
        "slug": "zero-trust-policy-engine-access",
        "title": "Security+ — Zero Trust policy engine",
        "stem": (
            "Which of the following best explains the use of a policy engine in a Zero Trust environment?"
        ),
        "name": "secplus_q27",
        "correct": "B",
        "explain": (
            "Correct. B — In Zero Trust, the policy engine decides each access request on current policy and "
            "context; it does not grant ongoing trust because the user authenticated earlier or was approved "
            "for a prior resource (no inherited implied trust). A central server applying default permissions "
            "across many resources resembles static, perimeter-style access, not per-request verification. "
            "Dynamic assignment from identity plus signals is part of evaluation, but the defining role is "
            "fresh decisions per request, not standing permission inherited from past events. Unknown roles "
            "with ML-only control is not how Zero Trust policy engines are defined."
        ),
        "choices": [
            (
                "It is used by a central server to apply default permissions across a range of network "
                "and computing resources."
            ),
            (
                "It is used to make access control decisions without inheriting permission decisions "
                "from prior events."
            ),
            (
                "It is used to dynamically assign user permissions based on a user's identity and "
                "previous activity."
            ),
            (
                "It is used when user roles are unknown and the organization wants to leverage ML "
                "to control access."
            ),
        ],
        "objectives": ["1.2", "3.1"],
    },
    {
        "slug": "design-change-management-review",
        "title": "Security+ — Change management (design change)",
        "stem": (
            "Prior to implementing a design change, the change must go through multiple steps to ensure that "
            "it does not cause any security issues. Which of the following is most likely to be one of those steps?"
        ),
        "name": "secplus_q28",
        "correct": "A",
        "explain": (
            "Correct. A — Formal change management includes management review or approval (often through a "
            "change advisory board) so impact, risk, and security implications are evaluated before "
            "implementation. Load testing checks performance and capacity, not whether the change is "
            "security-safe. Maintenance notifications inform stakeholders of work windows; they do not "
            "validate the change. Procedure updates document how work is done and usually follow approval, "
            "rather than serving as a pre-implementation security gate."
        ),
        "choices": [
            "Management review",
            "Load testing",
            "Maintenance notifications",
            "Procedure updates",
        ],
        "objectives": ["1.3"],
    },
    {
        "slug": "developer-code-signing-application-integrity",
        "title": "Security+ — Code signing (application integrity)",
        "stem": (
            "A software developer wishes to implement an application security technique that will provide "
            "assurance of the application's integrity. Which of the following techniques will achieve this?"
        ),
        "name": "secplus_q29",
        "correct": "D",
        "explain": (
            "Correct. D — Code signing attaches a publisher digital signature so installers and operating "
            "systems can verify the application was not altered after it was signed. Secure cookies protect "
            "session data in web applications but do not prove the binary or package is untampered. Input "
            "validation reduces flawed or malicious input; it does not attest to code integrity. Static "
            "analysis finds defects in source before release; it does not provide runtime assurance that "
            "the distributed application matches the trusted build."
        ),
        "choices": [
            "Secure cookies",
            "Input validation",
            "Static analysis",
            "Code signing",
        ],
        "objectives": ["1.4", "3.3"],
    },
    {
        "slug": "lost-mobile-device-fde",
        "title": "Security+ — FDE (lost mobile device)",
        "stem": (
            "Which of the following should be used to ensure an attacker is unable to read the contents of a "
            "mobile device's drive if the device is lost?"
        ),
        "name": "secplus_q30",
        "correct": "C",
        "explain": (
            "Correct. C — Full disk encryption (FDE) encrypts storage on the device so data stays unreadable "
            "without the correct key or passphrase, even if the drive is removed or imaged. A TPM can "
            "secure keys used for encryption but does not by itself encrypt all user data on the drive. "
            "ECC is an asymmetric algorithm, not a mobile drive protection control. An HSM is typically "
            "an enterprise appliance for centralized key operations, not the standard control for lost "
            "phone or tablet storage."
        ),
        "choices": [
            "TPM",
            "ECC",
            "FDE",
            "HSM",
        ],
        "objectives": ["1.4", "3.3"],
    },
    {
        "slug": "joint-development-ip-moa-breach",
        "title": "Security+ — MOA (joint development IP)",
        "stem": (
            "Company A jointly develops a product with Company B, which is located in a different country. "
            "Company A finds out that their intellectual property is being shared with unauthorized companies. "
            "Which of the following has been breached?"
        ),
        "name": "secplus_q31",
        "correct": "D",
        "explain": (
            "Correct. D — A memorandum of agreement (MOA) between partners defines how joint work is done, "
            "including confidentiality and permitted use of intellectual property; sharing IP with "
            "unauthorized third parties violates that agreement. An SLA covers service levels such as "
            "uptime, not partner IP handling. An AUP governs acceptable use of an organization's systems "
            "by its users. A statement of work (SOW) scopes tasks and deliverables for a project but is "
            "not the primary document for ongoing partner IP boundaries in a joint development relationship."
        ),
        "choices": [
            "SLA",
            "AUP",
            "SOW",
            "MOA",
        ],
        "objectives": ["5.3", "5.4"],
    },
    {
        "slug": "password-hashing-mathematical-algorithms",
        "title": "Security+ — Password hashing",
        "stem": (
            "A security administrator protects passwords by using hashing. Which of the following best "
            "describes what the administrator is doing?"
        ),
        "name": "secplus_q32",
        "correct": "C",
        "explain": (
            "Correct. C — Hashing runs passwords through a one-way mathematical algorithm to produce a "
            "fixed-length digest stored instead of plaintext; salts and strong algorithms keep identical "
            "passwords from producing the same hash. Appending characters describes padding or unrelated "
            "techniques, not hashing itself. Tokens make credentials time-bound or session-based; they are "
            "not how stored password verifiers are created. Rainbow tables are precomputed hash lookup "
            "tables attackers use; administrators do not build them to protect passwords."
        ),
        "choices": [
            "Adding extra characters at the end to increase password length",
            "Generating a token to make the passwords temporal",
            "Using mathematical algorithms to make passwords unique",
            "Creating a rainbow table to protect passwords in a list",
        ],
        "objectives": ["1.4", "4.5"],
    },
    {
        "slug": "legacy-gas-pipeline-scada",
        "title": "Security+ — SCADA (gas pipeline control)",
        "stem": (
            "A company wants to protect a specialized legacy platform that controls the physical flow of gas "
            "inside of pipes. Which of the following environments does the company need to secure to best "
            "achieve this goal?"
        ),
        "name": "secplus_q33",
        "correct": "B",
        "explain": (
            "Correct. B — SCADA (supervisory control and data acquisition) systems monitor and control "
            "industrial processes such as gas distribution in pipelines; securing that environment protects "
            "the legacy operational technology platform. IaaS is cloud infrastructure hosting, not the "
            "industrial control layer for physical plant operations. SDN abstracts network control planes "
            "and does not define the gas-flow control system itself. IoT covers connected devices broadly; "
            "pipeline operational control in this scenario is the SCADA/OT domain rather than generic IoT."
        ),
        "choices": [
            "IaaS",
            "SCADA",
            "SDN",
            "IoT",
        ],
        "objectives": ["2.2", "3.1"],
    },
    {
        "slug": "critical-system-patch-least-privilege",
        "title": "Security+ — Patch transfer (least privilege)",
        "stem": (
            "A user is attempting to patch a critical system, but the patch fails to transfer. Which of the "
            "following access controls is most likely inhibiting the transfer?"
        ),
        "name": "secplus_q34",
        "correct": "D",
        "explain": (
            "Correct. D — Least privilege limits users and processes to the minimum access needed; if the "
            "account or service lacks rights to write the patch or reach the critical system, the transfer "
            "fails until those permissions are granted for the maintenance task. Attribute-based control "
            "evaluates multiple attributes together; a simple failed file transfer on a critical system is "
            "most often explained by insufficient permissions under least privilege. Time-of-day control "
            "blocks access outside allowed windows, not typically described as a failed transfer mid-task. "
            "Role-based access ties rights to job role; the scenario points to lacking required privilege, "
            "which least privilege directly describes."
        ),
        "choices": [
            "Attribute-based",
            "Time of day",
            "Role-based",
            "Least privilege",
        ],
        "objectives": ["4.6", "1.2"],
    },
    {
        "slug": "client-sla-service-time-resources",
        "title": "Security+ — SLA (client service and timing)",
        "stem": (
            "Which of the following describes the understanding between a company and a client about what "
            "will be provided and the accepted time needed to provide the company with the resources?"
        ),
        "name": "secplus_q35",
        "correct": "A",
        "explain": (
            "Correct. A — A service level agreement (SLA) documents what the provider delivers to the client "
            "and the agreed timelines or performance targets, such as response times, availability, and "
            "when resources will be supplied. An MOU states mutual intent to cooperate but is less formal "
            "and not focused on measurable service commitments. An MOA formalizes responsibilities between "
            "partners, often for joint work or IP, not client service metrics. A business partnership "
            "agreement (BPA) defines partner relationships or procurement terms, not the standard "
            "client-facing service and timing document described here."
        ),
        "choices": [
            "SLA",
            "MOU",
            "MOA",
            "BPA",
        ],
        "objectives": ["5.3", "5.4"],
    },
    {
        "slug": "admin-access-bastion-host",
        "title": "Security+ — Bastion host (admin access)",
        "stem": (
            "A company needs to provide administrative access to internal resources while minimizing the traffic "
            "allowed through the security boundary. Which of the following methods is most secure?"
        ),
        "name": "secplus_q36",
        "correct": "A",
        "explain": (
            "Correct. A — A bastion (jump) host is a hardened system in a controlled zone that is the only "
            "approved entry for administrators reaching internal resources, reducing open paths through the "
            "firewall or boundary. A perimeter network (DMZ) segments public-facing services but does not by "
            "itself limit admin sessions to one controlled hop. A WAF filters web application traffic and does "
            "not replace secure administrative jump access. Single sign-on streamlines authentication but does "
            "not minimize which connections cross the security boundary."
        ),
        "choices": [
            "Implementing a bastion host",
            "Deploying a perimeter network",
            "Installing a WAF",
            "Utilizing single sign-on",
        ],
        "objectives": ["2.5", "3.2"],
    },
    {
        "slug": "dba-jump-server-database-segment",
        "title": "Security+ — Jump server (DBA access)",
        "stem": (
            "A company prevented direct access from the database administrators' workstations to the network "
            "segment that contains database servers. Which of the following should a database administrator "
            "use to access the database servers?"
        ),
        "name": "secplus_q37",
        "correct": "A",
        "explain": (
            "Correct. A — A jump server (bastion host) sits in a controlled zone; DBAs connect to it first, "
            "then reach database servers in the protected segment without exposing those servers directly "
            "to workstations. RADIUS authenticates remote network access; it is not the hop host used to "
            "reach an isolated DB segment. An HSM protects cryptographic keys, not routine DBA connectivity. "
            "A load balancer distributes client traffic across servers; it does not replace administrative "
            "jump access for DBAs."
        ),
        "choices": [
            "Jump server",
            "RADIUS",
            "HSM",
            "Load balancer",
        ],
        "objectives": ["2.5", "4.1"],
    },
    {
        "slug": "security-awareness-policies-handbooks-first",
        "title": "Security+ — Security awareness (policies first)",
        "stem": (
            "After a series of account compromises and credential misuse, a company hires a security manager "
            "to develop a security program. Which of the following steps should the security manager take "
            "first to increase security awareness?"
        ),
        "name": "secplus_q38",
        "correct": "D",
        "explain": (
            "Correct. D — Before campaigns and tools, update policies and handbooks so every employee knows "
            "required procedures for credentials, reporting, and acceptable use; awareness builds on that "
            "governance foundation. Evaluating risky-behavior tools supports detection and metrics but does "
            "not by itself inform staff of expectations. Quarterly newsletters are passive and infrequent. "
            "Phishing simulations are valuable after baseline policy and training are in place, not as the "
            "first step to establish organization-wide awareness."
        ),
        "choices": [
            "Evaluate tools that identify risky behavior and distribute reports on the findings.",
            "Send quarterly newsletters that explain the importance of password management.",
            "Develop phishing campaigns and notify the management team of any successes.",
            "Update policies and handbooks to ensure all employees are informed of the new procedures.",
        ],
        "objectives": ["5.1", "5.4"],
    },
    {
        "slug": "bulk-account-creation-orchestration",
        "title": "Security+ — Orchestration (bulk account script)",
        "stem": (
            "A systems administrator is creating a script that would save time and prevent human error when "
            "performing account creation for a large number of users. Which of the following would be a good "
            "use case for this task?"
        ),
        "name": "secplus_q39",
        "correct": "B",
        "explain": (
            "Correct. B — Orchestration automates repeatable workflows such as bulk user provisioning so "
            "the same steps run consistently across many accounts, reducing manual mistakes and saving time. "
            "Off-the-shelf software may help but does not describe the scripted, workflow automation pattern "
            "in the stem. A baseline defines standard secure configuration, not mass account creation scripts. "
            "Policy enforcement ensures rules are applied; it is not the primary label for scripted bulk "
            "provisioning work."
        ),
        "choices": [
            "Off-the-shelf software",
            "Orchestration",
            "Baseline",
            "Policy enforcement",
        ],
        "objectives": ["4.7", "4.1"],
    },
    {
        "slug": "data-retention-custodian-role",
        "title": "Security+ — Data custodian (retention)",
        "stem": (
            "An IT administrator needs to ensure data retention standards are implemented on an enterprise "
            "application. Which of the following describes the administrator's role?"
        ),
        "name": "secplus_q40",
        "correct": "B",
        "explain": (
            "Correct. B — A data custodian (steward) implements and maintains technical controls such as "
            "retention schedules, backups, and deletion on systems per standards set by the data owner. "
            "A processor handles personal data on behalf of a controller under privacy law; that label does "
            "not describe routine IT implementation of retention on an enterprise app. A privacy officer "
            "oversees privacy compliance program-wide, not day-to-day retention configuration. The data "
            "owner is accountable for classification and retention requirements but typically does not "
            "perform hands-on implementation on the application."
        ),
        "choices": [
            "Processor",
            "Custodian",
            "Privacy officer",
            "Owner",
        ],
        "objectives": ["5.4", "4.2"],
    },
    {
        "slug": "incident-identified-containment-next",
        "title": "Security+ — IR containment (after identification)",
        "stem": (
            "A security analyst identifies an incident in the network. Which of the following incident response "
            "activities would the security analyst perform next?"
        ),
        "name": "secplus_q41",
        "correct": "A",
        "explain": (
            "Correct. A — After detection and identification, containment limits blast radius by isolating "
            "affected hosts, blocking malicious traffic, or disabling compromised accounts. Detection and "
            "analysis precede identification; they are not the next step once the incident is already "
            "identified. Eradication removes the threat root cause after containment. Recovery restores "
            "normal operations and validates systems after eradication."
        ),
        "choices": [
            "Containment",
            "Detection",
            "Eradication",
            "Recovery",
        ],
        "objectives": ["4.8", "5.1"],
    },
    {
        "slug": "remote-access-ipsec-radius-aaa",
        "title": "Security+ — IPSec with RADIUS (remote AAA)",
        "stem": (
            "A company evaluates several options that would allow employees to have remote access to the "
            "network. The security team wants to ensure the solution includes AAA to comply with internal "
            "security policies. Which of the following should the security team recommend?"
        ),
        "name": "secplus_q42",
        "correct": "A",
        "explain": (
            "Correct. A — IPSec VPN provides encrypted remote access to the corporate network, and RADIUS "
            "delivers centralized authentication, authorization, and accounting for those sessions. RDP with "
            "LDAPS secures directory lookups but does not by itself supply full AAA for remote network "
            "access at scale. A web proxy forwards HTTP traffic and is not the standard remote-access plus "
            "AAA pairing for employees reaching internal resources. A jump server with 802.1X targets "
            "administrative hop and port-based network access control, not the typical employee VPN model "
            "with accounting required here."
        ),
        "choices": [
            "IPSec with RADIUS",
            "RDP connection with LDAPS",
            "Web proxy for all remote traffic",
            "Jump server with 802.1X",
        ],
        "objectives": ["4.6", "3.2"],
    },
    {
        "slug": "vpn-mfa-password-token-thumbprint",
        "title": "Security+ — VPN MFA (three factors)",
        "stem": (
            "A network manager wants to protect the company's VPN by implementing multifactor authentication "
            "that uses:\n"
            "• Something you know\n"
            "• Something you have\n"
            "• Something you are\n"
            "Which of the following would accomplish the manager's goal?"
        ),
        "name": "secplus_q43",
        "correct": "C",
        "explain": (
            "Correct. C — A password is something you know, an authentication token is something you have, "
            "and a thumbprint is something you are (biometric). Domain name, PKI, and GeoIP are not the "
            "classic three-factor pairing for VPN login. A VPN IP address and company ID do not map cleanly "
            "to know, have, and are. A company URL, TLS certificate, and home address are infrastructure or "
            "location data, not the required MFA factor types."
        ),
        "choices": [
            "Domain name, PKI, GeolP lookup",
            "VPN IP address, company ID, facial structure",
            "Password, authentication token, thumbprint",
            "Company URL, TLS certificate, home address",
        ],
        "objectives": ["4.6", "1.2"],
    },
    {
        "slug": "insider-threat-behavioral-analytics",
        "title": "Security+ — Behavioral analytics (insider threat)",
        "stem": (
            "An organization needs to monitor its users' activities to prevent insider threats. Which of the "
            "following solutions would help the organization achieve this goal?"
        ),
        "name": "secplus_q44",
        "correct": "A",
        "explain": (
            "Correct. A — Behavioral analytics (UEBA) establishes baselines for how users work and flags "
            "anomalous activity that may signal insider misuse or compromised accounts. Access control lists "
            "enforce static permit or deny rules; they do not continuously analyze user behavior. Identity "
            "and access management provisions and governs who can access what but does not by itself monitor "
            "ongoing actions for insider patterns. A network intrusion detection system focuses on network "
            "traffic and known attack signatures, not detailed user activity monitoring for insider threats."
        ),
        "choices": [
            "Behavioral analytics",
            "Access control lists",
            "Identity and access management",
            "Network intrusion detection system",
        ],
        "objectives": ["4.4", "2.4"],
    },
    {
        "slug": "sideloading-rootkit-threat",
        "title": "Security+ — Sideloading (rootkit)",
        "stem": (
            "Which of the following could potentially be introduced at the time of side loading?"
        ),
        "name": "secplus_q45",
        "correct": "B",
        "explain": (
            "Correct. B — Sideloading installs apps from unofficial sources outside store vetting, so "
            "malware such as a rootkit can be introduced with deep, hidden control of the device. User "
            "impersonation usually follows credential theft or social engineering, not the sideload install "
            "itself. An on-path attack intercepts communications in transit and is not what sideloading "
            "directly introduces. A buffer overflow is a coding flaw that may be exploited later; it is not "
            "the typical threat bundled at sideload time."
        ),
        "choices": [
            "User impersonation",
            "Rootkit",
            "On-path attack",
            "Buffer overflow",
        ],
        "objectives": ["2.2", "2.3"],
    },
    {
        "slug": "linux-shadow-permissions-chmod",
        "title": "Security+ — chmod (/etc/shadow permissions)",
        "stem": (
            "A systems administrator is auditing all company servers to ensure they meet the minimum security "
            "baseline. While auditing a Linux server, the systems administrator observes the /etc/shadow file "
            "has permissions beyond the baseline recommendation. Which of the following commands should the "
            "systems administrator use to resolve this issue?"
        ),
        "name": "secplus_q46",
        "correct": "A",
        "explain": (
            "Correct. A — chmod changes file permissions; tightening /etc/shadow (for example to 600 or "
            "640 as policy requires) restricts who can read password hashes. grep searches file contents and "
            "does not alter permissions. dd copies or converts data at the block level and is not used to "
            "fix shadow file modes. passwd updates user passwords, not the permission bits on /etc/shadow."
        ),
        "choices": [
            "chmod",
            "grep",
            "dd",
            "passwd",
        ],
        "objectives": ["4.1", "3.2"],
    },
    {
        "slug": "certificate-expired-status-crl",
        "title": "Security+ — CRL (certificate status)",
        "stem": (
            "Which of the following technologies assists in passively verifying the expired status of a "
            "digital certificate?"
        ),
        "name": "secplus_q47",
        "correct": "B",
        "explain": (
            "Correct. B — A certificate revocation list (CRL) is a published, downloadable list clients can "
            "check locally without a live per-certificate query, supporting passive validation of revoked or "
            "invalid certificates. OCSP requires an active online status request to a responder for each "
            "check. A TPM stores keys and performs hardware-backed crypto operations; it does not publish "
            "certificate status lists. A CSR is a request sent to a CA to apply for a new certificate, not "
            "a mechanism for verifying existing certificate status."
        ),
        "choices": [
            "OCSP",
            "CRL",
            "TPM",
            "CSR",
        ],
        "objectives": ["1.4", "4.6"],
    },
    {
        "slug": "pentest-local-credential-reuse-centralized-auth",
        "title": "Security+ — Centralized auth (credential reuse)",
        "stem": (
            "A security analyst is examining a penetration test report and notices that the tester pivoted to "
            "critical internal systems with the same local user ID and password. Which of the following would "
            "help prevent this in the future?"
        ),
        "name": "secplus_q48",
        "correct": "A",
        "explain": (
            "Correct. A — Centralized authentication (for example Active Directory) with enforced password "
            "policy removes duplicate local accounts that share one password across many hosts, blocking easy "
            "lateral movement with reused credentials. Complexity and history alone do not stop the same "
            "local account and password from existing on every system. An external authentication server is "
            "part of centralization but the exam answer emphasizes centralized auth plus policy together. "
            "Restricting password changes does not address shared local credentials used for pivoting."
        ),
        "choices": [
            "Implement centralized authentication with proper password policies",
            "Add password complexity rules and increase password history limits",
            "Connect the systems to an external authentication server",
            "Limit the ability of user accounts to change passwords",
        ],
        "objectives": ["4.6", "2.5"],
    },
    {
        "slug": "dr-plan-hot-site-immediate-operations",
        "title": "Security+ — Hot site (immediate DR)",
        "stem": (
            "A company wants to update its disaster recovery plan to include a dedicated location for immediate "
            "continued operations if a catastrophic event occurs. Which of the following options is best to "
            "include in the disaster recovery plan?"
        ),
        "name": "secplus_q49",
        "correct": "A",
        "explain": (
            "Correct. A — A hot site is fully equipped with hardware, connectivity, and near-current data so "
            "operations can resume immediately after a catastrophe. A warm site is lower cost but requires more "
            "restoration time before full operations. Geolocation refers to geographic placement strategy, not "
            "a staffed DR facility ready for instant failover. A cold site provides space and power only and "
            "needs the longest recovery window."
        ),
        "choices": [
            "Hot site",
            "Warm site",
            "Geolocation",
            "Cold site",
        ],
        "objectives": ["3.4", "5.2"],
    },
    {
        "slug": "web-form-regex-input-validation",
        "title": "Security+ — Input validation (regex policy)",
        "stem": (
            "An organization recently updated its security policy to include the following statement:\n\n"
            "Regular expressions are included in source code to remove special characters such as $, |, ;, &, "
            "` , and ? from variables set by forms in a web application.\n\n"
            "Which of the following best explains the security technique the organization adopted by making "
            "this addition to the policy?"
        ),
        "name": "secplus_q50",
        "correct": "C",
        "explain": (
            "Correct. C — Input validation sanitizes or rejects untrusted form data before use; stripping "
            "special characters with regular expressions reduces injection and command-manipulation risk. "
            "Identifying embedded keys finds secrets left in code, not filtering user input. Code debugging "
            "finds logic defects during development. Static code analysis scans source without running the "
            "app; the policy requires active validation logic in the application, not only an external scan."
        ),
        "choices": [
            "Identify embedded keys",
            "Code debugging",
            "Input validation",
            "Static code analysis",
        ],
        "objectives": ["2.5", "4.1"],
    },
    {
        "slug": "shared-backup-account-pam-sso-failure",
        "title": "Security+ — PAM (backup account, SSO failure)",
        "stem": (
            "A group of developers has a shared backup account to access the source code repository. Which of "
            "the following is the best way to secure the backup account if there is an SSO failure?"
        ),
        "name": "secplus_q51",
        "correct": "D",
        "explain": (
            "Correct. D — Privileged access management (PAM) vaults shared backup credentials, enforces "
            "checkout, monitoring, and rotation, and provides controlled break-glass access when SSO is "
            "unavailable. RAS (remote access service) enables remote connectivity but does not manage "
            "privileged shared accounts. EAP is a network authentication framework, not repository backup "
            "account control. SAML enables SSO federation; when SSO fails, SAML does not secure the shared "
            "backup account by itself."
        ),
        "choices": [
            "RAS",
            "EAP",
            "SAML",
            "PAM",
        ],
        "objectives": ["4.6", "5.1"],
    },
    {
        "slug": "unauthorized-app-install-sideloading",
        "title": "Security+ — Sideloading (definition)",
        "stem": (
            "Which of the following is a type of vulnerability that refers to the unauthorized installation "
            "of applications on a device through means other than the official application store?"
        ),
        "name": "secplus_q52",
        "correct": "D",
        "explain": (
            "Correct. D — Sideloading installs applications from outside the official app store, bypassing "
            "store review and device protections. Cross-site scripting injects scripts into web pages viewed "
            "by others. A buffer overflow writes beyond allocated memory in a program. Jailbreaking removes "
            "OS restrictions on a device; it is related but the term for installing apps outside the store "
            "is sideloading."
        ),
        "choices": [
            "Cross-site scripting",
            "Buffer overflow",
            "Jailbreaking",
            "Side loading",
        ],
        "objectives": ["2.3", "2.2"],
    },
    {
        "slug": "remote-auth-time-based-tokens",
        "title": "Security+ — Time-based tokens (remote MFA)",
        "stem": (
            "An organization wants to improve the company's security authentication method for remote employees. "
            "Given the following requirements:\n"
            "• Must work across SaaS and internal network applications\n"
            "• Must be device manufacturer agnostic\n"
            "• Must have offline capabilities\n"
            "Which of the following would be the most appropriate authentication method?"
        ),
        "name": "secplus_q53",
        "correct": "D",
        "explain": (
            "Correct. D — Time-based one-time password (TOTP) tokens integrate with many SaaS and on-premises "
            "apps, run on generic hardware or mobile apps from any vendor, and generate codes offline from a "
            "shared secret and clock. Username and password alone lack strong second-factor protection. "
            "Biometrics depend on specific device hardware and are not uniformly supported everywhere. SMS "
            "verification requires cellular delivery and does not work offline."
        ),
        "choices": [
            "Username and password",
            "Biometrics",
            "SMS verification",
            "Time-based tokens",
        ],
        "objectives": ["4.6", "1.2"],
    },
    {
        "slug": "staging-subset-customer-data-upgrades",
        "title": "Security+ — Staging (upgrade assessment)",
        "stem": (
            "Which of the following environments utilizes a subset of customer data and is most likely to be "
            "used to assess the impacts of major system upgrades and demonstrate system features?"
        ),
        "name": "secplus_q54",
        "correct": "D",
        "explain": (
            "Correct. D — Staging (pre-production) mirrors production with a subset or masked copy of customer "
            "data so teams can validate major upgrades and demonstrate features before go-live. Development "
            "is for building code, usually with minimal or synthetic data. Test focuses on finding defects "
            "with test cases rather than business-facing demos and upgrade impact reviews. Production runs "
            "live workloads with full customer data, not a safe subset for experimentation."
        ),
        "choices": [
            "Development",
            "Test",
            "Production",
            "Staging",
        ],
        "objectives": ["4.2", "1.3"],
    },
    {
        "slug": "maximum-accepted-risk-threshold",
        "title": "Security+ — Risk threshold",
        "stem": (
            "Which of the following describes the maximum allowance of accepted risk?"
        ),
        "name": "secplus_q55",
        "correct": "D",
        "explain": (
            "Correct. D — A risk threshold is the upper bound of risk the organization will accept before "
            "treatment or escalation is required. A risk indicator is a metric that signals conditions that "
            "may increase risk. Risk level categorizes severity (for example low, medium, high). A risk "
            "score is a calculated value from likelihood and impact, not the policy limit of acceptable risk."
        ),
        "choices": [
            "Risk indicator",
            "Risk level",
            "Risk score",
            "Risk threshold",
        ],
        "objectives": ["5.2"],
    },
    {
        "slug": "reported-phish-not-tuning-filters",
        "title": "Security+ — Email filter tuning (reports)",
        "stem": (
            "A security administrator receives multiple reports about the same suspicious email. Which of the "
            "following is the most likely reason for the malicious email's continued delivery?"
        ),
        "name": "secplus_q56",
        "correct": "B",
        "explain": (
            "Correct. B — User reports should update blocklists, rules, and sandbox signatures so the same "
            "campaign is blocked; if report data is not fed into filtering tools, identical messages keep "
            "arriving. Employees marking legitimate mail as spam affects false positives, not repeated "
            "delivery of the same reported threat. Shadow IT email bypasses corporate mail but is not the "
            "usual explanation when many users report the same message in corporate inboxes. Forwarding "
            "personal mail does not explain why a reported malicious message is not stopped organization-wide."
        ),
        "choices": [
            "Employees are flagging legitimate emails as spam.",
            "Information from reported emails is not being used to tune email filtering tools.",
            "Employees are using shadow IT solutions for email.",
            "Employees are forwarding personal emails to company email addresses.",
        ],
        "objectives": ["4.4", "2.2"],
    },
    {
        "slug": "os-vulnerability-system-wide-access",
        "title": "Security+ — OS vulnerability (system-wide impact)",
        "stem": (
            "Which of the following best explains a concern with OS-based vulnerabilities?"
        ),
        "name": "secplus_q57",
        "correct": "A",
        "explain": (
            "Correct. A — The operating system mediates memory, devices, and privileges for every application; "
            "an OS exploit can reach kernel or system services and affect all programs on the host. Patch "
            "frequency is a process concern but not the defining technical impact of OS flaws. User trust "
            "in the OS can hide compromise but does not describe why OS bugs are especially dangerous. OS "
            "exploits are not universally easier than application vulnerabilities."
        ),
        "choices": [
            "An exploit will give an attacker access to system functions that span multiple applications.",
            "The OS vendor's patch cycle is not frequent enough to mitigate the large number of threats.",
            "Most users trust the core operating system features and may not notice if the system has been compromised.",
            "Exploitation of an operating system vulnerability is typically easier than any other vulnerability.",
        ],
        "objectives": ["2.3", "2.4"],
    },
    {
        "slug": "bia-rto-downtime-tolerance",
        "title": "Security+ — RTO (BIA benefit)",
        "stem": (
            "Which of the following is a benefit of an RTO when conducting a business impact analysis?"
        ),
        "name": "secplus_q58",
        "correct": "D",
        "explain": (
            "Correct. D — Recovery time objective (RTO) defines the maximum acceptable downtime after an "
            "incident before business impact exceeds tolerance, guiding recovery priorities in a BIA. "
            "Likelihood and cost come from risk analysis, not RTO. Roles and responsibilities belong in "
            "incident response planning. The data state or point in time to restore to is recovery point "
            "objective (RPO), not RTO."
        ),
        "choices": [
            "It determines the likelihood of an incident and its cost.",
            "It determines the roles and responsibilities for incident responders.",
            "It determines the state that systems should be restored to following an incident.",
            "It determines how long an organization can tolerate downtime after an incident.",
        ],
        "objectives": ["3.4", "5.2"],
    },
    {
        "slug": "accounting-login-watering-hole-download",
        "title": "Security+ — Watering hole (auto download)",
        "stem": (
            "An employee from the accounting department logs in to a website. A desktop application "
            "automatically downloads on the employee's computer. Which of the following has occurred?"
        ),
        "name": "secplus_q59",
        "correct": "B",
        "explain": (
            "Correct. B — A watering hole attack compromises a site the target group is expected to visit; "
            "when victims authenticate or browse there, malware such as a fake application download is "
            "delivered. Cross-site scripting injects script into pages viewed by others and is not defined "
            "by a department-specific login triggering a desktop download. Typosquatting uses look-alike "
            "domain names from user typos, not a compromised legitimate site after login. A buffer overflow "
            "is a memory corruption flaw, not this social-engineering delivery pattern."
        ),
        "choices": [
            "XSS",
            "Watering hole",
            "Typosquatting",
            "Buffer overflow",
        ],
        "objectives": ["2.2", "2.4"],
    },
    {
        "slug": "risk-analysis-likelihood-exploitation",
        "title": "Security+ — Likelihood (exploitation chance)",
        "stem": (
            "Which of the following risk analysis attributes measures the chance that a vulnerability will be "
            "exploited?"
        ),
        "name": "secplus_q60",
        "correct": "D",
        "explain": (
            "Correct. D — Likelihood is the probability that a threat will exploit a vulnerability. Exposure "
            "factor is the percentage of asset value lost if the vulnerability is exploited. Impact is the "
            "magnitude of harm when exploitation occurs. Severity rates how serious the vulnerability is, "
            "not the probability it will be exploited."
        ),
        "choices": [
            "Exposure factor",
            "Impact",
            "Severity",
            "Likelihood",
        ],
        "objectives": ["5.2"],
    },
    {
        "slug": "incident-response-lessons-learned-reports",
        "title": "Security+ — Lessons learned (IR reports)",
        "stem": (
            "Which of the following phases of an incident response involves generating reports?"
        ),
        "name": "secplus_q61",
        "correct": "C",
        "explain": (
            "Correct. C — The lessons learned (post-incident) phase documents what happened, produces "
            "reports, and updates plans and controls based on findings. Preparation builds capabilities "
            "before an incident. Containment limits damage during the event. Recovery restores operations "
            "and services; formal reporting and review typically follow in lessons learned."
        ),
        "choices": [
            "Recovery",
            "Preparation",
            "Lessons learned",
            "Containment",
        ],
        "objectives": ["4.8", "5.1"],
    },
    {
        "slug": "dr-strategy-warm-quick-low-cost",
        "title": "Security+ — Warm (quick, low-cost recovery)",
        "stem": (
            "Which of the following data recovery strategies will result in a quick recovery at low cost?"
        ),
        "name": "secplus_q62",
        "correct": "D",
        "explain": (
            "Correct. D — A warm strategy balances cost and speed: partial hardware and connectivity are "
            "ready so recovery is faster than cold or manual options but cheaper than a fully mirrored hot "
            "site. Hot recovery is fastest but the most expensive. Cold sites are low cost but need the "
            "longest rebuild time. Manual recovery depends on staff effort and is typically slower."
        ),
        "choices": [
            "Hot",
            "Cold",
            "Manual",
            "Warm",
        ],
        "objectives": ["3.4", "5.2"],
    },
    {
        "slug": "certificate-presented-ocsp-validation",
        "title": "Security+ — OCSP (certificate validation)",
        "stem": (
            "Which of the following is used to validate a certificate when it is presented to a user?"
        ),
        "name": "secplus_q63",
        "correct": "A",
        "explain": (
            "Correct. A — OCSP lets a client query a responder in real time to confirm whether a presented "
            "certificate is still valid or has been revoked. A CSR is submitted to a CA to request a new "
            "certificate. A CA issues and signs certificates but is not the live status check at presentation. "
            "CRC detects data transmission errors; it does not validate digital certificates."
        ),
        "choices": [
            "OCSP",
            "CSR",
            "CA",
            "CRC",
        ],
        "objectives": ["1.4", "4.6"],
    },
    {
        "slug": "hr-fileshare-least-privilege-confidentiality",
        "title": "Security+ — Least privilege (HR confidentiality)",
        "stem": (
            "Which of the following security concepts is the best reason for permissions on a human resources "
            "fileshare to follow the principle of least privilege?"
        ),
        "name": "secplus_q64",
        "correct": "C",
        "explain": (
            "Correct. C — Least privilege on an HR fileshare limits access to only staff who need employee "
            "records, protecting confidentiality of sensitive personal data. Integrity focuses on preventing "
            "unauthorized changes; it is supported by access control but is not the primary driver for "
            "restricting who may view HR files. Availability ensures timely access for authorized users, "
            "not limiting disclosure. Non-repudiation proves who performed an action, not why access should "
            "be minimized."
        ),
        "choices": [
            "Integrity",
            "Availability",
            "Confidentiality",
            "Non-repudiation",
        ],
        "objectives": ["1.2", "4.6"],
    },
    {
        "slug": "email-malicious-attachments-inline-scan",
        "title": "Security+ — Inline email scan (attachments)",
        "stem": (
            "A security architect wants to prevent employees from receiving malicious attachments by email. "
            "Which of the following functions should the chosen solution do?"
        ),
        "name": "secplus_q65",
        "correct": "C",
        "explain": (
            "Correct. C — Inline scanning inspects messages and attachments as mail flows through the gateway "
            "and can block malware before it reaches user inboxes. IP reputation filters senders by address "
            "reputation but does not fully analyze attachment payloads. Tapping and monitoring copies traffic "
            "for analysis but does not by itself stop delivery at the gateway. SPF validates authorized senders "
            "and reduces spoofing; it does not scan attachments for malicious content."
        ),
        "choices": [
            "Apply IP address reputation data.",
            "Tap and monitor the email feed.",
            "Scan email traffic inline.",
            "Check SPF records.",
        ],
        "objectives": ["2.5", "4.1"],
    },
    {
        "slug": "vuln-remediation-rescan-network",
        "title": "Security+ — Rescan (post-remediation)",
        "stem": (
            "A security practitioner completes a vulnerability assessment on a company's network and finds "
            "several vulnerabilities, which the operations team remediates. Which of the following should "
            "be done next?"
        ),
        "name": "secplus_q66",
        "correct": "C",
        "explain": (
            "Correct. C — After remediation, rescanning verifies that fixes were applied and findings are "
            "closed, completing the assess-remediate-validate cycle. An audit may follow later for compliance "
            "but is not the immediate technical next step. Penetration testing is a separate exercise that "
            "may occur on its own schedule. Reporting documents results; validation through rescan should "
            "occur before treating remediation as complete."
        ),
        "choices": [
            "Conduct an audit.",
            "Initiate a penetration test.",
            "Rescan the network.",
            "Submit a report.",
        ],
        "objectives": ["4.3", "4.2"],
    },
    {
        "slug": "unauthorized-devices-nac-8021x-posture",
        "title": "Security+ — NAC (802.1X + posture)",
        "stem": (
            "A security engineer receives reports of unauthorized devices on the organization's network. "
            "Which of the following best describes a secure and effective way to mitigate the risks?"
        ),
        "name": "secplus_q67",
        "correct": "C",
        "explain": (
            "Correct. C — NAC with 802.1X and device certificates strongly authenticates endpoints, and "
            "posture checks verify compliance before granting network access, blocking unauthorized or "
            "noncompliant devices. Blocking only wireless until baseline match ignores wired rogue devices "
            "and lacks certificate-based identity. Accepting only static IP handshakes is weak and does not "
            "scale or bind identity to devices. Redirecting all devices to guest Wi-Fi for manual analyst "
            "review is impractical and delays legitimate users."
        ),
        "choices": [
            (
                "Deploy a NAC solution to block wireless connections until devices can be verified against "
                "the baseline configuration."
            ),
            "Set the NAC solution to only accept handshakes initiated from a static set of IP addresses.",
            (
                "Configure a NAC solution to enforce 802.1X authentication with device certificates and "
                "implement endpoint security checks."
            ),
            (
                "Implement a NAC solution that redirects all devices to the guest Wi-Fi for holding until "
                "a security analyst can validate the security compliance."
            ),
        ],
        "objectives": ["2.5", "4.1"],
    },
    {
        "slug": "new-email-servers-update-spf",
        "title": "Security+ — SPF (new mail servers)",
        "stem": (
            "A few weeks after deploying additional email servers, employees complain that messages are being "
            "marked as spam. Which needs to be updated?"
        ),
        "name": "secplus_q68",
        "correct": "D",
        "explain": (
            "Correct. D — SPF DNS records list which hosts may send mail for the domain; new outbound servers "
            "must be added or receivers may treat messages as spoofed and mark them spam. CNAME creates "
            "DNS aliases and does not authorize senders. SMTP is the mail transfer protocol already used by "
            "the servers. DLP inspects content for policy violations; it does not fix sender authentication "
            "when new servers are not listed in SPF."
        ),
        "choices": [
            "CNAME",
            "SMTP",
            "DLP",
            "SPF",
        ],
        "objectives": ["2.2", "4.1"],
    },
    {
        "slug": "pci-dss-failure-fines",
        "title": "Security+ — PCI DSS failure (fines)",
        "stem": (
            "Which of the following is the most likely outcome if a large bank fails an internal PCI DSS "
            "compliance assessment?"
        ),
        "name": "secplus_q69",
        "correct": "A",
        "explain": (
            "Correct. A — PCI DSS is enforced by payment card brands through acquirers; failing an assessment "
            "commonly results in fines that escalate while non-compliance continues. Audit findings describe "
            "what the assessment found, not the contractual penalty outcome. Sanctions may apply in severe "
            "cases but fines are the most direct and likely PCI consequence on the exam. Reputation damage "
            "can follow but is secondary to mandated financial penalties."
        ),
        "choices": [
            "Fines",
            "Audit findings",
            "Sanctions",
            "Reputation damage",
        ],
        "objectives": ["5.4", "5.5"],
    },
    {
        "slug": "zero-day-bastion-compensating-control",
        "title": "Security+ — Compensating control (bastion)",
        "stem": (
            "An alert references attacks associated with a zero-day exploit. An analyst places a bastion host "
            "in the network to reduce the risk of the exploit. Which of the following types of controls is the "
            "analyst implementing?"
        ),
        "name": "secplus_q70",
        "correct": "A",
        "explain": (
            "Correct. A — A compensating control substitutes when the primary control cannot fully address "
            "the risk; a bastion host limits direct access while a zero-day patch is unavailable. Detective "
            "controls identify events after they occur, such as logging and alerts. Operational controls "
            "are procedural day-to-day practices, not this technical workaround. Physical controls protect "
            "facilities and hardware, not network access paths for exploits."
        ),
        "choices": [
            "Compensating",
            "Detective",
            "Operational",
            "Physical",
        ],
        "objectives": ["1.1", "2.5"],
    },
    {
        "slug": "pentest-rules-of-engagement",
        "title": "Security+ — Rules of engagement (pentest)",
        "stem": (
            "Which of the following provides the details about the terms of a test with a third-party "
            "penetration tester?"
        ),
        "name": "secplus_q71",
        "correct": "A",
        "explain": (
            "Correct. A — Rules of engagement define scope, timing, targets, techniques allowed, contact "
            "procedures, and legal boundaries for a penetration test. Supply chain analysis evaluates "
            "vendor and component risk in the delivery chain. A right to audit clause lets an organization "
            "review a vendor's controls contractually. Due diligence is the broader investigation before "
            "engaging a third party, not the document that sets pentest terms."
        ),
        "choices": [
            "Rules of engagement",
            "Supply chain analysis",
            "Right to audit clause",
            "Due diligence",
        ],
        "objectives": ["5.3", "5.5"],
    },
    {
        "slug": "automate-account-permissions-user-provisioning",
        "title": "Security+ — User provisioning (bulk permissions)",
        "stem": (
            "An administrator wants to automate an account permissions update for a large number of accounts. "
            "Which of the following would best accomplish this task?"
        ),
        "name": "secplus_q72",
        "correct": "C",
        "explain": (
            "Correct. C — User provisioning automates creating, updating, and deprovisioning accounts and "
            "permissions at scale from HR or directory workflows. Security groups organize access but "
            "assigning many accounts still requires provisioning automation to apply changes in bulk. "
            "Federation links identity across organizations for SSO; it does not by itself bulk-update "
            "local permissions. Vertical scaling adds compute or storage capacity, not identity management."
        ),
        "choices": [
            "Security groups",
            "Federation",
            "User provisioning",
            "Vertical scaling",
        ],
        "objectives": ["4.6", "4.7"],
    },
    {
        "slug": "legacy-device-end-of-support-decommission",
        "title": "Security+ — End of support (legacy device)",
        "stem": (
            "A legacy device is being decommissioned and is no longer receiving updates or patches. Which of "
            "the following describes this scenario?"
        ),
        "name": "secplus_q73",
        "correct": "C",
        "explain": (
            "Correct. C — End of support is when the vendor stops providing patches and updates; the device "
            "becomes a security risk and is often decommissioned. End of life usually means the product is "
            "no longer sold but may still receive limited vendor support for a transition period. End of "
            "business and end of testing are not standard product lifecycle terms for unsupported hardware."
        ),
        "choices": [
            "End of business",
            "End of testing",
            "End of support",
            "End of life",
        ],
        "objectives": ["4.2", "4.3"],
    },
    {
        "slug": "technical-security-control-firewall",
        "title": "Security+ — Technical control (firewall)",
        "stem": "Which of the following is a technical security control?",
        "name": "secplus_q74",
        "correct": "D",
        "explain": (
            "Correct. D — A firewall is a technical control implemented in hardware or software to enforce "
            "network traffic rules. A security guard is a physical control. A policy is an administrative "
            "(managerial) control. A fence is a physical perimeter control."
        ),
        "choices": [
            "Security guard",
            "Policy",
            "Fence",
            "Firewall",
        ],
        "objectives": ["1.1", "2.5"],
    },
    {
        "slug": "rogue-device-mac-cloning-audit",
        "title": "Security+ — MAC cloning (rogue device audit)",
        "stem": "",
        "name": "secplus_q75",
        "correct": "A",
        "explain": (
            "Correct. A — The audit shows the same MAC address (EB-AC-11-82-42-F3) on two hosts with "
            "different IP addresses and hostnames, indicating MAC cloning to satisfy the known-hardware "
            "requirement while a personal device connects. A DHCP failure misassigns addresses but does "
            "not duplicate a legitimate MAC on a rogue host. An administrator bypass is possible but the "
            "report points to spoofed hardware identity, not policy exception. DNS hijacking of captive "
            "portal traffic does not explain duplicate MAC entries in an endpoint asset audit."
        ),
        "choices": [
            "A user performed a MAC cloning attack with a personal device.",
            "A DHCP failure caused an incorrect IP address to be distributed.",
            "An administrator bypassed the security controls for testing.",
            "DNS hijacking let an attacker intercept the captive portal traffic.",
        ],
        "prepend_html": build_endpoint_audit_report_exhibit(),
        "objectives": ["2.4", "4.1"],
    },
    {
        "slug": "decommission-data-retention-secure-destruction",
        "title": "Security+ — Retention (decommissioning)",
        "stem": (
            "Which of the following is a key reason to follow data retention policies during asset "
            "decommissioning?"
        ),
        "name": "secplus_q76",
        "correct": "A",
        "explain": (
            "Correct. A — Retention policies define how long data may be kept and when it must be destroyed; "
            "during decommissioning they ensure media is sanitized or destroyed when data is no longer "
            "required. Backing up all data before disposal is not the purpose of retention rules and can "
            "retain data longer than allowed. Employees should not access files on recycled hardware. "
            "Keeping all customer data indefinitely conflicts with minimization and regulatory retention "
            "limits."
        ),
        "choices": [
            "To ensure data is securely destroyed when no longer needed",
            "To make backup copies of all company data before disposing of hardware",
            "To allow employees to access old files even after the hardware is recycled",
            "To keep all customer data available in case it is required in the future",
        ],
        "objectives": ["5.4", "4.2"],
    },
    {
        "slug": "payroll-text-smishing-impersonation",
        "title": "Security+ — Smishing + impersonation (payroll text)",
        "stem": (
            "An employee receives a text message that appears to have been sent by the payroll department "
            "and is asking for credential verification. Which of the following social engineering techniques "
            "are being attempted? (Choose two.)"
        ),
        "name": "secplus_q77",
        "choose_two": True,
        "correct": ["C", "E"],
        "explain": (
            "Correct. C and E — Smishing is phishing delivered by SMS; impersonation is posing as a trusted "
            "party such as payroll to solicit credentials. Typosquatting uses look-alike domain names, not "
            "text messages. Phishing is related but the exam pair for an SMS channel is smishing plus "
            "impersonation of payroll. Vishing uses voice calls. Misinformation spreads false narratives "
            "broadly, not this targeted credential request."
        ),
        "choices": [
            "Typosquatting",
            "Phishing",
            "Impersonation",
            "Vishing",
            "Smishing",
            "Misinformation",
        ],
        "objectives": ["2.2", "2.4"],
    },
    {
        "slug": "batch-job-memory-injection-outbound-traffic",
        "title": "Security+ — Memory injection (abnormal process)",
        "stem": (
            "A security analyst is investigating an application server and discovers that software on the "
            "server is behaving abnormally. The software normally runs batch jobs locally and does not "
            "generate traffic, but the process is now generating outbound traffic over random high ports. "
            "Which of the following vulnerabilities has likely been exploited in this software?"
        ),
        "name": "secplus_q78",
        "correct": "A",
        "explain": (
            "Correct. A — Memory injection places malicious code inside a running process so it can abuse "
            "the application's trust and spawn unexpected outbound connections, such as C2 over random high "
            "ports. A race condition is a timing flaw between operations, not typical beaconing from a batch "
            "job. Side loading installs unauthorized applications from outside official stores. SQL injection "
            "targets databases through crafted queries, not local batch processes suddenly opening outbound "
            "sessions."
        ),
        "choices": [
            "Memory injection",
            "Race condition",
            "Side loading",
            "SQL injection",
        ],
        "objectives": ["2.3", "2.4"],
    },
    {
        "slug": "stakeholders-tabletop-exercise-roles",
        "title": "Security+ — Tabletop exercise",
        "stem": (
            "Various stakeholders are meeting to discuss their hypothetical roles and responsibilities in a "
            "specific situation, such as a security incident or major disaster. Which of the following best "
            "describes this meeting?"
        ),
        "name": "secplus_q79",
        "correct": "C",
        "explain": (
            "Correct. C — A tabletop exercise is a discussion-based drill where stakeholders walk through "
            "hypothetical scenarios and clarify roles without live system changes. A penetration test "
            "actively probes systems for vulnerabilities. Continuity of operations planning develops "
            "recovery procedures and documentation; the meeting described is the exercise format itself. "
            "A simulation typically involves hands-on or operational play-through rather than a guided "
            "discussion of responsibilities."
        ),
        "choices": [
            "Penetration test",
            "Continuity of operations planning",
            "Tabletop exercise",
            "Simulation",
        ],
        "objectives": ["3.4", "4.8"],
    },
    {
        "slug": "replace-expired-ssl-certificate-csr",
        "title": "Security+ — CSR (new SSL certificate)",
        "stem": (
            "An administrator must replace an expired SSL certificate. Which of the following does the "
            "administrator need to create the new SSL certificate?"
        ),
        "name": "secplus_q80",
        "correct": "A",
        "explain": (
            "Correct. A — A certificate signing request (CSR) contains the public key and identity details "
            "submitted to a CA to issue a new certificate. OCSP checks revocation status of an existing "
            "certificate. A private key is generated with the CSR but the CSR is what you send to the CA "
            "to obtain the signed cert. A CRL lists revoked certificates and is not used to request a new one."
        ),
        "choices": [
            "CSR",
            "OCSP",
            "Key",
            "CRL",
        ],
        "objectives": ["1.4", "4.6"],
    },
    {
        "slug": "unexpected-characters-sql-injection",
        "title": "Security+ — SQL injection (unexpected characters)",
        "stem": (
            "An attacker submits a request containing unexpected characters in an attempt to gain "
            "unauthorized access to information within the underlying systems. Which of the following "
            "best describes this attack?"
        ),
        "name": "secplus_q81",
        "correct": "D",
        "explain": (
            "Correct. D — SQL injection sends crafted input with special characters to manipulate database "
            "queries and read or modify data without authorization. Side loading installs applications from "
            "unofficial sources. Target of evaluation is the system assessed in a security evaluation, not "
            "an attack type. Resource reuse is a vulnerability class involving reusing resources unsafely, "
            "not malformed request characters against a database."
        ),
        "choices": [
            "Side loading",
            "Target of evaluation",
            "Resource reuse",
            "SQL injection",
        ],
        "objectives": ["2.3", "2.5"],
    },
    {
        "slug": "inbound-smb-rdp-honeynet-vlan",
        "title": "Security+ — Honeynet (SMB/RDP inbound)",
        "stem": (
            "A Chief Security Officer signs off on a request to allow inbound SMB and RDP from the "
            "internet to a single VLAN. Which of the following is the most likely explanation for this "
            "activity?"
        ),
        "name": "secplus_q82",
        "correct": "D",
        "explain": (
            "Correct. D — A honeynet deliberately exposes attractive services such as SMB and RDP on an "
            "isolated VLAN to lure attackers and study their behavior. A new file-sharing site would not "
            "normally require internet RDP to one VLAN. Penetration tests use scoped rules of engagement "
            "and are time-bound, not permanent inbound SMB and RDP. SASE integrates cloud security "
            "services and does not require opening legacy protocols from the internet to a single VLAN."
        ),
        "choices": [
            "The company built a new file-sharing site.",
            "The organization is preparing for a penetration test.",
            "The security team is integrating with an SASE platform.",
            "The security team created a honeynet.",
        ],
        "objectives": ["2.4", "2.5"],
    },
    {
        "slug": "annual-risk-assessment-recurring",
        "title": "Security+ — Recurring (annual risk assessment)",
        "stem": (
            "A company performs a risk assessment on the information security program each year. Which of "
            "the following best describes this risk assessment?"
        ),
        "name": "secplus_q83",
        "correct": "A",
        "explain": (
            "Correct. A — Recurring risk assessments run on a fixed schedule such as annually. Ad hoc "
            "assessments occur for a specific trigger without a regular cadence. One-time assessments "
            "happen once and are not repeated yearly. Continuous assessment monitors risk in real time or "
            "ongoing cycles, not strictly once per year."
        ),
        "choices": [
            "Recurring",
            "Ad hoc",
            "One time",
            "Continuous",
        ],
        "objectives": ["5.2"],
    },
    {
        "slug": "server-cluster-load-balancer-traffic",
        "title": "Security+ — Load balancer (cluster traffic)",
        "stem": (
            "A company has a website in a server cluster. One server is experiencing very high usage, while "
            "others are nearly unused. Which of the following should the company configure to help "
            "distribute traffic quickly?"
        ),
        "name": "secplus_q84",
        "correct": "C",
        "explain": (
            "Correct. C — A load balancer distributes client requests across multiple servers in a cluster "
            "so no single host bears all traffic. Server multiprocessing runs multiple processes on one "
            "machine but does not spread load across cluster members. A warm site is a disaster recovery "
            "location, not intra-cluster traffic distribution. A proxy server forwards requests for caching "
            "or policy but a load balancer is the standard answer for balancing web traffic across servers."
        ),
        "choices": [
            "Server multiprocessing",
            "Warm site",
            "Load balancer",
            "Proxy server",
        ],
        "objectives": ["3.2", "3.4"],
    },
    {
        "slug": "extended-power-failure-generator",
        "title": "Security+ — Generator (extended power outage)",
        "stem": (
            "Which of the following is the best safeguard to protect against an extended power failure?"
        ),
        "name": "secplus_q85",
        "correct": "D",
        "explain": (
            "Correct. D — Generators can supply electricity for hours or days during extended grid outages, "
            "keeping critical systems running after batteries and UPS capacity are exhausted. Off-site "
            "backups protect data if systems fail but do not provide continuous power. Batteries alone "
            "typically support only short runtime. Uninterruptible power supplies bridge brief outages and "
            "allow graceful shutdown but are not sized for long extended failures."
        ),
        "choices": [
            "Off-site backups",
            "Batteries",
            "Uninterruptible power supplies",
            "Generators",
        ],
        "objectives": ["3.4", "4.2"],
    },
    {
        "slug": "automate-infrastructure-deployment-iac",
        "title": "Security+ — IaC (automated deployment)",
        "stem": (
            "Which of the following technologies must be used in an organization that intends to automate "
            "infrastructure deployment?"
        ),
        "name": "secplus_q86",
        "correct": "A",
        "explain": (
            "Correct. A — Infrastructure as code (IaC) defines servers, networks, and services in "
            "machine-readable templates so deployment can be automated and repeated consistently. IaaS is "
            "a cloud service model for renting compute and storage, not the automation method itself. IoC "
            "is indicators of compromise used in threat detection. IoT is connected devices and sensors, "
            "not automated data-center or cloud infrastructure provisioning."
        ),
        "choices": [
            "IaC",
            "IaaS",
            "IoC",
            "IoT",
        ],
        "objectives": ["4.7", "3.1"],
    },
    {
        "slug": "unauthorized-disclosure-confidentiality",
        "title": "Security+ — Confidentiality (unauthorized disclosure)",
        "stem": (
            "Which of the following concepts protects sensitive information from unauthorized disclosure?"
        ),
        "name": "secplus_q87",
        "correct": "D",
        "explain": (
            "Correct. D — Confidentiality ensures data is accessible only to authorized parties and not "
            "disclosed to others. Integrity protects information from unauthorized modification. "
            "Availability ensures timely access for authorized users. Authentication verifies identity "
            "but is a mechanism; confidentiality is the goal of preventing unauthorized disclosure."
        ),
        "choices": [
            "Integrity",
            "Availability",
            "Authentication",
            "Confidentiality",
        ],
        "objectives": ["1.2"],
    },
    {
        "slug": "mobile-policy-company-owned-cobo",
        "title": "Security+ — COBO (mobile policy)",
        "stem": (
            "A company is changing its mobile device policy. The company has the following requirements:\n"
            "• Company-owned devices\n"
            "• Ability to harden the devices\n"
            "• Reduced security risk\n"
            "• Compatibility with company resources\n"
            "Which of the following would best meet these requirements?"
        ),
        "name": "secplus_q88",
        "correct": "D",
        "explain": (
            "Correct. D — COBO (corporate-owned, business-only) gives the organization full ownership "
            "and control to harden devices, restrict personal use, and enforce policies compatible with "
            "company resources, minimizing attack surface. BYOD is employee-owned with limited control. "
            "CYOD offers choice from an approved list but does not maximize hardening and risk reduction "
            "like business-only company ownership. COPE is company-owned but allows personal use, which "
            "adds risk compared with COBO when reduced security risk is a priority."
        ),
        "choices": [
            "BYOD",
            "CYOD",
            "COPE",
            "COBO",
        ],
        "objectives": ["4.1", "4.6"],
    },
    {
        "slug": "shared-files-malware-rat-infection",
        "title": "Security+ — RAT (shared files malware)",
        "stem": (
            "An administrator is investigating an incident and discovers several users' computers were "
            "infected with malware after viewing files that were shared with them. The administrator discovers "
            "no degraded performance in the infected machines and an examination of the log files does not "
            "show excessive failed logins. Which of the following attacks is most likely the cause of the malware?"
        ),
        "name": "secplus_q89",
        "correct": "B",
        "explain": (
            "Correct. B — A remote access Trojan is often delivered when users open shared or attached "
            "malicious files, giving attackers control without necessarily slowing the system or causing "
            "failed login spikes. A malicious flash drive spreads malware through removable media, not "
            "typically by viewing digitally shared files. Brute-forced passwords produce many failed logins "
            "in logs. Cryptojacking mines cryptocurrency and usually causes noticeable CPU use and degraded "
            "performance."
        ),
        "choices": [
            "Malicious flash drive",
            "Remote access Trojan",
            "Brute-forced password",
            "Cryptojacking",
        ],
        "objectives": ["2.2", "2.4"],
    },
    {
        "slug": "iot-smart-lighting-segmentation-credentials",
        "title": "Security+ — IoT (credentials + segmentation)",
        "stem": (
            "A smart lighting system is deployed in an office building. The devices connect to the corporate "
            "Wi-Fi and are managed via a cloud portal. Which of the following security techniques reduces "
            "risk for these IoT devices?"
        ),
        "name": "secplus_q90",
        "correct": "B",
        "explain": (
            "Correct. B — Changing default credentials closes a common IoT weakness, and network "
            "segmentation isolates lighting devices from critical corporate assets if they are compromised. "
            "Static IP addresses aid management but do not materially reduce exploit risk. Guest Wi-Fi may "
            "separate IoT from internal servers but is often less controlled and does not replace segmentation "
            "on corporate wireless. Granting vendor remote access increases third-party risk rather than "
            "reducing it."
        ),
        "choices": [
            "Assigning static IP addresses to the devices",
            "Updating default credentials and applying network segmentation",
            "Connecting the devices to the guest Wi-Fi to prevent interactions with corporate IT",
            "Allowing the vendor to have remote access for day-to-day management",
        ],
        "objectives": ["2.5", "3.2"],
    },
    {
        "slug": "vulnerability-risk-asset-inventory",
        "title": "Security+ — Asset inventory (vuln risk)",
        "stem": (
            "Which of the following would help ensure a security analyst is able to accurately measure the "
            "overall risk to an organization when a new vulnerability is disclosed?"
        ),
        "name": "secplus_q91",
        "correct": "A",
        "explain": (
            "Correct. A — A complete hardware and software inventory shows which assets run affected "
            "products and versions so risk can be scoped to real exposure. System classifications help "
            "prioritize by sensitivity but do not identify vulnerable assets. System owner lists speed "
            "remediation contacts but do not measure technical exposure. Third-party risk documentation "
            "addresses vendor relationships, not mapping internal assets to a new CVE."
        ),
        "choices": [
            "A full inventory of all hardware and software",
            "Documentation of system classifications",
            "A list of system owners and their departments",
            "Third-party risk assessment documentation",
        ],
        "objectives": ["4.2", "5.2"],
    },
    {
        "slug": "security-awareness-curriculum-threat-cadence",
        "title": "Security+ — Awareness curriculum (choose two)",
        "stem": (
            "Which of the following factors are the most important to address when formulating a training "
            "curriculum plan for a security awareness program? (Select two.)"
        ),
        "name": "secplus_q92",
        "choose_two": True,
        "correct": ["C", "E"],
        "explain": (
            "Correct. C and E — Curriculum should target industry-relevant threat vectors and set how "
            "often training runs and how long sessions last. Customer communication channels are not central "
            "to internal awareness curriculum design. Ethics reporting mechanisms are separate from security "
            "awareness content planning. Secure development training applies to developers, not the whole "
            "organization. Retraining after failed phishing simulations is follow-up policy, not core "
            "curriculum formulation."
        ),
        "choices": [
            "Channels by which the organization communicates with customers",
            "The reporting mechanisms for ethics violations",
            "Threat vectors based on the industry in which the organization operates",
            "Secure software development training for all personnel",
            "Cadence and duration of training events",
            "Retraining requirements for individuals who fail phishing simulations",
        ],
        "objectives": ["5.1", "5.4"],
    },
    {
        "slug": "mac-table-flood-port-security",
        "title": "Security+ — Port security (MAC flood)",
        "stem": (
            "A recent penetration test identified that an attacker could flood the MAC address table of "
            "network switches. Which of the following would best mitigate this type of attack?"
        ),
        "name": "secplus_q93",
        "correct": "B",
        "explain": (
            "Correct. B — Port security limits how many MAC addresses may be learned on a switch port and "
            "can block unknown addresses, preventing CAM table exhaustion from flooding. A load balancer "
            "distributes application traffic across servers, not switch MAC learning. An IPS may detect "
            "attack traffic but does not stop MAC table flooding at the switch. An NGFW filters traffic at "
            "the network boundary and does not control per-port MAC learning on access switches."
        ),
        "choices": [
            "Load balancer",
            "Port security",
            "IPS",
            "NGFW",
        ],
        "objectives": ["2.5", "3.2"],
    },
    {
        "slug": "hips-preventive-detective-controls",
        "title": "Security+ — HIPS controls (choose two)",
        "stem": (
            "Which of the following security controls are a company implementing by deploying HIPS? "
            "(Select two.)"
        ),
        "name": "secplus_q94",
        "choose_two": True,
        "correct": ["B", "F"],
        "explain": (
            "Correct. B and F — HIPS blocks malicious activity on endpoints (preventive) and monitors "
            "for suspicious behavior while logging and alerting (detective). Directive controls are policies "
            "that guide behavior. Physical controls protect facilities and hardware. Corrective controls "
            "restore systems after an incident. Compensating controls substitute when a primary control "
            "cannot be used."
        ),
        "choices": [
            "Directive",
            "Preventive",
            "Physical",
            "Corrective",
            "Compensating",
            "Detective",
        ],
        "objectives": ["1.1", "4.5"],
    },
    {
        "slug": "injection-attacks-input-validation",
        "title": "Security+ — Input validation (injection)",
        "stem": (
            "During a recent log review, an analyst found evidence of successful injection attacks. Which of "
            "the following will best address this issue?"
        ),
        "name": "secplus_q95",
        "correct": "D",
        "explain": (
            "Correct. D — Input validation rejects or sanitizes untrusted input before it reaches "
            "applications and databases, directly mitigating injection. Authentication verifies identity "
            "but does not stop malicious input from authenticated users. Secure cookies protect session "
            "data in browsers, not server-side injection. Static code analysis finds flaws during "
            "development; input validation addresses exploitation at runtime seen in logs."
        ),
        "choices": [
            "Authentication",
            "Secure cookies",
            "Static code analysis",
            "Input validation",
        ],
        "objectives": ["2.5", "4.1"],
    },
    {
        "slug": "tablets-missing-features-mdm",
        "title": "Security+ — MDM (tablet features)",
        "stem": (
            "Employees are missing features on company-provided tablets, affecting productivity. Management "
            "demands resolution in 48 hours. Which is the best solution?"
        ),
        "name": "secplus_q96",
        "correct": "C",
        "explain": (
            "Correct. C — Mobile device management (MDM) centrally deploys apps, policies, and "
            "configurations to many tablets quickly so missing features can be restored fleet-wide. EDR "
            "detects and responds to threats on endpoints, not productivity feature gaps. COPE describes "
            "company-owned devices with personal use, not rapid configuration deployment. FDE encrypts "
            "device storage and does not enable missing application features."
        ),
        "choices": [
            "EDR",
            "COPE",
            "MDM",
            "FDE",
        ],
        "objectives": ["4.1", "4.6"],
    },
    {
        "slug": "security-governance-roles-responsibilities",
        "title": "Security+ — Governance (roles and responsibilities)",
        "stem": (
            "Which of the following is the most important element when defining effective security governance?"
        ),
        "name": "secplus_q97",
        "correct": "C",
        "explain": (
            "Correct. C — Effective governance requires clear accountability through assigned roles "
            "such as owners, controllers, and custodians who are responsible for data and systems. "
            "Documenting external considerations supports compliance but is secondary to internal "
            "accountability. Onboarding and offboarding procedures are operational controls. Change "
            "management is important but is not the core structural element of governance."
        ),
        "choices": [
            "Discovering and documenting external considerations",
            "Developing procedures for employee onboarding and offboarding",
            "Assigning roles and responsibilities for owners, controllers, and custodians",
            "Defining and monitoring change management procedures",
        ],
        "objectives": ["5.1", "5.4"],
    },
    {
        "slug": "vulnerability-assessment-risk-false-positives",
        "title": "Security+ — Vuln assessment risk (false positives)",
        "stem": (
            "Which of the following is a risk of conducting a vulnerability assessment?"
        ),
        "name": "secplus_q98",
        "correct": "C",
        "explain": (
            "Correct. C — Vulnerability scans can generate false positives that waste time "
            "investigating non-issues and distract from real findings. Finding security gaps is the "
            "intended outcome of an assessment, not a risk of performing one. Disruption of operations "
            "can occur with aggressive scans but is mitigated with proper scheduling and settings. "
            "Unauthorized access is not an inherent risk of a properly scoped assessment."
        ),
        "choices": [
            "A disruption of business operations",
            "Unauthorized access to the system",
            "Reports of false positives",
            "Finding security gaps in the system",
        ],
        "objectives": ["4.3", "5.2"],
    },
    {
        "slug": "visitor-vestibule-physical-security-control",
        "title": "Security+ — Visitor vestibule (physical control)",
        "stem": (
            "Visitors to a secured facility are required to check in with a photo ID and enter the facility "
            "through an access control vestibule. Which of the following best describes this form of security "
            "control?"
        ),
        "name": "secplus_q99",
        "correct": "A",
        "explain": (
            "Correct. A — Photo ID check-in, guards, doors, locks, and mantrap vestibules are physical "
            "controls that restrict who can enter a space. Managerial (administrative) controls are policies "
            "and procedures. Technical controls use technology such as firewalls, encryption, and access "
            "lists. Operational controls are day-to-day processes and practices that support security "
            "programs but are not the category for facility entry hardware."
        ),
        "choices": [
            "Physical",
            "Managerial",
            "Technical",
            "Operational",
        ],
        "objectives": ["1.1", "2.5"],
    },
    {
        "slug": "inbound-firewall-deny-malicious-ip",
        "title": "Security+ — Inbound deny ACL (malicious IP)",
        "stem": (
            "During a security incident, the security operations team identified sustained network traffic from "
            "a malicious IP address: 10.1.4.9. A security analyst is creating an inbound firewall rule to block "
            "the IP address from accessing the organization's network. Which of the following fulfills this request?"
        ),
        "name": "secplus_q100",
        "correct": "B",
        "explain": (
            "Correct. B — On an inbound rule, traffic from the attacker uses 10.1.4.9/32 as the source and "
            "organization destinations as the target; deny ip source 10.1.4.9/32 destination 0.0.0.0/0 blocks "
            "that traffic. Option A reverses source and destination. Options C and D permit traffic instead of "
            "denying it."
        ),
        "choices": [
            "access-list inbound deny ip source 0.0.0.0/0 destination 10.1.4.9/32",
            "access-list inbound deny ip source 10.1.4.9/32 destination 0.0.0.0/0",
            "access-list inbound permit ip source 10.1.4.9/32 destination 0.0.0.0/0",
            "access-list inbound permit ip source 0.0.0.0/0 destination 10.1.4.9/32",
        ],
        "objectives": ["4.8", "3.2"],
    },
    {
        "slug": "spreadsheet-credentials-honeytoken",
        "title": "Security+ — Honeytoken (spreadsheet bait)",
        "stem": (
            "A security analyst created a fake account and saved the password in a non-readily accessible "
            "directory in a spreadsheet. An alert was also configured to notify the security team if the "
            "spreadsheet is opened. Which of the following best describes the deception method being deployed?"
        ),
        "name": "secplus_q101",
        "correct": "C",
        "explain": (
            "Correct. C — A honeytoken is planted fake data (credentials, records, or files) used as a "
            "tripwire; opening the spreadsheet triggers the alert. A honey account is a decoy user account "
            "monitored for logon activity. A honeypot is a decoy system or service. A honeynet is a network "
            "of multiple honeypots."
        ),
        "choices": [
            "Honeypot",
            "Honey account",
            "Honeytoken",
            "Honeynet",
        ],
        "objectives": ["1.1", "4.8"],
    },
    {
        "slug": "air-gapped-firmware-manual-updates",
        "title": "Security+ — Air-gapped firmware updates",
        "stem": (
            "A Chief Information Officer wants to ensure that network devices cannot connect to the public "
            "internet and the local network to directly perform firmware updates. The IT team must manually "
            "perform the update process by using a portable device. Which of the following architecture types "
            "best fits this description?"
        ),
        "name": "secplus_q102",
        "correct": "B",
        "explain": (
            "Correct. B — An air-gapped architecture isolates systems from external and routine internal "
            "network paths; updates are carried in on removable media by trusted staff. Microservices split "
            "applications into small services. SDN separates control and data planes for programmable "
            "networking. Serverless runs code without managing underlying servers."
        ),
        "choices": [
            "Microservices",
            "Air-gapped",
            "Software-defined networking",
            "Serverless",
        ],
        "objectives": ["3.1", "3.2"],
    },
    {
        "slug": "image-backup-full-system-recovery",
        "title": "Security+ — Image backup (full system)",
        "stem": (
            "A systems administrator wants to implement a backup solution. The solution needs to allow "
            "recovery of the entire system, including the operating system, in case of a disaster. Which of the "
            "following backup types should the administrator consider?"
        ),
        "name": "secplus_q103",
        "correct": "D",
        "explain": (
            "Correct. D — Image (full disk) backups capture the OS, applications, and data so the whole "
            "system can be restored after a disaster. Incremental backups save only changes since the last "
            "backup of any type. Differential backups save changes since the last full backup. A storage area "
            "network is shared block storage, not a backup method."
        ),
        "choices": [
            "Incremental",
            "Storage area network",
            "Differential",
            "Image",
        ],
        "objectives": ["3.4", "4.2"],
    },
    {
        "slug": "change-management-unauthorized-modifications",
        "title": "Security+ — Change management (unauthorized mods)",
        "stem": (
            "Which of the following prevents unauthorized modifications to internal processes, assets, and "
            "security controls?"
        ),
        "name": "secplus_q104",
        "correct": "A",
        "explain": (
            "Correct. A — Change management requires documented requests, review, approval, and testing before "
            "changes to systems, processes, or controls are implemented. Playbooks are runbooks for specific "
            "operational or incident tasks. Incident response handles security events after they occur. An "
            "acceptable use policy defines permitted user behavior on organizational resources."
        ),
        "choices": [
            "Change management",
            "Playbooks",
            "Incident response",
            "Acceptable use policy",
        ],
        "objectives": ["1.3"],
    },
    {
        "slug": "insider-threat-decoy-salaries-file",
        "title": "Security+ — Insider decoy (salaries file)",
        "stem": (
            "Which of the following techniques would attract the attention of a malicious attacker in an "
            "insider threat scenario?"
        ),
        "name": "secplus_q105",
        "correct": "A",
        "explain": (
            "Correct. A — A false file in a sensitive path such as /docs/salaries is a honeyfile or "
            "honeytoken used as bait; access can be monitored to detect malicious insiders. Weak passwords "
            "in /etc/shadow, vulnerable cron jobs, and similar changes create real weaknesses rather than "
            "safe decoys. A fake account in /etc/passwd is a honey account, but CompTIA emphasizes enticing "
            "decoy documents for insider lure scenarios like this stem."
        ),
        "choices": [
            "Creating a false text file in /docs/salaries",
            "Setting weak passwords in /etc/shadow",
            "Scheduling vulnerable jobs in /etc/crontab",
            "Adding a fake account to /etc/passwd",
        ],
        "objectives": ["1.1", "2.4"],
    },
    {
        "slug": "ir-stop-spread-containment-first",
        "title": "Security+ — IR containment (stop spread)",
        "stem": (
            "An incident response specialist must stop a malicious attack from expanding to other parts of "
            "an organization. Which of the following should the incident response specialist perform first?"
        ),
        "name": "secplus_q106",
        "correct": "C",
        "explain": (
            "Correct. C — Containment is performed first to limit blast radius (isolate hosts, block traffic, "
            "disable compromised accounts) before eradication and recovery. Eradication removes the threat "
            "after spread is controlled. Recovery restores normal operations after the threat is removed. "
            "Simulation is tabletop or exercise activity during preparation, not the first step during an "
            "active incident."
        ),
        "choices": [
            "Eradication",
            "Recovery",
            "Containment",
            "Simulation",
        ],
        "objectives": ["4.8"],
    },
    {
        "slug": "classified-defense-espionage-motivation",
        "title": "Security+ — Espionage motivation (insider)",
        "stem": (
            "A government worker secretly copies classified files that contain defense tactics information to an "
            "external drive. The government worker then gives the external drive to a corrupt organization. Which of "
            "the following best describes the motivation of the worker?"
        ),
        "name": "secplus_q107",
        "correct": "A",
        "explain": (
            "Correct. A — Espionage is stealing sensitive or classified information for an unauthorized party, "
            "often a competing or hostile organization. Data exfiltration describes how data leaves the environment, "
            "not why the actor did it. Financial gain is motivation for profit, which the stem does not establish. "
            "Blackmail uses stolen or embarrassing information to coerce a victim."
        ),
        "choices": [
            "Espionage",
            "Data exfiltration",
            "Financial gain",
            "Blackmail",
        ],
        "objectives": ["2.1", "2.4"],
    },
    {
        "slug": "phishing-sim-report-suspicious-email",
        "title": "Security+ — Report suspicious email (phish sim)",
        "stem": (
            "An organization conducts a self-evaluation with a phishing campaign that requests login credentials. "
            "The organization receives the following results:\n"
            "• None of the staff were fooled by the attempt due to proper security awareness.\n"
            "• Staff deleted the email without performing any additional actions.\n"
            "Which of the following security practices would add the most value to the organization?"
        ),
        "name": "secplus_q108",
        "correct": "B",
        "explain": (
            "Correct. B — Staff recognized the phish but did not report it; updating guidance to report "
            "suspicious incidents lets security analyze, block, and hunt related messages. Mandatory password "
            "resets add little when no credentials were compromised. More spear-phishing training has lower "
            "value when awareness already stopped the attack. VPN requirements for remote workers do not "
            "address the reporting gap shown by the simulation results."
        ),
        "choices": [
            "Implement a strict password reset policy for all senior managers after a security event.",
            "Update user guidance to include suspicious incident reporting.",
            "Conduct end-user training regarding spear-phishing attempts to raise awareness.",
            "Require remote workers to use a VPN when connecting to the organization's networks.",
        ],
        "objectives": ["5.1", "2.2"],
    },
    {
        "slug": "hardware-vulnerability-firmware-version",
        "title": "Security+ — Hardware vuln (firmware)",
        "stem": "Which of the following is a hardware-specific vulnerability?",
        "name": "secplus_q109",
        "correct": "A",
        "explain": (
            "Correct. A — Outdated or flawed firmware is tied to specific hardware devices and their "
            "embedded code. Buffer overflows are common software memory flaws on many platforms. SQL injection "
            "targets application databases. Cross-site scripting targets web applications in user browsers."
        ),
        "choices": [
            "Firmware version",
            "Buffer overflow",
            "SQL injection",
            "Cross-site scripting",
        ],
        "objectives": ["2.3"],
    },
    {
        "slug": "employee-pii-privacy-data-classification",
        "title": "Security+ — Privacy data classification (employee PII)",
        "stem": (
            "A security professional discovers a folder containing an employee's personal information on the "
            "enterprise's shared drive. Which of the following best describes the data type the security "
            "professional should use to identify organizational policies and standards concerning the storage "
            "of employees' personal information?"
        ),
        "name": "secplus_q110",
        "correct": "C",
        "explain": (
            "Correct. C — Privacy data includes personally identifiable information (PII) such as employee "
            "personal records; policies for collection, storage, and sharing fall under privacy standards. "
            "Legal data covers contracts and regulatory filings. Financial data covers monetary records. "
            "Intellectual property covers proprietary business creations such as trade secrets and patents."
        ),
        "choices": [
            "Legal",
            "Financial",
            "Privacy",
            "Intellectual property",
        ],
        "objectives": ["3.3", "5.4"],
    },
    {
        "slug": "mssp-firewall-benchmark-config-template",
        "title": "Security+ — Benchmarks (firewall templates)",
        "stem": (
            "An MSSP manages firewalls for hundreds of clients. Which of the following tools would be most "
            "helpful to create a standard configuration template in order to improve the efficiency of firewall "
            "changes?"
        ),
        "name": "secplus_q111",
        "correct": "B",
        "explain": (
            "Correct. B — Security benchmarks (for example CIS benchmarks) provide consensus secure "
            "configuration baselines that MSSPs reuse as standard templates across clients. SNMP monitors "
            "devices and sends traps but does not define secure config templates. NetFlow analyzes traffic "
            "flows. SCAP automates compliance checking against standardized security content; benchmarks "
            "supply the configuration guidance templates themselves."
        ),
        "choices": [
            "SNMP",
            "Benchmarks",
            "Netflow",
            "SCAP",
        ],
        "objectives": ["4.4", "3.2"],
    },
    {
        "slug": "memory-injection-running-process-example",
        "title": "Security+ — Memory injection (definition)",
        "stem": "Which of the following is an example of memory injection?",
        "name": "secplus_q112",
        "correct": "C",
        "explain": (
            "Correct. C — Memory injection copies malicious code into the memory space of a process that is "
            "already running so it executes with that process's privileges. Shared-variable access between "
            "processes can enable privilege escalation but is not the memory injection pattern described here. "
            "Unexpected data causing code execution describes a buffer overflow. Overwriting an executable on "
            "disk is file-based tampering, not injection into live process memory."
        ),
        "choices": [
            "Two processes access the same variable, allowing one to cause a privilege escalation.",
            "A process receives an unexpected amount of data, which causes malicious code to be executed.",
            "Malicious code is copied to the allocated space of an already running process.",
            "An executable is overwritten on the disk, and malicious code runs the next time it is executed.",
        ],
        "objectives": ["2.3"],
    },
    {
        "slug": "daily-vuln-scans-patch-status",
        "title": "Security+ — Daily vuln scans (patching)",
        "stem": (
            "Which of the following would best explain why a security analyst is running daily vulnerability "
            "scans on all corporate endpoints?"
        ),
        "name": "secplus_q113",
        "correct": "A",
        "explain": (
            "Correct. A — Regular endpoint vulnerability scans identify missing patches and misconfigurations "
            "so teams can track remediation and verify patching status. Shadow IT discovery targets "
            "unsanctioned cloud services. Hardware inventory tracking is asset management, not the primary "
            "goal of vuln scanning. Threat hunting focuses on active adversary behavior, often using EDR, "
            "SIEM, and network analytics rather than daily patch-gap scans."
        ),
        "choices": [
            "To track the status of patching installations",
            "To find shadow IT cloud deployments",
            "To continuously monitor the hardware inventory",
            "To hunt for active attackers in the network",
        ],
        "objectives": ["4.3", "2.5"],
    },
    {
        "slug": "typosquatting-url-impersonation",
        "title": "Security+ — Typosquatting (URL impersonation)",
        "stem": (
            "Which of the following is a social engineering attack in which a bad actor impersonates a web URL?"
        ),
        "name": "secplus_q114",
        "correct": "C",
        "explain": (
            "Correct. C — Typosquatting registers look-alike domain names (misspellings or similar strings) "
            "that mimic legitimate URLs to trick users. Pretexting builds a false story to manipulate victims. "
            "Misinformation spreads false or misleading claims broadly. A watering-hole attack compromises a "
            "site victims are likely to visit rather than impersonating the URL itself."
        ),
        "choices": [
            "Pretexting",
            "Misinformation",
            "Typosquatting",
            "Watering-hole",
        ],
        "objectives": ["2.2", "2.4"],
    },
    {
        "slug": "wifi-wpa3-heat-map-site-survey",
        "title": "Security+ — Wi-Fi heat map (WPA3 design)",
        "stem": (
            "An office wants to install a Wi-Fi network. The security team must ensure a secure design. The "
            "access points will be more powerful and use WPA3 with a 16-character randomized key. Which of "
            "the following should the security team do next?"
        ),
        "name": "secplus_q115",
        "correct": "A",
        "explain": (
            "Correct. A — After selecting encryption and key strength, a heat map or site survey maps coverage "
            "and signal bleed so AP placement limits exposure outside the building perimeter. IPSec tunnels "
            "from each AP are not the standard next step for basic secure office Wi-Fi design. Downgrading to "
            "WPA2-PSK weakens the chosen control. Disabling SSH may be hardening but does not replace proper "
            "RF planning before deployment."
        ),
        "choices": [
            "Create a heat map of the building perimeter",
            "Deploy IPSec tunnels from each access point to the controller.",
            "Enable WPA2-PSK with a 24-character randomized key.",
            "Disable SSH administration on all access points.",
        ],
        "objectives": ["3.2", "2.5"],
    },
    {
        "slug": "physically-isolate-secure-systems-air-gapped",
        "title": "Security+ — Air-gapped (physical isolation)",
        "stem": (
            "A security consultant is working with a client that wants to physically isolate its secure systems. "
            "Which of the following best describes this architecture?"
        ),
        "name": "secplus_q116",
        "correct": "B",
        "explain": (
            "Correct. B — An air-gapped architecture physically isolates systems from untrusted networks, "
            "including the public internet. SDN programmatically separates control and data planes but does "
            "not inherently mean physical isolation. Containerization packages applications for portability "
            "and density. High availability provides redundancy and uptime, not isolation from other networks."
        ),
        "choices": [
            "SDN",
            "Air gapped",
            "Containerized",
            "Highly available",
        ],
        "objectives": ["3.1", "3.2"],
    },
    {
        "slug": "web-logs-directory-traversal-etc-passwd",
        "title": "Security+ — Directory traversal (web logs)",
        "stem": "",
        "name": "secplus_q117",
        "correct": "C",
        "explain": (
            "Correct. C — The ../ sequences in the filename parameter attempt path traversal to read "
            "/etc/passwd and /etc/shadow outside the web root. File injection uploads or embeds malicious "
            "files rather than climbing directories. Privilege escalation raises permissions after access. "
            "Cookie forgery manipulates session cookies, not URL path parameters."
        ),
        "choices": [
            "File injection",
            "Privilege escalation",
            "Directory traversal",
            "Cookie forgery",
        ],
        "prepend_html": build_web_server_directory_traversal_log_exhibit(),
        "objectives": ["2.3", "2.4"],
    },
    {
        "slug": "lost-decryption-key-escrow-recovery",
        "title": "Security+ — Key escrow (lost decryption key)",
        "stem": "Which of the following can assist in recovering data if the decryption key is lost?",
        "name": "secplus_q118",
        "correct": "D",
        "explain": (
            "Correct. D — Key escrow stores a copy of encryption keys with a trusted party or secure process "
            "so encrypted data can be recovered if the primary key is lost. A CSR requests a digital "
            "certificate from a CA. Salting adds randomness to password hashing. A root of trust anchors "
            "hardware or firmware integrity, not lost key recovery."
        ),
        "choices": [
            "CSR",
            "Salting",
            "Root of trust",
            "Escrow",
        ],
        "objectives": ["1.4", "3.3"],
    },
    {
        "slug": "dr-plan-cold-site-minimum-cost",
        "title": "Security+ — Cold site (minimum DR cost)",
        "stem": (
            "The executive management team is mandating the company develop a disaster recovery plan. The "
            "cost must be kept to a minimum, and the money to fund additional internet connections is not "
            "available. Which of the following would be the best option?"
        ),
        "name": "secplus_q119",
        "correct": "B",
        "explain": (
            "Correct. B — A cold site provides basic facility space and power at the lowest cost without "
            "standing production hardware or dedicated internet links. A hot site is fully equipped for "
            "immediate failover and is the most expensive. A warm site pre-stages some systems and "
            "connectivity at moderate cost. Failover site is a general term and still implies ready "
            "infrastructure rather than minimal standby space only."
        ),
        "choices": [
            "Hot site",
            "Cold site",
            "Failover site",
            "Warm site",
        ],
        "objectives": ["3.4", "5.2"],
    },
    {
        "slug": "post-incident-review-root-cause",
        "title": "Security+ — Post-incident review (root cause)",
        "stem": (
            "Which of the following activities is included in the post-incident review phase?"
        ),
        "name": "secplus_q120",
        "correct": "A",
        "explain": (
            "Correct. A — Post-incident review (lessons learned) includes root cause analysis to learn how "
            "the incident occurred and prevent recurrence. Developing mitigation steps often follows from "
            "that analysis but root cause determination is a core review activity. Evidence validation "
            "occurs during investigation and forensics. Reestablishing system configuration is part of "
            "recovery, before the formal post-incident review."
        ),
        "choices": [
            "Determining the root cause of the incident",
            "Developing steps to mitigate the risks of the incident",
            "Validating the accuracy of the evidence collected during the investigation",
            "Reestablishing the compromised system's configuration and settings",
        ],
        "objectives": ["4.8", "5.1"],
    },
    {
        "slug": "external-attacks-nips-protection",
        "title": "Security+ — NIPS (external attacks)",
        "stem": (
            "Which of the following should an organization use to protect its environment from external attacks "
            "conducted by an unauthorized hacker?"
        ),
        "name": "secplus_q121",
        "correct": "D",
        "explain": (
            "Correct. D — A network intrusion prevention system (NIPS) sits at the network perimeter, "
            "detects attack patterns in traffic, and can block malicious activity inline before it reaches "
            "internal systems. ACLs filter by rules such as IP and port but do not analyze attack signatures "
            "the way NIPS does. IDS is primarily detective. HIDS monitors individual hosts rather than "
            "perimeter traffic from external attackers."
        ),
        "choices": [
            "ACL",
            "IDS",
            "HIDS",
            "NIPS",
        ],
        "objectives": ["2.5", "4.4"],
    },
    {
        "slug": "mdm-lost-phone-screen-lock-remote-wipe",
        "title": "Security+ — MDM (lost phone, choose two)",
        "stem": (
            "A company implemented an MDM policy to mitigate risks after repeated instances of employees "
            "losing company-provided mobile phones. In several cases, the lost phones were used maliciously to "
            "perform social engineering attacks against other employees. Which of the following MDM features "
            "should be configured to best address this issue? (Select two.)"
        ),
        "name": "secplus_q122",
        "choose_two": True,
        "correct": ["A", "B"],
        "explain": (
            "Correct. A and B — Screen locks block unauthorized use of a lost device so attackers cannot "
            "impersonate the employee via calls, texts, or apps. Remote wipe erases corporate data and stops "
            "further abuse when a device cannot be recovered. Full device encryption protects data at rest but "
            "does not stop active misuse if the device is unlocked. Push notifications, application management, "
            "and geolocation do not directly prevent social engineering from a lost unlocked phone."
        ),
        "choices": [
            "Screen locks",
            "Remote wipe",
            "Full device encryption",
            "Push notifications",
            "Application management",
            "Geolocation",
        ],
        "objectives": ["2.5", "4.1"],
    },
    {
        "slug": "international-expansion-on-premises-security",
        "title": "Security+ — On-premises (highest control)",
        "stem": (
            "An organization plans to expand its operations internationally and needs to keep data at the new "
            "location secure. The organization wants to use the most secure architecture model possible. Which of "
            "the following models offers the highest level of security?"
        ),
        "name": "secplus_q123",
        "correct": "C",
        "explain": (
            "Correct. C — On-premises infrastructure gives the organization direct control over physical "
            "security, access, and data at the new site without a cloud shared-responsibility split. Cloud "
            "and hybrid models depend on provider controls and customer configuration. Peer-to-peer "
            "architectures lack centralized enterprise security governance."
        ),
        "choices": [
            "Cloud-based",
            "Peer-to-peer",
            "On-premises",
            "Hybrid",
        ],
        "objectives": ["3.1", "3.2"],
    },
    {
        "slug": "containers-reduce-os-patching",
        "title": "Security+ — Containers (fewer OS patches)",
        "stem": (
            "An organization is looking to optimize its environment and reduce the number of patches necessary "
            "for operating systems. Which of the following will best help to achieve this objective?"
        ),
        "name": "secplus_q124",
        "correct": "D",
        "explain": (
            "Correct. D — Containers share the host OS kernel, so many workloads run on one patched host "
            "instead of each VM or server carrying a full guest operating system. Virtualization still "
            "requires patching every guest OS. Microservices describe application design, not fewer OS "
            "instances. A real-time operating system is specialized firmware or control software, not a "
            "general strategy to cut enterprise OS patch volume."
        ),
        "choices": [
            "Microservices",
            "Virtualization",
            "Real-time operating system",
            "Containers",
        ],
        "objectives": ["3.1", "3.2"],
    },
    {
        "slug": "saas-soc2-report-due-diligence",
        "title": "Security+ — Due diligence (SOC 2 report)",
        "stem": (
            "A security analyst is evaluating a SaaS application that the human resources department would "
            "like to implement. The analyst requests a SOC 2 report from the SaaS vendor. Which of the "
            "following processes is the analyst most likely conducting?"
        ),
        "name": "secplus_q125",
        "correct": "D",
        "explain": (
            "Correct. D — Due diligence is the vendor risk assessment performed before adopting a third-party "
            "service; reviewing a SOC 2 report is a common due diligence step. The SOC 2 report itself is "
            "an attestation from an independent auditor, not the process the customer analyst performs. "
            "Internal audit reviews the organization's own controls. Penetration testing actively probes "
            "for vulnerabilities rather than reviewing vendor audit documentation."
        ),
        "choices": [
            "Internal audit",
            "Penetration testing",
            "Attestation",
            "Due diligence",
        ],
        "objectives": ["5.3", "5.5"],
    },
    {
        "slug": "zero-trust-continuous-validation",
        "title": "Security+ — Zero Trust (continuous validation)",
        "stem": "Which of the following is an example of implementing Zero Trust architecture?",
        "name": "secplus_q126",
        "correct": "C",
        "explain": (
            "Correct. C — Zero Trust grants access only after ongoing verification of identity, device health, "
            "and context for each resource request, not a one-time login trust. Strong perimeter boundaries "
            "and prioritizing external perimeter defense reflect traditional castle-and-moat models. Verifying "
            "identity once at session start leaves later access unchallenged when risk changes."
        ),
        "choices": [
            "Building strong network boundaries to prevent intrusion",
            "Verifying user identity once at the start of the session",
            "Granting resource access after continuous validation",
            "Prioritizing perimeter defense to block external threats",
        ],
        "objectives": ["1.2", "3.1"],
    },
    {
        "slug": "web-server-go-live-harden-virtual-host",
        "title": "Security+ — Harden host (web server go-live)",
        "stem": (
            "Which of the following should a security team do first before a new web server goes live?"
        ),
        "name": "secplus_q127",
        "correct": "A",
        "explain": (
            "Correct. A — Hardening the virtual host is the first step: secure baseline configuration, "
            "disable unneeded services, and reduce attack surface before exposure. WAF rules depend on the "
            "application and are tuned after the host is secured. Network intrusion detection monitors traffic "
            "but does not replace baseline host hardening. Patch management is critical and often part of "
            "hardening, but securing the host configuration comes first in go-live preparation."
        ),
        "choices": [
            "Harden the virtual host.",
            "Create WAF rules.",
            "Enable network intrusion detection.",
            "Apply patch management",
        ],
        "objectives": ["3.2", "4.1"],
    },
    {
        "slug": "ip-camera-live-stream-srtp",
        "title": "Security+ — SRTP (encrypted camera stream)",
        "stem": (
            "An organization implemented cloud-managed IP cameras to monitor building entry points and "
            "sensitive areas. The service provider enables direct TCP/IP connection to stream live video "
            "footage from each camera. The organization wants to ensure this stream is encrypted and "
            "authenticated. Which of the following protocols should be implemented to best meet this objective?"
        ),
        "name": "secplus_q128",
        "correct": "B",
        "explain": (
            "Correct. B — SRTP (Secure Real-time Transport Protocol) encrypts and authenticates real-time "
            "media such as live IP camera video carried over RTP. SSH secures interactive shell and file "
            "sessions, not typical camera video streams. S/MIME protects email content. PPTP is an outdated "
            "VPN tunneling protocol and is not used to secure individual live video feeds."
        ),
        "choices": [
            "SSH",
            "SRTP",
            "S/MIME",
            "PPTP",
        ],
        "objectives": ["1.4", "3.2"],
    },
    {
        "slug": "revise-change-management-cloud-updates",
        "title": "Security+ — Revise CM policy (cloud)",
        "stem": (
            "Which of the following will most likely lead an organization to revise its change management "
            "policy?"
        ),
        "name": "secplus_q129",
        "correct": "C",
        "explain": (
            "Correct. C — Migrating to a cloud platform with more flexible, frequent updates requires "
            "revising change management policy for automated pipelines, faster approvals, and cloud-specific "
            "controls. Adding a production feature is a normal change handled by existing policy. A server "
            "running at maximum load is a capacity issue, not a policy driver. A legacy server that cannot "
            "meet regulations may require remediation or compensating controls, but the stem that best maps "
            "to policy revision for how changes are managed is the new cloud update model."
        ),
        "choices": [
            "An engineer adds a new feature to the production service",
            "A production server continuously runs at its maximum load.",
            "Software is migrated to a cloud that offers increased flexibility in its updates.",
            "A legacy server lacks support for new regulatory requirements.",
        ],
        "objectives": ["1.3"],
    },
    {
        "slug": "automate-data-sharing-api",
        "title": "Security+ — API (automate data sharing)",
        "stem": (
            "A security analyst wants to automate a task that shares data between systems. Which of the "
            "following is the best option for the analyst to use?"
        ),
        "name": "secplus_q130",
        "correct": "B",
        "explain": (
            "Correct. B — APIs provide structured, programmatic interfaces so systems can exchange data "
            "securely as part of automated workflows. SOAR orchestrates broader security response playbooks "
            "and often uses APIs underneath but is not the direct integration mechanism. SFTP transfers files "
            "but is not the best general option for automated system-to-system data sharing. RDP provides "
            "remote desktop access, not automated data exchange."
        ),
        "choices": [
            "SOAR",
            "API",
            "SFTP",
            "RDP",
        ],
        "objectives": ["4.7", "1.2"],
    },
    {
        "slug": "radius-server-aaa-authentication",
        "title": "Security+ — RADIUS (AAA)",
        "stem": (
            "Which of the following security concepts is accomplished with the installation of a RADIUS server?"
        ),
        "name": "secplus_q131",
        "correct": "B",
        "explain": (
            "Correct. B — RADIUS (Remote Authentication Dial-In User Service) centralizes authentication, "
            "authorization, and accounting (AAA) for network access. The exam option AA reflects "
            "authentication and authorization; accounting is also part of full AAA. CIA is the confidentiality, "
            "integrity, and availability triad. ACLs are access control lists on devices. PEM is a certificate "
            "encoding format, not what RADIUS implements."
        ),
        "choices": [
            "CIA",
            "AA",
            "ACL",
            "PEM",
        ],
        "objectives": ["1.2", "4.5"],
    },
    {
        "slug": "service-provider-baseline-enforcement-scale",
        "title": "Security+ — Baseline enforcement (MSP scale)",
        "stem": (
            "A service provider wants a cost-effective way to rapidly expand from providing internet links to "
            "managing them. Which of the following methods will allow the service provider to best scale its "
            "services while maintaining performance consistency?"
        ),
        "name": "secplus_q132",
        "correct": "C",
        "explain": (
            "Correct. C — Baseline enforcement standardizes secure configurations across customers so the "
            "provider can scale without performance or security drift. Escalation support handles incidents "
            "but does not standardize delivery at scale. Increasing workforce raises cost and does not ensure "
            "consistency. Technical debt accumulates shortcuts that harm long-term operations and consistency."
        ),
        "choices": [
            "Escalation support",
            "Increased workforce",
            "Baseline enforcement",
            "Technical debt",
        ],
        "objectives": ["4.7", "4.1"],
    },
    {
        "slug": "firewall-fail-closed-confidentiality-priority",
        "title": "Security+ — Fail-closed (confidentiality priority)",
        "stem": (
            "A company processes a large volume of business-to-business transactions and prioritizes data "
            "confidentiality over transaction availability. The company's firewall administrator must configure "
            "a new hardware-based firewall to replace the current one. Which of the following should the "
            "administrator do to best align with the company requirements in case a security event occurs?"
        ),
        "name": "secplus_q133",
        "correct": "A",
        "explain": (
            "Correct. A — Fail-closed mode stops traffic when the firewall data plane fails or is overwhelmed, "
            "favoring confidentiality over keeping transactions flowing. A final implicit deny is standard "
            "practice but does not define failure behavior. Prioritizing business-critical traffic improves "
            "availability for key apps. Rate limiting mitigates floods but does not express confidentiality "
            "over availability during a security event."
        ),
        "choices": [
            "Ensure the firewall data plane moves to fail-closed mode.",
            "Implement a deny-all rule as the last firewall ACL rule.",
            "Prioritize business-critical application traffic through the firewall.",
            "Configure rate limiting between the firewall interfaces.",
        ],
        "objectives": ["1.2", "3.2"],
    },
    {
        "slug": "fde-workstations-data-at-rest",
        "title": "Security+ — FDE (data at rest)",
        "stem": (
            "A network administrator deploys an FDE solution on all end user workstations. Which of the "
            "following data protection strategies does this describe?"
        ),
        "name": "secplus_q134",
        "correct": "D",
        "explain": (
            "Correct. D — Full disk encryption (FDE) protects data at rest on workstation storage. Masking "
            "redacts or hides sensitive field values for display. Data in transit protections apply while "
            "data moves across networks. Obfuscation makes data difficult to understand but is not the same "
            "as encrypting stored volumes. Data sovereignty concerns legal jurisdiction over where data is "
            "stored and processed."
        ),
        "choices": [
            "Masking",
            "Data in transit",
            "Obfuscation",
            "Data at rest",
            "Data sovereignty",
        ],
        "objectives": ["3.3", "1.4"],
    },
    {
        "slug": "next-gen-siem-automated-response",
        "title": "Security+ — Next-gen SIEM (automated response)",
        "stem": "Which of the following is a feature of a next-generation SIEM system?",
        "name": "secplus_q135",
        "correct": "B",
        "explain": (
            "Correct. B — Next-generation SIEM platforms add orchestration and automated response actions "
            "(playbooks) beyond traditional log collection and correlation. Virus signatures belong to "
            "antivirus or IPS engines. Deploying security agents is an EDR or endpoint management function. "
            "Vulnerability scanning is performed by dedicated scanners, though findings may feed a SIEM."
        ),
        "choices": [
            "Virus signatures",
            "Automated response actions",
            "Security agent deployment",
            "Vulnerability scanning",
        ],
        "objectives": ["4.4", "4.7"],
    },
    {
        "slug": "internet-facing-app-bug-bounty-program",
        "title": "Security+ — Bug bounty program",
        "stem": (
            "A company is expanding its threat surface program and allowing individuals to security test the "
            "company's internet-facing application. The company will compensate researchers based on the "
            "vulnerabilities discovered. Which of the following best describes the program the company is "
            "setting up?"
        ),
        "name": "secplus_q136",
        "correct": "B",
        "explain": (
            "Correct. B — A bug bounty rewards external researchers for reporting valid vulnerabilities in "
            "scoped systems. Open-source intelligence collects public information rather than paying for "
            "findings. A red team simulates adversaries in a controlled engagement, usually not an open "
            "crowdsourced reward model. Penetration testing is a contracted assessment, not typically an "
            "ongoing public compensation program for any researcher who reports bugs."
        ),
        "choices": [
            "Open-source intelligence",
            "Bug bounty",
            "Red team",
            "Penetration testing",
        ],
        "objectives": ["2.2", "5.5"],
    },
    {
        "slug": "wwww-domain-typosquatting-attack",
        "title": "Security+ — Typosquatting (wwww domain)",
        "stem": (
            "A company's website is www.company.com. Attackers purchased the domain wwww.company.com. "
            "Which of the following types of attacks describes this example?"
        ),
        "name": "secplus_q137",
        "correct": "A",
        "explain": (
            "Correct. A — Typosquatting registers look-alike domains that users may reach through typos, such "
            "as an extra w in www. Brand impersonation misuses a brand identity but is broader than a "
            "misspelled domain purchase. An on-path attack intercepts communications between parties. A "
            "watering-hole attack compromises a site victims are expected to visit."
        ),
        "choices": [
            "Typosquatting",
            "Brand Impersonation",
            "On-path",
            "Watering-hole",
        ],
        "objectives": ["2.2", "2.4"],
    },
    {
        "slug": "tabletop-exercise-update-irp",
        "title": "Security+ — Tabletop (update IRP)",
        "stem": "Which of the following is the best reason to perform a tabletop exercise?",
        "name": "secplus_q138",
        "correct": "C",
        "explain": (
            "Correct. C — Tabletop exercises walk stakeholders through scenarios to validate and improve the "
            "incident response plan (IRP). They may surface audit gaps but are not primarily for closing "
            "findings. Measuring remediation response times requires hands-on drills or live exercises. ROI "
            "calculations are a business metric, not the main purpose of a discussion-based tabletop."
        ),
        "choices": [
            "To address audit findings",
            "To collect remediation response times",
            "To update the IRP",
            "To calculate the ROI",
        ],
        "objectives": ["4.8", "5.1"],
    },
    {
        "slug": "rainbow-table-salting-defense",
        "title": "Security+ — Salting (rainbow tables)",
        "stem": (
            "Which of the following explains why an attacker cannot easily decrypt passwords using a rainbow "
            "table attack?"
        ),
        "name": "secplus_q139",
        "correct": "B",
        "explain": (
            "Correct. B — Salting adds unique random data to each password before hashing, defeating "
            "precomputed rainbow tables that target unsalted hashes. Digital signatures verify authenticity "
            "and integrity of messages or code. Hashing stores passwords as digests but alone does not stop "
            "rainbow tables without per-password salts. Perfect forward secrecy protects past session keys in "
            "TLS, not stored password databases."
        ),
        "choices": [
            "Digital signatures",
            "Salting",
            "Hashing",
            "Perfect forward secrecy",
        ],
        "objectives": ["1.4", "2.3"],
    },
    {
        "slug": "siem-logs-correlation-multiple-hosts",
        "title": "Security+ — SIEM (cross-host correlation)",
        "stem": (
            "Which of the following is the most likely reason a security analyst would review SIEM logs?"
        ),
        "name": "secplus_q140",
        "correct": "D",
        "explain": (
            "Correct. D — A SIEM aggregates and correlates security events from many hosts and sources to "
            "detect patterns a single log stream would miss. Password reset review may use identity logs "
            "directly. DDoS monitoring often relies on network flow and perimeter tools as well. Privacy "
            "breach scope assessment uses broader data governance and forensic sources beyond SIEM alone."
        ),
        "choices": [
            "To check for recent password reset attempts",
            "To monitor for potential DDoS attacks",
            "To assess the scope of a privacy breach",
            "To see correlations across multiple hosts",
        ],
        "objectives": ["4.4", "4.9"],
    },
    {
        "slug": "ryk-extension-ransomware-infection",
        "title": "Security+ — Ransomware (.ryk extension)",
        "stem": (
            "An administrator finds that all user workstations and servers are displaying a message that is "
            "associated with files containing an extension of .ryk. Which of the following types of infections "
            "is present on the systems?"
        ),
        "name": "secplus_q141",
        "correct": "D",
        "explain": (
            "Correct. D — A uniform ransom note and renamed encrypted files with a new extension such as .ryk "
            "indicate ransomware. A virus self-replicates by attaching to other files. A trojan masquerades as "
            "legitimate software. Spyware covertly collects information without typically encrypting files "
            "across the enterprise with a displayed ransom message."
        ),
        "choices": [
            "Virus",
            "Trojan",
            "Spyware",
            "Ransomware",
        ],
        "objectives": ["2.3", "2.4"],
    },
    {
        "slug": "failed-change-backout-plan",
        "title": "Security+ — Backout plan (failed change)",
        "stem": (
            "A company makes a change during the appropriate change window, but the unsuccessful change "
            "extends beyond the scheduled time and impacts customers. Which of the following would prevent "
            "this from reoccurring?"
        ),
        "name": "secplus_q142",
        "correct": "D",
        "explain": (
            "Correct. D — A backout (rollback) plan defines how to restore service quickly if a change fails, "
            "limiting customer impact beyond the maintenance window. User notification informs stakeholders "
            "but does not reverse a failed change. Change approval validates the change before work starts "
            "but does not address failure recovery. Risk analysis identifies potential issues beforehand "
            "rather than executing recovery when a change goes wrong."
        ),
        "choices": [
            "User notification",
            "Change approval",
            "Risk analysis",
            "Backout plan",
        ],
        "objectives": ["1.3", "4.8"],
    },
    {
        "slug": "vulnerability-management-reporting-prioritization",
        "title": "Security+ — Vuln mgmt (choose two)",
        "stem": (
            "Which of the following activities are associated with vulnerability management? (Select two.)"
        ),
        "name": "secplus_q143",
        "choose_two": True,
        "correct": ["A", "B"],
        "explain": (
            "Correct. A and B — Vulnerability management includes prioritizing findings by risk and severity "
            "and reporting status to stakeholders. Exploiting vulnerabilities is an attacker or pentest "
            "activity, not a defensive management step. Correlation is primarily a SIEM or analytics function. "
            "Containment is an incident response activity. A tabletop exercise validates incident response "
            "plans."
        ),
        "choices": [
            "Reporting",
            "Prioritization",
            "Exploiting",
            "Correlation",
            "Containment",
            "Tabletop exercise",
        ],
        "objectives": ["4.3"],
    },
    {
        "slug": "unknown-patch-fim-rootkit",
        "title": "Security+ — Rootkit (FIM / bad patch)",
        "stem": (
            "A user downloads a patch from an unknown repository. FIM alerts indicate OS file hashes have "
            "changed. Which attack most likely occurred?"
        ),
        "name": "secplus_q144",
        "correct": "D",
        "explain": (
            "Correct. D — A malicious patch from an untrusted source can install a rootkit that alters OS "
            "files and is detected by file integrity monitoring. A logic bomb waits for a trigger condition. "
            "A keylogger captures input and does not typically change core OS file hashes. Ransomware "
            "usually renames and encrypts user data with ransom notes rather than silently modifying OS "
            "binaries through a fake patch."
        ),
        "choices": [
            "Logic bomb",
            "Keylogger",
            "Ransomware",
            "Rootkit",
        ],
        "objectives": ["2.3", "2.4"],
    },
    {
        "slug": "risk-avoidance-different-market-segment",
        "title": "Security+ — Risk avoidance (market segment)",
        "stem": (
            "A company is aware of a given security risk related to a specific market segment. The business "
            "chooses not to accept responsibility and targets its services to a different market segment. "
            "Which of the following describes this risk management strategy?"
        ),
        "name": "secplus_q145",
        "correct": "C",
        "explain": (
            "Correct. C — Avoidance eliminates exposure by not engaging in the risky activity, here by "
            "serving a different market instead of accepting risk in the original segment. Transfer shifts "
            "risk to another party such as through insurance. An exception or exemption is an approved "
            "deviation from policy while still operating in scope, not leaving the market entirely."
        ),
        "choices": [
            "Exemption",
            "Exception",
            "Avoid",
            "Transfer",
        ],
        "objectives": ["5.2"],
    },
    {
        "slug": "file-label-data-classification",
        "title": "Security+ — Data classification (file label)",
        "stem": (
            "Which of the following should be used to select a label for a file based on the file's value, "
            "sensitivity, or applicable regulations?"
        ),
        "name": "secplus_q146",
        "correct": "C",
        "explain": (
            "Correct. C — Data classification assigns labels such as public, internal, or confidential based "
            "on sensitivity and regulatory requirements. Verification confirms identity or correctness. "
            "Certification is formal attestation of compliance or skills. An inventory lists assets or files "
            "but does not define the labeling criteria."
        ),
        "choices": [
            "Verification",
            "Certification",
            "Classification",
            "Inventory",
        ],
        "objectives": ["3.3", "5.4"],
    },
    {
        "slug": "security-awareness-phishing-campaign",
        "title": "Security+ — Awareness program (phishing)",
        "stem": (
            "A security officer is implementing a security awareness program and is placing security-themed "
            "posters around the building and is assigning online user training. Which of the following would "
            "the security officer most likely implement?"
        ),
        "name": "secplus_q147",
        "correct": "C",
        "explain": (
            "Correct. C — Simulated phishing campaigns are a common awareness control alongside posters and "
            "e-learning to measure and improve user behavior. A password policy sets technical requirements "
            "but is not the typical hands-on awareness activity paired with training. Access badges enforce "
            "physical entry control. A risk assessment identifies and ranks risks rather than delivering "
            "user awareness content."
        ),
        "choices": [
            "Password policy",
            "Access badges",
            "Phishing campaign",
            "Risk assessment",
        ],
        "objectives": ["5.1", "2.2"],
    },
    {
        "slug": "decommission-drive-sanitization-recycling",
        "title": "Security+ — Sanitization (recycling)",
        "stem": (
            "A company requires hard drives to be securely wiped before sending decommissioned systems to "
            "recycling. Which of the following best describes this policy?"
        ),
        "name": "secplus_q148",
        "correct": "B",
        "explain": (
            "Correct. B — Sanitization removes data from storage media so it cannot be recovered, using methods "
            "such as secure wipe or purge before equipment is recycled. Destruction physically destroys "
            "media so it cannot be reused. Enumeration and inventory track or list assets rather than define "
            "secure data removal procedures."
        ),
        "choices": [
            "Enumeration",
            "Sanitization",
            "Destruction",
            "Inventory",
        ],
        "objectives": ["4.2", "3.3"],
    },
    {
        "slug": "osint-public-breach-information",
        "title": "Security+ — OSINT (public breach info)",
        "stem": (
            "Which of the following can be best used to discover a company's publicly available breach "
            "information?"
        ),
        "name": "secplus_q149",
        "correct": "A",
        "explain": (
            "Correct. A — OSINT gathers information from public sources such as news, breach disclosures, "
            "and open databases. A SIEM correlates internal security logs. CVE lists vulnerability identifiers. "
            "CVSS scores vulnerability severity; neither CVE nor CVSS reports whether a company suffered a "
            "public breach."
        ),
        "choices": [
            "OSINT",
            "SIEM",
            "CVE",
            "CVSS",
        ],
        "objectives": ["4.3", "4.9"],
    },
    {
        "slug": "physical-security-tailgating-situational-awareness",
        "title": "Security+ — Situational awareness (tailgating)",
        "stem": (
            "The physical security team at a company receives reports that employees are not displaying "
            "their badges. The team also observes employees tailgating at controlled entrances. Which of the "
            "following topics will the security team most likely emphasize in upcoming security training?"
        ),
        "name": "secplus_q150",
        "correct": "B",
        "explain": (
            "Correct. B — Situational awareness training addresses wearing badges, challenging unknown "
            "persons, and not allowing tailgating at secured doors. Social engineering covers manipulation "
            "tactics; tailgating can be one example but the stem focuses on employee vigilance and physical "
            "protocols. Phishing targets electronic messages. An acceptable use policy governs system and "
            "resource use, not physical entry behavior."
        ),
        "choices": [
            "Social engineering",
            "Situational awareness",
            "Phishing",
            "Acceptable use policy",
        ],
        "objectives": ["2.2", "5.1"],
    },
    {
        "slug": "donate-network-hardware-sanitization",
        "title": "Security+ — Sanitization (donate hardware)",
        "stem": (
            "An organization wants to donate its aging network hardware. Which of the following should the "
            "organization perform to prevent any network details from leaking?"
        ),
        "name": "secplus_q151",
        "correct": "B",
        "explain": (
            "Correct. B — Sanitization removes stored configurations, credentials, and data from devices before "
            "they leave the organization so network details are not exposed. Destruction renders equipment "
            "unusable and unsuitable for donation. Certification attests to compliance but does not erase "
            "device contents. Data retention defines how long data is kept, not how to clear hardware being "
            "donated."
        ),
        "choices": [
            "Destruction",
            "Sanitization",
            "Certification",
            "Data retention",
        ],
        "objectives": ["4.2", "3.3"],
    },
    {
        "slug": "national-id-dlp-accidental-disclosure",
        "title": "Security+ — DLP (national identity data)",
        "stem": (
            "A business is expanding to a new country and must protect customers from accidental disclosure "
            "of specific national identity information. Which of the following should the security engineer "
            "update to best meet business requirements?"
        ),
        "name": "secplus_q152",
        "correct": "C",
        "explain": (
            "Correct. C — DLP policies can detect and block transmission of regulated national identity data "
            "in email, cloud uploads, and endpoints to prevent accidental disclosure. A SIEM aggregates "
            "and correlates logs but does not primarily stop data exfiltration at the channel. SCAP automates "
            "configuration compliance checking. A WAF protects web applications from common web attacks, "
            "not organization-wide accidental PII leakage."
        ),
        "choices": [
            "SIEM",
            "SCAP",
            "DLP",
            "WAF",
        ],
        "objectives": ["3.3", "4.4"],
    },
    {
        "slug": "data-sanitization-used-hard-drives",
        "title": "Security+ — Sanitization (used drives)",
        "stem": "Which of the following is prevented by proper data sanitization?",
        "name": "secplus_q153",
        "correct": "A",
        "explain": (
            "Correct. A — Sanitization overwrites or purges data on storage media so attackers cannot recover "
            "information from discarded or donated hard drives. End-of-life support is a vendor lifecycle "
            "issue addressed by replacement or compensating controls. Incorrect classification is mitigated "
            "by classification policy and labeling. Inventory accuracy is an asset management function, not "
            "sanitization."
        ),
        "choices": [
            "Hackers' ability to obtain data from used hard drives",
            "Devices reaching end-of-life and losing support",
            "Disclosure of sensitive data through incorrect classification",
            "Incorrect inventory data leading to a laptop shortage",
        ],
        "objectives": ["4.2", "3.3"],
    },
    {
        "slug": "multiple-log-types-siem-management",
        "title": "Security+ — SIEM (multiple log types)",
        "stem": (
            "Which of the following strategies should an organization use to efficiently manage and analyze "
            "multiple types of logs?"
        ),
        "name": "secplus_q154",
        "correct": "A",
        "explain": (
            "Correct. A — A SIEM centralizes collection, normalization, correlation, and analysis of logs from "
            "diverse systems. Custom scripts may work at small scale but lack integrated correlation and "
            "reporting at enterprise level. EDR focuses on endpoint telemetry rather than all log sources. A "
            "UTM consolidates perimeter security functions but is not a full multi-source log management "
            "platform."
        ),
        "choices": [
            "Deploy a SIEM solution",
            "Create custom scripts to aggregate and analyze logs",
            "Implement EDR technology",
            "Install a unified threat management appliance",
        ],
        "objectives": ["4.4", "4.9"],
    },
    {
        "slug": "input-field-sql-injection-data-manipulation",
        "title": "Security+ — SQL injection (input field)",
        "stem": (
            "Which of the following enables the use of an input field to run commands that can view or "
            "manipulate data?"
        ),
        "name": "secplus_q155",
        "correct": "D",
        "explain": (
            "Correct. D — SQL injection sends crafted input in a form or parameter to execute unintended "
            "database queries that read or change data. Cross-site scripting runs script in a user browser. "
            "Side loading installs unauthorized applications on a device. A buffer overflow corrupts memory "
            "by exceeding buffer bounds, not typically through database query injection in an input field."
        ),
        "choices": [
            "Cross-site scripting",
            "Side loading",
            "Buffer overflow",
            "SQL injection",
        ],
        "objectives": ["2.3", "2.5"],
    },
    {
        "slug": "bulk-unsolicited-messages-phishing",
        "title": "Security+ — Phishing (bulk unsolicited email)",
        "stem": (
            "An administrator learns that users are receiving large quantities of unsolicited messages. The "
            "administrator checks the content filter and sees hundreds of messages sent to multiple users. "
            "Which of the following best describes this kind of attack?"
        ),
        "name": "secplus_q156",
        "correct": "D",
        "explain": (
            "Correct. D — Mass unsolicited email to many users is commonly phishing or spam carrying "
            "phishing lures; among the choices, phishing best fits deceptive bulk messages. A watering-hole "
            "attack compromises a site users visit. Typosquatting uses look-alike domains, not bulk inbox "
            "delivery. Business email compromise is a targeted impersonation scam, not hundreds of generic "
            "messages to many users."
        ),
        "choices": [
            "Watering hole",
            "Typosquatting",
            "Business email compromise",
            "Phishing",
        ],
        "objectives": ["2.2", "2.4"],
    },
    {
        "slug": "repeatable-sanitization-reuse-hard-drives",
        "title": "Security+ — Sanitization (reuse drives)",
        "stem": (
            "Which of the following is a common data removal option for companies that want to wipe sensitive "
            "data from hard drives in a repeatable manner but allow the hard drives to be reused?"
        ),
        "name": "secplus_q157",
        "correct": "A",
        "explain": (
            "Correct. A — Sanitization uses documented procedures such as secure overwrite or purge so data "
            "cannot be recovered while media can be reused. Standard formatting does not reliably remove "
            "recoverable data. Degaussing magnetically erases many HDDs and often prevents reuse. "
            "Defragmentation reorganizes file storage and is not a secure data removal method."
        ),
        "choices": [
            "Sanitization",
            "Formatting",
            "Degaussing",
            "Defragmentation",
        ],
        "objectives": ["4.2", "3.3"],
    },
    {
        "slug": "ceo-gift-card-smishing-attack",
        "title": "Security+ — Smishing (CEO gift cards)",
        "stem": (
            "An employee receives a text message from an unknown number claiming to be the company's Chief "
            "Executive Officer and asking the employee to purchase several gift cards. Which of the following "
            "types of attacks does this describe?"
        ),
        "name": "secplus_q158",
        "correct": "B",
        "explain": (
            "Correct. B — Smishing is phishing conducted through SMS text messages. Vishing uses voice "
            "calls. Pretexting is creating a false scenario and may be present here, but the question asks "
            "for the attack type tied to the text channel. Phishing is broader; smishing is the specific term "
            "for fraudulent texts."
        ),
        "choices": [
            "Vishing",
            "Smishing",
            "Pretexting",
            "Phishing",
        ],
        "objectives": ["2.2", "2.4"],
    },
    {
        "slug": "private-cloud-sensitive-data-ipsec",
        "title": "Security+ — IPSec (private cloud comms)",
        "stem": (
            "A systems administrator needs to ensure the secure communication of sensitive data within the "
            "organization's private cloud. Which of the following is the best choice for the administrator "
            "to implement?"
        ),
        "name": "secplus_q159",
        "correct": "A",
        "explain": (
            "Correct. A — IPSec encrypts and authenticates IP traffic between systems and is commonly used "
            "to protect communications in private cloud and hybrid networks. SHA-1 is a legacy hash "
            "algorithm for integrity, not a full communication protection suite. RSA is an asymmetric "
            "algorithm used within protocols such as TLS but is not a standalone network encryption choice. "
            "A TGT is a Kerberos ticket used for authentication, not for encrypting data in transit."
        ),
        "choices": [
            "IPSec",
            "SHA-1",
            "RSA",
            "TGT",
        ],
        "objectives": ["1.4", "3.2"],
    },
    {
        "slug": "iac-configuration-managed-replicated",
        "title": "Security+ — IaC (managed configuration)",
        "stem": (
            "Which of the following makes Infrastructure as Code (IaC) a preferred security architecture "
            "over traditional infrastructure models?"
        ),
        "name": "secplus_q160",
        "correct": "B",
        "explain": (
            "Correct. B — IaC defines infrastructure in version-controlled code so secure configurations are "
            "managed consistently and replicated across environments with less manual drift. It does not "
            "make common attacks ineffective by itself. Outsourcing is a cloud or MSSP decision, not unique "
            "to IaC. Optimization across instances is a performance benefit, not the primary security "
            "architecture advantage cited for IaC."
        ),
        "choices": [
            "Common attacks are less likely to be effective.",
            "Configuration can be better managed and replicated.",
            "Outsourcing to a third party with more expertise in network defense is possible.",
            "Optimization can occur across a number of computing instances.",
        ],
        "objectives": ["3.1", "3.2"],
    },
    {
        "slug": "bc-staff-capacity-planning",
        "title": "Security+ — Capacity planning (BC staffing)",
        "stem": (
            "A company is developing a business continuity strategy and needs to determine how many staff "
            "members would be required to sustain the business in the case of a disruption. Which of the "
            "following best describes this step?"
        ),
        "name": "secplus_q161",
        "correct": "A",
        "explain": (
            "Correct. A — Capacity planning estimates the people, systems, and resources needed to maintain "
            "required service levels during a disruption. Redundancy provides duplicate components for "
            "resilience but does not calculate staffing requirements. Geographic dispersion spreads sites to "
            "reduce regional risk. A tabletop exercise is a discussion-based drill to test plans, not a "
            "staffing analysis step."
        ),
        "choices": [
            "Capacity planning",
            "Redundancy",
            "Geographic dispersion",
            "Tabletop exercise",
        ],
        "objectives": ["3.4", "5.1"],
    },
    {
        "slug": "reissue-laptop-retention-sanitization",
        "title": "Security+ — Reissue laptop (choose two)",
        "stem": (
            "A security administrator is reissuing a former employee's laptop. Which of the following is the "
            "best combination of data handling activities for the administrator to perform? (Select two.)"
        ),
        "name": "secplus_q162",
        "choose_two": True,
        "correct": ["A", "E"],
        "explain": (
            "Correct. A and E — Data retention ensures business or legal records are preserved or handled per "
            "policy before the device is wiped. Sanitization securely removes the former employee's data so "
            "the laptop can be reissued safely. Certification attests to compliance but does not perform "
            "device data handling. Tokenization protects data in systems, not end-of-life media on a laptop. "
            "Classification labels sensitivity but reissue centers on retention obligations and secure wipe. "
            "Enumeration inventories assets rather than clearing user data."
        ),
        "choices": [
            "Data retention",
            "Certification",
            "Tokenization",
            "Classification",
            "Sanitization",
            "Enumeration",
        ],
        "objectives": ["4.2", "3.3"],
    },
    {
        "slug": "team-folder-access-role-based-group",
        "title": "Security+ — RBAC (team folder access)",
        "stem": (
            "An engineer moved to another team and is unable to access the new team's shared folders while "
            "still being able to access the shared folders from the former team. After opening a ticket, the "
            "engineer discovers that the account was never moved to the new group. Which of the following "
            "access controls is most likely causing the lack of access?"
        ),
        "name": "secplus_q163",
        "correct": "A",
        "explain": (
            "Correct. A — Role-based access control grants permissions through group or role membership; "
            "without assignment to the new team group, shared folder access is denied. Discretionary access "
            "lets owners assign permissions individually rather than through mandatory group roles. Time-of-day "
            "restrictions limit access by schedule. Least privilege is a principle to limit rights but the "
            "direct cause here is missing role assignment, not minimum necessary access alone."
        ),
        "choices": [
            "Role-based",
            "Discretionary",
            "Time of day",
            "Least privilege",
        ],
        "objectives": ["4.5", "1.2"],
    },
    {
        "slug": "harden-end-user-devices-fde-epp",
        "title": "Security+ — Endpoint hardening (choose two)",
        "stem": (
            "Which of the following are the best for hardening end-user devices? (Select two.)"
        ),
        "name": "secplus_q164",
        "choose_two": True,
        "correct": ["A", "D"],
        "explain": (
            "Correct. A and D — Full disk encryption protects data at rest if a device is lost or stolen. "
            "Endpoint protection provides anti-malware, host firewall, and EDR capabilities on the device. "
            "Group-level permissions and account lockout support access control but are not the primary pair "
            "cited for device hardening in exam objectives. A proxy server filters web traffic at the network. "
            "Segmentation separates network segments rather than hardening a single endpoint."
        ),
        "choices": [
            "Full disk encryption",
            "Group-level permissions",
            "Account lockout",
            "Endpoint protection",
            "Proxy server",
            "Segmentation",
        ],
        "objectives": ["2.5", "4.1"],
    },
    {
        "slug": "phishing-link-malware-awareness-training",
        "title": "Security+ — Awareness training (phishing malware)",
        "stem": (
            "An employee clicked a malicious link in an email and downloaded malware onto the company's "
            "computer network. The malicious program exfiltrated thousands of customer records. Which of the "
            "following should the company implement to prevent this in the future?"
        ),
        "name": "secplus_q165",
        "correct": "A",
        "explain": (
            "Correct. A — Security awareness training reduces successful phishing clicks that start malware "
            "infections and later data theft. Network monitoring detects activity after it occurs. Endpoint "
            "protection can block malware execution but does not stop the social engineering click. Data loss "
            "prevention limits exfiltration but does not prevent the initial compromise from a malicious email."
        ),
        "choices": [
            "User awareness training",
            "Network monitoring",
            "Endpoint protection",
            "Data loss prevention",
        ],
        "objectives": ["5.1", "2.2"],
    },
    {
        "slug": "payroll-insider-manipulation-detective-control",
        "title": "Security+ — Detective control (payroll insider)",
        "stem": (
            "Which of the following security controls would best guard a payroll system against insider "
            "manipulation threats?"
        ),
        "name": "secplus_q166",
        "correct": "C",
        "explain": (
            "Correct. C — Detective controls such as audit logs, reconciliations, and exception reporting "
            "identify unauthorized payroll changes after they occur. Compensating controls substitute when a "
            "primary control cannot be used. Deterrent controls discourage misconduct but do not verify "
            "transactions. Corrective controls restore systems after an incident rather than guard against "
            "ongoing manipulation."
        ),
        "choices": [
            "Compensating",
            "Deterrent",
            "Detective",
            "Corrective",
        ],
        "objectives": ["1.1", "5.4"],
    },
    {
        "slug": "block-unknown-programs-application-allow-list",
        "title": "Security+ — Application allow list",
        "stem": "Which of the following would be the best way to block unknown programs from executing?",
        "name": "secplus_q167",
        "correct": "B",
        "explain": (
            "Correct. B — An application allow list permits only approved executables to run, blocking unknown "
            "or unapproved programs. An access control list filters network traffic by rule. A host-based "
            "firewall controls network connections, not which applications may launch. A DLP solution "
            "monitors and blocks sensitive data movement, not unauthorized program execution."
        ),
        "choices": [
            "Access control list",
            "Application allow list.",
            "Host-based firewall",
            "DLP solution",
        ],
        "objectives": ["2.5", "4.1"],
    },
    {
        "slug": "on-premises-access-swipe-biometric",
        "title": "Security+ — On-prem access (choose two)",
        "stem": (
            "Which of the following are the best security controls for controlling on-premises access? "
            "(Select two.)"
        ),
        "name": "secplus_q168",
        "choose_two": True,
        "correct": ["A", "D"],
        "explain": (
            "Correct. A and D — Swipe cards (badge readers) and biometric scanners are physical access "
            "controls that restrict who may enter a facility. Picture ID supports identity verification but is not "
            "an automated access control mechanism by itself. Phone authentication apps are typically used for "
            "logical MFA rather than primary door control. Cameras support monitoring and deterrence. A "
            "memorable password is unrelated to physical entry control."
        ),
        "choices": [
            "Swipe card",
            "Picture ID",
            "Phone authentication application",
            "Biometric scanner",
            "Camera",
            "Memorable",
        ],
        "objectives": ["1.1", "4.5"],
    },
    {
        "slug": "tcp-445-high-traffic-worm-root-cause",
        "title": "Security+ — Worm (TCP 445 SMB flood)",
        "stem": (
            "A security team receives reports about high latency and complete network unavailability "
            "throughout most of the office building. Flow logs from the campus switches show high traffic on "
            "TCP 445. Which of the following is most likely the root cause of this incident?"
        ),
        "name": "secplus_q169",
        "correct": "C",
        "explain": (
            "Correct. C — Worms such as those spreading via SMB exploit TCP port 445 and generate heavy "
            "scanning and replication traffic that can saturate the network. A buffer overflow is a host memory "
            "flaw, not campus-wide SMB floods. NTP amplification uses UDP, not TCP 445. Kerberoasting targets "
            "Kerberos service accounts and does not produce mass SMB port traffic."
        ),
        "choices": [
            "Buffer overflow",
            "NTP amplification attack",
            "Worm",
            "Kerberoasting attack",
        ],
        "objectives": ["2.3", "2.4"],
    },
    {
        "slug": "cmd-exe-fim-hash-change-rootkit",
        "title": "Security+ — Rootkit (cmd.exe FIM alert)",
        "stem": (
            "A systems administrator receives the following alert from a file integrity monitoring tool: "
            "The hash of the cmd.exe file has changed. The systems administrator checks the OS logs and "
            "notices that no patches were applied in the last two months. Which of the following most likely "
            "occurred?"
        ),
        "name": "secplus_q170",
        "correct": "D",
        "explain": (
            "Correct. D — Without a legitimate patch or update, a changed hash on a core binary such as cmd.exe "
            "suggests unauthorized modification, which rootkits often perform to hide or persist on the system. "
            "Changing file permissions does not alter the file hash. A cryptographic collision is exceedingly "
            "unlikely in this operational context. Taking a filesystem snapshot does not change on-disk file "
            "content or its hash."
        ),
        "choices": [
            "The end user changed the file permissions.",
            "A cryptographic collision was detected.",
            "A snapshot of the file system was taken.",
            "A rootkit was deployed.",
        ],
        "objectives": ["2.3", "4.4"],
    },
    {
        "slug": "incident-cost-sle-risk-quantification",
        "title": "Security+ — SLE (risk quantification)",
        "stem": (
            "A security analyst estimates that a small security incident will cost $10,000 and will occur twice "
            "per year. The analyst recommends a budget of $20,000 for next year. Which of the following does the "
            "$10,000 represent?"
        ),
        "name": "secplus_q171",
        "correct": "B",
        "explain": (
            "Correct. B — Single loss expectancy (SLE) is the monetary impact of one occurrence of the risk "
            "($10,000). Annualized rate of occurrence (ARO) is how often it happens per year (2). Annualized loss "
            "expectancy (ALE) is SLE × ARO ($20,000), which matches the recommended budget. Recovery point "
            "objective (RPO) is a continuity metric for acceptable data loss, not per-incident cost."
        ),
        "choices": [
            "ARO",
            "SLE",
            "ALE",
            "RPO",
        ],
        "objectives": ["1.2", "5.5"],
    },
    {
        "slug": "container-image-hardening-production",
        "title": "Security+ — Container image hardening (choose two)",
        "stem": (
            "Which of the following hardening techniques must be applied on a container image before "
            "deploying it to a production environment? (Select two)."
        ),
        "name": "secplus_q172",
        "choose_two": True,
        "correct": ["A", "C"],
        "explain": (
            "Correct. A and C — Hardened container images minimize attack surface by removing unnecessary "
            "default applications and disabling insecure services such as Telnet. A NIPS is network "
            "infrastructure, not baked into an image. DNS reconfiguration is environment-specific, not a "
            "standard image baseline step. Adding an SFTP server increases exposure. Deleting public "
            "certificates would break trusted TLS, not harden the image."
        ),
        "choices": [
            "Remove default applications.",
            "Install a NIPS.",
            "Disable Telnet.",
            "Reconfigure the DNS",
            "Add an SFTP server.",
            "Delete the public certificate.",
        ],
        "objectives": ["2.5", "4.5"],
    },
    {
        "slug": "windows-4625-bruteforce-admin-log",
        "title": "Security+ — Brute-force (Event 4625 log)",
        "stem": "",
        "name": "secplus_q173",
        "correct": "A",
        "explain": (
            "Correct. A — Repeated Event ID 4625 failures against the Administrator account in seconds, "
            "with sub status 0xC000006A (valid username, wrong password), match automated password guessing "
            "(brute-force). Privilege escalation follows successful compromise, not a string of failed "
            "logons. A failed password audit is a compliance review activity, not this attack pattern. A "
            "forgotten password might cause a few failures, not rapid automated attempts from a remote address."
        ),
        "choices": [
            "Brute-force attack",
            "Privilege escalation",
            "Failed password audit",
            "Forgotten password by the user",
        ],
        "prepend_html": build_windows_4625_bruteforce_exhibit(),
        "objectives": ["2.4", "4.9"],
    },
    {
        "slug": "supply-chain-servers-acquisition-process",
        "title": "Security+ — Supply chain (acquisition process)",
        "stem": (
            "A company is concerned with supply chain compromise of new servers and wants to limit this risk. "
            "Which of the following should the company review first?"
        ),
        "name": "secplus_q174",
        "correct": "B",
        "explain": (
            "Correct. B — Supply chain risk for new hardware is addressed first in how systems are procured: "
            "trusted vendors, authorized channels, inspection, and contractual security requirements before "
            "deployment. Sanitization applies when retiring or reusing equipment. Change management governs "
            "post-deployment modifications. Asset tracking inventories assets after they are in the environment "
            "but does not prevent compromised hardware from entering during purchase."
        ),
        "choices": [
            "Sanitization procedure",
            "Acquisition process",
            "Change management",
            "Asset tracking",
        ],
        "objectives": ["5.1", "5.5"],
    },
    {
        "slug": "inadvertent-malware-application-allow-list",
        "title": "Security+ — Inadvertent malware (allow list)",
        "stem": (
            "Which of the following can best protect against an employee inadvertently installing malware on a "
            "company system?"
        ),
        "name": "secplus_q175",
        "correct": "D",
        "explain": (
            "Correct. D — An application allow list blocks any executable that is not explicitly approved, so "
            "accidental downloads or installs cannot run even if the user clicks them. A host-based firewall "
            "filters network traffic, not which programs may launch. System isolation limits spread after "
            "compromise but does not stop the initial unauthorized install. Least privilege restricts rights "
            "but many malware payloads still run under a standard user account."
        ),
        "choices": [
            "Host-based firewall",
            "System isolation",
            "Least privilege",
            "Application allow list",
        ],
        "objectives": ["2.5", "4.1"],
    },
    {
        "slug": "sdlc-policy-peer-review-requirements",
        "title": "Security+ — SDLC policy (peer review)",
        "stem": (
            "A Chief Information Security Officer (CISO) has developed information security policies that "
            "relate to the software development methodology. Which of the following would the CISO most likely "
            "include in the organization's documentation?"
        ),
        "name": "secplus_q176",
        "correct": "A",
        "explain": (
            "Correct. A — SDLC policies document process requirements such as mandatory peer code review before "
            "release. Multifactor authentication is an access control, not a development-methodology policy item. "
            "Branch protection rules are version-control operational settings, not typical policy prose. Secrets "
            "management configurations are technical implementation details; policies reference secure handling of "
            "secrets but not vault or pipeline config values."
        ),
        "choices": [
            "Peer review requirements",
            "Multifactor authentication",
            "Branch protection tests",
            "Secrets management configurations",
        ],
        "objectives": ["5.1", "5.5"],
    },
    {
        "slug": "data-sovereignty-global-regulations",
        "title": "Security+ — Data sovereignty (global regulations)",
        "stem": (
            "Which of the following explains how to determine the global regulations that data is subject to "
            "regardless of the country where the data is stored?"
        ),
        "name": "secplus_q177",
        "correct": "B",
        "explain": (
            "Correct. B — Data sovereignty is the principle that data remains governed by the laws of the "
            "jurisdiction where it originated or where the data subject resides, even when stored elsewhere "
            "(for example, GDPR for EU subjects). Geographic dispersion spreads data across sites for "
            "availability. Geographic restrictions limit where data may be stored or accessed. Data "
            "segmentation divides datasets for security or isolation, not legal jurisdiction."
        ),
        "choices": [
            "Geographic dispersion",
            "Data sovereignty",
            "Geographic restrictions",
            "Data segmentation",
        ],
        "objectives": ["5.1", "5.6"],
    },
    {
        "slug": "research-laws-regulations-due-diligence",
        "title": "Security+ — Due diligence (legal research)",
        "stem": (
            "Which of the following best describes the practice of researching laws and regulations related to "
            "information security operations within a specific industry?"
        ),
        "name": "secplus_q178",
        "correct": "C",
        "explain": (
            "Correct. C — Due diligence is the investigation process of identifying applicable laws, regulations, "
            "and industry requirements before operations or partnerships proceed. Compliance reporting documents "
            "adherence after controls are in place. GDPR is one specific privacy regulation, not the general "
            "practice of legal research. Attestation is a formal statement or certification that requirements "
            "are met, not the upfront research itself."
        ),
        "choices": [
            "Compliance reporting",
            "GDPR",
            "Due diligence",
            "Attestation",
        ],
        "objectives": ["5.6", "5.5"],
    },
    {
        "slug": "incident-frequency-aro-definition",
        "title": "Security+ — ARO (incident frequency)",
        "stem": (
            "Which of the following best represents how frequently an incident is expected to happen each year?"
        ),
        "name": "secplus_q179",
        "correct": "D",
        "explain": (
            "Correct. D — Annualized rate of occurrence (ARO) is the expected number of times a risk event "
            "happens per year. Recovery time objective (RTO) is maximum acceptable downtime after an outage. "
            "Single loss expectancy (SLE) is the cost of one occurrence. Annualized loss expectancy (ALE) is "
            "SLE × ARO, the expected annual monetary loss."
        ),
        "choices": [
            "RTO",
            "ALE",
            "SLE",
            "ARO",
        ],
        "objectives": ["1.2", "5.5"],
    },
    {
        "slug": "insider-records-permission-restrictions",
        "title": "Security+ — Insider records (permission restrictions)",
        "stem": (
            "A malicious insider from the marketing team alters records and transfers company funds to a personal "
            "account. Which of the following methods would be the best way to secure company records in the future?"
        ),
        "name": "secplus_q180",
        "correct": "A",
        "explain": (
            "Correct. A — Permission restrictions enforce least privilege so marketing staff cannot modify financial "
            "records or initiate transfers they do not need for their role. Hashing can support integrity checking "
            "but does not by itself stop an authorized writer from changing data. Input validation blocks malformed "
            "or malicious input, not insider abuse of legitimate access. An access control list typically filters "
            "network traffic rather than granular record-level rights on sensitive data."
        ),
        "choices": [
            "Permission restrictions",
            "Hashing",
            "Input validation",
            "Access control list",
        ],
        "objectives": ["1.1", "4.6"],
    },
    {
        "slug": "power-failure-resiliency-production-failover",
        "title": "Security+ — Power resiliency (production failover)",
        "stem": (
            "Which of the following would be the best way to test resiliency in the event of a primary power failure?"
        ),
        "name": "secplus_q181",
        "correct": "D",
        "explain": (
            "Correct. D — Production failover verifies that redundant power and backup systems (UPS, generator, "
            "alternate site) actually take over when primary power fails. A tabletop exercise is discussion-only "
            "and does not prove technical failover. Simulation testing practices scenarios in controlled "
            "conditions but is not the best proof of power-path resiliency. Parallel processing spreads compute "
            "load across processors; it is not a power-failure test method."
        ),
        "choices": [
            "Parallel processing",
            "Tabletop exercise",
            "Simulation testing",
            "Production failover",
        ],
        "objectives": ["3.4", "5.4"],
    },
    {
        "slug": "fingerprinted-files-email-dlp",
        "title": "Security+ — DLP (fingerprinted files)",
        "stem": (
            "An administrator has identified and fingerprinted specific files that will generate an alert if an "
            "attempt is made to email these files outside of the organization. Which of the following best describes "
            "the tool the administrator is using?"
        ),
        "name": "secplus_q182",
        "correct": "A",
        "explain": (
            "Correct. A — Data loss prevention (DLP) fingerprints sensitive content and monitors channels such as "
            "email to alert or block unauthorized exfiltration. SNMP traps report network device events. SCAP "
            "provides standardized formats for vulnerability and configuration assessment. An intrusion prevention "
            "system blocks malicious traffic patterns, not outbound email of classified files."
        ),
        "choices": [
            "DLP",
            "SNMP traps",
            "SCAP",
            "IPS",
        ],
        "objectives": ["4.5", "3.3"],
    },
    {
        "slug": "resigned-batch-jobs-job-rotation",
        "title": "Security+ — Job rotation (batch jobs)",
        "stem": (
            "An employee recently resigned from a company. The employee was responsible for managing and "
            "supporting weekly batch jobs over the past five years. A few weeks after the employee resigned, one "
            "of the batch jobs failed and caused a major disruption. Which of the following would work best to "
            "prevent this type of incident from reoccurring?"
        ),
        "name": "secplus_q183",
        "correct": "A",
        "explain": (
            "Correct. A — Job rotation cross-trains multiple staff on critical batch processes so knowledge and "
            "support are not lost when one person leaves. Retention focuses on keeping employees, not eliminating "
            "single points of expertise. Outsourcing shifts work to a vendor but does not by itself ensure "
            "internal redundancy. Separation of duties splits conflicting tasks to reduce fraud; it is not the "
            "primary control for operational knowledge silos after resignation."
        ),
        "choices": [
            "Job rotation",
            "Retention",
            "Outsourcing",
            "Separation of duties",
        ],
        "objectives": ["5.4", "1.1"],
    },
    {
        "slug": "tabletop-exercise-ir-familiarization",
        "title": "Security+ — Tabletop (IR familiarization)",
        "stem": (
            "Which of the following objectives is best achieved by a tabletop exercise?"
        ),
        "name": "secplus_q184",
        "correct": "A",
        "explain": (
            "Correct. A — Tabletop exercises are discussion-based drills where participants walk through "
            "incident response scenarios to learn roles, procedures, and coordination without disrupting live "
            "systems. Rules of engagement are set for red/blue team tests, not tabletops. Determining impact "
            "of an actual breach is live incident response. Parallel investigations are operational workload, "
            "not the purpose of a tabletop."
        ),
        "choices": [
            "Familiarizing participants with the incident response process",
            "Deciding red and blue team rules of engagement",
            "Quickly determining the impact of an actual security breach",
            "Conducting multiple security investigations in parallel",
        ],
        "objectives": ["5.4", "4.8"],
    },
    {
        "slug": "counterfeit-hardware-supply-chain-analysis",
        "title": "Security+ — Counterfeit hardware (supply chain)",
        "stem": (
            "A company is required to use certified hardware when building networks. Which of the following "
            "best addresses the risks associated with procuring counterfeit hardware?"
        ),
        "name": "secplus_q185",
        "correct": "A",
        "explain": (
            "Correct. A — A thorough supply chain analysis verifies origin, authenticity, and integrity across "
            "OEMs, resellers, shipping, and delivery before hardware is deployed. An acquisition policy alone "
            "does not verify components. A right to audit clause supports vendor oversight but is not the "
            "comprehensive counterfeit-risk practice the question emphasizes. Penetration testing suppliers "
            "targets exploitable weaknesses, not hardware authenticity in the procurement chain."
        ),
        "choices": [
            "A thorough analysis of the supply chain",
            "A legally enforceable corporate acquisition policy",
            "A right to audit clause in vendor contracts and SOWs",
            "An in-depth penetration test of all suppliers and vendors",
        ],
        "objectives": ["5.1", "5.5"],
    },
    {
        "slug": "zero-trust-validate-traffic-between-systems",
        "title": "Security+ — Zero Trust (validate traffic)",
        "stem": (
            "Which of the following security principles most likely requires validation before allowing traffic "
            "between systems?"
        ),
        "name": "secplus_q186",
        "correct": "C",
        "explain": (
            "Correct. C — Zero Trust requires explicit verification of identity, device health, and policy for "
            "every connection; no implicit trust based on network location. Policy enforcement applies rules "
            "but is not the overarching principle described. Authentication verifies identity but is only one "
            "part of Zero Trust validation. Confidentiality protects data from unauthorized disclosure and does "
            "not define pre-traffic verification between systems."
        ),
        "choices": [
            "Policy enforcement",
            "Authentication",
            "Zero Trust architecture",
            "Confidentiality",
        ],
        "objectives": ["3.2", "1.2"],
    },
    {
        "slug": "school-arp-poisoning-unskilled-attacker",
        "title": "Security+ — ARP poisoning (unskilled attacker)",
        "stem": (
            "While a school district is performing state testing, a security analyst notices all internet services "
            "are unavailable. The analyst discovers that ARP poisoning is occurring on the network and then "
            "terminates access for the host. Which of the following is most likely responsible for this malicious "
            "activity?"
        ),
        "name": "secplus_q187",
        "correct": "A",
        "explain": (
            "Correct. A — ARP poisoning is a basic on-path technique often run with free tools and fits an "
            "unskilled attacker (script kiddie) disrupting a school network during testing. Shadow IT is "
            "unsanctioned services or devices, not LAN ARP spoofing. Credential stuffing reuses stolen passwords "
            "against logins and does not poison ARP tables. DMARC failures concern email authentication, not "
            "Layer 2 redirection on the LAN."
        ),
        "choices": [
            "Unskilled attacker",
            "Shadow IT",
            "Credential stuffing",
            "DMARC failure",
        ],
        "objectives": ["2.1", "2.4"],
    },
    {
        "slug": "phishing-lateral-ransomware-ips-spread",
        "title": "Security+ — IPS (ransomware spread)",
        "stem": (
            "A hacker gained access to a system via a phishing attempt that was a direct result of a user clicking "
            "a suspicious link. The link laterally deployed ransomware, which laid dormant for multiple weeks, across "
            "the network. Which of the following would have mitigated the spread?"
        ),
        "name": "secplus_q188",
        "correct": "A",
        "explain": (
            "Correct. A — An intrusion prevention system (IPS) operates inline and can block malicious traffic "
            "patterns associated with lateral movement, command-and-control, and ransomware propagation. An IDS "
            "detects and alerts but does not stop spread by itself. A WAF protects web applications from HTTP-layer "
            "attacks, not general network ransomware movement. UAT is software acceptance testing, not a security "
            "control."
        ),
        "choices": [
            "IPS",
            "IDS",
            "WAF",
            "UAT",
        ],
        "objectives": ["4.5", "2.4"],
    },
    {
        "slug": "aggregate-logs-alerts-siem",
        "title": "Security+ — SIEM (log aggregation)",
        "stem": (
            "Which of the following should be used to aggregate log data in order to create alerts and detect "
            "anomalous activity?"
        ),
        "name": "secplus_q189",
        "correct": "A",
        "explain": (
            "Correct. A — A security information and event management (SIEM) platform collects logs from many "
            "sources, correlates events, generates alerts, and supports anomaly detection. A WAF protects web "
            "applications at the HTTP layer. Network taps copy traffic for analysis but do not aggregate logs "
            "or drive enterprise alerting by themselves. An IDS detects suspicious network activity on monitored "
            "segments but is not the primary enterprise log aggregation and correlation tool."
        ),
        "choices": [
            "SIEM",
            "WAF",
            "Network taps",
            "IDS",
        ],
        "objectives": ["4.4", "4.9"],
    },
    {
        "slug": "insurance-policy-risk-transfer",
        "title": "Security+ — Risk transfer (insurance)",
        "stem": (
            "A company decides to purchase an insurance policy. Which of the following risk management "
            "strategies is this company implementing?"
        ),
        "name": "secplus_q190",
        "correct": "D",
        "explain": (
            "Correct. D — Transfer shifts financial impact of a risk to a third party; cyber or liability "
            "insurance is a classic transfer control. Mitigate reduces likelihood or impact with technical or "
            "procedural controls. Accept acknowledges residual risk without further action. Avoid eliminates "
            "the risk by not performing the activity that creates it."
        ),
        "choices": [
            "Mitigate",
            "Accept",
            "Avoid",
            "Transfer",
        ],
        "objectives": ["1.2", "5.5"],
    },
    {
        "slug": "wpa2-enterprise-radius-8021x-directory",
        "title": "Security+ — WPA2-Enterprise (802.1X + RADIUS)",
        "stem": (
            "Following a security review, an organization must ensure users verify their identities against the "
            "company's identity services with individual credentials leveraging WPA2-Enterprise for wireless access. "
            "Which of the following configuration steps correctly applies RADIUS in this environment?"
        ),
        "name": "secplus_q191",
        "correct": "A",
        "explain": (
            "Correct. A — WPA2-Enterprise uses 802.1X port-based access control; the wireless infrastructure "
            "forwards authentication to RADIUS, which validates individual credentials against the corporate "
            "directory. Self-signed certificates on every device are not the standard directory-backed user "
            "model described. MAC filtering uses hardware addresses, not per-user identity services. Requiring "
            "MFA on the controller alone does not replace 802.1X plus RADIUS integration with identity services."
        ),
        "choices": [
            "Enabling 802.1X authentication and integrating it with the corporate directory",
            "Installing self-signed certificates on all user devices",
            "Enabling MAC filters for all wireless clients",
            "Configuring the wireless controller to require multifactor authentication",
        ],
        "objectives": ["4.6", "3.5"],
    },
    {
        "slug": "data-sovereignty-at-rest-cross-border",
        "title": "Security+ — Data sovereignty (at rest abroad)",
        "stem": (
            "Which of the following data types relates to data sovereignty?"
        ),
        "name": "secplus_q192",
        "correct": "D",
        "explain": (
            "Correct. D — Data sovereignty concerns legal jurisdiction when data is stored or processed "
            "outside its country of origin while still subject to that nation's laws (for example, EU data in a "
            "U.S. cloud region). Public classification in other countries is a labeling issue, not sovereignty. "
            "PII while traveling focuses on mobile users, not cross-border storage law. Health data shared "
            "between doctors abroad is a specific sector transfer scenario, not the general sovereignty data type."
        ),
        "choices": [
            "Data classified as public in other countries",
            "Personally Identifiable data while traveling",
            "Health data shared between doctors in other nations",
            "Data at rest outside of a country's borders",
        ],
        "objectives": ["5.1", "5.6"],
    },
    {
        "slug": "sdlc-penetration-testing-methodology",
        "title": "Security+ — SDLC (pentest methodology)",
        "stem": (
            "Which of the following topics would most likely be included within an organization's SDLC?"
        ),
        "name": "secplus_q193",
        "correct": "C",
        "explain": (
            "Correct. C — The SDLC includes security testing phases; penetration testing methodology defines "
            "how applications are assessed before release. Information security policy is broader organizational "
            "governance that guides the SDLC but is not a topic inside the development lifecycle itself. "
            "Service-level agreements define service metrics with providers, not software build phases. Branch "
            "protection is a version-control setting, not a core SDLC topic on the exam."
        ),
        "choices": [
            "Service-level agreements",
            "Information security policy",
            "Penetration testing methodology",
            "Branch protection requirements",
        ],
        "objectives": ["5.1", "5.5"],
    },
    {
        "slug": "industry-blog-watering-hole-malware",
        "title": "Security+ — Watering hole (industry blog)",
        "stem": (
            "Malware spread across a company's network after an employee visited a compromised industry blog. "
            "Which of the following best describes this type of attack?"
        ),
        "name": "secplus_q194",
        "correct": "C",
        "explain": (
            "Correct. C — A watering-hole attack infects a site that a targeted audience is likely to visit; "
            "when employees browse the compromised blog, malware can spread into the network. Impersonation "
            "pretends to be a trusted person or system. Disinformation spreads false narratives. Smishing uses "
            "fraudulent SMS messages, not a poisoned website."
        ),
        "choices": [
            "Impersonation",
            "Disinformation",
            "Watering-hole",
            "Smishing",
        ],
        "objectives": ["2.2", "2.4"],
    },
    {
        "slug": "honeypot-analyze-attacker-techniques",
        "title": "Security+ — Honeypot (attacker analysis)",
        "stem": (
            "Which of the following would most likely be deployed to obtain and analyze attacker activity and "
            "techniques?"
        ),
        "name": "secplus_q195",
        "correct": "C",
        "explain": (
            "Correct. C — A honeypot is a decoy system designed to attract attackers so defenders can observe "
            "and study their tools, tactics, and procedures. A firewall filters traffic by policy. An IDS detects "
            "suspicious activity but is not primarily a lure for detailed attacker behavior analysis. A Layer 3 "
            "switch routes traffic between networks and does not capture attacker techniques."
        ),
        "choices": [
            "Firewall",
            "IDS",
            "Honeypot",
            "Layer 3 switch",
        ],
        "objectives": ["4.5", "2.4"],
    },
    {
        "slug": "pentest-partially-known-environment-device",
        "title": "Security+ — Pentest (partially known)",
        "stem": (
            "An organization wants a third-party vendor to do a penetration test that targets a specific device. "
            "The organization has provided basic information about the device. Which of the following best "
            "describes this kind of penetration test?"
        ),
        "name": "secplus_q196",
        "correct": "A",
        "explain": (
            "Correct. A — A partially known (gray-box) test gives the tester limited information such as basic "
            "device details but not full architecture or credentials for everything. An unknown (black-box) test "
            "provides no prior target information. A known (white-box) test supplies extensive documentation and "
            "access. Integrated is not a standard CompTIA label for pentest knowledge levels."
        ),
        "choices": [
            "Partially known environment",
            "Unknown environment",
            "Integrated",
            "Known environment",
        ],
        "objectives": ["5.3", "5.5"],
    },
    {
        "slug": "endpoint-management-unauthorized-changes",
        "title": "Security+ — Endpoint management (monitoring)",
        "stem": (
            "Which of the following actions could a security engineer take to ensure workstations and servers are "
            "properly monitored for unauthorized changes and software?"
        ),
        "name": "secplus_q197",
        "correct": "D",
        "explain": (
            "Correct. D — Endpoint management software inventories installed software, enforces configuration "
            "baselines, and alerts on unauthorized changes from a central console. Logging scheduled tasks alone "
            "covers only that persistence mechanism. Monitoring egress traffic focuses on network exfiltration, not "
            "local system integrity. Blocking known malicious signatures is IPS-style prevention, not comprehensive "
            "endpoint change and software monitoring."
        ),
        "choices": [
            "Configure all systems to log scheduled tasks.",
            "Collect and monitor all traffic exiting the network.",
            "Block traffic based on known malicious signatures.",
            "Install endpoint management software on all systems.",
        ],
        "objectives": ["4.6", "4.5"],
    },
    {
        "slug": "mfa-patch-preventative-technical-controls",
        "title": "Security+ — MFA/patch controls (choose two)",
        "stem": (
            "A security manager is implementing MFA and patch management. Which of the following would best "
            "describe the control type and category? (Select two.)"
        ),
        "name": "secplus_q198",
        "choose_two": True,
        "correct": ["E", "F"],
        "explain": (
            "Correct. E and F — MFA and patch management are technical controls enforced through systems and "
            "software. Both are preventative: MFA blocks unauthorized access before it succeeds, and patching "
            "closes vulnerabilities before exploitation. Physical controls protect facilities. Managerial controls "
            "are policies and governance. Detective controls identify events after they occur. Administrator is "
            "not a standard control category on the exam."
        ),
        "choices": [
            "Physical",
            "Managerial",
            "Detective",
            "Administrator",
            "Preventative",
            "Technical",
        ],
        "objectives": ["1.2", "4.6"],
    },
    {
        "slug": "consultant-remote-access-ipsec",
        "title": "Security+ — IPSec (consultant remote access)",
        "stem": (
            "A security consultant needs secure, remote access to a client environment. Which of the following "
            "should the security consultant most likely use to gain access?"
        ),
        "name": "secplus_q199",
        "correct": "C",
        "explain": (
            "Correct. C — IPSec VPNs provide encrypted, authenticated remote access into a client network. EAP "
            "authenticates users on wired or wireless links but is not the remote-access tunnel itself. DHCP "
            "assigns IP addresses. NAT translates addresses between networks and does not by itself deliver "
            "secure consultant connectivity."
        ),
        "choices": [
            "EAP",
            "DHCP",
            "IPSec",
            "NAT",
        ],
        "objectives": ["3.5", "4.6"],
    },
    {
        "slug": "banned-vendor-hardware-refresh-sanctions",
        "title": "Security+ — Sanctions (banned vendor)",
        "stem": (
            "A company receives an alert that a network device vendor, which is widely used in the enterprise, "
            "has been banned by the government. Which of the following will the company's general counsel most "
            "likely be concerned with during a hardware refresh of these devices?"
        ),
        "name": "secplus_q200",
        "correct": "A",
        "explain": (
            "Correct. A — When a vendor is government-banned, general counsel focuses on sanctions and legal "
            "compliance: avoiding purchase, use, or refresh of prohibited equipment. Data sovereignty concerns "
            "where data is stored and which laws apply. Replacement cost is operational and financial. Loss of "
            "license is a software licensing issue, not the primary legal risk of a sanctioned vendor."
        ),
        "choices": [
            "Sanctions",
            "Data sovereignty",
            "Cost of replacement",
            "Loss of license",
        ],
        "objectives": ["5.6", "5.3"],
    },
    {
        "slug": "cloud-iot-management-encrypted-connection",
        "title": "Security+ — IoT cloud (encrypted connection)",
        "stem": (
            "Which of the following security measures is required when using a cloud-based platform for IoT "
            "management?"
        ),
        "name": "secplus_q201",
        "correct": "A",
        "explain": (
            "Correct. A — IoT management traffic crosses untrusted networks to the cloud; encrypted connections "
            "(for example TLS) protect data in transit from eavesdropping and tampering. Federated identity and "
            "single sign-on improve authentication convenience but do not by themselves secure transmission. A "
            "firewall filters traffic but does not replace encryption for device-to-cloud communications."
        ),
        "choices": [
            "Encrypted connection",
            "Federated identity",
            "Firewall",
            "Single sign-on",
        ],
        "objectives": ["3.4", "4.5"],
    },
    {
        "slug": "vpn-login-impossible-travel-indicator",
        "title": "Security+ — Impossible travel (VPN logs)",
        "stem": "",
        "name": "secplus_q202",
        "correct": "A",
        "explain": (
            "Correct. A — Impossible travel flags logins from distant locations faster than the user could "
            "physically travel (Chicago, then Rome, then Chicago again in minutes). Account lockout follows "
            "repeated failed authentication. Blocked content is a web-filter indicator. Concurrent session "
            "usage is the same account active from two places at the same time, not rapid sequential "
            "geographic hops."
        ),
        "choices": [
            "Impossible travel",
            "Account lockout",
            "Blocked content",
            "Concurrent session usage",
        ],
        "prepend_html": build_vpn_impossible_travel_log_exhibit(),
        "objectives": ["4.9", "2.4"],
    },
    {
        "slug": "ips-active-mode-signature-blocking",
        "title": "Security+ — IPS (active mode)",
        "stem": (
            "A security engineer is installing an IPS to block signature-based attacks in the environment. "
            "Which of the following modes will best accomplish this task?"
        ),
        "name": "secplus_q203",
        "correct": "D",
        "explain": (
            "Correct. D — Active (inline) mode lets the IPS drop or reset traffic that matches attack "
            "signatures in real time. Monitor and sensor modes are typically passive observation without "
            "blocking. Audit mode logs activity for review and does not stop malicious packets on the wire."
        ),
        "choices": [
            "Monitor",
            "Sensor",
            "Audit",
            "Active",
        ],
        "objectives": ["4.5", "2.4"],
    },
    {
        "slug": "c2-exfiltration-packet-capture-forensics",
        "title": "Security+ — Packet capture (C2 exfiltration)",
        "stem": (
            "During an investigation, a security analyst discovers traffic going out to a command-and-control "
            "server. The analyst must find out if any data exfiltration has occurred. Which of the following "
            "would best help the analyst determine this?"
        ),
        "name": "secplus_q204",
        "correct": "D",
        "explain": (
            "Correct. D — Packet capture (PCAP) records full network traffic so analysts can inspect payloads, "
            "session size, and content to confirm whether data left the environment over the C2 channel. "
            "Application logs show app events but not complete transmitted data. Metadata summarizes flows "
            "without payload contents. Network logs document connections but lack the depth to verify "
            "exfiltrated content."
        ),
        "choices": [
            "Application log",
            "Metadata",
            "Network log",
            "Packet capture",
        ],
        "objectives": ["4.9", "2.4"],
    },
    {
        "slug": "web-server-tls-public-key-certificate",
        "title": "Security+ — Public key (HTTPS/TLS)",
        "stem": (
            "Which of the following should be deployed on an externally facing web server in order to establish "
            "an encrypted connection?"
        ),
        "name": "secplus_q205",
        "correct": "A",
        "explain": (
            "Correct. A — HTTPS/TLS presents a server certificate containing the public key so clients can "
            "authenticate the site and negotiate an encrypted session. The matching private key must stay on "
            "the server and is never shared. Asymmetric key describes the key pair type, not the deployable "
            "artifact in the certificate. Symmetric keys are derived for the session after the handshake, "
            "not deployed as the server's long-term credential."
        ),
        "choices": [
            "Public key",
            "Private Key",
            "Asymmetric key",
            "Symmetric key",
        ],
        "objectives": ["1.4", "3.3"],
    },
    {
        "slug": "payment-site-email-phishing-credentials",
        "title": "Security+ — Phishing (fake payment site)",
        "stem": (
            "An employee clicked a link in an email from a payment website that asked the employee to update "
            "contact information. The employee entered the log-in information but received a \"page not found\" "
            "error message. Which of the following types of social engineering attacks occurred?"
        ),
        "name": "secplus_q206",
        "correct": "D",
        "explain": (
            "Correct. D — Phishing uses fraudulent email and a deceptive login page to harvest credentials. "
            "The page-not-found message often appears after the fake site has already captured the username "
            "and password. Brand impersonation may be part of the lure but phishing is the attack type for "
            "email plus credential theft. Pretexting is a fabricated scenario to manipulate someone; here the "
            "defining channel is a malicious email link. Typosquatting relies on look-alike domain typos, not "
            "a crafted message with a login form."
        ),
        "choices": [
            "Brand impersonation",
            "Pretexting",
            "Typosquatting",
            "Phishing",
        ],
        "objectives": ["2.2", "2.4"],
    },
    {
        "slug": "vm-escape-hypervisor-compromise-other-vms",
        "title": "Security+ — VM escape (hypervisor consequence)",
        "stem": (
            "Which of the following is a possible consequence of a VM escape?"
        ),
        "name": "secplus_q207",
        "correct": "B",
        "explain": (
            "Correct. B — VM escape breaks guest isolation so an attacker can reach the hypervisor or host "
            "and potentially compromise other virtual machines on the same platform. Malicious instructions "
            "in memory with elevated permissions describe privilege escalation, not the cross-VM boundary "
            "failure. Unencrypted data readable across separate environments aligns more with resource reuse "
            "or poor segmentation than escape itself. Installing unapproved software is application control "
            "policy, not a virtualization escape outcome."
        ),
        "choices": [
            "Malicious instructions can be inserted into memory and give the attacker elevated permissions.",
            "An attacker can access the hypervisor and compromise other VMs.",
            "Unencrypted data can be read by a user in a separate environment.",
            "Users can install software that is not on the manufacturer's approved list.",
        ],
        "objectives": ["3.1", "3.3"],
    },
    {
        "slug": "pentest-database-input-validation-sqli",
        "title": "Security+ — SQLi (database input validation)",
        "stem": (
            "A penetration testing report indicated that an organization should implement controls related to "
            "database input validation. Which of the following best identifies the type of vulnerability that "
            "was likely discovered during the test?"
        ),
        "name": "secplus_q208",
        "correct": "D",
        "explain": (
            "Correct. D — SQL injection exploits untrusted input sent to a database; parameterized queries "
            "and input validation are common mitigations. XSS injects script into web pages viewed by users. "
            "Command injection runs operating-system commands through an application. Buffer overflow writes "
            "past memory bounds and is not the vulnerability tied to database query sanitization."
        ),
        "choices": [
            "XSS",
            "Command injection",
            "Buffer overflow",
            "SQLi",
        ],
        "objectives": ["2.3", "2.5"],
    },
    {
        "slug": "cold-site-insufficient-capacity-planning",
        "title": "Security+ — Capacity planning (cold site)",
        "stem": (
            "An organization discovers that its cold site does not have enough storage and computers available. "
            "Which of the following was most likely the cause of this failure?"
        ),
        "name": "secplus_q209",
        "correct": "A",
        "explain": (
            "Correct. A — Capacity planning forecasts the systems, storage, and staffing required to meet "
            "recovery objectives; understocking a cold site is a capacity shortfall. Load balancing distributes "
            "production traffic across nodes, not DR site provisioning. Backups protect data copies but do not "
            "by themselves ensure enough hardware is staged at the recovery site. Platform diversity is using "
            "different technologies, not the root cause of insufficient computers and storage."
        ),
        "choices": [
            "Capacity planning",
            "Load balancing",
            "Backups",
            "Platform diversity",
        ],
        "objectives": ["3.4", "5.1"],
    },
    {
        "slug": "software-release-hashing-integrity",
        "title": "Security+ — Hashing (software release integrity)",
        "stem": (
            "Which of the following should be used to ensure that a new software release has not been modified "
            "before reaching the user?"
        ),
        "name": "secplus_q210",
        "correct": "C",
        "explain": (
            "Correct. C — Comparing a cryptographic hash of the downloaded release to a vendor-published digest "
            "verifies integrity so tampering is detected before installation. Tokenization substitutes sensitive "
            "data with non-sensitive tokens. Encryption protects confidentiality in transit or at rest but is not "
            "the usual integrity check users apply to a release file. Obfuscation hides code logic and does not "
            "prove the binary was unchanged in distribution."
        ),
        "choices": [
            "Tokenization",
            "Encryption",
            "Hashing",
            "Obfuscation",
        ],
        "objectives": ["1.4", "4.6"],
    },
    {
        "slug": "secure-baseline-establish-deploy-maintain",
        "title": "Security+ — Secure baseline lifecycle",
        "stem": (
            "Which of the following most accurately describes the order in which a security engineer should "
            "implement secure baselines?"
        ),
        "name": "secplus_q211",
        "correct": "C",
        "explain": (
            "Correct. C — Establish defines the minimum secure configuration standard, deploy rolls it out "
            "to systems, and maintain keeps baselines current through patching, drift monitoring, and updates. "
            "Deploying before a baseline exists has no approved standard to apply. Maintaining before deployment "
            "has nothing in production to sustain. Deploy-then-establish reverses definition and rollout."
        ),
        "choices": [
            "Deploy, maintain, establish",
            "Establish, maintain, deploy",
            "Establish, deploy, maintain",
            "Deploy, establish, maintain",
        ],
        "objectives": ["4.1", "4.6"],
    },
    {
        "slug": "hardware-repair-mean-time-to-repair",
        "title": "Security+ — MTTR (hardware repair time)",
        "stem": (
            "An organization would like to calculate the time needed to resolve a hardware issue with a server. "
            "Which of the following risk management processes describes this example?"
        ),
        "name": "secplus_q212",
        "correct": "D",
        "explain": (
            "Correct. D — Mean time to repair (MTTR) is the average time to diagnose, fix, and restore a failed "
            "component such as server hardware. Recovery point objective (RPO) is the maximum acceptable data "
            "loss window measured in time. Mean time between failures (MTBF) is average uptime between failures, "
            "a reliability metric. Recovery time objective (RTO) is the maximum acceptable downtime to restore "
            "business services after a disruption, not the average repair duration itself."
        ),
        "choices": [
            "Recovery point objective",
            "Mean time between failures",
            "Recovery time objective",
            "Mean time to repair",
        ],
        "objectives": ["5.1", "5.2"],
    },
    {
        "slug": "pentest-unknown-environment-external-attack",
        "title": "Security+ — Pentest (unknown / external attack)",
        "stem": (
            "Which of the following best describes a penetration test that resembles an actual external attack?"
        ),
        "name": "secplus_q213",
        "correct": "D",
        "explain": (
            "Correct. D — An unknown (black-box) test gives the tester no prior internal knowledge, closely "
            "mirroring how an external attacker probes from outside. A known (white-box) test provides extensive "
            "documentation and access. A partially known (gray-box) test supplies limited information such as a "
            "specific target scope. A bug bounty is a crowdsourced reward program for reported flaws, not a "
            "pentest knowledge-level classification."
        ),
        "choices": [
            "Known environment",
            "Partially known environment",
            "Bug bounty",
            "Unknown environment",
        ],
        "objectives": ["5.3", "5.5"],
    },
    {
        "slug": "ssl-certificate-not-trusted-root-ca",
        "title": "Security+ — Root certificate (SSL trust)",
        "stem": (
            "An administrator is installing an SSL certificate on a new system. During testing, errors indicate that "
            "the certificate is not trusted. The administrator has verified with the issuing CA and has validated the "
            "private key. Which of the following should the administrator check for next?"
        ),
        "name": "secplus_q214",
        "correct": "C",
        "explain": (
            "Correct. C — Clients must trust the chain to a root CA; missing the root or intermediate certificates "
            "in the local trust store commonly causes untrusted certificate errors even when the leaf cert and "
            "private key are valid. A wildcard certificate affects hostname coverage, not whether the chain is "
            "trusted. The CSR is used to obtain the certificate and is not the usual next check after install. "
            "The public key is embedded in the certificate; pairing was already validated with the private key."
        ),
        "choices": [
            "If the wildcard certificate is configured",
            "If the certificate signing request is valid",
            "If the root certificate is installed",
            "If the public key is configured",
        ],
        "objectives": ["1.4", "4.6"],
    },
    {
        "slug": "host-isolation-network-resource-inaccessible",
        "title": "Security+ — Host isolation",
        "stem": (
            "Which of the following should be used to ensure a device is inaccessible to a network-connected "
            "resource?"
        ),
        "name": "secplus_q215",
        "correct": "C",
        "explain": (
            "Correct. C — Host isolation quarantines or segments a system so it cannot reach or be reached by "
            "other network-connected resources, such as during incident response. Disabling unused services "
            "reduces local attack surface but does not fully block network connectivity. A web application "
            "firewall protects HTTP applications, not general host-to-network access. A network-based IDS "
            "detects suspicious traffic and does not by itself enforce isolation."
        ),
        "choices": [
            "Disablement of unused services",
            "Web application firewall",
            "Host isolation",
            "Network-based IDS",
        ],
        "objectives": ["4.5", "4.9"],
    },
    {
        "slug": "lobby-jack-port-security-visitor",
        "title": "Security+ — Port security (lobby jack)",
        "stem": (
            "A visitor plugs a laptop into a network jack in the lobby and is able to connect to the company's "
            "network. Which of the following should be configured on the existing network infrastructure to best "
            "prevent this activity?"
        ),
        "name": "secplus_q216",
        "correct": "A",
        "explain": (
            "Correct. A — Port security on switch ports can restrict allowed MAC addresses, limit learned "
            "addresses, or shut down unauthorized connections when an unknown device is plugged in. A web "
            "application firewall protects HTTP services, not physical switch access. Transport layer security "
            "encrypts traffic in transit and does not block an unauthorized host from joining the LAN. A VPN "
            "provides secure remote access over untrusted networks, not control of who may use an open lobby "
            "Ethernet jack."
        ),
        "choices": [
            "Port security",
            "Web application firewall",
            "Transport layer security",
            "Virtual private network",
        ],
        "objectives": ["4.5", "3.3"],
    },
    {
        "slug": "university-two-cloud-platform-diversity",
        "title": "Security+ — Platform diversity (dual cloud)",
        "stem": (
            "A university uses two different cloud solutions for storing student data. Which of the following "
            "does this scenario represent?"
        ),
        "name": "secplus_q217",
        "correct": "C",
        "explain": (
            "Correct. C — Platform diversity uses multiple vendors or technology stacks to reduce dependence "
            "on a single platform and limit impact if one provider fails or is compromised. Load balancing "
            "distributes traffic or workload across resources for performance or availability. Parallel processing "
            "runs tasks simultaneously across processors or nodes. Clustering groups systems to act as a unified "
            "high-availability unit, not necessarily different cloud providers."
        ),
        "choices": [
            "Load balancing",
            "Parallel processing",
            "Platform diversity",
            "Clustering",
        ],
        "objectives": ["3.1", "3.4"],
    },
    {
        "slug": "code-deployment-serverless-architecture",
        "title": "Security+ — Serverless (code deployment)",
        "stem": (
            "A company wants to reduce the time and expense associated with code deployment. Which of the "
            "following technologies should the company utilize?"
        ),
        "name": "secplus_q218",
        "correct": "A",
        "explain": (
            "Correct. A — Serverless architecture lets teams deploy functions without provisioning or managing "
            "servers, reducing deployment time and operational cost through provider-managed scaling and "
            "pay-per-use execution. Thin clients are lightweight end-user terminals, not application deployment "
            "platforms. A private cloud is an on-premises or dedicated cloud model and still requires "
            "infrastructure management. Virtual machines add guest OS overhead compared with deploying code "
            "directly as managed functions."
        ),
        "choices": [
            "Serverless architecture",
            "Thin clients",
            "Private cloud",
            "Virtual machines",
        ],
        "objectives": ["3.1", "3.2"],
    },
    {
        "slug": "web-app-auth-weakness-dynamic-analysis",
        "title": "Security+ — Dynamic analysis (web auth)",
        "stem": (
            "A company needs to determine whether authentication weaknesses in a customer-facing web "
            "application exist. Which of the following is the best technique to use?"
        ),
        "name": "secplus_q219",
        "correct": "D",
        "explain": (
            "Correct. D — Dynamic analysis (DAST) tests the running web application, probing login flows, "
            "session handling, and access controls as an attacker would against a live system. Static analysis "
            "reviews source code and may miss runtime authentication logic flaws. Packet capture passively "
            "observes traffic and does not systematically exercise auth mechanisms. Agent-based scanning targets "
            "hosts with installed agents. Network-based scanning finds network-layer issues, not deep web "
            "authentication weaknesses."
        ),
        "choices": [
            "Static analysis",
            "Packet capture",
            "Agent-based scanning",
            "Dynamic analysis",
            "Network-based scanning",
        ],
        "objectives": ["5.3", "5.5"],
    },
    {
        "slug": "hard-drive-wipe-tool-repurpose",
        "title": "Security+ — Wipe tool (repurpose drive)",
        "stem": (
            "Which of the following techniques can be used to sanitize the data contained on a hard drive while "
            "allowing for the hard drive to be repurposed?"
        ),
        "name": "secplus_q220",
        "correct": "D",
        "explain": (
            "Correct. D — A wipe tool performs secure overwrite or purge so data is not recoverable while the "
            "drive can be reused. Degaussing magnetically erases many HDDs and often renders media unreliable "
            "or unusable. A drive shredder physically destroys the device. A retention platform manages how "
            "long data is kept for policy or legal holds, not secure erasure for reuse."
        ),
        "choices": [
            "Degaussing",
            "Drive shredder",
            "Retention platform",
            "Wipe tool",
        ],
        "objectives": ["4.2", "3.3"],
    },
    {
        "slug": "admin-phishing-email-server-password",
        "title": "Security+ — Recognizing phishing (awareness)",
        "stem": (
            "An employee emailed a new systems administrator a malicious web link and convinced the "
            "administrator to change the email server's password. The employee used this access to remove the "
            "mailboxes of key personnel. Which of the following security awareness concepts would help prevent "
            "this threat in the future?"
        ),
        "name": "secplus_q221",
        "correct": "A",
        "explain": (
            "Correct. A — Recognizing phishing trains users to spot deceptive emails, suspicious links, and "
            "urgent credential-change requests before acting. Situational awareness is broader operational "
            "mindfulness and is less specific to fraudulent email lures. Password managers help store credentials "
            "but do not stop an administrator from being socially engineered into changing a server password. "
            "Reviewing email policies is an administrative activity, not end-user awareness that blocks this "
            "attack path."
        ),
        "choices": [
            "Recognizing phishing",
            "Providing situational awareness training",
            "Using password management",
            "Reviewing email policies",
        ],
        "objectives": ["2.2", "5.4"],
    },
    {
        "slug": "sql-log-or-1-equals-1-injection",
        "title": "Security+ — SQLi (OR 1=1 in logs)",
        "stem": (
            "An analyst discovers a suspicious item in the SQL server logs. Which of the following could be "
            "evidence of an attempted SQL injection?"
        ),
        "name": "secplus_q222",
        "correct": "D",
        "explain": (
            "Correct. D — UserId = 10 OR 1=1 is a classic tautology injection that can return all rows or bypass "
            "authentication logic in dynamic SQL. cat /etc/shadow is an operating-system command associated with "
            "command injection, not SQL syntax. dig performs DNS lookup and is not a SQL injection pattern. "
            "cd .. / .. / .. / attempts directory traversal in a filesystem path, not a database query."
        ),
        "choices": [
            "cat /etc/shadow",
            "dig 25.36.99.11",
            "cd .. / .. / .. /",
            "UserId = 10 OR 1=1;",
        ],
        "objectives": ["2.3", "2.5"],
    },
    {
        "slug": "layoffs-disgruntled-employee-supervisor-training",
        "title": "Security+ — Insider threat (layoffs awareness)",
        "stem": (
            "A company is in the process of cutting jobs to manage costs. The Chief Information Security Officer is "
            "concerned about the increased risk of an insider threat. Which of the following would most likely help "
            "the security awareness team address this potential threat?"
        ),
        "name": "secplus_q223",
        "correct": "B",
        "explain": (
            "Correct. B — Training supervisors to spot and manage disgruntled employees is an awareness and "
            "people-focused control during layoffs, when insider risk often rises. Disabling accounts early for "
            "those likely to be terminated is an access-management step coordinated with HR, not an awareness "
            "program deliverable. DLP monitoring targeted staff is a technical control with privacy and legal "
            "considerations, not primary awareness training. Social engineering awareness for executives does not "
            "directly address disgruntled insiders during workforce reductions."
        ),
        "choices": [
            "Immediately disable the accounts of staff who are likely to be terminated.",
            "Train supervisors to identify and manage disgruntled employees.",
            "Configure DLP to monitor staff who will be terminated.",
            "Raise awareness for business leaders on social engineering techniques.",
        ],
        "objectives": ["2.2", "5.4"],
    },
    {
        "slug": "suspicious-email-file-sandbox-analysis",
        "title": "Security+ — Sandbox (suspicious file)",
        "stem": (
            "An employee asks a security analyst to scan a suspicious email that contains a link to a file on a "
            "file-sharing site. The analyst determines that the file is safe after downloading and scanning the "
            "file with antivirus software. When the employee opens the file, their device is infected with "
            "ransomware. Which of the following steps should the analyst have taken?"
        ),
        "name": "secplus_q224",
        "correct": "C",
        "explain": (
            "Correct. C — Executing the file in an isolated sandbox reveals runtime behavior such as "
            "ransomware activity that static antivirus scans can miss. A code editor is for reviewing source "
            "text, not safely observing malicious execution. Netstat shows connections after something is "
            "already running and is not a substitute for controlled detonation. Checking a file hash with OSINT "
            "helps only when the sample is already known; unknown or polymorphic malware may have no useful "
            "reputation data."
        ),
        "choices": [
            "Review the file in a code editor.",
            "Monitor the file connections with netstat.",
            "Execute the file in a sandbox.",
            "Retrieve the file hash and check with OSINT.",
        ],
        "objectives": ["4.9", "2.4"],
    },
    {
        "slug": "risk-assessment-osint-no-proprietary-info",
        "title": "Security+ — OSINT (risk assessment)",
        "stem": (
            "An administrator wants to perform a risk assessment without using proprietary company information. "
            "Which of the following methods should the administrator use to gather information?"
        ),
        "name": "secplus_q225",
        "correct": "C",
        "explain": (
            "Correct. C — Open-source intelligence collects publicly available data such as DNS records, "
            "published advisories, and breach disclosures without accessing internal proprietary systems. "
            "Network scanning probes the organization's own hosts and requires internal scope or permission. "
            "Penetration testing exercises systems under rules of engagement and typically uses internal "
            "knowledge. Configuration auditing reviews internal device settings and company-specific baselines."
        ),
        "choices": [
            "Network scanning",
            "Penetration testing",
            "Open-source intelligence",
            "Configuration auditing",
        ],
        "objectives": ["5.1", "5.5"],
    },
    {
        "slug": "mfa-token-bypass-pretexting-attack",
        "title": "Security+ — Pretexting (MFA bypass)",
        "stem": (
            "An IT team rolls out a new management application that uses a randomly generated MFA token sent "
            "to the administrator's phone. Despite this new MFA precaution, there is a security breach of the same "
            "software. Which of the following describes this kind of attack?"
        ),
        "name": "secplus_q226",
        "correct": "D",
        "explain": (
            "Correct. D — Pretexting uses a fabricated scenario to trick the administrator into sharing the "
            "MFA code, approving a fraudulent login, or otherwise helping bypass the control. Smishing is phishing "
            "delivered specifically by SMS; the stem does not require that channel. Typosquatting uses look-alike "
            "domains. Espionage is broad intelligence gathering and is not the standard CompTIA label for this "
            "social engineering bypass of MFA."
        ),
        "choices": [
            "Smishing",
            "Typosquatting",
            "Espionage",
            "Pretexting",
        ],
        "objectives": ["2.2", "2.4"],
    },
    {
        "slug": "lost-mobile-device-mdm-prevent-data-loss",
        "title": "Security+ — MDM (lost mobile device)",
        "stem": (
            "An employee who was working remotely lost a mobile device containing company data. Which of the "
            "following provides the best solution to prevent future data loss?"
        ),
        "name": "secplus_q227",
        "correct": "A",
        "explain": (
            "Correct. A — Mobile device management enforces policies, encryption, and remote lock or wipe so "
            "lost devices can be contained before data is exposed. DLP helps block unauthorized data movement "
            "but does not centrally erase a missing phone. FDE protects data at rest if the device is powered "
            "off and locked but does not provide ongoing remote response after loss. EDR detects and responds "
            "to endpoint threats and is not the primary control for lost mobile device data protection."
        ),
        "choices": [
            "MDM",
            "DLP",
            "FDE",
            "EDR",
        ],
        "objectives": ["4.1", "4.5"],
    },
    {
        "slug": "data-classification-most-impacted-when-lost",
        "title": "Security+ — Critical data (loss impact)",
        "stem": (
            "Which of the following describes the category of data that is most impacted when it is lost?"
        ),
        "name": "secplus_q228",
        "correct": "D",
        "explain": (
            "Correct. D — Critical data is essential to operations and business continuity; losing it causes "
            "the greatest operational disruption. Confidential data must be protected from unauthorized "
            "disclosure, but loss is not always framed as the highest operational impact category. Public data "
            "is intended for open use with minimal harm if unavailable. Private data covers personal information "
            "where privacy harm matters, but CompTIA ties the strongest loss-of-data impact to critical."
        ),
        "choices": [
            "Confidential",
            "Public",
            "Private",
            "Critical",
        ],
        "objectives": ["3.3", "5.1"],
    },
    {
        "slug": "web-app-vulnerability-no-patch-zero-day",
        "title": "Security+ — Zero-day (no patch)",
        "stem": (
            "A security company informs its customers of a new vulnerability that affects web applications. The "
            "vulnerability does not have an available patch at the moment. Which of the following best describes "
            "this vulnerability?"
        ),
        "name": "secplus_q229",
        "correct": "A",
        "explain": (
            "Correct. A — A zero-day vulnerability is known (or actively exploited) before the vendor releases a "
            "fix. XSS is a web attack that injects script into pages users view. SQLi manipulates database "
            "queries through untrusted input. Buffer overflow writes past allocated memory bounds. Those are "
            "attack or flaw types, not the label for an unpatched newly disclosed issue."
        ),
        "choices": [
            "Zero-day",
            "XSS",
            "SQLi",
            "Buffer overflow",
        ],
        "objectives": ["2.3", "2.5"],
    },
    {
        "slug": "iaas-enclave-csp-responsibility-matrix",
        "title": "Security+ — Responsibility matrix (IaaS)",
        "stem": (
            "A customer has a contract with a CSP and wants to identify which controls should be implemented in "
            "the IaaS enclave. Which of the following is most likely to contain this information?"
        ),
        "name": "secplus_q230",
        "correct": "B",
        "explain": (
            "Correct. B — A responsibility matrix documents shared responsibility, mapping which security and "
            "operational controls the customer versus the CSP must implement in an IaaS enclave. A statement of "
            "work defines project scope and deliverables. A service-level agreement sets performance targets such as "
            "uptime. A master service agreement is the overarching legal contract and may reference the matrix but "
            "does not usually list control-by-control ownership by itself."
        ),
        "choices": [
            "Statement of work",
            "Responsibility matrix",
            "Service-level agreement",
            "Master service agreement",
        ],
        "objectives": ["3.4", "5.1"],
    },
    {
        "slug": "unsupported-critical-system-risk-accept",
        "title": "Security+ — Risk accept (unsupported system)",
        "stem": (
            "A systems administrator discovers a system that is no longer receiving support from the vendor. "
            "However, this system and its environment are critical to running the business, cannot be modified, and "
            "must stay online. Which of the following risk treatments is the most appropriate in this situation?"
        ),
        "name": "secplus_q231",
        "correct": "B",
        "explain": (
            "Correct. B — Accept acknowledges the residual risk when the system cannot be replaced, patched, or "
            "taken offline; compensating controls such as segmentation and monitoring often accompany acceptance. "
            "Reject is not a standard risk treatment in this framework. Transfer shifts financial liability but does "
            "not resolve an unsupported critical system that must run. Avoid would remove or stop using the system, "
            "which the scenario rules out because it is business-critical and must stay online."
        ),
        "choices": [
            "Reject",
            "Accept",
            "Transfer",
            "Avoid",
        ],
        "objectives": ["5.1", "5.2"],
    },
    {
        "slug": "encrypt-data-algorithms-key-length",
        "title": "Security+ — Encryption (algorithms and key length)",
        "stem": (
            "Which of the following are the most important considerations when encrypting data? (Select two)."
        ),
        "name": "secplus_q232",
        "choose_two": True,
        "correct": ["B", "D"],
        "explain": (
            "Correct. B and D — The encryption algorithm and key length determine cryptographic strength and "
            "resistance to brute-force attacks. Obfuscation hides logic or representation but is not a core "
            "encryption parameter. Data masking substitutes values for display or testing and is separate from "
            "encrypting data at rest or in transit. Tokenization replaces sensitive data with tokens in payment "
            "or privacy workflows. Salting adds randomness before hashing passwords and is not the primary "
            "consideration for general data encryption."
        ),
        "choices": [
            "Obfuscation",
            "Algorithms",
            "Data masking",
            "Key length",
            "Tokenization",
            "Salting",
        ],
        "objectives": ["1.4", "3.3"],
    },
    {
        "slug": "production-patch-change-control-first",
        "title": "Security+ — Change control (production patch)",
        "stem": (
            "A technician needs to apply a high-priority patch to a production system. Which of the following steps "
            "should be taken first?"
        ),
        "name": "secplus_q233",
        "correct": "C",
        "explain": (
            "Correct. C — Change control documents, approves, and schedules production changes before patching "
            "begins, even when urgency is high. Air-gapping isolates a system from networks and is not the usual "
            "first step for a planned patch. Moving the system to another segment may occur during maintenance "
            "but follows an approved change plan. Applying the patch immediately skips governance and rollback "
            "planning required in production environments."
        ),
        "choices": [
            "Air gap the system.",
            "Move the system to a different network segment.",
            "Create a change control request.",
            "Apply the patch to the system.",
        ],
        "objectives": ["4.1", "4.6"],
    },
    {
        "slug": "bank-vendor-stolen-laptop-encryption-at-rest",
        "title": "Security+ — Encryption at rest (stolen laptop)",
        "stem": (
            "A bank insists all of its vendors must prevent data loss on stolen laptops. Which of the following "
            "strategies is the bank requiring?"
        ),
        "name": "secplus_q234",
        "correct": "A",
        "explain": (
            "Correct. A — Encryption at rest, such as full-disk encryption, keeps stored data unreadable if a "
            "laptop is stolen and the drive is accessed offline. Masking obscures values in displays or test data "
            "and does not protect an entire stolen device. Data classification labels sensitivity but does not "
            "by itself encrypt storage. Permission restrictions limit who can access data during normal use "
            "and do not stop offline reads of an unencrypted stolen drive."
        ),
        "choices": [
            "Encryption at rest",
            "Masking",
            "Data classification",
            "Permission restrictions",
        ],
        "objectives": ["3.3", "1.4"],
    },
    {
        "slug": "iam-shift-access-time-of-day-restrictions",
        "title": "Security+ — Time-of-day restrictions (shifts)",
        "stem": (
            "A security engineer at a large company needs to enhance IAM to ensure that employees can only "
            "access corporate systems during their shifts. Which of the following access controls should the "
            "security engineer implement?"
        ),
        "name": "secplus_q235",
        "correct": "B",
        "explain": (
            "Correct. B — Time-of-day restrictions allow access only within defined windows that match employee "
            "shifts. Role-based access assigns permissions by job function, not schedule. Least privilege limits "
            "rights to what is required for the role but does not restrict login to shift hours. Biometric "
            "authentication verifies identity but does not by itself block access outside scheduled times."
        ),
        "choices": [
            "Role-based",
            "Time-of-day restrictions",
            "Least privilege",
            "Biometric authentication",
        ],
        "objectives": ["4.6", "3.2"],
    },
    {
        "slug": "change-management-board-approved-update",
        "title": "Security+ — Change management (board approval)",
        "stem": (
            "Which of the following is an example of change management?"
        ),
        "name": "secplus_q236",
        "correct": "A",
        "explain": (
            "Correct. A — Change management requires formal request, review, and approval before production "
            "updates are implemented; board approval fits that governance step. Setting a user password is routine "
            "account administration. A penetration test before patching is security testing that may support a "
            "change but is not change management itself. Auditing equipment for an executive report is asset "
            "inventory or audit activity, not the controlled change lifecycle."
        ),
        "choices": [
            "Implementing an update after a board grants approval",
            "Setting a new password for a user",
            "Performing a penetration test before deploying a patch",
            "Auditing all system equipment before sending the list to the Chief Executive Officer",
        ],
        "objectives": ["4.1", "4.6"],
    },
    {
        "slug": "database-encrypted-insider-threat-domain-user",
        "title": "Security+ — Insider threat (encrypted DB files)",
        "stem": (
            "An administrator discovers that some files on a database server were recently encrypted. The "
            "administrator sees from the security logs that the data was last accessed by a domain user. Which of the "
            "following best describes the type of attack that occurred?"
        ),
        "name": "secplus_q237",
        "correct": "A",
        "explain": (
            "Correct. A — An insider threat abuses legitimate access such as a domain account to harm systems; "
            "encryption of database files with access tied to a domain user fits this pattern, including a "
            "compromised insider credential. Social engineering is a manipulation technique, not the classification "
            "when logs show an internal account performed the action. A watering-hole attack compromises a site "
            "victims visit. Unauthorized attacker is vague; CompTIA emphasizes insider threat when a trusted domain "
            "user account is involved."
        ),
        "choices": [
            "Insider threat",
            "Social engineering",
            "Watering-hole",
            "Unauthorized attacker",
        ],
        "objectives": ["2.2", "2.4"],
    },
    {
        "slug": "high-risk-region-ip-geolocation-mitigation",
        "title": "Security+ — IP geolocation (high-risk regions)",
        "stem": (
            "Which of the following can be used to mitigate attacks from high-risk regions?"
        ),
        "name": "secplus_q238",
        "correct": "C",
        "explain": (
            "Correct. C — IP geolocation maps source addresses to countries or regions so firewalls and access "
            "policies can block or challenge traffic from high-risk areas. Obfuscation hides code or data "
            "representation and does not filter by geography. Data sovereignty governs where data may legally "
            "reside, not inbound attack source filtering. Encryption protects confidentiality and integrity but "
            "does not stop connections based on region of origin."
        ),
        "choices": [
            "Obfuscation",
            "Data sovereignty",
            "IP geolocation",
            "Encryption",
        ],
        "objectives": ["4.5", "3.4"],
    },
    {
        "slug": "login-script-baseline-enforcement",
        "title": "Security+ — Baseline enforcement (login script)",
        "stem": (
            "A systems administrator creates a script that validates OS version, patch levels, and installed "
            "applications when users log in. Which of the following examples best describes the purpose of this script?"
        ),
        "name": "secplus_q239",
        "correct": "C",
        "explain": (
            "Correct. C — Baseline enforcement checks endpoints against a defined secure configuration such "
            "as OS version, patches, and approved software at login. Resource scaling adjusts compute capacity "
            "for demand. Policy enumeration lists policies rather than verifying system state on each login. "
            "Guardrails implementation usually refers to cloud or platform guardrails, not a login script that "
            "validates local patch and application compliance."
        ),
        "choices": [
            "Resource scaling",
            "Policy enumeration",
            "Baseline enforcement",
            "Guardrails implementation",
        ],
        "objectives": ["4.1", "4.6"],
    },
    {
        "slug": "supply-chain-provider-privileged-access-target",
        "title": "Security+ — Supply chain (privileged access)",
        "stem": (
            "Which of the following explains how a supply chain service provider could introduce a security "
            "vulnerability into an organization?"
        ),
        "name": "secplus_q240",
        "correct": "D",
        "explain": (
            "Correct. D — A provider with privileged access to client systems can be compromised and used as a "
            "path into the organization, a common supply chain risk. Delaying hardware shipments affects "
            "operations but does not by itself introduce a technical vulnerability through trusted access. "
            "Outsourcing customer service changes support staffing, not privileged technical access to client "
            "systems. Failing to encrypt an internal database is the organization's control gap, not how a "
            "supply chain partner introduces risk through trusted connectivity."
        ),
        "choices": [
            "Delaying hardware shipments needed for system upgrades",
            "Outsourcing customer service operations to a foreign call center",
            "Failing to encrypt data stored on the organization's internal database",
            "Having privileged access to client systems and becoming a target for attackers",
        ],
        "objectives": ["5.1", "5.5"],
    },
    {
        "slug": "database-misconfiguration-sql-injection",
        "title": "Security+ — SQL injection (DB misconfiguration)",
        "stem": (
            "Which of the following involves an attempt to take advantage of database misconfigurations?"
        ),
        "name": "secplus_q241",
        "correct": "B",
        "explain": (
            "Correct. B — SQL injection exploits weak database and application configuration such as excessive "
            "privileges, dynamic query construction, or missing input controls to read or modify data. Buffer "
            "overflow corrupts memory by writing past buffer bounds. VM escape breaks out of a virtual machine "
            "to the host. Memory injection inserts code into process memory and is not specific to database "
            "misconfiguration."
        ),
        "choices": [
            "Buffer overflow",
            "SQL injection",
            "VM escape",
            "Memory injection",
        ],
        "objectives": ["2.3", "2.5"],
    },
    {
        "slug": "domain-admin-audit-remove-rotate-passwords",
        "title": "Security+ — Domain admin audit (remediate)",
        "stem": (
            "A security audit of an organization revealed that most of the IT staff members have domain "
            "administrator credentials and do not change the passwords regularly. Which of the following solutions "
            "should the security team propose to resolve the findings in the most complete way?"
        ),
        "name": "secplus_q242",
        "correct": "B",
        "explain": (
            "Correct. B — Reviewing the domain administrators group removes excessive privileged accounts and "
            "rotating all passwords addresses both audit findings in one remediation. Password rotation GPOs alone "
            "do not reduce how many staff hold domain admin rights. IdP integration with SSO and MFA strengthens "
            "authentication but does not by itself right-size membership in the administrators group. A PAM vault "
            "with RBAC is a strong long-term control but the most direct complete fix for too many domain admins "
            "plus stale passwords is audit, remove unneeded admins, and rotate credentials."
        ),
        "choices": [
            "Creating group policies to enforce password rotation on domain administrator credentials",
            "Reviewing the domain administrator group, removing all unnecessary administrators, and rotating all passwords",
            "Integrating the domain administrator's group with an IdP and requiring SSO with MFA for all access",
            "Securing domain administrator credentials in a PAM vault and controlling access with role-based access control",
        ],
        "objectives": ["4.6", "5.4"],
    },
    {
        "slug": "alert-fatigue-false-positive-ignored",
        "title": "Security+ — False positive (alert fatigue)",
        "stem": (
            "Which of the following alert types is the most likely to be ignored over time?"
        ),
        "name": "secplus_q243",
        "correct": "C",
        "explain": (
            "Correct. C — False positives are benign events flagged as incidents; repeated noise leads to "
            "alert fatigue and analysts ignoring alerts. True positives indicate real issues that should be "
            "investigated. True negatives mean no alert when nothing is wrong, so there is nothing to ignore. "
            "False negatives are missed real threats; they are dangerous but are not the alert type staff "
            "learn to dismiss from repeated benign notifications."
        ),
        "choices": [
            "True positive",
            "True negative",
            "False positive",
            "False negative",
        ],
        "objectives": ["4.9", "4.4"],
    },
    {
        "slug": "ha-network-recovery-responsiveness",
        "title": "Security+ — HA network (choose two)",
        "stem": (
            "Which of the following must be considered when designing a high-availability network? (Choose two)."
        ),
        "name": "secplus_q244",
        "choose_two": True,
        "correct": ["A", "D"],
        "explain": (
            "Correct. A and D — High-availability design requires ease of recovery so failures restore service "
            "quickly with minimal downtime, and responsiveness so the network handles load and failover without "
            "degrading performance. Ability to patch supports maintenance but is not a primary HA design pillar. "
            "Physical isolation and attack surface are security architecture concerns. Extensible authentication "
            "addresses identity scale, not availability goals."
        ),
        "choices": [
            "Ease of recovery",
            "Ability to patch",
            "Physical isolation",
            "Responsiveness",
            "Attack surface",
            "Extensible authentication",
        ],
        "objectives": ["3.1", "3.4"],
    },
    {
        "slug": "internal-audit-control-gaps-remediation",
        "title": "Security+ — Internal audit (control gaps)",
        "stem": (
            "Which of the following is the most likely benefit of conducting an internal audit?"
        ),
        "name": "secplus_q245",
        "correct": "C",
        "explain": (
            "Correct. C — Internal audits evaluate controls and processes to identify gaps the organization "
            "can remediate before external review or incidents. Shareholder reporting is more associated with "
            "external assurance and governance disclosures. Audit reports are formal and tracked, not informal "
            "and casually reassigned. Internal audits complement but do not eliminate required external audits."
        ),
        "choices": [
            "Findings are reported to shareholders.",
            "Reports are not formal and can be reassigned.",
            "Control gaps are identified for remediation.",
            "The need for external audits is eliminated.",
        ],
        "objectives": ["5.4", "5.5"],
    },
    {
        "slug": "network-device-hardening-telnet-to-ssh",
        "title": "Security+ — Device hardening (SSH vs Telnet)",
        "stem": (
            "A network engineer is increasing the overall security of network devices and needs to harden the "
            "devices. Which of the following will best accomplish this task?"
        ),
        "name": "secplus_q246",
        "correct": "C",
        "explain": (
            "Correct. C — Replacing Telnet with SSH encrypts device management traffic and removes cleartext "
            "credential exposure. Centralized logging improves detection and auditing but does not by itself "
            "remove an insecure management protocol. Creating more local administrator accounts can expand "
            "privileged access unless tightly controlled. Enabling HTTP administration exposes credentials and "
            "configuration in cleartext and weakens hardening."
        ),
        "choices": [
            "Configuring centralized logging",
            "Generating local administrator accounts",
            "Replacing Telnet with SSH",
            "Enabling HTTP administration",
        ],
        "objectives": ["4.1", "4.6"],
    },
    {
        "slug": "asset-tracking-unauthorized-devices",
        "title": "Security+ — Asset tracking (rogue devices)",
        "stem": (
            "Which of the following is a security benefit of an effective IT asset tracking system?"
        ),
        "name": "secplus_q247",
        "correct": "A",
        "explain": (
            "Correct. A — Asset tracking maintains an inventory of authorized hardware and software so "
            "unauthorized or unmanaged devices on the network are easier to detect. DLP prevents prohibited "
            "data exfiltration from endpoints. Automated root cause analysis for all incidents is beyond typical "
            "asset inventory scope and relies on logging and investigation tools. Backup and recovery procedures "
            "are continuity controls, not the primary security benefit of asset tracking."
        ),
        "choices": [
            "Helping identify unauthorized or unmanaged devices connected to the network",
            "Preventing prohibited data exfiltration from endpoints on the network",
            "Assisting with automated root cause analysis for all security incidents on the network",
            "Ensuring proper data backup and recovery procedures are in place",
        ],
        "objectives": ["4.1", "4.9"],
    },
    {
        "slug": "byod-mdm-approved-applications-only",
        "title": "Security+ — MDM (approved apps on BYOD)",
        "stem": (
            "A company is implementing a policy to allow employees to use their personal equipment for work. "
            "However, the company wants to ensure that only company-approved applications can be installed. "
            "Which of the following addresses this concern?"
        ),
        "name": "secplus_q248",
        "correct": "A",
        "explain": (
            "Correct. A — MDM can enforce application allow lists and block or remove unapproved software on "
            "employee-owned devices used for work. Containerization separates corporate data in a work profile "
            "but is not primarily how only approved applications are installed across the device. DLP monitors "
            "and blocks sensitive data movement, not application installation policy. FIM detects unauthorized "
            "file changes and does not control which applications may be installed."
        ),
        "choices": [
            "MDM",
            "Containerization",
            "DLP",
            "FIM",
        ],
        "objectives": ["4.1", "4.5"],
    },
    {
        "slug": "risk-ale-15000-twice-in-three-years",
        "title": "Security+ — ALE ($15k, 2 in 3 years)",
        "stem": (
            "A security analyst determines that a security breach will have a financial impact of $15,000 and is "
            "expected to occur twice within a three-year period. Which of the following is the ALE for this risk?"
        ),
        "name": "secplus_q249",
        "correct": "B",
        "explain": (
            "Correct. B — ALE equals SLE times ARO. Here SLE is $15,000 per incident and ARO is 2 events in "
            "3 years, or 2/3 per year. $15,000 × (2/3) = $10,000 annualized loss expectancy. $7,500 would use "
            "one occurrence in three years. $15,000 is the single-loss value, not annualized. $30,000 would "
            "assume two full losses every year rather than twice in three years."
        ),
        "choices": [
            "$7,500",
            "$10,000",
            "$15,000",
            "$30,000",
        ],
        "objectives": ["5.1", "5.2"],
    },
    {
        "slug": "file-server-slow-resource-consumption-alert",
        "title": "Security+ — Resource consumption (file server)",
        "stem": "",
        "name": "secplus_q250",
        "correct": "D",
        "explain": (
            "Correct. D — Very high CPU and memory utilization indicate resource consumption, which explains "
            "a slow and intermittently available file server. Concurrent session usage is the same account "
            "active from multiple locations at once. Network saturation would show high network utilization, "
            "not primarily CPU and memory pegged. Account lockout follows repeated failed logins and does not "
            "match server performance metrics."
        ),
        "choices": [
            "Concurrent session usage",
            "Network saturation",
            "Account lockout",
            "Resource consumption",
        ],
        "prepend_html": build_file_server_resource_exhibit(),
        "objectives": ["4.9", "2.4"],
    },
    {
        "slug": "mou-vs-sow-legally-binding",
        "title": "Security+ — MOU vs SOW",
        "stem": (
            "Which of the following best describes the main difference between an MOU and an SOW?"
        ),
        "name": "secplus_q251",
        "correct": "A",
        "explain": (
            "Correct. A — A memorandum of understanding (MOU) states mutual intent and is often non-binding, "
            "while a statement of work (SOW) defines deliverables and outcomes in a binding engagement. An MOU "
            "does not primarily identify engagement details while an SOW names who will engage; both documents "
            "can require signatures from involved parties. An SOW is the detailed task and deliverable document; "
            "an MOU is typically higher-level cooperation, not more detailed than an SOW."
        ),
        "choices": [
            "An MOU is usually not legally binding, while an SOW is usually legally binding about outcomes.",
            "An MOU identifies engagement details, while an SOW specifies who will engage.",
            "An MOU requires signatures from both parties, while an SOW only requires a signature from the service provider.",
            "An MOU is typically very detailed about tasks, while an SOW is typically high-level.",
        ],
        "objectives": ["5.1", "5.5"],
    },
    {
        "slug": "server-hardening-disable-accounts-services",
        "title": "Security+ — Server hardening (choose two)",
        "stem": (
            "An administrator needs to perform server hardening before deployment. Which of the following steps "
            "should the administrator take? (Select two)."
        ),
        "name": "secplus_q252",
        "choose_two": True,
        "correct": ["A", "C"],
        "explain": (
            "Correct. A and C — Hardening reduces attack surface by disabling default accounts with known "
            "credentials and removing unnecessary services that expand exposure. Adding the server to an asset "
            "inventory supports tracking but is not hardening itself. Default passwords should be changed or "
            "removed, not documented for reuse. Sending logs to a SIEM is detective monitoring after deployment. "
            "Joining a domain integrates the server but is not the core pre-deployment hardening step."
        ),
        "choices": [
            "Disable default accounts.",
            "Add the server to the asset inventory.",
            "Remove unnecessary services.",
            "Document default passwords.",
            "Send server logs to the SIEM.",
            "Join the server to the corporate domain.",
        ],
        "objectives": ["4.1", "4.6"],
    },
    {
        "slug": "sql-update-temp-field-race-condition",
        "title": "Security+ — Race condition (SQL update)",
        "stem": (
            "During a SQL update of a database, a temporary field used as part of the update sequence was "
            "modified by an attacker before the update completed in order to allow access to the system. Which of "
            "the following best describes this type of vulnerability?"
        ),
        "name": "secplus_q253",
        "correct": "A",
        "explain": (
            "Correct. A — A race condition exploits timing between steps; changing a temporary field before the "
            "update finishes is a time-of-check versus time-of-use flaw. Memory injection inserts code into "
            "process memory. Malicious update tampers with software distribution or patches. Side loading "
            "installs applications from unofficial sources on a device."
        ),
        "choices": [
            "Race condition",
            "Memory injection",
            "Malicious update",
            "Side loading",
        ],
        "objectives": ["2.3", "2.5"],
    },
    {
        "slug": "phishing-incentive-gamification-awareness",
        "title": "Security+ — Gamification (phishing incentives)",
        "stem": (
            "After multiple phishing simulations, the Chief Security Officer announces a new program that "
            "incentivizes employees to not click phishing links in the upcoming quarter. Which of the following "
            "security awareness execution techniques does this represent?"
        ),
        "name": "secplus_q254",
        "correct": "D",
        "explain": (
            "Correct. D — Gamification uses rewards, competition, or incentives to encourage desired security "
            "behaviors such as avoiding phishing links. Computer-based training delivers interactive lessons "
            "but is not defined by quarterly incentives. Insider threat awareness focuses on malicious or "
            "negligent insiders, not phishing click rates. A SOAR playbook automates incident response workflows, "
            "not employee awareness campaigns."
        ),
        "choices": [
            "Computer-based training",
            "Insider threat awareness",
            "SOAR playbook",
            "Gamification",
        ],
        "objectives": ["2.2", "5.4"],
    },
    {
        "slug": "iaas-database-security-client-responsibility",
        "title": "Security+ — Shared responsibility (IaaS DB)",
        "stem": (
            "Which of the following roles, according to the shared responsibility model, is responsible for securing "
            "the company's database in an IaaS model for a cloud environment?"
        ),
        "name": "secplus_q255",
        "correct": "A",
        "explain": (
            "Correct. A — In IaaS the client (customer) secures the guest OS, applications, and data including "
            "database configuration, access controls, and encryption. The cloud provider secures the underlying "
            "infrastructure such as physical hosts and hypervisor. A third-party vendor is not the standard shared "
            "responsibility party unless contracted separately. A DBA may administer the database but shared "
            "responsibility assigns cloud workload security to the customer in IaaS."
        ),
        "choices": [
            "Client",
            "Third-party vendor",
            "Cloud provider",
            "DBA",
        ],
        "objectives": ["3.4", "5.1"],
    },
    {
        "slug": "powershell-ioc-edr-logs-investigation",
        "title": "Security+ — EDR logs (PowerShell IoC)",
        "stem": (
            "A security analyst investigates an incident in which a PowerShell script was identified as a potential "
            "IoC. Which of the following will best help the analyst identify an attempt to compromise the system?"
        ),
        "name": "secplus_q256",
        "correct": "C",
        "explain": (
            "Correct. C — EDR logs capture endpoint process execution, script activity, and behavioral alerts "
            "where PowerShell is commonly abused. SNMP logs report network device health and status. Firewall "
            "logs show permitted or denied connections at the perimeter. IPS logs record network signature "
            "matches and may miss host-based PowerShell abuse that never triggered inline network rules."
        ),
        "choices": [
            "SNMP logs",
            "Firewall logs",
            "EDR logs",
            "IPS logs",
        ],
        "objectives": ["4.9", "2.4"],
    },
    {
        "slug": "bia-backup-schedule-rpo",
        "title": "Security+ — RPO (backup schedule / BIA)",
        "stem": (
            "Which of the following metrics impacts the backup schedule as part of the BIA?"
        ),
        "name": "secplus_q257",
        "correct": "B",
        "explain": (
            "Correct. B — Recovery point objective (RPO) is the maximum acceptable data loss window and "
            "directly drives how often backups must run. Recovery time objective (RTO) is maximum acceptable "
            "downtime to restore service, not backup frequency. Mean time to repair (MTTR) is average repair "
            "duration. Mean time between failures (MTBF) is average time between failures, a reliability metric."
        ),
        "choices": [
            "RTO",
            "RPO",
            "MTTR",
            "MTBF",
        ],
        "objectives": ["3.4", "5.2"],
    },
    {
        "slug": "removable-media-malware-awareness-training",
        "title": "Security+ — Removable media (awareness)",
        "stem": (
            "While a user reviews their email, a host gets infected by malware from an external hard drive plugged "
            "into the host. The malware steals all the user's credentials stored in the browser. Which of the "
            "following training topics should the user review to prevent this situation from reoccurring?"
        ),
        "name": "secplus_q258",
        "correct": "B",
        "explain": (
            "Correct. B — Removable media and cables training covers risks of untrusted USB drives and external "
            "storage that can introduce malware when connected. Operational security is broader workplace "
            "security behavior. Password management addresses credential strength and storage practices but "
            "does not stop infection from a plugged-in drive. Social engineering targets deceptive messages and "
            "calls; the compromise path here was the external hard drive, not the email review itself."
        ),
        "choices": [
            "Operational security",
            "Removable media and cables",
            "Password management",
            "Social engineering",
        ],
        "objectives": ["2.2", "5.4"],
    },
    {
        "slug": "new-regulation-gap-analysis-next",
        "title": "Security+ — Gap analysis (new regulation)",
        "stem": (
            "A new security regulation was announced that will take effect in the coming year. A company must "
            "comply with it to remain in business. Which of the following activities should the company perform next?"
        ),
        "name": "secplus_q259",
        "correct": "A",
        "explain": (
            "Correct. A — Gap analysis compares current controls and practices to the new regulation to identify "
            "what must change before the effective date. Policy review and security procedure evaluation follow "
            "once gaps are known. Threat scope reduction is a risk treatment approach and is not the standard "
            "first step when a new mandatory regulation is announced."
        ),
        "choices": [
            "Gap analysis",
            "Policy review",
            "Security procedure evaluation",
            "Threat scope reduction",
        ],
        "objectives": ["5.1", "5.4"],
    },
    {
        "slug": "dlp-dns-filtering-email-web-protection",
        "title": "Security+ — DLP and DNS filtering (choose two)",
        "stem": (
            "A company plans to secure its systems by:\n"
            "Preventing users from sending sensitive data over corporate email\n"
            "Restricting access to potentially harmful websites\n"
            "Which of the following features should the company set up? (Select two)."
        ),
        "name": "secplus_q260",
        "choose_two": True,
        "correct": ["A", "B"],
        "explain": (
            "Correct. A and B — DLP software detects and blocks sensitive data leaving the organization through "
            "email. DNS filtering blocks or redirects requests to malicious or disallowed sites by category or "
            "reputation. File integrity monitoring detects unauthorized file changes, not outbound email content. "
            "A stateful firewall tracks connection state but is not the primary control for email DLP or web "
            "category filtering. Guardrails are cloud policy boundaries, not the usual email and web controls "
            "described. Antivirus signatures detect known malware, not policy-based email or website restriction."
        ),
        "choices": [
            "DLP software",
            "DNS filtering",
            "File integrity monitoring",
            "Stateful firewall",
            "Guardrails",
            "Antivirus signatures",
        ],
        "objectives": ["4.5", "3.3"],
    },
    {
        "slug": "soc-soar-reduce-manual-analyst-work",
        "title": "Security+ — SOAR (reduce SOC manual work)",
        "stem": (
            "A growing company would like to enhance the ability of its security operations center to detect threats "
            "but reduce the amount of manual work required for the security analysts. Which of the following would "
            "best enable the reduction in manual work?"
        ),
        "name": "secplus_q261",
        "correct": "A",
        "explain": (
            "Correct. A — SOAR automates orchestration and response playbooks so analysts spend less time on "
            "repetitive triage and manual steps. A SIEM aggregates and correlates logs for detection but often "
            "increases alert volume without automation. MDM manages mobile devices. DLP prevents unauthorized "
            "data movement and does not automate SOC analyst workflows."
        ),
        "choices": [
            "SOAR",
            "SIEM",
            "MDM",
            "DLP",
        ],
        "objectives": ["4.9", "4.4"],
    },
    {
        "slug": "data-in-transit-tls-13-protection",
        "title": "Security+ — TLS 1.3 (data in transit)",
        "stem": (
            "Which of the following would be the most appropriate way to protect data in transit?"
        ),
        "name": "secplus_q262",
        "correct": "C",
        "explain": (
            "Correct. C — TLS 1.3 is a current protocol that encrypts and authenticates data moving across "
            "networks such as HTTPS. SHA-256 is a hash algorithm for integrity, not a transport encryption "
            "protocol. SSL 3.0 is deprecated and vulnerable and should not be used. AES-256 is a symmetric "
            "cipher often used inside TLS but is not by itself the end-to-end protection mechanism for data "
            "in transit."
        ),
        "choices": [
            "SHA-256",
            "SSL 3.0",
            "TLS 1.3",
            "AES-256",
        ],
        "objectives": ["1.4", "3.3"],
    },
    {
        "slug": "remote-to-office-recurring-training-awareness",
        "title": "Security+ — Recurring training (remote to office)",
        "stem": (
            "A technician wants to improve the situational and environmental awareness of existing users as they "
            "transition from remote to in-office work. Which of the following is the best option?"
        ),
        "name": "secplus_q263",
        "correct": "C",
        "explain": (
            "Correct. C — Modifying recurring training updates content for existing users on office-specific "
            "risks such as physical security and environmental awareness during the transition. Periodic "
            "reminders help but are less structured than updated recurring training. New hire documentation "
            "applies to new employees, not the existing workforce changing work location. A phishing campaign "
            "targets email deception skills and does not broadly cover in-office environmental awareness."
        ),
        "choices": [
            "Send out periodic security reminders.",
            "Update the content of new hire documentation.",
            "Modify the content of recurring training.",
            "Implement a phishing campaign",
        ],
        "objectives": ["2.2", "5.4"],
    },
    {
        "slug": "waf-policies-iac-automatic-deployment",
        "title": "Security+ — IaC (WAF on deploy)",
        "stem": (
            "A security team wants WAF policies to be automatically created when applications are deployed. "
            "Which concept describes this capability?"
        ),
        "name": "secplus_q264",
        "correct": "A",
        "explain": (
            "Correct. A — Infrastructure as code (IaC) defines WAF rules and other controls in versioned "
            "templates that deploy automatically with applications. IoT refers to connected devices such as "
            "sensors and appliances. IoC is an indicator of compromise used in threat detection. IaaS is a "
            "cloud service model providing virtualized infrastructure, not automated policy provisioning code."
        ),
        "choices": [
            "IaC",
            "IoT",
            "IoC",
            "IaaS",
        ],
        "objectives": ["3.1", "4.1"],
    },
    {
        "slug": "sqli-forensics-application-log-threat-command",
        "title": "Security+ — SQLi forensics (application log)",
        "stem": (
            "A forensic engineer determines that the root cause of a compromise is a SQL injection attack. "
            "Which of the following should the engineer review to identify the command used by the threat actor?"
        ),
        "name": "secplus_q265",
        "correct": "B",
        "explain": (
            "Correct. B — Application logs (web server, WAF, or application framework logs) record HTTP "
            "requests and user input where malicious SQL payloads appear. Metadata describes file or object "
            "properties, not injected query strings. System logs focus on OS and service events and rarely "
            "capture full application-layer attack strings. NetFlow summarizes connection metadata such as "
            "IPs and ports without HTTP or SQL payload content."
        ),
        "choices": [
            "Metadata",
            "Application log",
            "System log",
            "Netflow log",
        ],
        "objectives": ["4.3", "4.8"],
    },
    {
        "slug": "nac-platform-wired-attack-surface",
        "title": "Security+ — NAC (wired attack surface)",
        "stem": (
            "After a security incident, a systems administrator asks the company to buy a NAC platform. "
            "Which of the following attack surfaces is the systems administrator trying to protect?"
        ),
        "name": "secplus_q266",
        "correct": "B",
        "explain": (
            "Correct. B — Network access control (NAC) enforces authentication and compliance before devices "
            "join the corporate wired or wireless LAN, reducing risk from unauthorized endpoints on physical "
            "ports. Bluetooth is a short-range personal-area wireless surface. NFC is proximity contactless "
            "communication. SCADA covers industrial control systems and OT networks, which use different "
            "segmentation and controls than typical enterprise NAC deployments."
        ),
        "choices": [
            "Bluetooth",
            "Wired",
            "NFC",
            "SCADA",
        ],
        "objectives": ["3.3", "4.6"],
    },
    {
        "slug": "vendor-diversity-zero-day-resiliency-benefit",
        "title": "Security+ — Vendor diversity (zero-day)",
        "stem": "Which of the following is a benefit of vendor diversity?",
        "name": "secplus_q267",
        "correct": "B",
        "explain": (
            "Correct. B — Using multiple vendors limits blast radius when a zero-day affects one product line; "
            "not every system shares the same vulnerable codebase. Patch availability varies by vendor and is "
            "not improved simply by diversifying suppliers. Secure configuration guides are vendor-specific, so "
            "diversity increases documentation work rather than universal applicability. Load balancing distributes "
            "traffic for availability and is unrelated to vendor diversity."
        ),
        "choices": [
            "Patch availability",
            "Zero-day resiliency",
            "Secure configuration guide applicability",
            "Load balancing",
        ],
        "objectives": ["2.4", "3.9"],
    },
    {
        "slug": "executive-boardroom-tabletop-incident-response",
        "title": "Security+ — Tabletop exercise (IR plan)",
        "stem": (
            "Which of the following describes an executive team that is meeting in a board room and testing the "
            "company's incident response plan?"
        ),
        "name": "secplus_q268",
        "correct": "C",
        "explain": (
            "Correct. C — A tabletop exercise is a discussion-based walkthrough where leaders review roles, "
            "decisions, and procedures against a scenario without live system failover. Continuity of operations "
            "focuses on sustaining critical business functions during disruption. Capacity planning forecasts "
            "resource needs for growth or demand. Parallel processing runs multiple tasks simultaneously in "
            "computing and is unrelated to incident response testing."
        ),
        "choices": [
            "Continuity of operations",
            "Capacity planning",
            "Tabletop exercise",
            "Parallel processing",
        ],
        "objectives": ["2.4", "5.2"],
    },
    {
        "slug": "controls-assurance-independent-audit-report",
        "title": "Security+ — Independent audit (control assurance)",
        "stem": (
            "An organization is required to provide assurance that its controls are properly designed and "
            "operating effectively. Which of the following reports will best achieve the objective?"
        ),
        "name": "secplus_q269",
        "correct": "C",
        "explain": (
            "Correct. C — An independent audit (for example SOC 2 or ISO 27001 certification) attests that "
            "controls are suitably designed and operating effectively over a defined period. Red teaming "
            "simulates adversary tactics to test defenses but does not issue formal control assurance. "
            "Penetration testing finds exploitable weaknesses in systems and applications. A vulnerability "
            "assessment identifies known flaws and misconfigurations but does not evaluate overall control "
            "design and operating effectiveness for stakeholders."
        ),
        "choices": [
            "Red teaming",
            "Penetration testing",
            "Independent audit",
            "Vulnerability assessment",
        ],
        "objectives": ["5.5", "5.6"],
    },
    {
        "slug": "ids-database-login-credential-replay-attack",
        "title": "Security+ — Credential replay (IDS log)",
        "stem": (
            "A network security analyst monitors the network's IDS, which has flagged unusual activity. "
            "The IDS has detected multiple login attempts to a database server within a short period. "
            "These attempts come from various IP addresses that are not normally recognized by the network's "
            "usual traffic patterns. Each attempt uses the same username and password."
        ),
        "name": "secplus_q270",
        "correct": "B",
        "explain": (
            "Correct. B — Credential replay reuses captured or leaked username and password pairs; a "
            "distributed botnet can flood the same credentials from many hosts in seconds, producing rapid "
            "failed logins like these. Cross-site scripting injects malicious scripts in web content. "
            "Distributed denial of service overwhelms availability with traffic volume, not repeated "
            "authentication with one account. SQL injection manipulates database queries through application "
            "input, not parallel failed database logins from many internal IPs."
        ),
        "choices": [
            "Cross-site scripting",
            "Credential replay",
            "Distributed denial of service",
            "SQL injection",
        ],
        "prepend_html": build_ids_database_credential_replay_exhibit(),
        "objectives": ["2.4", "4.9"],
    },
    {
        "slug": "aup-managerial-control-type",
        "title": "Security+ — AUP (managerial control)",
        "stem": "Which of the following control types is AUP an example of?",
        "name": "secplus_q271",
        "correct": "B",
        "explain": (
            "Correct. B — An acceptable use policy (AUP) is a managerial (administrative) control: a documented "
            "policy that defines permitted and prohibited use of organizational resources. Physical controls "
            "include locks, guards, and fences. Technical controls use technology such as firewalls and "
            "encryption to enforce security. Operational controls are people-executed procedures such as "
            "backup or change-management steps performed in daily operations."
        ),
        "choices": [
            "Physical",
            "Managerial",
            "Technical",
            "Operational",
        ],
        "objectives": ["1.2", "5.5"],
    },
    {
        "slug": "saas-separate-logins-idp-federation-remediation",
        "title": "Security+ — IdP integration (SaaS logins)",
        "stem": (
            "A security analyst needs to propose a remediation plan for each item in a risk register. The item "
            "with the highest priority requires employees to have separate logins for SaaS solutions and different "
            "password complexity requirements for each solution. Which of the following implementation plans will "
            "most likely resolve this security issue?"
        ),
        "name": "secplus_q272",
        "correct": "B",
        "explain": (
            "Correct. B — Federating SaaS applications with a central identity provider enables single sign-on "
            "and one organizational password policy (often with MFA), eliminating separate local accounts and "
            "conflicting complexity rules per app. A unified complexity standard alone still leaves multiple "
            "disparate logins. Wildcard certificates protect TLS transport, not authentication sprawl. Geofencing "
            "restricts access by location and does not consolidate identities or password requirements."
        ),
        "choices": [
            "Creating a unified password complexity standard",
            "Integrating each SaaS solution with the Identity provider",
            "Securing access to each SaaS by using a single wildcard certificate",
            "Configuring geofencing on each SaaS solution",
        ],
        "objectives": ["3.8", "5.3"],
    },
    {
        "slug": "drp-critical-systems-restore-order-outage",
        "title": "Security+ — DRP (restore order)",
        "stem": (
            "A security team created a document that details the order in which critical systems should be "
            "brought back online after a major outage. Which of the following documents did the team create?"
        ),
        "name": "secplus_q273",
        "correct": "D",
        "explain": (
            "Correct. D — A disaster recovery plan (DRP) defines recovery priorities, procedures, and the "
            "sequence for restoring critical systems after a major outage. A communication plan specifies who "
            "is notified and how during an incident. An incident response plan covers detection, containment, "
            "and eradication of security events. A data retention policy defines how long data is kept and "
            "when it is disposed of, not system restoration order."
        ),
        "choices": [
            "Communication plan",
            "Incident response plan",
            "Data retention policy",
            "Disaster recovery plan",
        ],
        "objectives": ["3.6", "5.2"],
    },
    {
        "slug": "legacy-critical-app-mitigate-missing-preventive-controls",
        "title": "Security+ — Mitigate (legacy critical app)",
        "stem": (
            "Which of the following risk management strategies should an enterprise adopt first if a legacy "
            "application is critical to business operations and there are preventative controls that are not yet "
            "implemented?"
        ),
        "name": "secplus_q274",
        "correct": "A",
        "explain": (
            "Correct. A — Mitigate by implementing the missing preventative controls to reduce likelihood or "
            "impact while keeping the business-critical legacy application in service. Accept is appropriate "
            "only after controls are considered and residual risk is formally approved. Transfer shifts "
            "financial or contractual risk but does not replace implementing technical safeguards on a system "
            "you must continue to run. Avoid means eliminating the activity or asset, which is impractical "
            "when the legacy application is essential to operations."
        ),
        "choices": [
            "Mitigate",
            "Accept",
            "Transfer",
            "Avoid",
        ],
        "objectives": ["1.2", "5.3"],
    },
    {
        "slug": "customer-data-role-subject-marketing-custodian",
        "title": "Security+ — Data subject (customer role)",
        "stem": (
            "A company's marketing department collects, modifies, and stores sensitive customer data. The "
            "infrastructure team is responsible for securing the data while in transit and at rest. Which of the "
            "following data roles describes the customer?"
        ),
        "name": "secplus_q275",
        "correct": "C",
        "explain": (
            "Correct. C — The customer is the data subject: the individual whose personal information is "
            "collected and processed. A processor handles data on behalf of a controller under contract. "
            "A custodian implements technical safeguards such as encryption and access controls, which here "
            "fits the infrastructure team. The data owner is accountable for classification and use of the "
            "data, typically a business unit such as marketing, not the customer."
        ),
        "choices": [
            "Processor",
            "Custodian",
            "Subject",
            "Owner",
        ],
        "objectives": ["5.7", "5.8"],
    },
    {
        "slug": "application-availability-load-balancing-replace-server",
        "title": "Security+ — Load balancing (availability)",
        "stem": (
            "A company wants to improve the availability of its application with a solution that requires minimal "
            "effort in the event a server needs to be replaced or added. Which of the following would be the best "
            "solution to meet these objectives?"
        ),
        "name": "secplus_q276",
        "correct": "A",
        "explain": (
            "Correct. A — Load balancing distributes traffic across a pool of servers so a new or replacement "
            "node can be added with minimal reconfiguration. Fault tolerance keeps a system running despite "
            "component failure but does not by itself simplify scaling out application servers. Proxy servers "
            "relay client requests and are not primarily an availability pool for backend replacement. Replication "
            "copies data for redundancy or recovery and is not the simplest way to add application servers "
            "to a live service tier."
        ),
        "choices": [
            "Load balancing",
            "Fault tolerance",
            "Proxy servers",
            "Replication",
        ],
        "objectives": ["3.4", "4.2"],
    },
    {
        "slug": "web-log-useragent-command-injection-input-sanitization",
        "title": "Security+ — Input sanitization (command injection log)",
        "stem": "",
        "name": "secplus_q277",
        "correct": "A",
        "explain": (
            "Correct. A — The User-Agent header contains shell command substitution ($(…)), indicating "
            "command injection; input sanitization and validation of all untrusted HTTP input prevent the "
            "application or downstream processor from executing OS commands. Secure cookies protect session "
            "data in browsers. Static code analysis finds flaws during development but is not the primary "
            "runtime control for malicious request headers in logs. Sandboxing limits impact of executed code "
            "but does not stop injection at the entry point as directly as sanitizing input."
        ),
        "choices": [
            "Input sanitization",
            "Secure cookies",
            "Static code analysis",
            "Sandboxing",
        ],
        "prepend_html": build_web_server_command_injection_useragent_exhibit(),
        "objectives": ["2.3", "2.5"],
    },
    {
        "slug": "financial-industry-tokenization-mask-sensitive-data",
        "title": "Security+ — Tokenization (financial masking)",
        "stem": (
            "Which solution is most likely used in the financial industry to mask sensitive data?"
        ),
        "name": "secplus_q278",
        "correct": "A",
        "explain": (
            "Correct. A — Tokenization replaces card numbers and other sensitive values with non-sensitive "
            "tokens while the real data stays in a secure vault, which is common in payment and banking "
            "environments. Hashing is one-way and is used for integrity and password verification, not "
            "reversible business use of account data. Salting strengthens password hashes against rainbow "
            "tables. Steganography hides data inside other files and is not a standard financial-industry "
            "control for payment or account masking."
        ),
        "choices": [
            "Tokenization",
            "Hashing",
            "Salting",
            "Steganography",
        ],
        "objectives": ["1.4", "3.10"],
    },
    {
        "slug": "soar-reduce-steps-identify-contain-threats",
        "title": "Security+ — SOAR (identify and contain)",
        "stem": (
            "A security manager wants to reduce the number of steps required to identify and contain basic "
            "threats. Which of the following will help achieve this goal?"
        ),
        "name": "secplus_q279",
        "correct": "A",
        "explain": (
            "Correct. A — SOAR (security orchestration, automation, and response) runs playbooks that automate "
            "triage, enrichment, and containment actions so analysts complete fewer manual steps. A SIEM "
            "aggregates and correlates logs for detection but does not by itself orchestrate automated "
            "response. DMARC is an email authentication policy against spoofing and phishing. A network IDS "
            "detects suspicious traffic and alerts analysts but does not automate containment workflows."
        ),
        "choices": [
            "SOAR",
            "SIEM",
            "DMARC",
            "NIDS",
        ],
        "objectives": ["4.9", "4.4"],
    },
    {
        "slug": "digital-forensics-preservation-evidence-integrity",
        "title": "Security+ — Preservation (evidence integrity)",
        "stem": (
            "Which of the following elements of digital forensics should a company use if it needs to ensure the "
            "integrity of evidence?"
        ),
        "name": "secplus_q280",
        "correct": "A",
        "explain": (
            "Correct. A — Preservation protects evidence from alteration using chain of custody, write blockers, "
            "and cryptographic hashes so integrity can be verified in court or investigations. E-discovery is the "
            "legal process of locating electronically stored information for litigation. Acquisition is the act "
            "of collecting or imaging data; preservation maintains integrity before, during, and after collection. "
            "Containment is an incident response step that limits spread of an attack, not the forensic element "
            "that safeguards evidence integrity."
        ),
        "choices": [
            "Preservation",
            "E-discovery",
            "Acquisition",
            "Containment",
        ],
        "objectives": ["4.8", "4.9"],
    },
    {
        "slug": "compensating-control-high-risk-website-firewall-threat-prevention",
        "title": "Security+ — Compensating control (high-risk site)",
        "stem": (
            "Which of the following is a compensating control for providing user access to a high-risk website?"
        ),
        "name": "secplus_q281",
        "correct": "A",
        "explain": (
            "Correct. A — When business need requires access to a risky site, enabling firewall threat "
            "prevention (IPS, malware filtering, URL reputation) compensates by adding protection the primary "
            "block would have provided. Capturing web traffic in a SIEM supports detection and investigation but "
            "does not by itself reduce risk at access time. Allowing any port to the destination widens exposure "
            "and is not a control. Blocking the site on endpoint protection denies access and contradicts "
            "providing user access rather than compensating for it."
        ),
        "choices": [
            "Enabling threat prevention features on the firewall",
            "Configuring a SIEM tool to capture all web traffic",
            "Setting firewall rules to allow traffic from any port to that destination",
            "Blocking that website on the endpoint protection software",
        ],
        "objectives": ["1.2", "3.3"],
    },
    {
        "slug": "cvss-prioritize-vulnerability-remediation",
        "title": "Security+ — CVSS (prioritize remediation)",
        "stem": "Which of the following is a use of CVSS?",
        "name": "secplus_q282",
        "correct": "D",
        "explain": (
            "Correct. D — The Common Vulnerability Scoring System (CVSS) assigns standardized severity scores "
            "so organizations can prioritize which vulnerabilities to remediate first. Patch cost is a business "
            "and risk-management calculation, not the purpose of CVSS. Identifying open ports and services is "
            "done through scanning and enumeration. Static and dynamic code analysis tools find exploitable code "
            "defects during development or testing, not through CVSS scoring."
        ),
        "choices": [
            "To determine the cost associated with patching systems",
            "To identify unused ports and services that should be closed",
            "To analyze code for defects that could be exploited",
            "To prioritize the remediation of vulnerabilities",
        ],
        "objectives": ["4.3", "5.3"],
    },
    {
        "slug": "ddos-protection-availability-security-concept",
        "title": "Security+ — Availability (DDoS protection)",
        "stem": (
            "Which of the following security concepts is being followed when implementing a product that offers "
            "protection against DDoS attacks?"
        ),
        "name": "secplus_q283",
        "correct": "A",
        "explain": (
            "Correct. A — DDoS attacks aim to deny service by overwhelming resources; anti-DDoS controls protect "
            "availability so legitimate users can still reach systems. Non-repudiation proves who performed an "
            "action and cannot be denied later. Integrity ensures data is not altered without authorization. "
            "Confidentiality protects information from unauthorized disclosure."
        ),
        "choices": [
            "Availability",
            "Non-repudiation",
            "Integrity",
            "Confidentiality",
        ],
        "objectives": ["1.2", "3.1"],
    },
    {
        "slug": "financial-cloud-homomorphic-encrypted-processing",
        "title": "Security+ — Homomorphic (cloud processing)",
        "stem": (
            "A financial institution would like to store its customer data in the cloud but still allow the data to "
            "be accessed and manipulated while encrypted. Doing so would prevent the cloud service provider from "
            "being able to decipher the data due to its sensitivity. The financial institution is not concerned about "
            "computational overheads and slow speeds. Which of the following cryptographic techniques would best "
            "meet the requirement?"
        ),
        "name": "secplus_q284",
        "correct": "C",
        "explain": (
            "Correct. C — Homomorphic encryption allows operations on ciphertext so the cloud provider processes "
            "data without seeing plaintext. Asymmetric encryption uses key pairs for confidentiality and signatures "
            "but does not support general computation on encrypted data in the cloud. Symmetric encryption protects "
            "data at rest or in transit but the provider could decrypt if it held the key. Ephemeral keys are "
            "short-lived session keys for forward secrecy, not encrypted-data processing in untrusted clouds."
        ),
        "choices": [
            "Asymmetric",
            "Symmetric",
            "Homomorphic",
            "Ephemeral",
        ],
        "objectives": ["1.4", "3.10"],
    },
    {
        "slug": "reduce-enterprise-attack-surface-disable-unused-services",
        "title": "Security+ — Attack surface (disable services)",
        "stem": (
            "Which of the following is the best method to reduce the attack surface of an enterprise network?"
        ),
        "name": "secplus_q285",
        "correct": "A",
        "explain": (
            "Correct. A — Disabling unused network services on servers removes unnecessary listening ports and "
            "protocols enterprise-wide, directly shrinking the attack surface. Port security on wired switches "
            "limits unauthorized endpoints at access ports but does not reduce exposed services on servers. "
            "Changing default printer passwords hardens one device class, not the broad network footprint. A "
            "guest wireless network segments visitors but does not by itself minimize exploitable services "
            "across the enterprise."
        ),
        "choices": [
            "Disable unused network services on servers.",
            "Use port security for wired connections.",
            "Change default passwords for network printers.",
            "Create a guest wireless network for visitors.",
        ],
        "objectives": ["3.3", "4.1"],
    },
    {
        "slug": "accounting-fake-vendor-invoice-scam",
        "title": "Security+ — Invoice scam (fake vendor)",
        "stem": (
            "An employee in the accounting department receives an email containing a demand for payment for "
            "services performed by a vendor. However, the vendor is not in the vendor management database. "
            "Which of the following in this scenario is an example of?"
        ),
        "name": "secplus_q286",
        "correct": "D",
        "explain": (
            "Correct. D — An invoice scam (fake invoice fraud) sends payment demands for goods or services from "
            "a vendor that is not legitimate or not registered in the organization's vendor system. Pretexting "
            "fabricates a story to elicit information rather than primarily to trigger a fraudulent payment. "
            "Impersonation may be used as a tactic but the scenario best matches invoice fraud. Ransomware "
            "encrypts systems and demands ransom, not payment for fabricated vendor services."
        ),
        "choices": [
            "Pretexting",
            "Impersonation",
            "Ransomware",
            "Invoice scam",
        ],
        "objectives": ["2.1", "2.4"],
    },
    {
        "slug": "global-privacy-compliance-dpa-third-party-vendors",
        "title": "Security+ — DPA (global privacy compliance)",
        "stem": (
            "A company processes personal data from customers in multiple countries. Which of the following "
            "actions is most critical for maintaining legal compliance with global privacy regulations?"
        ),
        "name": "secplus_q287",
        "correct": "C",
        "explain": (
            "Correct. C — Regulations such as GDPR require data processing agreements (DPAs) with third-party "
            "processors that define security obligations, subprocessors, and lawful handling when personal data "
            "crosses borders. Encrypting data on local servers alone does not satisfy international transfer and "
            "processor-contract requirements. A data privacy officer may be required in some jurisdictions but "
            "contractual processor controls are foundational for vendor relationships. Strong passwords and "
            "firewalls are baseline technical controls and do not replace privacy governance with processors."
        ),
        "choices": [
            "Storing all customer data on encrypted local servers",
            "Hiring a data privacy officer to review contracts",
            "Ensuring DPAs are in place with third-party vendors",
            "Using strong passwords and firewalls on all endpoints",
        ],
        "objectives": ["5.7", "5.8"],
    },
    {
        "slug": "full-disk-encryption-confidentiality-concept",
        "title": "Security+ — Confidentiality (disk encryption)",
        "stem": (
            "A security administrator is implementing encryption on all hard drives in an organization. "
            "Which of the following security concepts is the administrator applying?"
        ),
        "name": "secplus_q288",
        "correct": "D",
        "explain": (
            "Correct. D — Encrypting hard drives protects data at rest from unauthorized disclosure if a device "
            "is lost or stolen, which supports confidentiality. Integrity ensures data is not altered without "
            "authorization. Authentication verifies identity before granting access. Zero Trust is a security "
            "model that requires continuous verification and least privilege, not the specific concept "
            "described by full-disk encryption alone."
        ),
        "choices": [
            "Integrity",
            "Authentication",
            "Zero Trust",
            "Confidentiality",
        ],
        "objectives": ["1.2", "3.10"],
    },
    {
        "slug": "hr-onboarding-phish-social-engineering-attack-vector",
        "title": "Security+ — Social engineering (HR phish)",
        "stem": (
            "A new employee logs in to the email system for the first time and notices a message from human "
            "resources about onboarding. The employee hovers over a few of the links within the email and discovers "
            "that the links do not correspond to links associated with the company. Which of the following attack "
            "vectors is most likely being used?"
        ),
        "name": "secplus_q289",
        "correct": "B",
        "explain": (
            "Correct. B — A fraudulent HR onboarding message with misleading links is social engineering that "
            "manipulates users through email (phishing). Business email compromise typically targets wire transfers "
            "or executive impersonation for financial fraud, not a new hire's first-day onboarding lure. An "
            "unsecured network is a wireless or transport exposure, not deceptive email content. Default "
            "credentials exploit unchanged factory passwords, not malicious links in a message."
        ),
        "choices": [
            "Business email",
            "Social engineering",
            "Unsecured network",
            "Default credentials",
        ],
        "objectives": ["2.1", "2.4"],
    },
    {
        "slug": "visitor-badge-endpoint-concurrent-session-alert",
        "title": "Security+ — Concurrent session (visitor badge alert)",
        "stem": "",
        "name": "secplus_q290",
        "correct": "C",
        "explain": (
            "Correct. C — Concurrent session usage means the same account is active from more than one "
            "workstation or location at the same time, which can indicate shared credentials or compromise "
            "on a visitor-badge issuance endpoint. Blocked content is a web-filter indicator. A brute-force "
            "attack shows repeated failed authentication attempts. Account lockout follows too many failed "
            "logins and disables the account."
        ),
        "choices": [
            "Blocked content",
            "Brute-force attack",
            "Concurrent session usage",
            "Account lockout",
        ],
        "prepend_html": build_visitor_badge_concurrent_session_exhibit(),
        "objectives": ["4.4", "4.9"],
    },
    {
        "slug": "ransomware-usb-recovery-sandboxing-environment",
        "title": "Security+ — Sandboxing (ransomware USB recovery)",
        "stem": (
            "A security analyst must recover files from a USB drive associated with a ransomware attack. "
            "Which of the following tools will help the analyst securely retrieve the files?"
        ),
        "name": "secplus_q291",
        "correct": "A",
        "explain": (
            "Correct. A — A sandboxing environment isolates analysis and recovery from production systems so "
            "ransomware on the USB cannot spread while the analyst examines and extracts files. An intrusion "
            "prevention system blocks malicious network traffic inline and does not mount or recover USB media. "
            "A file integrity management tool detects unauthorized file changes on monitored systems but does "
            "not safely handle infected removable media. Static code analysis reviews source code for defects "
            "during development, not forensic recovery from attack media."
        ),
        "choices": [
            "Sandboxing environment",
            "Intrusion prevention system",
            "File integrity management tool",
            "Static code analysis tool",
        ],
        "objectives": ["4.8", "4.9"],
    },
    {
        "slug": "ir-containment-phase-minimize-disruption",
        "title": "Security+ — Containment (minimize disruption)",
        "stem": (
            "Which of the following phases of the incident response process attempts to minimize disruption?"
        ),
        "name": "secplus_q292",
        "correct": "B",
        "explain": (
            "Correct. B — Containment limits spread and impact by isolating affected systems, accounts, or "
            "network segments so the organization can continue operating while the incident is handled. "
            "Recovery restores normal operations after containment and eradication. Preparation builds plans "
            "and capabilities before an incident occurs. Analysis investigates scope, indicators, and root cause "
            "but does not by itself limit ongoing business disruption."
        ),
        "choices": [
            "Recovery",
            "Containment",
            "Preparation",
            "Analysis",
        ],
        "objectives": ["4.8", "5.2"],
    },
    {
        "slug": "merger-align-security-programs-nist-csf",
        "title": "Security+ — CSF (merger alignment)",
        "stem": (
            "Two companies are in the process of merging. The companies need to decide how to standardize their "
            "information security programs. Which of the following would best align the security programs?"
        ),
        "name": "secplus_q293",
        "correct": "C",
        "explain": (
            "Correct. C — Adopting the same NIST Cybersecurity Framework (CSF) gives both organizations a common "
            "structure (Identify, Protect, Detect, Respond, Recover) to align policies, controls, and maturity. "
            "Shared CIS baselines help harden systems but do not by themselves unify enterprise security programs. "
            "Joint best practices lack a formal, comparable framework. A vulnerability report assesses technical "
            "findings and does not establish a unified program architecture for the merged entity."
        ),
        "choices": [
            "Shared deployment of CIS baselines",
            "Joint cybersecurity best practices",
            "Both companies following the same CSF",
            "Assessment of controls in a vulnerability report",
        ],
        "objectives": ["5.5", "5.6"],
    },
    {
        "slug": "ceo-smishing-gift-card-training-warning",
        "title": "Security+ — Smishing response (choose two)",
        "stem": (
            "Several employees received a fraudulent text message from someone claiming to be the Chief "
            "Executive Officer (CEO). The message stated:\n\n"
            "\"I'm in an airport right now with no access to email. I need you to buy gift cards for employee "
            "recognition awards. Please send the gift cards to the following email address.\"\n\n"
            "Which of the following are the best responses to this situation? (Choose two.)"
        ),
        "name": "secplus_q294",
        "choose_two": True,
        "correct": ["B", "C"],
        "explain": (
            "Correct. B and C — Warn the organization immediately so employees do not comply with the "
            "fraudulent request, and add smishing awareness (including simulations) to annual training to "
            "reduce future success. Canceling legitimate recognition gift cards does not address the attack. "
            "Changing the CEO's phone number does not stop number spoofing. Forensics on the CEO's phone is "
            "unnecessary when the attack is spoofed SMS social engineering, not compromise of the CEO device. "
            "Mobile device management governs corporate mobile policy but does not by itself remediate an "
            "active smishing campaign."
        ),
        "choices": [
            "Cancel current employee recognition gift cards.",
            "Add a smishing exercise to the annual company training.",
            "Issue a general email warning to the company.",
            "Have the CEO change phone numbers.",
            "Conduct a forensic investigation on the CEO's phone.",
            "Implement mobile device management.",
        ],
        "objectives": ["2.1", "5.4"],
    },
    {
        "slug": "malicious-file-signature-static-analysis",
        "title": "Security+ — Static analysis (file signature)",
        "stem": (
            "A security engineer needs to quickly identify a signature from a known malicious file. Which of the "
            "following analysis methods would the security engineer most likely use?"
        ),
        "name": "secplus_q295",
        "correct": "A",
        "explain": (
            "Correct. A — Static analysis examines the file without executing it, using hashes, strings, and "
            "signature databases to quickly identify known malware. Sandbox analysis runs the sample in an "
            "isolated environment to observe behavior and takes longer. Network traffic analysis inspects "
            "packets and flows, not file contents on disk. Package monitoring is not the standard method for "
            "extracting antivirus or IOC signatures from a malicious file sample."
        ),
        "choices": [
            "Static",
            "Sandbox",
            "Network traffic",
            "Package monitoring",
        ],
        "objectives": ["4.9", "2.3"],
    },
    {
        "slug": "malware-desktops-first-step-contain-hosts",
        "title": "Security+ — Contain hosts (malware on desktops)",
        "stem": (
            "A cybersecurity incident response team at a large company receives notification that malware is "
            "present on several corporate desktops. No known indicators of compromise have been found on the "
            "network. Which of the following should the team do first to secure the environment?"
        ),
        "name": "secplus_q296",
        "correct": "A",
        "explain": (
            "Correct. A — Containment is the first priority once malware is confirmed on endpoints: isolate "
            "impacted hosts to stop spread while investigation and eradication continue. Adding malware to an "
            "application blocklist helps prevent execution but does not immediately isolate already-infected "
            "systems. Segmenting a database server may follow risk assessment but is not the first action when "
            "desktops are known compromised. Firewall rules to block outbound beaconing are useful when C2 "
            "indicators exist; the stem states no network IOCs are known yet."
        ),
        "choices": [
            "Contain the impacted hosts",
            "Add the malware to the application blocklist.",
            "Segment the core database server.",
            "Implement firewall rules to block outbound beaconing",
        ],
        "objectives": ["4.8", "5.2"],
    },
    {
        "slug": "data-exfiltration-firewall-network-logs-investigation",
        "title": "Security+ — Exfiltration (firewall/network logs)",
        "stem": (
            "A company suffered a critical incident where 30GB of data was exfiltrated from the corporate network. "
            "Which of the following actions is the most efficient way to identify where the system data was "
            "exfiltrated from and where it was sent?"
        ),
        "name": "secplus_q297",
        "correct": "A",
        "explain": (
            "Correct. A — Firewall and network logs (including NetFlow) record source internal hosts, destination "
            "IPs or domains, and large outbound byte counts, which efficiently maps exfiltration paths for a "
            "30GB transfer. IPS and IDS logs focused on reconnaissance scans do not show bulk data movement "
            "destinations. Endpoint logs for file-sharing applications may show local activity but do not "
            "reliably trace volume and external recipients across the network. External vulnerability scans "
            "identify weaknesses before exploitation, not where data was sent after exfiltration."
        ),
        "choices": [
            (
                "Analyze firewall and network logs for large amounts of outbound traffic to external IP "
                "addresses or domains."
            ),
            (
                "Analyze IPS and IDS logs to find the IP addresses used by the attacker for reconnaissance scans."
            ),
            (
                "Analyze endpoint and application logs to see whether file-sharing programs were running."
            ),
            "Analyze external vulnerability scans to identify exploitable systems.",
        ],
        "objectives": ["4.9", "4.4"],
    },
    {
        "slug": "certificate-internal-source-self-signed",
        "title": "Security+ — Self-signed certificate",
        "stem": (
            "Which of the following is an example of a certificate that is generated by an internal source?"
        ),
        "name": "secplus_q298",
        "correct": "C",
        "explain": (
            "Correct. C — A self-signed certificate is issued and signed by the same organization or host rather "
            "than a public third-party certificate authority, which is common for internal services. A digital "
            "signature is a cryptographic operation that proves integrity and authenticity, not a certificate type. "
            "An asymmetric key is a public-private key pair used with PKI but is not itself a certificate. A "
            "symmetric key is a shared secret for encryption and is unrelated to X.509 certificates."
        ),
        "choices": [
            "Digital signature",
            "Asymmetric key",
            "Self-signed",
            "Symmetric key",
        ],
        "objectives": ["1.4", "3.10"],
    },
    {
        "slug": "ics-proprietary-controls-harsh-environment",
        "title": "Security+ — ICS (harsh environment)",
        "stem": (
            "Which of the following uses proprietary controls and is designed to function in harsh environments "
            "over many years with limited remote access management?"
        ),
        "name": "secplus_q299",
        "correct": "A",
        "explain": (
            "Correct. A — Industrial control systems (ICS) such as SCADA and PLCs often use proprietary protocols, "
            "operate for decades in harsh plant or utility environments, and limit remote management for safety and "
            "availability. Microservers are compact general-purpose servers, not industrial OT platforms. Containers "
            "package applications for portable deployment in cloud or DevOps environments. IoT devices are networked "
            "sensors and appliances and differ from large-scale industrial control infrastructure described in the stem."
        ),
        "choices": [
            "ICS",
            "Microservers",
            "Containers",
            "IoT",
        ],
        "objectives": ["3.2", "3.5"],
    },
    {
        "slug": "tabletop-generator-failure-bia-risk-management",
        "title": "Security+ — BIA (tabletop generator risk)",
        "stem": (
            "While conducting a business continuity tabletop exercise, the security team becomes concerned by "
            "potential impacts if a generator fails during failover. Which of the following is the team most likely "
            "to consider in regard to risk management activities?"
        ),
        "name": "secplus_q300",
        "correct": "C",
        "explain": (
            "Correct. C — A business impact analysis (BIA) identifies critical functions, dependencies such as power "
            "and generators, and the operational and financial impact if failover fails—exactly what a tabletop "
            "exercise explores. RPO defines acceptable data loss measured in time between backups. ARO is the "
            "estimated annual frequency of a threat event in quantitative risk analysis. MTTR is the average time "
            "to repair or restore a failed component, not the structured impact assessment that drives BCP."
        ),
        "choices": [
            "RPO",
            "ARO",
            "BIA",
            "MTTR",
        ],
        "objectives": ["3.6", "5.1"],
    },
    {
        "slug": "foreign-callers-company-numbers-weak-sip-security",
        "title": "Security+ — Weak SIP (unauthorized calls)",
        "stem": (
            "Callers speaking a foreign language are using company phone numbers to make unsolicited phone calls "
            "to a partner organization. A security analyst validates through phone system logs that the calls are "
            "occurring and the numbers are not being spoofed. Which of the following is the most likely explanation?"
        ),
        "name": "secplus_q301",
        "correct": "B",
        "explain": (
            "Correct. B — Weak SIP or PBX security allows unauthorized parties to place outbound calls through the "
            "company's trunk so caller ID shows legitimate company numbers without spoofing because the calls "
            "originate on the corporate phone system. Executives avoiding roaming charges would not produce "
            "unsolicited foreign-language campaigns to a partner. Disgruntled insiders are possible but the stem "
            "emphasizes external-style abuse of telephony infrastructure. Duplicate numbers assigned by a carrier "
            "would not show as authenticated outbound calls in the company's own phone logs."
        ),
        "choices": [
            "The executive team is traveling internationally and trying to avoid roaming charges",
            "The company's SIP server security settings are weak.",
            "Disgruntled employees are making calls to the partner organization.",
            "The service provider has assigned multiple companies the same numbers",
        ],
        "objectives": ["3.3", "4.4"],
    },
    {
        "slug": "attorney-copier-ldap-secure-print-prevention",
        "title": "Security+ — LDAP on printer (secure print)",
        "stem": (
            "An attorney prints confidential documents to a copier in an office space near multiple workstations and "
            "a reception desk. When the attorney goes to the copier to retrieve the documents, the documents are "
            "missing. Which of the following would best prevent this from reoccurring?"
        ),
        "name": "secplus_q302",
        "correct": "C",
        "explain": (
            "Correct. C — LDAP authentication on the printer enables secure pull printing so jobs are held until "
            "the attorney authenticates at the device, preventing others from taking output left in a public tray. "
            "Moving the copier to the legal department reduces exposure but does not stop unauthorized pickup in "
            "shared areas. DLP on the workstation controls digital exfiltration, not physical document theft at "
            "the printer. A physical penetration test evaluates controls but does not by itself prevent walk-up "
            "document loss."
        ),
        "choices": [
            "Place the copier in the legal department.",
            "Configure DLP on the attorney's workstation.",
            "Set up LDAP authentication on the printer.",
            "Conduct a physical penetration test.",
        ],
        "objectives": ["3.10", "4.5"],
    },
    {
        "slug": "raas-threat-actor-organized-crime-ciso-report",
        "title": "Security+ — Organized crime (RaaS)",
        "stem": (
            "A Chief Information Security Officer (CISO) wants to explicitly raise awareness about the increase of "
            "ransomware-as-a-service in a report to the management team. Which of the following best describes the "
            "threat actor in the CISO's report?"
        ),
        "name": "secplus_q303",
        "correct": "D",
        "explain": (
            "Correct. D — Ransomware-as-a-service (RaaS) is typically operated by organized crime groups that sell "
            "or lease ransomware kits to affiliates for financial gain. Insider threats are trusted users abusing "
            "internal access. Hacktivists pursue ideological or political goals rather than RaaS business models. "
            "Nation-state actors may use destructive malware but RaaS as a commercial affiliate service is most "
            "closely associated with cybercriminal enterprises."
        ),
        "choices": [
            "Insider threat",
            "Hacktivist",
            "Nation-state",
            "Organized crime",
        ],
        "objectives": ["2.4", "5.4"],
    },
    {
        "slug": "marketing-email-spf-next-dkim",
        "title": "Security+ — DKIM (after SPF)",
        "stem": (
            "A company wants to minimize the chance of its outgoing marketing emails getting flagged as spam. "
            "The company decides to list the email servers on the proper DNS record. Which of the following "
            "protocols should the company apply next?"
        ),
        "name": "secplus_q304",
        "correct": "C",
        "explain": (
            "Correct. C — Listing authorized senders in DNS is SPF; the typical next step is DKIM, which adds a "
            "cryptographic signature so receivers can verify message integrity and domain alignment. DMARC is "
            "usually implemented after SPF and DKIM to publish policy and reporting. DLP prevents unauthorized "
            "data movement and does not authenticate outbound email for deliverability."
        ),
        "choices": [
            "DMARC",
            "DLP",
            "DKIM",
            "SPF",
        ],
        "objectives": ["3.3", "4.1"],
    },
    {
        "slug": "quarantine-infected-system-air-gapped",
        "title": "Security+ — Air gap (quarantine infected system)",
        "stem": (
            "Which of the following activities should a systems administrator perform to quarantine a potentially "
            "infected system?"
        ),
        "name": "secplus_q305",
        "correct": "A",
        "explain": (
            "Correct. A — Moving the device to an air-gapped environment isolates it from corporate and internet "
            "networks so malware cannot spread while the system may still be analyzed. Disabling remote log-in "
            "through Group Policy limits one access path but does not fully isolate the host. Converting a "
            "production endpoint into a sandbox is not standard practice; sandboxes are separate analysis "
            "environments. Remote wipe through MDM eradicates data on mobile devices and is eradication, not "
            "quarantine for investigation."
        ),
        "choices": [
            "Move the device into an air-gapped environment.",
            "Disable remote log-in through Group Policy.",
            "Convert the device into a sandbox.",
            "Remote wipe the device using the MDM platform.",
        ],
        "objectives": ["4.8", "4.5"],
    },
    {
        "slug": "standardize-server-builds-infrastructure-as-code",
        "title": "Security+ — IaC (standardize server builds)",
        "stem": (
            "A company that has a large IT operation is looking to better control, standardize, and lower the time "
            "required to build new servers. Which of the following architectures will best achieve the company's "
            "objectives?"
        ),
        "name": "secplus_q306",
        "correct": "B",
        "explain": (
            "Correct. B — Infrastructure as code (IaC) defines servers and configuration in versioned templates "
            "so builds are repeatable, standardized, and fast to deploy. IoT refers to connected devices and "
            "sensors, not enterprise server provisioning. PaaS provides a cloud application platform and does not "
            "by itself standardize on-premises server build processes. ICS covers industrial control environments "
            "in operational technology, not general IT server construction."
        ),
        "choices": [
            "IoT",
            "IaC",
            "PaaS",
            "ICS",
        ],
        "objectives": ["3.1", "4.1"],
    },
    {
        "slug": "ciso-compliance-tracking-internal-auditing",
        "title": "Security+ — Internal auditing (compliance)",
        "stem": (
            "A Chief Information Security Officer would like to conduct frequent, detailed reviews of systems and "
            "procedures to track compliance objectives. Which of the following is the best method to achieve this "
            "objective?"
        ),
        "name": "secplus_q307",
        "correct": "C",
        "explain": (
            "Correct. C — Internal auditing provides ongoing, detailed evaluation of controls, systems, and "
            "procedures against compliance requirements. Third-party attestation offers periodic external assurance "
            "but is not the primary frequent internal tracking mechanism. Penetration testing finds exploitable "
            "weaknesses in a point-in-time technical exercise. Vulnerability scans identify known flaws and "
            "misconfigurations but do not comprehensively assess procedural compliance."
        ),
        "choices": [
            "Third-party attestation",
            "Penetration testing",
            "Internal auditing",
            "Vulnerability scans",
        ],
        "objectives": ["5.5", "5.6"],
    },
    {
        "slug": "unusual-dns-queries-non-business-hours-exfiltration",
        "title": "Security+ — DNS exfiltration (unusual queries)",
        "stem": (
            "A security analyst receives alerts about an internal system sending a large amount of unusual DNS "
            "queries to systems on the internet over short periods of time during non-business hours. Which of the "
            "following is most likely occurring?"
        ),
        "name": "secplus_q308",
        "correct": "B",
        "explain": (
            "Correct. B — High volumes of abnormal outbound DNS queries, especially off-hours, often indicate "
            "DNS tunneling used to exfiltrate data past filters that allow DNS. Worms typically spread via "
            "exploits or shares rather than sustained unusual DNS to external hosts. Logic bombs trigger "
            "destructive actions on a schedule and do not match bulk DNS query patterns. Ransomware focuses "
            "on encrypting local files and may use other C2 channels; the stem specifically points to DNS "
            "query volume as the indicator."
        ),
        "choices": [
            "A worm is propagating across the network.",
            "Data is being exfiltrated.",
            "A logic bomb is deleting data.",
            "Ransomware is encrypting files.",
        ],
        "objectives": ["4.4", "4.9"],
    },
    {
        "slug": "siem-automation-orchestration-workforce-multiplier",
        "title": "Security+ — Workforce multiplier (SIEM automation)",
        "stem": (
            "A security engineer would like to enhance the use of automation and orchestration within the SIEM. "
            "Which of the following would be the primary benefit of this enhancement?"
        ),
        "name": "secplus_q309",
        "correct": "D",
        "explain": (
            "Correct. D — Automation and orchestration in a SIEM (often through SOAR integration) multiply analyst "
            "capacity by running repetitive enrichment and response steps at machine speed. Increased complexity "
            "is a potential drawback, not the primary benefit. Removing technical debt is a development or "
            "architecture goal, not the main outcome of SIEM orchestration. Guard rails are policy controls; "
            "automation may enforce them but the chief value is scaling human effectiveness."
        ),
        "choices": [
            "It increases complexity.",
            "It removes technical debt.",
            "It adds additional guard rails.",
            "It acts as a workforce multiplier.",
        ],
        "objectives": ["4.7", "4.9"],
    },
    {
        "slug": "tokenization-strategy-surrogate-values",
        "title": "Security+ — Tokenization (surrogate values)",
        "stem": (
            "Which of the following is an example of a data protection strategy that uses tokenization?"
        ),
        "name": "secplus_q310",
        "correct": "B",
        "explain": (
            "Correct. B — Tokenization replaces sensitive data elements with non-sensitive surrogate tokens while "
            "the original values are stored securely in a vault for authorized lookup. Encrypting databases "
            "protects confidentiality at rest but does not substitute tokens for data fields. Removing sensitive "
            "data from production is data minimization or masking, not tokenization. Hashing is one-way and "
            "cannot return the original value through a token mapping."
        ),
        "choices": [
            "Encrypting databases containing sensitive data",
            "Replacing sensitive data with surrogate values",
            "Removing sensitive data from production systems",
            "Hashing sensitive data in critical systems",
        ],
        "objectives": ["1.4", "3.10"],
    },
    {
        "slug": "unencrypted-plc-management-traffic-scada",
        "title": "Security+ — SCADA (unencrypted PLC traffic)",
        "stem": (
            "In which of the following will unencrypted PLC management traffic most likely be found?"
        ),
        "name": "secplus_q311",
        "correct": "D",
        "explain": (
            "Correct. D — SCADA and other industrial control environments often use legacy programmable logic "
            "controllers (PLCs) with unencrypted management and field protocols. Software-defined networking "
            "abstracts enterprise data-plane control and is not the OT PLC domain. IoT is a broad category of "
            "connected devices and does not specifically describe industrial PLC backplanes. VPNs encrypt "
            "traffic in tunnels and are used to protect remote access, not as the typical source of cleartext "
            "PLC management on plant floors."
        ),
        "choices": [
            "SDN",
            "IoT",
            "VPN",
            "SCADA",
        ],
        "objectives": ["3.2", "3.5"],
    },
    {
        "slug": "dr-site-geographic-dispersion-natural-disaster-backups",
        "title": "Security+ — Geographic dispersion (DR backups)",
        "stem": (
            "A company is planning a disaster recovery site and needs to ensure that a single natural disaster "
            "would not result in the complete loss of regulated backup data. Which of the following should the "
            "company consider?"
        ),
        "name": "secplus_q312",
        "correct": "A",
        "explain": (
            "Correct. A — Geographic dispersion places backup and recovery sites in separate regions so one "
            "natural disaster cannot destroy primary and regulated backup data together. Platform diversity uses "
            "different technologies for resilience but does not address regional catastrophe. A hot site speeds "
            "recovery but must still be geographically separated to survive the same event. Load balancing "
            "distributes traffic across nodes for availability, not protection from a single regional disaster."
        ),
        "choices": [
            "Geographic dispersion",
            "Platform diversity",
            "Hot site",
            "Load balancing",
        ],
        "objectives": ["3.4", "3.6"],
    },
    {
        "slug": "sideloading-unapproved-software-repository",
        "title": "Security+ — Side loading (unapproved repo)",
        "stem": (
            "Which of the following vulnerabilities is associated with installing software outside of a "
            "manufacturer's approved software repository?"
        ),
        "name": "secplus_q313",
        "correct": "D",
        "explain": (
            "Correct. D — Side loading installs applications from sources other than the manufacturer's "
            "official app store or repository, bypassing vetting and increasing malware risk. Jailbreaking "
            "removes OS restrictions on mobile devices and may enable side loading but is not the same as "
            "installing from an unapproved repository. Memory injection inserts code into a running process. "
            "Resource reuse involves reusing system resources insecurely, such as predictable identifiers, "
            "not unofficial software installation."
        ),
        "choices": [
            "Jailbreaking",
            "Memory injection",
            "Resource reuse",
            "Side loading",
        ],
        "objectives": ["2.3", "3.3"],
    },
    {
        "slug": "remote-work-no-vpn-secure-web-gateway",
        "title": "Security+ — SWG (remote without VPN)",
        "stem": (
            "A company recently decided to allow employees to work remotely. The company wants to protect user "
            "data without using a VPN. Which of the following technologies should the company implement?"
        ),
        "name": "secplus_q314",
        "correct": "A",
        "explain": (
            "Correct. A — A secure web gateway (SWG) provides cloud-delivered web and internet traffic filtering "
            "and policy enforcement for remote users without routing all traffic through a corporate VPN. A "
            "virtual private cloud endpoint connects privately to cloud services and does not secure general "
            "remote employee internet use. Deep packet inspection is an analysis technique used inside firewalls "
            "and IDS, not a standalone remote-access protection service. A next-generation firewall primarily "
            "protects the network perimeter and does not by itself secure off-network remote users without VPN "
            "or similar remote access."
        ),
        "choices": [
            "Secure web gateway",
            "Virtual private cloud end point",
            "Deep packet inspection",
            "Next-generation firewall",
        ],
        "objectives": ["3.3", "4.5"],
    },
    {
        "slug": "bank-pii-server-file-integrity-monitoring",
        "title": "Security+ — FIM (PII not modified)",
        "stem": (
            "A bank set up a new server that contains customers' PII. Which of the following should the bank use "
            "to make sure the sensitive data is not modified?"
        ),
        "name": "secplus_q315",
        "correct": "C",
        "explain": (
            "Correct. C — File integrity monitoring (FIM) detects unauthorized changes to files and critical "
            "system objects so the bank can alert on modification of sensitive data. Full disk encryption "
            "protects confidentiality if media is lost or stolen but does not detect in-place tampering. "
            "Network access control admits or blocks endpoints on the network and does not monitor file "
            "changes on the server. User behavior analytics flags anomalous user activity patterns rather than "
            "integrity of specific files containing PII."
        ),
        "choices": [
            "Full disk encryption",
            "Network access control",
            "File integrity monitoring",
            "User behavior analytics",
        ],
        "objectives": ["3.10", "4.4"],
    },
    {
        "slug": "data-modified-in-transit-hashing-integrity",
        "title": "Security+ — Hashing (integrity in transit)",
        "stem": (
            "Which of the following techniques would identify whether data has been modified in transit?"
        ),
        "name": "secplus_q316",
        "correct": "A",
        "explain": (
            "Correct. A — Hashing (or HMAC and signatures built on hashes) produces a digest that changes if "
            "data is altered in transit, allowing integrity verification at the receiver. Tokenization replaces "
            "sensitive values with surrogates for storage or processing. Masking obscures data for display or "
            "testing. Encryption primarily protects confidentiality; integrity in transit is commonly verified "
            "with hashes or authenticated modes rather than encryption alone."
        ),
        "choices": [
            "Hashing",
            "Tokenization",
            "Masking",
            "Encryption",
        ],
        "objectives": ["1.4", "3.10"],
    },
    {
        "slug": "traveling-employees-endpoint-hips-protection",
        "title": "Security+ — HIPS (traveling employees)",
        "stem": (
            "A systems administrator needs to provide traveling employees with a tool that will protect company "
            "devices regardless of where they are working. Which of the following should the administrator implement?"
        ),
        "name": "secplus_q317",
        "correct": "D",
        "explain": (
            "Correct. D — A host-based intrusion prevention system (HIPS) runs on the endpoint and can detect "
            "and block malicious activity wherever the device connects. Isolation quarantines systems after "
            "compromise and is not continuous protection for mobile workers. Segmentation divides network zones "
            "at the infrastructure layer and does not travel with laptops off-site. Access control lists on "
            "firewalls or routers enforce policy at network boundaries and do not protect devices on untrusted "
            "networks away from corporate controls."
        ),
        "choices": [
            "Isolation",
            "Segmentation",
            "ACL",
            "HIPS",
        ],
        "objectives": ["4.5", "3.3"],
    },
    {
        "slug": "new-tactic-no-siem-alerts-threat-hunting",
        "title": "Security+ — Threat hunting (new TTP)",
        "stem": (
            "A cyber operations team informs a security analyst about a new tactic malicious actors are using to "
            "compromise networks. SIEM alerts have not yet been configured. Which of the following best describes "
            "what the security analyst should do to identify this behavior?"
        ),
        "name": "secplus_q318",
        "correct": "D",
        "explain": (
            "Correct. D — Threat hunting is proactive investigation for indicators of new tactics when automated "
            "alerts are not yet in place. Digital forensics preserves and analyzes evidence after an incident is "
            "suspected or confirmed. E-discovery locates electronically stored information for legal proceedings. "
            "Incident response is the broader process of handling security events after detection, not the "
            "proactive search for unknown behavior before alerts exist."
        ),
        "choices": [
            "Digital forensics",
            "E-discovery",
            "Incident response",
            "Threat hunting",
        ],
        "objectives": ["4.9", "5.2"],
    },
    {
        "slug": "foreign-government-hires-organized-crime-critical-systems",
        "title": "Security+ — Organized crime (state-hired)",
        "stem": (
            "Which of the following threat actors is the most likely to be hired by a foreign government to attack "
            "critical systems located in other countries?"
        ),
        "name": "secplus_q319",
        "correct": "C",
        "explain": (
            "Correct. C — Organized crime groups are frequently used as proxies or contractors for financially "
            "motivated or destructive operations against foreign critical infrastructure while providing "
            "plausible deniability for the sponsoring government. Hacktivists act on ideology rather than as "
            "typical government contractors. Whistleblowers disclose information from inside an organization. "
            "Unskilled attackers lack the capability to conduct sustained attacks on critical systems abroad."
        ),
        "choices": [
            "Hacktivist",
            "Whistleblower",
            "Organized crime",
            "Unskilled attacker",
        ],
        "objectives": ["2.4", "5.4"],
    },
    {
        "slug": "vulnerability-prioritization-focus-cvss",
        "title": "Security+ — CVSS (vuln prioritization)",
        "stem": (
            "Which of the following should an organization focus on the most when making decisions about "
            "vulnerability prioritization?"
        ),
        "name": "secplus_q320",
        "correct": "B",
        "explain": (
            "Correct. B — CVSS provides a standardized severity score so teams can rank which vulnerabilities "
            "to remediate first, often combined with asset criticality and exposure. Exposure factor is used "
            "in quantitative risk calculations such as SLE and ALE, not as the primary vuln-scoring framework. "
            "CVE is an identifier catalog for known vulnerabilities, not a prioritization score. Industry impact "
            "is contextual but not the standard metric CompTIA cites for ordering remediation work."
        ),
        "choices": [
            "Exposure factor",
            "CVSS",
            "CVE",
            "Industry impact",
        ],
        "objectives": ["4.3", "5.3"],
    },
    {
        "slug": "guest-quarantine-mdm-compliance-attestation",
        "title": "Security+ — Compliance attestation (MDM)",
        "stem": (
            "An administrator has configured a quarantine subnet for all guest devices that connect to the network. "
            "Which of the following would be best for the security team to configure on the MDM before allowing "
            "access to corporate resources?"
        ),
        "name": "secplus_q321",
        "correct": "B",
        "explain": (
            "Correct. B — Compliance attestation on MDM verifies the device meets security requirements such as "
            "encryption, OS version, and passcode policy before granting access to corporate resources. Device "
            "fingerprinting identifies device characteristics for analytics but does not enforce posture. NAC "
            "controls network admission at the infrastructure layer and is not an MDM configuration. 802.1X "
            "authenticates endpoints on wired or wireless ports and is typically implemented on network devices, "
            "not as the primary MDM gate before corporate access."
        ),
        "choices": [
            "Device fingerprinting",
            "Compliance attestation",
            "NAC",
            "802.1X",
        ],
        "objectives": ["4.6", "3.8"],
    },
    {
        "slug": "network-auth-8021x-certificate-nac-quarantine",
        "title": "Security+ — 802.1X (cert + NAC posture)",
        "stem": (
            "A systems administrator is redesigning how devices will perform network authentication. The following "
            "requirements need to be met:\n\n"
            "• An existing internal certificate must be used.\n"
            "• Wired and wireless networks must be supported.\n"
            "• Any unapproved device should be isolated in a quarantine subnet.\n"
            "• Approved devices should be updated before accessing resources.\n\n"
            "Which of the following would best meet the requirements?"
        ),
        "name": "secplus_q322",
        "correct": "A",
        "explain": (
            "Correct. A — 802.1X port-based access control supports wired and wireless authentication with "
            "certificates (for example EAP-TLS) and integrates with NAC for quarantine VLANs and posture "
            "remediation before full access. EAP is an authentication framework carried inside 802.1X, not the "
            "overall solution by itself. RADIUS is the backend authentication server 802.1X often uses but does "
            "not define quarantine or update enforcement. WPA2 secures wireless links and does not cover wired "
            "access, certificate-based admission, or quarantine posture workflows."
        ),
        "choices": [
            "802.1X",
            "EAP",
            "RADIUS",
            "WPA2",
        ],
        "objectives": ["4.1", "4.6"],
    },
    {
        "slug": "file-integrity-confirmation-hashing-strategy",
        "title": "Security+ — Hashing (file integrity)",
        "stem": (
            "Which of the following data protection strategies can be used to confirm file integrity?"
        ),
        "name": "secplus_q323",
        "correct": "C",
        "explain": (
            "Correct. C — Hashing produces a fixed digest of a file; comparing hashes at different times confirms "
            "whether the file changed. Masking obscures sensitive values for display or testing. Encryption "
            "protects confidentiality and does not by itself prove the file is unchanged. Obfuscation hides code "
            "or logic readability and is not an integrity verification method."
        ),
        "choices": [
            "Masking",
            "Encryption",
            "Hashing",
            "Obfuscation",
        ],
        "objectives": ["1.4", "3.10"],
    },
    {
        "slug": "operational-changes-scheduled-downtime-window",
        "title": "Security+ — Scheduled downtime",
        "stem": (
            "Which of the following best practices gives administrators a set period to perform changes to an "
            "operational system to ensure availability and minimize business impacts?"
        ),
        "name": "secplus_q324",
        "correct": "B",
        "explain": (
            "Correct. B — Scheduled downtime defines an approved maintenance window when changes occur so "
            "stakeholders expect reduced availability and impact is controlled. Impact analysis evaluates "
            "potential effects before a change but does not allocate the change window itself. A backout plan "
            "describes how to roll back if a change fails. Change management boards review and approve changes "
            "but the set maintenance period is established through scheduled downtime planning."
        ),
        "choices": [
            "Impact analysis",
            "Scheduled downtime",
            "Backout plan",
            "Change management boards",
        ],
        "objectives": ["1.3", "5.2"],
    },
    {
        "slug": "bia-process-estimate-system-recovery-time",
        "title": "Security+ — BIA (recovery time estimate)",
        "stem": "Which of the following tasks is typically included in the BIA process?",
        "name": "secplus_q325",
        "correct": "A",
        "explain": (
            "Correct. A — A business impact analysis (BIA) identifies critical functions and estimates recovery "
            "time requirements such as RTO and maximum tolerable downtime for systems and processes. "
            "Communication strategy is developed in incident response and crisis communications planning. "
            "Evaluating the overall risk management plan is a separate governance activity. Backup and recovery "
            "procedures are implemented in disaster recovery planning after BIA informs priorities. The "
            "incident response plan is its own document, though BIA results support IR and BCP."
        ),
        "choices": [
            "Estimating the recovery time of systems",
            "Identifying the communication strategy",
            "Evaluating the risk management plan",
            "Establishing the backup and recovery procedures",
            "Developing the incident response plan",
        ],
        "objectives": ["3.6", "5.1"],
    },
    {
        "slug": "saas-purchase-review-third-party-audit",
        "title": "Security+ — Third-party audit (SaaS purchase)",
        "stem": (
            "A security analyst is reviewing the security of a SaaS application that the company intends to purchase. "
            "Which of the following documentations should the security analyst request from the SaaS application "
            "vendor?"
        ),
        "name": "secplus_q326",
        "correct": "B",
        "explain": (
            "Correct. B — A third-party audit report (for example SOC 2 or ISO 27001) provides independent "
            "assurance that the vendor's security controls are designed and operating effectively. A service-level "
            "agreement defines availability and support commitments, not detailed security attestation. A "
            "statement of work scopes a specific project engagement. A data privacy agreement governs personal "
            "data handling and may be required separately but does not replace independent security assurance "
            "for vendor due diligence."
        ),
        "choices": [
            "Service-level agreement",
            "Third-party audit",
            "Statement of work",
            "Data privacy agreement",
        ],
        "objectives": ["5.5", "5.6"],
    },
    {
        "slug": "osint-social-engineering-testing-activity",
        "title": "Security+ — OSINT (social engineering test)",
        "stem": "Which of the following activities uses OSINT?",
        "name": "secplus_q327",
        "correct": "A",
        "explain": (
            "Correct. A — Open source intelligence (OSINT) gathers publicly available information such as social "
            "media, websites, and job postings to craft believable social engineering tests. Analyzing internal "
            "security logs is operational monitoring, not OSINT. Collecting evidence of malicious activity is "
            "forensics or incident response on organizational data. Producing indicators of compromise comes "
            "from malware or threat analysis, not primarily from public-source reconnaissance."
        ),
        "choices": [
            "Social engineering testing",
            "Data analysis of logs",
            "Collecting evidence of malicious activity",
            "Producing IOC for malicious artifacts",
        ],
        "objectives": ["4.9", "2.1"],
    },
    {
        "slug": "firewall-fail-open-availability-priority-website",
        "title": "Security+ — Fail-open (availability priority)",
        "stem": (
            "An organization designs an inbound firewall with a fail-open configuration while implementing a "
            "website. Which of the following does the organization consider to be the highest priority?"
        ),
        "name": "secplus_q328",
        "correct": "C",
        "explain": (
            "Correct. C — Fail-open allows traffic through if the firewall fails, prioritizing availability so "
            "the website remains reachable. Fail-closed would block traffic on failure and favors confidentiality "
            "or security over uptime. Non-repudiation proves actions cannot be denied. Integrity ensures data "
            "is not altered without authorization."
        ),
        "choices": [
            "Confidentiality",
            "Non-repudiation",
            "Availability",
            "Integrity",
        ],
        "objectives": ["1.2", "3.1"],
    },
    {
        "slug": "aup-preventive-security-control-type",
        "title": "Security+ — AUP (preventive control)",
        "stem": (
            "Which of the following security control types does an acceptable use policy best represent?"
        ),
        "name": "secplus_q329",
        "correct": "D",
        "explain": (
            "Correct. D — An acceptable use policy (AUP) is a preventive control because it defines permitted "
            "behavior upfront to stop misuse before it occurs. Detective controls identify events after they "
            "happen, such as log review or IDS alerts. Compensating controls substitute when a primary control "
            "cannot fully address risk. Corrective controls remediate issues after an incident, such as "
            "restoring systems or applying patches."
        ),
        "choices": [
            "Detective",
            "Compensating",
            "Corrective",
            "Preventive",
        ],
        "objectives": ["1.2", "5.5"],
    },
    {
        "slug": "xss-insert-scripts-control-client-browser",
        "title": "Security+ — XSS (client browser)",
        "stem": (
            "Which of the following is a type of vulnerability that involves inserting scripts into web-based "
            "applications in order to take control of the client's web browser?"
        ),
        "name": "secplus_q330",
        "correct": "B",
        "explain": (
            "Correct. B — Cross-site scripting (XSS) injects malicious scripts into web content executed in the "
            "victim's browser. SQL injection manipulates backend database queries through untrusted input. A "
            "zero-day exploit uses an unknown vulnerability but is not defined by script injection in browsers. "
            "An on-path attack intercepts or alters communications between parties in transit."
        ),
        "choices": [
            "SQL injection",
            "Cross-site scripting",
            "Zero-day exploit",
            "On-path attack",
        ],
        "objectives": ["2.3", "2.5"],
    },
    {
        "slug": "low-cost-cloud-app-hosting-serverless",
        "title": "Security+ — Serverless (cloud hosting)",
        "stem": (
            "A systems administrator is looking for a low-cost application-hosting solution that is cloud-based. "
            "Which of the following meets these requirements?"
        ),
        "name": "secplus_q331",
        "correct": "A",
        "explain": (
            "Correct. A — Serverless frameworks run application code in the cloud on a pay-per-use model without "
            "managing servers, which is a common low-cost hosting approach. A Type 1 hypervisor virtualizes "
            "workloads on bare-metal hosts and is typically on-premises infrastructure, not cloud app hosting. "
            "SD-WAN optimizes wide-area network connectivity between sites. SDN separates network control "
            "from the data plane and does not provide application hosting."
        ),
        "choices": [
            "Serverless framework",
            "Type 1 hypervisor",
            "SD-WAN",
            "SDN",
        ],
        "objectives": ["3.1", "3.4"],
    },
    {
        "slug": "saas-firewall-ports-supply-chain-vendor-risk",
        "title": "Security+ — Supply chain (SaaS deployment)",
        "stem": (
            "A technician is opening ports on a firewall for a new system being deployed and supported by a SaaS "
            "provider. Which of the following is a risk in the new system?"
        ),
        "name": "secplus_q332",
        "correct": "C",
        "explain": (
            "Correct. C — A system deployed and maintained by an external SaaS provider introduces supply chain "
            "vendor risk because the organization depends on the vendor's security and access practices. "
            "Default credentials are a generic hardening issue not specific to SaaS-supported deployments. "
            "A non-segmented network is an architecture concern but the stem emphasizes third-party support. "
            "Vulnerable software is a broad risk; supply chain vendor risk captures reliance on the external "
            "provider opening and supporting the integration."
        ),
        "choices": [
            "Default credentials",
            "Non-segmented network",
            "Supply chain vendor",
            "Vulnerable software",
        ],
        "objectives": ["5.1", "5.5"],
    },
    {
        "slug": "daily-server-security-settings-automation-check",
        "title": "Security+ — Automation (daily settings check)",
        "stem": (
            "Which of the following is the best way to consistently determine on a daily basis whether security "
            "settings on servers have been modified?"
        ),
        "name": "secplus_q333",
        "correct": "A",
        "explain": (
            "Correct. A — Automation such as configuration management, file integrity monitoring, and "
            "scheduled compliance scans can check server security settings daily at scale with consistent "
            "results. A compliance checklist supports periodic reviews but relies on manual execution. "
            "Attestation is formal assurance from an auditor, not a daily operational control. A manual audit "
            "does not scale for consistent daily verification across many servers."
        ),
        "choices": [
            "Automation",
            "Compliance checklist",
            "Attestation",
            "Manual audit",
        ],
        "objectives": ["4.7", "4.1"],
    },
    {
        "slug": "track-vm-build-code-version-control",
        "title": "Security+ — Version control (VM build code)",
        "stem": (
            "A company wants to track modifications to the code used to build new virtual servers. Which of the "
            "following will the company most likely deploy?"
        ),
        "name": "secplus_q334",
        "correct": "D",
        "explain": (
            "Correct. D — A version control tool such as Git records who changed build scripts or infrastructure-"
            "as-code and when, with full revision history. A change management ticketing system tracks approval "
            "and workflow for changes but does not version source files. A behavioral analyzer monitors user "
            "activity patterns for anomalies. A collaboration platform supports communication and documents but "
            "is not the primary system for tracking code modifications."
        ),
        "choices": [
            "Change management ticketing system",
            "Behavioral analyzer",
            "Collaboration platform",
            "Version control tool",
        ],
        "objectives": ["3.1", "4.1"],
    },
    {
        "slug": "compromising-photos-blackmail-threat-intent",
        "title": "Security+ — Blackmail (threat intent)",
        "stem": (
            "A government official receives a blank envelope containing photos and a note instructing the official "
            "to wire a large sum of money by midnight to prevent the photos from being leaked on the Internet. "
            "Which of the following best describes the threat actor's intent?"
        ),
        "name": "secplus_q335",
        "correct": "D",
        "explain": (
            "Correct. D — Blackmail coerces payment by threatening to expose damaging material if demands are not "
            "met. Organized crime describes a category of criminal enterprise, not the specific intent in this "
            "scenario. Philosophical beliefs motivate hacktivists or ideologically driven actors. Espionage "
            "seeks intelligence or secrets for strategic advantage rather than payment to suppress photos."
        ),
        "choices": [
            "Organized crime",
            "Philosophical beliefs",
            "Espionage",
            "Blackmail",
        ],
        "objectives": ["2.1", "2.4"],
    },
    {
        "slug": "router-mgmt-ip-restrict-preventive-control",
        "title": "Security+ — Preventive (router mgmt ACL)",
        "stem": (
            "Which of the following control types involves restricting IP connectivity to a router's web "
            "management interface to protect it from being exploited by a vulnerability?"
        ),
        "name": "secplus_q336",
        "correct": "C",
        "explain": (
            "Correct. C — Restricting which IP addresses can reach the management interface is a preventive "
            "technical control that blocks exploitation attempts before they succeed. Corrective controls "
            "respond after an incident such as patching or restoring systems. Physical controls protect "
            "facilities and hardware access. Managerial controls are policies and governance documents rather "
            "than network-layer access restrictions."
        ),
        "choices": [
            "Corrective",
            "Physical",
            "Preventive",
            "Managerial",
        ],
        "objectives": ["1.2", "4.1"],
    },
    {
        "slug": "legacy-iot-vulnerability-segmentation-mitigate",
        "title": "Security+ — Segmentation (legacy IoT)",
        "stem": (
            "A newly identified network access vulnerability has been found in the OS of legacy IoT devices. "
            "Which of the following would best mitigate this vulnerability quickly?"
        ),
        "name": "secplus_q337",
        "correct": "C",
        "explain": (
            "Correct. C — Network segmentation isolates legacy IoT devices so a vulnerability cannot easily reach "
            "other systems, and it can be implemented quickly when patching is slow or unavailable. Insurance "
            "transfers financial risk but does not reduce technical exposure. Patching is preferred when updates "
            "exist but legacy IoT often lacks timely vendor fixes. Replacement is a long-term strategy, not the "
            "fastest mitigation."
        ),
        "choices": [
            "Insurance",
            "Patching",
            "Segmentation",
            "Replacement",
        ],
        "objectives": ["3.3", "4.1"],
    },
    {
        "slug": "login-rejected-spring2023-password-spraying",
        "title": "Security+ — Password spraying (login log)",
        "stem": "",
        "name": "secplus_q338",
        "correct": "A",
        "explain": (
            "Correct. A — Password spraying tries one or a few passwords against many accounts; the log shows "
            "the same password (Spring2023) used for administrator, jsmith, guest, cpolk, and fmartin within "
            "seconds, each rejected. Account forgery creates fake accounts rather than guessing credentials. "
            "Pass-the-hash reuses captured password hashes, not repeated plaintext attempts across users. "
            "Brute-force hammers many passwords against one account, not one password against many accounts."
        ),
        "choices": [
            "Password spraying",
            "Account forgery",
            "Pass-the-hash",
            "Brute-force",
        ],
        "prepend_html": build_login_rejected_spring2023_spraying_exhibit(),
        "objectives": ["2.4", "4.9"],
    },
    {
        "slug": "employees-frequent-site-watering-hole-attack",
        "title": "Security+ — Watering hole (frequented site)",
        "stem": (
            "Which of the following security threats aims to compromise a website that multiple employees "
            "frequently visit?"
        ),
        "name": "secplus_q339",
        "correct": "C",
        "explain": (
            "Correct. C — A watering hole attack poisons a site the target organization is likely to visit so "
            "malware can reach many employees. Supply chain risk comes through vendors or third-party products. "
            "Typosquatting uses look-alike domain names from user typing errors. Impersonation pretends to be "
            "a trusted person or system rather than compromising a commonly visited website."
        ),
        "choices": [
            "Supply chain",
            "Typosquatting",
            "Watering hole",
            "Impersonation",
        ],
        "objectives": ["2.2", "2.4"],
    },
    {
        "slug": "avoid-bloatware-application-allow-list",
        "title": "Security+ — Application allow list (bloatware)",
        "stem": (
            "Which of the following mitigation techniques would a security analyst most likely use to avoid "
            "bloatware on devices?"
        ),
        "name": "secplus_q340",
        "correct": "B",
        "explain": (
            "Correct. B — An application allow list permits only approved software to install or run, blocking "
            "unwanted preinstalled or third-party bloatware. Disabling unused ports and protocols reduces "
            "network exposure but does not control installed applications. Changing default passwords addresses "
            "credential risk, not unnecessary software. Access control permissions govern user rights to "
            "resources but do not prevent unauthorized applications from executing."
        ),
        "choices": [
            "Disabled ports/protocols",
            "Application allow list",
            "Default password changes",
            "Access control permissions",
        ],
        "objectives": ["3.3", "4.1"],
    },
    {
        "slug": "log-script-tag-xss-vulnerability",
        "title": "Security+ — XSS (script in logs)",
        "stem": "",
        "name": "secplus_q341",
        "correct": "A",
        "explain": (
            "Correct. A — Injected script tags such as <script>function(send_info)</script> in application "
            "input or logs indicate cross-site scripting (XSS). SQL injection manipulates database queries "
            "with SQL syntax. DDoS overwhelms availability with traffic volume. CSRF tricks an authenticated "
            "user's browser into submitting unwanted requests and does not rely on injected script tags."
        ),
        "choices": [
            "XSS",
            "SQLi",
            "DDoS",
            "CSRF",
        ],
        "prepend_html": build_xss_script_tag_log_exhibit(),
        "objectives": ["2.3", "2.5"],
    },
    {
        "slug": "internal-endpoint-connections-host-based-firewall",
        "title": "Security+ — Host-based firewall (internal traffic)",
        "stem": (
            "A systems administrator set up a perimeter firewall but continues to notice suspicious connections "
            "between internal endpoints. Which of the following should be set up in order to mitigate the threat "
            "posed by the suspicious activity?"
        ),
        "name": "secplus_q342",
        "correct": "A",
        "explain": (
            "Correct. A — A host-based firewall on each endpoint can filter east-west traffic between internal "
            "systems when a perimeter firewall only controls north-south flow. A web application firewall "
            "protects HTTP applications at the edge, not general internal host-to-host connections. An access "
            "control list on a perimeter device does not inspect traffic that stays inside the LAN. An "
            "application allow list controls which programs run, not network connections between endpoints."
        ),
        "choices": [
            "Host-based firewall",
            "Web application firewall",
            "Access control list",
            "Application allow list",
        ],
        "objectives": ["4.5", "3.3"],
    },
    {
        "slug": "critical-patch-asset-inventory-systems",
        "title": "Security+ — Asset inventory (patch rollout)",
        "stem": (
            "An important patch for a critical application has just been released, and a systems administrator is "
            "identifying all of the systems requiring the patch. Which of the following must be maintained in order "
            "to ensure that all systems requiring the patch are updated?"
        ),
        "name": "secplus_q343",
        "correct": "A",
        "explain": (
            "Correct. A — An accurate asset inventory lists hardware, software, and versions so administrators "
            "can find every system running the affected application and confirm patching coverage. Network "
            "enumeration discovers live hosts at a point in time but is not the maintained record of "
            "authorized assets and installed software. Data certification attests to data quality or compliance "
            "and does not track which endpoints need updates. The procurement process governs acquisition, not "
            "ongoing visibility into deployed systems."
        ),
        "choices": [
            "Asset inventory",
            "Network enumeration",
            "Data certification",
            "Procurement process",
        ],
        "objectives": ["4.2", "4.5"],
    },
    {
        "slug": "incident-response-first-stage-detection",
        "title": "Security+ — IR first stage (detection)",
        "stem": (
            "Which of the following activities is the first stage in the incident response process?"
        ),
        "name": "secplus_q344",
        "correct": "A",
        "explain": (
            "Correct. A — Detection is the first operational stage once monitoring and preparation are in "
            "place: recognizing that an event may be a security incident. Declaration is not a standard "
            "CompTIA incident response phase name. Containment follows detection and analysis to limit "
            "damage. Vacation is not part of the incident response lifecycle."
        ),
        "choices": [
            "Detection",
            "Declaration",
            "Containment",
            "Vacation",
        ],
        "objectives": ["5.5"],
    },
    {
        "slug": "decommissioned-laptops-data-wiping",
        "title": "Security+ — Wiping (decommissioned laptops)",
        "stem": (
            "A company is concerned about the theft of client data from decommissioned laptops. Which of the "
            "following is the most cost-effective method to decrease this risk?"
        ),
        "name": "secplus_q345",
        "correct": "A",
        "explain": (
            "Correct. A — Secure wiping (sanitization) overwrites or cryptographically erases data so it cannot "
            "be recovered from drives before laptops are reused or disposed of, at lower cost than physical "
            "destruction. Recycling addresses environmental disposal but does not by itself remove recoverable "
            "data. Shredding or crushing media is highly effective but expensive and usually reserved for the "
            "highest sensitivity. Simple deletion leaves recoverable remnants and does not adequately protect "
            "client data."
        ),
        "choices": [
            "Wiping",
            "Recycling",
            "Shredding",
            "Deletion",
        ],
        "objectives": ["3.2", "5.5"],
    },
    {
        "slug": "detect-fraud-job-rotation-different-roles",
        "title": "Security+ — Job rotation (fraud detection)",
        "stem": (
            "Which of the following is best used to detect fraud by assigning employees to different roles?"
        ),
        "name": "secplus_q346",
        "correct": "D",
        "explain": (
            "Correct. D — Job rotation moves staff through different roles so a successor may uncover "
            "irregularities or concealed activity left by the prior occupant. Least privilege limits access "
            "to what is needed and is preventive, not a detective fraud control tied to role changes. "
            "Mandatory vacation requires time away so another employee can review work; it detects fraud "
            "through absence, not by rotating roles. Separation of duties splits conflicting tasks among "
            "people at the same time to prevent one person from completing a fraudulent transaction alone."
        ),
        "choices": [
            "Least privilege",
            "Mandatory vacation",
            "Separation of duties",
            "Job rotation",
        ],
        "objectives": ["5.4", "1.1"],
    },
    {
        "slug": "encrypted-outbound-endpoint-logs-investigation",
        "title": "Security+ — Endpoint logs (encrypted outbound)",
        "stem": (
            "A security analyst investigates abnormal outbound traffic from a corporate endpoint. The traffic is "
            "encrypted and uses non-standard ports. Which of the following data sources should the analyst use "
            "first to confirm whether this traffic is malicious?"
        ),
        "name": "secplus_q347",
        "correct": "C",
        "explain": (
            "Correct. C — Endpoint logs tie outbound connections to the process, user, and command-line activity "
            "on the host, which is the fastest way to confirm malicious behavior when payloads are encrypted. "
            "Application logs cover only specific programs and may miss malware running outside those apps. "
            "Vulnerability scans find weaknesses proactively and do not validate live suspicious sessions. "
            "Packet captures show headers and timing but encrypted payloads often cannot be inspected without "
            "keys, so PCAP alone is slower for confirming malware on the originating endpoint."
        ),
        "choices": [
            "Application logs",
            "Vulnerability scans",
            "Endpoint logs",
            "Packet captures",
        ],
        "objectives": ["4.9", "4.4"],
    },
    {
        "slug": "billing-system-fraudulent-checks-application-logs",
        "title": "Security+ — Application logs (billing fraud)",
        "stem": (
            "An employee used a company's billing system to issue fraudulent checks. The administrator is "
            "looking for evidence of other occurrences of this activity. Which of the following should the "
            "administrator examine?"
        ),
        "name": "secplus_q348",
        "correct": "A",
        "explain": (
            "Correct. A — Application logs from the billing system record user actions such as check creation, "
            "approval, and modification, which is where prior fraudulent issuances would appear. Vulnerability "
            "scanner logs document discovered weaknesses, not business transactions. IDS and IPS logs focus on "
            "network attacks and policy violations, not internal accounting activity. Firewall logs show "
            "permitted or denied network flows, not which employee issued checks in an application."
        ),
        "choices": [
            "Application logs",
            "Vulnerability scanner logs",
            "IDS/IPS logs",
            "Firewall logs",
        ],
        "objectives": ["4.9", "5.5"],
    },
    {
        "slug": "saas-domain-credentials-single-sign-on",
        "title": "Security+ — SSO (SaaS domain credentials)",
        "stem": (
            "A data administrator is configuring authentication for a SaaS application and would like to reduce the "
            "number of credentials employees need to maintain. The company prefers to use domain credentials to "
            "access new SaaS applications. Which of the following methods would allow this functionality?"
        ),
        "name": "secplus_q349",
        "correct": "A",
        "explain": (
            "Correct. A — Single sign-on federates SaaS access with the corporate identity provider so employees "
            "use existing domain credentials instead of separate passwords per application. LEAP is a legacy "
            "wireless authentication protocol, not SaaS federation. MFA adds verification factors but does not "
            "by itself reduce the number of distinct accounts. PEAP protects wireless 802.1X sessions and is "
            "not used to extend domain logins to cloud SaaS."
        ),
        "choices": [
            "SSO",
            "LEAP",
            "MFA",
            "PEAP",
        ],
        "objectives": ["5.5", "5.6"],
    },
    {
        "slug": "decoy-vulnerable-infrastructure-honeypot-reconnaissance",
        "title": "Security+ — Honeypot (reconnaissance alerts)",
        "stem": (
            "A company wants to get alerts when others are researching and doing reconnaissance on the company. "
            "One approach would be to host a part of the infrastructure online with known vulnerabilities that "
            "would appear to be company assets. Which of the following describes this approach?"
        ),
        "name": "secplus_q350",
        "correct": "D",
        "explain": (
            "Correct. D — A honeypot is a decoy system or service that looks like a real asset to lure "
            "reconnaissance and attacks while generating alerts for defenders. A watering hole compromises sites "
            "the target frequents to deliver malware. A bug bounty pays researchers to report flaws in real "
            "systems under agreed rules. A DNS sinkhole redirects malicious domain lookups to block command and "
            "control, not to masquerade as company infrastructure."
        ),
        "choices": [
            "Watering hole",
            "Bug bounty",
            "DNS sinkhole",
            "Honeypot",
        ],
        "objectives": ["4.8", "1.1"],
    },
    {
        "slug": "third-party-contract-end-data-retention-liability",
        "title": "Security+ — Data retention (contract end)",
        "stem": (
            "Which of the following should an organization implement to avoid unnecessary liability after the end "
            "of a legal contract obligation with a third party?"
        ),
        "name": "secplus_q351",
        "correct": "C",
        "explain": (
            "Correct. C — Data retention policies define how long information is kept and when it must be "
            "destroyed or returned after contractual obligations end, reducing exposure from holding data "
            "longer than permitted. Data encryption protects confidentiality but does not limit post-contract "
            "liability from retained records. Data classification labels sensitivity and handling requirements "
            "but does not schedule disposal when agreements expire. A data inventory identifies what exists but "
            "does not by itself enforce timely deletion after a third-party contract ends."
        ),
        "choices": [
            "Data encryption",
            "Data classification",
            "Data retention",
            "Data inventory",
        ],
        "objectives": ["5.6", "5.2"],
    },
    {
        "slug": "vendor-email-compromise-awareness-familiar-addresses",
        "title": "Security+ — Awareness (compromised vendor email)",
        "stem": (
            "While updating the security awareness training, a security analyst wants to address issues created if "
            "vendors' email accounts are compromised. Which of the following recommendations should the security "
            "analyst include in the training?"
        ),
        "name": "secplus_q352",
        "correct": "D",
        "explain": (
            "Correct. D — When a vendor mailbox is compromised, messages often come from a familiar address but "
            "contain unusual payment, banking, or urgency requests; staff should verify out-of-band before acting. "
            "Avoiding images from new vendors does not address BEC from established partners. Deleting mail from "
            "unknown providers ignores attacks sent from legitimate compromised vendor accounts. Requiring "
            "invoices as attachments does not stop fraud and can increase malicious attachment risk."
        ),
        "choices": [
            "Refrain from clicking on images included in emails from new vendors.",
            "Delete emails from unknown service provider partners.",
            "Require that invoices be sent as attachments.",
            "Be alert to unexpected requests from familiar email addresses.",
        ],
        "objectives": ["2.2", "5.4"],
    },
    {
        "slug": "phishing-false-positives-awareness-training",
        "title": "Security+ — Awareness training (phishing FP)",
        "stem": (
            "The number of tickets the help desk has been receiving has increased recently due to numerous "
            "false-positive phishing reports. Which of the following would be best to help to reduce the false "
            "positives?"
        ),
        "name": "secplus_q353",
        "correct": "B",
        "explain": (
            "Correct. B — Better security awareness training teaches employees how to recognize real phishing "
            "indicators and when legitimate messages are safe, which lowers unnecessary help desk reports. More "
            "phishing simulations can increase reporting volume and do not by themselves improve discrimination. "
            "Hiring more help desk staff handles ticket load but does not reduce false positives. An incident "
            "reporting web page may streamline submissions but does not teach users to report more accurately."
        ),
        "choices": [
            "Performing more phishing simulation campaigns",
            "Improving security awareness training",
            "Hiring more help desk staff",
            "Implementing an incident reporting web page",
        ],
        "objectives": ["5.4", "2.2"],
    },
    {
        "slug": "web-filter-block-http-unencrypted-urls",
        "title": "Security+ — Web filter (block HTTP)",
        "stem": (
            "A company's web filter is configured to scan the URL for strings and deny access when matches are "
            "found. Which of the following search strings should an analyst employ to prohibit access to "
            "non-encrypted websites?"
        ),
        "name": "secplus_q354",
        "correct": "B",
        "explain": (
            "Correct. B — Non-encrypted web traffic uses the http:// scheme; denying URLs containing http:// "
            "blocks cleartext HTTP sessions while https:// remains encrypted. encryption=off is not a standard "
            "URL component web filters match. A pattern such as www.*.com blocks broad name formats regardless "
            "of protocol. Port :443 is used by HTTPS and would target encrypted traffic, not unencrypted sites."
        ),
        "choices": [
            "encryption=off",
            "http://",
            "www.*.com",
            ":443",
        ],
        "objectives": ["4.6", "3.5"],
    },
    {
        "slug": "critical-systems-air-gapped-remote-access-isolation",
        "title": "Security+ — Air-gapped (remote access isolation)",
        "stem": (
            "Which of the following architecture models ensures that critical systems are physically isolated from "
            "the network to prevent access from users with remote access privileges?"
        ),
        "name": "secplus_q355",
        "correct": "C",
        "explain": (
            "Correct. C — An air-gapped architecture removes network connectivity so remote users cannot reach "
            "critical systems over corporate or VPN paths. Segmentation divides networks logically but systems "
            "remain connected. Virtualized environments share hosts and networks and are not physically isolated. "
            "Serverless workloads run in cloud provider networks and depend on continuous connectivity."
        ),
        "choices": [
            "Segmentation",
            "Virtualized",
            "Air-gapped",
            "Serverless",
        ],
        "objectives": ["3.1", "3.2"],
    },
    {
        "slug": "cfo-vendor-friend-conflict-of-interest",
        "title": "Security+ — Conflict of interest (CFO vendor)",
        "stem": (
            "A vendor salesperson is a personal friend of a company's Chief Financial Officer (CFO). The company "
            "recently made a large purchase from the vendor, which was directly approved by the CFO. Which of the "
            "following best describes this situation?"
        ),
        "name": "secplus_q356",
        "correct": "B",
        "explain": (
            "Correct. B — A conflict of interest exists when a decision maker's personal relationship may "
            "influence business judgments, such as a CFO approving a large purchase from a friend's employer. "
            "Rules of engagement define authorized scope for security assessments. Due diligence is the "
            "investigation performed before entering agreements. Contractual impact describes legal consequences "
            "of contract terms. Reputational damage is harm to public trust, not the label for this ethics issue."
        ),
        "choices": [
            "Rules of engagement",
            "Conflict of interest",
            "Due diligence",
            "Contractual impact",
            "Reputational damage",
        ],
        "objectives": ["5.3", "5.6"],
    },
    {
        "slug": "osint-public-platforms-security-exposures",
        "title": "Security+ — OSINT (public platforms)",
        "stem": (
            "Which of the following best describes a common use of OSINT?"
        ),
        "name": "secplus_q357",
        "correct": "C",
        "explain": (
            "Correct. C — Open source intelligence (OSINT) collects publicly available information from websites, "
            "social media, DNS records, and other open platforms to identify exposures useful for risk assessment "
            "or testing. Monitoring internal systems and traffic is operational security monitoring. Installing "
            "patches is vulnerability remediation. Encrypting and storing data in the cloud is a data protection "
            "control, not intelligence gathering from public sources."
        ),
        "choices": [
            "Monitoring internal systems and network traffic to detect abnormal behavior",
            "Installing and configuring security patches to fix known vulnerabilities",
            "Collecting information from public platforms to find possible security exposures",
            "Encrypting sensitive company data and storing it securely in the cloud",
        ],
        "objectives": ["4.9", "2.1"],
    },
    {
        "slug": "team-file-permissions-access-control-list",
        "title": "Security+ — ACL (file permissions)",
        "stem": (
            "A systems administrator wants to use a technical solution to explicitly define file permissions for the "
            "entire team. Which of the following should the administrator implement?"
        ),
        "name": "secplus_q358",
        "correct": "A",
        "explain": (
            "Correct. A — Access control lists (ACLs) specify which users or groups may read, write, or execute "
            "files and folders on servers and workstations. Monitoring observes activity but does not assign "
            "permissions. Isolation separates systems or networks and is not the primary mechanism for per-file "
            "team access rules. A host intrusion prevention system blocks suspicious host behavior and does not "
            "define file-level authorization for a team."
        ),
        "choices": [
            "ACL",
            "Monitoring",
            "Isolation",
            "HIPS",
        ],
        "objectives": ["3.3", "5.5"],
    },
    {
        "slug": "outbound-dns-acl-single-resolver-10-50-10-25",
        "title": "Security+ — Firewall ACL (outbound DNS)",
        "stem": (
            "An enterprise is trying to limit outbound DNS traffic originating from its internal network. Outbound "
            "DNS requests will only be allowed from one device with the IP address 10.50.10.25. Which of the "
            "following firewall ACLs will accomplish this goal?"
        ),
        "name": "secplus_q359",
        "correct": "D",
        "explain": (
            "Correct. D — The permit line allows outbound UDP/TCP port 53 only when the source is 10.50.10.25; "
            "the deny line blocks DNS from all other internal sources. Option A permits all sources then denies "
            "the allowed host. Option B treats 10.50.10.25 as the destination instead of the source. Option C "
            "permits all DNS traffic before a deny that targets the wrong address role."
        ),
        "choices": [
            (
                "Access list outbound permit 0.0.0.0/0 0.0.0.0/0 port 53; "
                "Access list outbound deny 10.50.10.25/32 0.0.0.0/0 port 53"
            ),
            (
                "Access list outbound permit 0.0.0.0/0 10.50.10.25/32 port 53; "
                "Access list outbound deny 0.0.0.0/0 0.0.0.0/0 port 53"
            ),
            (
                "Access list outbound permit 0.0.0.0/0 0.0.0.0/0 port 53; "
                "Access list outbound deny 0.0.0.0/0 10.50.10.25/32 port 53"
            ),
            (
                "Access list outbound permit 10.50.10.25/32 0.0.0.0/0 port 53; "
                "Access list outbound deny 0.0.0.0/0 0.0.0.0/0 port 53"
            ),
        ],
        "objectives": ["3.3", "4.6"],
    },
    {
        "slug": "firewall-open-ports-attack-surface-principle",
        "title": "Security+ — Attack surface (open ports)",
        "stem": (
            "A small business initially plans to open common communications ports (21, 22, 25, 80, 443) on its "
            "firewall to allow broad access to its screened subnet. However, their security consultant advises "
            "against this action. Which of the following security principles is the consultant addressing?"
        ),
        "name": "secplus_q360",
        "correct": "B",
        "explain": (
            "Correct. B — Opening many services and ports increases the attack surface, the set of exposed "
            "entry points an adversary can target; the consultant recommends limiting what is exposed. Secure "
            "access service edge is a cloud network architecture model, not the principle for avoiding excessive "
            "open ports. Least privilege limits rights to the minimum required and is related but the exam pairs "
            "unnecessary open ports with attack surface reduction. Separation of duties splits conflicting tasks "
            "among people, not firewall port exposure."
        ),
        "choices": [
            "Secure access service edge",
            "Attack surface",
            "Least privilege",
            "Separation of duties",
        ],
        "objectives": ["3.1", "3.3"],
    },
    {
        "slug": "contractor-access-expansion-risk-appetite",
        "title": "Security+ — Risk appetite (contractor access)",
        "stem": (
            "A company is considering an expansion of access controls for an application that contractors and "
            "internal employees use to reduce costs. Which of the following risk elements should the "
            "implementation team understand before granting access to the application?"
        ),
        "name": "secplus_q361",
        "correct": "B",
        "explain": (
            "Correct. B — Risk appetite is the amount and type of risk leadership is willing to accept; widening "
            "access for contractors must align with that posture before implementation. A risk threshold is the "
            "level at which risk becomes unacceptable and triggers action. Risk tolerance is the acceptable "
            "variation around objectives for a specific risk. A risk register documents identified risks but does "
            "not by itself define how much risk the organization will accept."
        ),
        "choices": [
            "Threshold",
            "Appetite",
            "Tolerance",
            "Register",
        ],
        "objectives": ["5.2", "5.3"],
    },
    {
        "slug": "hacktivist-vs-insider-threat-distinction",
        "title": "Security+ — Hacktivist vs insider threat",
        "stem": (
            "Which of the following best distinguishes hacktivists from insider threats?"
        ),
        "name": "secplus_q362",
        "correct": "C",
        "explain": (
            "Correct. C — Insider threats abuse legitimate internal access or affiliation; hacktivists typically "
            "operate from outside without prior organizational access. Ideological motivation describes "
            "hacktivists but option A awkwardly contrasts beliefs with access rather than insider status. "
            "Hacktivists are not generally employed by the target at attack time; that describes many insiders. "
            "Personal or employment-related dissatisfaction is a common insider motive, not a defining "
            "hacktivist trait."
        ),
        "choices": [
            "Hacktivists often act based on ideological or political beliefs rather than organizational access.",
            "Hacktivists are generally employed by the target organization at the time of attack.",
            "Hacktivists often target organizations without prior access or internal affiliation.",
            "Hacktivists are primarily motivated by personal conflicts or employment-related dissatisfaction.",
        ],
        "objectives": ["2.1", "2.4"],
    },
    {
        "slug": "vendor-bank-change-business-email-compromise",
        "title": "Security+ — BEC (vendor payment redirect)",
        "stem": (
            "A company's accounts payable clerk receives a message from a vendor asking to change their bank "
            "account before paying an invoice. The clerk makes the change and sends the payment to the new account. "
            "Days later, the clerk receives another message from the same vendor with a request for a missing "
            "payment to the original bank account. Which of the following has most likely occurred?"
        ),
        "name": "secplus_q363",
        "correct": "D",
        "explain": (
            "Correct. D — Business email compromise uses impersonated or compromised vendor email to redirect "
            "legitimate payments to attacker-controlled accounts; the real vendor later requests payment to the "
            "original bank. A phishing campaign is broad credential or malware lures, not this targeted payment "
            "fraud pattern. Data exfiltration is unauthorized removal of data, not wire diversion. Pretext "
            "calling is voice-based social engineering, not email-driven invoice fraud."
        ),
        "choices": [
            "Phishing campaign",
            "Data exfiltration",
            "Pretext calling",
            "Business email compromise",
        ],
        "objectives": ["2.2", "2.4"],
    },
    {
        "slug": "marketing-unsanctioned-software-shadow-it",
        "title": "Security+ — Shadow IT (unsanctioned SaaS)",
        "stem": (
            "The marketing department set up its own project management software without telling the appropriate "
            "departments. Which of the following describes this scenario?"
        ),
        "name": "secplus_q364",
        "correct": "A",
        "explain": (
            "Correct. A — Shadow IT is the use of hardware, software, or cloud services without approval from IT "
            "or security, such as a department deploying its own project management tool. An insider threat "
            "involves trusted users intentionally or negligently harming the organization, not simply adopting "
            "unapproved tools. Data exfiltration is unauthorized removal of sensitive data. Service disruption is "
            "an availability incident such as an outage or denial of service."
        ),
        "choices": [
            "Shadow IT",
            "Insider threat",
            "Data exfiltration",
            "Service disruption",
        ],
        "objectives": ["3.9", "5.6"],
    },
    {
        "slug": "printing-center-hygiene-dumpster-diving",
        "title": "Security+ — Dumpster diving (printing centers)",
        "stem": (
            "During a recent company safety stand-down, the cyber-awareness team gave a presentation on the "
            "importance of cyber hygiene. One topic the team covered was best practices for printing centers. "
            "Which of the following describes an attack method that relates to printing centers?"
        ),
        "name": "secplus_q365",
        "correct": "D",
        "explain": (
            "Correct. D — Dumpster diving is searching discarded paper for sensitive information; misprints and "
            "abandoned output from printing centers often end up in trash without shredding. Whaling is targeted "
            "phishing against high-value executives. Credential harvesting collects login secrets through scams or "
            "malware. Prepending inserts or alters text such as email headers and is not a physical print-center "
            "risk."
        ),
        "choices": [
            "Whaling",
            "Credential harvesting",
            "Prepending",
            "Dumpster diving",
        ],
        "objectives": ["2.1", "5.4"],
    },
    {
        "slug": "banking-audit-regulatory-requirement",
        "title": "Security+ — Audit (banking regulatory)",
        "stem": (
            "Which of the following is the best reason to complete an audit in a banking environment?"
        ),
        "name": "secplus_q366",
        "correct": "A",
        "explain": (
            "Correct. A — Financial institutions face mandatory regulatory and compliance audits from frameworks "
            "and supervisors that require independent verification of controls. Organizational change may "
            "trigger reviews but is not the primary driver in banking. Self-assessment supports internal "
            "governance but does not replace mandated external scrutiny. Service-level requirements define "
            "operational performance targets, not the chief reason regulated banks conduct audits."
        ),
        "choices": [
            "Regulatory requirement",
            "Organizational change",
            "Self-assessment requirement",
            "Service-level requirement",
        ],
        "objectives": ["5.6", "5.3"],
    },
    {
        "slug": "authorized-devices-access-lists-admission",
        "title": "Security+ — Access lists (authorized devices)",
        "stem": (
            "A company wants to ensure that only authorized devices can enter an environment. Which of the "
            "following will the company most likely use to implement the control?"
        ),
        "name": "secplus_q367",
        "correct": "A",
        "explain": (
            "Correct. A — Access lists on firewalls, routers, or switches can permit only known addresses or "
            "hosts and deny all others attempting to reach or join a network segment. Remote connection services "
            "enable off-site user access rather than admission control for devices entering a facility or VLAN. "
            "Screened subnets isolate public-facing systems but do not by themselves authenticate each endpoint. "
            "A centralized proxy filters application traffic, not which devices may attach to the environment."
        ),
        "choices": [
            "Access lists",
            "Remote connection",
            "Screened subnets",
            "Centralized proxy",
        ],
        "objectives": ["3.3", "4.6"],
    },
    {
        "slug": "site-recovery-resource-group-rbac",
        "title": "Security+ — RBAC (site recovery resource group)",
        "stem": (
            "A systems administrator wants to prevent users from being able to access data based on their "
            "responsibilities. The administrator also wants to apply the required access structure via a simplified "
            "format. Which of the following should the administrator apply to the site recovery resource group?"
        ),
        "name": "secplus_q368",
        "correct": "A",
        "explain": (
            "Correct. A — Role-based access control assigns permissions to roles tied to job responsibilities and "
            "grants users roles, simplifying management for resource groups such as site recovery. ACLs define "
            "per-resource allow or deny rules but are not the role-centric model described. SAML federates "
            "authentication for single sign-on and does not by itself structure authorization by responsibility. "
            "Group Policy Objects deploy Windows domain settings and are not the primary access model for cloud "
            "recovery resource groups."
        ),
        "choices": [
            "RBAC",
            "ACL",
            "SAML",
            "GPO",
        ],
        "objectives": ["3.3", "5.5"],
    },
    {
        "slug": "cspm-misconfigurations-soar-workflows",
        "title": "Security+ — SOAR (CSPM workflows)",
        "stem": (
            "A security team purchases a tool for cloud security posture management. The team is quickly "
            "overwhelmed by the number of misconfigurations that the tool detects. Which of the following should "
            "the security team configure to establish workflows for cloud resource security?"
        ),
        "name": "secplus_q369",
        "correct": "C",
        "explain": (
            "Correct. C — Security orchestration, automation, and response (SOAR) ties CSPM findings to playbooks "
            "that triage, assign, and remediate misconfigurations at scale. A cloud access security broker governs "
            "use of sanctioned cloud applications and data in transit to SaaS. IAM manages identities and role "
            "assignments but does not orchestrate remediation workflows for posture findings. Extended detection "
            "and response correlates threat telemetry across vectors rather than driving cloud misconfiguration "
            "work queues."
        ),
        "choices": [
            "CASB",
            "IAM",
            "SOAR",
            "XDR",
        ],
        "objectives": ["4.5", "4.9"],
    },
    {
        "slug": "web-server-vulnerability-patching",
        "title": "Security+ — Patching (web server vuln)",
        "stem": (
            "Which of the following actions best addresses a vulnerability found on a company's web server?"
        ),
        "name": "secplus_q370",
        "correct": "A",
        "explain": (
            "Correct. A — Patching applies vendor fixes that remediate the underlying flaw on the web server. "
            "Segmentation limits exposure between network zones but does not remove the vulnerability on the "
            "host. Decommissioning removes the system entirely and is disproportionate when the service must "
            "remain available. Monitoring detects suspicious activity but does not correct the weakness itself."
        ),
        "choices": [
            "Patching",
            "Segmentation",
            "Decommissioning",
            "Monitoring",
        ],
        "objectives": ["4.2", "4.5"],
    },
    {
        "slug": "dr-site-validate-simulated-failover",
        "title": "Security+ — Simulated failover (DR site)",
        "stem": (
            "Which of the following is the best way to validate the integrity and availability of a disaster recovery "
            "site?"
        ),
        "name": "secplus_q371",
        "correct": "A",
        "explain": (
            "Correct. A — A simulated failover exercises cutover to the disaster recovery site and confirms that "
            "systems, data, and services are available and consistent. A tabletop exercise is discussion-based and "
            "does not prove technical recovery works. Testing generators validates power only, not application or "
            "data recovery. Defining database encryption requirements is a design control, not validation of DR "
            "site readiness."
        ),
        "choices": [
            "Lead a simulated failover.",
            "Conduct a tabletop exercise.",
            "Periodically test the generators.",
            "Develop requirements for database encryption.",
        ],
        "objectives": ["3.4", "5.2"],
    },
    {
        "slug": "admin-credential-guessing-user-activity-logs",
        "title": "Security+ — User activity logs (credential guessing)",
        "stem": (
            "A university employee logged on to the academic server and attempted to guess the system administrators' "
            "log-in credentials. Which of the following security measures should the university have implemented to "
            "detect the employee's attempts to gain access to the administrators' accounts?"
        ),
        "name": "secplus_q372",
        "correct": "D",
        "explain": (
            "Correct. D — User activity and authentication logs record failed and successful logon attempts so "
            "analysts can detect password-guessing against privileged accounts. Two-factor authentication strengthens "
            "authentication but is preventive rather than the primary detective control cited here. A firewall "
            "filters network traffic and does not by itself log local interactive logon guessing on a server. An "
            "intrusion prevention system blocks known attack patterns on the network but is not the standard way to "
            "detect repeated local credential guesses against administrator accounts."
        ),
        "choices": [
            "Two-factor authentication",
            "Firewall",
            "Intrusion prevention system",
            "User activity logs",
        ],
        "objectives": ["4.9", "4.4"],
    },
    {
        "slug": "file-server-confidential-data-acl-restrict",
        "title": "Security+ — ACL (file server confidential data)",
        "stem": (
            "After an audit, an administrator discovers all users have access to confidential data on a file server. "
            "Which of the following should the administrator use to restrict access to the data quickly?"
        ),
        "name": "secplus_q373",
        "correct": "D",
        "explain": (
            "Correct. D — Access control lists on the file server (such as NTFS and share permissions) directly "
            "limit which users or groups can read or modify confidential folders. Group Policy can deploy settings "
            "domain-wide but is slower to target a specific data set than adjusting ACLs on the resource. Content "
            "filtering governs web or email traffic, not local file share authorization. Data loss prevention "
            "monitors and blocks sensitive data movement but does not quickly replace overly permissive file "
            "permissions."
        ),
        "choices": [
            "Group Policy",
            "Content filtering",
            "Data loss prevention",
            "Access control lists",
        ],
        "objectives": ["3.3", "5.5"],
    },
    {
        "slug": "mssp-alerts-automated-ticket-creation-itsm",
        "title": "Security+ — Automated ticket creation (MSSP alerts)",
        "stem": (
            "Alerts from email protection systems and MSSPs must be entered into an IT service management system "
            "and assigned to the security team. Which of the following should an organization implement to enable "
            "this functionality?"
        ),
        "name": "secplus_q374",
        "correct": "B",
        "explain": (
            "Correct. B — Automated ticket creation integrates alerting tools and managed security providers with "
            "the ITSM platform so incidents are opened and routed to the security team without manual data entry. "
            "Automated compliance monitoring tracks policy adherence against baselines. Automated vulnerability "
            "scans discover flaws on systems and do not assign MSSP alerts to a service desk queue. Automated "
            "indicator sharing exchanges threat intelligence between organizations, not internal ticketing workflows."
        ),
        "choices": [
            "Automated compliance monitoring",
            "Automated ticket creation",
            "Automated vulnerability scans",
            "Automated indicator sharing",
        ],
        "objectives": ["4.9", "4.5"],
    },
    {
        "slug": "help-desk-admin-console-least-privilege",
        "title": "Security+ — Least privilege (help desk admin)",
        "stem": (
            "An IT manager informs the entire help desk staff that only the IT manager and the help desk lead will "
            "have access to the administrator console of the help desk software. Which of the following security "
            "techniques is the IT manager setting up?"
        ),
        "name": "secplus_q375",
        "correct": "D",
        "explain": (
            "Correct. D — Least privilege limits access to the minimum needed for each role; most help desk staff "
            "need ticket functions, not the administrator console. Hardening reduces attack surface on systems "
            "through secure configuration and patching. Employee monitoring observes user activity for policy "
            "violations. Configuration enforcement ensures devices meet baselines but does not by itself define "
            "which staff may use privileged application consoles."
        ),
        "choices": [
            "Hardening",
            "Employee monitoring",
            "Configuration enforcement",
            "Least privilege",
        ],
        "objectives": ["3.3", "5.5"],
    },
    {
        "slug": "datacenter-attack-surface-upgrade-eol-os",
        "title": "Security+ — Attack surface (upgrade EOL OS)",
        "stem": (
            "A security administrator needs to reduce the attack surface in the company's data centers. Which of "
            "the following should the security administrator do to complete this task?"
        ),
        "name": "secplus_q376",
        "correct": "D",
        "explain": (
            "Correct. D — End-of-support operating systems no longer receive security patches, leaving known "
            "vulnerabilities exposed; upgrading removes that unpatched exposure. A honeynet is a decoy environment "
            "and does not shrink production attack surface. Group Policy can enforce baselines but defining policy "
            "alone does not remediate unsupported platforms. High availability improves uptime and resilience, not "
            "the number of exploitable weaknesses."
        ),
        "choices": [
            "Implement a honeynet.",
            "Define Group Policy on the servers.",
            "Configure the servers for high availability.",
            "Upgrade end-of-support operating systems.",
        ],
        "objectives": ["3.1", "4.2"],
    },
    {
        "slug": "after-hours-remote-data-copy-insider-threat",
        "title": "Security+ — Insider threat (after-hours exfil)",
        "stem": (
            "An administrator was notified that a user logged in remotely after hours and copied large amounts of "
            "data to a personal device. Which of the following best describes the user's activity?"
        ),
        "name": "secplus_q377",
        "correct": "D",
        "explain": (
            "Correct. D — An insider threat is a trusted user abusing legitimate access, such as off-hours remote "
            "logon and copying company data to a personal device. Penetration testing is authorized security "
            "testing with defined scope and rules of engagement. A phishing campaign is external social engineering "
            "against users. An external audit is independent review of controls, not unauthorized data removal by "
            "an employee."
        ),
        "choices": [
            "Penetration testing",
            "Phishing campaign",
            "External audit",
            "Insider threat",
        ],
        "objectives": ["2.1", "2.4"],
    },
    {
        "slug": "off-premises-migration-cloud-provider-security-first",
        "title": "Security+ — Cloud provider security (migration first)",
        "stem": (
            "A business received a small grant to migrate its infrastructure to an off-premises solution. Which of "
            "the following should be considered first?"
        ),
        "name": "secplus_q378",
        "correct": "A",
        "explain": (
            "Correct. A — Before committing grant funds, the organization should evaluate cloud provider security "
            "posture, certifications, and shared responsibility commitments. Implementation cost matters but follows "
            "vendor due diligence. Staff skill gaps are addressed during planning and training after provider "
            "selection. Architecture security is essential but is designed after choosing a trustworthy provider "
            "and understanding which controls the customer must implement."
        ),
        "choices": [
            "Security of cloud providers",
            "Cost of implementation",
            "Ability of engineers",
            "Security of architecture",
        ],
        "objectives": ["3.4", "5.6"],
    },
    {
        "slug": "preventive-physical-security-bollards",
        "title": "Security+ — Bollards (preventive physical)",
        "stem": (
            "Which of the following is a preventive physical security control?"
        ),
        "name": "secplus_q379",
        "correct": "B",
        "explain": (
            "Correct. B — Bollards are physical barriers that prevent vehicles from entering protected areas. "
            "Video surveillance primarily detects and records events after they occur. Alarm systems alert when "
            "intrusion is detected. Motion sensors detect movement and are detective controls rather than "
            "physical prevention."
        ),
        "choices": [
            "Video surveillance system",
            "Bollards",
            "Alarm system",
            "Motion sensors",
        ],
        "objectives": ["1.1", "3.10"],
    },
    {
        "slug": "pentest-badge-unauthorized-area-physical",
        "title": "Security+ — Physical pentest (badge entry)",
        "stem": (
            "During a penetration test, a vendor attempts to enter an unauthorized area using an access badge. "
            "Which of the following types of tests does this represent?"
        ),
        "name": "secplus_q380",
        "correct": "D",
        "explain": (
            "Correct. D — A physical penetration test evaluates facility controls such as badges, locks, and "
            "guards by attempting unauthorized entry. Defensive testing focuses on detecting and blocking attacks "
            "from the blue team perspective. Passive testing gathers information without direct interaction. "
            "Offensive testing is a broad term for attacking systems and networks; badge-based entry tests "
            "physical security specifically."
        ),
        "choices": [
            "Defensive",
            "Passive",
            "Offensive",
            "Physical",
        ],
        "objectives": ["4.3", "3.10"],
    },
    {
        "slug": "remote-access-vpn-agent-ipsec-tunnel",
        "title": "Security+ — IPSec (remote access VPN agent)",
        "stem": (
            "A security engineer configured a remote access VPN. The remote access VPN allows end users to connect "
            "to the network by using an agent that is installed on the endpoint, which establishes an encrypted "
            "tunnel. Which of the following protocols did the engineer most likely implement?"
        ),
        "name": "secplus_q381",
        "correct": "B",
        "explain": (
            "Correct. B — IPSec is commonly used for remote access VPN clients that build encrypted tunnels between "
            "endpoints and the corporate network. GRE encapsulates traffic but does not provide encryption by "
            "itself. SD-WAN optimizes and secures WAN connectivity between sites rather than describing a typical "
            "endpoint VPN agent tunnel. EAP is an authentication framework for network access, not the VPN tunnel "
            "protocol."
        ),
        "choices": [
            "GRE",
            "IPSec",
            "SD-WAN",
            "EAP",
        ],
        "objectives": ["3.5", "4.6"],
    },
    {
        "slug": "need-to-know-roles-confidentiality",
        "title": "Security+ — Confidentiality (need to know)",
        "stem": (
            "Client files can only be accessed by employees who need to know the information and have specified "
            "roles in the company. Which of the following best describes this security concept?"
        ),
        "name": "secplus_q382",
        "correct": "B",
        "explain": (
            "Correct. B — Confidentiality ensures information is disclosed only to authorized individuals, such as "
            "employees with a business need to know and appropriate roles. Availability concerns timely and "
            "reliable access for authorized use. Integrity ensures data is accurate and unaltered by unauthorized "
            "parties. Non-repudiation provides proof that an action occurred and who performed it."
        ),
        "choices": [
            "Availability",
            "Confidentiality",
            "Integrity",
            "Non-repudiation",
        ],
        "objectives": ["1.2", "3.3"],
    },
    {
        "slug": "open-service-ports-attack-surface-exposure",
        "title": "Security+ — Open ports (attack surface)",
        "stem": (
            "Which of the following best explains how open service ports increase an organization's attack surface?"
        ),
        "name": "secplus_q383",
        "correct": "D",
        "explain": (
            "Correct. D — Each open port advertises a service that attackers can probe; unnecessary or poorly "
            "restricted services expand exploitable entry points. Endpoint antivirus may miss some threats but "
            "that is not why ports increase attack surface. A remote entry point may involve open ports but "
            "attack surface also includes internal and unnecessary services, not only internet-facing VPN. "
            "Automatic updates reduce risk windows; open ports themselves do not provide updates."
        ),
        "choices": [
            "They are commonly overlooked by endpoint antivirus tools during scans.",
            "They can make the company's remote entry point available to the internet.",
            "They enable automatic application updates to reduce vulnerability windows.",
            "They can expose unnecessary services to unauthorized access if not properly restricted.",
        ],
        "objectives": ["3.1", "3.3"],
    },
    {
        "slug": "secure-zone-policy-zero-trust",
        "title": "Security+ — Zero Trust (secure zone policy)",
        "stem": (
            "A systems administrator is working on a solution with the following requirements:\n"
            "• Provide a secure zone.\n"
            "• Enforce a company-wide access control policy.\n"
            "• Reduce the scope of threats.\n"
            "Which of the following is the systems administrator setting up?"
        ),
        "name": "secplus_q384",
        "correct": "A",
        "explain": (
            "Correct. A — Zero Trust architecture uses segmented secure zones, centralized policy enforcement, "
            "and least-privilege access to limit lateral movement and shrink the blast radius of threats. AAA "
            "describes authentication, authorization, and accounting functions but is not the overall "
            "architecture name for these combined requirements. Non-repudiation proves actions occurred and "
            "cannot be denied. CIA names confidentiality, integrity, and availability goals, not a deployable "
            "access model."
        ),
        "choices": [
            "Zero Trust",
            "AAA",
            "Non-repudiation",
            "CIA",
        ],
        "objectives": ["3.1", "3.4"],
    },
    {
        "slug": "email-digital-signature-non-repudiation",
        "title": "Security+ — Non-repudiation (email signature)",
        "stem": (
            "A user sends an email that includes a digital signature for validation. Which of the following security "
            "concepts would ensure that a user cannot deny that they sent the email?"
        ),
        "name": "secplus_q385",
        "correct": "A",
        "explain": (
            "Correct. A — Non-repudiation provides evidence that an action occurred and who performed it, so "
            "the sender cannot later deny sending the signed message. Confidentiality protects content from "
            "unauthorized disclosure. Integrity ensures the message was not altered in transit. Authentication "
            "verifies identity at logon or connection time but does not by itself prevent denial after the fact."
        ),
        "choices": [
            "Non-repudiation",
            "Confidentiality",
            "Integrity",
            "Authentication",
        ],
        "objectives": ["1.2", "1.4"],
    },
    {
        "slug": "saas-multiple-logins-select-idp-first",
        "title": "Security+ — Select IdP (SaaS SSO first step)",
        "stem": (
            "An organization is adopting cloud services at a rapid pace and now has multiple SaaS applications in use. "
            "Each application has a separate log-in, so the security team wants to reduce the number of credentials "
            "each employee must maintain. Which of the following is the first step the security team should take?"
        ),
        "name": "secplus_q386",
        "correct": "D",
        "explain": (
            "Correct. D — The team must choose a central identity provider before federating SaaS applications and "
            "enabling protocols such as SAML or OAuth. Enabling SAML comes after an IdP is selected and integrated. "
            "OAuth tokens are issued during application federation, not as the initial planning step. Password "
            "vaulting stores many credentials but does not replace separate logins with single sign-on."
        ),
        "choices": [
            "Enable SAML",
            "Create OAuth tokens.",
            "Use password vaulting.",
            "Select an IdP",
        ],
        "objectives": ["3.8", "5.5"],
    },
    {
        "slug": "unrelated-sensitive-projects-uba-detection",
        "title": "Security+ — UBA (unauthorized project access)",
        "stem": (
            "Executives at a company are concerned about employees accessing systems and information about "
            "sensitive company projects unrelated to the employees' normal job duties. Which of the following "
            "enterprise security capabilities will the security team most likely deploy to detect that activity?"
        ),
        "name": "secplus_q387",
        "correct": "A",
        "explain": (
            "Correct. A — User behavior analytics (UBA) establishes baselines for how users access systems and "
            "data and alerts when activity deviates, such as reaching projects outside normal job duties. EDR "
            "focuses on endpoint threats and malware execution. NAC controls which devices may join the network. "
            "DLP prevents or detects unauthorized movement of sensitive data but is not primarily aimed at "
            "detecting access to unrelated internal projects."
        ),
        "choices": [
            "UBA",
            "EDR",
            "NAC",
            "DLP",
        ],
        "objectives": ["4.9", "4.4"],
    },
    {
        "slug": "pci-dss-noncompliance-customer-reputational-damage",
        "title": "Security+ — Reputational damage (PCI DSS retail)",
        "stem": (
            "Which of the following consequences would a retail chain most likely face from customers in the event "
            "the retailer is non-compliant with PCI DSS?"
        ),
        "name": "secplus_q388",
        "correct": "D",
        "explain": (
            "Correct. D — Customers most directly impose reputational harm through lost trust and reduced "
            "patronage when payment security failures become public. Contractual impacts arise between the "
            "retailer and acquirers or partners, not from shoppers. Sanctions are imposed by regulators or "
            "governments. Fines are levied by card brands and acquirers rather than by individual customers."
        ),
        "choices": [
            "Contractual impacts",
            "Sanctions",
            "Fines",
            "Reputational damage",
        ],
        "objectives": ["5.4", "5.6"],
    },
    {
        "slug": "incident-response-final-step-lessons-learned",
        "title": "Security+ — IR final step (lessons learned)",
        "stem": (
            "Which of the following is the final step of the incident response process?"
        ),
        "name": "secplus_q389",
        "correct": "A",
        "explain": (
            "Correct. A — Lessons learned (post-incident activity) is the final phase after recovery, capturing "
            "what worked and updating plans and controls. Eradication removes threat artifacts from the "
            "environment. Containment limits spread during an active incident. Recovery restores systems and "
            "services to normal operations before the post-incident review."
        ),
        "choices": [
            "Lessons learned",
            "Eradication",
            "Containment",
            "Recovery",
        ],
        "objectives": ["5.5"],
    },
    {
        "slug": "ceo-phish-ransomware-awareness-training-prevention",
        "title": "Security+ — Awareness training (CEO phish ransomware)",
        "stem": (
            "An employee clicks a malicious link in an email that appears to be from the company's Chief Executive "
            "Officer. The employee's computer is infected with ransomware that encrypts the company's files. Which "
            "of the following is the most effective way for the company to prevent similar incidents in the future?"
        ),
        "name": "secplus_q390",
        "correct": "A",
        "explain": (
            "Correct. A — Security awareness training teaches employees to spot executive impersonation, verify "
            "unexpected links, and avoid enabling ransomware through phishing. Database encryption protects stored "
            "data confidentiality but does not stop users from executing malware from email. Segmentation limits "
            "lateral movement after compromise but does not prevent the initial click. Reporting suspicious emails "
            "is valuable but is one component of a broader awareness program rather than the most complete "
            "preventive measure alone."
        ),
        "choices": [
            "Security awareness training",
            "Database encryption",
            "Segmentation",
            "Reporting suspicious emails",
        ],
        "objectives": ["5.4", "2.2"],
    },
    {
        "slug": "eol-hardware-vendor-patches-vulnerability",
        "title": "Security+ — EOL hardware (no patches)",
        "stem": (
            "Which of the following is a vulnerability concern for end-of-life hardware?"
        ),
        "name": "secplus_q391",
        "correct": "D",
        "explain": (
            "Correct. D — End-of-life hardware no longer receives vendor security patches, leaving known "
            "vulnerabilities unaddressed. Improper disposal can cause data release but is a disposal-process "
            "risk rather than the primary vulnerability while hardware remains in use. Supply chain gaps affect "
            "replacement availability, not unpatched flaws on deployed gear. New software resource demands are "
            "compatibility concerns, not the defining security issue of unsupported hardware."
        ),
        "choices": [
            "Failure to follow hardware disposal procedures could result in unintended data release.",
            "The supply chain may not have replacement hardware.",
            "Newly released software may require computing resources not available on legacy hardware.",
            "The vendor may stop providing patches and updates.",
        ],
        "objectives": ["4.2", "3.2"],
    },
    {
        "slug": "browser-exploit-signatures-ips-block",
        "title": "Security+ — IPS (browser exploit signatures)",
        "stem": (
            "An enterprise has been experiencing attacks focused on exploiting vulnerabilities in older browser "
            "versions with well-known exploits. Which of the following security solutions should be configured to "
            "best provide the ability to monitor and block these known signature-based attacks?"
        ),
        "name": "secplus_q392",
        "correct": "D",
        "explain": (
            "Correct. D — An intrusion prevention system uses signature databases to detect and inline-block "
            "known exploit traffic such as browser attacks. ACLs filter by addresses and ports, not exploit "
            "signatures. DLP focuses on sensitive data movement, not browser vulnerability exploitation. An IDS "
            "can alert on signatures but typically does not block traffic inline the way an IPS does."
        ),
        "choices": [
            "ACL",
            "DLP",
            "IDS",
            "IPS",
        ],
        "objectives": ["4.5", "2.4"],
    },
    {
        "slug": "av-false-positives-heuristic-edr-replacement",
        "title": "Security+ — EDR (replace AV heuristics)",
        "stem": (
            "A company's antivirus solution is effective in blocking malware but often has false positives. The "
            "security team has spent a significant amount of time on investigations but cannot determine a root "
            "cause. The company is looking for a heuristic solution. Which of the following should replace the "
            "antivirus solution?"
        ),
        "name": "secplus_q393",
        "correct": "B",
        "explain": (
            "Correct. B — Endpoint detection and response uses behavioral and heuristic analysis with detailed "
            "telemetry to investigate alerts and identify root causes beyond signature-only antivirus. A SIEM "
            "aggregates logs from many sources but does not replace endpoint malware protection. DLP prevents "
            "unauthorized data exfiltration. An IDS monitors network traffic and does not provide endpoint "
            "heuristic malware controls."
        ),
        "choices": [
            "SIEM",
            "EDR",
            "DLP",
            "IDS",
        ],
        "objectives": ["4.5", "4.9"],
    },
    {
        "slug": "encryption-key-multiple-entities-key-escrow",
        "title": "Security+ — Key escrow (shared key access)",
        "stem": (
            "Which of the following is the best way to securely store an encryption key for a data set in a manner "
            "that allows multiple entities to access the key when needed?"
        ),
        "name": "secplus_q394",
        "correct": "D",
        "explain": (
            "Correct. D — Key escrow places encryption keys with a trusted escrow process or party so authorized "
            "entities can retrieve them under policy when required. Public key infrastructure manages "
            "certificates and trust chains for asymmetric cryptography. An open public ledger is not a standard "
            "enterprise control for confidential key storage. Public key encryption protects data in transit or "
            "at rest with key pairs but does not by itself store a shared symmetric key for multiple custodians."
        ),
        "choices": [
            "Public key infrastructure",
            "Open public ledger",
            "Public key encryption",
            "Key escrow",
        ],
        "objectives": ["1.4", "3.3"],
    },
    {
        "slug": "cloud-breach-sensitivity-data-classification",
        "title": "Security+ — Data classification (breach sensitivity)",
        "stem": (
            "An organization experiences a compromise in a cloud-hosted solution that contains customer "
            "information. Which of the following strategies will help determine the sensitivity level of the breach?"
        ),
        "name": "secplus_q395",
        "correct": "C",
        "explain": (
            "Correct. C — Data classification labels information by sensitivity and regulatory impact so responders "
            "can gauge breach severity when customer data is involved. Permission restrictions limit who may "
            "access data but do not measure how sensitive exposed data was. A tabletop exercise rehearses "
            "incident response and does not classify compromised information. An asset inventory lists systems "
            "and ownership but does not by itself define the sensitivity of data stored in them."
        ),
        "choices": [
            "Permission restrictions",
            "Tabletop exercise",
            "Data classification",
            "Asset inventory",
        ],
        "objectives": ["5.2", "5.5"],
    },
    {
        "slug": "manufacturing-legacy-embedded-systems-pentest",
        "title": "Security+ — Embedded systems (manufacturing legacy)",
        "stem": (
            "A manufacturing organization receives the results from a penetration test. According to the results, "
            "legacy devices that are critical to continued business function display vulnerabilities. The devices have "
            "minimal vendor support and should be segmented and monitored closely. Which of the following devices "
            "were most likely identified?"
        ),
        "name": "secplus_q396",
        "correct": "B",
        "explain": (
            "Correct. B — Embedded systems in manufacturing such as industrial controllers often run legacy "
            "firmware with limited patching and require network segmentation and monitoring. Workstations are "
            "general-purpose endpoints with routine vendor support. Core routers are network infrastructure "
            "typically maintained by vendors with ongoing updates. DNS servers are standard IT services that "
            "receive regular security patches."
        ),
        "choices": [
            "Workstations",
            "Embedded systems",
            "Core router",
            "DNS server",
        ],
        "objectives": ["4.2", "3.2"],
    },
    {
        "slug": "ceo-email-financial-info-bec-attack-vector",
        "title": "Security+ — BEC (CEO financial request)",
        "stem": (
            "An unexpected and out-of-character email message from a Chief Executive Officer's corporate account "
            "asked an employee to provide financial information and to change the recipient's contact number. "
            "Which of the following attack vectors is most likely being used?"
        ),
        "name": "secplus_q397",
        "correct": "A",
        "explain": (
            "Correct. A — Business email compromise uses impersonated or compromised executive email to solicit "
            "financial data or alter payment details such as contact numbers for fraud. Phishing is broader "
            "deceptive email and is less specific than BEC for executive-driven payment fraud. Brand "
            "impersonation mimics a company brand to customers rather than an internal CEO message to staff. "
            "Pretexting builds a fabricated scenario, often by phone, and is not the standard label for this "
            "email pattern."
        ),
        "choices": [
            "Business email compromise",
            "Phishing",
            "Brand impersonation",
            "Pretexting",
        ],
        "objectives": ["2.2", "2.4"],
    },
    {
        "slug": "certificate-management-misconfiguration-vulnerability",
        "title": "Security+ — Misconfiguration (certificates)",
        "stem": (
            "Which of the following types of vulnerabilities is primarily caused by improper use and management of "
            "cryptographic certificates?"
        ),
        "name": "secplus_q398",
        "correct": "A",
        "explain": (
            "Correct. A — Certificate-related flaws such as expired certificates, incorrect bindings, untrusted "
            "chains, or weak TLS settings are classified as misconfigurations from poor certificate lifecycle "
            "management. Resource reuse reuses cryptographic material such as keys or nonces in ways that "
            "break security. Insecure key storage exposes private keys through poor protection of key material. "
            "Weak cipher suites concern deprecated algorithms, which is related but distinct from certificate "
            "issuance and renewal errors."
        ),
        "choices": [
            "Misconfiguration",
            "Resource reuse",
            "Insecure key storage",
            "Weak cipher suites",
        ],
        "objectives": ["4.2", "1.4"],
    },
    {
        "slug": "laptop-web-filtering-agent-based-remote",
        "title": "Security+ — Agent-based (web filtering)",
        "stem": (
            "An organization issued new laptops to all employees and wants to provide web filtering both in and out "
            "of the office without configuring additional access to the network. Which of the following types of "
            "web filtering should a systems administrator configure?"
        ),
        "name": "secplus_q399",
        "correct": "A",
        "explain": (
            "Correct. A — Agent-based web filtering runs on each laptop and enforces policy on or off the corporate "
            "network without requiring VPN or proxy tunneling. A centralized proxy routes traffic through an "
            "on-premises or cloud proxy and usually needs extra network configuration for remote users. URL "
            "scanning is a technique to evaluate addresses and is not a deployment model. Content categorization "
            "classifies sites but does not by itself deliver filtering everywhere without an agent or proxy path."
        ),
        "choices": [
            "Agent-based",
            "Centralized proxy",
            "URL scanning",
            "Content categorization",
        ],
        "objectives": ["4.6", "3.5"],
    },
    {
        "slug": "legacy-server-critical-app-segmentation",
        "title": "Security+ — Segmentation (legacy critical server)",
        "stem": (
            "Which of the following would be the best way to handle a critical business application that is running "
            "on a legacy server?"
        ),
        "name": "secplus_q400",
        "correct": "A",
        "explain": (
            "Correct. A — Segmentation places the legacy server on a restricted network zone so the critical "
            "application can continue operating while limiting exposure when patches or replacement are difficult. "
            "Isolation may be too restrictive if the application requires connectivity to other business systems. "
            "Hardening is valuable but legacy platforms often lack full vendor support for secure configuration. "
            "Decommissioning removes the server and is not viable while the application remains business-critical."
        ),
        "choices": [
            "Segmentation",
            "Isolation",
            "Hardening",
            "Decommissioning",
        ],
        "objectives": ["3.3", "4.1"],
    },
    {
        "slug": "firewall-rules-change-management-procedure",
        "title": "Security+ — Change management (firewall rules)",
        "stem": (
            "Which of the following should a security administrator adhere to when setting up a new set of firewall "
            "rules?"
        ),
        "name": "secplus_q401",
        "correct": "D",
        "explain": (
            "Correct. D — Change management procedures require approval, testing, documentation, and rollback "
            "planning before production firewall changes. A disaster recovery plan addresses restoring operations "
            "after major outages. An incident response procedure guides handling active security events. A business "
            "continuity plan maintains critical functions during disruption and does not govern routine rule changes."
        ),
        "choices": [
            "Disaster recovery plan",
            "Incident response procedure",
            "Business continuity plan",
            "Change management procedure",
        ],
        "objectives": ["5.5", "4.6"],
    },
    {
        "slug": "insider-malicious-code-peer-review-approval",
        "title": "Security+ — Peer review (insider dev code)",
        "stem": (
            "Which of the following practices would be best to prevent an insider from introducing malicious code "
            "into a company's development process?"
        ),
        "name": "secplus_q402",
        "correct": "D",
        "explain": (
            "Correct. D — Mandatory peer review and approval before code is merged adds oversight so one insider "
            "cannot silently insert malicious changes. Vulnerability scanning finds common flaws but may miss "
            "intentional backdoors. Open-source component usage increases supply chain exposure rather than "
            "blocking insider tampering. Quality assurance testing validates functionality and may not detect "
            "deliberate malicious logic hidden in approved features."
        ),
        "choices": [
            "Code scanning for vulnerabilities",
            "Open-source component usage",
            "Quality assurance testing",
            "Peer review and approval",
        ],
        "objectives": ["5.1", "5.5"],
    },
    {
        "slug": "smartphone-unauthorized-software-jailbreaking",
        "title": "Security+ — Jailbreaking (unauthorized mobile apps)",
        "stem": (
            "A user would like to install software and features that are not available with a smartphone's default "
            "software. Which of the following would allow the user to install unauthorized software and enable new "
            "features?"
        ),
        "name": "secplus_q403",
        "correct": "C",
        "explain": (
            "Correct. C — Jailbreaking removes manufacturer restrictions on a mobile device so users can install "
            "unauthorized applications and enable capabilities outside the default OS. Side loading installs apps "
            "from unofficial sources but does not by itself unlock all restricted system features. Cross-site "
            "scripting is a web application attack. SOU is not a standard mobile security term on the exam."
        ),
        "choices": [
            "SOU",
            "Cross-site scripting",
            "Jailbreaking",
            "Side loading",
        ],
        "objectives": ["2.3", "3.3"],
    },
    {
        "slug": "caller-id-spoof-credit-card-vishing",
        "title": "Security+ — Vishing (caller ID spoof)",
        "stem": (
            "A customer of a large company receives a phone call from someone claiming to work for the company "
            "and asking for the customer's credit card information. The customer sees the caller ID is the same as "
            "the company's main phone number. Which of the following attacks is the customer most likely a target of?"
        ),
        "name": "secplus_q404",
        "correct": "D",
        "explain": (
            "Correct. D — Vishing is social engineering over voice calls, often with caller ID spoofing to appear "
            "legitimate while requesting payment card or account data. Phishing typically uses deceptive email. "
            "Whaling targets high-level executives with tailored lures. Smishing uses SMS text messages rather than "
            "phone calls."
        ),
        "choices": [
            "Phishing",
            "Whaling",
            "Smishing",
            "Vishing",
        ],
        "objectives": ["2.2", "2.4"],
    },
    {
        "slug": "ir-documentation-next-tabletop-exercise",
        "title": "Security+ — Tabletop (after IR docs)",
        "stem": (
            "A security manager created new documentation to use in response to various types of security incidents. "
            "Which of the following is the next step the manager should take?"
        ),
        "name": "secplus_q405",
        "correct": "D",
        "explain": (
            "Correct. D — After drafting incident response documentation, a tabletop exercise validates roles, "
            "decisions, and gaps with stakeholders before a live incident. Setting maximum data retention is "
            "a records-management task unrelated to exercising new playbooks. Storing documents on an air-gapped "
            "network is not the standard follow-up to publishing usable IR procedures. Reviewing data "
            "classification may inform document handling but does not test whether the incident plans work."
        ),
        "choices": [
            "Set the maximum data retention policy.",
            "Securely store the documents on an air-gapped network.",
            "Review the documents' data classification policy.",
            "Conduct a tabletop exercise with the team.",
        ],
        "objectives": ["5.5", "4.8"],
    },
    {
        "slug": "ransomware-recovery-offline-backup-rpo-rto",
        "title": "Security+ — Offline backup (ransomware RPO/RTO)",
        "stem": (
            "The Chief Information Security Officer of an organization needs to ensure recovery from ransomware "
            "would likely occur within the organization's agreed-upon RPOs and RTOs. Which of the following backup "
            "scenarios would best ensure recovery?"
        ),
        "name": "secplus_q406",
        "correct": "B",
        "explain": (
            "Correct. B — Offline magnetic media keeps backup copies disconnected from production networks so "
            "ransomware cannot encrypt them, supporting reliable recovery within RPO and RTO targets when "
            "combined with daily full backups. Hourly differentials on a local SAN remain online and can be "
            "encrypted during an attack. Daily cloud differentials help if immutability exists but networked "
            "credentials can still be abused. Weekly full with daily incremental on NAS shares are online and "
            "commonly targeted by ransomware."
        ),
        "choices": [
            "Hourly differential backups stored on a local SAN array",
            "Daily full backups stored on premises in magnetic offline media",
            "Daily differential backups maintained by a third-party cloud provider",
            "Weekly full backups with daily incremental stored on a NAS drive",
        ],
        "objectives": ["3.6", "5.2"],
    },
    {
        "slug": "vdi-file-copy-time-based-access-control",
        "title": "Security+ — Time-based access (VDI file copy)",
        "stem": (
            "A company wants to ensure employees are allowed to copy files from a virtual desktop during the "
            "workday but are restricted during non-working hours. Which of the following security measures should "
            "the company set up?"
        ),
        "name": "secplus_q407",
        "correct": "C",
        "explain": (
            "Correct. C — Time-based access control permits or denies actions such as copying files according to "
            "defined schedules such as business hours. Digital rights management governs how content is used and "
            "distributed but is not primarily a work-hours gate for VDI clipboard or file export. Role-based access "
            "control assigns rights by job role, not time of day. Network access control admits endpoints to the "
            "network and does not schedule virtual desktop file-copy permissions."
        ),
        "choices": [
            "Digital rights management",
            "Role-based access control",
            "Time-based access control",
            "Network access control",
        ],
        "objectives": ["3.3", "5.5"],
    },
    {
        "slug": "encryption-vs-hashing-ciphertext-checksum",
        "title": "Security+ — Encryption vs hashing",
        "stem": (
            "Which of the following describes the difference between encryption and hashing?"
        ),
        "name": "secplus_q408",
        "correct": "B",
        "explain": (
            "Correct. B — Encryption is reversible with the proper key and transforms cleartext into ciphertext for "
            "confidentiality. Hashing is a one-way function that produces a fixed checksum or digest to verify "
            "integrity. Either technology may be used in transit or at rest depending on design. Encryption "
            "primarily provides confidentiality, while hashing supports integrity verification, not the reverse. "
            "Hashing does not use private-key exchange; symmetric and asymmetric encryption handle keys differently."
        ),
        "choices": [
            "Encryption protects data in transit, while hashing protects data at rest.",
            "Encryption replaces cleartext with ciphertext, while hashing calculates a checksum.",
            "Encryption ensures data integrity, while hashing ensures data confidentiality.",
            "Encryption uses a public-key exchange, while hashing uses a private key.",
        ],
        "objectives": ["1.2", "1.4"],
    },
    {
        "slug": "remote-connection-confidentiality-vpn",
        "title": "Security+ — VPN (remote confidentiality)",
        "stem": (
            "Which of the following is the best way to improve the confidentiality of remote connections to an "
            "enterprise's infrastructure?"
        ),
        "name": "secplus_q409",
        "correct": "B",
        "explain": (
            "Correct. B — Virtual private networks encrypt remote sessions so data crossing untrusted networks "
            "remains confidential. Firewalls enforce access policy but do not by themselves encrypt remote user "
            "traffic end to end. Extensive logging supports auditing and investigation, not confidentiality. "
            "Intrusion detection systems identify suspicious activity and do not protect remote session privacy."
        ),
        "choices": [
            "Firewalls",
            "Virtual private networks",
            "Extensive logging",
            "Intrusion detection systems",
        ],
        "objectives": ["3.5", "1.2"],
    },
    {
        "slug": "government-noncompliance-sanctions-concern",
        "title": "Security+ — Sanctions (regulatory noncompliance)",
        "stem": (
            "Which of the following would be the greatest concern for a company that is aware of the consequences "
            "of non-compliance with government regulations?"
        ),
        "name": "secplus_q410",
        "correct": "B",
        "explain": (
            "Correct. B — Sanctions such as fines, penalties, and legal restrictions are the primary government "
            "consequences organizations seek to avoid when regulations apply. The right to be forgotten is an "
            "individual privacy right under some laws, not the overarching penalty for corporate non-compliance. "
            "External compliance reporting demonstrates adherence to regulators. Attestation is evidence that "
            "controls meet requirements, not the penalty for failing them."
        ),
        "choices": [
            "Right to be forgotten",
            "Sanctions",
            "External compliance reporting",
            "Attestation",
        ],
        "objectives": ["5.6", "5.4"],
    },
    {
        "slug": "soc-just-in-time-playbook-reference",
        "title": "Security+ — Playbook (SOC reference)",
        "stem": (
            "Which of the following is most likely to be used as a just-in-time reference document within a "
            "security operations center?"
        ),
        "name": "secplus_q411",
        "correct": "C",
        "explain": (
            "Correct. C — Playbooks provide step-by-step procedures analysts follow during active incidents or "
            "repeatable SOC tasks. A change management policy governs how production changes are approved. A "
            "risk profile summarizes organizational risk posture for planning. A SIEM profile may tune detection "
            "rules or user behavior baselines but is not the primary just-in-time operational runbook."
        ),
        "choices": [
            "Change management policy",
            "Risk profile",
            "Playbook",
            "SIEM profile",
        ],
        "objectives": ["4.9", "5.5"],
    },
    {
        "slug": "compliance-segmentation-firewall-block-external",
        "title": "Security+ — Firewall rules (segmentation)",
        "stem": (
            "As part of new compliance audit requirements, multiple servers need to be segmented on different "
            "networks and should be reachable only from authorized internal systems. Which of the following would "
            "meet the requirements?"
        ),
        "name": "secplus_q412",
        "correct": "A",
        "explain": (
            "Correct. A — Firewall rules enforce network segmentation by blocking external access and permitting "
            "only approved internal sources to reach each segment. A wireless access point for public network "
            "access would expose internal resources outward, not isolate them. An IPSec tunnel secures traffic "
            "between endpoints but does not by itself place servers on separate restricted segments. An internal "
            "jump server centralizes administrative access but is not the primary control for segmenting many "
            "servers across networks."
        ),
        "choices": [
            "Configure firewall rules to block external access to internal resources.",
            "Set up a WAP to allow internal access from public networks.",
            "Implement a new IPSec tunnel from internal resources.",
            "Deploy an internal jump server to access resources.",
        ],
        "objectives": ["3.3", "4.6"],
    },
    {
        "slug": "intellectual-property-awareness-insider-threat",
        "title": "Security+ — Insider threat (IP awareness)",
        "stem": (
            "An organization maintains intellectual property that it wants to protect. Which of the following "
            "concepts would be most beneficial to add to the company's security awareness training program?"
        ),
        "name": "secplus_q413",
        "correct": "A",
        "explain": (
            "Correct. A — Insider threat awareness teaches employees to recognize and report risky or malicious "
            "handling of proprietary information by people with legitimate access. Simulated threats and phishing "
            "awareness focus on external social engineering rather than protecting IP from trusted insiders. "
            "Business continuity planning addresses maintaining operations during disruptions, not day-to-day "
            "safeguarding of intellectual property."
        ),
        "choices": [
            "Insider threat detection",
            "Simulated threats",
            "Phishing awareness",
            "Business continuity planning",
        ],
        "objectives": ["5.4", "2.1"],
    },
    {
        "slug": "unauthorized-website-aup-violation",
        "title": "Security+ — AUP (unauthorized website)",
        "stem": (
            "A new employee accessed an unauthorized website. An investigation found that the employee violated "
            "the company's rules. Which of the following did the employee violate?"
        ),
        "name": "secplus_q414",
        "correct": "B",
        "explain": (
            "Correct. B — An acceptable use policy defines permitted behavior on company systems, including which "
            "websites and resources employees may access. A memorandum of understanding states mutual intent "
            "between organizations. A non-disclosure agreement protects confidential information shared with "
            "third parties. A memorandum of agreement formalizes responsibilities between parties for joint work."
        ),
        "choices": [
            "MOU",
            "AUP",
            "NDA",
            "MOA",
        ],
        "objectives": ["5.4", "5.3"],
    },
    {
        "slug": "regulatory-audit-gap-analysis-self-assessment",
        "title": "Security+ — Self-assessment (audit gap analysis)",
        "stem": (
            "A company prepares for an upcoming regulatory audit. The company wants to perform a gap analysis "
            "in the most cost-effective way. Which of the following will help the company achieve this goal?"
        ),
        "name": "secplus_q415",
        "correct": "A",
        "explain": (
            "Correct. A — An internal self-assessment compares current controls to regulatory requirements using "
            "existing staff before paying for external tests. Active reconnaissance probes external attack "
            "surface and does not map controls to audit frameworks. A red team penetration test is valuable "
            "but costly and is not the most cost-effective gap analysis method. A tabletop exercise rehearses "
            "incident response and does not systematically measure regulatory compliance gaps."
        ),
        "choices": [
            "Internal self-assessment",
            "Active reconnaissance",
            "Red team penetration test",
            "Tabletop exercise",
        ],
        "objectives": ["5.1", "5.4"],
    },
    {
        "slug": "sso-access-tokens-oauth-authorization",
        "title": "Security+ — OAuth (SSO access tokens)",
        "stem": (
            "An organization has recently decided to implement SSO. The requirements are to leverage access tokens "
            "and focus on application authorization rather than user authentication. Which of the following "
            "solutions would the engineering team most likely configure?"
        ),
        "name": "secplus_q416",
        "correct": "D",
        "explain": (
            "Correct. D — OAuth issues access tokens that authorize applications to act on behalf of users without "
            "handling primary authentication itself. LDAP provides directory authentication services. Federation "
            "describes trust relationships between domains but is not a specific token protocol. SAML exchanges "
            "assertions for browser SSO and is more commonly tied to authentication federation than OAuth-style "
            "application authorization tokens."
        ),
        "choices": [
            "LDAP",
            "Federation",
            "SAML",
            "OAuth",
        ],
        "objectives": ["3.8", "5.5"],
    },
    {
        "slug": "recovery-site-warm-no-immediate-failover",
        "title": "Security+ — Warm site (no immediate failover)",
        "stem": (
            "A business needs a recovery site but does not require immediate failover. The business also wants to "
            "reduce the workload required to recover from an outage. Which of the following recovery sites is the "
            "best option?"
        ),
        "name": "secplus_q417",
        "correct": "C",
        "explain": (
            "Correct. C — A warm site pre-stages partial infrastructure and data so recovery takes less effort "
            "than a cold site while avoiding the cost of instant hot-site failover. A hot site supports immediate "
            "failover, which the business does not require. A cold site is cheapest but requires the most rebuild "
            "work during recovery. Geographically dispersed describes backup location strategy, not a recovery "
            "site tier with staged systems."
        ),
        "choices": [
            "Hot",
            "Cold",
            "Warm",
            "Geographically dispersed",
        ],
        "objectives": ["3.4", "5.2"],
    },
    {
        "slug": "vendor-installer-hash-integrity-verification",
        "title": "Security+ — Hash integrity (vendor installer)",
        "stem": (
            "For which of the following reasons would a systems administrator leverage a hash from an installer "
            "file that is posted on a vendor's website?"
        ),
        "name": "secplus_q418",
        "correct": "A",
        "explain": (
            "Correct. A — Comparing a locally computed hash to the value published by the vendor verifies the "
            "installer was not altered or corrupted during download. Digital signatures or code signing validate "
            "authenticity of the publisher, not a simple hash comparison alone. A hash does not activate software "
            "licenses. Calculating a checksum is the method used; the reason is to confirm file integrity against "
            "the vendor-provided value."
        ),
        "choices": [
            "To test the integrity of the file",
            "To validate the authenticity of the file",
            "To activate the license for the file",
            "To calculate the checksum of the file",
        ],
        "objectives": ["1.2", "1.4"],
    },
    {
        "slug": "microsegmentation-software-defined-networking",
        "title": "Security+ — SDN (microsegmentation)",
        "stem": (
            "Which of the following technologies can achieve microsegmentation?"
        ),
        "name": "secplus_q419",
        "correct": "B",
        "explain": (
            "Correct. B — Software-defined networking enables granular, policy-driven segmentation down to "
            "individual workloads or applications. Next-generation firewalls enforce security at boundaries but "
            "are not the primary technology for fine-grained east-west microsegmentation. Embedded systems are "
            "specialized control devices, not a network virtualization layer. Air-gapped networks are physically "
            "isolated and do not provide internal microsegmentation within a connected environment."
        ),
        "choices": [
            "Next-generation firewalls",
            "Software-defined networking",
            "Embedded systems",
            "Air-gapped",
        ],
        "objectives": ["3.1", "3.4"],
    },
    {
        "slug": "mfa-push-notifications-byod-seamless",
        "title": "Security+ — Push notifications (MFA BYOD)",
        "stem": (
            "A company is currently utilizing usernames and passwords, and it wants to integrate an MFA method that "
            "is seamless, can integrate easily into a user's workflow, and can utilize employee-owned devices. "
            "Which of the following will meet these requirements?"
        ),
        "name": "secplus_q420",
        "correct": "A",
        "explain": (
            "Correct. A — Push notifications to an authenticator app on a personal smartphone provide quick "
            "approve-or-deny MFA with minimal workflow disruption. Phone calls are slower and more intrusive. "
            "Smart cards require company-issued hardware rather than employee-owned phones. Offline backup codes "
            "are a fallback method and are not a seamless primary MFA experience."
        ),
        "choices": [
            "Push notifications",
            "Phone call",
            "Smart card",
            "Offline backup codes",
        ],
        "objectives": ["3.8", "5.5"],
    },
    {
        "slug": "network-traffic-transit-tls-encrypted-protocols",
        "title": "Security+ — TLS (traffic in transit)",
        "stem": (
            "A network administrator wants to ensure that network traffic is highly secure while in transit. Which "
            "of the following actions best describes the actions the network administrator should take?"
        ),
        "name": "secplus_q421",
        "correct": "B",
        "explain": (
            "Correct. B — Requiring TLS and other encrypted protocols protects confidentiality and integrity of "
            "data in transit while permitting only authorized secure traffic. NAC and firewall policies control "
            "admission and access but do not by themselves encrypt all transit data. Blocking HTTPS directory "
            "traversal at the IPS addresses one attack pattern, not comprehensive in-transit protection. EDR "
            "monitors endpoints for malware and unauthorized applications, not encryption of network flows."
        ),
        "choices": [
            (
                "Ensure that NAC is enforced on all network segments, and confirm that firewalls have updated "
                "policies to block unauthorized traffic."
            ),
            (
                "Ensure only TLS and other encrypted protocols are selected for use on the network, and only "
                "permit authorized traffic via secure protocols."
            ),
            (
                "Configure the perimeter IPS to block inbound HTTPS directory traversal traffic, and verify "
                "that signatures are updated on a daily basis."
            ),
            (
                "Ensure the EDR software monitors for unauthorized applications that could be used by threat "
                "actors, and configure alerts for the security team."
            ),
        ],
        "objectives": ["1.2", "4.6"],
    },
    {
        "slug": "patch-update-secure-baseline-sop",
        "title": "Security+ — SOP (patch secure baseline)",
        "stem": (
            "Which of the following would a security administrator use to comply with a secure baseline during a "
            "patch update?"
        ),
        "name": "secplus_q422",
        "correct": "C",
        "explain": (
            "Correct. C — A standard operating procedure documents step-by-step tasks to apply patches while "
            "maintaining the secure baseline configuration. An information security policy sets high-level "
            "requirements but not operational patch steps. Service-level expectations define performance "
            "targets such as uptime, not how to harden systems during maintenance. A test result report records "
            "outcomes after testing rather than guiding baseline compliance during the update."
        ),
        "choices": [
            "Information security policy",
            "Service-level expectations",
            "Standard operating procedure",
            "Test result report",
        ],
        "objectives": ["4.1", "5.1"],
    },
    {
        "slug": "application-out-of-scope-management-attestation",
        "title": "Security+ — Attestation (app out of scope)",
        "stem": (
            "The internal audit team determines a software application is no longer in scope for external reporting "
            "requirements. Which of the following will confirm management's perspective that the application is no "
            "longer applicable?"
        ),
        "name": "secplus_q423",
        "correct": "D",
        "explain": (
            "Correct. D — Management acknowledgement and attestation formally documents that leadership accepts "
            "the application is out of scope for external reporting. Data inventory and retention track what "
            "exists and how long it is kept but do not by themselves record management sign-off. The right to "
            "be forgotten is an individual data privacy request. Due care and due diligence describe reasonable "
            "effort standards, not formal scope confirmation."
        ),
        "choices": [
            "Data inventory and retention",
            "Right to be forgotten",
            "Due care and due diligence",
            "Acknowledgement and attestation",
        ],
        "objectives": ["5.6", "5.3"],
    },
    {
        "slug": "remote-malicious-urls-sase-inline-filtering",
        "title": "Security+ — SASE (malicious URL filtering)",
        "stem": (
            "A security analyst must prevent remote users from accessing malicious URLs. The sites need to be "
            "checked inline for reputation, content, or categorization. Which of the following technologies will "
            "help secure the enterprise?"
        ),
        "name": "secplus_q424",
        "correct": "B",
        "explain": (
            "Correct. B — Secure access service edge (SASE) delivers cloud-based secure web gateway and "
            "policy enforcement so remote traffic is inspected inline for URL reputation, content, and "
            "categorization. A VPN encrypts remote access but does not by itself provide inline malicious URL "
            "filtering. An IDS detects network attacks and does not block URLs based on reputation. SD-WAN "
            "optimizes wide-area routing and is not primarily a URL security inspection platform."
        ),
        "choices": [
            "VPN",
            "SASE",
            "IDS",
            "SD-WAN",
        ],
        "objectives": ["4.6", "3.5"],
    },
    {
        "slug": "government-project-data-confidential-restricted",
        "title": "Security+ — Data classification (government project)",
        "stem": (
            "A company is developing a critical system for the government and storing project information on a "
            "fileshare. Which of the following describes how this data will most likely be classified? (Select two.)"
        ),
        "name": "secplus_q425",
        "choose_two": True,
        "correct": ["B", "F"],
        "explain": (
            "Correct. B and F — Government critical-system project files require strong protection and are "
            "classified as confidential and often restricted to limit access to authorized personnel only. "
            "Private is a lower commercial label and is not the standard pair for sensitive government work. "
            "Public classification would expose information inappropriately. Operational and urgent describe "
            "priority or use, not data sensitivity labels."
        ),
        "choices": [
            "Private",
            "Confidential",
            "Public",
            "Operational",
            "Urgent",
            "Restricted",
        ],
        "objectives": ["5.2", "5.5"],
    },
    {
        "slug": "risk-transfer-cost-vs-impact-ale",
        "title": "Security+ — ALE (risk transfer vs impact)",
        "stem": (
            "Which of the following would be most useful in determining whether the long-term cost to transfer a "
            "risk is less than the impact of the risk?"
        ),
        "name": "secplus_q426",
        "correct": "D",
        "explain": (
            "Correct. D — Annualized loss expectancy (ALE) equals single loss expectancy (SLE) times annual rate "
            "of occurrence (ARO), giving expected yearly monetary impact. Organizations compare ALE to recurring "
            "transfer costs such as insurance premiums to decide if risk transfer is economical. ARO is only "
            "frequency, not total annual loss. RTO and RPO are disaster-recovery time and data-loss objectives. "
            "SLE measures one incident, not the long-term annualized impact used for transfer decisions."
        ),
        "choices": [
            "ARO",
            "RTO",
            "RPO",
            "ALE",
            "SLE",
        ],
        "objectives": ["1.2", "5.1"],
    },
    {
        "slug": "suspicious-ip-logins-mfa-prevention",
        "title": "Security+ — MFA (suspicious IP logins)",
        "stem": (
            "An administrator notices that several users are logging in from suspicious IP addresses. After "
            "speaking with the users, the administrator determines that the employees were not logging in from those IP "
            "addresses and resets the affected users' passwords. Which of the following should the administrator "
            "implement to prevent this type of attack from succeeding in the future?"
        ),
        "name": "secplus_q427",
        "correct": "A",
        "explain": (
            "Correct. A — Multifactor authentication requires a second factor beyond the password, so stolen or "
            "reused credentials alone cannot complete sign-in from attacker-controlled IP addresses. Permissions "
            "assignment defines what authorized users may access after login; it does not stop fraudulent "
            "authentication. Access management is broad identity governance and is less specific than MFA for "
            "blocking credential abuse. Password complexity makes guessing harder but does not stop use of "
            "phished, leaked, or reset credentials."
        ),
        "choices": [
            "Multifactor authentication",
            "Permissions assignment",
            "Access management",
            "Password complexity",
        ],
        "objectives": ["3.4", "5.4"],
    },
    {
        "slug": "soc-benign-activity-alert-tuning",
        "title": "Security+ — Alert tuning (benign activity)",
        "stem": (
            "A security operations center determines that the malicious activity detected on a server is normal. "
            "Which of the following activities describes the act of ignoring detected activity in the future?"
        ),
        "name": "secplus_q428",
        "correct": "A",
        "explain": (
            "Correct. A — Tuning adjusts detection rules, thresholds, or baselines so known-benign behavior no "
            "longer raises alerts, reducing false positives without stopping monitoring entirely. Aggregating "
            "combines log and event data for analysis but does not suppress future detections. Quarantining "
            "isolates hosts or files to contain threats. Archiving stores historical records for retention and "
            "is not the process of excluding normal activity from alerting."
        ),
        "choices": [
            "Tuning",
            "Aggregating",
            "Quarantining",
            "Archiving",
        ],
        "objectives": ["4.3", "4.5"],
    },
    {
        "slug": "database-trap-user-honeytoken",
        "title": "Security+ — Honeytoken (database trap account)",
        "stem": (
            "A company discovers suspicious transactions that were entered into the company's database and "
            "attached to a user account that was created as a trap for malicious activity. Which of the following "
            "is the user account an example of?"
        ),
        "name": "secplus_q429",
        "correct": "A",
        "explain": (
            "Correct. A — A honeytoken is decoy data such as fake credentials, records, or accounts planted to "
            "detect unauthorized use; activity tied to the trap account signals an attacker interacting with bait. "
            "A honeynet is a network of decoy systems. A honeypot is a decoy host or service meant to attract "
            "attackers. A honeyfile is a planted file that alerts when opened, not a database user account."
        ),
        "choices": [
            "Honeytoken",
            "Honeynet",
            "Honeypot",
            "Honeyfile",
        ],
        "objectives": ["4.8", "1.1"],
    },
    {
        "slug": "privacy-compliance-data-protection-policies-first",
        "title": "Security+ — Privacy compliance (policies first)",
        "stem": (
            "A company processes and stores sensitive data on its own systems. Which of the following steps "
            "should the company take first to ensure compliance with privacy regulations?"
        ),
        "name": "secplus_q430",
        "correct": "B",
        "explain": (
            "Correct. B — Privacy compliance begins with data protection policies aligned to legal requirements "
            "and staff training so the organization knows what sensitive data it holds and how it may be used, "
            "shared, and retained. Access controls and encryption are essential technical safeguards but follow "
            "governance that defines requirements. Incident response and disaster recovery plans support resilience "
            "but are not the first privacy-compliance step. Purchasing security software without policy and "
            "process alignment does not establish regulatory accountability."
        ),
        "choices": [
            "Implement access controls and encryption.",
            "Develop and provide training on data protection policies.",
            "Create incident response and disaster recovery plans.",
            "Purchase and install security software.",
        ],
        "objectives": ["5.7", "5.8"],
    },
    {
        "slug": "two-companies-secure-connectivity-vpn",
        "title": "Security+ — VPN (inter-company connectivity)",
        "stem": (
            "An administrator must implement a solution that provides security and network connectivity between "
            "two companies. Which of the following infrastructure solutions is the best for this purpose?"
        ),
        "name": "secplus_q431",
        "correct": "B",
        "explain": (
            "Correct. B — A VPN creates an encrypted tunnel between organizations so traffic crosses untrusted "
            "networks securely, which is the standard approach for site-to-site or partner connectivity. A UTM "
            "bundles perimeter security functions for one site but is not the primary inter-company link. NAC "
            "enforces endpoint admission to a local network and does not connect two separate companies. An NGFW "
            "filters and inspects traffic at a perimeter but pairing organizations still relies on VPN or similar "
            "encrypted connectivity between sites."
        ),
        "choices": [
            "UTM",
            "VPN",
            "NAC",
            "NGFW",
        ],
        "objectives": ["4.6", "3.5"],
    },
    {
        "slug": "retail-site-miscategorized-gambling-content-filter",
        "title": "Security+ — Content filter categorization (retail site)",
        "stem": (
            "Users at a company are reporting they are unable to access the URL for a new retail website because "
            "it is flagged as gambling and is being blocked. Which of the following changes would allow users to "
            "access the site?"
        ),
        "name": "secplus_q432",
        "correct": "D",
        "explain": (
            "Correct. D — Web or URL content filters block sites by category; a miscategorized retail URL must be "
            "recategorized or allowlisted in the filter so legitimate shopping traffic is permitted. A generic "
            "firewall HTTPS permit rule does not fix category-based blocking and is overly broad. An IPS permits "
            "or blocks attack signatures, not gambling versus shopping URL categories. DLP rules that detect "
            "credit card data govern sensitive data movement, not URL reputation or site classification."
        ),
        "choices": [
            "Creating a firewall rule to allow HTTPS traffic",
            "Configuring the IPS to allow shopping",
            "Tuning the DLP rule that detects credit card data",
            "Updating the categorization in the content filter",
        ],
        "objectives": ["4.6", "3.3"],
    },
    {
        "slug": "shredded-devices-legal-backup-data-retention",
        "title": "Security+ — Data retention (shredded devices)",
        "stem": (
            "A legal department must maintain a backup from all devices that have been shredded and recycled by "
            "a third party. Which of the following best describes this requirement?"
        ),
        "name": "secplus_q433",
        "correct": "A",
        "explain": (
            "Correct. A — Data retention policies define how long information must be preserved, including backups "
            "kept after hardware is destroyed so legal and regulatory obligations can still be met. Certification "
            "documents that a vendor performed destruction to an agreed standard but does not describe maintaining "
            "archived copies. Sanitization removes data from media before reuse or disposal. Destruction is the "
            "physical shredding or recycling process itself, not the legal requirement to retain backups afterward."
        ),
        "choices": [
            "Data retention",
            "Certification",
            "Sanitation",
            "Destruction",
        ],
        "objectives": ["5.4", "5.7"],
    },
    {
        "slug": "classified-sensitive-data-exfiltration-dlp",
        "title": "Security+ — DLP (classified data exfiltration)",
        "stem": (
            "An IT manager is increasing the security capabilities of an organization after a data classification "
            "initiative determined that sensitive data could be exfiltrated from the environment. Which of the "
            "following solutions would mitigate the risk?"
        ),
        "name": "secplus_q434",
        "correct": "C",
        "explain": (
            "Correct. C — Data loss prevention monitors and blocks sensitive data leaving the environment across "
            "email, web, endpoints, and cloud channels using classification labels and content inspection. XDR "
            "correlates threat telemetry for detection and response but is not primarily a data-exfiltration control. "
            "SPF validates authorized mail senders for a domain and does not stop outbound sensitive files. DMARC "
            "builds on SPF and DKIM to reduce email spoofing and phishing abuse, not unauthorized data leakage."
        ),
        "choices": [
            "XDR",
            "SPF",
            "DLP",
            "DMARC",
        ],
        "objectives": ["3.3", "4.2"],
    },
    {
        "slug": "cope-mdm-policy-remote-wipe-encryption",
        "title": "Security+ — COPE policy (select two)",
        "stem": (
            "An organization is implementing a COPE mobile device management policy. Which of the following "
            "should the organization include in the COPE policy? (Select two.)"
        ),
        "name": "secplus_q435",
        "choose_two": True,
        "correct": ["A", "B"],
        "explain": (
            "Correct. A and B — COPE devices are company-owned but allow limited personal use; the policy must "
            "protect corporate data with remote wipe if a device is lost or an employee leaves and with encryption "
            "so data at rest stays confidential. Password length alone is one control and does not by itself define "
            "COPE governance. Data usage caps address billing, not core security policy. Employee data ownership "
            "aligns with BYOD, where users own devices and data separation is negotiated. Personal app store access "
            "may be permitted under COPE but is a usage allowance, not a required security control in the policy."
        ),
        "choices": [
            "Remote wiping of the device",
            "Data encryption",
            "Requiring passwords with eight characters",
            "Data usage caps",
            "Employee data ownership",
            "Personal application store access",
        ],
        "objectives": ["4.1", "4.6"],
    },
    {
        "slug": "cloud-responsibility-matrix-customer-data",
        "title": "Security+ — Responsibility matrix (customer data)",
        "stem": (
            "Which of the following is most likely in a responsibility matrix in a cloud computing environment?"
        ),
        "name": "secplus_q436",
        "correct": "A",
        "explain": (
            "Correct. A — Under the shared responsibility model, the customer always owns protection of their "
            "information and data in IaaS, PaaS, and SaaS; the matrix documents that obligation regardless of "
            "service model. The cloud provider offers identity services but the customer configures accounts, "
            "access, and connected-device governance in most models. Physical network infrastructure is a provider "
            "responsibility. Endpoint security for devices connecting to cloud services remains with the customer."
        ),
        "choices": [
            "The customer is responsible for information and data regardless of the cloud model used.",
            "The cloud provider is responsible for account and identity management for connected devices.",
            "The customer and the cloud provider share responsibility for the physical network infrastructure.",
            "The cloud provider is responsible for the security of endpoints connected to the infrastructure.",
        ],
        "objectives": ["3.4", "5.1"],
    },
    {
        "slug": "database-access-hardening-jump-server-hbf",
        "title": "Security+ — Database access hardening (select two)",
        "stem": (
            "Which of the following will harden access to a new database system? (Select two)"
        ),
        "name": "secplus_q437",
        "choose_two": True,
        "correct": ["A", "E"],
        "explain": (
            "Correct. A and E — A jump server forces administrative connections through a hardened bastion "
            "instead of direct access from many workstations, centralizing control and logging. A host-based "
            "firewall on the database host restricts which sources and ports may reach the database service. A "
            "network IDS detects suspicious traffic but does not by itself restrict who may connect. Monitoring "
            "supports detection and audit but is not an access-hardening control. A proxy can filter some traffic "
            "but is not the primary database access pattern on the exam. A WAF protects web applications at HTTP "
            "layer, not typical database listener access."
        ),
        "choices": [
            "Jump server",
            "NIDS",
            "Monitoring",
            "Proxy server",
            "Host-based firewall",
            "WAF",
        ],
        "objectives": ["4.1", "3.2"],
    },
    {
        "slug": "cloud-hosting-virtualization-isolation-resources",
        "title": "Security+ — Virtualization and isolation (cloud hosting)",
        "stem": (
            "A security team is setting up a new environment for hosting the organization's on-premises software "
            "application as a cloud-based service. Which of the following should the team ensure is in place in order "
            "for the organization to follow security best practices?"
        ),
        "name": "secplus_q438",
        "correct": "A",
        "explain": (
            "Correct. A — Cloud delivery relies on virtualization with strong isolation between workloads and tenants "
            "so applications on shared hardware do not interfere or leak data across boundaries. (Exam items may spell "
            "this as visualization; the intent is virtualization.) Network segmentation protects traffic paths but "
            "does not by itself establish compute isolation in the cloud stack. Data encryption and strong "
            "authentication are required controls but are not the foundational architectural practice for hosting "
            "applications securely as a cloud service."
        ),
        "choices": [
            "Visualization and isolation of resources",
            "Network segmentation",
            "Data encryption",
            "Strong authentication policies",
        ],
        "objectives": ["3.4", "4.1"],
    },
    {
        "slug": "sms-otp-riskier-than-totp-interception",
        "title": "Security+ — SMS OTP vs TOTP risk",
        "stem": (
            "Which of the following best describes why the SMS OTP authentication method is more risky to "
            "implement than the TOTP method?"
        ),
        "name": "secplus_q439",
        "correct": "C",
        "explain": (
            "Correct. C — SMS one-time codes travel over the cellular network and can be intercepted, redirected "
            "through SIM swap or SS7 abuse, or exposed on the device, while TOTP codes are generated locally in "
            "an authenticator app and are not sent over SMS. Requiring active mobile service is an operational "
            "dependency, not the primary security weakness. Longer SMS code validity increases exposure time but "
            "interception risk is the core reason SMS OTP is considered weaker than TOTP. SMS codes are issued by "
            "a service provider; TOTP uses standard HMAC-based algorithms—the issue is delivery channel risk, not a "
            "weaker OTP generation algorithm on the phone."
        ),
        "choices": [
            "The SMS OTP method requires an end user to have an active mobile telephone service and SIM card.",
            "Generally, SMS OTP codes are valid for up to 15 minutes while the TOTP time frame is 30 to 60 seconds",
            "The SMS OTP is more likely to be intercepted and lead to unauthorized disclosure of the code than the TOTP method.",
            "The algorithm used to generate an SMS OTP code is weaker than the one used to generate a TOTP code",
        ],
        "objectives": ["3.4", "5.4"],
    },
    {
        "slug": "login-database-breach-impact-password-hashing",
        "title": "Security+ — Hashing (login database breach)",
        "stem": (
            "An organization wants to limit potential impact to its log-in database in the event of a breach. Which of "
            "the following options is the security team most likely to recommend?"
        ),
        "name": "secplus_q440",
        "correct": "B",
        "explain": (
            "Correct. B — Storing password verifiers as salted one-way hashes limits breach impact because attackers "
            "obtain digests rather than reusable plaintext credentials. Tokenization replaces sensitive values with "
            "tokens, commonly for payment or lookup data, not standard password storage in authentication databases. "
            "Obfuscation hides format but is reversible and does not provide strong credential protection. "
            "Segmentation reduces lateral movement in the network but does not protect stored credentials if the "
            "database itself is exfiltrated."
        ),
        "choices": [
            "Tokenization",
            "Hashing",
            "Obfuscation",
            "Segmentation",
        ],
        "objectives": ["1.4", "4.5"],
    },
    {
        "slug": "dpo-data-inventory-breach-impact",
        "title": "Security+ — Data inventory (DPO breach impact)",
        "stem": (
            "Which of the following is the most relevant reason a DPO would develop a data inventory?"
        ),
        "name": "secplus_q441",
        "correct": "B",
        "explain": (
            "Correct. B — A data protection officer maintains a data inventory to map what personal and sensitive "
            "information exists, where it resides, and who processes it so breach impact, notification scope, and "
            "regulatory obligations can be assessed quickly. Storage capacity planning is an IT operations concern, "
            "not the primary privacy driver. Inventories support lawful retention limits and minimization rather than "
            "extending how long data is kept. Deduplication improves data quality and efficiency but is not the core "
            "reason a DPO builds an inventory for compliance."
        ),
        "choices": [
            "To manage data storage requirements better",
            "To determine the impact in the event of a breach",
            "To extend the length of time data can be retained",
            "To automate the reduction of duplicated data",
        ],
        "objectives": ["5.7", "5.8"],
    },
    {
        "slug": "environmental-variables-vulnerability-scope-impact",
        "title": "Security+ — Environmental variables (vulnerability review)",
        "stem": (
            "Which of the following is a reason environmental variables are a concern when reviewing potential "
            "system vulnerabilities?"
        ),
        "name": "secplus_q442",
        "correct": "A",
        "explain": (
            "Correct. A — Environment variables can hold paths, credentials, and configuration that change how far "
            "an exploit spreads or what data is exposed, so reviewers must assess their contents when scoring scope "
            "and impact. Overwriting in-memory values may occur in specific attacks but is not the primary reason "
            "they matter during vulnerability review. They do not define system-wide cryptographic standards. Patch "
            "scheduling is governed by change and patch management processes, not environment variables."
        ),
        "choices": [
            "The contents of environmental variables could affect the scope and impact of an exploited vulnerability.",
            "In-memory environmental variable values can be overwritten and used by attackers to insert malicious code.",
            "Environmental variables define cryptographic standards for the system and could create vulnerabilities if deprecated algorithms are used.",
            "Environmental variables will determine when updates are run and could mitigate the likelihood of vulnerability exploitation.",
        ],
        "objectives": ["2.3", "4.1"],
    },
    {
        "slug": "server-replacement-cost-quantitative-risk-analysis",
        "title": "Security+ — Quantitative risk analysis (server cost)",
        "stem": (
            "An administrator is estimating the cost associated with an attack that could result in the replacement of "
            "a physical server. Which of the following processes is the administrator performing?"
        ),
        "name": "secplus_q443",
        "correct": "A",
        "explain": (
            "Correct. A — Quantitative risk analysis assigns numeric values such as replacement cost, downtime, and "
            "annualized loss to threats and controls. A disaster recovery test exercises recovery procedures rather "
            "than estimating attack cost. A physical security controls review evaluates facility protections, not "
            "financial impact modeling. Threat modeling maps threats, assets, and mitigations but does not by itself "
            "mean calculating dollar costs of server replacement."
        ),
        "choices": [
            "Quantitative risk analysis",
            "Disaster recovery test",
            "Physical security controls review",
            "Threat modeling",
        ],
        "objectives": ["1.2", "5.1"],
    },
    {
        "slug": "cloud-adoption-saas-vendor-patching",
        "title": "Security+ — SaaS (vendor patching goal)",
        "stem": (
            "While considering the organization's cloud-adoption strategy, the Chief Information Security Officer "
            "sets a goal to outsource patching of firmware, operating systems, and applications to the chosen cloud "
            "vendor. Which of the following best meets this goal?"
        ),
        "name": "secplus_q444",
        "correct": "E",
        "explain": (
            "Correct. E — In SaaS the provider maintains the full application stack, including firmware on "
            "underlying infrastructure, operating systems, and the application itself; the customer focuses on "
            "data, identity, and configuration. PaaS offloads the platform and OS but the customer still patches "
            "applications they deploy. IaaS leaves guest OS and application patching with the customer. Community "
            "and private cloud describe deployment models, not how much patching is outsourced. Containerization "
            "is a packaging technology and does not by itself shift all patch duties to the vendor."
        ),
        "choices": [
            "Community cloud",
            "PaaS",
            "Containerization",
            "Private cloud",
            "SaaS",
            "IaaS",
        ],
        "objectives": ["3.4", "5.1"],
    },
    {
        "slug": "xss-vulnerability-input-validation-remediation",
        "title": "Security+ — Input validation (XSS remediation)",
        "stem": (
            "An administrator discovers a cross-site scripting vulnerability on a company website. Which of the "
            "following will most likely remediate the issue?"
        ),
        "name": "secplus_q445",
        "correct": "A",
        "explain": (
            "Correct. A — Input validation and output encoding reject or neutralize untrusted data before it is "
            "reflected or stored in pages, which fixes the underlying XSS flaw. An NGFW filters network traffic "
            "but does not repair application code. A vulnerability scan finds issues but does not remediate them. "
            "A WAF can block many XSS payloads as a compensating control but does not replace fixing unsafe input "
            "handling in the application."
        ),
        "choices": [
            "Input validation",
            "NGFW",
            "Vulnerability scan",
            "WAF",
        ],
        "objectives": ["2.5", "4.1"],
    },
    {
        "slug": "automation-script-knowledge-single-point-failure",
        "title": "Security+ — Script knowledge sharing (SPOF)",
        "stem": (
            "A security analyst developed a script to automate a trivial and repeatable task. Which of the following "
            "best describes the benefits of ensuring other team members understand how the script works?"
        ),
        "name": "secplus_q446",
        "correct": "D",
        "explain": (
            "Correct. D — Shared understanding ensures others can run, maintain, or fix the automation if the author "
            "is unavailable, avoiding a single point of failure in operations. Reducing implementation cost is not "
            "the primary outcome of documentation and cross-training. Identifying complexity may occur during review "
            "but is not the main benefit described. Technical debt remediation addresses accumulated design shortcuts, "
            "not team reliance on one person's script knowledge."
        ),
        "choices": [
            "To reduce implementation cost",
            "To identify complexity",
            "To remediate technical debt",
            "To prevent a single point of failure",
        ],
        "objectives": ["4.9", "5.4"],
    },
    {
        "slug": "social-engineering-training-phishing-campaign-test",
        "title": "Security+ — Phishing campaign (training effectiveness)",
        "stem": (
            "A security administrator wants to determine if the company's social engineering training is effective. "
            "Which of the following should the administrator do to complete this task?"
        ),
        "name": "secplus_q447",
        "correct": "D",
        "explain": (
            "Correct. D — A controlled phishing campaign measures whether employees still click malicious links or "
            "disclose credentials after training, providing objective evidence of program effectiveness. A honeypot "
            "detects external attackers probing systems, not employee susceptibility to social engineering. Surveys "
            "capture opinions but not real behavior under pressure. Focus groups gather qualitative feedback but do "
            "not test how staff respond to realistic lures."
        ),
        "choices": [
            "Set up a honeypot.",
            "Send out a survey.",
            "Set up a focus group.",
            "Conduct a phishing campaign.",
        ],
        "objectives": ["5.1", "2.2"],
    },
    {
        "slug": "one-way-transform-salting-complexity",
        "title": "Security+ — Salting (before hashing)",
        "stem": (
            "Which of the following is used to add extra complexity before using a one-way data transformation "
            "algorithm?"
        ),
        "name": "secplus_q448",
        "correct": "D",
        "explain": (
            "Correct. D — Salting appends or prepends unique random data to input such as passwords before hashing, "
            "so identical passwords produce different digests and rainbow tables are less effective. Key stretching "
            "repeatedly applies a one-way function to increase work factor over time rather than adding random "
            "material immediately before the first hash. Data masking obscures values for display or testing and is "
            "reversible. Steganography hides data inside other files and is unrelated to password hashing."
        ),
        "choices": [
            "Key stretching",
            "Data masking",
            "Steganography",
            "Salting",
        ],
        "objectives": ["1.4", "4.5"],
    },
    {
        "slug": "sqli-breach-input-sanitization-developers",
        "title": "Security+ — Input sanitization (SQLi prevention)",
        "stem": (
            "While investigating a recent security breach an analyst finds that an attacker gained access by SQL "
            "injection through a company website. Which of the following should the analyst recommend to the website "
            "developers to prevent this from reoccurring?"
        ),
        "name": "secplus_q449",
        "correct": "B",
        "explain": (
            "Correct. B — Input sanitization and parameterized queries prevent untrusted web input from altering "
            "database commands, which stops SQL injection at the application layer. Secure cookies protect session "
            "data in browsers but do not block malicious SQL in requests. Code signing verifies software integrity "
            "and distribution, not dynamic user input to a web application. Blocklists of bad strings are brittle and "
            "easily bypassed compared with proper input handling."
        ),
        "choices": [
            "Secure cookies",
            "Input sanitization",
            "Code signing",
            "Blocklist",
        ],
        "objectives": ["2.5", "4.1"],
    },
    {
        "slug": "byod-primary-concern-jailbreaking",
        "title": "Security+ — BYOD (jailbreaking concern)",
        "stem": (
            "Which of the following is a primary security concern for a company setting up a BYOD program?"
        ),
        "name": "secplus_q450",
        "correct": "D",
        "explain": (
            "Correct. D — BYOD allows employee-owned phones and tablets; jailbreaking or rooting bypasses "
            "manufacturer controls and weakens MDM enforcement, enabling unvetted apps and greater malware risk. "
            "End-of-life applies to unsupported systems generally, not the defining BYOD mobile risk. Buffer "
            "overflow is an application coding flaw, not a program-level BYOD concern. VM escape targets "
            "virtualization hypervisors and is not the primary issue when personal devices access corporate data."
        ),
        "choices": [
            "End of life",
            "Buffer overflow",
            "VM escape",
            "Jailbreaking",
        ],
        "objectives": ["4.1", "4.6"],
    },
    {
        "slug": "insider-pii-misuse-privacy-legislation-training",
        "title": "Security+ — Privacy legislation training (PII misuse)",
        "stem": (
            "An employee decides to collect PII data from the company's system for personal use. The employee "
            "compresses the data into a single encrypted file before sending the file to their personal email. The "
            "security department becomes aware of the attempted misuse and blocks the attachment from leaving the "
            "corporate environment. Which of the following types of employee training would most likely reduce the "
            "occurrence of this type of issue?"
        ),
        "name": "secplus_q451",
        "correct": "A",
        "explain": (
            "Correct. A — Privacy legislation training explains legal duties for handling PII, prohibited personal use, "
            "and consequences of unauthorized collection or disclosure, which directly addresses insider misuse of "
            "customer or employee data. Social engineering training targets external manipulation, not voluntary theft. "
            "Risk management is an organizational process, not the primary end-user training type for PII misuse. "
            "Company compliance training helps but privacy law training most directly covers lawful PII handling. "
            "Phishing and remote work training do not focus on improper internal collection of regulated data."
        ),
        "choices": [
            "Privacy legislation",
            "Social engineering",
            "Risk management",
            "Company compliance",
            "Phishing",
            "Remote work",
        ],
        "objectives": ["5.7", "5.8"],
    },
    {
        "slug": "c2-investigation-endpoint-logs-deleted-firewall",
        "title": "Security+ — Firewall logs (C2, cleared endpoint)",
        "stem": (
            "A security analyst is investigating a workstation that is suspected of outbound communication to a "
            "command-and-control server. During the investigation, the analyst discovered that logs on the endpoint "
            "were deleted. Which of the following logs would the analyst most likely look at next?"
        ),
        "name": "secplus_q452",
        "correct": "B",
        "explain": (
            "Correct. B — When local endpoint logs are deleted, firewall logs still record outbound connections, "
            "destinations, ports, and timestamps to identify suspected command-and-control traffic from the "
            "workstation. IPS logs may exist but the exam emphasizes perimeter firewall connection records for this "
            "scenario. ACLs are policy definitions, not the primary log source for reconstructing C2 sessions. "
            "Windows security logs reside on the same compromised endpoint and were likely cleared with other "
            "local logs."
        ),
        "choices": [
            "IPS",
            "Firewall",
            "ACL",
            "Windows security",
        ],
        "objectives": ["4.4", "4.9"],
    },
    {
        "slug": "sql-credit-card-pending-purchases-tokenization",
        "title": "Security+ — Tokenization (credit cards in SQL)",
        "stem": (
            "A database administrator is updating the company's SQL database, which stores credit card information "
            "for pending purchases. Which of the following is the best method to secure the data against a potential "
            "breach?"
        ),
        "name": "secplus_q453",
        "correct": "C",
        "explain": (
            "Correct. C — Tokenization replaces primary account numbers with non-sensitive tokens in the database "
            "while card data remains in a secure vault, limiting PCI exposure if the SQL database is breached. "
            "Hashing is one-way and prevents retrieving card numbers needed to complete pending purchases. "
            "Obfuscation is reversible and weaker than tokenization for payment data. Masking hides digits for "
            "display but does not replace stored PANs with vault-backed tokens across transactional systems."
        ),
        "choices": [
            "Hashing",
            "Obfuscation",
            "Tokenization",
            "Masking",
        ],
        "objectives": ["1.4", "3.10"],
    },
    {
        "slug": "network-share-deletions-permissions-fim",
        "title": "Security+ — FIM (network share changes)",
        "stem": (
            "An organization has issues with deleted network share data and improper permissions. Which solution "
            "helps track and remediate these?"
        ),
        "name": "secplus_q454",
        "correct": "C",
        "explain": (
            "Correct. C — File integrity monitoring detects unauthorized file deletions, modifications, and "
            "permission changes on servers and network shares so teams can investigate and restore or correct ACLs. "
            "DLP focuses on preventing sensitive data from leaving the organization, not share-level file and "
            "permission integrity. EDR targets endpoint malware and behavior on hosts, not centralized share ACL "
            "drift. ACLs define access rules but do not by themselves monitor or remediate improper changes over time."
        ),
        "choices": [
            "DLP",
            "EDR",
            "FIM",
            "ACL",
        ],
        "objectives": ["4.5", "3.3"],
    },
    {
        "slug": "open-source-libraries-zero-day-remediation",
        "title": "Security+ — Zero day (open-source libraries)",
        "stem": (
            "A company relies on open-source software libraries to build the software used by its customers. Which "
            "of the following vulnerability types would be the most difficult to remediate due to the company's "
            "reliance on open-source libraries?"
        ),
        "name": "secplus_q455",
        "correct": "D",
        "explain": (
            "Correct. D — A zero-day flaw in an upstream library has no vendor patch yet, so the company must wait "
            "for maintainers or apply compensating controls while still depending on the vulnerable component. "
            "Buffer overflows in libraries are serious but can be fixed when updates are published. SQL injection "
            "and cross-site scripting are commonly remediated in application code the company controls, such as "
            "parameterized queries and input validation, even when libraries are present."
        ),
        "choices": [
            "Buffer overflow",
            "SQL injection",
            "Cross-site scripting",
            "Zero day",
        ],
        "objectives": ["2.3", "4.2"],
    },
    {
        "slug": "legacy-system-firewall-compensating-controls",
        "title": "Security+ — Compensating controls (legacy system)",
        "stem": (
            "An organization disabled unneeded services and placed a firewall in front of a business-critical legacy "
            "system. Which of the following best describes the actions taken by the organization?"
        ),
        "name": "secplus_q456",
        "correct": "D",
        "explain": (
            "Correct. D — Compensating controls provide alternate safeguards when primary remediation such as "
            "replacing or fully patching the legacy system is not feasible; disabling services and adding a "
            "protective firewall reduce exposure around the weakness. An exception is an approved deviation from "
            "policy without substitute controls. Segmentation may be part of the design but the stem describes "
            "substitute protections for a system that cannot meet standard controls. Risk transfer shifts financial "
            "impact to a third party and does not describe these technical mitigations."
        ),
        "choices": [
            "Exception",
            "Segmentation",
            "Risk transfer",
            "Compensating controls",
        ],
        "objectives": ["3.2", "5.1"],
    },
    {
        "slug": "cloud-logging-monitoring-siem",
        "title": "Security+ — SIEM (cloud logging and monitoring)",
        "stem": (
            "Which of the following tools is best for logging and monitoring in a cloud environment?"
        ),
        "name": "secplus_q457",
        "correct": "D",
        "explain": (
            "Correct. D — A SIEM aggregates and correlates logs from cloud platforms, identity services, workloads, "
            "and network controls to support monitoring, alerting, and investigation. An IPS focuses on inline "
            "attack prevention, not centralized log management across cloud services. FIM tracks file and "
            "permission changes on systems but is not a full cloud-wide logging platform. NAC enforces endpoint "
            "admission to networks and does not provide enterprise log aggregation and monitoring."
        ),
        "choices": [
            "IPS",
            "FIM",
            "NAC",
            "SIEM",
        ],
        "objectives": ["4.9", "3.4"],
    },
    {
        "slug": "exploit-undetected-os-memory-injection",
        "title": "Security+ — Memory injection (OS evasion)",
        "stem": (
            "Which of the following allows an exploit to go undetected by the operating system?"
        ),
        "name": "secplus_q458",
        "correct": "C",
        "explain": (
            "Correct. C — Memory injection runs malicious code inside a legitimate process address space, often "
            "without writing files to disk, so traditional OS and file-based controls may not detect the activity. "
            "Firmware vulnerabilities operate below the OS and are serious but are not the technique described for "
            "runtime evasion within OS-managed processes. Side loading installs unapproved applications and may still "
            "be visible to OS controls. Encrypted payloads obscure content in transit or at rest but do not by "
            "themselves hide in-process execution from the operating system."
        ),
        "choices": [
            "Firmware vulnerabilities",
            "Side loading",
            "Memory injection",
            "Encrypted payloads",
        ],
        "objectives": ["2.3", "2.5"],
    },
    {
        "slug": "malicious-video-file-metadata-forensics",
        "title": "Security+ — File metadata (video forensics)",
        "stem": (
            "A security analyst locates a potentially malicious video file on a server and needs to identify both the "
            "creation date and the file's creator. Which of the following actions would most likely give the security "
            "analyst the information required?"
        ),
        "name": "secplus_q459",
        "correct": "D",
        "explain": (
            "Correct. D — File metadata and filesystem attributes record creation timestamps, ownership, and embedded "
            "author or producer fields that identify who created the video. A SHA-256 hash supports integrity checks "
            "and threat intelligence lookups but does not reveal creator or creation time. Hexdump shows raw content "
            "and is inefficient for structured date and author fields. Endpoint logs may show access events but "
            "often lack reliable creator attribution for a specific file on a server."
        ),
        "choices": [
            "Obtain the file's SHA-256 hash.",
            "Use hexdump on the file's contents.",
            "Check endpoint logs.",
            "Query the file's metadata.",
        ],
        "objectives": ["4.9", "2.4"],
    },
    {
        "slug": "after-login-granting-access-authorization",
        "title": "Security+ — Authorization (after login)",
        "stem": (
            "Which of the following security concepts is accomplished when granting access after an individual has "
            "logged into a computer network?"
        ),
        "name": "secplus_q460",
        "correct": "A",
        "explain": (
            "Correct. A — Authorization determines what resources and actions a user may access after authentication "
            "has verified their identity at login. Identification is claiming an identity such as entering a username. "
            "Authentication validates that identity during sign-in. Non-repudiation provides proof that an action "
            "occurred and cannot be denied, which is separate from granting permissions after login."
        ),
        "choices": [
            "Authorization",
            "Identification",
            "Non-repudiation",
            "Authentication",
        ],
        "objectives": ["1.2", "5.4"],
    },
    {
        "slug": "outdated-algorithms-keys-cryptographic-vulnerability",
        "title": "Security+ — Cryptographic vulnerability (outdated algorithms)",
        "stem": (
            "Which of the following is a type of vulnerability that may result from outdated algorithms or keys?"
        ),
        "name": "secplus_q461",
        "correct": "B",
        "explain": (
            "Correct. B — Cryptographic vulnerabilities arise when weak or deprecated algorithms, short key lengths, "
            "or expired certificates undermine confidentiality and integrity. Hash collisions are a specific "
            "attack against weak hash functions but are not the broad vulnerability category named in the stem. "
            "Buffer overflows corrupt memory through improper bounds checking. Input validation flaws come from "
            "failing to sanitize untrusted application input."
        ),
        "choices": [
            "Hash collision",
            "Cryptographic",
            "Buffer overflow",
            "Input validation",
        ],
        "objectives": ["2.3", "1.4"],
    },
    {
        "slug": "telnet-scan-false-positive-encryption-verified",
        "title": "Security+ — False positive (Telnet encryption)",
        "stem": (
            "After reviewing the following vulnerability scanning report:\n"
            "Server: 192.168.14.6\n"
            "Service: Telnet\n"
            "Port: 23 Protocol: TCP Status: Open Severity: High\n"
            "Vulnerability: Use of an insecure network protocol\n"
            "A security analyst performs the following test: nmap -p 23 192.168.14.6 --script telnet-encryption\n"
            "PORT   STATE SERVICE REASON\n"
            "23/tcp open  telnet  syn-ack\n"
            "| telnet-encryption:\n"
            "|   Telnet server supports encryption\n"
            "Which of the following would the security analyst conclude for this reported vulnerability?"
        ),
        "name": "secplus_q462",
        "correct": "A",
        "explain": (
            "Correct. A — The scanner flagged Telnet as inherently insecure, but follow-up testing shows the service "
            "supports encryption, so the high finding does not apply and is a false positive. A rescan alone does "
            "not change the verified result. Noise refers to low-value repetitive alerts, not a disproven finding. "
            "Compensating controls are alternate safeguards when the primary control cannot be used; here the "
            "protocol supports encryption and the original alert was incorrect."
        ),
        "choices": [
            "It is a false positive.",
            "A rescan is required.",
            "It is considered noise.",
            "Compensating controls exist.",
        ],
        "objectives": ["4.3", "2.3"],
    },
    {
        "slug": "credit-card-last-four-masking",
        "title": "Security+ — Masking (credit card last four)",
        "stem": (
            "Which of the following methods to secure credit card data is best to use when a requirement is to see "
            "only the last four numbers on a credit card?"
        ),
        "name": "secplus_q463",
        "correct": "C",
        "explain": (
            "Correct. C — Masking displays only the last four digits while hiding the rest of the primary account "
            "number for user interfaces and receipts. Encryption protects the full value but does not by itself "
            "present a last-four-only view. Hashing is one-way and is not used to show partial card numbers. "
            "Tokenization replaces the PAN with a surrogate token for processing and storage, not for displaying "
            "only the last four digits on screen."
        ),
        "choices": [
            "Encryption",
            "Hashing",
            "Masking",
            "Tokenization",
        ],
        "objectives": ["1.4", "3.10"],
    },
    {
        "slug": "ir-preparation-roles-responsibilities",
        "title": "Security+ — Preparation (IR roles)",
        "stem": (
            "Which of the following is the phase in the incident response process when a security analyst reviews "
            "roles and responsibilities?"
        ),
        "name": "secplus_q464",
        "correct": "A",
        "explain": (
            "Correct. A — Preparation builds the incident response plan, defines team roles and responsibilities, "
            "and establishes tools and communication paths before an event occurs. Recovery restores systems and "
            "services to normal operations. Lessons learned captures improvements after the incident closes. "
            "Analysis investigates indicators, scope, and root cause during an active incident."
        ),
        "choices": [
            "Preparation",
            "Recovery",
            "Lessons learned",
            "Analysis",
        ],
        "objectives": ["4.8", "3.4"],
    },
    {
        "slug": "jsmith-domain-mfa-brute-force-log",
        "title": "Security+ — Brute force (jsmith MFA log)",
        "stem": (
            "Which of the following is the best explanation for what the security analyst has discovered?"
        ),
        "name": "secplus_q465",
        "correct": "C",
        "explain": (
            "Correct. C — Repeated successful password authentications with consecutive failed MFA attempts "
            "and invalid codes indicate an attacker who has the password is guessing MFA tokens to complete "
            "sign-in, which is brute forcing the second factor. Account lockout may eventually occur but the "
            "log pattern shows active guessing, not only that lockout happened. A keylogger could explain how "
            "the password was obtained but the log shows ongoing MFA failures, not keystroke capture. Ransomware "
            "would not produce this authentication and MFA failure pattern in domain activity logs."
        ),
        "choices": [
            "The user jsmith's account has been locked out.",
            "A keylogger is installed on jsmith's workstation.",
            "An attacker is attempting to brute force jsmith's account.",
            "Ransomware has been deployed in the domain.",
        ],
        "prepend_html": build_jsmith_domain_mfa_log_exhibit(),
        "objectives": ["2.4", "4.9"],
    },
    {
        "slug": "directive-managerial-control-aup",
        "title": "Security+ — Directive control (AUP)",
        "stem": "Which of the following is a directive managerial control?",
        "name": "secplus_q466",
        "correct": "A",
        "explain": (
            "Correct. A — An acceptable use policy is a managerial directive control that tells personnel what "
            "behavior is required or prohibited on organizational systems. A login warning banner is a deterrent "
            "control that warns users of monitoring and legal consequences. A master service agreement is a "
            "contractual document governing vendor relationships, not an employee directive. A no trespassing "
            "sign is a physical deterrent, not a managerial policy."
        ),
        "choices": [
            "Acceptable use policy",
            "Login warning banner",
            "Master service agreement",
            "No trespassing sign",
        ],
        "objectives": ["1.2", "5.5"],
    },
    {
        "slug": "dev-team-corporate-policy-internal-noncompliance",
        "title": "Security+ — Internal non-compliance (corporate policy)",
        "stem": (
            "A security officer observes that a software development team is not complying with its corporate "
            "security policy on encrypting confidential data. Which of the following categories refers to this type "
            "of non-compliance?"
        ),
        "name": "secplus_q467",
        "correct": "D",
        "explain": (
            "Correct. D — Internal non-compliance is failure to follow the organization's own policies, standards, "
            "and procedures such as a corporate encryption requirement. External non-compliance involves outside "
            "obligations such as customer contracts or partner requirements. Standard non-compliance typically "
            "means deviation from adopted industry or framework standards rather than the company's own policy. "
            "Regulation non-compliance is violation of laws or government rules, not solely an internal policy gap."
        ),
        "choices": [
            "External",
            "Standard",
            "Regulation",
            "Internal",
        ],
        "objectives": ["5.5", "5.7"],
    },
    {
        "slug": "sqli-web-logs-check-users-table-first",
        "title": "Security+ — SQLi logs (check users first)",
        "stem": (
            "While investigating a possible incident, a security analyst discovers the following log entries:\n"
            "• 67.118.34.157 ----- [28/Jul/2022:10:26:59 -0300] \"GET /query.php?q=wireless%20headphones "
            "/ HTTP/1.0\" 200 12737\n"
            "• 132.18.222.103 ---- [28/Jul/2022:10:27:10 -0300] \"GET /query.php?q=123 INSERT INTO users "
            "VALUES('temp','pass123')# / HTTP/1.0\" 200 935\n"
            "• 12.45.101.121 ----- [28/Jul/2022:10:27:22 -0300] \"GET /query.php?q=mp3%20players / HTTP/1.0\" "
            "200 14650\n"
            "Which of the following should the analyst do first?"
        ),
        "name": "secplus_q468",
        "correct": "D",
        "explain": (
            "Correct. D — The second log line shows SQL injection attempting to create user temp with password "
            "pass123 and returned HTTP 200; the analyst should first verify whether the users table contains new "
            "unauthorized accounts to determine impact. Implementing a WAF is a longer-term control, not the "
            "first investigative step. Disabling query.php is containment after confirming compromise scope. "
            "Blocking brute-force attempts does not address SQL injection or rogue account creation."
        ),
        "choices": [
            "Implement a WAF",
            "Disable the query.php script",
            "Block brute-force attempts on temporary users",
            "Check the users table for new accounts",
        ],
        "objectives": ["2.4", "4.8"],
    },
    {
        "slug": "epp-false-positive-download-misconfiguration",
        "title": "Security+ — EPP false positive (misconfiguration)",
        "stem": (
            "A security analyst is investigating an alert that was produced by endpoint protection software. The "
            "analyst determines this event was a false positive triggered by an employee who attempted to download a "
            "file. Which of the following is the most likely reason the download was blocked?"
        ),
        "name": "secplus_q469",
        "correct": "A",
        "explain": (
            "Correct. A — A false positive on a benign employee download most often results from endpoint protection "
            "misconfiguration such as overly aggressive heuristics, outdated allowlists, or incorrect policy "
            "settings. A zero-day in the file would imply a real threat, not a false positive. A supply chain "
            "compromise of the vendor is unrelated to one benign download being flagged. Incorrect file "
            "permissions on disk do not typically cause endpoint protection to block a download at detection time."
        ),
        "choices": [
            "A misconfiguration in the endpoint protection software",
            "A zero-day vulnerability in the file",
            "A supply chain attack on the endpoint protection vendor",
            "Incorrect file permissions",
        ],
        "objectives": ["4.5", "4.3"],
    },
    {
        "slug": "zero-day-mission-critical-compensating-controls",
        "title": "Security+ — Zero-day (HA production mitigation)",
        "stem": (
            "Which of the following is the best mitigation for a zero-day vulnerability found in mission-critical "
            "production servers that must be highly available?"
        ),
        "name": "secplus_q470",
        "correct": "C",
        "explain": (
            "Correct. C — With no vendor patch for a zero-day, monitoring plus compensating controls such as "
            "segmentation, IPS signatures, access restrictions, and enhanced logging reduce risk while keeping "
            "mission-critical systems online. Migrating to containers is a major change that does not remove the "
            "underlying flaw and can disrupt availability. Removing production systems to an isolated network "
            "conflicts with high-availability requirements. Patching quickly is ideal when a fix exists, but a "
            "zero-day may have no patch yet and rushed changes risk outage on critical servers."
        ),
        "choices": [
            "Virtualizing and migrating to a containerized instance",
            "Removing and sandboxing to an isolated network",
            "Monitoring and implementing compensating controls",
            "Patching and redeploying to production as quickly as possible",
        ],
        "objectives": ["2.3", "3.2"],
    },
    {
        "slug": "web-filter-malicious-links-categorization-review",
        "title": "Security+ — Content categorization (web filter)",
        "stem": (
            "An administrator implements web-filtering products but still sees that users are visiting malicious "
            "links. Which of the following configuration items does the security administrator need to review?"
        ),
        "name": "secplus_q471",
        "correct": "B",
        "explain": (
            "Correct. B — Web filters rely on URL reputation and content categorization; miscategorized or "
            "outdated categories can allow malicious sites through until policies and category databases are "
            "corrected. An IPS blocks attack patterns and is not the primary web URL category configuration. "
            "Encryption settings do not define which sites the filter classifies as malicious. DNS service "
            "resolution may be filtered separately but the web-filtering product decision to permit malicious "
            "links is driven by categorization and policy rules."
        ),
        "choices": [
            "Intrusion prevention system",
            "Content categorization",
            "Encryption",
            "DNS service",
        ],
        "objectives": ["4.6", "3.3"],
    },
    {
        "slug": "departing-employees-customer-data-uba",
        "title": "Security+ — UBA (insider customer data)",
        "stem": (
            "A company is experiencing issues with employees leaving the company for a competitor and taking "
            "customer contact information with them. Which of the following tools will help prevent this from "
            "reoccurring?"
        ),
        "name": "secplus_q472",
        "correct": "D",
        "explain": (
            "Correct. D — User and entity behavior analytics detects anomalous access such as bulk downloads of "
            "customer records, unusual hours, or spikes before resignation that indicate insider data theft. FIM "
            "monitors unauthorized file changes on systems but does not focus on user access patterns to CRM data. "
            "NAC controls which devices join the network. An IDS detects network attacks and is not optimized for "
            "insider misuse of authorized accounts."
        ),
        "choices": [
            "FIM",
            "NAC",
            "IDS",
            "UBA",
        ],
        "objectives": ["4.9", "3.3"],
    },
    {
        "slug": "rush-deploy-insufficient-due-diligence-risk-acceptance",
        "title": "Security+ — Risk acceptance (rushed deployment)",
        "stem": (
            "In a rush to meet an end-of-year business goal, the IT department was told to implement a new "
            "business application. The security engineer reviews the attributes of the application and decides the "
            "time needed to perform due diligence is insufficient from a cybersecurity perspective. Which of the "
            "following best describes the security engineer's response?"
        ),
        "name": "secplus_q473",
        "correct": "B",
        "explain": (
            "Correct. B — Risk acceptance is the decision to proceed while acknowledging residual risk when full "
            "due diligence or controls cannot be completed in the available time. Risk tolerance is the level of "
            "variation from risk appetite an organization will endure. Risk appetite is leadership's overall "
            "willingness to take risk for business objectives, not one engineer's conclusion about a single "
            "deployment timeline. Risk importance is not a standard risk-management term on the exam."
        ),
        "choices": [
            "Risk tolerance",
            "Risk acceptance",
            "Risk importance",
            "Risk appetite",
        ],
        "objectives": ["1.2", "5.1"],
    },
    {
        "slug": "air-gapped-network-data-loss-removable-devices",
        "title": "Security+ — Air-gapped data loss (removable media)",
        "stem": (
            "Which of the following is the most common data loss path for an air-gapped network?"
        ),
        "name": "secplus_q474",
        "correct": "D",
        "explain": (
            "Correct. D — Air-gapped networks block routine network exfiltration, so data most often leaves on "
            "removable media (USB drives, external disks, optical media) carried by users or insiders. A bastion "
            "host is a controlled jump point, not the typical exfiltration path for isolated segments. Unsecured "
            "Bluetooth can leak data wirelessly but is less common than removable devices in hardened air-gap "
            "environments. Unpatched operating systems increase compromise risk but are not themselves the primary "
            "data-loss channel."
        ),
        "choices": [
            "Bastion host",
            "Unsecured Bluetooth",
            "Unpatched OS",
            "Removable devices",
        ],
        "objectives": ["3.3", "4.1"],
    },
    {
        "slug": "manual-account-errors-user-provisioning-script",
        "title": "Security+ — User provisioning script (account creation)",
        "stem": (
            "The management team notices that new accounts that are set up manually do not always have correct "
            "access or permissions. Which of the following automation techniques should a systems administrator "
            "use to streamline account creation?"
        ),
        "name": "secplus_q475",
        "correct": "D",
        "explain": (
            "Correct. D — A user provisioning script automates account creation from a defined template so each "
            "account receives the same roles, groups, and permissions, reducing manual misconfiguration. A guard "
            "rail script enforces policy boundaries during changes but does not replace standardized onboarding "
            "workflows. A ticketing workflow tracks requests and approvals; it does not by itself assign correct "
            "access. An escalation script routes incidents or alerts to higher tiers, not routine account setup."
        ),
        "choices": [
            "Guard rail script",
            "Ticketing workflow",
            "Escalation script",
            "User provisioning script",
        ],
        "objectives": ["4.7", "4.1"],
    },
    {
        "slug": "sla-response-time-escalation-performance-metrics",
        "title": "Security+ — SLA (response time and escalation)",
        "stem": (
            "Which of the following agreements defines response time, escalation points, and performance "
            "metrics?"
        ),
        "name": "secplus_q476",
        "correct": "D",
        "explain": (
            "Correct. D — A service level agreement (SLA) spells out measurable service commitments such as "
            "response times, escalation paths when thresholds are missed, and performance metrics like uptime "
            "or resolution targets. A blanket purchase agreement (BPA) is a procurement vehicle for recurring "
            "purchases, not operational service metrics. A memorandum of agreement (MOA) documents shared "
            "responsibilities between parties but is not the primary vehicle for timed support commitments. A "
            "non-disclosure agreement (NDA) restricts disclosure of confidential information."
        ),
        "choices": [
            "BPA",
            "MOA",
            "NDA",
            "SLA",
        ],
        "objectives": ["5.3", "5.4"],
    },
    {
        "slug": "same-password-different-hashes-salting",
        "title": "Security+ — Salting (identical passwords, different hashes)",
        "stem": (
            "An analyst identifies that multiple users have the same passwords, but the hashes appear to be "
            "completely different. Which of the following most likely explains this issue?"
        ),
        "name": "secplus_q477",
        "correct": "B",
        "explain": (
            "Correct. B — Salting adds unique random data to each password before hashing, so identical plaintext "
            "passwords produce different stored hashes and defeat rainbow-table reuse across accounts. Data "
            "masking hides sensitive values for display or testing and does not change password-hash storage. "
            "Key escrow holds encryption keys for recovery by authorized parties. Tokenization replaces sensitive "
            "data with non-sensitive tokens, typically for payment or account numbers, not password databases."
        ),
        "choices": [
            "Data masking",
            "Salting",
            "Key escrow",
            "Tokenization",
        ],
        "objectives": ["1.4", "2.3"],
    },
    {
        "slug": "ir-understand-incident-source-analysis",
        "title": "Security+ — Analysis (incident source)",
        "stem": (
            "During an investigation, an incident response team attempts to understand the source of an incident. "
            "Which of the following incident response activities describes this process?"
        ),
        "name": "secplus_q478",
        "correct": "A",
        "explain": (
            "Correct. A — Analysis investigates indicators, scope, and root cause, including how the incident "
            "started and which systems or accounts were involved. Lessons learned is a post-incident review after "
            "recovery to improve future response. Detection is the initial identification that an event may be "
            "malicious or policy violating. Containment limits spread and impact after the team understands enough "
            "to act, but determining source and scope is analysis work."
        ),
        "choices": [
            "Analysis",
            "Lessons learned",
            "Detection",
            "Containment",
        ],
        "objectives": ["4.8", "3.4"],
    },
    {
        "slug": "xss-web-server-compromise-waf-prevention",
        "title": "Security+ — WAF (XSS prevention)",
        "stem": (
            "An attacker used XSS to compromise a web server. Which of the following solutions could have been "
            "used to prevent this attack?"
        ),
        "name": "secplus_q479",
        "correct": "C",
        "explain": (
            "Correct. C — A web application firewall (WAF) inspects HTTP/HTTPS traffic and can block common "
            "application-layer attacks such as cross-site scripting before they reach the web server. A next-generation "
            "firewall (NGFW) adds application awareness at the network edge but is not specialized for web-app "
            "payload inspection like a WAF. A unified threat management (UTM) appliance bundles gateway services "
            "but is a general perimeter tool, not the primary control for web-specific XSS. Network access control "
            "(NAC) governs which devices may join the network and does not filter malicious web requests."
        ),
        "choices": [
            "NGFW",
            "UTM",
            "WAF",
            "NAC",
        ],
        "objectives": ["3.3", "4.1"],
    },
    {
        "slug": "hq-branch-vpn-data-in-transit",
        "title": "Security+ — VPN (data in transit)",
        "stem": (
            "An organization is leveraging a VPN between its headquarters and a branch location. Which of the "
            "following is the VPN protecting?"
        ),
        "name": "secplus_q480",
        "correct": "B",
        "explain": (
            "Correct. B — A site-to-site VPN encrypts traffic as it crosses untrusted networks between locations, "
            "protecting data in transit from eavesdropping and tampering. Data in use is information actively "
            "processed in memory or applications on endpoints. Geographic restrictions concern where content or "
            "services may be accessed by region. Data sovereignty addresses legal jurisdiction over where data "
            "is stored and processed, not the confidentiality of packets between offices."
        ),
        "choices": [
            "Data in use",
            "Data in transit",
            "Geographic restrictions",
            "Data sovereignty",
        ],
        "objectives": ["3.3", "1.4"],
    },
    {
        "slug": "malicious-insider-risk-uba",
        "title": "Security+ — UBA (malicious insider)",
        "stem": (
            "A company identified the potential for malicious insiders to harm the organization. Which of the "
            "following measures should the organization implement to reduce this risk?"
        ),
        "name": "secplus_q481",
        "correct": "C",
        "explain": (
            "Correct. C — User behavior analytics establishes baselines for normal activity and alerts on "
            "anomalies such as unusual access times, bulk downloads, or privilege abuse that may indicate "
            "malicious insiders. Unified threat management bundles perimeter security services and is not "
            "focused on insider misuse of legitimate credentials. A web application firewall protects web apps "
            "from common HTTP attacks. An intrusion detection system targets network-based attacks and often "
            "misses insiders who use authorized accounts."
        ),
        "choices": [
            "Unified threat management",
            "Web application firewall",
            "User behavior analytics",
            "Intrusion detection system",
        ],
        "objectives": ["4.9", "3.3"],
    },
    {
        "slug": "multi-provider-email-spf-authorized-senders",
        "title": "Security+ — SPF (multiple email providers)",
        "stem": (
            "A company uses multiple providers to send its marketing, internal, and support emails. Many of the "
            "emails are marked as spam. Which of the following changes should the company make to ensure legitimate "
            "emails are validated?"
        ),
        "name": "secplus_q482",
        "correct": "D",
        "explain": (
            "Correct. D — SPF DNS records list every host or provider authorized to send mail for the domain; when "
            "marketing, internal, and support mail each use different services, all sending sources must appear in "
            "SPF or receivers may treat messages as spoofed. Disabling DKIM removes a key authentication signature "
            "and worsens deliverability. A DMARC reject policy should follow working SPF and DKIM alignment; "
            "implementing reject alone does not authorize multiple legitimate senders. MX records direct inbound "
            "mail delivery and do not validate outbound messages from third-party providers."
        ),
        "choices": [
            "Disable DKIM to avoid signature conflicts.",
            'Implement DMARC with a "reject" policy to enforce sender validation.',
            "Replace the domain's MX record with the marketing provider's services.",
            "Update the SPF record to include all authorized sending sources.",
        ],
        "objectives": ["2.2", "4.1"],
    },
    {
        "slug": "always-on-vpn-fail-host-content-filtering",
        "title": "Security+ — Host content filtering (VPN failure)",
        "stem": (
            "The security team notices that the Always On VPN solution sometimes fails to connect. This leaves "
            "remote users unprotected because they cannot connect to the on-premises web proxy. Which of the "
            "following changes will best provide web protection in this scenario?"
        ),
        "name": "secplus_q483",
        "correct": "D",
        "explain": (
            "Correct. D — Host-based content filtering enforces web policy on the endpoint so protection continues "
            "even when the VPN or on-premises proxy is unreachable. Network access control admits or blocks "
            "devices on the corporate LAN and does not secure browsing during VPN outages. Pointing the local "
            "gateway at the VPN does not restore filtering when the tunnel fails. Publishing the internal proxy "
            "with a public NAT exposes infrastructure to the internet and is not a recommended compensating control."
        ),
        "choices": [
            "Implement network access control.",
            "Configure the local gateway to point to the VPN.",
            "Create a public NAT to the on-premises proxy.",
            "Install a host-based content filtering solution.",
        ],
        "objectives": ["4.6", "3.3"],
    },
    {
        "slug": "secure-data-track-changes-fim",
        "title": "Security+ — FIM (track data changes)",
        "stem": (
            "A security administrator needs a method to secure data in an environment that includes some form of "
            "checks so that the administrator can track any changes. Which of the following should the "
            "administrator set up to achieve this goal?"
        ),
        "name": "secplus_q484",
        "correct": "D",
        "explain": (
            "Correct. D — File integrity monitoring (FIM) baselines critical files and alerts when unauthorized "
            "creates, modifications, or deletions occur so administrators can track changes. SPF authorizes email "
            "senders in DNS and does not monitor stored data. A group policy object (GPO) enforces Windows "
            "configuration settings but is not a dedicated change-detection control for arbitrary data files. "
            "Network access control (NAC) governs endpoint admission to the network."
        ),
        "choices": [
            "SPF",
            "GPO",
            "NAC",
            "FIM",
        ],
        "objectives": ["3.10", "4.4"],
    },
    {
        "slug": "wifi-filter-bypass-rogue-access-point",
        "title": "Security+ — Rogue AP (filter bypass)",
        "stem": (
            "A business uses Wi-Fi with content filtering enabled. An employee noticed a coworker accessed a "
            "blocked site from a work computer and reported the issue. While investigating the issue, a security "
            "administrator found another device providing internet access to certain employees. Which of the "
            "following best describes the security risk?"
        ),
        "name": "secplus_q485",
        "correct": "B",
        "explain": (
            "Correct. B — A rogue access point is an unauthorized wireless device that lets users connect outside "
            "corporate Wi-Fi controls, bypassing content filtering and other security policies. A missing host-based "
            "agent could weaken endpoint protection but does not explain a separate device handing out internet. "
            "A hidden SSID on approved infrastructure is still managed corporate Wi-Fi, not an alternate path around "
            "filters. Jamming a valid access point would reduce availability, not provide alternate internet access."
        ),
        "choices": [
            "The host-based security agent is not running on all computers.",
            "A rogue access point is allowing users to bypass controls.",
            "Employees who have certain credentials are using a hidden SSID.",
            "A valid access point is being jammed to limit availability.",
        ],
        "objectives": ["4.3", "3.3"],
    },
    {
        "slug": "fake-credentials-document-honeyfile",
        "title": "Security+ — Honeyfile (decoy document)",
        "stem": (
            "A systems administrator uses deception techniques to help detect and study attacks within a network. "
            "The administrator deploys a document filled with fake passwords and customer payment information. "
            "Which of the following techniques is the administrator using?"
        ),
        "name": "secplus_q486",
        "correct": "C",
        "explain": (
            "Correct. C — A honeyfile is a decoy document or file planted with enticing fake data; access or "
            "exfiltration attempts can be monitored to detect attackers. A honeytoken is a single piece of decoy "
            "data such as a credential or record, not necessarily framed as a standalone bait file. A honeypot "
            "is a decoy system or service that mimics a real host. A honeynet is a collection of honeypots "
            "forming an isolated deception network."
        ),
        "choices": [
            "Honeytoken",
            "Honeypot",
            "Honeyfile",
            "Honeynet",
        ],
        "objectives": ["4.8", "3.2"],
    },
    {
        "slug": "forensic-evidence-handling-chain-of-custody",
        "title": "Security+ — Chain of custody (forensics)",
        "stem": (
            "Which of the following best describes the practice of preserving and documenting the handling of "
            "forensic evidence?"
        ),
        "name": "secplus_q487",
        "correct": "C",
        "explain": (
            "Correct. C — Chain of custody is the documented record of who collected evidence, when it changed "
            "hands, and how it was stored or analyzed so it remains admissible and untampered. Acquisition is the "
            "initial collection of evidence, not the ongoing documentation of every transfer. E-discovery is the "
            "legal process of identifying and producing electronically stored information for litigation. Forensic "
            "tabletop exercises are discussion-based drills to practice incident response, not evidence handling "
            "logs."
        ),
        "choices": [
            "Acquisition of evidence",
            "E-discovery",
            "Chain of custody",
            "Forensic tabletop exercises",
        ],
        "objectives": ["4.8", "5.2"],
    },
    {
        "slug": "ciso-ignores-vulnerabilities-risk-accept",
        "title": "Security+ — Risk accept (ignored vulnerabilities)",
        "stem": (
            "Which of the following risk management strategies is being used when a Chief Information Security "
            "Officer ignores known vulnerabilities identified during a risk assessment?"
        ),
        "name": "secplus_q488",
        "correct": "D",
        "explain": (
            "Correct. D — Accept (risk acceptance) is the decision to take no further action on identified risk "
            "and live with the residual exposure, often after documenting leadership approval. Transfer shifts risk "
            "to another party such as through insurance or contracts. Avoid eliminates the activity or asset that "
            "creates the risk. Mitigate implements controls to reduce likelihood or impact rather than ignoring "
            "findings."
        ),
        "choices": [
            "Transfer",
            "Avoid",
            "Mitigate",
            "Accept",
        ],
        "objectives": ["1.2", "5.1"],
    },
    {
        "slug": "offensive-assessment-pen-test-red-team",
        "title": "Security+ — Red team (pen test and social engineering)",
        "stem": (
            "A company hired a consultant to perform an offensive security assessment covering penetration "
            "testing and social engineering. Which of the following teams will conduct this assessment activity?"
        ),
        "name": "secplus_q489",
        "correct": "D",
        "explain": (
            "Correct. D — A red team simulates real-world attackers through offensive techniques such as "
            "penetration testing and social engineering to test defenses. A white team often oversees or "
            "facilitates exercises rather than performing the attacks. A purple team blends offensive and "
            "defensive staff to improve detection and response together. A blue team focuses on defense, "
            "monitoring, and incident response."
        ),
        "choices": [
            "White",
            "Purple",
            "Blue",
            "Red",
        ],
        "objectives": ["2.2", "5.5"],
    },
    {
        "slug": "public-rdp-vpn-jump-server-firewall",
        "title": "Security+ — VPN and jump server (exposed RDP)",
        "stem": (
            "A security analyst scans a company's public network and discovers a host is running a remote desktop "
            "that can be used to access the production network. Which of the following changes should the security "
            "analyst recommend?"
        ),
        "name": "secplus_q490",
        "correct": "B",
        "explain": (
            "Correct. B — Remote desktop should not be exposed on the public internet; require VPN access and place "
            "a jump server inside the firewall so administrators reach production only through a controlled "
            "bastion. Changing the RDP port is obscurity and does not remove internet exposure. A web proxy on the "
            "RDP host does not secure remote desktop or production access paths. Joining the server to the domain "
            "and lengthening passwords still leaves RDP discoverable and brute-forceable from the internet."
        ),
        "choices": [
            "Changing the remote desktop port to a non-standard number",
            "Setting up a VPN and placing the jump server inside the firewall",
            "Using a proxy for web connections from the remote desktop server",
            "Connecting the remote server to the domain and increasing the password length",
        ],
        "objectives": ["4.6", "3.2"],
    },
    {
        "slug": "decrease-hardware-attack-surface-virtualization",
        "title": "Security+ — Virtualization (hardware attack surface)",
        "stem": (
            "Which of the following should a systems administrator use to decrease the company's hardware attack "
            "surface?"
        ),
        "name": "secplus_q491",
        "correct": "D",
        "explain": (
            "Correct. D — Virtualization consolidates workloads onto fewer physical hosts, reducing the number of "
            "machines that must be powered, patched, and physically protected, which shrinks the hardware attack "
            "surface. Replication copies data or systems for availability and does not remove physical devices. "
            "Isolation separates systems or networks logically but does not by itself reduce how much hardware "
            "exists. Centralization gathers management or services but may still leave many physical endpoints "
            "deployed."
        ),
        "choices": [
            "Replication",
            "Isolation",
            "Centralization",
            "Virtualization",
        ],
        "objectives": ["4.1", "3.6"],
    },
    {
        "slug": "contract-employees-gpo-logon-hours",
        "title": "Security+ — GPO logon hours (contract staff)",
        "stem": (
            "A program manager wants to ensure contract employees can only use the company's computers "
            "Monday through Friday from 9 a.m. to 5 p.m. Which of the following would best enforce this access "
            "control?"
        ),
        "name": "secplus_q492",
        "correct": "A",
        "explain": (
            "Correct. A — A group policy object (GPO) can apply logon hours (time-of-day restrictions) to contract "
            "employee accounts so they may authenticate only during the approved window on domain-joined computers. "
            "Discretionary access with rule-based permissions governs resource rights, not workstation logon "
            "schedules. OAuth delegates authorization for applications and APIs; it does not enforce corporate PC "
            "logon hours. SAML federation authenticates users from an external identity provider but does not by "
            "itself limit when accounts may sign in to company systems."
        ),
        "choices": [
            "Creating a GPO for all contract employees and setting time-of-day log-in restrictions",
            "Creating a discretionary access policy and setting rule-based access for contract employees",
            "Implementing an OAuth server and then setting least privilege for contract employees",
            "Implementing SAML with federation to the contract employees' authentication server",
        ],
        "objectives": ["4.6", "3.2"],
    },
    {
        "slug": "datacenter-safety-controls-fail-open",
        "title": "Security+ — Safety controls fail open (data center)",
        "stem": (
            "Security controls in a data center are being reviewed to ensure data is properly protected and that "
            "human life considerations are included. Which of the following best describes how the controls should "
            "be set up?"
        ),
        "name": "secplus_q493",
        "correct": "C",
        "explain": (
            "Correct. C — Safety controls such as emergency exits and fire suppression should fail open so people "
            "are never trapped when systems lose power or fail. Logical security and remote access controls should "
            "fail closed to deny unauthorized access when a failure occurs. Logging should not fail open in a way "
            "that silently stops audit trails while access continues; redundancy is preferred. The stem pairs data "
            "protection with human life, and fail-open safety design is the life-safety requirement."
        ),
        "choices": [
            "Remote access points should fail closed.",
            "Logging controls should fail open.",
            "Safety controls should fail open.",
            "Logical security controls should fail closed.",
        ],
        "objectives": ["3.7", "5.1"],
    },
    {
        "slug": "secure-data-in-transit-encryption",
        "title": "Security+ — Encryption (data in transit)",
        "stem": (
            "Which of the following methods to secure data is most often used to protect data in transit?"
        ),
        "name": "secplus_q494",
        "correct": "A",
        "explain": (
            "Correct. A — Encryption such as TLS, VPN, and IPsec protects confidentiality and integrity while data "
            "moves across networks. Obfuscation makes data harder to understand but is not the primary control for "
            "network transit. Permission restrictions govern who may access resources and do not encrypt packets "
            "in flight. Hashing verifies integrity and supports storage or authentication use cases; it is not the "
            "usual method to protect data in transit from eavesdropping."
        ),
        "choices": [
            "Encryption",
            "Obfuscation",
            "Permission restrictions",
            "Hashing",
        ],
        "objectives": ["1.4", "3.3"],
    },
    {
        "slug": "eol-business-critical-system-isolation",
        "title": "Security+ — Isolation (EOL critical system)",
        "stem": (
            "Which of the following would most likely prevent exploitation of an end-of-life, business-critical "
            "system?"
        ),
        "name": "secplus_q495",
        "correct": "B",
        "explain": (
            "Correct. B — Network isolation or segmentation limits exposure of an unsupported system that cannot be "
            "patched or removed, blocking many attack paths while it remains online for business needs. Monitoring "
            "detects suspicious activity but does not by itself stop exploitation. Decommissioning removes the "
            "system, which is not viable when the asset is business-critical and must continue operating. "
            "Encryption protects data confidentiality and does not remediate unpatched operating system flaws."
        ),
        "choices": [
            "Monitoring",
            "Isolation",
            "Decommissioning",
            "Encryption",
        ],
        "objectives": ["3.2", "4.2"],
    },
    {
        "slug": "inbound-malicious-traffic-ips-automated-block",
        "title": "Security+ — IPS (inbound malicious traffic)",
        "stem": (
            "A security manager needs an automated solution that will take immediate action to protect an "
            "organization against inbound malicious traffic. Which of the following is the best solution?"
        ),
        "name": "secplus_q496",
        "correct": "B",
        "explain": (
            "Correct. B — An intrusion prevention system (IPS) operates inline and can automatically block or drop "
            "malicious inbound traffic as it is detected. Unified endpoint management (UEM) deploys policies and "
            "software to endpoints but does not inspect and block network attacks at the perimeter. A web "
            "application firewall protects HTTP and HTTPS applications, not all inbound network threats. A VPN "
            "provides encrypted remote access and does not by itself stop malicious traffic directed at the "
            "organization."
        ),
        "choices": [
            "UEM",
            "IPS",
            "WAF",
            "VPN",
        ],
        "objectives": ["4.5", "3.3"],
    },
    {
        "slug": "bec-gift-card-executive-display-name",
        "title": "Security+ — BEC (gift card request)",
        "stem": (
            "Which of the following scenarios describes a possible business email compromise attack?"
        ),
        "name": "secplus_q497",
        "correct": "A",
        "explain": (
            "Correct. A — Business email compromise often impersonates an executive (display name spoofing) to "
            "pressure employees into urgent wire transfers, invoice changes, or gift card purchases. Ransomware "
            "after opening an attachment encrypts files and demands payment to restore access, which is a different "
            "attack type. An HR impersonation asking for cloud administrator credentials is targeted phishing or "
            "pretexting, not the typical BEC payment-fraud pattern. A link to a fake company email portal is "
            "credential phishing rather than executive-driven financial fraud."
        ),
        "choices": [
            (
                "An employee receives a gift card request in an email that has an executive's name in the display "
                "field of the email."
            ),
            (
                "Employees who open an email attachment receive messages demanding payment in order to access "
                "files."
            ),
            (
                "A service desk employee receives an email from the HR director asking for log-in credentials to a "
                "cloud administrator account."
            ),
            (
                "An employee receives an email with a link to a phishing site that is designed to look like the "
                "company's email portal."
            ),
        ],
        "objectives": ["2.2", "2.4"],
    },
]


def sync_hub_slugs(chain: list[dict]) -> None:
    slugs = [q["slug"] for q in chain]
    inner = ",\n    ".join(json.dumps(s) for s in slugs)
    HUB_JS.parent.mkdir(parents=True, exist_ok=True)
    if HUB_JS.is_file():
        text = HUB_JS.read_text(encoding="utf-8")
        patched, n = re.subn(
            r"window\.SECPLUS_PRACTICE\.SLUGS\s*=\s*\[[\s\S]*?\];",
            f"window.SECPLUS_PRACTICE.SLUGS = [\n    {inner}\n  ];",
            text,
            count=1,
        )
        if n:
            HUB_JS.write_text(patched, encoding="utf-8")
            return
    body = f"""(function () {{
  "use strict";
  window.SECPLUS_PRACTICE = window.SECPLUS_PRACTICE || {{}};
  window.SECPLUS_PRACTICE.SLUGS = [
    {inner}
  ];
}})();
"""
    HUB_JS.write_text(body, encoding="utf-8")


def sync_topic_map(chain: list[dict]) -> None:
    assignments: dict[str, list[str]] = {}
    if TOPIC_MAP.is_file():
        data = json.loads(TOPIC_MAP.read_text(encoding="utf-8"))
        raw = data.get("assignments")
        if isinstance(raw, dict):
            assignments = {k: list(v) for k, v in raw.items()}
    for q in chain:
        key = f"{q['slug']}.html"
        assignments[key] = list(q.get("objectives") or ["2.0"])
    payload = {
        "schemaVersion": 1,
        "notes": "Assign Security+ question files to SY0-701 objective IDs (e.g. 2.0, 3.0).",
        "assignments": dict(sorted(assignments.items())),
    }
    TOPIC_MAP.parent.mkdir(parents=True, exist_ok=True)
    TOPIC_MAP.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    domain_lookup, objective_lookup = _load_objective_lookups()
    n = len(CHAIN)
    for i, q in enumerate(CHAIN):
        prev_slug = CHAIN[i - 1]["slug"] if i > 0 else None
        next_slug = CHAIN[i + 1]["slug"] if i + 1 < n else None
        if q.get("choose_two"):
            content = render_page_choose_two(
                title=q["title"],
                choices=q["choices"],
                name=q["name"],
                correct=list(q["correct"]),
                explain=q["explain"],
                stem=q["stem"],
                prepend_html=q.get("prepend_html", ""),
                prev_slug=prev_slug,
                next_slug=next_slug,
                objective_ids=list(q.get("objectives") or []),
                domain_lookup=domain_lookup,
                objective_lookup=objective_lookup,
            )
        else:
            content = render_page(
                title=q["title"],
                slug=q["slug"],
                choices=q["choices"],
                name=q["name"],
                correct=q["correct"],
                explain=q["explain"],
                stem=q["stem"],
                prepend_html=q.get("prepend_html", ""),
                prev_slug=prev_slug,
                next_slug=next_slug,
                objective_ids=list(q.get("objectives") or []),
                domain_lookup=domain_lookup,
                objective_lookup=objective_lookup,
            )
        path = OUT / f"{q['slug']}.html"
        path.write_text(content, encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")
    sync_hub_slugs(CHAIN)
    sync_topic_map(CHAIN)
    print(f"Updated {HUB_JS.relative_to(ROOT)} ({n} slugs)")
    print(f"Updated {TOPIC_MAP.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
