(function () {
  "use strict";

  var KEY = "secplusHomeSample";
  var MCQ_BASE = "/COMP_TIA_SEC+/SEC+_Questions/";
  var HASH_RE = /^#secplusHS=(\d+)$/;

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
    var path = normalizePath(location.pathname);
    for (var i = 0; i < session.order.length; i++) {
      if (itemMatchesPath(session.order[i], path)) return i;
    }
    var iHint = hashIndex();
    if (iHint >= 0 && iHint < session.order.length && itemMatchesPath(session.order[iHint], path)) {
      return iHint;
    }
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
      location.replace(itemHref(session.order[hint], hint));
      return -2;
    }
    location.replace(itemHref(session.order[0], 0));
    return -2;
  }

  function itemHref(item, index) {
    var hash = "#secplusHS=" + index;
    if (item.type === "sim") return item.path + hash;
    return MCQ_BASE + item.slug + ".html" + hash;
  }

  function ensureSimNav(session, index) {
    var path = normalizePath(location.pathname);
    if (path.indexOf("/sec+_sim_hot_spot/") === -1) return null;

    var nav = document.querySelector("nav.secplus-sample-sim-nav");
    if (!nav) {
      nav = document.createElement("nav");
      nav.className = "secplus-sample-sim-nav";
      nav.setAttribute("aria-label", "Sample navigation");
      nav.innerHTML =
        '<a class="secplus-sample-sim-nav__prev" href="#">Back</a>' +
        '<span class="secplus-sample-sim-nav__progress" aria-live="polite"></span>' +
        '<a class="secplus-sample-sim-nav__next" href="#">Next</a>';
      document.body.appendChild(nav);
    }

    var home = document.querySelector("a.home-link");
    if (home) {
      home.textContent = "Exit sample";
      home.href = session.finishHome || "/comptia-sec+-home.html";
      home.classList.add("secplus-sample-exit");
    }

    return {
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
        history.replaceState(null, "", location.pathname + location.search + "#secplusHS=" + index);
      } catch (e) {}
    }

    if (els.prevEl) {
      if (index > 0) {
        els.prevEl.href = itemHref(order[index - 1], index - 1);
        els.prevEl.textContent = "Back";
        els.prevEl.classList.remove("nav-link--disabled");
        els.prevEl.removeAttribute("aria-hidden");
      } else {
        els.prevEl.href = session.finishHome || "/comptia-sec+-home.html";
        els.prevEl.textContent = "Home";
      }
    }

    if (els.nextEl) {
      if (index + 1 < order.length) {
        els.nextEl.href = itemHref(order[index + 1], index + 1);
        els.nextEl.textContent = "Next";
        els.nextEl.classList.remove("nav-link--disabled");
        els.nextEl.removeAttribute("aria-hidden");
        els.onclick = null;
      } else {
        var finish = session.finishHome || "/comptia-sec+-home.html";
        els.nextEl.href = finish;
        els.nextEl.textContent = "Finish sample";
        els.nextEl.onclick = function (ev) {
          clearSampleSession();
        };
      }
    }

    var home = document.querySelector("a.nav-home");
    if (home) home.href = session.finishHome || "/comptia-sec+-home.html";
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

  function scheduleRuns() {
    run();
    setTimeout(run, 0);
    window.addEventListener("load", run);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", scheduleRuns);
  } else {
    scheduleRuns();
  }
})();
