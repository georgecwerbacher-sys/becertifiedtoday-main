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
    ".terminal .line-boot{white-space:pre-wrap;word-break:break-word;color:#94a3b8;font-size:.82rem;line-height:1.45;margin-bottom:10px;padding:10px 12px;border-radius:6px;background:#0a0e14;border:1px solid #1e293b}";

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
