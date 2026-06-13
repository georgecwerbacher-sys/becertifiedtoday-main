/**
 * Shared CLI container helpers (templates/containers/cli-container-template.html).
 * Labs keep device-specific ids (scrollR10, cmdR10, …); markup uses template classes
 * scrollback-area, prompt-el, cmdline-input alongside legacy names.
 */
(function () {
  function isModeNavigationCommand(normalizedCmd) {
    var u = String(normalizedCmd || "");
    return (
      u === "configure terminal" ||
      u === "end" ||
      u === "exit" ||
      u.indexOf("interface ") === 0
    );
  }

  function expandInterfaceEcho(raw) {
    var s = String(raw || "").trim();
    var m = /^(interface|int)\s+e(\d+)\/(\d+)$/i.exec(s);
    if (m) {
      return "interface Ethernet" + m[2] + "/" + m[3];
    }
    return s;
  }

  var CLI_UNSUPPORTED_MSG = "% command not supported in this lab simulation";
  var CLI_UNSUPPORTED_NUMERIC_HINT_MSG =
    "% command not supported in this lab simulation — check the lab Tasks and Verification sections for the exact values.";
  var CLI_VERIFY_INSTRUCTIONS_MSG =
    "% command not supported in this lab simulation. Verify the lab instructions (Tasks and Helper) for the required values.";
  var COPY_RUN_START_OK_MSG = "configuration has been written to memory";
  var CCNA_TRAINING_PORTAL_HREF = "/CCNA-Study/CCNA_Training_Portal.html";
  /** Order matches CCNA_Training_Portal.html Lab Simulations grid. */
  var CCNA_LAB_CHAIN = [
    "/CCNA-Study/CCNA_labs/cli-lab-trunk_lacp.html",
    "/CCNA-Study/CCNA_labs/cli-lab-vlan-sim.html",
    "/CCNA-Study/CCNA_labs/cli-lab-ip-services-sim-v2.html",
    "/CCNA-Study/CCNA_labs/cli-lab-nat-dhcp-sim.html",
    "/CCNA-Study/CCNA_labs/cli-lab-native_vlan_lacp.html",
    "/CCNA-Study/CCNA_labs/cli-lab-static-routing.html",
    "/CCNA-Study/CCNA_labs/ipv4_ipv6_assign.html",
    "/CCNA-Study/CCNA_labs/cli-lab-ospf_config_sim_v3.html",
    "/CCNA-Study/CCNA_labs/cli-lab-named-acl-snoopimg.html",
  ];

  /** @deprecated use CLI_UNSUPPORTED_MSG */
  var INVALID_INPUT_MSG = CLI_UNSUPPORTED_MSG;
  /** @deprecated use CLI_UNSUPPORTED_NUMERIC_HINT_MSG */
  var INVALID_INPUT_NUMERIC_HINT_MSG = CLI_UNSUPPORTED_NUMERIC_HINT_MSG;

  function invalidInputMsgForNormalizedCmd(u) {
    return /\d/.test(String(u || "")) ? CLI_UNSUPPORTED_NUMERIC_HINT_MSG : CLI_UNSUPPORTED_MSG;
  }

  function unsupportedCmdMsg(u) {
    return invalidInputMsgForNormalizedCmd(u);
  }

  var LAB_SUBMODE_CONTEXT_MODES = {
    "config-if": true,
    "config-if-range": true,
    "config-std-nacl": true,
    "config-ext-nacl": true,
    "config-vlan": true,
    "config-line": true,
    "config-router": true,
  };

  var LAB_INTERFACE_ENTRY_PROBES = [
    "interface gigabitethernet0/0",
    "interface gigabitethernet0/1",
    "interface gigabitethernet0/2",
    "interface ethernet0/0",
    "interface ethernet0/1",
    "interface ethernet0/2",
    "interface range gigabitethernet0/1 - 2",
    "interface port-channel15",
    "interface loopback0",
    "interface vlan1",
  ];

  function stepTestPasses(step, line) {
    if (!step || typeof step.test !== "function") return false;
    try {
      return !!step.test(line);
    } catch (_) {
      return false;
    }
  }

  function findStepIndexMatchingLine(steps, fromIndex, line) {
    if (!steps || fromIndex < 0) return -1;
    for (var i = Math.max(0, fromIndex); i < steps.length; i++) {
      if (stepTestPasses(steps[i], line)) return i;
    }
    return -1;
  }

  function isInterfaceNavCommand(u) {
    return u.indexOf("interface ") === 0;
  }

  function promptEndsWithConfig(promptText) {
    return /\(config\)#$/.test(String(promptText || ""));
  }

  function promptEndsWithConfigSubmode(promptText) {
    return /\(config-[^)]+\)#$/.test(String(promptText || ""));
  }

  function isSkippableStepForInterfaceSwitch(step) {
    if (!step) return false;
    if (stepTestPasses(step, "exit")) return true;
    if (step.mode === "config" || step.mode === "config-if-range") {
      for (var i = 0; i < LAB_INTERFACE_ENTRY_PROBES.length; i++) {
        if (stepTestPasses(step, LAB_INTERFACE_ENTRY_PROBES[i])) return true;
      }
    }
    return false;
  }

  /**
   * IOS: from (config-if)# (or other config sub-mode), type the next interface command without exit.
   * Also accepts interface entry from (config)# when a pending exit step was soft-skipped.
   * @returns {{ newStepIndex: number }|null}
   */
  function tryLabDirectInterfaceSwitch(opts) {
    var steps = opts.steps;
    var stepIndex = opts.stepIndex;
    var line = opts.line;
    var u = String(opts.normalizedCmd != null ? opts.normalizedCmd : line || "");
    var promptText = opts.promptText || "";

    if (!steps || stepIndex >= steps.length) return null;
    if (!isInterfaceNavCommand(u)) return null;

    var inSubmode = promptEndsWithConfigSubmode(promptText);
    var inConfig = promptEndsWithConfig(promptText);
    if (!inSubmode && !inConfig) return null;

    var targetIdx = findStepIndexMatchingLine(steps, stepIndex, line);
    if (targetIdx === -1 || targetIdx < stepIndex) return null;

    for (var j = stepIndex; j < targetIdx; j++) {
      if (!isSkippableStepForInterfaceSwitch(steps[j])) return null;
    }

    return { newStepIndex: targetIdx + 1 };
  }

  /**
   * After soft exit to (config)#, re-enter ACL/interface/router sub-mode for the pending step.
   * @returns {{ reenter: true }|null}
   */
  function tryLabReenterSubmodeContext(opts) {
    var steps = opts.steps;
    var stepIndex = opts.stepIndex;
    var line = opts.line;
    var u = String(opts.normalizedCmd != null ? opts.normalizedCmd : line || "");
    var overrideMode = opts.overrideMode;

    if (!steps || stepIndex >= steps.length) return null;
    if (overrideMode !== "config") return null;

    var pending = steps[stepIndex];
    var pendingMode = pending && pending.mode;
    if (!LAB_SUBMODE_CONTEXT_MODES[pendingMode]) return null;

    if (pendingMode === "config-std-nacl" && u.indexOf("ip access-list") === 0) {
      for (var k = stepIndex - 1; k >= 0; k--) {
        if (steps[k].mode === "config" && stepTestPasses(steps[k], line)) {
          return { reenter: true };
        }
        if (steps[k].mode === "exec") break;
      }
    }

    if (pendingMode === "config-router" && u.indexOf("router ") === 0) {
      for (var r = stepIndex - 1; r >= 0; r--) {
        if (steps[r].mode === "config" && stepTestPasses(steps[r], line)) {
          return { reenter: true };
        }
        if (steps[r].mode === "exec") break;
      }
    }

    if (isInterfaceNavCommand(u)) {
      for (var n = stepIndex - 1; n >= 0; n--) {
        if ((steps[n].mode === "config" || steps[n].mode === "config-if-range") && stepTestPasses(steps[n], line)) {
          return { reenter: true };
        }
        if (steps[n].mode === "exec") break;
      }
      if (stepIndex > 0 && stepTestPasses(steps[stepIndex - 1], line)) {
        return { reenter: true };
      }
    }

    return null;
  }

  /**
   * Shared IOS-like interface context navigation for graded LAB_STEPS engines.
   * @returns {boolean} true when the line was handled (direct switch or sub-mode re-entry)
   */
  function applyLabStepInterfaceNav(opts) {
    var direct = tryLabDirectInterfaceSwitch(opts);
    if (direct) {
      var prevStepIndex = opts.stepIndex;
      if (typeof opts.setStepIndex === "function") opts.setStepIndex(direct.newStepIndex);
      if (typeof opts.clearOverride === "function") opts.clearOverride();
      if (typeof opts.refreshPrompt === "function") opts.refreshPrompt();
      if (typeof opts.onStepAdvanced === "function") {
        opts.onStepAdvanced(prevStepIndex, direct.newStepIndex);
      }
      return true;
    }
    var reenter = tryLabReenterSubmodeContext(opts);
    if (reenter) {
      if (typeof opts.clearOverride === "function") opts.clearOverride();
      if (typeof opts.refreshPrompt === "function") opts.refreshPrompt();
      return true;
    }
    return false;
  }

  var localHistoryByInput = new WeakMap();

  function getLocalHistoryState(input) {
    var state = localHistoryByInput.get(input);
    if (state) return state;
    state = { entries: [], idx: 0 };
    localHistoryByInput.set(input, state);
    return state;
  }

  function pushLocalHistory(input, raw) {
    var cmd = String(raw || "").trim();
    if (!cmd) return;
    var state = getLocalHistoryState(input);
    if (!state.entries.length || state.entries[state.entries.length - 1] !== cmd) {
      state.entries.push(cmd);
    }
    state.idx = state.entries.length;
  }

  function bindLocalHistory(input) {
    if (!input || input.dataset.localHistoryReady === "1") return;
    input.dataset.localHistoryReady = "1";
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        pushLocalHistory(input, input.value);
        return;
      }
      var usePrev = e.key === "ArrowUp" || (e.key === "Tab" && !e.shiftKey);
      var useNext = e.key === "ArrowDown" || (e.key === "Tab" && e.shiftKey);
      if (!usePrev && !useNext) return;
      var state = getLocalHistoryState(input);
      if (!state.entries.length) return;
      e.preventDefault();
      if (usePrev) {
        state.idx = Math.max(0, state.idx - 1);
      } else {
        state.idx = Math.min(state.entries.length, state.idx + 1);
      }
      input.value = state.idx >= state.entries.length ? "" : state.entries[state.idx];
    });
  }

  function pathLooksLikeCcnaLab(p) {
    p = String(p || "").toLowerCase();
    return (
      p.indexOf("/ccna-study/ccna_labs/") !== -1 ||
      p.indexOf("/ccna_sim_exam/embed/lab/") !== -1
    );
  }

  function isCcnaLabEmbedPath() {
    if (pathLooksLikeCcnaLab(location.pathname)) return true;
    try {
      return pathLooksLikeCcnaLab(sessionStorage.getItem("ccnaLastRealPath"));
    } catch (_) {}
    return !!document.querySelector(".cli-modal-overlay .scrollback-area");
  }

  function isExamSimEmbed() {
    try {
      return new URLSearchParams(location.search).get("examSim") === "1";
    } catch (_) {
      return false;
    }
  }

  /** CCNA CLI lab pages (portal, sample, timed exam embed). */
  function isBctCliBannerContext() {
    return isCcnaLabEmbedPath();
  }

  var EXAM_SIM_CLI_BANNER_TEXT =
    "================================================================================\n" +
    "  Be Certified Today — BCT Lab Simulator v.1_2026\n" +
    "================================================================================\n" +
    "\n" +
    "Help commands are disabled; only commands required for this lab scenario are\n" +
    "available. Use the Helper button to review the lab outline and topology if needed.\n" +
    "================================================================================";

  /** Login-style banner when a CLI modal opens on CCNA lab pages. */
  function showExamSimCliBanner(scrollbackEl) {
    if (!scrollbackEl || !isBctCliBannerContext()) return;
    var prev = scrollbackEl.querySelector('[data-bct-exam-sim-banner="1"]');
    if (prev) prev.remove();
    var div = document.createElement("div");
    div.className = "line-boot";
    div.setAttribute("data-bct-exam-sim-banner", "1");
    div.style.whiteSpace = "pre-wrap";
    div.textContent = EXAM_SIM_CLI_BANNER_TEXT;
    scrollbackEl.insertBefore(div, scrollbackEl.firstChild);
    scrollbackEl.scrollTop = 0;
  }

  var BCT_CLI_BANNER_LAB_CSS =
    ".terminal .line-boot{white-space:pre-wrap;word-break:break-word;color:#94a3b8;font-size:.82rem;line-height:1.45;margin-bottom:10px;padding:10px 12px;border-radius:6px;background:#0a0e14;border:1px solid #1e293b}" +
    ".scrollback-area .line-show-help{white-space:pre-wrap;margin:4px 0 8px}";

  function injectBctCliBannerLabStyles() {
    if (!isBctCliBannerContext()) return;
    if (document.head.querySelector("style[data-bcc-cli-banner-lab]")) return;
    var s = document.createElement("style");
    s.setAttribute("data-bcc-cli-banner-lab", "1");
    s.textContent = BCT_CLI_BANNER_LAB_CSS;
    document.head.appendChild(s);
  }

  function wireBctCliOpenBanner() {
    if (!isBctCliBannerContext()) return;

    function onOverlayOpened(overlay) {
      if (!overlay || !overlay.classList.contains("is-open")) return;
      requestAnimationFrame(function () {
        var scroll = overlay.querySelector(".scrollback-area");
        if (scroll) showExamSimCliBanner(scroll);
      });
    }

    document.querySelectorAll(".cli-modal-overlay").forEach(function (overlay) {
      if (overlay.dataset.bctExamSimCliBanner === "1") return;
      overlay.dataset.bctExamSimCliBanner = "1";
      new MutationObserver(function (mutations) {
        mutations.forEach(function (m) {
          if (m.attributeName === "class") onOverlayOpened(overlay);
        });
      }).observe(overlay, { attributes: true, attributeFilter: ["class"] });
      if (overlay.classList.contains("is-open")) onOverlayOpened(overlay);
    });
  }

  function initBctCliBanner() {
    if (!isBctCliBannerContext()) return;
    injectBctCliBannerLabStyles();
    wireBctCliOpenBanner();
  }

  function scheduleBctCliBannerInit() {
    function run() {
      initBctCliBanner();
    }
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", run, { once: true });
      return;
    }
    if (document.querySelector(".cli-modal-overlay")) {
      run();
      return;
    }
    document.addEventListener("DOMContentLoaded", run, { once: true });
  }

  scheduleBctCliBannerInit();

  function normalizeLabPagePath(p) {
    var s = String(p || "").split("#")[0].split("?")[0];
    if (!s) return "";
    if (s.length > 1 && s.charAt(s.length - 1) === "/") s = s.slice(0, -1);
    return s;
  }

  function ccnaLabChainIndex(pathname) {
    var cur = normalizeLabPagePath(pathname);
    for (var i = 0; i < CCNA_LAB_CHAIN.length; i++) {
      if (normalizeLabPagePath(CCNA_LAB_CHAIN[i]) === cur) return i;
    }
    return -1;
  }

  function ccnaLabTopChromeStyles() {
    return (
      "body.bcc-ccna-lab-top-chrome .page-logo-watermark{" +
      "position:fixed;inset:0;z-index:0;pointer-events:none;display:flex;align-items:center;justify-content:center;overflow:hidden;" +
      "}" +
      "body.bcc-ccna-lab-top-chrome .page-logo-watermark img{" +
      "width:min(85vw,720px);max-height:85vh;height:auto;object-fit:contain;opacity:0.16;" +
      "}" +
      "body.bcc-ccna-lab-top-chrome .wrap{position:relative;z-index:1;}" +
      "body.bcc-ccna-lab-top-chrome .lab-top-bar{" +
      "display:flex;justify-content:flex-end;align-items:center;flex-direction:row-reverse;gap:12px;width:100%;margin:0 0 2rem;" +
      "}" +
      "body.bcc-ccna-lab-top-chrome .lab-top-bar .site-logo-corner," +
      "body.bcc-ccna-lab-top-chrome.bcc-sample-experience .lab-top-bar .site-logo-corner," +
      "body.bcc-ccna-lab-top-chrome.ccna-sample-guest-ui .lab-top-bar .site-logo-corner{" +
      "position:static!important;" +
      "top:auto!important;" +
      "left:auto!important;" +
      "right:auto!important;" +
      "bottom:auto!important;" +
      "z-index:auto!important;" +
      "display:inline-flex!important;" +
      "align-items:center!important;" +
      "justify-content:center!important;" +
      "align-self:flex-end!important;" +
      "margin:0!important;" +
      "background:transparent!important;" +
      "border:none!important;" +
      "padding:0!important;" +
      "backdrop-filter:none!important;" +
      "box-shadow:none!important;" +
      "border-radius:0!important;" +
      "pointer-events:auto!important;" +
      "}" +
      "body.bcc-ccna-lab-top-chrome a.site-logo-corner{text-decoration:none!important;color:inherit!important;}" +
      "body.bcc-ccna-lab-top-chrome a.site-logo-corner:focus-visible{outline:2px solid #4f84d8!important;outline-offset:3px!important;}" +
      "body.bcc-ccna-lab-top-chrome .lab-top-bar .site-logo-corner img{display:block;width:52px;height:52px;background:transparent!important;}" +
      "body.bcc-ccna-lab-top-chrome span.site-logo-corner{pointer-events:none!important;}" +
      "body.bcc-ccna-lab-top-chrome .lab-top-bar .lab-top-next," +
      "body.bcc-ccna-lab-top-chrome.bcc-sample-experience .lab-top-bar .lab-top-next{" +
      "position:static!important;" +
      "top:auto!important;" +
      "right:auto!important;" +
      "left:auto!important;" +
      "z-index:auto!important;" +
      "flex:0 0 auto!important;" +
      "margin:0!important;" +
      "text-decoration:none!important;" +
      "background:#254b8a!important;" +
      "border:1px solid #3d6dbb!important;" +
      "color:#e6edf3!important;" +
      "border-radius:10px!important;" +
      "padding:10px 16px!important;" +
      "font-weight:700!important;" +
      "font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif!important;" +
      "font-size:0.9rem!important;" +
      "box-shadow:none!important;" +
      "}" +
      "body.bcc-ccna-lab-top-chrome .lab-top-bar .lab-top-next:hover{filter:brightness(1.08)!important;}" +
      "body.bcc-ccna-lab-top-chrome .lab-top-bar .lab-top-next:focus-visible{outline:2px solid #4f84d8!important;outline-offset:3px!important;}" +
      "body.bcc-ccna-lab-top-chrome.ccna-question-ui{" +
      "background:#ffffff!important;color:#1a3d6e!important;position:relative!important;" +
      "}" +
      "body.bcc-ccna-lab-top-chrome .card,body.bcc-ccna-lab-top-chrome main.card{" +
      "background:transparent!important;border:none!important;box-shadow:none!important;color:#1a3d6e!important;" +
      "}" +
      "body.bcc-ccna-lab-top-chrome h1,body.bcc-ccna-lab-top-chrome .wrap h2,body.bcc-ccna-lab-top-chrome .wrap h3,body.bcc-ccna-lab-top-chrome .wrap h4{" +
      "color:#1a3d6e!important;" +
      "}" +
      "body.bcc-ccna-lab-top-chrome .wrap .objective,body.bcc-ccna-lab-top-chrome .wrap .tasks,body.bcc-ccna-lab-top-chrome .wrap .tasks li," +
      "body.bcc-ccna-lab-top-chrome .wrap .study-meta,body.bcc-ccna-lab-top-chrome .wrap .lab-spoiler-note,body.bcc-ccna-lab-top-chrome .wrap p," +
      "body.bcc-ccna-lab-top-chrome .wrap li,body.bcc-ccna-lab-top-chrome .wrap label,body.bcc-ccna-lab-top-chrome .wrap .device-pick," +
      "body.bcc-ccna-lab-top-chrome .wrap .device-pick strong{" +
      "color:#1a3d6e!important;" +
      "}" +
      "body.bcc-ccna-lab-top-chrome h1{color:#1a3d6e!important;}" +
      "body.bcc-ccna-lab-top-chrome .wrap .tasks-blue-box,body.bcc-ccna-lab-top-chrome .wrap .device-pick,body.bcc-ccna-lab-top-chrome .wrap .topology-scrape," +
      "body.bcc-ccna-lab-top-chrome .wrap .address-table-wrap,body.bcc-ccna-lab-top-chrome .wrap .lab-info-panel{" +
      "background:transparent!important;border:1px solid #3d6dbb!important;color:#1a3d6e!important;" +
      "}" +
      "body.bcc-ccna-lab-top-chrome .tasks-blue-box .tasks,body.bcc-ccna-lab-top-chrome .tasks-blue-box ol.tasks," +
      "body.bcc-ccna-lab-top-chrome .tasks-blue-box ol.tasks li,body.bcc-ccna-lab-top-chrome .tasks-blue-box .tasks strong," +
      "body.bcc-ccna-lab-top-chrome .tasks-blue-box ol.tasks strong,body.bcc-ccna-lab-top-chrome .topology-scrape p.helper-cli-desc{" +
      "color:#1a3d6e!important;" +
      "}" +
      "body.bcc-ccna-lab-top-chrome .wrap .diagram-wrap{" +
      "background:#ffffff!important;border:1px solid #3d6dbb!important;" +
      "}" +
      "body.bcc-ccna-lab-top-chrome .sim-nav{" +
      "background:rgba(255,255,255,0.94)!important;border-top:1px solid #3d6dbb!important;" +
      "}" +
      "body.bcc-ccna-lab-top-chrome .pass-banner{" +
      "color:#ffffff!important;" +
      "}"
    );
  }

  function ensureLabPageWatermark() {
    if (document.querySelector(".page-logo-watermark")) return;
    var wm = document.createElement("div");
    wm.className = "page-logo-watermark";
    wm.setAttribute("aria-hidden", "true");
    wm.innerHTML =
      '<img src="/images/logo/becertifiedtoday_logo_image_trans.png" alt="" />';
    document.body.insertBefore(wm, document.body.firstChild);
  }

  function ensureLabTopBar() {
    var wrap = document.querySelector(".wrap");
    if (!wrap) return null;
    var bar = wrap.querySelector(".lab-top-bar");
    if (!bar) {
      bar = document.createElement("header");
      bar.className = "lab-top-bar";
      bar.setAttribute("aria-label", "Lab navigation");
      wrap.insertBefore(bar, wrap.firstChild);
    }
    return bar;
  }

  function ensureCcnaLabLogoLink() {
    var logo = document.querySelector(".site-logo-corner");
    if (!logo || logo.tagName === "SPAN") return null;
    var anchor = logo;
    if (logo.tagName !== "A") {
      anchor = document.createElement("a");
      anchor.className = logo.className;
      anchor.innerHTML = logo.innerHTML;
      logo.parentNode.replaceChild(anchor, logo);
    }
    anchor.href = CCNA_TRAINING_PORTAL_HREF;
    anchor.setAttribute("aria-label", "CCNA training portal");
    anchor.removeAttribute("aria-hidden");
    anchor.style.background = "transparent";
    anchor.style.border = "none";
    anchor.style.padding = "0";
    anchor.style.backdropFilter = "none";
    anchor.style.boxShadow = "none";
    anchor.style.borderRadius = "0";
    var logoImg = anchor.querySelector("img");
    if (logoImg) logoImg.style.background = "transparent";
    return anchor;
  }

  function wireCcnaLabNextButton(chainIdx, bar) {
    if (chainIdx < 0 || !bar) return;
    var existing = bar.querySelector(".lab-top-next");
    if (existing) existing.remove();
    var nextHref =
      chainIdx < CCNA_LAB_CHAIN.length - 1
        ? CCNA_LAB_CHAIN[chainIdx + 1]
        : CCNA_TRAINING_PORTAL_HREF;
    var label = chainIdx < CCNA_LAB_CHAIN.length - 1 ? "Next lab" : "Training portal";
    var btn = document.createElement("a");
    btn.className = "lab-top-next";
    btn.href = nextHref;
    btn.textContent = label;
    btn.setAttribute(
      "aria-label",
      chainIdx < CCNA_LAB_CHAIN.length - 1 ? "Open next lab simulation" : "Back to CCNA training portal"
    );
    bar.appendChild(btn);
  }

  function initCcnaLabTopChrome() {
    var chainIdx = ccnaLabChainIndex(location.pathname);
    if (chainIdx < 0) return;
    if (!document.head.querySelector("style[data-bcc-ccna-lab-top-chrome]")) {
      var styleEl = document.createElement("style");
      styleEl.setAttribute("data-bcc-ccna-lab-top-chrome", "1");
      styleEl.textContent = ccnaLabTopChromeStyles();
      document.head.appendChild(styleEl);
    }
    document.body.classList.add("bcc-ccna-lab-top-chrome", "ccna-question-ui");
    ensureLabPageWatermark();
    var bar = ensureLabTopBar();
    var logo = ensureCcnaLabLogoLink();
    if (logo && bar && logo.parentNode !== bar) {
      bar.insertBefore(logo, bar.firstChild);
    }
    wireCcnaLabNextButton(chainIdx, bar);
  }

  function scheduleCcnaLabTopChromeInit() {
    function run() {
      initCcnaLabTopChrome();
    }
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", run, { once: true });
      return;
    }
    run();
  }

  scheduleCcnaLabTopChromeInit();

  /**
   * Baseline IOS `?` help for all router labs (privileged EXEC + config submodes).
   * Override per lab: pass `routerHelp: { show: [...], configGlobal: [...], ... }` to tryAppendIosHelp,
   * or set `var ROUTER_CLI_HELP = { ipRoute: [...] }` in the lab page (only overridden keys replace defaults).
   */
  var DEFAULT_ROUTER_CLI_HELP = {
    /** Privileged EXEC — host# ? */
    exec: [
      { cmd: "configure" },
      { cmd: "show" },
      { cmd: "ping" },
      { cmd: "traceroute" },
      { cmd: "copy" },
      { cmd: "erase" },
      { cmd: "reload" },
      { cmd: "exit" },
      { cmd: "disable" },
      { cmd: "terminal" },
      { cmd: "ssh" },
      { cmd: "telnet" },
      { cmd: "debug" },
      { cmd: "undebug" },
    ],
    show: [
      { cmd: "clock" },
      { cmd: "history" },
      { cmd: "ip interface brief" },
      { cmd: "ip route" },
      { cmd: "running-config" },
      { cmd: "startup-config" },
      { cmd: "version" },
    ],
    configExec: [
      { cmd: "memory" },
      { cmd: "network" },
      { cmd: "overwrite-network" },
      { cmd: "terminal" },
    ],
    configGlobal: [
      { cmd: "aaa" },
      { cmd: "access-list" },
      { cmd: "banner" },
      { cmd: "boot" },
      { cmd: "cdp" },
      { cmd: "crypto" },
      { cmd: "do" },
      { cmd: "enable" },
      { cmd: "end" },
      { cmd: "exit" },
      { cmd: "hostname" },
      { cmd: "interface" },
      { cmd: "ip" },
      { cmd: "line" },
      { cmd: "logging" },
      { cmd: "mac" },
      { cmd: "ntp" },
      { cmd: "router" },
      { cmd: "service" },
      { cmd: "snmp-server" },
      { cmd: "username" },
      { cmd: "vlan" },
      { cmd: "vrf" },
    ],
    configIf: [
      { cmd: "ip address <ip-address> <subnet-mask>" },
      { cmd: "description <text>" },
      { cmd: "shutdown" },
      { cmd: "no shutdown" },
      { cmd: "exit" },
      { cmd: "do <command>" },
      { cmd: "end" },
    ],
    configLine: [
      { cmd: "exec-timeout <minutes> <seconds>" },
      { cmd: "logging synchronous" },
      { cmd: "exit" },
      { cmd: "do <command>" },
      { cmd: "end" },
    ],
    configRouter: [
      { cmd: "network" },
      { cmd: "passive-interface" },
      { cmd: "router-id" },
      { cmd: "exit" },
    ],
    configAcl: [{ cmd: "deny" }, { cmd: "permit" }, { cmd: "exit" }],
    ip: [
      { cmd: "route" },
      { cmd: "routing" },
      { cmd: "cef" },
      { cmd: "subnet-zero" },
      { cmd: "default-gateway" },
      { cmd: "default-network" },
    ],
    ipRoute: [
      { cmd: "ip route <destination_network> <subnet_mask> <next_hop_or_interface>" },
      { cmd: "<A.B.C.D>" },
      { cmd: "vrf" },
      { cmd: "profile" },
      { cmd: "track" },
      { cmd: "multicast" },
    ],
  };

  /** Baseline IOS `?` help for switch labs — override via opts.switchHelp (same key names). */
  var DEFAULT_SWITCH_CLI_HELP = {
    exec: DEFAULT_ROUTER_CLI_HELP.exec,
    show: [
      { cmd: "history" },
      { cmd: "interfaces trunk" },
      { cmd: "etherchannel summary" },
      { cmd: "ip interface brief" },
      { cmd: "mac address-table" },
      { cmd: "running-config" },
      { cmd: "startup-config" },
      { cmd: "version" },
      { cmd: "vlan brief" },
    ],
    configExec: DEFAULT_ROUTER_CLI_HELP.configExec,
    configGlobal: [
      { cmd: "hostname <name>" },
      { cmd: "vlan <vlan-id>" },
      { cmd: "interface <interface-id>" },
      { cmd: "spanning-tree" },
      { cmd: "line con 0" },
      { cmd: "line vty 0 4" },
      { cmd: "exit" },
      { cmd: "do <command>" },
      { cmd: "end" },
    ],
    configIf: [
      { cmd: "description <text>" },
      { cmd: "switchport" },
      { cmd: "channel-group" },
      { cmd: "spanning-tree" },
      { cmd: "shutdown" },
      { cmd: "no shutdown" },
      { cmd: "exit" },
      { cmd: "do <command>" },
      { cmd: "end" },
    ],
    configLine: DEFAULT_ROUTER_CLI_HELP.configLine,
    configRouter: [],
    configAcl: DEFAULT_ROUTER_CLI_HELP.configAcl,
    ip: [],
    ipRoute: [],
  };

  /** @deprecated use DEFAULT_ROUTER_CLI_HELP.show */
  var SHOW_HELP_ROUTER = DEFAULT_ROUTER_CLI_HELP.show;
  /** @deprecated use DEFAULT_SWITCH_CLI_HELP.show */
  var SHOW_HELP_SWITCH = DEFAULT_SWITCH_CLI_HELP.show;
  /** @deprecated use DEFAULT_ROUTER_CLI_HELP.configExec */
  var CONFIG_HELP_EXEC = DEFAULT_ROUTER_CLI_HELP.configExec;
  /** @deprecated use DEFAULT_ROUTER_CLI_HELP.ip */
  var IP_HELP_CONFIG_ROUTER = DEFAULT_ROUTER_CLI_HELP.ip;
  /** @deprecated use DEFAULT_ROUTER_CLI_HELP.ipRoute */
  var IP_ROUTE_HELP_CONFIG_ROUTER = DEFAULT_ROUTER_CLI_HELP.ipRoute;
  /** @deprecated use DEFAULT_ROUTER_CLI_HELP.configGlobal */
  var MODE_HELP_CONFIG_ROUTER = DEFAULT_ROUTER_CLI_HELP.configGlobal;
  /** @deprecated use DEFAULT_SWITCH_CLI_HELP.configGlobal */
  var MODE_HELP_CONFIG_SWITCH = DEFAULT_SWITCH_CLI_HELP.configGlobal;
  /** @deprecated use DEFAULT_ROUTER_CLI_HELP.configIf */
  var MODE_HELP_CONFIG_IF_ROUTER = DEFAULT_ROUTER_CLI_HELP.configIf;
  /** @deprecated use DEFAULT_SWITCH_CLI_HELP.configIf */
  var MODE_HELP_CONFIG_IF_SWITCH = DEFAULT_SWITCH_CLI_HELP.configIf;
  /** @deprecated use DEFAULT_ROUTER_CLI_HELP.configLine */
  var MODE_HELP_CONFIG_LINE = DEFAULT_ROUTER_CLI_HELP.configLine;
  /** @deprecated use DEFAULT_ROUTER_CLI_HELP.configRouter */
  var MODE_HELP_CONFIG_ROUTER_OSPF = DEFAULT_ROUTER_CLI_HELP.configRouter;
  /** @deprecated use DEFAULT_ROUTER_CLI_HELP.configAcl */
  var MODE_HELP_CONFIG_ACL = DEFAULT_ROUTER_CLI_HELP.configAcl;

  function defaultHelpBundle(deviceType) {
    return deviceType === "switch" ? DEFAULT_SWITCH_CLI_HELP : DEFAULT_ROUTER_CLI_HELP;
  }

  /**
   * Resolve a help list: lab override (full replace for that key) or shared default.
   * @param {object} opts - tryAppendIosHelp options
   * @param {'router'|'switch'} deviceType
   * @param {string} key - e.g. show, configGlobal, ipRoute
   */
  function resolveHelpList(opts, deviceType, key) {
    opts = opts || {};
    var labHelp = deviceType === "switch" ? opts.switchHelp : opts.routerHelp;
    if (labHelp && Array.isArray(labHelp[key]) && labHelp[key].length) {
      return labHelp[key];
    }
    var defaults = defaultHelpBundle(deviceType);
    return defaults[key] || [];
  }

  /**
   * Build tryAppendIosHelp options for a lab device session.
   * @param {'router'|'switch'} deviceType
   * @param {string} promptText
   * @param {object|null|undefined} labHelp - partial override; null uses all defaults
   */
  function iosHelpOpts(deviceType, promptText, labHelp) {
    var o = { deviceType: deviceType, promptText: promptText };
    if (labHelp && typeof labHelp === "object") {
      if (deviceType === "switch") o.switchHelp = labHelp;
      else o.routerHelp = labHelp;
    }
    return o;
  }

  function isShowHelpQuery(raw) {
    var t = String(raw || "")
      .trim()
      .toLowerCase()
      .replace(/\s+/g, " ");
    return t === "show ?" || t === "sh ?" || t === "do show ?" || t === "do sh ?";
  }

  /**
   * @param {{deviceType?:'router'|'switch', extra?:Array<{cmd:string}>}} [opts]
   */
  function showCommandHelpText(opts) {
    opts = opts || {};
    var deviceType = opts.deviceType || "router";
    return formatHelpEntries(resolveHelpList(opts, deviceType, "show"), opts.extra);
  }

  /**
   * If raw is `show ?` (or sh ?), append IOS-style command list and return true.
   * @param {Function} appendFn - (className, text) => void
   */
  function tryAppendShowHelp(raw, appendFn, opts) {
    if (!isShowHelpQuery(raw)) return false;
    if (typeof appendFn === "function") {
      appendFn("line-sys line-show-help", showCommandHelpText(opts));
    }
    return true;
  }

  /** IOS-style `configure ?` / `config ?` at privileged EXEC (subcommands only). */

  function isConfigHelpQuery(raw) {
    var t = String(raw || "")
      .trim()
      .toLowerCase()
      .replace(/\s+/g, " ");
    return (
      t === "config ?" ||
      t === "configure ?" ||
      t === "conf ?" ||
      t === "configuration ?" ||
      t === "do config ?" ||
      t === "do configure ?" ||
      t === "do conf ?"
    );
  }

  /**
   * @param {{extra?:Array<{cmd:string,desc:string}>}} [opts]
   */
  function configCommandHelpText(opts) {
    opts = opts || {};
    var deviceType = opts.deviceType || "router";
    var extra = opts.configExtra || opts.extra || [];
    return formatHelpEntries(resolveHelpList(opts, deviceType, "configExec"), extra);
  }

  /**
   * If raw is `config ?` / `configure ?` / `conf ?`, append IOS-style list and return true.
   * @param {Function} appendFn - (className, text) => void
   */
  function tryAppendConfigHelp(raw, appendFn, opts) {
    if (!isConfigHelpQuery(raw)) return false;
    if (typeof appendFn === "function") {
      appendFn("line-sys line-show-help", configCommandHelpText(opts));
    }
    return true;
  }

  /** Router global `ip ?` at host(config)# — subcommands after `ip`. */

  function isIpHelpQuery(raw) {
    var t = String(raw || "")
      .trim()
      .toLowerCase()
      .replace(/\s+/g, " ");
    return t === "ip ?" || t === "do ip ?";
  }

  /**
   * @param {{deviceType?:'router'|'switch', promptText?:string, ipExtra?:Array<{cmd:string}>}} [opts]
   */
  function ipCommandHelpText(opts) {
    opts = opts || {};
    return formatHelpEntries(resolveHelpList(opts, "router", "ip"), opts.ipExtra);
  }

  /**
   * `ip ?` at router (config)# only.
   * @param {Function} appendFn - (className, text) => void
   */
  function tryAppendIpHelp(raw, appendFn, opts) {
    if (!isIpHelpQuery(raw)) return false;
    opts = opts || {};
    if ((opts.deviceType || "router") !== "router") return false;
    if (parsePromptMode(opts.promptText) !== "config") return false;
    if (typeof appendFn === "function") {
      appendFn("line-sys line-show-help", ipCommandHelpText(opts));
    }
    return true;
  }

  /** Router `ip route ?` at host(config)#. */

  function isIpRouteHelpQuery(raw) {
    var t = String(raw || "")
      .trim()
      .toLowerCase()
      .replace(/\s+/g, " ");
    return t === "ip route ?" || t === "do ip route ?";
  }

  /**
   * @param {{ipRouteExtra?:Array<{cmd:string}>}} [opts]
   */
  function ipRouteCommandHelpText(opts) {
    opts = opts || {};
    return formatHelpEntries(resolveHelpList(opts, "router", "ipRoute"), opts.ipRouteExtra);
  }

  /**
   * `ip route ?` at router (config)# only.
   * @param {Function} appendFn - (className, text) => void
   */
  function tryAppendIpRouteHelp(raw, appendFn, opts) {
    if (!isIpRouteHelpQuery(raw)) return false;
    opts = opts || {};
    if ((opts.deviceType || "router") !== "router") return false;
    if (parsePromptMode(opts.promptText) !== "config") return false;
    if (typeof appendFn === "function") {
      appendFn("line-sys line-show-help", ipRouteCommandHelpText(opts));
    }
    return true;
  }

  /** Handle `show ?`, `config ?`, `ip ?`, `ip route ?`, and config-mode `?` in one call. */
  function tryAppendIosHelp(raw, appendFn, opts) {
    if (tryAppendShowHelp(raw, appendFn, opts)) return true;
    if (tryAppendConfigHelp(raw, appendFn, opts)) return true;
    if (tryAppendIpRouteHelp(raw, appendFn, opts)) return true;
    if (tryAppendIpHelp(raw, appendFn, opts)) return true;
    return tryAppendModeHelp(raw, appendFn, opts);
  }

  function isBareHelpQuery(raw) {
    var t = String(raw || "")
      .trim()
      .toLowerCase()
      .replace(/\s+/g, " ");
    return t === "?" || t === "help";
  }

  /** Derive IOS mode from prompt text, e.g. R1(config)# → config. */
  function parsePromptMode(promptText) {
    var m = /\(([^)]+)\)#$/.exec(String(promptText || ""));
    if (!m) return "exec";
    var tag = m[1];
    if (tag === "config") return "config";
    if (tag === "config-if" || tag.indexOf("config-if-range") === 0) return "config-if";
    if (tag === "config-router") return "config-router";
    if (tag.indexOf("config-std-nacl") === 0 || tag.indexOf("config-ext-nacl") === 0) return "config-acl";
    if (tag === "config-vlan") return "config-vlan";
    if (tag.indexOf("config-line") === 0) return "config-line";
    return "config";
  }

  function formatHelpEntries(base, extra) {
    var seen = {};
    var lines = [];

    function addEntry(entry) {
      if (!entry || !entry.cmd || seen[entry.cmd]) return;
      seen[entry.cmd] = true;
      lines.push("  " + entry.cmd);
    }

    (base || []).forEach(addEntry);
    (extra || []).forEach(addEntry);
    return lines.join("\n");
  }

  /**
   * @param {{deviceType?:'router'|'switch', mode?:string, promptText?:string, modeExtra?:Array<{cmd:string}>}} [opts]
   */
  function modeCommandHelpText(opts) {
    opts = opts || {};
    var mode = opts.mode || parsePromptMode(opts.promptText);
    var deviceType = opts.deviceType || "router";
    var key;

    if (mode === "config-if") key = "configIf";
    else if (mode === "config-line") key = "configLine";
    else if (mode === "config-router") key = "configRouter";
    else if (mode === "config-acl") key = "configAcl";
    else if (mode === "config") key = "configGlobal";
    else if (mode === "exec") key = "exec";
    else key = "configGlobal";

    return formatHelpEntries(resolveHelpList(opts, deviceType, key), opts.modeExtra);
  }

  /**
   * Bare `?` / `help` at privileged EXEC (#) or in a configuration submode.
   * @param {Function} appendFn - (className, text) => void
   */
  function tryAppendModeHelp(raw, appendFn, opts) {
    if (!isBareHelpQuery(raw)) return false;
    var text = modeCommandHelpText(opts);
    if (!text) return false;
    if (typeof appendFn === "function") {
      appendFn("line-sys line-show-help", text);
    }
    return true;
  }

  /** Per-device IOS explore nav; delegates to cli-ios-mode.js when loaded. */
  function createExploreNav(host) {
    var iosMode =
      typeof window !== "undefined" && window.cliIosMode ? window.cliIosMode : null;
    if (iosMode && typeof iosMode.createDeviceExplore === "function") {
      return iosMode.createDeviceExplore(host);
    }
    return {
      getMode: function () {
        return null;
      },
      reset: function () {},
      promptWith: function (labPrompt) {
        return labPrompt || host + "#";
      },
      trySubmit: function () {
        return false;
      },
    };
  }

  var api = {
    isModeNavigationCommand: isModeNavigationCommand,
    expandInterfaceEcho: expandInterfaceEcho,
    CLI_UNSUPPORTED_MSG: CLI_UNSUPPORTED_MSG,
    CLI_UNSUPPORTED_NUMERIC_HINT_MSG: CLI_UNSUPPORTED_NUMERIC_HINT_MSG,
    CLI_VERIFY_INSTRUCTIONS_MSG: CLI_VERIFY_INSTRUCTIONS_MSG,
    COPY_RUN_START_OK_MSG: COPY_RUN_START_OK_MSG,
    CCNA_TRAINING_PORTAL_HREF: CCNA_TRAINING_PORTAL_HREF,
    CCNA_LAB_CHAIN: CCNA_LAB_CHAIN,
    initCcnaLabTopChrome: initCcnaLabTopChrome,
    INVALID_INPUT_MSG: INVALID_INPUT_MSG,
    INVALID_INPUT_NUMERIC_HINT_MSG: INVALID_INPUT_NUMERIC_HINT_MSG,
    invalidInputMsgForNormalizedCmd: invalidInputMsgForNormalizedCmd,
    unsupportedCmdMsg: unsupportedCmdMsg,
    tryLabDirectInterfaceSwitch: tryLabDirectInterfaceSwitch,
    tryLabReenterSubmodeContext: tryLabReenterSubmodeContext,
    applyLabStepInterfaceNav: applyLabStepInterfaceNav,
    bindLocalHistory: bindLocalHistory,
    createExploreNav: createExploreNav,
    isShowHelpQuery: isShowHelpQuery,
    showCommandHelpText: showCommandHelpText,
    tryAppendShowHelp: tryAppendShowHelp,
    isConfigHelpQuery: isConfigHelpQuery,
    configCommandHelpText: configCommandHelpText,
    tryAppendConfigHelp: tryAppendConfigHelp,
    isIpHelpQuery: isIpHelpQuery,
    ipCommandHelpText: ipCommandHelpText,
    tryAppendIpHelp: tryAppendIpHelp,
    isIpRouteHelpQuery: isIpRouteHelpQuery,
    ipRouteCommandHelpText: ipRouteCommandHelpText,
    tryAppendIpRouteHelp: tryAppendIpRouteHelp,
    tryAppendIosHelp: tryAppendIosHelp,
    isBareHelpQuery: isBareHelpQuery,
    parsePromptMode: parsePromptMode,
    modeCommandHelpText: modeCommandHelpText,
    tryAppendModeHelp: tryAppendModeHelp,
    DEFAULT_ROUTER_CLI_HELP: DEFAULT_ROUTER_CLI_HELP,
    DEFAULT_SWITCH_CLI_HELP: DEFAULT_SWITCH_CLI_HELP,
    resolveHelpList: resolveHelpList,
    iosHelpOpts: iosHelpOpts,
    SHOW_HELP_ROUTER: SHOW_HELP_ROUTER,
    SHOW_HELP_SWITCH: SHOW_HELP_SWITCH,
    CONFIG_HELP_EXEC: CONFIG_HELP_EXEC,
    IP_HELP_CONFIG_ROUTER: IP_HELP_CONFIG_ROUTER,
    IP_ROUTE_HELP_CONFIG_ROUTER: IP_ROUTE_HELP_CONFIG_ROUTER,
    MODE_HELP_CONFIG_ROUTER: MODE_HELP_CONFIG_ROUTER,
    MODE_HELP_CONFIG_SWITCH: MODE_HELP_CONFIG_SWITCH,
    MODE_HELP_CONFIG_LINE: MODE_HELP_CONFIG_LINE,
    isCcnaLabEmbedPath: isCcnaLabEmbedPath,
    isExamSimEmbed: isExamSimEmbed,
    isBctCliBannerContext: isBctCliBannerContext,
    EXAM_SIM_CLI_BANNER_TEXT: EXAM_SIM_CLI_BANNER_TEXT,
    showExamSimCliBanner: showExamSimCliBanner,
    injectBctCliBannerLabStyles: injectBctCliBannerLabStyles,
    wireBctCliOpenBanner: wireBctCliOpenBanner,
    initBctCliBanner: initBctCliBanner,
  };

  window.cliLabContainer = api;

  if (typeof window.expandInterfaceEcho !== "function") {
    window.expandInterfaceEcho = expandInterfaceEcho;
  }
  if (typeof window.isModeNavigationCommand !== "function") {
    window.isModeNavigationCommand = isModeNavigationCommand;
  }
  if (typeof window.invalidInputMsgForNormalizedCmd !== "function") {
    window.invalidInputMsgForNormalizedCmd = invalidInputMsgForNormalizedCmd;
  }
  if (typeof window.unsupportedCmdMsg !== "function") {
    window.unsupportedCmdMsg = unsupportedCmdMsg;
  }
  if (typeof window.bindLocalHistory !== "function") {
    window.bindLocalHistory = bindLocalHistory;
  }
})();
