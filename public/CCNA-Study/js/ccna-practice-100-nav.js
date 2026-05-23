(function () {
  "use strict";

  var KEY = "ccnaPractice100";
  var BASE = "/CCNA-Study/CCNA_questions/";
  var finishHref = "/CCNA-Study/CCNA_Training_Portal.html";
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
        nextEl.href = BASE + ns + ".html#ccnaP=" + (i + 1);
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
            window.location.href = finishHref;
          },
          { once: true }
        );
      }
    }

    if (prevEl) {
      prevEl.style.display = "";
      if (i > 0) {
        var ps = order[i - 1];
        prevEl.href = BASE + ps + ".html#ccnaP=" + (i - 1);
        prevEl.textContent = "Back";
      } else {
        prevEl.style.display = "none";
      }
    }

    return { mode: mode, i: i, slug: slug };
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

    var domainFilter = session.domain ? String(session.domain) : "";
    var versionMax = session.versionMax ? parseInt(String(session.versionMax), 10) : 0;

    var outsiders = [];
    var insiders = [];
    for (var j = 0; j < allSlugs.length; j++) {
      var cand = allSlugs[j];
      if (inOrder[cand]) continue;
      if (versionMax && hubIndexForSlug(cand, allSlugs) > versionMax) continue;
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
    var nav = applyPracticeNav(slug);
    if (!nav) return;

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
