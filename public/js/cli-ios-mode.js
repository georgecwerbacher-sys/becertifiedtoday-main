/**
 * IOS-style config hierarchy for lab simulators: "exit" walks up one level
 * (e.g. config-ext-nacl → config → privileged) without advancing the lab step.
 * Use with a per-flow exitLevel counter; reset exitLevel to 0 on any non-exit
 * command or when the step index changes.
 */
(function (global) {
  const PARENT = {
    "config-ext-nacl": "config",
    "config-if": "config",
    "config-line": "config",
    "config-router": "config",
    "config-vrf": "config",
    "config-cmap": "config",
    "config-pmap": "config",
    "config-pmap-c": "config-pmap",
    "config-cp": "config",
    "config-ip-sla-echo": "config",
    "config-ip-sla-http": "config",
    "config-fe": "config",
    "config": "privileged",
    "privileged": null,
    "exec": null,
  };

  function effectiveMode(baseMode, exitLevel) {
    let m = baseMode == null ? "privileged" : baseMode;
    for (let i = 0; i < exitLevel; i++) {
      const next = PARENT[m];
      if (next == null) break;
      m = next;
    }
    return m;
  }

  function canExit(baseMode, exitLevel) {
    const eff = effectiveMode(baseMode, exitLevel);
    return PARENT[eff] != null;
  }

  function promptFromMode(host, mode) {
    const m = mode == null ? "privileged" : mode;
    if (m === "exec" || m === "privileged") return `${host}#`;
    if (m === "config") return `${host}(config)#`;
    if (m === "config-if") return `${host}(config-if)#`;
    if (m === "config-line") return `${host}(config-line)#`;
    if (m === "config-router") return `${host}(config-router)#`;
    if (m === "config-vrf") return `${host}(config-vrf)#`;
    if (m === "config-ext-nacl") return `${host}(config-ext-nacl)#`;
    if (m === "config-cmap") return `${host}(config-cmap)#`;
    if (m === "config-pmap") return `${host}(config-pmap)#`;
    if (m === "config-pmap-c") return `${host}(config-pmap-c)#`;
    if (m === "config-cp") return `${host}(config-cp)#`;
    if (m === "config-fe") return `${host}(config-flow-exporter)#`;
    if (m === "config-ip-sla-echo") return `${host}(config-ip-sla-echo)#`;
    if (m === "config-ip-sla-http") return `${host}(config-ip-sla-http)#`;
    return `${host}#`;
  }

  /** Prompt for steps[index].mode after applying exitLevel parent walks. */
  function promptForStep(host, steps, index, exitLevel) {
    if (!steps || index >= steps.length) return `${host}#`;
    const eff = effectiveMode(steps[index].mode, exitLevel || 0);
    return promptFromMode(host, eff);
  }

  function isConfigureTerminal(u) {
    return u === "conf t" || u === "configure terminal";
  }

  function isInterfaceCommand(u) {
    return /^interface\s+\S/.test(u) || /^int\s+\S/.test(u);
  }

  function isEndCommand(u) {
    return u === "end";
  }

  function isExitCommand(u) {
    return u === "exit";
  }

  /**
   * IOS-like explore navigation (conf t, interface, exit, end) without lab grading.
   * exploreMode: null | "config" | "config-if"
   */
  function applyExploreNav(exploreMode, normalizedCmd) {
    const u = String(normalizedCmd || "");
    if (isConfigureTerminal(u)) {
      return { handled: true, exploreMode: "config" };
    }
    if (isEndCommand(u)) {
      if (exploreMode === "config" || exploreMode === "config-if") {
        return { handled: true, exploreMode: null };
      }
      return { handled: false, exploreMode: exploreMode || null };
    }
    if (isInterfaceCommand(u)) {
      return { handled: true, exploreMode: "config-if" };
    }
    if (isExitCommand(u)) {
      if (exploreMode === "config-if") {
        return { handled: true, exploreMode: "config" };
      }
      if (exploreMode === "config") {
        return { handled: true, exploreMode: null };
      }
      return { handled: false, exploreMode: exploreMode || null };
    }
    return { handled: false, exploreMode: exploreMode || null };
  }

  function explorePrompt(host, exploreMode) {
    if (exploreMode === "config") return `${host}(config)#`;
    if (exploreMode === "config-if") return `${host}(config-if)#`;
    return null;
  }

  /** Default normalizer: trim, lowercase, collapse spaces. */
  function normalizeCmd(line) {
    return String(line || "")
      .trim()
      .toLowerCase()
      .replace(/\s+/g, " ");
  }

  /** Explore overlay wins over the lab step prompt when set. */
  function promptWithExplore(host, exploreMode, labPrompt) {
    return explorePrompt(host, exploreMode) || labPrompt || `${host}#`;
  }

  /**
   * Handle conf t / interface / exit / end without lab grading.
   * Returns true when the command was handled (echo + prompt update).
   */
  function tryExploreSubmit(opts) {
    const line = opts.line;
    const trimmed = String(line || "").trim();
    if (!trimmed) return false;
    const normalizeFn = opts.normalize || normalizeCmd;
    const u = normalizeFn(line);
    const getExplore = opts.getExploreMode || function () {
      return null;
    };
    const setExplore = opts.setExploreMode || function () {};
    const currentExplore = getExplore();
    const nav = applyExploreNav(currentExplore, u);
    if (!nav.handled) return false;
    if (typeof opts.matchesLabStep === "function" && opts.matchesLabStep(line)) {
      return false;
    }

    const host = opts.host || "Router";
    const getLabPrompt = opts.getLabPrompt || function () {
      return `${host}#`;
    };
    const prompt = explorePrompt(host, currentExplore) || getLabPrompt();
    const echoLine =
      typeof opts.expandEcho === "function" ? opts.expandEcho(line) : line;

    if (!opts.alreadyEchoed) {
      opts.appendLine(opts.scrollEl, "line-user", prompt + " " + echoLine);
      if (opts.cmdInput) opts.cmdInput.value = "";
    }
    setExplore(nav.exploreMode);
    if (opts.onExploreChange) opts.onExploreChange(nav.exploreMode);
    if (opts.onAccepted) opts.onAccepted(line);
    return true;
  }

  /** Per-device explore state + promptWith / trySubmit helpers for lab pages. */
  function createDeviceExplore(host) {
    let exploreMode = null;
    return {
      getMode: function () {
        return exploreMode;
      },
      reset: function () {
        exploreMode = null;
      },
      promptWith: function (labPrompt) {
        return promptWithExplore(host, exploreMode, labPrompt);
      },
      trySubmit: function (line, ctx) {
        return tryExploreSubmit({
          line: line,
          host: host,
          getExploreMode: function () {
            return exploreMode;
          },
          setExploreMode: function (m) {
            exploreMode = m;
          },
          getLabPrompt: ctx.getLabPrompt,
          scrollEl: ctx.scrollEl,
          appendLine: ctx.appendLine,
          cmdInput: ctx.cmdInput,
          normalize: ctx.normalize,
          expandEcho: ctx.expandEcho,
          onExploreChange: ctx.onExploreChange,
          onAccepted: ctx.onAccepted,
          matchesLabStep: ctx.matchesLabStep,
          alreadyEchoed: ctx.alreadyEchoed,
        });
      },
    };
  }

  global.cliIosMode = {
    PARENT,
    effectiveMode,
    canExit,
    promptFromMode,
    promptForStep,
    isConfigureTerminal,
    isInterfaceCommand,
    isEndCommand,
    isExitCommand,
    applyExploreNav,
    explorePrompt,
    normalizeCmd,
    promptWithExplore,
    tryExploreSubmit,
    createDeviceExplore,
  };
})(typeof window !== "undefined" ? window : globalThis);
