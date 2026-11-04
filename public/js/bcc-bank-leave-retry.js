/**
 * Shared leave-bank prompt: if the learner missed questions in a portal bank
 * session, ask whether to retry those misses before exiting to Home/Finish.
 */
(function () {
  "use strict";

  if (window.__bccBankLeaveRetryBound) return;
  window.__bccBankLeaveRetryBound = true;

  var STYLE_ID = "bcc-bank-leave-retry-style";
  var MODAL_ID = "bccBankLeaveRetryModal";
  var MISSED_ENCOR_KEY = "ccnpBankMissedIds";

  function pathLower() {
    try {
      return (location.pathname || "").toLowerCase();
    } catch (e) {
      return "";
    }
  }

  function isSampleOrExam() {
    try {
      if (sessionStorage.getItem("ccnpTestSimQueue")) return true;
      if (sessionStorage.getItem("ccnpExamSim") === "1") return true;
      if (sessionStorage.getItem("secplusExamSim") === "1") return true;
      if (sessionStorage.getItem("ccnaHomeSample")) return true;
      if (sessionStorage.getItem("encorHomeSample")) return true;
      if (sessionStorage.getItem("secplusHomeSample")) return true;
      if (new URLSearchParams(location.search).get("sample") === "1") return true;
      if (new URLSearchParams(location.search).get("examSim") === "1") return true;
      if (sessionStorage.getItem("ccnpUrlMaskPath") === "/sample") return true;
    } catch (e) {}
    return false;
  }

  function readJson(key) {
    try {
      var raw = sessionStorage.getItem(key);
      if (!raw) return null;
      return JSON.parse(raw);
    } catch (e) {
      return null;
    }
  }

  function writeJson(key, value) {
    try {
      sessionStorage.setItem(key, JSON.stringify(value));
    } catch (e) {}
  }

  function uniquePush(list, id) {
    var s = String(id);
    if (!s) return list;
    if (list.indexOf(s) >= 0) return list;
    list.push(s);
    return list;
  }

  function currentSlug() {
    var m = (location.pathname || "").match(/\/([^/]+?)(?:\.html)?\/?$/i);
    return m ? decodeURIComponent(m[1]) : "";
  }

  function currentEncorId() {
    var m = (location.pathname || "").match(/question-(\d+)(?:\.html)?\/?$/i);
    return m ? m[1] : "";
  }

  function adapters() {
    return [
      {
        id: "ccna",
        key: "ccnaPractice100",
        base: "/CCNA-Study/CCNA_questions/",
        hash: "ccnaP",
        home: "/ccna-home.html",
        active: function () {
          var s = readJson("ccnaPractice100");
          return !!(s && Array.isArray(s.order) && s.order.length);
        },
        currentId: currentSlug,
        getMissed: function () {
          var s = readJson("ccnaPractice100");
          return s && Array.isArray(s.missed) ? s.missed.slice() : [];
        },
        trackMiss: function (id) {
          var s = readJson("ccnaPractice100");
          if (!s) return;
          s.missed = uniquePush(Array.isArray(s.missed) ? s.missed : [], id);
          writeJson("ccnaPractice100", s);
        },
        clearMissed: function () {
          var s = readJson("ccnaPractice100");
          if (!s) return;
          s.missed = [];
          writeJson("ccnaPractice100", s);
        },
        startRetry: function (missed) {
          var s = readJson("ccnaPractice100") || { v: 1 };
          s.v = 1;
          s.mode = "retry";
          s.order = missed.slice();
          s.missed = [];
          s.leaveRetry = true;
          writeJson("ccnaPractice100", s);
          location.href = this.base + missed[0] + ".html#" + this.hash + "=0";
        },
        clearSession: function () {
          try {
            sessionStorage.removeItem("ccnaPractice100");
          } catch (e) {}
        },
        exitHref: function () {
          return "/ccna-home.html";
        },
      },
      {
        id: "secplus",
        key: "secplusPractice",
        base: "/COMP_TIA_SEC+/SEC+_Questions/",
        hash: "secplusP",
        home: "/comptia-sec+-home.html",
        active: function () {
          var s = readJson("secplusPractice");
          return !!(s && Array.isArray(s.order) && s.order.length);
        },
        currentId: currentSlug,
        getMissed: function () {
          var s = readJson("secplusPractice");
          return s && Array.isArray(s.missed) ? s.missed.slice() : [];
        },
        trackMiss: function (id) {
          var s = readJson("secplusPractice");
          if (!s) return;
          s.missed = uniquePush(Array.isArray(s.missed) ? s.missed : [], id);
          writeJson("secplusPractice", s);
        },
        clearMissed: function () {
          var s = readJson("secplusPractice");
          if (!s) return;
          s.missed = [];
          writeJson("secplusPractice", s);
        },
        startRetry: function (missed) {
          var s = readJson("secplusPractice") || { v: 1 };
          s.v = 1;
          s.mode = "retry";
          s.order = missed.slice();
          s.missed = [];
          s.leaveRetry = true;
          writeJson("secplusPractice", s);
          location.href = this.base + missed[0] + ".html#" + this.hash + "=0";
        },
        clearSession: function () {
          try {
            sessionStorage.removeItem("secplusPractice");
          } catch (e) {}
        },
        exitHref: function () {
          return "/comptia-sec+-home.html";
        },
      },
      {
        id: "ccnaauto",
        key: "ccnaautoPractice",
        base: "/CCNAAUTO-Study/CCNAAUTO_Questions/",
        hash: "ccnaautoP",
        home: "/ccnaauto-home.html",
        active: function () {
          var s = readJson("ccnaautoPractice");
          return !!(s && Array.isArray(s.order) && s.order.length);
        },
        currentId: currentSlug,
        getMissed: function () {
          var s = readJson("ccnaautoPractice");
          return s && Array.isArray(s.missed) ? s.missed.slice() : [];
        },
        trackMiss: function (id) {
          var s = readJson("ccnaautoPractice");
          if (!s) return;
          s.missed = uniquePush(Array.isArray(s.missed) ? s.missed : [], id);
          writeJson("ccnaautoPractice", s);
        },
        clearMissed: function () {
          var s = readJson("ccnaautoPractice");
          if (!s) return;
          s.missed = [];
          writeJson("ccnaautoPractice", s);
        },
        startRetry: function (missed) {
          var s = readJson("ccnaautoPractice") || { v: 1 };
          s.v = 1;
          s.mode = "retry";
          s.order = missed.slice();
          s.missed = [];
          s.leaveRetry = true;
          writeJson("ccnaautoPractice", s);
          location.href = this.base + missed[0] + ".html#" + this.hash + "=0";
        },
        clearSession: function () {
          try {
            sessionStorage.removeItem("ccnaautoPractice");
          } catch (e) {}
        },
        exitHref: function () {
          return "/ccnaauto-home.html";
        },
      },
      {
        id: "encor",
        key: "encor",
        base: "/CCNP-ENCOR-Study/ENCOR_Questions/question-",
        home: "/ccnp-home.html",
        active: function () {
          if (isSampleOrExam()) return false;
          var q = readJson("ccnpQuestionQueue");
          if (Array.isArray(q) && q.length) return true;
          var linear = readJson("ccnpLinearScope");
          if (linear && Array.isArray(linear.ids) && linear.ids.length) return true;
          try {
            if (sessionStorage.getItem("ccnpReviewMode") === "1") {
              var rq = readJson("ccnpReviewQueue");
              if (Array.isArray(rq) && rq.length) return true;
            }
          } catch (e) {}
          return false;
        },
        currentId: currentEncorId,
        getMissed: function () {
          var m = readJson(MISSED_ENCOR_KEY);
          return Array.isArray(m) ? m.map(String) : [];
        },
        trackMiss: function (id) {
          var m = readJson(MISSED_ENCOR_KEY);
          if (!Array.isArray(m)) m = [];
          writeJson(MISSED_ENCOR_KEY, uniquePush(m, String(id)));
        },
        clearMissed: function () {
          try {
            sessionStorage.removeItem(MISSED_ENCOR_KEY);
          } catch (e) {}
        },
        startRetry: function (missed) {
          var ids = missed.map(function (x) {
            return parseInt(x, 10);
          }).filter(function (n) {
            return Number.isFinite(n);
          });
          if (!ids.length) return;
          try {
            sessionStorage.removeItem("ccnpReviewMode");
            sessionStorage.removeItem("ccnpReviewQueue");
            sessionStorage.removeItem("ccnpReviewTotal");
            sessionStorage.removeItem("ccnpLinearScope");
            sessionStorage.setItem("ccnpQuestionQueue", JSON.stringify(ids));
            sessionStorage.setItem("ccnpQuestionQueueIndex", "0");
            sessionStorage.removeItem(MISSED_ENCOR_KEY);
          } catch (e) {}
          location.href = this.base + ids[0] + ".html";
        },
        clearSession: function () {
          try {
            sessionStorage.removeItem("ccnpQuestionQueue");
            sessionStorage.removeItem("ccnpQuestionQueueIndex");
            sessionStorage.removeItem("ccnpLinearScope");
            sessionStorage.removeItem("ccnpReviewMode");
            sessionStorage.removeItem("ccnpReviewQueue");
            sessionStorage.removeItem("ccnpReviewTotal");
            sessionStorage.removeItem(MISSED_ENCOR_KEY);
          } catch (e) {}
        },
        exitHref: function () {
          return "/ccnp-home.html";
        },
      },
    ];
  }

  function activeAdapter() {
    if (isSampleOrExam()) return null;
    var list = adapters();
    for (var i = 0; i < list.length; i++) {
      if (list[i].active()) return list[i];
    }
    return null;
  }

  function ensureStyles() {
    if (document.getElementById(STYLE_ID)) return;
    var el = document.createElement("style");
    el.id = STYLE_ID;
    el.textContent =
      "#" +
      MODAL_ID +
      "{position:fixed;inset:0;z-index:100000;display:none;align-items:center;justify-content:center;padding:16px;background:rgba(8,11,22,.82);backdrop-filter:blur(6px)}" +
      "#" +
      MODAL_ID +
      ".is-open{display:flex}" +
      "#" +
      MODAL_ID +
      " .bcc-leave-card{width:min(440px,100%);border-radius:14px;border:1px solid #2d3b5a;background:#121a2b;color:#e6edf3;padding:22px;box-shadow:0 18px 48px rgba(0,0,0,.45)}" +
      "#" +
      MODAL_ID +
      " h2{margin:0 0 10px;font-size:1.15rem;font-weight:800;letter-spacing:-.02em}" +
      "#" +
      MODAL_ID +
      " p{margin:0 0 18px;color:#b8c3d6;line-height:1.5;font-size:.95rem}" +
      "#" +
      MODAL_ID +
      " .bcc-leave-actions{display:flex;flex-wrap:wrap;gap:10px;justify-content:flex-end}" +
      "#" +
      MODAL_ID +
      " button{appearance:none;border-radius:10px;padding:10px 14px;font:inherit;font-weight:800;cursor:pointer}" +
      "#" +
      MODAL_ID +
      " .bcc-leave-no{border:1px solid #4b556b;background:#2a3040;color:#e6edf3}" +
      "#" +
      MODAL_ID +
      " .bcc-leave-yes{border:1px solid #4f84d8;background:#2f66bf;color:#e6edf3}";
    document.head.appendChild(el);
  }

  function ensureModal() {
    ensureStyles();
    var modal = document.getElementById(MODAL_ID);
    if (modal) return modal;
    modal = document.createElement("div");
    modal.id = MODAL_ID;
    modal.setAttribute("role", "dialog");
    modal.setAttribute("aria-modal", "true");
    modal.setAttribute("aria-labelledby", "bccLeaveRetryTitle");
    modal.innerHTML =
      '<div class="bcc-leave-card">' +
      '<h2 id="bccLeaveRetryTitle">Retry missed questions?</h2>' +
      '<p id="bccLeaveRetryText"></p>' +
      '<div class="bcc-leave-actions">' +
      '<button type="button" class="bcc-leave-no" id="bccLeaveRetryNo">No, leave</button>' +
      '<button type="button" class="bcc-leave-yes" id="bccLeaveRetryYes">Yes, retry missed</button>' +
      "</div></div>";
    document.body.appendChild(modal);
    return modal;
  }

  var pendingExitHref = null;
  var pendingAdapter = null;

  function closeModal() {
    var modal = document.getElementById(MODAL_ID);
    if (modal) modal.classList.remove("is-open");
    pendingExitHref = null;
    pendingAdapter = null;
  }

  function openModal(adapter, missed, exitHref) {
    var modal = ensureModal();
    var text = document.getElementById("bccLeaveRetryText");
    var n = missed.length;
    text.textContent =
      "You missed " +
      n +
      " question" +
      (n === 1 ? "" : "s") +
      " in this bank. Would you like to retry the missed question" +
      (n === 1 ? "" : "s") +
      " before leaving?";
    pendingExitHref = exitHref || adapter.exitHref();
    pendingAdapter = adapter;
    modal.classList.add("is-open");
  }

  function leaveWithoutRetry() {
    var href = pendingExitHref;
    var adapter = pendingAdapter;
    closeModal();
    if (adapter) adapter.clearSession();
    location.href = href || "/";
  }

  function retryMissed() {
    var adapter = pendingAdapter;
    if (!adapter) {
      closeModal();
      return;
    }
    var missed = adapter.getMissed();
    closeModal();
    if (!missed.length) {
      adapter.clearSession();
      location.href = adapter.exitHref();
      return;
    }
    adapter.startRetry(missed);
  }

  function bindModalButtons() {
    var modal = ensureModal();
    var yes = document.getElementById("bccLeaveRetryYes");
    var no = document.getElementById("bccLeaveRetryNo");
    if (yes && !yes.dataset.bound) {
      yes.dataset.bound = "1";
      yes.addEventListener("click", retryMissed);
    }
    if (no && !no.dataset.bound) {
      no.dataset.bound = "1";
      no.addEventListener("click", leaveWithoutRetry);
    }
    if (!modal.dataset.bound) {
      modal.dataset.bound = "1";
      modal.addEventListener("click", function (e) {
        if (e.target === modal) leaveWithoutRetry();
      });
    }
  }

  function trackToAdapterId() {
    var adapter = activeAdapter();
    return adapter ? adapter.id : null;
  }

  function recordLearnerOutcome(correct) {
    if (!window.BCC_LEARNER || typeof window.BCC_LEARNER.recordAttempts !== "function") return;
    var adapter = activeAdapter();
    if (!adapter) return;
    var id = adapter.currentId();
    if (!id) return;
    var track =
      adapter.id === "encor"
        ? "encor"
        : adapter.id === "secplus"
          ? "secplus"
          : adapter.id === "ccnaauto"
            ? "ccnaauto"
            : "ccna";
    window.BCC_LEARNER.recordAttempts({
      track: track,
      mode: "bank",
      item_id: String(id),
      domain: null,
      correct: !!correct,
    });
  }

  function trackCurrentMissIfNeeded() {
    var adapter = activeAdapter();
    if (!adapter) return;
    var box = document.getElementById("answerBox");
    if (!box) return;
    var id = adapter.currentId();
    if (!id) return;
    if (box.classList.contains("incorrect")) {
      adapter.trackMiss(id);
      if (box.dataset.bccLeaveRecorded !== "1") {
        box.dataset.bccLeaveRecorded = "1";
        recordLearnerOutcome(false);
      }
      return;
    }
    if (box.classList.contains("correct") && box.dataset.bccLeaveRecorded !== "1") {
      box.dataset.bccLeaveRecorded = "1";
      recordLearnerOutcome(true);
    }
  }

  function observeMisses() {
    var box = document.getElementById("answerBox");
    if (!box || box.dataset.bccLeaveMissObs === "1") return;
    box.dataset.bccLeaveMissObs = "1";
    var obs = new MutationObserver(function () {
      trackCurrentMissIfNeeded();
    });
    obs.observe(box, { attributes: true, attributeFilter: ["class"] });
    trackCurrentMissIfNeeded();
  }

  function textLooksLikeLeave(label) {
    var t = String(label || "").trim().toLowerCase();
    return (
      t === "home" ||
      t === "finish" ||
      t === "finish session" ||
      t === "finish sample" ||
      t === "back to launcher" ||
      t === "back to home" ||
      t.indexOf("finish") === 0
    );
  }

  function hrefLooksLikeLeave(href, adapter) {
    if (!href) return false;
    var h = String(href).toLowerCase();
    if (h === "#" || h.indexOf("javascript:") === 0) return false;
    var homes = [
      "/ccna-home.html",
      "/ccnp-home.html",
      "/comptia-sec+-home.html",
      "/ccnaauto-home.html",
      "/ccna-study/ccna_training_portal.html",
      "/ccnp-encor-study/encor_training_portal.html",
      "/comp_tia_sec+/sec+_training_portal.html",
      "/ccnaauto-study/ccnaauto_training_portal.html",
    ];
    for (var i = 0; i < homes.length; i++) {
      if (h.indexOf(homes[i]) >= 0) return true;
    }
    if (adapter && adapter.home && h.indexOf(String(adapter.home).toLowerCase()) >= 0) return true;
    return false;
  }

  function isLeaveAnchor(a, adapter) {
    if (!a || a.tagName !== "A") return false;
    if (a.classList.contains("nav-home") || a.classList.contains("sim-nav-home")) return true;
    if (a.classList.contains("site-logo-corner")) return true;
    if (a.classList.contains("topbar-brand")) return true;
    var label = (a.textContent || "").replace(/\s+/g, " ");
    if (textLooksLikeLeave(label)) return true;
    return hrefLooksLikeLeave(a.getAttribute("href") || "", adapter);
  }

  function isIntraBankNext(a, adapter) {
    if (!a) return false;
    if (a.classList.contains("nav-next") || a.classList.contains("nav-prev")) {
      var label = ((a.textContent || "").trim() || "").toLowerCase();
      if (label === "next" || label === "back" || label === "previous") {
        // Finish labels are leave; plain Next/Back within bank are not.
        if (textLooksLikeLeave(label)) return false;
        var href = (a.getAttribute("href") || "").toLowerCase();
        if (hrefLooksLikeLeave(href, adapter)) return false;
        return true;
      }
    }
    return false;
  }

  function promptLeave(adapter, exitHref) {
    var missed = adapter.getMissed();
    if (!missed.length) {
      adapter.clearSession();
      location.href = exitHref || adapter.exitHref();
      return;
    }
    bindModalButtons();
    openModal(adapter, missed, exitHref || adapter.exitHref());
  }

  function onDocumentClick(e) {
    var adapter = activeAdapter();
    if (!adapter) return;
    var t = e.target;
    if (!t || typeof t.closest !== "function") return;
    var a = t.closest("a");
    if (!a || !document.body.contains(a)) return;
    if (isIntraBankNext(a, adapter)) return;
    if (!isLeaveAnchor(a, adapter)) return;

    var missed = adapter.getMissed();
    if (!missed.length) {
      // Still clear session when leaving a finished bank with no misses.
      adapter.clearSession();
      return;
    }

    e.preventDefault();
    e.stopPropagation();
    if (typeof e.stopImmediatePropagation === "function") e.stopImmediatePropagation();
    promptLeave(adapter, a.href || adapter.exitHref());
  }

  function boot() {
    if (isSampleOrExam()) return;
    var adapter = activeAdapter();
    if (!adapter) return;
    observeMisses();
    document.addEventListener("click", onDocumentClick, true);
    bindModalButtons();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
