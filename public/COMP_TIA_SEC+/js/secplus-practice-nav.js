(function () {
  "use strict";

  var KEY = "secplusPractice";
  var REVIEW_MARKS_KEY = "secplusMarkForReview";
  var SECPLUS_HOME_SAMPLE_KEY = "secplusHomeSample";
  var BASE = "/COMP_TIA_SEC+/SEC+_Questions/";
  var PORTAL = "/COMP_TIA_SEC+/SEC+_Training_Portal.html";
  var TOPIC_MAP_URL = "/COMP_TIA_SEC+/data/secplus-question-topic-map.json";
  var SECPLUS_STATIC_SAMPLE_TOTAL = 3;
  var SECPLUS_VERSION_LABEL = "Version 1.1 2026";
  var SECPLUS_DOMAIN_NAMES = {
    "1.0": "General Security Concepts",
    "2.0": "Threats, Vulnerabilities, and Mitigations",
    "3.0": "Security Architecture",
    "4.0": "Security Operations",
    "5.0": "Security Program Management and Oversight",
  };

  function isExamSimEmbed() {
    try {
      if (sessionStorage.getItem("secplusExamSim") === "1") return true;
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

  function slugFromPath() {
    var m = location.pathname.match(/\/([^/]+)\.html$/);
    return m ? decodeURIComponent(m[1]) : "";
  }

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

  function writeSession(s) {
    try {
      sessionStorage.setItem(KEY, JSON.stringify(s));
    } catch (e) {}
  }

  function hashIndex() {
    var m = /^#secplusP=(\d+)$/.exec(location.hash || "");
    return m ? parseInt(m[1], 10) : 0;
  }

  function homeSampleHashIndex() {
    var m = /^#secplusHS=(\d+)$/.exec(location.hash || "");
    return m ? parseInt(m[1], 10) : 0;
  }

  function pickIndexForSlug(order, slug, iHint) {
    var hits = [];
    for (var k = 0; k < order.length; k++) {
      if (order[k] === slug) hits.push(k);
    }
    if (!hits.length) return -1;
    for (var a = 0; a < hits.length; a++) {
      if (hits[a] >= iHint) return hits[a];
    }
    return hits[0];
  }

  function guestSampleActive() {
    try {
      return !!sessionStorage.getItem(SECPLUS_HOME_SAMPLE_KEY);
    } catch (e) {
      return false;
    }
  }

  function finishHrefForSession() {
    return guestSampleActive() ? "/comptia-sec+-home.html" : PORTAL;
  }

  function staticSampleQuestionIndex() {
    var m = /\/SEC\+_Samples\/sample-question-(\d+)\.html$/i.exec(location.pathname);
    return m ? parseInt(m[1], 10) : 0;
  }

  function isStaticSecplusSamplePage() {
    return staticSampleQuestionIndex() > 0;
  }

  function shouldUseSampleBottomNav() {
    return guestSampleActive() || isStaticSecplusSamplePage();
  }

  function readHomeSampleSession() {
    try {
      var raw = sessionStorage.getItem(SECPLUS_HOME_SAMPLE_KEY);
      if (!raw) return null;
      var s = JSON.parse(raw);
      if (!s || !Array.isArray(s.order) || !s.order.length) return null;
      return s;
    } catch (e) {
      return null;
    }
  }

  function reviewMarkKey(slug, practiceIndex) {
    if (isStaticSecplusSamplePage()) return "static:" + slug;
    var session = readSession();
    if (session) {
      var i =
        practiceIndex != null && practiceIndex >= 0
          ? practiceIndex
          : pickIndexForSlug(session.order, slug, hashIndex());
      if (i >= 0) return "secplus:" + (session.bank || "1") + ":" + i + ":" + slug;
    }
    return "static:" + slug;
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

  function isMarkedForReview(slug, practiceIndex) {
    return !!readReviewMarks()[reviewMarkKey(slug, practiceIndex)];
  }

  function setMarkedForReview(slug, practiceIndex, flagged) {
    var marks = readReviewMarks();
    var key = reviewMarkKey(slug, practiceIndex);
    if (flagged) marks[key] = true;
    else delete marks[key];
    writeReviewMarks(marks);
  }

  function practiceIndexForSlug(slug) {
    var session = readSession();
    if (!session) return null;
    var i = pickIndexForSlug(session.order, slug, hashIndex());
    return i >= 0 ? i : null;
  }

  function ensureReviewMarkBox() {
    var wrap = document.querySelector(".review-mark-box");
    if (wrap) return wrap;
    var footer = document.querySelector(".answer-footer");
    if (!footer) return null;
    var side = document.querySelector(".answer-side-actions");
    if (!side) return null;
    wrap = document.createElement("label");
    wrap.className = "review-mark-box";
    wrap.id = "reviewMarkWrap";
    wrap.innerHTML =
      '<input type="checkbox" id="reviewMark" aria-label="Mark for review" />' +
      '<span class="review-mark-box__label">Review</span>';
    side.appendChild(wrap);
    return wrap;
  }

  function syncReviewMarkUI(slug, practiceIndex) {
    var wrap = ensureReviewMarkBox();
    if (!wrap) return;
    var input = wrap.querySelector('input[type="checkbox"]');
    if (!input) return;
    var flagged = isMarkedForReview(slug, practiceIndex);
    input.checked = flagged;
    wrap.classList.toggle("is-flagged", flagged);
  }

  function initMarkForReview(slug) {
    var practiceIndex = practiceIndexForSlug(slug);
    ensureReviewMarkBox();
    syncReviewMarkUI(slug, practiceIndex);

    var wrap = document.querySelector(".review-mark-box");
    if (!wrap || wrap.dataset.reviewWired) return;
    wrap.dataset.reviewWired = "1";
    var input = wrap.querySelector('input[type="checkbox"]');
    if (!input) return;
    input.addEventListener("change", function () {
      var idx = practiceIndexForSlug(slug);
      setMarkedForReview(slug, idx, input.checked);
      wrap.classList.toggle("is-flagged", input.checked);
    });
  }

  function getTopicAssignments() {
    if (window._secplusTopicAssignments && typeof window._secplusTopicAssignments === "object") {
      return Promise.resolve(window._secplusTopicAssignments);
    }
    if (window._secplusTopicAssignments === false) return Promise.resolve(null);
    if (!window._secplusTopicAssignmentsPromise) {
      window._secplusTopicAssignmentsPromise = fetch(TOPIC_MAP_URL, { credentials: "same-origin" })
        .then(function (res) {
          if (!res.ok) throw new Error("topic map http " + res.status);
          return res.json();
        })
        .then(function (data) {
          var a = data && data.assignments;
          var obj = a && typeof a === "object" ? a : {};
          window._secplusTopicAssignments = obj;
          return obj;
        })
        .catch(function () {
          window._secplusTopicAssignments = false;
          return null;
        });
    }
    return window._secplusTopicAssignmentsPromise;
  }

  function syncQuestionTopicMeta(slug) {
    if (isStaticSecplusSamplePage()) return;

    var versionEl = document.querySelector(".question-topic-meta__version");
    var subjectEl = document.querySelector(".question-topic-meta__subject");
    if (versionEl) versionEl.textContent = SECPLUS_VERSION_LABEL;

    getTopicAssignments().then(function (assignments) {
      if (!subjectEl || !assignments) return;
      var objs = assignments[slug + ".html"];
      if (!objs || !objs.length) {
        subjectEl.textContent = "";
        return;
      }
      var maj = String(objs[0]).split(".")[0] + ".0";
      var name = SECPLUS_DOMAIN_NAMES[maj] || "Domain " + maj;
      subjectEl.textContent = maj + " " + name;
    });
  }

  function resolveProgressText(slug, practiceIndex) {
    var session = readSession();
    if (session && practiceIndex != null && practiceIndex >= 0) {
      return "Question " + (practiceIndex + 1) + " of " + session.order.length;
    }

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

    if (slug && session) {
      var i = pickIndexForSlug(session.order, slug, hashIndex());
      if (i >= 0) return "Question " + (i + 1) + " of " + session.order.length;
    }

    var staticN = staticSampleQuestionIndex();
    if (staticN > 0) {
      return "Question " + staticN + " of " + SECPLUS_STATIC_SAMPLE_TOTAL;
    }

    return "";
  }

  function formatDomainLabel(domainId) {
    var name = SECPLUS_DOMAIN_NAMES[domainId] || "";
    return domainId + (name ? " " + name : "");
  }

  function domainsFromSampleOrder(order) {
    var seen = Object.create(null);
    var list = [];
    (order || []).forEach(function (item) {
      if (!item || item.type !== "mcq" || !item.domain) return;
      if (seen[item.domain]) return;
      seen[item.domain] = true;
      list.push(item.domain);
    });
    list.sort(function (a, b) {
      return parseFloat(a) - parseFloat(b);
    });
    return list;
  }

  function ensureSampleSubjectsFooter() {
    var card = document.querySelector(".question-shell .card") || document.querySelector("main.card") || document.querySelector(".card");
    if (!card) return null;
    var footer = card.querySelector(".sample-subjects-footer");
    if (!footer) {
      footer = document.createElement("div");
      footer.className = "sample-subjects-footer";
      footer.setAttribute("aria-label", "SY0-701 domains in this sample");
      var title = document.createElement("p");
      title.className = "sample-subjects-footer__title";
      title.textContent = "SY0-701 domains in this sample";
      footer.appendChild(title);
      var list = document.createElement("ul");
      list.className = "sample-subjects-footer__list";
      footer.appendChild(list);
      card.appendChild(footer);
    }
    return footer.querySelector(".sample-subjects-footer__list");
  }

  function syncSampleSubjectsFooter() {
    var session = readHomeSampleSession();
    if (!session || !session.order || !session.order.length) {
      var stale = document.querySelector(".sample-subjects-footer");
      if (stale) stale.remove();
      return;
    }
    var allMcq = session.order.every(function (item) {
      return item && item.type === "mcq";
    });
    if (!allMcq) return;

    var listEl = ensureSampleSubjectsFooter();
    if (!listEl) return;

    var domains = Array.isArray(session.sampleDomains) && session.sampleDomains.length
      ? session.sampleDomains
      : domainsFromSampleOrder(session.order);
    listEl.textContent = "";
    domains.forEach(function (domainId) {
      var li = document.createElement("li");
      li.textContent = formatDomainLabel(domainId);
      listEl.appendChild(li);
    });
  }

  function syncProgressDisplay(slug, practiceIndex) {
    var text = resolveProgressText(slug, practiceIndex);
    if (!text) return;
    var el = document.querySelector(".ccna-practice-progress");
    if (el) el.textContent = text;
    syncQuestionTopicMeta(slug);
    syncSampleSubjectsFooter();
  }

  function ensureSampleBottomNav() {
    var nav = document.getElementById("secplusSampleSimNav");
    if (!nav) {
      nav = document.createElement("nav");
      nav.id = "secplusSampleSimNav";
      nav.className = "sim-nav secplus-sample-sim-nav";
      nav.setAttribute("aria-label", "Sample navigation");

      var prev = document.createElement("span");
      prev.className = "sim-nav-btn sim-nav-prev secplus-sample-prev sim-nav-btn--disabled";
      prev.setAttribute("aria-hidden", "true");
      prev.textContent = "Back";

      var home = document.createElement("a");
      home.className = "sim-nav-btn sim-nav-home";
      home.href = finishHrefForSession();
      home.textContent = "Home";

      var next = document.createElement("a");
      next.className = "sim-nav-btn secplus-sample-next";
      next.href = "#";
      next.textContent = "Next";

      nav.appendChild(prev);
      nav.appendChild(home);
      nav.appendChild(next);
      document.body.appendChild(nav);
    }

    document.body.classList.add("secplus-sample-guest-ui");
    if (isStaticSecplusSamplePage()) {
      document.body.classList.add("secplus-static-sample");
    }

    var topNav = document.querySelector("nav.question-nav");
    if (topNav && shouldUseSampleBottomNav()) {
      topNav.style.display = "none";
    }
  }

  function syncSampleBottomNavLink(bar, bottomSelector, topSelector, role) {
    var bottomEl = bar.querySelector(bottomSelector);
    var topEl = document.querySelector(topSelector);
    if (!bottomEl) return;

    var baseClass = "sim-nav-btn";
    if (role === "prev") baseClass += " sim-nav-prev secplus-sample-prev";
    if (role === "next") baseClass += " secplus-sample-next";

    if (topEl && topEl.tagName === "A") {
      var synced = topEl.cloneNode(true);
      synced.className = baseClass;
      synced.classList.remove("nav-link", "nav-prev", "nav-next", "nav-home", "next-link", "nav-link--disabled");
      bottomEl.parentNode.replaceChild(synced, bottomEl);
      return;
    }

    if (topEl && topEl.classList.contains("nav-link--disabled")) {
      var disabled = document.createElement("span");
      disabled.className = baseClass + " sim-nav-btn--disabled";
      disabled.textContent = (topEl.textContent || "Back").trim();
      disabled.setAttribute("aria-hidden", "true");
      bottomEl.parentNode.replaceChild(disabled, bottomEl);
    }
  }

  function staticSamplePageName(n) {
    return "sample-question-" + n + ".html";
  }

  function syncStaticSampleBottomNav() {
    var n = staticSampleQuestionIndex();
    if (!n) return;
    var bar = document.getElementById("secplusSampleSimNav");
    if (!bar) return;

    var home = bar.querySelector(".sim-nav-home");
    if (home) home.href = "/comptia-sec+-home.html";

    var prevHref = n > 1 ? staticSamplePageName(n - 1) : null;
    var nextHref = n < SECPLUS_STATIC_SAMPLE_TOTAL ? staticSamplePageName(n + 1) : null;

    var prevEl = bar.querySelector(".secplus-sample-prev, .sim-nav-prev");
    if (prevEl) {
      if (prevHref) {
        var prevA = document.createElement("a");
        prevA.className = "sim-nav-btn sim-nav-prev secplus-sample-prev";
        prevA.href = prevHref;
        prevA.textContent = "Back";
        prevEl.parentNode.replaceChild(prevA, prevEl);
      } else {
        var prevSpan = document.createElement("span");
        prevSpan.className = "sim-nav-btn sim-nav-prev secplus-sample-prev sim-nav-btn--disabled";
        prevSpan.textContent = "Back";
        prevSpan.setAttribute("aria-hidden", "true");
        prevEl.parentNode.replaceChild(prevSpan, prevEl);
      }
    }

    var nextEl = bar.querySelector(".secplus-sample-next");
    if (nextEl) {
      if (nextHref) {
        var nextA = document.createElement("a");
        nextA.className = "sim-nav-btn secplus-sample-next";
        nextA.href = nextHref;
        nextA.textContent = "Next";
        nextEl.parentNode.replaceChild(nextA, nextEl);
      } else {
        var finishA = document.createElement("a");
        finishA.className = "sim-nav-btn secplus-sample-next";
        finishA.href = "/comptia-sec+-home.html";
        finishA.textContent = "Finish";
        nextEl.parentNode.replaceChild(finishA, nextEl);
      }
    }
  }

  function syncSampleBottomNav(slug, practiceIndex) {
    if (!shouldUseSampleBottomNav()) return;
    var bar = document.getElementById("secplusSampleSimNav");
    if (!bar) return;

    if (isStaticSecplusSamplePage()) {
      syncStaticSampleBottomNav();
      syncProgressDisplay(slug, practiceIndex);
      return;
    }

    var home = bar.querySelector(".sim-nav-home");
    if (home) home.href = finishHrefForSession();

    syncSampleBottomNavLink(bar, ".secplus-sample-prev, .sim-nav-prev", "a.nav-prev, span.nav-prev", "prev");
    syncSampleBottomNavLink(bar, ".secplus-sample-next", "a.nav-next", "next");

    syncProgressDisplay(slug, practiceIndex);
  }

  function findNextPrevElements() {
    return {
      prevEl: document.querySelector("a.nav-prev"),
      nextEl: document.querySelector("a.nav-next"),
    };
  }

  function applyPracticeNav(slug) {
    var session = readSession();
    if (!session) return null;
    var order = session.order;
    var iHint = hashIndex();
    var i = pickIndexForSlug(order, slug, iHint);
    if (i < 0) return null;
    if (i !== iHint) {
      try {
        history.replaceState(null, "", location.pathname + location.search + "#secplusP=" + i);
      } catch (e) {}
    }

    var els = findNextPrevElements();
    if (els.nextEl) {
      if (i + 1 < order.length) {
        els.nextEl.href = BASE + order[i + 1] + ".html#secplusP=" + (i + 1);
        els.nextEl.textContent = "Next";
        els.nextEl.classList.remove("nav-link--disabled");
        els.nextEl.removeAttribute("aria-hidden");
      } else {
        els.nextEl.href = PORTAL;
        els.nextEl.textContent = "Finish";
      }
    }
    if (els.prevEl && i > 0) {
      els.prevEl.href = BASE + order[i - 1] + ".html#secplusP=" + (i - 1);
      els.prevEl.textContent = "Back";
      els.prevEl.classList.remove("nav-link--disabled");
      els.prevEl.removeAttribute("aria-hidden");
    }

    if (shouldUseSampleBottomNav()) {
      syncSampleBottomNav(slug, i);
    } else {
      syncProgressDisplay(slug, i);
    }

    return { mode: session.mode || "linear", index: i };
  }

  function applySampleFallbackNav(slug) {
    ensureSampleBottomNav();
    var topHome = document.querySelector("a.nav-home");
    if (topHome) topHome.href = finishHrefForSession();
    syncSampleBottomNav(slug, null);
  }

  function bindReviewQueue(slug) {
    var session = readSession();
    if (!session || session.mode !== "review") return;

    var box = document.getElementById("answerBox");
    if (!box) return;

    var obs = new MutationObserver(function () {
      if (box.classList.contains("correct")) {
        delete box.dataset.secplusReviewQueued;
        return;
      }
      if (!box.classList.contains("incorrect")) return;
      if (box.dataset.secplusReviewQueued) return;
      box.dataset.secplusReviewQueued = "1";

      var s2 = readSession();
      if (!s2 || s2.mode !== "review") return;
      var nowI = pickIndexForSlug(s2.order, slug, hashIndex());
      if (nowI < 0 || s2.order[nowI] !== slug) return;
      s2.order.push(slug);
      writeSession(s2);
      applyPracticeNav(slug);
    });
    obs.observe(box, { attributes: true, attributeFilter: ["class"] });
  }

  function run() {
    try {
      if (sessionStorage.getItem(SECPLUS_HOME_SAMPLE_KEY) && !document.body.classList.contains("secplus-question-ui")) {
        /* guest MCQ from bank still uses secplus-question-ui when regenerated */
      }
    } catch (e) {}

    var slug = slugFromPath();
    if (!slug && !isStaticSecplusSamplePage()) return;
    if (isStaticSecplusSamplePage()) {
      slug = "sample-question-" + staticSampleQuestionIndex();
    }
    if (!slug) return;

    if (shouldUseSampleBottomNav()) {
      ensureSampleBottomNav();
    }

    hideShowAnswerInExamSim();

    var nav = applyPracticeNav(slug);
    if (!nav && shouldUseSampleBottomNav()) {
      applySampleFallbackNav(slug);
      initMarkForReview(slug);
      return;
    }
    if (!nav) {
      if (isStaticSecplusSamplePage()) {
        syncProgressDisplay(slug, null);
      }
      initMarkForReview(slug);
      syncQuestionTopicMeta(slug);
      syncSampleSubjectsFooter();
      return;
    }

    initMarkForReview(slug);
    bindReviewQueue(slug);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();
