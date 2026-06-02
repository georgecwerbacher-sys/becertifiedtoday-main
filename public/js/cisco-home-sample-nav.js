(function () {
  "use strict";

  var SESSIONS = {
    ccna: {
      key: "ccnaHomeSample",
      hashRe: /^#ccnaHS=(\d+)$/,
      hashPrefix: "ccnaHS=",
      maskPath: "/sample",
      storageScript: "/js/ccna-free-assessment-storage.js",
      leadScript: "/js/ccna-lead-capture.js",
      showLeadModal: function () {
        return window.showCcnaFreeSimLeadModal;
      },
      productLabel: "CCNA",
      examLabel: "200-301",
    },
    encor: {
      key: "encorHomeSample",
      hashRe: /^#encorHS=(\d+)$/,
      hashPrefix: "encorHS=",
      maskPath: "/sample",
      storageScript: "/CCNP-ENCOR-Study/js/encor-test-sim-storage.js",
      leadScript: "/js/encor-lead-capture.js",
      showLeadModal: function () {
        return window.showEncorFreeSimLeadModal;
      },
      productLabel: "ENCOR",
      examLabel: "350-401",
    },
  };

  function readSession(cfg) {
    try {
      var raw = sessionStorage.getItem(cfg.key);
      if (!raw) return null;
      var s = JSON.parse(raw);
      if (!s || !Array.isArray(s.order) || !s.order.length) return null;
      s._cfg = cfg;
      return s;
    } catch (e) {
      return null;
    }
  }

  function sampleKindHint() {
    try {
      return sessionStorage.getItem("ccnpSampleKind") || "";
    } catch (e) {
      return "";
    }
  }

  function isCcnaSamplePath(path) {
    return (
      path.indexOf("/ccna-study/") !== -1 || path.indexOf("/ccna_sim_exam/") !== -1
    );
  }

  function isEncorSamplePath(path) {
    return path.indexOf("/ccnp-encor-study/") !== -1;
  }

  function isEncorSampleKind(kind) {
    return kind.indexOf("encor") === 0 || kind === "labs" || kind === "drag";
  }

  function resolveLeadConfig(session) {
    if (!session) return SESSIONS.ccna;
    if (session.product === "encor") return SESSIONS.encor;
    if (session.product === "ccna") return SESSIONS.ccna;

    var path = pathnameForMatch();
    if (isCcnaSamplePath(path)) return SESSIONS.ccna;
    if (isEncorSamplePath(path)) return SESSIONS.encor;

    var kind = sampleKindHint();
    if (kind.indexOf("ccna") === 0) return SESSIONS.ccna;
    if (isEncorSampleKind(kind)) return SESSIONS.encor;

    if (session._cfg) return session._cfg;
    if (isEncorSamplePath(path)) return SESSIONS.encor;
    return SESSIONS.ccna;
  }

  function activeSessionConfig() {
    var ccna = readSession(SESSIONS.ccna);
    var encor = readSession(SESSIONS.encor);
    var path = pathnameForMatch();
    var kind = sampleKindHint();

    if (isCcnaSamplePath(path) && ccna) return ccna;
    if (isEncorSamplePath(path) && encor) return encor;

    if (kind.indexOf("ccna") === 0 && ccna) return ccna;
    if (isEncorSampleKind(kind) && encor) return encor;

    if (isEncorSamplePath(path)) return encor || ccna;
    if (isCcnaSamplePath(path)) return ccna || encor;

    if (ccna) return ccna;
    return encor;
  }

  function isSingleTrackSample(session) {
    if (!session || !Array.isArray(session.order)) return false;
    var t = session.order[0] && session.order[0].type;
    for (var i = 0; i < session.order.length; i++) {
      if (session.order[i] && session.order[i].type !== t) return false;
    }
    return session.order.length > 0;
  }

  function sampleMaskBase(session) {
    try {
      return sessionStorage.getItem("ccnpUrlMaskPath") || session._cfg.maskPath;
    } catch (e) {
      return session._cfg.maskPath;
    }
  }

  function pathnameForMatch() {
    var path = normalizePath(location.pathname);
    if (path === "/sample" || path === "/sample/") {
      try {
        var remembered = sessionStorage.getItem("ccnaLastRealPath");
        if (remembered) return normalizePath(remembered);
      } catch (e) {}
    }
    return path;
  }

  function normalizePath(path) {
    try {
      return decodeURIComponent(path || "").toLowerCase();
    } catch (e) {
      return (path || "").toLowerCase();
    }
  }

  function realItemHref(session, item, index) {
    var hash = "#" + session._cfg.hashPrefix + index;
    if (item.type === "mcq" && item.slug) {
      return "/CCNA-Study/CCNA_questions/" + item.slug + ".html?sample=1" + hash;
    }
    if (item.type === "mcq" && item.id != null) {
      return (
        "/CCNP-ENCOR-Study/ENCOR_Questions/question-" +
        item.id +
        ".html?sample=1" +
        hash
      );
    }
    return item.path + (item.path.indexOf("?") >= 0 ? "&" : "?") + "sample=1" + hash;
  }

  function itemMatchesPath(item, path) {
    if (item.type === "lab" || item.type === "dnd") {
      return path === normalizePath(item.path);
    }
    if (item.slug) return path.endsWith("/" + item.slug.toLowerCase() + ".html");
    if (item.id != null) return path.endsWith("/question-" + item.id + ".html");
    return false;
  }

  function hashIndex(session) {
    var m = session._cfg.hashRe.exec(location.hash || "");
    return m ? parseInt(m[1], 10) : 0;
  }

  function currentItemIndex(session) {
    var path = pathnameForMatch();
    for (var i = 0; i < session.order.length; i++) {
      if (itemMatchesPath(session.order[i], path)) return i;
    }
    var hint = hashIndex(session);
    if (hint >= 0 && hint < session.order.length) return hint;
    return -1;
  }

  function clearSampleSession(session) {
    try {
      sessionStorage.removeItem(session._cfg.key);
      sessionStorage.removeItem("ccnpUrlMaskPath");
      sessionStorage.removeItem("ccnpSampleKind");
    } catch (e) {}
  }

  function navigateAfterSample(url, session) {
    clearSampleSession(session);
    location.href = url;
  }

  function loadScriptOnce(src, onLoad, onError) {
    var existing = document.querySelector('script[src="' + src + '"]');
    if (existing) {
      if (existing.getAttribute("data-bcc-loaded") === "1") {
        onLoad();
        return;
      }
      existing.addEventListener("load", onLoad, { once: true });
      existing.addEventListener("error", onError, { once: true });
      return;
    }
    var s = document.createElement("script");
    s.src = src;
    s.onload = function () {
      s.setAttribute("data-bcc-loaded", "1");
      onLoad();
    };
    s.onerror = onError;
    (document.body || document.head).appendChild(s);
  }

  function loadLeadCapture(session, callback) {
    var cfg = resolveLeadConfig(session);

    function invoke() {
      callback(cfg);
    }

    var show = cfg.showLeadModal();
    if (typeof show === "function") {
      invoke();
      return;
    }

    function loadLeadScript() {
      loadScriptOnce(
        cfg.leadScript,
        invoke,
        function () {
          navigateAfterSample(
            (session.finishHome || "/") + (session.leadCaptureHash || ""),
            session
          );
        }
      );
    }

    if (cfg.storageScript) {
      loadScriptOnce(cfg.storageScript, loadLeadScript, loadLeadScript);
      return;
    }

    loadLeadScript();
  }

  function openFreeSimLeadModal(session, finishHome) {
    logSampleEvent(session, "email_modal_open");
    loadLeadCapture(session, function (cfg) {
      var show = cfg.showLeadModal();
      if (typeof show !== "function") {
        navigateAfterSample(
          finishHome + (session.leadCaptureHash || ""),
          session
        );
        return;
      }
      var kind =
        session.order[0] && session.order[0].type === "lab"
          ? "lab"
          : session.order[0] && session.order[0].type === "dnd"
            ? "dnd"
            : "questions";
      show({
        finishHome: finishHome,
        method: cfg.key + "_sample_popup",
        sampleKind: kind,
        onBeforeNavigate: function () {
          clearSampleSession(session);
        },
      });
    });
  }

  function logSampleEvent(session, event, extra) {
    if (typeof window.bccLogSampleLeadEvent !== "function" || !session) return;
    var product = session.product === "encor" ? "encor" : "ccna";
    var kind =
      session.order[0] && session.order[0].type === "lab"
        ? "lab"
        : session.order[0] && session.order[0].type === "dnd"
          ? "dnd"
          : "questions";
    var payload = {
      event: event,
      product: product,
      sampleKind: kind,
      source: (session._cfg && session._cfg.key) || "",
    };
    if (extra) {
      for (var k in extra) {
        if (Object.prototype.hasOwnProperty.call(extra, k)) payload[k] = extra[k];
      }
    }
    window.bccLogSampleLeadEvent(payload);
  }

  function ensureSampleLeadAnalytics() {
    if (typeof window.bccLogSampleLeadEvent === "function") return;
    if (document.querySelector('script[src="/js/sample-lead-analytics.js"]')) return;
    var s = document.createElement("script");
    s.src = "/js/sample-lead-analytics.js";
    s.async = true;
    (document.head || document.body).appendChild(s);
  }

  function showFreeSimUpsellModal(session, finishHome) {
    if (document.getElementById("ciscoSampleFreeSimUpsell")) return;

    ensureSampleLeadAnalytics();
    logSampleEvent(session, "sample_finished");

    var cfg = resolveLeadConfig(session);
    var kind =
      session.order[0] && session.order[0].type === "lab"
        ? "lab"
        : session.order[0] && session.order[0].type === "dnd"
          ? "drag-and-drop"
          : "questions";

    var lead =
      kind === "lab"
        ? "You finished the sample lab. Unlock the free <strong>45-minute timed simulation</strong>—20 multiple-choice questions, 2 drag-and-drop items, and 1 CLI lab, with a scorecard when you finish."
        : kind === "drag-and-drop"
          ? "You finished the sample drag-and-drop. Try the free <strong>45-minute timed simulation</strong> next—20 multiple-choice questions, 2 drag-and-drop items, and 1 CLI lab, with Back and Next navigation like test day."
          : "You finished the sample questions. Try the free <strong>45-minute timed simulation</strong> next—20 multiple-choice questions, 2 drag-and-drop items, and 1 CLI lab, with a scorecard when you finish.";

    var root = document.createElement("div");
    root.id = "ciscoSampleFreeSimUpsell";
    root.className = "cisco-sample-upsell-root";
    root.setAttribute("role", "presentation");
    root.innerHTML =
      '<div class="cisco-sample-upsell-backdrop" data-cisco-upsell-dismiss tabindex="-1"></div>' +
      '<div class="cisco-sample-upsell-panel" role="dialog" aria-modal="true" aria-labelledby="ciscoSampleFreeSimUpsellTitle" tabindex="-1">' +
      '<button type="button" class="cisco-sample-upsell-close" data-cisco-upsell-dismiss aria-label="Close dialog">×</button>' +
      '<p class="cisco-sample-upsell-eyebrow">Free ' +
      cfg.examLabel +
      " timed simulation</p>" +
      '<h2 id="ciscoSampleFreeSimUpsellTitle">Ready for a full timed dry run?</h2>' +
      '<p class="cisco-sample-upsell-lead">' +
      lead +
      "</p>" +
      '<div class="cisco-sample-upsell-actions">' +
      '<button type="button" class="cisco-sample-upsell-primary">Start free timed simulation</button>' +
      '<button type="button" class="cisco-sample-upsell-secondary" data-cisco-upsell-home>Return to ' +
      cfg.productLabel +
      " home</button>" +
      "</div>" +
      "</div>";

    document.body.appendChild(root);
    document.body.classList.add("cisco-sample-upsell-open");

    var panel = root.querySelector(".cisco-sample-upsell-panel");
    var prevOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    function closeModal() {
      root.remove();
      document.body.classList.remove("cisco-sample-upsell-open");
      document.body.style.overflow = prevOverflow;
      document.removeEventListener("keydown", onKey);
    }

    function onKey(ev) {
      if (ev.key === "Escape") {
        ev.preventDefault();
        closeModal();
      }
    }

    document.addEventListener("keydown", onKey);

    root.querySelectorAll("[data-cisco-upsell-dismiss]").forEach(function (el) {
      el.addEventListener("click", closeModal);
    });

    root.querySelector("[data-cisco-upsell-home]").addEventListener("click", function () {
      navigateAfterSample(finishHome || session.finishHome, session);
    });

    root.querySelector(".cisco-sample-upsell-primary").addEventListener("click", function () {
      closeModal();
      openFreeSimLeadModal(session, finishHome);
    });

    if (panel) panel.focus();
  }

  function completeSample(session, finishHome) {
    if (isSingleTrackSample(session)) {
      showFreeSimUpsellModal(session, finishHome);
      return;
    }
    navigateAfterSample(finishHome || session.finishHome, session);
  }

  function wireNavLink(el, session, item, index) {
    if (!el || !item) return;
    if (isSingleTrackSample(session)) {
      el.href = sampleMaskBase(session) + "#" + session._cfg.hashPrefix + index;
      el.onclick = function (ev) {
        ev.preventDefault();
        location.assign(realItemHref(session, item, index));
      };
    } else {
      el.href = realItemHref(session, item, index);
      el.onclick = null;
    }
  }

  function ensureBottomNav(session, index) {
    var nav = document.querySelector("nav.cisco-home-sample-nav");
    if (!nav) {
      nav = document.createElement("nav");
      nav.className = "cisco-home-sample-nav";
      nav.setAttribute("aria-label", "Sample navigation");
      nav.innerHTML =
        '<a class="cisco-home-sample-nav__home" href="#">Home</a>' +
        '<a class="cisco-home-sample-nav__prev" href="#">Back</a>' +
        '<span class="cisco-home-sample-nav__progress" aria-live="polite"></span>' +
        '<a class="cisco-home-sample-nav__next" href="#">Next</a>';
      document.body.appendChild(nav);
      document.body.classList.add("cisco-home-sample-active");
    }

    var finishHome = session.finishHome;
    var homeExit = document.querySelector("a.home-link");
    if (homeExit) {
      homeExit.setAttribute("hidden", "");
      homeExit.style.display = "none";
    }

    var topNav = document.querySelector("nav.question-nav");
    if (topNav) topNav.style.display = "none";

    return {
      homeEl: nav.querySelector(".cisco-home-sample-nav__home"),
      prevEl: nav.querySelector(".cisco-home-sample-nav__prev"),
      nextEl: nav.querySelector(".cisco-home-sample-nav__next"),
      progressEl: nav.querySelector(".cisco-home-sample-nav__progress"),
    };
  }

  function findMcqNav() {
    return {
      prevEl: document.querySelector("a.nav-prev"),
      nextEl: document.querySelector("a.nav-next"),
      progressEl: document.querySelector(".cisco-sample-progress"),
    };
  }

  function ensureMcqProgress(host) {
    if (!host || host.querySelector(".cisco-sample-progress")) {
      return host && host.querySelector(".cisco-sample-progress");
    }
    var el = document.createElement("span");
    el.className = "cisco-sample-progress";
    el.setAttribute("aria-live", "polite");
    var links = host.querySelector(".question-nav-links");
    if (links) links.insertBefore(el, links.querySelector("a.nav-next"));
    return el;
  }

  function applyNav(session, index) {
    var order = session.order;
    var isLabOrDnd = order[index] && (order[index].type === "lab" || order[index].type === "dnd");
    var els = isLabOrDnd ? ensureBottomNav(session, index) : findMcqNav();

    if (!els) return;

    if (!isLabOrDnd) {
      ensureMcqProgress(document.querySelector("nav.question-nav"));
      els.progressEl = document.querySelector(".cisco-sample-progress");
    }

    if (els.progressEl) {
      var item = order[index];
      if (item && (item.type === "lab" || item.type === "dnd")) {
        els.progressEl.textContent =
          (item.type === "lab" ? "Lab" : "Drag-and-drop") +
          " — item " +
          (index + 1) +
          " of " +
          order.length;
      } else {
        var mcqNum = 0;
        for (var p = 0; p <= index; p++) {
          if (order[p] && order[p].type === "mcq") mcqNum++;
        }
        els.progressEl.textContent = "Question " + mcqNum + " of " + session.mcqCount;
      }
    }

    if (index !== hashIndex(session)) {
      try {
        history.replaceState(
          null,
          "",
          sampleMaskBase(session) + "#" + session._cfg.hashPrefix + index
        );
      } catch (e) {}
    }

    var finishHome = session.finishHome;

    if (els.prevEl) {
      if (index > 0) {
        wireNavLink(els.prevEl, session, order[index - 1], index - 1);
        els.prevEl.textContent = "Back";
        els.prevEl.classList.remove("nav-link--disabled");
      } else {
        els.prevEl.href = "#";
        els.prevEl.textContent = "Back";
        els.prevEl.classList.add("nav-link--disabled");
        els.prevEl.onclick = function (ev) {
          ev.preventDefault();
        };
      }
    }

    if (els.nextEl) {
      if (index + 1 < order.length) {
        wireNavLink(els.nextEl, session, order[index + 1], index + 1);
        els.nextEl.textContent = "Next";
        els.nextEl.classList.remove("nav-link--disabled");
      } else {
        els.nextEl.href = finishHome;
        els.nextEl.textContent = "Finish sample";
        els.nextEl.onclick = function (ev) {
          ev.preventDefault();
          completeSample(session, finishHome);
        };
      }
    }

    var home = document.querySelector("a.nav-home");
    if (home) {
      home.href = finishHome;
      home.textContent = "Home";
      home.onclick = function () {
        clearSampleSession(session);
      };
    }

    if (els.homeEl) {
      els.homeEl.href = finishHome;
      els.homeEl.onclick = function () {
        clearSampleSession(session);
      };
    }
  }

  function reconcileLocation(session) {
    var index = currentItemIndex(session);
    if (index >= 0) return index;
    var hint = hashIndex(session);
    if (hint >= 0 && hint < session.order.length) {
      location.replace(realItemHref(session, session.order[hint], hint));
      return -2;
    }
    location.replace(realItemHref(session, session.order[0], 0));
    return -2;
  }

  function injectStyles() {
    if (document.head.querySelector("style[data-cisco-home-sample-nav]")) return;
    var s = document.createElement("style");
    s.setAttribute("data-cisco-home-sample-nav", "1");
    s.textContent =
      ".cisco-sample-progress{font-size:.8rem;font-weight:700;color:#9fb0cc;margin:0 8px;white-space:nowrap}" +
      ".cisco-home-sample-nav{position:fixed;left:0;right:0;bottom:0;z-index:10001;display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:10px;padding:12px 16px calc(12px + env(safe-area-inset-bottom,0px));background:rgba(11,16,32,.94);border-top:1px solid #2d3b5a;backdrop-filter:blur(10px)}" +
      ".cisco-home-sample-nav a{text-decoration:none;background:#2f66bf;border:1px solid #4f84d8;color:#f4f7ff;border-radius:10px;padding:10px 18px;font-weight:700;min-width:5.5rem;text-align:center;box-sizing:border-box}" +
      ".cisco-home-sample-nav a:hover{filter:brightness(1.08)}" +
      ".cisco-home-sample-nav a.nav-link--disabled{opacity:.45;pointer-events:none}" +
      ".cisco-home-sample-nav__progress{font-size:.85rem;font-weight:700;color:#b8c3d6}" +
      "body.cisco-home-sample-active{padding-bottom:calc(88px + env(safe-area-inset-bottom,0px))!important}" +
      ".cisco-sample-upsell-root{position:fixed;inset:0;z-index:20002;display:flex;align-items:center;justify-content:center;padding:16px}" +
      ".cisco-sample-upsell-backdrop{position:absolute;inset:0;background:rgba(8,12,24,.72);backdrop-filter:blur(4px)}" +
      ".cisco-sample-upsell-panel{position:relative;z-index:1;width:min(520px,100%);max-height:min(90vh,640px);overflow:auto;margin:0;padding:clamp(20px,4vw,28px) clamp(18px,3.5vw,26px) 22px;border-radius:16px;border:1px solid #4f84d8;background:linear-gradient(165deg,rgba(22,32,52,.98) 0%,rgba(14,20,36,.99) 100%);color:#e6edf3;box-shadow:0 24px 64px rgba(0,0,0,.45)}" +
      ".cisco-sample-upsell-close{position:absolute;top:10px;right:12px;border:0;background:transparent;color:#9fb0cc;font-size:1.6rem;line-height:1;cursor:pointer;padding:4px 8px}" +
      ".cisco-sample-upsell-eyebrow{margin:0 0 8px;font-size:.78rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#a8c4f0}" +
      ".cisco-sample-upsell-panel h2{margin:0 0 12px;font-size:clamp(1.15rem,3vw,1.45rem);line-height:1.25;color:#fff}" +
      ".cisco-sample-upsell-lead{margin:0 0 18px;font-size:.95rem;line-height:1.55;color:#cbd5e1}" +
      ".cisco-sample-upsell-actions{display:flex;flex-direction:column;gap:10px}" +
      ".cisco-sample-upsell-primary{display:inline-flex;justify-content:center;align-items:center;border:1px solid #4f84d8;background:#2f66bf;color:#f4f7ff;border-radius:10px;padding:12px 18px;font:inherit;font-weight:800;cursor:pointer;width:100%;box-sizing:border-box}" +
      ".cisco-sample-upsell-primary:hover{filter:brightness(1.08)}" +
      ".cisco-sample-upsell-secondary{border:1px solid rgba(159,176,204,.45);background:transparent;color:#e6edf3;border-radius:10px;padding:11px 18px;font:inherit;font-weight:700;cursor:pointer}" +
      ".cisco-sample-upsell-secondary:hover{background:rgba(255,255,255,.06)}";
    document.head.appendChild(s);
  }

  function run() {
    var session = activeSessionConfig();
    if (!session) return;
    injectStyles();
    var index = reconcileLocation(session);
    if (index < 0) return;
    applyNav(session, index);
  }

  function onHashChange() {
    var session = activeSessionConfig();
    if (!session || !isSingleTrackSample(session)) return;
    var hint = hashIndex(session);
    if (hint < 0 || hint >= session.order.length) return;
    if (!itemMatchesPath(session.order[hint], pathnameForMatch())) {
      location.replace(realItemHref(session, session.order[hint], hint));
    }
  }

  function scheduleRuns() {
    run();
    setTimeout(run, 0);
    window.addEventListener("load", run);
    window.addEventListener("hashchange", onHashChange);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", scheduleRuns);
  } else {
    scheduleRuns();
  }
})();
