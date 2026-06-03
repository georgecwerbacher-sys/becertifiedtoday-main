(function () {
  "use strict";

  var REVIEW_MARKS_KEY = "encorMarkForReview";
  var ENCOR_HOME_SAMPLE_KEY = "encorHomeSample";
  var QUEUE_KEY = "ccnpQuestionQueue";
  var LINEAR_SCOPE_KEY = "ccnpLinearScope";
  var REVIEW_MODE_KEY = "ccnpReviewMode";
  var REVIEW_QUEUE_KEY = "ccnpReviewQueue";
  var BASE = "/CCNP-ENCOR-Study/ENCOR_Questions/";
  var PORTAL = "/CCNP-ENCOR-Study/ENCOR_Training_Portal.html";
  var GUEST_HOME = "/ccnp-home.html";
  var SUBJECTS_URL = "/CCNP-ENCOR-Study/js/question-subjects.json";
  var VERSION_LABEL = "350-401 ENCOR v1.2";

  function questionIdFromPath() {
    var m = (location.pathname || "").match(/question-(\d+)\.html/i);
    return m ? parseInt(m[1], 10) : null;
  }

  function isSampleMode() {
    try {
      if (new URLSearchParams(location.search).get("sample") === "1") return true;
      return sessionStorage.getItem("ccnpUrlMaskPath") === "/sample";
    } catch (e) {
      return false;
    }
  }

  function isExamSimEmbed() {
    try {
      if (sessionStorage.getItem("ccnpTestSimQueue")) return true;
      if (sessionStorage.getItem("ccnpExamSim") === "1") return true;
      return new URLSearchParams(location.search).get("examSim") === "1";
    } catch (e) {
      return false;
    }
  }

  function hideShowAnswerInExamSim() {
    if (!isExamSimEmbed()) return;
    var showBtn = document.getElementById("showBtn");
    if (showBtn) showBtn.style.display = "none";
    document.querySelectorAll(".nav-show-answer").forEach(function (el) {
      el.style.display = "none";
    });
    document.querySelectorAll(".review-mark-box").forEach(function (el) {
      el.style.display = "none";
    });
  }

  function readHomeSampleSession() {
    try {
      var raw = sessionStorage.getItem(ENCOR_HOME_SAMPLE_KEY);
      if (!raw) return null;
      var s = JSON.parse(raw);
      if (!s || !Array.isArray(s.order) || !s.order.length) return null;
      return s;
    } catch (e) {
      return null;
    }
  }

  function homeSampleHashIndex() {
    var m = /^#encorHS=(\d+)$/.exec(location.hash || "");
    return m ? parseInt(m[1], 10) : 0;
  }

  function guestSampleActive() {
    try {
      return !!sessionStorage.getItem(ENCOR_HOME_SAMPLE_KEY);
    } catch (e) {
      return false;
    }
  }

  function parseQueue() {
    try {
      var raw = sessionStorage.getItem(QUEUE_KEY);
      if (!raw) return null;
      var q = JSON.parse(raw);
      return Array.isArray(q) && q.length ? q : null;
    } catch (e) {
      return null;
    }
  }

  function parseLinearScope() {
    try {
      var raw = sessionStorage.getItem(LINEAR_SCOPE_KEY);
      if (!raw) return null;
      var o = JSON.parse(raw);
      return o && Array.isArray(o.ids) && o.ids.length ? o.ids : null;
    } catch (e) {
      return null;
    }
  }

  function parseReviewQueue() {
    try {
      var raw = sessionStorage.getItem(REVIEW_QUEUE_KEY);
      if (!raw) return null;
      var q = JSON.parse(raw);
      return Array.isArray(q) && q.length ? q : null;
    } catch (e) {
      return null;
    }
  }

  function isReviewMode() {
    try {
      return sessionStorage.getItem(REVIEW_MODE_KEY) === "1";
    } catch (e) {
      return false;
    }
  }

  function questionHref(id) {
    var href = BASE + "question-" + id + ".html";
    if (isSampleMode()) href += (href.indexOf("?") >= 0 ? "&" : "?") + "sample=1";
    return href;
  }

  function activeHomeHref() {
    return isSampleMode() ? GUEST_HOME : PORTAL;
  }

  function getSubjects() {
    if (window.__encorQuestionSubjects) {
      return Promise.resolve(window.__encorQuestionSubjects);
    }
    if (window.__encorQuestionSubjects === false) return Promise.resolve(null);
    if (!window.__encorQuestionSubjectsPromise) {
      window.__encorQuestionSubjectsPromise = fetch(SUBJECTS_URL, { cache: "no-store" })
        .then(function (r) {
          if (!r.ok) throw new Error("subjects");
          return r.json();
        })
        .then(function (data) {
          window.__encorQuestionSubjects = data;
          return data;
        })
        .catch(function () {
          window.__encorQuestionSubjects = false;
          return null;
        });
    }
    return window.__encorQuestionSubjectsPromise;
  }

  function syncQuestionTopicMeta(qid) {
    var versionEl = document.querySelector(".question-topic-meta__version");
    var subjectEl = document.querySelector(".question-topic-meta__subject");
    if (versionEl) versionEl.textContent = VERSION_LABEL;
    if (!subjectEl || qid == null) return;

    getSubjects().then(function (data) {
      if (!data || !data.questions) return;
      var entry = data.questions[String(qid)];
      if (!entry) {
        subjectEl.textContent = "";
        return;
      }
      subjectEl.textContent =
        typeof entry === "string"
          ? entry
          : entry.label || (entry.section && entry.name ? entry.section + " " + entry.name : "");
    });
  }

  function resolveProgressText(qid) {
    var homeSample = readHomeSampleSession();
    if (homeSample) {
      var idx = homeSampleHashIndex();
      var item = homeSample.order[idx];
      if (item && item.type === "mcq") {
        var mcqNum = 0;
        for (var p = 0; p <= idx; p++) {
          if (homeSample.order[p] && homeSample.order[p].type === "mcq") mcqNum++;
        }
        var mcqTotal = homeSample.mcqCount;
        if (typeof mcqTotal !== "number") {
          mcqTotal = 0;
          for (var t = 0; t < homeSample.order.length; t++) {
            if (homeSample.order[t] && homeSample.order[t].type === "mcq") mcqTotal++;
          }
        }
        return "Question " + mcqNum + " of " + mcqTotal;
      }
    }

    if (isReviewMode()) {
      var rq = parseReviewQueue();
      if (rq && rq.length) {
        var ri = rq.indexOf(qid);
        if (ri >= 0) return "Review " + (ri + 1) + " of " + rq.length;
      }
    }

    var queue = parseQueue();
    if (queue) {
      var qi = queue.indexOf(qid);
      if (qi >= 0) return "Question " + (qi + 1) + " of " + queue.length;
    }

    var linear = parseLinearScope();
    if (linear) {
      var li = linear.indexOf(qid);
      if (li >= 0) return "Question " + (li + 1) + " of " + linear.length;
    }

    return "";
  }

  function syncProgressDisplay(qid) {
    var text = resolveProgressText(qid);
    var el = document.querySelector(".ccna-practice-progress");
    if (el && text) el.textContent = text;
    syncQuestionTopicMeta(qid);
  }

  function reviewMarkKey(qid) {
    return "encor:" + qid;
  }

  function readReviewMarks() {
    try {
      var raw = sessionStorage.getItem(REVIEW_MARKS_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch (e) {
      return {};
    }
  }

  function writeReviewMarks(marks) {
    try {
      sessionStorage.setItem(REVIEW_MARKS_KEY, JSON.stringify(marks));
    } catch (e) {}
  }

  function initMarkForReview(qid) {
    var wrap = document.querySelector(".review-mark-box");
    if (!wrap) return;
    var input = wrap.querySelector('input[type="checkbox"]');
    if (!input) return;
    var flagged = !!readReviewMarks()[reviewMarkKey(qid)];
    input.checked = flagged;
    wrap.classList.toggle("is-flagged", flagged);
    if (wrap.dataset.reviewWired) return;
    wrap.dataset.reviewWired = "1";
    input.addEventListener("change", function () {
      var marks = readReviewMarks();
      var key = reviewMarkKey(qid);
      if (input.checked) marks[key] = true;
      else delete marks[key];
      writeReviewMarks(marks);
      wrap.classList.toggle("is-flagged", input.checked);
    });
  }

  function resolveNext(qid) {
    if (isReviewMode()) {
      var rq = parseReviewQueue();
      if (rq && rq.length) {
        if (rq[0] !== qid && rq.indexOf(qid) < 0) return { href: questionHref(rq[0]), label: "Next" };
        if (rq.length >= 2) return { href: questionHref(rq[1]), label: "Next" };
      }
    }
    var queue = parseQueue();
    if (queue) {
      var qi = queue.indexOf(qid);
      if (qi >= 0 && queue[qi + 1] != null) {
        return { href: questionHref(queue[qi + 1]), label: "Next" };
      }
      if (qi >= 0) return { href: activeHomeHref(), label: isSampleMode() ? "Finish sample" : "Back to launcher" };
    }
    var linear = parseLinearScope();
    if (linear) {
      var li = linear.indexOf(qid);
      if (li >= 0 && linear[li + 1] != null) {
        return { href: questionHref(linear[li + 1]), label: "Next" };
      }
      if (li >= 0) return { href: activeHomeHref(), label: "Back to launcher" };
    }
    return null;
  }

  function resolveBack(qid) {
    var homeSample = readHomeSampleSession();
    if (homeSample) {
      var idx = homeSampleHashIndex();
      if (idx > 0) {
        var prev = homeSample.order[idx - 1];
        if (prev && prev.type === "mcq" && prev.id != null) {
          return { href: questionHref(prev.id) + "#encorHS=" + (idx - 1), label: "Back" };
        }
      }
      return null;
    }
    if (isReviewMode()) return null;
    var queue = parseQueue();
    if (queue) {
      var qi = queue.indexOf(qid);
      if (qi > 0) return { href: questionHref(queue[qi - 1]), label: "Back" };
      return null;
    }
    var linear = parseLinearScope();
    if (linear) {
      var li = linear.indexOf(qid);
      if (li > 0) return { href: questionHref(linear[li - 1]), label: "Back" };
      return null;
    }
    return null;
  }

  function wireNavLink(el, target) {
    if (!el || !target) return;
    el.href = target.href;
    el.textContent = target.label;
    el.classList.remove("nav-link--disabled");
    el.removeAttribute("aria-hidden");
  }

  function applySessionNav(qid) {
    var home = document.querySelector("a.nav-home");
    if (home) home.href = activeHomeHref();

    var nextEl = document.querySelector("a.nav-next");
    var prevEl = document.querySelector("a.nav-prev");
    var next = resolveNext(qid);
    var back = resolveBack(qid);

    if (nextEl && next) wireNavLink(nextEl, next);
    if (prevEl && back) wireNavLink(prevEl, back);
  }

  function ensureGuestBottomNav(qid) {
    if (!guestSampleActive()) return;
    var topNav = document.querySelector("nav.question-nav");
    if (topNav) topNav.style.display = "none";

    var nav = document.getElementById("encorSampleSimNav");
    if (!nav) {
      nav = document.createElement("nav");
      nav.id = "encorSampleSimNav";
      nav.className = "sim-nav encor-sample-sim-nav";
      nav.setAttribute("aria-label", "Sample navigation");
      nav.innerHTML =
        '<span class="sim-nav-btn sim-nav-prev encor-sample-prev sim-nav-btn--disabled" aria-hidden="true">Back</span>' +
        '<a class="sim-nav-btn sim-nav-home" href="' +
        GUEST_HOME +
        '">Home</a>' +
        '<a class="sim-nav-btn encor-sample-next" href="#">Next</a>';
      document.body.appendChild(nav);
      document.body.classList.add("encor-sample-guest-ui");
    }

    syncGuestBottomNav(qid);
  }

  function syncGuestBottomNav(qid) {
    var bar = document.getElementById("encorSampleSimNav");
    if (!bar || qid == null) return;

    var prevTop = document.querySelector("a.nav-prev");
    var nextTop = document.querySelector("a.nav-next");
    var prevBottom = bar.querySelector(".encor-sample-prev, .sim-nav-prev");
    var nextBottom = bar.querySelector(".encor-sample-next");

    if (prevTop && prevTop.tagName === "A" && prevBottom) {
      var prevA = prevTop.cloneNode(true);
      prevA.className = "sim-nav-btn sim-nav-prev encor-sample-prev";
      prevBottom.parentNode.replaceChild(prevA, prevBottom);
    } else if (prevBottom) {
      prevBottom.className = "sim-nav-btn sim-nav-prev encor-sample-prev sim-nav-btn--disabled";
      prevBottom.setAttribute("aria-hidden", "true");
    }

    if (nextTop && nextTop.tagName === "A" && nextBottom) {
      var nextA = nextTop.cloneNode(true);
      nextA.className = "sim-nav-btn encor-sample-next";
      nextBottom.parentNode.replaceChild(nextA, nextBottom);
    }
  }

  function run() {
    if (!document.body.classList.contains("encor-question-ui")) return;
    var qid = questionIdFromPath();
    if (qid == null) return;

    hideShowAnswerInExamSim();
    applySessionNav(qid);
    syncProgressDisplay(qid);
    initMarkForReview(qid);

    if (guestSampleActive()) {
      ensureGuestBottomNav(qid);
      syncGuestBottomNav(qid);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();
