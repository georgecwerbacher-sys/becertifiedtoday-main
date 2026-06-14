(function () {
  "use strict";

  var KEY = "ccnaPractice100";
  var BASE = "/CCNA-Study/CCNA_questions/";
  function guestSampleActive() {
    try {
      if (new URLSearchParams(location.search).get("sample") === "1") return true;
      return sessionStorage.getItem("ccnpUrlMaskPath") === "/sample";
    } catch (e) {
      return false;
    }
  }

  function finishHrefForSession() {
    return guestSampleActive() ? "/ccna-home.html" : "/CCNA-Study/CCNA_Training_Portal.html";
  }
  var TOPIC_MAP_URL = "/CCNA-Study/data/ccna-question-topic-map.json";
  var MANIFEST_URL = "/CCNA-Study/data/ccna-practice-questions-manifest.json";
  /** Upper bound on how many extra cross-bank items adaptive mode may inject (excludes retries of the missed slug). */
  var ADAPTIVE_CROSS_BANK_CAP = 120;

  window.CCNA_PRACTICE_100 = window.CCNA_PRACTICE_100 || {};

  function slugFromPath() {
    var m = location.pathname.match(/\/([^/]+)\.html$/);
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

  function writeSession(s) {
    try {
      sessionStorage.setItem(KEY, JSON.stringify(s));
    } catch (e) {}
  }

  function hashIndex() {
    var h = location.hash || "";
    var m = /^#ccnaP=(\d+)$/.exec(h);
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

  function sampleQuerySuffix() {
    return guestSampleActive() ? "?sample=1" : "";
  }

  var CCNA_STATIC_SAMPLE_TOTAL = 5;
  var CCNA_HOME_SAMPLE_KEY = "ccnaHomeSample";
  var CCNA_DOMAIN_NAMES = {
    "1.0": "Network Fundamentals",
    "2.0": "Network Access",
    "3.0": "IP Connectivity",
    "4.0": "IP Services",
    "5.0": "Security Fundamentals",
    "6.0": "Automation and Programmability",
  };
  var CCNA_VERSION_11_LABEL = "Version 1.1 2026";
  var CCNA_VERSION_20_LABEL = "Version 2.0 2026";
  var CCNA_UPDATED_LABEL = "Updated for 2026";
  var VERSION_20_SLUGS_URL = "/CCNA-Study/data/ccna-version-2-0-slugs.json";

  function sessionVersionFilter(session) {
    if (!session) return "";
    if (session.version === "v20" || session.version === "v11") return session.version;
    if (session.versionMin) return "v20";
    if (session.versionMax) return "v11";
    return "";
  }

  function reviewMarkKey(slug, practiceIndex) {
    if (isStaticCcnaSamplePage()) return "static:" + slug;
    var session = readSession();
    if (session) {
      var i =
        practiceIndex != null && practiceIndex >= 0
          ? practiceIndex
          : pickIndexForSlug(session.order, slug, hashIndex());
      if (i >= 0) return "p100:" + (session.bank || "1") + ":" + i + ":" + slug;
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
    var marks = readReviewMarks();
    return !!marks[reviewMarkKey(slug, practiceIndex)];
  }

  function setMarkedForReview(slug, practiceIndex, flagged) {
    var marks = readReviewMarks();
    var key = reviewMarkKey(slug, practiceIndex);
    if (flagged) marks[key] = true;
    else delete marks[key];
    writeReviewMarks(marks);
  }

  function ensureAnswerSideActions() {
    var side = document.querySelector(".answer-side-actions");
    if (side) return side;

    var footer = document.querySelector(".answer-footer");
    if (!footer) return null;

    side = document.createElement("div");
    side.className = "answer-side-actions";
    var review = footer.querySelector(".review-mark-box");
    if (review) {
      review.parentNode.removeChild(review);
      side.appendChild(review);
    }
    footer.appendChild(side);
    return side;
  }

  function ensureReviewMarkBox() {
    var wrap = document.querySelector(".review-mark-box");
    if (wrap) return wrap;

    var footer = document.querySelector(".answer-footer");
    var actions = document.querySelector(".answer-actions");
    if (!actions) return null;

    if (!footer) {
      footer = document.createElement("div");
      footer.className = "answer-footer";
      actions.parentNode.insertBefore(footer, actions);
      footer.appendChild(actions);
    }

    var side = ensureAnswerSideActions();
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

  function practiceIndexForSlug(slug) {
    var session = readSession();
    if (!session) return null;
    var i = pickIndexForSlug(session.order, slug, hashIndex());
    return i >= 0 ? i : null;
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

  function readHomeSampleSession() {
    try {
      var raw = sessionStorage.getItem(CCNA_HOME_SAMPLE_KEY);
      if (!raw) return null;
      var s = JSON.parse(raw);
      if (!s || !Array.isArray(s.order) || !s.order.length) return null;
      return s;
    } catch (e) {
      return null;
    }
  }

  function homeSampleHashIndex() {
    var m = /^#ccnaHS=(\d+)$/.exec(location.hash || "");
    return m ? parseInt(m[1], 10) : 0;
  }

  function staticSampleQuestionIndex() {
    var m = /\/CCNA_Samples\/sample-question-(\d+)\.html$/i.exec(location.pathname);
    return m ? parseInt(m[1], 10) : 0;
  }

  function isStaticCcnaSamplePage() {
    return staticSampleQuestionIndex() > 0;
  }

  function shouldUseSampleBottomNav() {
    return guestSampleActive() || isStaticCcnaSamplePage();
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
      if (i >= 0) {
        return "Question " + (i + 1) + " of " + session.order.length;
      }
    }

    var staticN = staticSampleQuestionIndex();
    if (staticN > 0) {
      return "Question " + staticN + " of " + CCNA_STATIC_SAMPLE_TOTAL;
    }

    return "";
  }

  function ensureQuestionTopicMeta() {
    if (document.querySelector(".question-topic-meta")) return document.querySelector(".question-topic-meta");

    var block = document.querySelector(".question-progress-block");
    var actions = document.querySelector(".answer-actions");
    if (!block && actions) {
      block = document.createElement("div");
      block.className = "question-progress-block";
      var progress = actions.querySelector(".ccna-practice-progress");
      if (progress) {
        actions.removeChild(progress);
        block.appendChild(progress);
      } else {
        progress = document.createElement("span");
        progress.className = "ccna-practice-progress";
        progress.setAttribute("aria-live", "polite");
        block.appendChild(progress);
      }
      actions.appendChild(block);
    }
    if (!block) return null;

    var meta = document.createElement("p");
    meta.className = "question-topic-meta";
    meta.innerHTML =
      '<span class="question-topic-meta__version"></span>' +
      '<span class="question-topic-meta__subject"></span>';
    block.appendChild(meta);
    return meta;
  }

  function getVersion20SlugSet() {
    var inst = window.CCNA_PRACTICE_100;
    if (inst._version20SlugSet && typeof inst._version20SlugSet === "object") {
      return Promise.resolve(inst._version20SlugSet);
    }
    if (inst._version20SlugSet === false) return Promise.resolve(false);
    if (inst._version20SlugsPromise && typeof inst._version20SlugsPromise.then === "function") {
      return inst._version20SlugsPromise;
    }
    if (!inst._version20SlugsPromiseNav) {
      inst._version20SlugsPromiseNav = fetch(VERSION_20_SLUGS_URL, { credentials: "same-origin" })
        .then(function (res) {
          if (!res.ok) throw new Error("version 2.0 slugs http " + res.status);
          return res.json();
        })
        .then(function (data) {
          var set = {};
          var slugs = data && data.slugs;
          if (Array.isArray(slugs)) {
            for (var i = 0; i < slugs.length; i++) {
              if (slugs[i]) set[String(slugs[i])] = true;
            }
          }
          inst._version20SlugSet = set;
          return set;
        })
        .catch(function () {
          inst._version20SlugSet = false;
          return false;
        });
    }
    return inst._version20SlugsPromiseNav;
  }

  function isVersion20Slug(slug, v20Set) {
    return !!(slug && v20Set && v20Set[slug]);
  }

  function bakedVersionLabelFromDom() {
    var el = document.querySelector(".question-topic-meta__version");
    if (!el) return "";
    return String(el.textContent || "").trim();
  }

  function versionLabelForSlug(slug, v20Set) {
    if (document.body && document.body.classList.contains("dragdrop-exercise")) {
      return CCNA_UPDATED_LABEL;
    }
    if (/\/CCNA_labs\//i.test(location.pathname)) {
      return CCNA_UPDATED_LABEL;
    }
    var session = readSession();
    var versionFilter = sessionVersionFilter(session);
    if (versionFilter === "v20") return CCNA_VERSION_20_LABEL;
    if (versionFilter === "v11") return CCNA_VERSION_11_LABEL;
    if (v20Set && typeof v20Set === "object") {
      return isVersion20Slug(slug, v20Set) ? CCNA_VERSION_20_LABEL : CCNA_VERSION_11_LABEL;
    }
    var hub = window.CCNA_PRACTICE_100 || {};
    var hubSet = hub._version20SlugSet;
    if (hubSet && typeof hubSet === "object") {
      return isVersion20Slug(slug, hubSet) ? CCNA_VERSION_20_LABEL : CCNA_VERSION_11_LABEL;
    }
    return bakedVersionLabelFromDom() || CCNA_VERSION_11_LABEL;
  }

  function subjectLabelForSlug(assignments, slug) {
    if (!assignments || !slug) return "";
    var objs = assignments[slug + ".html"];
    if (!objs || !objs.length) return "";
    var majNum = String(objs[0]).split(".")[0];
    if (!/^[1-6]$/.test(majNum)) return "";
    var majKey = majNum + ".0";
    var name = CCNA_DOMAIN_NAMES[majKey] || "Domain " + majKey;
    return majNum + " \u2014 " + name;
  }

  function syncQuestionTopicMeta(slug) {
    if (isStaticCcnaSamplePage()) return;

    var versionEl = document.querySelector(".question-topic-meta__version");
    var subjectEl = document.querySelector(".question-topic-meta__subject");
    if (!versionEl && !subjectEl) {
      ensureQuestionTopicMeta();
      versionEl = document.querySelector(".question-topic-meta__version");
      subjectEl = document.querySelector(".question-topic-meta__subject");
    }
    if (!versionEl && !subjectEl) return;

    function applyVersionLabel(v20Set) {
      if (versionEl) versionEl.textContent = versionLabelForSlug(slug, v20Set);
    }
    applyVersionLabel(null);
    getVersion20SlugSet().then(function (v20Set) {
      applyVersionLabel(v20Set && typeof v20Set === "object" ? v20Set : null);
    });

    getTopicAssignments().then(function (assignments) {
      if (!subjectEl) return;
      subjectEl.textContent = subjectLabelForSlug(assignments, slug);
    });
  }

  function ensurePracticeProgressHost() {
    var el = document.querySelector(".ccna-practice-progress");
    if (el) return el;

    var actions = document.querySelector(".answer-actions");
    if (actions) {
      var block = document.querySelector(".question-progress-block");
      if (!block) {
        block = document.createElement("div");
        block.className = "question-progress-block";
        actions.appendChild(block);
      }
      el = document.createElement("span");
      el.className = "ccna-practice-progress";
      el.setAttribute("aria-live", "polite");
      block.insertBefore(el, block.firstChild);
      ensureQuestionTopicMeta();
      return el;
    }

    var box = document.getElementById("answerBox");
    if (box && box.parentNode) {
      el = document.createElement("p");
      el.className = "ccna-practice-progress ccna-practice-progress--standalone";
      el.setAttribute("aria-live", "polite");
      box.parentNode.insertBefore(el, box);
      return el;
    }

    return null;
  }

  function syncProgressDisplay(slug, practiceIndex) {
    var text = resolveProgressText(slug, practiceIndex);
    if (!text) return;

    var el = document.querySelector(".ccna-practice-progress");
    if (!el) el = ensurePracticeProgressHost();
    if (el) el.textContent = text;
    syncQuestionTopicMeta(slug);
  }

  function ensureSampleBottomNav() {
    var nav = document.getElementById("ccnaSampleSimNav");
    if (!nav) {
      nav = document.createElement("nav");
      nav.id = "ccnaSampleSimNav";
      nav.className = "sim-nav ccna-sample-sim-nav";
      nav.setAttribute("aria-label", "Sample navigation");

      var prev = document.createElement("span");
      prev.className = "sim-nav-btn sim-nav-prev ccna-sample-prev sim-nav-btn--disabled";
      prev.setAttribute("aria-hidden", "true");
      prev.textContent = "Back";

      var home = document.createElement("a");
      home.className = "sim-nav-btn sim-nav-home";
      home.href = finishHrefForSession();
      home.textContent = "Home";

      var next = document.createElement("a");
      next.className = "sim-nav-btn ccna-sample-next";
      next.href = "#";
      next.textContent = "Next";

      nav.appendChild(prev);
      nav.appendChild(home);
      nav.appendChild(next);
      document.body.appendChild(nav);
    } else if (!nav.querySelector(".ccna-sample-prev, .sim-nav-prev")) {
      var prevEl = document.createElement("span");
      prevEl.className = "sim-nav-btn sim-nav-prev ccna-sample-prev sim-nav-btn--disabled";
      prevEl.setAttribute("aria-hidden", "true");
      prevEl.textContent = "Back";
      nav.insertBefore(prevEl, nav.firstChild);
    }

    document.body.classList.add("ccna-sample-guest-ui");
    if (isStaticCcnaSamplePage()) {
      document.body.classList.add("ccna-static-sample");
    }

    var topNav = document.querySelector("nav.question-nav");
    if (topNav && (guestSampleActive() || isStaticCcnaSamplePage())) {
      topNav.style.display = "none";
    }
  }

  function syncSampleBottomNavLink(bar, bottomSelector, topSelector, role) {
    var bottomEl = bar.querySelector(bottomSelector);
    var topEl = document.querySelector(topSelector);
    if (!bottomEl) return;

    var baseClass = "sim-nav-btn";
    if (role === "prev") baseClass += " sim-nav-prev ccna-sample-prev";
    if (role === "next") baseClass += " ccna-sample-next";

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
      return;
    }

    if (role === "prev") {
      var back = document.createElement("span");
      back.className = baseClass + " sim-nav-btn--disabled";
      back.textContent = "Back";
      back.setAttribute("aria-hidden", "true");
      bottomEl.parentNode.replaceChild(back, bottomEl);
    }
  }

  function staticSamplePageName(n) {
    return "sample-question-" + n + ".html";
  }

  function syncStaticSampleBottomNav() {
    var n = staticSampleQuestionIndex();
    if (!n) return;
    var bar = document.getElementById("ccnaSampleSimNav");
    if (!bar) return;

    var home = bar.querySelector(".sim-nav-home");
    if (home) home.href = "/ccna-home.html";

    var prevHref = n > 1 ? staticSamplePageName(n - 1) : null;
    var nextHref = n < CCNA_STATIC_SAMPLE_TOTAL ? staticSamplePageName(n + 1) : null;

    var prevEl = bar.querySelector(".ccna-sample-prev, .sim-nav-prev");
    if (prevEl) {
      if (prevHref) {
        var prevA = document.createElement("a");
        prevA.className = "sim-nav-btn sim-nav-prev ccna-sample-prev";
        prevA.href = prevHref;
        prevA.textContent = "Back";
        prevEl.parentNode.replaceChild(prevA, prevEl);
      } else {
        var prevSpan = document.createElement("span");
        prevSpan.className = "sim-nav-btn sim-nav-prev ccna-sample-prev sim-nav-btn--disabled";
        prevSpan.textContent = "Back";
        prevSpan.setAttribute("aria-hidden", "true");
        prevEl.parentNode.replaceChild(prevSpan, prevEl);
      }
    }

    var nextEl = bar.querySelector(".ccna-sample-next");
    if (nextEl) {
      if (nextHref) {
        var nextA = document.createElement("a");
        nextA.className = "sim-nav-btn ccna-sample-next";
        nextA.href = nextHref;
        nextA.textContent = "Next";
        nextEl.parentNode.replaceChild(nextA, nextEl);
      } else {
        var finishA = document.createElement("a");
        finishA.className = "sim-nav-btn ccna-sample-next";
        finishA.href = "/ccna-home.html";
        finishA.textContent = "Finish";
        nextEl.parentNode.replaceChild(finishA, nextEl);
      }
    }
  }

  function syncSampleBottomNav(slug, practiceIndex) {
    if (!shouldUseSampleBottomNav()) return;
    var bar = document.getElementById("ccnaSampleSimNav");
    if (!bar) return;

    if (isStaticCcnaSamplePage()) {
      syncStaticSampleBottomNav();
      syncProgressDisplay(slug, practiceIndex);
      return;
    }

    var home = bar.querySelector(".sim-nav-home");
    if (home) home.href = finishHrefForSession();

    syncSampleBottomNavLink(bar, ".ccna-sample-prev, .sim-nav-prev", "a.nav-prev, span.nav-prev", "prev");
    syncSampleBottomNavLink(bar, ".ccna-sample-next", "a.nav-next", "next");

    syncProgressDisplay(slug, practiceIndex);
  }

  function findNextPrevElements() {
    var prevEl = document.querySelector("a.nav-prev");
    var nextEl = document.querySelector("a.nav-next");
    if (prevEl || nextEl) {
      return { nextEl: nextEl, prevEl: prevEl };
    }
    var nextLinks = document.querySelectorAll("a.next-link");
    for (var n = 0; n < nextLinks.length; n++) {
      var t = (nextLinks[n].textContent || "").trim();
      if (/^next/i.test(t)) nextEl = nextLinks[n];
      if (/previous|^back/i.test(t)) prevEl = nextLinks[n];
    }
    return { nextEl: nextEl, prevEl: prevEl };
  }

  /** Refresh Next/Previous from current session (call again after review queue grows). */
  function applyPracticeNav(slug) {
    var session = readSession();
    if (!session) return null;
    var order = session.order;
    var mode = session.mode || "linear";
    var iHint = hashIndex();
    var i = pickIndexForSlug(order, slug, iHint);
    if (i < 0) return null;
    if (i !== iHint) {
      try {
        history.replaceState(null, "", location.pathname + location.search + "#ccnaP=" + i);
      } catch (e) {}
    }

    var els = findNextPrevElements();
    var nextEl = els.nextEl;
    var prevEl = els.prevEl;

    if (nextEl && nextEl.parentNode) {
      var freshNext = nextEl.cloneNode(true);
      nextEl.parentNode.replaceChild(freshNext, nextEl);
      nextEl = freshNext;
    }

    if (nextEl) {
      if (i + 1 < order.length) {
        var ns = order[i + 1];
        nextEl.href = BASE + ns + ".html" + sampleQuerySuffix() + "#ccnaP=" + (i + 1);
        nextEl.textContent = "Next";
      } else {
        nextEl.href = "#";
        nextEl.textContent = "Finish session";
        nextEl.addEventListener(
          "click",
          function (e) {
            e.preventDefault();
            try {
              sessionStorage.removeItem(KEY);
            } catch (x) {}
            window.location.href = finishHrefForSession();
          },
          { once: true }
        );
      }
    }

    if (prevEl) {
      prevEl.style.display = "";
      if (i > 0) {
        var ps = order[i - 1];
        prevEl.href = BASE + ps + ".html" + sampleQuerySuffix() + "#ccnaP=" + (i - 1);
        prevEl.textContent = "Back";
      } else {
        prevEl.style.display = "none";
      }
    }

    if (shouldUseSampleBottomNav()) {
      syncSampleBottomNav(slug, i);
    } else if (readSession()) {
      syncProgressDisplay(slug, i);
    }

    return { mode: mode, i: i, slug: slug };
  }

  function applySampleFallbackNav(slug) {
    ensureSampleBottomNav();
    var els = findNextPrevElements();
    var topNext = els.nextEl;
    var topHome = document.querySelector("a.nav-home");
    if (topHome) topHome.href = finishHrefForSession();
    if (topNext && !readSession()) {
      var href = topNext.getAttribute("href") || "#";
      if (href.indexOf("sample=1") === -1 && href.indexOf(".html") !== -1) {
        topNext.href = href.replace(/\.html(?=[#?]|$)/, ".html?sample=1");
      }
    }
    syncSampleBottomNav(slug, null);
  }

  function getTopicAssignments() {
    var inst = window.CCNA_PRACTICE_100;
    if (inst._topicAssignments && typeof inst._topicAssignments === "object") {
      return Promise.resolve(inst._topicAssignments);
    }
    if (inst._topicAssignments === false) return Promise.resolve(null);
    if (inst._topicAssignmentsPromise && typeof inst._topicAssignmentsPromise.then === "function") {
      return inst._topicAssignmentsPromise.then(function (a) {
        return a && typeof a === "object" ? a : null;
      });
    }
    if (!inst._topicAssignmentsPromiseNav) {
      inst._topicAssignmentsPromiseNav = fetch(TOPIC_MAP_URL, { credentials: "same-origin" })
        .then(function (res) {
          if (!res.ok) throw new Error("topic map http " + res.status);
          return res.json();
        })
        .then(function (data) {
          var a = data && data.assignments;
          var obj = a && typeof a === "object" ? a : {};
          inst._topicAssignments = obj;
          return obj;
        })
        .catch(function () {
          inst._topicAssignments = false;
          return null;
        });
    }
    return inst._topicAssignmentsPromiseNav;
  }

  function getAllSlugs() {
    var inst = window.CCNA_PRACTICE_100;
    if (Array.isArray(inst.ALL_SLUGS) && inst.ALL_SLUGS.length) {
      return Promise.resolve(inst.ALL_SLUGS);
    }
    if (!inst._allSlugsPromiseNav) {
      inst._allSlugsPromiseNav = fetch(MANIFEST_URL, { credentials: "same-origin" })
        .then(function (res) {
          if (!res.ok) throw new Error("manifest http " + res.status);
          return res.json();
        })
        .then(function (data) {
          var items = data && data.items;
          if (!Array.isArray(items)) return [];
          var slugs = [];
          for (var i = 0; i < items.length; i++) {
            if (items[i] && items[i].slug) slugs.push(items[i].slug);
          }
          inst.ALL_SLUGS = slugs;
          return slugs;
        })
        .catch(function () {
          return [];
        });
    }
    return inst._allSlugsPromiseNav;
  }

  function slugMatchesMajor(assignments, slug, major) {
    if (!assignments || !slug) return false;
    var objs = assignments[slug + ".html"];
    if (!objs || !objs.length) return false;
    var want = String(major);
    for (var i = 0; i < objs.length; i++) {
      if (String(objs[i]).split(".")[0] === want) return true;
    }
    return false;
  }

  function hubIndexForSlug(slug, allSlugs) {
    if (!slug || !Array.isArray(allSlugs)) return null;
    for (var i = 0; i < allSlugs.length; i++) {
      if (allSlugs[i] === slug) return i + 1;
    }
    return null;
  }

  function majorsFromMissedObjectives(assignments, missedSlug) {
    if (!assignments || !missedSlug) return [];
    var objs = assignments[missedSlug + ".html"];
    if (!objs || !objs.length) return [];
    var set = {};
    for (var i = 0; i < objs.length; i++) {
      var maj = String(objs[i]).split(".")[0];
      if (/^[1-6]$/.test(maj)) set[maj] = true;
    }
    return Object.keys(set);
  }

  function slugMatchesWeakMajors(assignments, slug, majors) {
    if (!assignments || !majors.length) return false;
    var objs = assignments[slug + ".html"];
    if (!objs || !objs.length) return false;
    for (var i = 0; i < objs.length; i++) {
      var maj = String(objs[i]).split(".")[0];
      if (majors.indexOf(maj) >= 0) return true;
    }
    return false;
  }

  function pickCrossBankAdaptiveSlug(session, missedSlug, assignments, allSlugs) {
    if ((session.adaptiveExtrasInjected || 0) >= ADAPTIVE_CROSS_BANK_CAP) return null;
    var majors = majorsFromMissedObjectives(assignments, missedSlug);
    if (!majors.length) return null;
    if (!Array.isArray(allSlugs) || !allSlugs.length) return null;

    var inOrder = {};
    for (var u = 0; u < session.order.length; u++) inOrder[session.order[u]] = true;

    var domainFilter = session.domain ? String(session.domain) : "";
    var versionFilter = sessionVersionFilter(session);
    var v20Set =
      window.CCNA_PRACTICE_100 && window.CCNA_PRACTICE_100._version20SlugSet
        ? window.CCNA_PRACTICE_100._version20SlugSet
        : null;

    if (session.filtered || versionFilter) {
      var filteredPool = [];
      for (var fj = 0; fj < allSlugs.length; fj++) {
        var fcand = allSlugs[fj];
        if (inOrder[fcand]) continue;
        if (versionFilter === "v20" && !isVersion20Slug(fcand, v20Set)) continue;
        if (versionFilter === "v11" && isVersion20Slug(fcand, v20Set)) continue;
        if (domainFilter && !slugMatchesMajor(assignments, fcand, domainFilter)) continue;
        if (!slugMatchesWeakMajors(assignments, fcand, majors)) continue;
        filteredPool.push(fcand);
      }
      if (!filteredPool.length) return null;
      return filteredPool[Math.floor(Math.random() * filteredPool.length)];
    }

    var bankId = session.bank || "1";
    var n = parseInt(String(bankId), 10);
    if (!n || n < 1) n = 1;
    var bankSize =
      window.CCNA_PRACTICE_100 && window.CCNA_PRACTICE_100.BANK_SIZE
        ? window.CCNA_PRACTICE_100.BANK_SIZE
        : 100;
    var start = (n - 1) * bankSize;
    var bankSlice = allSlugs.slice(start, Math.min(start + bankSize, allSlugs.length));
    var inBank = {};
    for (var bi = 0; bi < bankSlice.length; bi++) inBank[bankSlice[bi]] = true;

    var outsiders = [];
    var insiders = [];
    for (var j = 0; j < allSlugs.length; j++) {
      var cand = allSlugs[j];
      if (inOrder[cand]) continue;
      if (!slugMatchesWeakMajors(assignments, cand, majors)) continue;
      if (domainFilter && !slugMatchesMajor(assignments, cand, domainFilter)) continue;
      if (!inBank[cand]) outsiders.push(cand);
      else insiders.push(cand);
    }
    var pool = outsiders.length ? outsiders : insiders;
    if (!pool.length) return null;
    return pool[Math.floor(Math.random() * pool.length)];
  }

  function run() {
    var slug = slugFromPath();
    if (!slug) return;

    if (shouldUseSampleBottomNav()) {
      ensureSampleBottomNav();
    }

    var nav = applyPracticeNav(slug);
    if (!nav && shouldUseSampleBottomNav()) {
      applySampleFallbackNav(slug);
      initMarkForReview(slug);
      return;
    }
    if (!nav) {
      if (staticSampleQuestionIndex() > 0) {
        syncProgressDisplay(slug, null);
      }
      initMarkForReview(slug);
      return;
    }

    initMarkForReview(slug);

    var s0 = readSession();
    var adaptive = !!(s0 && s0.adaptive);
    if (nav.mode !== "review" && !adaptive) return;

    var box = document.getElementById("answerBox");
    if (!box) return;

    var slugRef = slug;
    var obs = new MutationObserver(function () {
      if (box.classList.contains("correct")) {
        delete box.dataset.ccnaReviewQueued;
        return;
      }
      if (!box.classList.contains("incorrect")) return;
      if (box.dataset.ccnaReviewQueued) return;
      box.dataset.ccnaReviewQueued = "1";

      function finishEnqueue(assignments, allSlugs) {
        try {
          var s2 = readSession();
          if (!s2) return;
          if (s2.mode !== "review" && !s2.adaptive) return;
          var nowI = pickIndexForSlug(s2.order, slugRef, hashIndex());
          if (nowI < 0 || s2.order[nowI] !== slugRef) return;

          var assignObj = assignments && typeof assignments === "object" ? assignments : null;

          if (s2.adaptive && assignObj) {
            var extra = pickCrossBankAdaptiveSlug(s2, slugRef, assignObj, allSlugs || []);
            if (extra) {
              s2.order.push(extra);
              s2.adaptiveExtrasInjected = (s2.adaptiveExtrasInjected || 0) + 1;
            }
          }

          if (s2.mode === "review" || s2.adaptive) {
            s2.order.push(slugRef);
          }
          writeSession(s2);
          applyPracticeNav(slugRef);
          if (shouldUseSampleBottomNav()) {
            var s3 = readSession();
            var idx3 = s3 ? pickIndexForSlug(s3.order, slugRef, hashIndex()) : -1;
            syncSampleBottomNav(slugRef, idx3 >= 0 ? idx3 : null);
          }
        } catch (e2) {}
      }

      var s2head = readSession();
      var useAdaptiveResources = !!(s2head && s2head.adaptive);
      if (useAdaptiveResources) {
        Promise.all([getTopicAssignments(), getAllSlugs()]).then(function (pair) {
          if (!box.classList.contains("incorrect")) return;
          finishEnqueue(pair[0], pair[1]);
        });
      } else {
        finishEnqueue(null, null);
      }
    });
    obs.observe(box, { attributes: true, attributeFilter: ["class"] });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();
