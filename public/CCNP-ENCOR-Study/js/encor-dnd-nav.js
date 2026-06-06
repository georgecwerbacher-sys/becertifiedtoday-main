(function () {
  "use strict";

  var QUEUE_KEY = "ccnpQuestionQueue";
  var LINEAR_SCOPE_KEY = "ccnpLinearScope";
  var REVIEW_MODE_KEY = "ccnpReviewMode";
  var REVIEW_QUEUE_KEY = "ccnpReviewQueue";
  var DND_BASE = "/CCNP-ENCOR-Study/CCNP-ENCOR-Drag-Drop/";
  var MCQ_BASE = "/CCNP-ENCOR-Study/ENCOR_Questions/";
  var finishHref = "/CCNP-ENCOR-Study/ENCOR_Training_Portal.html";
  var STUDY_CFG_URL = "/CCNP-ENCOR-Study/js/study-config.json";

  var cfgPromise = null;

  function loadCfg() {
    if (window.__ccnpStudyConfig) {
      return Promise.resolve(window.__ccnpStudyConfig);
    }
    if (!cfgPromise) {
      cfgPromise = fetch(STUDY_CFG_URL, { cache: "no-store" })
        .then(function (r) {
          return r.ok ? r.json() : {};
        })
        .catch(function () {
          return {};
        })
        .then(function (cfg) {
          window.__ccnpStudyConfig = cfg;
          return cfg;
        });
    }
    return cfgPromise;
  }

  function isDragDropId(id, cfg) {
    var n = Number(id);
    if ((cfg.dragDropIds || []).indexOf(n) >= 0) return true;
    if ((cfg.dragDropJsonIds || []).indexOf(n) >= 0) return true;
    return false;
  }

  function questionHref(id, cfg) {
    var dnd = isDragDropId(id, cfg);
    var base = dnd
      ? cfg.dragDropDirectory
        ? "/" + cfg.dragDropDirectory + "/question-"
        : DND_BASE + "question-"
      : cfg.sourceDirectory
        ? "/" + cfg.sourceDirectory + "/question-"
        : MCQ_BASE + "question-";
    return base + id + ".html";
  }

  function examSimEmbed() {
    try {
      if (sessionStorage.getItem("ccnpTestSimQueue")) return true;
      if (sessionStorage.getItem("ccnpExamSim") === "1") return true;
      return new URLSearchParams(location.search).get("examSim") === "1";
    } catch (e) {
      return false;
    }
  }

  function applyExamSimEmbedStyles() {
    if (document.head.querySelector("style[data-encor-dnd-exam-sim]")) return;
    var s = document.createElement("style");
    s.setAttribute("data-encor-dnd-exam-sim", "1");
    s.textContent =
      "nav.sim-nav{display:none!important}" +
      ".actions{display:none!important}" +
      ".ccna-objective-tag{display:none!important}" +
      "body.dragdrop-exercise{padding-bottom:16px!important;place-items:start}" +
      "body.dragdrop-exercise{padding-bottom:calc(16px + env(safe-area-inset-bottom,0px))!important}";
    document.head.appendChild(s);
  }

  function questionIdFromPath() {
    var m = location.pathname.match(/\/question-(\d+)\.html$/i);
    return m ? parseInt(m[1], 10) : null;
  }

  function readOrder() {
    try {
      if (sessionStorage.getItem(REVIEW_MODE_KEY) === "1") {
        var rq = JSON.parse(sessionStorage.getItem(REVIEW_QUEUE_KEY) || "null");
        if (Array.isArray(rq) && rq.length) return rq;
      }
      var raw = sessionStorage.getItem(QUEUE_KEY);
      if (raw) {
        var q = JSON.parse(raw);
        if (Array.isArray(q) && q.length) return q;
      }
      var ls = JSON.parse(sessionStorage.getItem(LINEAR_SCOPE_KEY) || "null");
      if (ls && Array.isArray(ls.ids) && ls.ids.length) return ls.ids;
    } catch (e) {}
    return null;
  }

  function hashIndex() {
    var m = /^#encorDd=(\d+)$/.exec(location.hash || "");
    return m ? parseInt(m[1], 10) : 0;
  }

  function clearSessionKeys() {
    try {
      sessionStorage.removeItem(QUEUE_KEY);
      sessionStorage.removeItem("ccnpQuestionQueueIndex");
      sessionStorage.removeItem(LINEAR_SCOPE_KEY);
      sessionStorage.removeItem(REVIEW_MODE_KEY);
      sessionStorage.removeItem(REVIEW_QUEUE_KEY);
    } catch (e) {}
  }

  function wireNav(order, qid, cfg) {
    var nav = document.querySelector("nav.sim-nav");
    if (!nav || nav.dataset.encorDndNavBound === "1") return;

    var i = order.indexOf(qid);
    if (i < 0) return;

    nav.dataset.encorDndNavBound = "1";

    try {
      if (hashIndex() !== i) {
        history.replaceState(null, "", location.pathname + location.search + "#encorDd=" + i);
      }
    } catch (e) {}

    var prevA = document.createElement("a");
    prevA.className = "sim-nav-btn next-link";
    prevA.textContent = "Previous";

    var nextA = document.createElement("a");
    nextA.className = "sim-nav-btn next-link";
    nextA.textContent = "Next drag-and-drop";

    if (i > 0) {
      prevA.href = questionHref(order[i - 1], cfg) + "#encorDd=" + (i - 1);
    } else {
      prevA.style.display = "none";
      prevA.removeAttribute("href");
    }

    if (i + 1 < order.length) {
      nextA.href = questionHref(order[i + 1], cfg) + "#encorDd=" + (i + 1);
    } else {
      nextA.href = "#";
      nextA.textContent = "Finish session";
      nextA.addEventListener(
        "click",
        function (e) {
          e.preventDefault();
          clearSessionKeys();
          window.location.href = finishHref;
        },
        { once: true }
      );
    }

    nav.insertBefore(nextA, nav.firstChild);
    nav.insertBefore(prevA, nav.firstChild);
  }

  function run() {
    if (!document.body || !document.body.classList.contains("dragdrop-exercise")) return;
    if (!document.body.classList.contains("encor-dnd-ui")) return;
    if (examSimEmbed()) {
      applyExamSimEmbedStyles();
      return;
    }

    var qid = questionIdFromPath();
    if (!qid) return;

    var order = readOrder();
    if (!order) return;

    loadCfg().then(function (cfg) {
      wireNav(order, qid, cfg || {});
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();
