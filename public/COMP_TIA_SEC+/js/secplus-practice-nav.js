(function () {
  "use strict";

  var KEY = "secplusPractice";
  var BASE = "/COMP_TIA_SEC+/SEC+_Questions/";
  var PORTAL = "/COMP_TIA_SEC+/SEC+_Training_Portal.html";

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
    return { mode: session.mode || "linear", index: i };
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
    var slug = slugFromPath();
    if (!slug) return;
    var nav = applyPracticeNav(slug);
    if (nav) bindReviewQueue(slug);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();
