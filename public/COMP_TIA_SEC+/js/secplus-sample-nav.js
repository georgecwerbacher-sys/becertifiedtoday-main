(function () {
  "use strict";

  var KEY = "secplusHomeSample";
  var MCQ_BASE = "/COMP_TIA_SEC+/SEC+_Questions/";
  var HASH_RE = /^#secplusHS=(\d+)$/;
  var FINISH_HOME = "/comptia-sec+-home.html";
  var FREE_SIM_RUNNER = "/COMP_TIA_SEC+/test-simulation-runner.html?free=1";
  var LEAD_CAPTURE_FALLBACK = FREE_SIM_RUNNER;

  function readSession() {
    try {
      var raw = sessionStorage.getItem(KEY);
      if (!raw) return null;
      var s = JSON.parse(raw);
      if (!s || !Array.isArray(s.order) || !s.order.length) return null;
      return s;
    } catch (e) {
      return null;
    }
  }

  function isQuestionsOnlySample(session) {
    if (!session || !Array.isArray(session.order)) return false;
    for (var i = 0; i < session.order.length; i++) {
      if (session.order[i] && session.order[i].type !== "mcq") return false;
    }
    return session.order.length > 0;
  }

  function isSimOnlySample(session) {
    if (!session || !Array.isArray(session.order)) return false;
    for (var i = 0; i < session.order.length; i++) {
      if (session.order[i] && session.order[i].type !== "sim") return false;
    }
    return session.order.length > 0;
  }

  function isDarkWebSampleSim(session) {
    if (!isSimOnlySample(session) || !session.order.length) return false;
    var item = session.order[0];
    return !!(
      item &&
      item.type === "sim" &&
      normalizePath(item.path).indexOf("simulation-dark-web-account-protection") !== -1
    );
  }

  function usesMaskedNav(session) {
    return isQuestionsOnlySample(session) || isSimOnlySample(session);
  }

  function sampleMaskBase() {
    try {
      return sessionStorage.getItem("secplusUrlMaskPath") || "/secplus-sample";
    } catch (e) {
      return "/secplus-sample";
    }
  }

  function pathnameForMatch() {
    var path = normalizePath(location.pathname);
    if (path === "/secplus-sample" || path === "/secplus-sample/") {
      try {
        var remembered = sessionStorage.getItem("ccnaLastRealPath");
        if (remembered) return normalizePath(remembered);
      } catch (e) {}
    }
    return path;
  }

  function realItemHref(item, index) {
    var hash = "#secplusHS=" + index;
    if (item.type === "sim") return item.path + hash;
    return MCQ_BASE + item.slug + ".html" + hash;
  }

  function navItemHref(session, item, index) {
    if (usesMaskedNav(session)) {
      return sampleMaskBase() + "#secplusHS=" + index;
    }
    return realItemHref(item, index);
  }

  function wireNavLink(el, session, item, index) {
    if (!el || !item) return;
    if (usesMaskedNav(session)) {
      el.href = navItemHref(session, item, index);
      el.onclick = function (ev) {
        ev.preventDefault();
        location.assign(realItemHref(item, index));
      };
    } else {
      el.href = realItemHref(item, index);
      el.onclick = null;
    }
  }

  function hashIndex() {
    var m = HASH_RE.exec(location.hash || "");
    return m ? parseInt(m[1], 10) : 0;
  }

  function normalizePath(path) {
    try {
      return decodeURIComponent(path || "").toLowerCase();
    } catch (e) {
      return (path || "").toLowerCase();
    }
  }

  function itemMatchesPath(item, path) {
    if (item.type === "sim") return path === normalizePath(item.path);
    return !!(item.slug && path.endsWith("/" + item.slug.toLowerCase() + ".html"));
  }

  function currentItemIndex(session) {
    var path = pathnameForMatch();
    for (var i = 0; i < session.order.length; i++) {
      if (itemMatchesPath(session.order[i], path)) return i;
    }
    var iHint = hashIndex();
    if (iHint >= 0 && iHint < session.order.length && itemMatchesPath(session.order[iHint], path)) {
      return iHint;
    }
    if (iHint >= 0 && iHint < session.order.length) return iHint;
    return -1;
  }

  function clearSampleSession() {
    try {
      sessionStorage.removeItem(KEY);
      sessionStorage.removeItem("secplusUrlMaskPath");
      sessionStorage.removeItem("secplusSampleKind");
    } catch (e) {}
  }

  function sampleKindLabel() {
    try {
      var kind = sessionStorage.getItem("secplusSampleKind") || "";
      if (kind === "sim-dark-web" || kind === "sim-malware") return "simulation";
      if (kind === "questions") return "questions";
    } catch (e) {}
    return "sample";
  }

  function navigateAfterSample(url) {
    clearSampleSession();
    location.href = url;
  }

  function shouldOfferFreeSimUpsell(session) {
    return usesMaskedNav(session) && (isQuestionsOnlySample(session) || isSimOnlySample(session));
  }

  function loadSecplusFreeSimLauncher(callback) {
    if (typeof window.startSecplusFreeSimulation === "function") {
      callback();
      return;
    }
    var chain = [];
    if (typeof window.grantSecplusGuestFreeSimAccess !== "function") {
      chain.push(function (next) {
        var existing = document.querySelector('script[src="/COMP_TIA_SEC+/js/secplus-test-sim-storage.js"]');
        if (existing) {
          existing.addEventListener("load", next);
          existing.addEventListener("error", next);
          return;
        }
        var s = document.createElement("script");
        s.src = "/COMP_TIA_SEC+/js/secplus-test-sim-storage.js";
        s.onload = next;
        s.onerror = next;
        (document.body || document.head).appendChild(s);
      });
    }
    chain.push(function (next) {
      var existing = document.querySelector('script[src="/js/secplus-lead-capture.js"]');
      if (existing) {
        existing.addEventListener("load", next);
        existing.addEventListener("error", next);
        return;
      }
      var s = document.createElement("script");
      s.src = "/js/secplus-lead-capture.js";
      s.onload = next;
      s.onerror = next;
      (document.body || document.head).appendChild(s);
    });
    var i = 0;
    function step() {
      if (i >= chain.length) {
        callback();
        return;
      }
      chain[i++](step);
    }
    step();
  }

  function openFreeSimLeadModal(finishHome) {
    logSecplusSampleEvent("free_sim_start_click");
    loadSecplusFreeSimLauncher(function () {
      if (typeof window.startSecplusFreeSimulation === "function") {
        window.startSecplusFreeSimulation({
          finishHome: finishHome || FINISH_HOME,
          method: "secplus_free_sim_sample_popup",
          onBeforeNavigate: clearSampleSession,
          onConsumed: function () {
            navigateAfterSample((finishHome || FINISH_HOME) + "#purchase");
          },
        });
        return;
      }
      navigateAfterSample(FREE_SIM_RUNNER);
    });
  }

  function logSecplusSampleEvent(event, extra) {
    if (typeof window.bccLogSampleLeadEvent !== "function") return;
    var payload = {
      event: event,
      product: "secplus",
      sampleKind: sampleKindLabel(),
      source: "secplusHomeSample",
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

  function showFreeSimUpsellModal(finishHome) {
    if (document.getElementById("secplusSampleFreeSimUpsell")) return;

    ensureSampleLeadAnalytics();
    logSecplusSampleEvent("sample_finished");

    var session = readSession();
    var kind = sampleKindLabel();
    var lead;
    if (kind === "simulation" && isDarkWebSampleSim(session)) {
      lead =
        "You finished the <strong>BeCertifiedToday.com</strong> dark web IR preview (case IR-2024-0847)—the same simulation in the paid library. " +
        "Unlock the full <strong>35-minute timed exam</strong>: 20 multiple-choice questions plus this PBQ-style item, with Back, mark-for-review, and a domain scorecard.";
    } else if (kind === "simulation") {
      lead =
        "You finished the performance-based preview. Unlock the full <strong>35-minute timed simulation</strong>—20 multiple-choice questions plus a PBQ-style item, with Back and mark-for-review and a domain scorecard when you finish.";
    } else {
      lead =
        "You finished the sample questions. Try the free <strong>35-minute timed simulation</strong> next—20 multiple-choice questions plus a PBQ-style item, with Back and mark-for-review and a domain scorecard when you finish.";
    }

    var root = document.createElement("div");
    root.id = "secplusSampleFreeSimUpsell";
    root.className = "secplus-sample-upsell-root";
    root.setAttribute("role", "presentation");
    root.innerHTML =
      '<div class="secplus-sample-upsell-backdrop" data-secplus-upsell-dismiss tabindex="-1"></div>' +
      '<div class="secplus-sample-upsell-panel" role="dialog" aria-modal="true" aria-labelledby="secplusSampleFreeSimUpsellTitle" tabindex="-1">' +
      '<button type="button" class="secplus-sample-upsell-close" data-secplus-upsell-dismiss aria-label="Close dialog">×</button>' +
      '<p class="secplus-sample-upsell-eyebrow">Free SY0-701 timed simulation</p>' +
      '<h2 id="secplusSampleFreeSimUpsellTitle">Ready for a full timed dry run?</h2>' +
      '<p class="secplus-sample-upsell-lead">' +
      lead +
      "</p>" +
      '<div class="secplus-sample-upsell-actions">' +
      '<button type="button" class="secplus-sample-upsell-primary">Start free timed simulation</button>' +
      '<button type="button" class="secplus-sample-upsell-secondary" data-secplus-upsell-home>Return to Security+ home</button>' +
      "</div>" +
      "</div>";

    document.body.appendChild(root);
    document.body.classList.add("secplus-sample-upsell-open");

    var panel = root.querySelector(".secplus-sample-upsell-panel");
    var prevOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    function closeModal() {
      root.remove();
      document.body.classList.remove("secplus-sample-upsell-open");
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

    root.querySelectorAll("[data-secplus-upsell-dismiss]").forEach(function (el) {
      el.addEventListener("click", closeModal);
    });

    root.querySelector("[data-secplus-upsell-home]").addEventListener("click", function () {
      navigateAfterSample(finishHome || FINISH_HOME);
    });

    root.querySelector(".secplus-sample-upsell-primary").addEventListener("click", function () {
      closeModal();
      openFreeSimLeadModal(finishHome);
    });

    if (panel) panel.focus();
  }

  function completeSample(session, finishHome) {
    if (shouldOfferFreeSimUpsell(session)) {
      showFreeSimUpsellModal(finishHome);
      return;
    }
    navigateAfterSample(finishHome || FINISH_HOME);
  }

  function reconcileLocation(session) {
    var index = currentItemIndex(session);
    if (index >= 0) return index;
    var hint = hashIndex();
    if (hint >= 0 && hint < session.order.length) {
      location.replace(realItemHref(session.order[hint], hint));
      return -2;
    }
    location.replace(realItemHref(session.order[0], 0));
    return -2;
  }

  function itemHref(item, index) {
    return realItemHref(item, index);
  }

  function ensureSimNav(session, index) {
    var item = session.order[index];
    if (!item || item.type !== "sim") return null;

    var nav = document.querySelector("nav.secplus-sample-sim-nav");
    if (!nav) {
      nav = document.createElement("nav");
      nav.className = "secplus-sample-sim-nav";
      nav.setAttribute("aria-label", "Sample navigation");
      var backLink = isDarkWebSampleSim(session)
        ? ""
        : '<a class="secplus-sample-sim-nav__prev" href="#">Back</a>';
      nav.innerHTML =
        '<a class="secplus-sample-sim-nav__home" href="#">Home</a>' +
        backLink +
        '<span class="secplus-sample-sim-nav__progress" aria-live="polite"></span>' +
        '<a class="secplus-sample-sim-nav__next" href="#">Next</a>';
      document.body.appendChild(nav);
    } else if (isDarkWebSampleSim(session)) {
      var staleBack = nav.querySelector(".secplus-sample-sim-nav__prev");
      if (staleBack) staleBack.remove();
    }

    var finishHome = session.finishHome || FINISH_HOME;
    var homeExit = document.querySelector("a.home-link");
    if (homeExit) {
      if (usesMaskedNav(session)) {
        homeExit.setAttribute("hidden", "");
        homeExit.style.display = "none";
      } else {
        homeExit.removeAttribute("hidden");
        homeExit.style.display = "";
        homeExit.textContent = "Exit sample";
        homeExit.href = finishHome;
        homeExit.classList.add("secplus-sample-exit");
        homeExit.onclick = function () {
          clearSampleSession();
        };
      }
    }

    var deepDiveBtn = document.getElementById("deepDiveBtn");
    if (deepDiveBtn) {
      deepDiveBtn.hidden = false;
      deepDiveBtn.style.display = "";
    }
    if (usesMaskedNav(session)) {
      document.body.classList.add("secplus-home-sample-sim");
    }

    var homeBar = nav.querySelector(".secplus-sample-sim-nav__home");
    if (homeBar) {
      homeBar.href = finishHome;
      homeBar.onclick = function () {
        clearSampleSession();
      };
    }

    return {
      homeEl: homeBar,
      prevEl: nav.querySelector(".secplus-sample-sim-nav__prev"),
      nextEl: nav.querySelector(".secplus-sample-sim-nav__next"),
      progressEl: nav.querySelector(".secplus-sample-sim-nav__progress"),
    };
  }

  function findMcqNav() {
    return {
      prevEl: document.querySelector("a.nav-prev"),
      nextEl: document.querySelector("a.nav-next"),
      progressEl: document.querySelector(".secplus-sample-progress"),
    };
  }

  function ensureMcqProgress(host) {
    if (!host || host.querySelector(".secplus-sample-progress")) return host.querySelector(".secplus-sample-progress");
    var el = document.createElement("span");
    el.className = "secplus-sample-progress";
    el.setAttribute("aria-live", "polite");
    var links = host.querySelector(".question-nav-links");
    if (links) links.insertBefore(el, links.querySelector("a.nav-next"));
    return el;
  }

  function applyNav(session, index) {
    var order = session.order;
    var isSim = order[index] && order[index].type === "sim";
    var els = isSim ? ensureSimNav(session, index) : findMcqNav();

    if (!els) return;

    if (!isSim) {
      var navHost = document.querySelector("nav.question-nav");
      ensureMcqProgress(navHost);
      els.progressEl = document.querySelector(".secplus-sample-progress");
    }

    if (els.progressEl) {
      var item = order[index];
      if (item && item.type === "sim") {
        if (isDarkWebSampleSim(session)) {
          els.progressEl.textContent = "BeCertifiedToday.com IR · guest sample";
        } else {
          els.progressEl.textContent = "Simulation — item " + (index + 1) + " of " + order.length;
        }
      } else {
        var mcqNum = 0;
        for (var p = 0; p <= index; p++) {
          if (order[p] && order[p].type === "mcq") mcqNum++;
        }
        var mcqTotal = session.mcqCount;
        if (typeof mcqTotal !== "number") {
          mcqTotal = 0;
          for (var t = 0; t < order.length; t++) {
            if (order[t] && order[t].type === "mcq") mcqTotal++;
          }
        }
        els.progressEl.textContent = "Question " + mcqNum + " of " + mcqTotal;
      }
    }

    if (index !== hashIndex()) {
      try {
        var url =
          usesMaskedNav(session)
            ? sampleMaskBase() + "#secplusHS=" + index
            : location.pathname + location.search + "#secplusHS=" + index;
        history.replaceState(null, "", url);
      } catch (e) {}
    }

    var finishHome = session.finishHome || FINISH_HOME;
    var maskedNav = usesMaskedNav(session);

    if (els.prevEl && !isDarkWebSampleSim(session)) {
      if (index > 0) {
        wireNavLink(els.prevEl, session, order[index - 1], index - 1);
        els.prevEl.textContent = "Back";
        els.prevEl.classList.remove("nav-link--disabled");
        els.prevEl.removeAttribute("aria-hidden");
      } else if (maskedNav) {
        els.prevEl.href = "#";
        els.prevEl.textContent = "Back";
        els.prevEl.classList.add("nav-link--disabled");
        els.prevEl.setAttribute("aria-hidden", "true");
        els.prevEl.onclick = function (ev) {
          ev.preventDefault();
        };
      } else {
        els.prevEl.href = finishHome;
        els.prevEl.textContent = "Home";
        els.prevEl.onclick = function () {
          clearSampleSession();
        };
      }
    }

    if (els.nextEl) {
      if (index + 1 < order.length) {
        wireNavLink(els.nextEl, session, order[index + 1], index + 1);
        els.nextEl.textContent = "Next";
        els.nextEl.classList.remove("nav-link--disabled");
        els.nextEl.removeAttribute("aria-hidden");
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
        clearSampleSession();
      };
    }

    if (els.homeEl) {
      els.homeEl.href = finishHome;
      els.homeEl.onclick = function () {
        clearSampleSession();
      };
    }
  }

  function injectStyles() {
    if (document.head.querySelector("style[data-secplus-sample-nav]")) return;
    var s = document.createElement("style");
    s.setAttribute("data-secplus-sample-nav", "1");
    s.textContent =
      ".secplus-sample-progress{font-size:.8rem;font-weight:700;color:#9fb0cc;margin:0 8px;white-space:nowrap}" +
      ".secplus-sample-sim-nav{position:fixed;left:0;right:0;bottom:0;z-index:10001;display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:10px;padding:12px 16px calc(12px + env(safe-area-inset-bottom,0px));background:rgba(11,16,32,.94);border-top:1px solid #2d3b5a;backdrop-filter:blur(10px)}" +
      ".secplus-sample-sim-nav a{text-decoration:none;background:#5b21b6;border:1px solid #7c3aed;color:#f3e8ff;border-radius:10px;padding:10px 18px;font-weight:700;min-width:5.5rem;text-align:center;box-sizing:border-box}" +
      ".secplus-sample-sim-nav a:hover{filter:brightness(1.08)}" +
      ".secplus-sample-sim-nav__progress{font-size:.85rem;font-weight:700;color:#b8c3d6}" +
      "body:has(.secplus-sample-sim-nav){padding-bottom:calc(88px + env(safe-area-inset-bottom,0px))!important}" +
      "a.home-link.secplus-sample-exit{right:auto;left:14px}" +
      ".secplus-sample-upsell-root{position:fixed;inset:0;z-index:20002;display:flex;align-items:center;justify-content:center;padding:16px}" +
      ".secplus-sample-upsell-backdrop{position:absolute;inset:0;background:rgba(8,12,24,.72);backdrop-filter:blur(4px)}" +
      ".secplus-sample-upsell-panel{position:relative;z-index:1;width:min(520px,100%);max-height:min(90vh,640px);overflow:auto;margin:0;padding:clamp(20px,4vw,28px) clamp(18px,3.5vw,26px) 22px;border-radius:16px;border:1px solid #7c3aed;background:linear-gradient(165deg,rgba(22,32,52,.98) 0%,rgba(14,20,36,.99) 100%);color:#e6edf3;box-shadow:0 24px 64px rgba(0,0,0,.45)}" +
      ".secplus-sample-upsell-close{position:absolute;top:10px;right:12px;border:0;background:transparent;color:#9fb0cc;font-size:1.6rem;line-height:1;cursor:pointer;padding:4px 8px}" +
      ".secplus-sample-upsell-eyebrow{margin:0 0 8px;font-size:.78rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#c4b5fd}" +
      ".secplus-sample-upsell-panel h2{margin:0 0 12px;font-size:clamp(1.15rem,3vw,1.45rem);line-height:1.25;color:#fff}" +
      ".secplus-sample-upsell-lead{margin:0 0 18px;font-size:.95rem;line-height:1.55;color:#cbd5e1}" +
      ".secplus-sample-upsell-actions{display:flex;flex-direction:column;gap:10px}" +
      ".secplus-sample-upsell-primary{display:inline-flex;justify-content:center;align-items:center;text-decoration:none;background:#5b21b6;border:1px solid #7c3aed;color:#f3e8ff;border-radius:10px;padding:12px 18px;font:inherit;font-weight:800;text-align:center;cursor:pointer;width:100%;box-sizing:border-box}" +
      ".secplus-sample-upsell-primary:hover{filter:brightness(1.08)}" +
      ".secplus-sample-upsell-secondary{border:1px solid rgba(159,176,204,.45);background:transparent;color:#e6edf3;border-radius:10px;padding:11px 18px;font:inherit;font-weight:700;cursor:pointer}" +
      ".secplus-sample-upsell-secondary:hover{background:rgba(255,255,255,.06)}";
    document.head.appendChild(s);
  }

  function run() {
    var session = readSession();
    if (!session) return;
    injectStyles();
    var index = reconcileLocation(session);
    if (index < 0) return;
    applyNav(session, index);
  }

  function onHashChange() {
    var session = readSession();
    if (!session || !usesMaskedNav(session)) return;
    var hint = hashIndex();
    if (hint < 0 || hint >= session.order.length) return;
    var item = session.order[hint];
    if (!itemMatchesPath(item, pathnameForMatch())) {
      location.replace(realItemHref(item, hint));
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
