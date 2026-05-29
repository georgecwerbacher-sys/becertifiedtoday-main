(function () {
  "use strict";

  var KEY = "secplusHomeSample";
  var MCQ_BASE = "/COMP_TIA_SEC+/SEC+_Questions/";
  var HASH_RE = /^#secplusHS=(\d+)$/;
  var FINISH_HOME = "/comptia-sec+-home.html";

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
    } catch (e) {}
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
        els.progressEl.textContent = "Simulation — item " + (index + 1) + " of " + order.length;
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
        els.nextEl.onclick = function () {
          clearSampleSession();
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
      "a.home-link.secplus-sample-exit{right:auto;left:14px}";
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
