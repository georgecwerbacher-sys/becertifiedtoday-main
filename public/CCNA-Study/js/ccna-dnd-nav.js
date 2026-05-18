(function () {
  "use strict";

  var KEY = "ccnaDnd25";
  var BASE = "/CCNA-Study/CCNA_D_D/";
  var finishHref = "/CCNA-Study/CCNA_Training_Portal.html";

  function examSimEmbed() {
    try {
      return new URLSearchParams(location.search).get("examSim") === "1";
    } catch (e) {
      return false;
    }
  }

  function applyExamSimEmbedStyles() {
    if (document.head.querySelector("style[data-ccna-dnd-exam-sim]")) return;
    var s = document.createElement("style");
    s.setAttribute("data-ccna-dnd-exam-sim", "1");
    s.textContent =
      "nav.sim-nav{display:none!important}" +
      ".actions{display:none!important}" +
      ".ccna-objective-tag{display:none!important}" +
      "body.dragdrop-exercise{padding-bottom:16px!important;place-items:start}" +
      "body.dragdrop-exercise{padding-bottom:calc(16px + env(safe-area-inset-bottom,0px))!important}";
    document.head.appendChild(s);
  }

  function slugFromPath() {
    var m = location.pathname.match(/\/CCNA_D_D\/(.+)\.html$/i);
    return m ? decodeURIComponent(m[1]) : "";
  }

  function readSession() {
    try {
      var raw = sessionStorage.getItem(KEY);
      if (!raw) return null;
      var s = JSON.parse(raw);
      if (!s || s.v !== 1 || !Array.isArray(s.order) || !s.order.length) return null;
      return s;
    } catch (e) {
      return null;
    }
  }

  function hashIndex() {
    var h = location.hash || "";
    var m = /^#ccnaDd=(\d+)$/.exec(h);
    return m ? parseInt(m[1], 10) : 0;
  }

  function modeQuery(session) {
    var m = session.mode === "review" ? "review" : "random";
    return "?mode=" + m;
  }

  function urlForSlug(session, slug, idx) {
    return BASE + slug + ".html" + modeQuery(session) + "#ccnaDd=" + idx;
  }

  function run() {
    if (!document.body || !document.body.classList.contains("dragdrop-exercise")) return;
    if (examSimEmbed()) {
      applyExamSimEmbedStyles();
      return;
    }
    var slug = slugFromPath();
    if (!slug) return;
    var session = readSession();
    var nav = document.querySelector("nav.sim-nav");
    if (!nav || nav.dataset.ccnaDndNavBound === "1") return;
    if (!session) return;

    var order = session.order;
    var i = order.indexOf(slug);
    if (i < 0) return;

    nav.dataset.ccnaDndNavBound = "1";

    try {
      if (hashIndex() !== i) {
        history.replaceState(null, "", location.pathname + location.search + "#ccnaDd=" + i);
      }
    } catch (e) {}

    var prevA = document.createElement("a");
    prevA.className = "sim-nav-btn next-link";
    prevA.textContent = "Previous";

    var nextA = document.createElement("a");
    nextA.className = "sim-nav-btn next-link";
    nextA.textContent = "Next drag-and-drop";

    if (i > 0) {
      prevA.href = urlForSlug(session, order[i - 1], i - 1);
    } else {
      prevA.style.display = "none";
      prevA.removeAttribute("href");
    }

    if (i + 1 < order.length) {
      nextA.href = urlForSlug(session, order[i + 1], i + 1);
    } else {
      nextA.href = "#";
      nextA.textContent = "Finish session";
      nextA.addEventListener(
        "click",
        function (e) {
          e.preventDefault();
          try {
            sessionStorage.removeItem(KEY);
          } catch (x) {}
          window.location.href = finishHref;
        },
        { once: true }
      );
    }

    nav.insertBefore(nextA, nav.firstChild);
    nav.insertBefore(prevA, nav.firstChild);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();
