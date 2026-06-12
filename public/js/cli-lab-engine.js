/**
 * Shared IOS CLI session engine for CCNA / ENCOR lab simulators.
 * Depends on cli-lab-container.js and cli-ios-mode.js (load both first).
 *
 * Lab pages define steps + snapshots; this module handles prompts, explore
 * navigation, show commands, copy run start, boot banner, and grading flow.
 */
(function (global) {
  var container = global.cliLabContainer;
  var iosMode = global.cliIosMode;

  var MSG = {
    HELP_DISABLED: "help feature disabled for tester",
    SHOW_DISABLED: "% Unrecognized show command in this lab simulation",
    SHOW_VERSION_DEFAULT:
      "Cisco IOS Software, BeCertifiedToday Lab Simulator\n" +
      "Version 17.9.4a, RELEASE SOFTWARE\n" +
      "Technical Support: help feature disabled for tester\n" +
      "Copyright (c) BeCertifiedToday. All rights reserved.",
    COPY_OK:
      "Destination filename [startup-config]?\nBuilding configuration...\n[OK]",
    COPY_EXEC_ONLY:
      "% Error: Run copy running-configuration startup-configuration only from privileged EXEC (#), not from configuration mode.",
    COPY_STEPS_INCOMPLETE:
      "% Error: Finish the lab task sequence on this device before saving to startup-config.",
    VERIFY_HINT: container ? container.CLI_VERIFY_INSTRUCTIONS_MSG : "% Check lab Tasks for the required value.",
    UNSUPPORTED: container ? container.CLI_UNSUPPORTED_MSG : "% command not supported in this lab simulation",
  };

  function normalizeIosCmd(s) {
    var t = String(s || "")
      .trim()
      .toLowerCase()
      .replace(/\s+/g, " ")
      .replace(/[.;]+$/, "");
    if (t === "conf t" || t === "config t") t = "configure terminal";
    if (t === "sh run" || t === "show run" || t === "sh running-config") t = "show running-config";
    if (t === "do show run" || t === "do sh run") t = "do show running-config";
    if (t === "sh ver" || t === "show ver" || t === "sh version") t = "show version";
    if (t === "sh history" || t === "sh hist" || t === "show hist") t = "show history";
    if (t === "do sh history" || t === "do sh hist" || t === "do show hist") t = "do show history";
    if (t === "copy run start" || t === "copy run st") t = "copy running-configuration startup-configuration";
    if (t === "copy running-config startup-config") t = "copy running-configuration startup-configuration";
    if (t.indexOf("int ") === 0) t = "interface " + t.slice(4);
    if (/^interface e\d+\/\d+$/.test(t)) t = t.replace(/^interface e/, "interface ethernet");
    if (t === "no shut") t = "no shutdown";
    return t;
  }

  function matchShowRun(raw) {
    var u = normalizeIosCmd(raw);
    return u === "show running-config" || u === "do show running-config";
  }

  function matchShowVersion(raw) {
    return normalizeIosCmd(raw) === "show version";
  }

  function matchShowHistory(raw) {
    var u = normalizeIosCmd(raw);
    return u === "show history" || u === "do show history";
  }

  function matchCopyRunStart(raw) {
    return normalizeIosCmd(raw) === "copy running-configuration startup-configuration";
  }

  function isModeNavigationCommand(u) {
    return container
      ? container.isModeNavigationCommand(u)
      : u === "configure terminal" ||
          u === "end" ||
          u === "exit" ||
          u.indexOf("interface ") === 0;
  }

  function expandInterfaceEcho(raw) {
    return container ? container.expandInterfaceEcho(raw) : raw;
  }

  function unsupportedMsg(u) {
    if (container && typeof container.invalidInputMsgForNormalizedCmd === "function") {
      return container.invalidInputMsgForNormalizedCmd(u);
    }
    return MSG.UNSUPPORTED;
  }

  function promptForMode(host, mode) {
    if (iosMode && typeof iosMode.promptFromMode === "function") {
      return iosMode.promptFromMode(host, mode);
    }
    if (mode === "config") return host + "(config)#";
    if (mode === "config-if") return host + "(config-if)#";
    return host + "#";
  }

  function labPromptForStep(host, steps, stepIndex) {
    if (!steps || stepIndex >= steps.length) return promptForMode(host, "exec");
    return promptForMode(host, steps[stepIndex].mode || "exec");
  }

  function inPrivilegedExec(host, steps, stepIndex, exploreMode) {
    if (exploreMode === "config" || exploreMode === "config-if") return false;
    if (!steps || stepIndex >= steps.length) return true;
    var m = steps[stepIndex].mode || "exec";
    return m === "exec" || m === "privileged";
  }

  function appendLine(scrollEl, className, text) {
    if (!scrollEl) return;
    var div = document.createElement("div");
    div.className = className;
    div.textContent = text;
    scrollEl.appendChild(div);
    scrollEl.scrollTop = scrollEl.scrollHeight;
  }

  function appendBlock(scrollEl, className, text) {
    if (!scrollEl) return;
    var div = document.createElement("div");
    div.className = className;
    div.style.whiteSpace = "pre-wrap";
    div.textContent = text;
    scrollEl.appendChild(div);
    scrollEl.scrollTop = scrollEl.scrollHeight;
  }

  function contextualHelp(host, steps, stepIndex, exploreMode) {
    var effExplore = exploreMode;
    if (effExplore === "config") {
      return "configure commands:\n  exit  End current mode and return to privileged EXEC\n  end   Return to privileged EXEC\n  hostname  Set system hostname\n  interface  Select interface to configure";
    }
    if (effExplore === "config-if") {
      return "interface commands:\n  exit  Exit interface configuration mode\n  end   Return to privileged EXEC\n  shutdown / no shutdown\n  switchport / ip address (lab-specific)";
    }
    if (steps && stepIndex < steps.length && typeof steps[stepIndex].help === "string") {
      return steps[stepIndex].help;
    }
    return (
      "Exec commands:\n  configure terminal  Enter global configuration mode\n  show running-config  Display current configuration\n  show version  System hardware and software status\n  copy running-config startup-config  Save configuration"
    );
  }

  function isBctCliBannerContext() {
    if (container && typeof container.isBctCliBannerContext === "function") {
      return container.isBctCliBannerContext();
    }
    try {
      var params = new URLSearchParams(location.search);
      if (params.get("examSim") === "1") return true;
      var p = (location.pathname || "").toLowerCase();
      var onLab =
        p.indexOf("/ccna-study/ccna_labs/") !== -1 ||
        p.indexOf("/ccna_sim_exam/embed/lab/") !== -1;
      if (!onLab) return false;
      if (params.get("sample") === "1") return true;
      if (sessionStorage.getItem("ccnaHomeSample")) return true;
    } catch (_) {}
    return false;
  }

  function defaultLoginBanner(host) {
    if (isBctCliBannerContext()) {
      return container && container.EXAM_SIM_CLI_BANNER_TEXT
        ? container.EXAM_SIM_CLI_BANNER_TEXT
        : (
            "================================================================================\n" +
            "  Be Certified Today — BCT Lab Simulator v.1_2026\n" +
            "================================================================================\n" +
            "\n" +
            "Exam simulation environment. Help commands are disabled; only commands required\n" +
            "for this lab scenario are available. Use the Helper button to review the lab\n" +
            "outline and topology if needed.\n" +
            "================================================================================"
          );
    }
    return (
      "================================================================================\n" +
      "  Be Certified Today (BCT) IOS Lab Simulator — " +
      host +
      "\n" +
      "================================================================================\n" +
      "\n" +
      "This is a browser-based training simulator, not a live Cisco device.\n" +
      "Only commands required for this lab scenario are supported — designed\n" +
      "for realistic exam-style practice, not full IOS.\n" +
      "\n" +
      "Not affiliated with Cisco Systems, Inc.\n" +
      "\n" +
      "Copyright (c) Be Certified Today. All rights reserved.\n" +
      "================================================================================"
    );
  }

  function resolveLoginBanner(opts, host) {
    if (opts.bootBanner === false || opts.loginBanner === false) return null;
    if (typeof opts.bootBanner === "string" && opts.bootBanner) return opts.bootBanner;
    if (typeof opts.loginBanner === "string" && opts.loginBanner) return opts.loginBanner;
    return defaultLoginBanner(host);
  }

  /**
   * @param {object} opts
   * @param {string} opts.host - Hostname (R1, SW1, …)
   * @param {'router'|'switch'} [opts.deviceType]
   * @param {{scroll:HTMLElement,prompt:HTMLElement,cmdline:HTMLElement,terminal?:HTMLElement}} opts.elements
   * @param {Array<{mode:string,test:Function,help?:string,wrongShape?:Function,hint?:string}>} [opts.steps]
   * @param {string} [opts.showRunningConfig]
   * @param {string} [opts.showVersion]
   * @param {string|false} [opts.bootBanner] - default BCT login banner; false to omit; string to override
   * @param {string|false} [opts.loginBanner] - alias for bootBanner
   * @param {boolean} [opts.graded=true]
   * @param {Function} [opts.normalize=normalizeIosCmd]
   * @param {Function} [opts.onStepAdvance]
   * @param {Function} [opts.onAllStepsComplete]
   * @param {{enabled?:boolean,requireStepsComplete?:boolean,onSaved?:Function}} [opts.copyRunStart]
   * @param {Record<string,string>} [opts.showCommands] - extra show cmd -> output
   */
  function createIosDevice(opts) {
    var host = opts.host || "Router";
    var deviceType = opts.deviceType || "router";
    var el = opts.elements || {};
    var steps = opts.steps || [];
    var normalizeFn = opts.normalize || normalizeIosCmd;
    var graded = opts.graded !== false;
    var copyCfg = opts.copyRunStart || {};
    var showVersionText = opts.showVersion || MSG.SHOW_VERSION_DEFAULT;
    var loginBanner = resolveLoginBanner(opts, host);

    var stepIndex = 0;
    var nvramSaved = false;
    var exploreNav = container ? container.createExploreNav(host) : null;

    function labPrompt() {
      return labPromptForStep(host, steps, stepIndex);
    }

    function updatePrompt() {
      if (!el.prompt) return;
      var base = exploreNav ? exploreNav.promptWith(labPrompt()) : labPrompt();
      el.prompt.textContent = base;
    }

    function flashTerminal() {
      if (!el.terminal) return;
      el.terminal.classList.remove("terminal-flash");
      void el.terminal.offsetWidth;
      el.terminal.classList.add("terminal-flash");
    }

    function reset() {
      stepIndex = 0;
      nvramSaved = false;
      if (exploreNav) exploreNav.reset();
      if (el.scroll) el.scroll.innerHTML = "";
      if (el.cmdline) {
        el.cmdline.value = "";
        el.cmdline.disabled = false;
      }
      if (loginBanner) appendBlock(el.scroll, "line-boot", loginBanner);
      updatePrompt();
      flashTerminal();
    }

    function echoCommand(line, normalized) {
      var promptText = el.prompt ? el.prompt.textContent : host + "#";
      var hide = isModeNavigationCommand(normalized);
      var echoLine = expandInterfaceEcho(String(line || "").trim());
      if (!hide || normalized.indexOf("interface ") === 0) {
        appendLine(el.scroll, "line-user", promptText + " " + echoLine);
      }
    }

    function tryExplore(line) {
      if (!exploreNav) return false;
      return exploreNav.trySubmit(line, {
        getLabPrompt: labPrompt,
        scrollEl: el.scroll,
        appendLine: appendLine,
        cmdInput: el.cmdline,
        normalize: normalizeFn,
        expandEcho: expandInterfaceEcho,
        onExploreChange: updatePrompt,
        matchesLabStep: function (raw) {
          if (!graded || !steps.length || stepIndex >= steps.length) return false;
          try {
            return steps[stepIndex].test(raw, normalizeFn(raw));
          } catch (_) {
            return false;
          }
        },
      });
    }

    function handleShowCommands(line, normalized) {
      if (matchShowRun(line)) {
        if (opts.showRunningConfig) appendBlock(el.scroll, "line-showrun", opts.showRunningConfig);
        else appendLine(el.scroll, "line-sys", "% Configuration not available in this lab.");
        return true;
      }
      if (inPrivilegedExec(host, steps, stepIndex, exploreNav ? exploreNav.getMode() : null) && matchShowVersion(line)) {
        appendBlock(el.scroll, "line-sys", showVersionText);
        return true;
      }
      if (matchShowHistory(line)) {
        appendLine(el.scroll, "line-sys", "  (command history available via Arrow Up in this terminal)");
        return true;
      }
      if (opts.showCommands && normalized.indexOf("show ") === 0) {
        if (opts.showCommands[normalized]) {
          appendBlock(el.scroll, "line-sys", opts.showCommands[normalized]);
          return true;
        }
      }
      if (
        inPrivilegedExec(host, steps, stepIndex, exploreNav ? exploreNav.getMode() : null) &&
        (normalized.indexOf("show ") === 0 || normalized.indexOf("sh ") === 0)
      ) {
        appendLine(el.scroll, "line-bad", MSG.SHOW_DISABLED);
        return true;
      }
      return false;
    }

    function handleCopyRunStart() {
      if (copyCfg.enabled === false) return false;
      if (!inPrivilegedExec(host, steps, stepIndex, exploreNav ? exploreNav.getMode() : null)) {
        appendLine(el.scroll, "line-bad", MSG.COPY_EXEC_ONLY);
        return true;
      }
      if (copyCfg.requireStepsComplete !== false && graded && stepIndex < steps.length) {
        appendLine(el.scroll, "line-bad", MSG.COPY_STEPS_INCOMPLETE);
        return true;
      }
      appendBlock(el.scroll, "line-sys", MSG.COPY_OK);
      nvramSaved = true;
      if (typeof copyCfg.onSaved === "function") copyCfg.onSaved();
      return true;
    }

    function submit() {
      if (!el.cmdline || el.cmdline.disabled) return;
      var line = el.cmdline.value;
      var trimmed = String(line || "").trim();
      var normalized = normalizeFn(line);

      if (!trimmed) {
        el.cmdline.value = "";
        return;
      }

      if (normalized === "?") {
        echoCommand(line, normalized);
        el.cmdline.value = "";
        appendBlock(el.scroll, "line-sys", contextualHelp(host, steps, stepIndex, exploreNav ? exploreNav.getMode() : null));
        return;
      }

      if (matchShowRun(line)) {
        echoCommand(line, normalized);
        el.cmdline.value = "";
        handleShowCommands(line, normalized);
        return;
      }

      if (tryExplore(line)) return;

      echoCommand(line, normalized);
      el.cmdline.value = "";

      if (matchCopyRunStart(line)) {
        handleCopyRunStart();
        return;
      }

      if (handleShowCommands(line, normalized)) return;

      if (!graded) {
        appendLine(el.scroll, "line-bad", unsupportedMsg(normalized));
        return;
      }

      if (stepIndex >= steps.length) {
        appendLine(el.scroll, "line-bad", unsupportedMsg(normalized));
        return;
      }

      var step = steps[stepIndex];
      if (typeof step.wrongShape === "function" && step.wrongShape(normalized, line)) {
        appendLine(el.scroll, "line-bad", step.hint || MSG.VERIFY_HINT);
        return;
      }

      var passed = false;
      try {
        passed = step.test(line, normalized);
      } catch (_) {
        passed = false;
      }

      if (passed) {
        stepIndex += 1;
        if (typeof opts.onStepAdvance === "function") {
          opts.onStepAdvance(stepIndex - 1, stepIndex);
        }
        if (stepIndex >= steps.length) {
          updatePrompt();
          if (typeof opts.onAllStepsComplete === "function") opts.onAllStepsComplete();
        } else {
          updatePrompt();
        }
      } else {
        var errMsg = step.hint || unsupportedMsg(normalized);
        appendLine(el.scroll, "line-bad", errMsg);
      }
    }

    function bindEnter() {
      if (!el.cmdline) return;
      if (container && typeof container.bindLocalHistory === "function") {
        container.bindLocalHistory(el.cmdline);
      }
      el.cmdline.addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
          e.preventDefault();
          submit();
        }
      });
    }

    bindEnter();

    return {
      host: host,
      reset: reset,
      submit: submit,
      updatePrompt: updatePrompt,
      getStepIndex: function () {
        return stepIndex;
      },
      setStepIndex: function (n) {
        stepIndex = n;
        updatePrompt();
      },
      isNvramSaved: function () {
        return nvramSaved;
      },
      appendLine: function (cls, text) {
        appendLine(el.scroll, cls, text);
      },
      appendSyslog: function (text) {
        appendLine(el.scroll, "line-syslog", text);
      },
      disable: function () {
        if (el.cmdline) el.cmdline.disabled = true;
      },
      enable: function () {
        if (el.cmdline) el.cmdline.disabled = false;
      },
      focus: function () {
        if (el.cmdline && !el.cmdline.disabled) el.cmdline.focus();
      },
    };
  }

  /**
   * Lightweight PC / host prompt session (PC1>, Router> user mode stub, etc.)
   */
  function createPcSession(opts) {
    var host = opts.host || "PC1";
    var promptSuffix = opts.promptSuffix || ">";
    var el = opts.elements || {};
    var handlers = opts.handlers || {};

    function promptText() {
      return host + promptSuffix;
    }

    function updatePrompt() {
      if (el.prompt) {
        el.prompt.textContent = promptText();
        if (promptSuffix === ">") el.prompt.classList.add("pc-prompt");
      }
    }

    function reset() {
      if (el.scroll) el.scroll.innerHTML = "";
      if (el.cmdline) {
        el.cmdline.value = "";
        el.cmdline.disabled = false;
      }
      updatePrompt();
    }

    function submit() {
      if (!el.cmdline || el.cmdline.disabled) return;
      var line = el.cmdline.value;
      var trimmed = String(line || "").trim();
      var normalized = normalizeIosCmd(line);
      appendLine(el.scroll, "line-user", promptText() + " " + line);
      el.cmdline.value = "";
      if (!trimmed) return;

      if (typeof handlers[normalized] === "function") {
        handlers[normalized](line, normalized);
        return;
      }
      for (var key in handlers) {
        if (Object.prototype.hasOwnProperty.call(handlers, key) && key.indexOf("/") === 0) {
          var re = new RegExp(key.slice(1), "i");
          if (re.test(normalized)) {
            handlers[key](line, normalized);
            return;
          }
        }
      }
      appendLine(
        el.scroll,
        "line-bad",
        "'" +
          trimmed +
          "' is not recognized as an internal or external command,\noperable program or batch file."
      );
    }

    function bindEnter() {
      if (!el.cmdline) return;
      if (container && typeof container.bindLocalHistory === "function") {
        container.bindLocalHistory(el.cmdline);
      }
      el.cmdline.addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
          e.preventDefault();
          submit();
        }
      });
    }

    bindEnter();
    updatePrompt();

    return {
      reset: reset,
      submit: submit,
      appendLine: function (cls, text) {
        appendLine(el.scroll, cls, text);
      },
      focus: function () {
        if (el.cmdline && !el.cmdline.disabled) el.cmdline.focus();
      },
    };
  }

  /** Draggable CLI modal + z-index stacking (skip interactive controls). */
  function wireFloatingModal(dialogEl, overlayEl, onBump) {
    if (!dialogEl || !overlayEl) return;
    var header = dialogEl.querySelector(".cli-modal-header");
    dialogEl.addEventListener("pointerdown", function (e) {
      if (e.target.closest("button, input, textarea, select, label, a[href]")) return;
      if (typeof onBump === "function") onBump(overlayEl);
    });
    if (!header) return;
    var drag = null;
    header.addEventListener("pointerdown", function (e) {
      if (e.button !== 0) return;
      if (e.target.closest(".cli-modal-close")) return;
      var r = dialogEl.getBoundingClientRect();
      dialogEl.style.left = r.left + "px";
      dialogEl.style.top = r.top + "px";
      dialogEl.style.transform = "none";
      dialogEl.classList.add("is-dragging");
      drag = { id: e.pointerId, sx: e.clientX, sy: e.clientY, ox: r.left, oy: r.top };
      try {
        header.setPointerCapture(e.pointerId);
      } catch (_) {}
      e.preventDefault();
    });
    header.addEventListener("pointermove", function (e) {
      if (!drag || e.pointerId !== drag.id) return;
      dialogEl.style.left = drag.ox + (e.clientX - drag.sx) + "px";
      dialogEl.style.top = drag.oy + (e.clientY - drag.sy) + "px";
    });
    function endDrag(e) {
      if (!drag || e.pointerId !== drag.id) return;
      drag = null;
      dialogEl.classList.remove("is-dragging");
      try {
        header.releasePointerCapture(e.pointerId);
      } catch (_) {}
    }
    header.addEventListener("pointerup", endDrag);
    header.addEventListener("pointercancel", endDrag);
  }

  function openModal(overlayEl, dialogEl, onBump) {
    if (!overlayEl) return;
    overlayEl.classList.add("is-open");
    overlayEl.setAttribute("aria-hidden", "false");
    if (typeof onBump === "function") onBump(overlayEl);
    if (dialogEl) dialogEl.focus();
  }

  function closeModal(overlayEl) {
    if (!overlayEl) return;
    overlayEl.classList.remove("is-open");
    overlayEl.setAttribute("aria-hidden", "true");
  }

  global.cliLabEngine = {
    MSG: MSG,
    normalizeIosCmd: normalizeIosCmd,
    matchShowRun: matchShowRun,
    matchShowVersion: matchShowVersion,
    matchShowHistory: matchShowHistory,
    matchCopyRunStart: matchCopyRunStart,
    promptForMode: promptForMode,
    labPromptForStep: labPromptForStep,
    defaultLoginBanner: defaultLoginBanner,
    appendLine: appendLine,
    appendBlock: appendBlock,
    createIosDevice: createIosDevice,
    createPcSession: createPcSession,
    wireFloatingModal: wireFloatingModal,
    openModal: openModal,
    closeModal: closeModal,
  };
})(typeof window !== "undefined" ? window : globalThis);
