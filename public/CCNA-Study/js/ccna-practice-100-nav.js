(function () {
  "use strict";

  var KEY = "ccnaPractice100";
  var BASE = "/CCNA-Study/CCNA_questions/";
  var finishHref = "/CCNA-Study/ccna-index.html";

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
    var nextLinks = document.querySelectorAll("a.next-link");
    var nextEl = null;
    var prevEl = null;
    for (var n = 0; n < nextLinks.length; n++) {
      var t = (nextLinks[n].textContent || "").trim();
      if (/next/i.test(t)) nextEl = nextLinks[n];
      if (/previous/i.test(t)) prevEl = nextLinks[n];
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
        nextEl.textContent = "Next question";
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
        prevEl.textContent = "Previous question";
      } else {
        prevEl.style.display = "none";
      }
    }

    return { mode: mode, i: i, slug: slug };
  }

  function run() {
    var slug = slugFromPath();
    if (!slug) return;
    var nav = applyPracticeNav(slug);
    if (!nav) return;

    if (nav.mode !== "review") return;

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
      try {
        var s2 = readSession();
        if (!s2 || s2.mode !== "review") return;
        var nowI = pickIndexForSlug(s2.order, slugRef, hashIndex());
        if (nowI < 0 || s2.order[nowI] !== slugRef) return;
        s2.order.push(slugRef);
        writeSession(s2);
        applyPracticeNav(slugRef);
      } catch (e2) {}
    });
    obs.observe(box, { attributes: true, attributeFilter: ["class"] });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }

})();
