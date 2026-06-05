#!/usr/bin/env python3
"""Split monolithic PBQ section fragments into folder-sized section files."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PBQ = ROOT / "public/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production"

EXHIBIT_LAUNCHERS = """<ul class="pbq-exhibit-launchers">
  <li><button type="button" class="btn btn-secondary" data-pbq-modal="#exhibit-corpus">Exhibit A — Policy corpus index</button></li>
  <li><button type="button" class="btn btn-secondary" data-pbq-modal="#exhibit-chat-log">Exhibit B — HR chat API log</button></li>
  <li><button type="button" class="btn btn-secondary" data-pbq-modal="#exhibit-retrieved-chunk">Exhibit C — Retrieved chunk</button></li>
  <li><button type="button" class="btn btn-secondary" data-pbq-modal="#exhibit-poisoned-pdf">Exhibit D — Quarantined upload</button></li>
</ul>"""

ACME_CONFIG_SCRIPT = """<script>
(function () {
  var CONFIG = {
    "cfg-vector-access": "secure",
    "cfg-retrieval": "filter",
    "cfg-corpus": "approved",
    "cfg-training": "no-train",
    "cfg-logging": "redact",
    "cfg-context": "untrusted"
  };
  var root = document.getElementById("acme-config");
  if (!root) return;
  var actionBtns = root.querySelectorAll(".actions button");
  var checkBtn = actionBtns[0];
  var showBtn = actionBtns[1];
  var resetBtn = actionBtns[2];
  var result = root.querySelector(".actions [id$='result']");
  if (!checkBtn || !showBtn || !resetBtn || !result) return;
  function configOk() {
    var ok = true;
    root.querySelectorAll("[data-setting]").forEach(function (sel) {
      var key = sel.getAttribute("data-setting");
      var pass = sel.value === CONFIG[key];
      sel.classList.toggle("pbq-ai-select--bad", sel.value && !pass);
      sel.classList.toggle("pbq-ai-select--good", pass);
      if (!pass) ok = false;
    });
    return ok;
  }
  function clearMarks() {
    root.querySelectorAll(".pbq-ai-select--bad, .pbq-ai-select--good").forEach(function (el) {
      el.classList.remove("pbq-ai-select--bad", "pbq-ai-select--good");
    });
  }
  checkBtn.addEventListener("click", function () {
    clearMarks();
    if (configOk()) {
      result.className = "is-pass";
      result.textContent = "Correct — system configuration settings are secure.";
    } else {
      result.className = "is-fail";
      result.textContent = "Incorrect. Review vector API, retrieval filters, corpus scope, training, logging, and context handling.";
    }
  });
  showBtn.addEventListener("click", function () {
    Object.keys(CONFIG).forEach(function (key) {
      var sel = root.querySelector('[data-setting="' + key + '"]');
      if (sel) sel.value = CONFIG[key];
    });
    clearMarks();
    configOk();
    result.className = "is-pass";
    result.textContent = "Configuration filled in. Continue to Guardrails.";
  });
  resetBtn.addEventListener("click", function () {
    root.querySelectorAll("[data-setting]").forEach(function (sel) { sel.value = ""; });
    clearMarks();
    result.className = "";
    result.textContent = "";
  });
})();
</script>"""

ACME_GUARD_SCRIPT = """<script>
(function () {
  var GUARDS = {
    "gr-prompt-injection": true,
    "gr-output-pii": true,
    "gr-retrieval-filter": true,
    "gr-rate-limit": true,
    "gr-ingest-scan": true,
    "gr-anonymous": false,
    "gr-debug-prompts": false,
    "gr-external-tools": false
  };
  var root = document.getElementById("acme-guardrails");
  if (!root) return;
  var actionBtns = root.querySelectorAll(".actions button");
  var checkBtn = actionBtns[0];
  var showBtn = actionBtns[1];
  var resetBtn = actionBtns[2];
  var result = root.querySelector(".actions [id$='result']");
  if (!checkBtn || !showBtn || !resetBtn || !result) return;
  function guardsOk() {
    var ok = true;
    root.querySelectorAll("[data-guard]").forEach(function (input) {
      var key = input.getAttribute("data-guard");
      var pass = input.checked === GUARDS[key];
      input.closest(".pbq-ai-toggle").classList.toggle("pbq-ai-toggle--bad", !pass);
      input.closest(".pbq-ai-toggle").classList.toggle("pbq-ai-toggle--good", pass);
      if (!pass) ok = false;
    });
    return ok;
  }
  function clearMarks() {
    root.querySelectorAll(".pbq-ai-toggle--bad, .pbq-ai-toggle--good").forEach(function (el) {
      el.classList.remove("pbq-ai-toggle--bad", "pbq-ai-toggle--good");
    });
  }
  checkBtn.addEventListener("click", function () {
    clearMarks();
    if (guardsOk()) {
      result.className = "is-pass";
      result.textContent = "Correct — guardrails match recommended production state.";
    } else {
      result.className = "is-fail";
      result.textContent = "Incorrect. Enable injection, PII, retrieval, rate-limit, and ingest scanning; disable anonymous access, debug prompts, and unrestricted tools.";
    }
  });
  showBtn.addEventListener("click", function () {
    Object.keys(GUARDS).forEach(function (key) {
      var input = root.querySelector('[data-guard="' + key + '"]');
      if (input) input.checked = GUARDS[key];
    });
    clearMarks();
    guardsOk();
    result.className = "is-pass";
    result.textContent = "Guardrails set. Continue to Attack mitigations.";
  });
  resetBtn.addEventListener("click", function () {
    root.querySelectorAll("[data-guard]").forEach(function (input) { input.checked = false; });
    clearMarks();
    result.className = "";
    result.textContent = "";
  });
})();
</script>"""

ACME_ATTACKS_SCRIPT = """<script>
(function () {
  var CONFIG = {
    "cfg-vector-access": "secure",
    "cfg-retrieval": "filter",
    "cfg-corpus": "approved",
    "cfg-training": "no-train",
    "cfg-logging": "redact",
    "cfg-context": "untrusted"
  };
  var GUARDS = {
    "gr-prompt-injection": true,
    "gr-output-pii": true,
    "gr-retrieval-filter": true,
    "gr-rate-limit": true,
    "gr-ingest-scan": true,
    "gr-anonymous": false,
    "gr-debug-prompts": false,
    "gr-external-tools": false
  };
  var ATTACKS = {
    "atk-1": "input-guard",
    "atk-2": "ingest-sanitize",
    "atk-3": "ingest-controls",
    "atk-4": "minimize-dlp",
    "atk-5": "rbac-retrieval"
  };
  var CORRECT_MSG =
    "Correct. Part 1 complete: secure configuration, guardrails, and attack mitigations all pass.";
  var root = document.getElementById("acme-attacks");
  if (!root) return;
  var actionBtns = root.querySelectorAll(".actions button");
  var checkBtn = actionBtns[0];
  var showBtn = actionBtns[1];
  var resetBtn = actionBtns[2];
  var result = root.querySelector(".actions [id$='result']");
  if (!checkBtn || !showBtn || !resetBtn || !result) return;
  function configOk() {
    var ok = true;
    document.querySelectorAll("#acme-config [data-setting]").forEach(function (sel) {
      if (sel.value !== CONFIG[sel.getAttribute("data-setting")]) ok = false;
    });
    return ok;
  }
  function guardsOk() {
    var ok = true;
    document.querySelectorAll("#acme-guardrails [data-guard]").forEach(function (input) {
      if (input.checked !== GUARDS[input.getAttribute("data-guard")]) ok = false;
    });
    return ok;
  }
  function attacksOk() {
    var ok = true;
    root.querySelectorAll("[data-attack]").forEach(function (sel) {
      var pass = sel.value === ATTACKS[sel.getAttribute("data-attack")];
      sel.classList.toggle("pbq-ai-select--bad", sel.value && !pass);
      sel.classList.toggle("pbq-ai-select--good", pass);
      if (!pass) ok = false;
    });
    return ok;
  }
  checkBtn.addEventListener("click", function () {
    var c = configOk();
    var g = guardsOk();
    var a = attacksOk();
    if (c && g && a) {
      result.className = "is-pass";
      result.textContent = CORRECT_MSG;
    } else {
      result.className = "is-fail";
      var parts = [];
      if (!c) parts.push("configuration (folder section)");
      if (!g) parts.push("guardrails (folder section)");
      if (!a) parts.push("attack mitigations");
      result.textContent = "Incorrect. Review " + parts.join(", ") + ".";
    }
  });
  showBtn.addEventListener("click", function () {
    Object.keys(ATTACKS).forEach(function (key) {
      var sel = root.querySelector('[data-attack="' + key + '"]');
      if (sel) sel.value = ATTACKS[key];
    });
    attacksOk();
    result.className = "is-pass";
    result.textContent = CORRECT_MSG;
  });
  resetBtn.addEventListener("click", function () {
    root.querySelectorAll("[data-attack]").forEach(function (sel) { sel.value = ""; });
    result.className = "";
    result.textContent = "";
  });
})();
</script>"""

UBUNTU_SCRIPT = """<script>
(function () {
  var root = document.querySelector("[data-ubuntu-harden]");
  if (!root) return;
  var gradeBtn = document.querySelector("#ubuntu-consequences .pbq-ssh-actions .btn-primary");
  var resetBtn = document.querySelector("#ubuntu-consequences .pbq-ssh-actions .btn-secondary");
  var gradeResult = document.querySelector("#ubuntu-consequences .result");
  var scoreSshd = document.querySelector("#ubuntu-intro #score-sshd");
  var scoreF2b = document.querySelector("#ubuntu-intro #score-f2b");
  var scoreUfw = document.querySelector("#ubuntu-intro #score-ufw");
  var scoreCq = document.querySelector("#ubuntu-intro #score-cq");
  var PASS_MSG =
    "Correct — all four areas pass. SSH is on 4422 with keys-only auth, fail2ban watches the same port, UFW allows management SSH and public web only with default deny inbound, and you understand lockout and persistence cleanup.";
  function fieldOk(select) {
    var val = select.value.trim();
    var want = select.getAttribute("data-correct");
    var pass = val !== "" && val === want;
    select.classList.toggle("pbq-ssh-select--ok", pass);
    select.classList.toggle("pbq-ssh-select--bad", val !== "" && !pass);
    return pass ? 1 : 0;
  }
  function gradeSshd() {
    var n = 0;
    document.querySelectorAll("#ubuntu-sshd .pbq-ssh-select").forEach(function (sel) { n += fieldOk(sel); });
    if (scoreSshd) scoreSshd.innerHTML = "sshd_config <strong>" + n + "</strong> / 7 pts";
    return n === 7;
  }
  function gradeFail2ban() {
    var n = 0;
    document.querySelectorAll("#ubuntu-fail2ban .pbq-ssh-select").forEach(function (sel) { n += fieldOk(sel); });
    if (scoreF2b) scoreF2b.innerHTML = "fail2ban <strong>" + n + "</strong> / 4 pts";
    return n === 4;
  }
  function gradeUfw() {
    var n = 0;
    document.querySelectorAll("#ubuntu-ufw .pbq-ssh-ufw-select").forEach(function (sel) {
      var val = sel.value.trim();
      var want = sel.getAttribute("data-correct");
      var pass = val !== "" && val === want;
      sel.classList.toggle("pbq-ssh-select--ok", pass);
      sel.classList.toggle("pbq-ssh-select--bad", val !== "" && !pass);
      if (pass) n += 1;
    });
    if (scoreUfw) scoreUfw.innerHTML = "ufw rules <strong>" + n + "</strong> / 3 pts";
    return n === 3;
  }
  function gradeConsequences() {
    var n = 0;
    document.querySelectorAll("#ubuntu-consequences .pbq-ssh-cq").forEach(function (fs) {
      var want = fs.getAttribute("data-correct");
      var picked = fs.querySelector('input[type="radio"]:checked');
      var pass = picked && picked.value === want;
      fs.classList.toggle("pbq-ssh-cq--ok", !!pass);
      fs.classList.toggle("pbq-ssh-cq--bad", picked && !pass);
      if (pass) n += 1;
    });
    if (scoreCq) scoreCq.innerHTML = "Consequence Qs <strong>" + n + "</strong> / 4 pts";
    return n === 4;
  }
  if (gradeBtn) gradeBtn.addEventListener("click", function () {
    var ok = gradeSshd() && gradeFail2ban() && gradeUfw() && gradeConsequences();
    if (!gradeResult) return;
    if (ok) {
      gradeResult.className = "result is-pass";
      gradeResult.textContent = PASS_MSG;
    } else {
      gradeResult.className = "result is-fail";
      gradeResult.textContent =
        "Not yet correct. Check score badges on Overview — align Port 4422 across sshd, fail2ban, and UFW.";
    }
  });
  if (resetBtn) resetBtn.addEventListener("click", function () {
    document.querySelectorAll("[id^='ubuntu-'] .pbq-ssh-select, [id^='ubuntu-'] .pbq-ssh-ufw-select").forEach(function (sel) {
      sel.selectedIndex = 0;
      sel.classList.remove("pbq-ssh-select--ok", "pbq-ssh-select--bad");
    });
    document.querySelectorAll("#ubuntu-consequences .pbq-ssh-cq input").forEach(function (r) { r.checked = false; });
    if (scoreSshd) scoreSshd.innerHTML = "sshd_config <strong>0</strong> / 7 pts";
    if (scoreF2b) scoreF2b.innerHTML = "fail2ban <strong>0</strong> / 4 pts";
    if (scoreUfw) scoreUfw.innerHTML = "ufw rules <strong>0</strong> / 3 pts";
    if (scoreCq) scoreCq.innerHTML = "Consequence Qs <strong>0</strong> / 4 pts";
    if (gradeResult) { gradeResult.className = ""; gradeResult.textContent = ""; }
  });
})();
</script>"""


def read_fragment(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"<article[^>]*>(.*)</article>", text, re.DOTALL)
    return m.group(1).strip() if m else text.strip()


def write_fragment(path: Path, section_id: str, inner: str, script: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = f'<article class="pbq-section-fragment" data-id="{section_id}">{inner}</article>'
    if script:
        body += "\n" + script.strip()
    path.write_text(body + "\n", encoding="utf-8")


def between(html: str, start: str, end: str) -> str:
    i = html.find(start)
    if i < 0:
        return ""
    j = html.find(end, i + len(start))
    return html[i : j if j >= 0 else len(html)].strip()


def split_acme() -> None:
    html = read_fragment(PBQ / "acme-rag-hr-ai/sections/acme-p1.html")
    base = PBQ / "acme-rag-hr-ai/sections"
    grid = between(html, '<div class="pbq-ai-exhibit-grid">', "</div>\n        </section>")
    arch = between(html, '<figure class="pbq-ai-arch"', "</figure>")
    config = between(
        html,
        '<section class="pbq-ai-section" aria-labelledby="config-heading">',
        '<section class="pbq-ai-section" aria-labelledby="guard-heading">',
    )
    guard = between(
        html,
        '<section class="pbq-ai-section" aria-labelledby="guard-heading">',
        '<section class="pbq-ai-section" aria-labelledby="attack-heading">',
    )
    attacks = between(
        html,
        '<section class="pbq-ai-section" aria-labelledby="attack-heading">',
        '<div class="actions">',
    )
    actions = between(html, '<div class="actions">', "</div>")

    exhibits = f"""<h1>Exhibits &amp; architecture</h1>
      <p class="pbq-sub">BeCertifiedToday HR RAG — open exhibits in popups; use architecture links to jump to the same content.</p>
      <div class="sim-frame pbq-ai-sim" data-acme-part1>
        {arch}
        <section class="pbq-ai-section" aria-labelledby="docs-heading">
          <h2 id="docs-heading">Policy corpus and retrieval exhibits</h2>
          {EXHIBIT_LAUNCHERS}
          <div class="pbq-exhibit-store" hidden aria-hidden="true"><div class="pbq-ai-exhibit-grid">{grid}</div></div>
        </section>
      </div>"""

    write_fragment(
        base / "acme-exhibits.html",
        "acme-exhibits",
        exhibits,
    )
    write_fragment(
        base / "acme-config.html",
        "acme-config",
        f'<h1>Task 1 — System configuration</h1><div data-acme-part1>{config}{actions}</div>',
        ACME_CONFIG_SCRIPT,
    )
    write_fragment(
        base / "acme-guardrails.html",
        "acme-guardrails",
        f'<h1>Task 2 — Guardrails</h1><div data-acme-part1>{guard}{actions}</div>',
        ACME_GUARD_SCRIPT,
    )
    write_fragment(
        base / "acme-attacks.html",
        "acme-attacks",
        f'<h1>Task 3 — Attack mitigations</h1><p class="pbq-instructions">Checks configuration and guardrails from prior folder sections too.</p><div data-acme-part1>{attacks}{actions}</div>',
        ACME_ATTACKS_SCRIPT,
    )


def split_zta() -> None:
    html = read_fragment(PBQ / "zero-trust-zta-migration/sections/zta-p1.html")
    script = re.search(r"<script(?![^>]*src=)[^>]*>.*?</script>", Path(PBQ / "zero-trust-zta-migration/sections/zta-p1.html").read_text(), re.DOTALL)
    fig = re.search(r"<figure class=\"pbq-exhibit.*?</figure>", html, re.DOTALL)
    fig_html = fig.group(0).replace('id="zt-exhibit-title"', 'id="zt-exhibit-panel"') if fig else ""
    stem_block = between(html, '<p class="pbq-stem"', '<div class="actions">')
    actions = between(html, '<div class="actions">', "</div>")
    base = PBQ / "zero-trust-zta-migration/sections"
    write_fragment(
        base / "zta-exhibit.html",
        "zta-exhibit",
        f"""<h1>Zero Trust — Reference exhibit</h1>
      <p class="pbq-sub">Open the exhibit popup, then answer the question under <strong>Core concept</strong>.</p>
      <div class="sim-frame">
        <button type="button" class="btn btn-primary" data-pbq-modal="#zt-exhibit-panel">Open exhibit — perimeter vs ZTA</button>
        <div class="pbq-exhibit-store" hidden aria-hidden="true">{fig_html}</div>
      </div>""",
    )
    write_fragment(
        base / "zta-concept.html",
        "zta-concept",
        f"<h1>Zero Trust — Core concept</h1><div class=\"sim-frame\">{stem_block}{actions}</div>",
        script.group(0) if script else "",
    )


def split_ubuntu() -> None:
    html = read_fragment(PBQ / "ubuntu-ssh-breach-hardening/sections/ubuntu-all.html")
    base = PBQ / "ubuntu-ssh-breach-hardening/sections"
    intro = re.search(
        r"(<header class=\"pbq-ssh-scenario\">.*?</div>\s*</div>)",
        html,
        re.DOTALL,
    )
    intro_html = intro.group(1) if intro else ""
    if "pbq-ssh-score-row" not in intro_html:
        intro_html = re.search(
            r"(<header.*?</header>\s*<div class=\"pbq-ssh-score-row\".*?</div>)",
            html,
            re.DOTALL,
        )
        intro_html = intro_html.group(1) if intro_html else ""

    def panel(name: str) -> str:
        m = re.search(rf'<div id="panel-{name}"[^>]*>.*?</div>\s*(?=<div id="panel-|<div class="pbq-ssh-actions")', html, re.DOTALL)
        return m.group(0) if m else ""

    actions = re.search(
        r'<div class="pbq-ssh-actions">.*?</div>\s*<p id="gradeResult".*?</p>',
        html,
        re.DOTALL,
    )
    write_fragment(
        base / "ubuntu-intro.html",
        "ubuntu-intro",
        f"{intro_html}<p class=\"pbq-instructions\">Use each folder section for one config area. Grade on <strong>Consequence Qs</strong>.</p>",
    )
    for key, title in [
        ("sshd", "sshd_config"),
        ("fail2ban", "jail.local (fail2ban)"),
        ("ufw", "UFW rules"),
    ]:
        write_fragment(
            base / f"ubuntu-{key}.html",
            f"ubuntu-{key}",
            f'<h1>{title}</h1><div class="pbq-ssh-sim" data-ubuntu-harden>{panel(key)}</div>',
        )
    cq = panel("consequences")
    write_fragment(
        base / "ubuntu-consequences.html",
        "ubuntu-consequences",
        f'<h1>Consequence questions</h1><div data-ubuntu-harden>{cq}{actions.group(0) if actions else ""}</div>',
        UBUNTU_SCRIPT,
    )


def patch_acme_p2() -> None:
    path = PBQ / "acme-rag-hr-ai/sections/acme-p2.html"
    text = path.read_text(encoding="utf-8")
    fig = re.search(r'<figure class="pbq-ai-exhibit[^>]*id="exhibit-part2-chat".*?</figure>', text, re.DOTALL)
    if not fig:
        return
    html = read_fragment(path)
    html = html.replace(
        fig.group(0),
        '<p><button type="button" class="btn btn-secondary" data-pbq-modal="#exhibit-part2-chat">Open exhibit — prompt injection chat log</button></p>',
    )
    html += f'\n<div class="pbq-exhibit-store" hidden aria-hidden="true">{fig.group(0)}</div>'
    script = re.search(r"<script(?![^>]*src=)[^>]*>.*?</script>", text, re.DOTALL)
    write_fragment(path, "acme-p2", html, script.group(0) if script else "")


def main() -> None:
    split_acme()
    split_zta()
    split_ubuntu()
    patch_acme_p2()
    print("split-pbq-sections: done")


if __name__ == "__main__":
    main()
