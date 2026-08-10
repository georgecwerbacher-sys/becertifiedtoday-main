(function () {
  "use strict";

  var KEY = "secplusHomeSample";
  var INDEX_KEY = "secplusHomeSampleIndex";
  var MCQ_BASE = "/COMP_TIA_SEC+/SEC+_Questions/";
  var HASH_RE = /^#secplusHS=(\d+)$/;
  var FINISH_HOME = "/comptia-sec+-home.html";
  var PBQ_LIBRARY_TOTAL = 34;
  var SCORES_KEY = "pbqScores";
  var suppressHashNav = false;
  var navBooted = false;

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

  function isQuestionsOnlySample(session) {
    if (!session || !Array.isArray(session.order)) return false;
    for (var i = 0; i < session.order.length; i++) {
      if (session.order[i] && session.order[i].type !== "mcq") return false;
    }
    return session.order.length > 0;
  }

  function isSimOnlySample(session) {
    if (!session || !Array.isArray(session.order)) return false;
    for (var i = 0; i < session.order.length; i++) {
      if (session.order[i] && session.order[i].type !== "sim") return false;
    }
    return session.order.length > 0;
  }

  function writeSession(session) {
    try {
      sessionStorage.setItem(KEY, JSON.stringify(session));
    } catch (e) {}
  }

  function isMultiPbqSample(session) {
    return isSimOnlySample(session) && session.order.length > 1;
  }

  function isDarkWebSampleSim(session) {
    if (!isSimOnlySample(session) || !session.order.length) return false;
    if (isMultiPbqSample(session)) return false;
    var item = session.order[0];
    return !!(
      item &&
      item.type === "sim" &&
      normalizePath(item.path).indexOf("dark-web-account-protection") !== -1
    );
  }

  function pbqMetaFromPage(session, index) {
    var item = session.order[index] || {};
    var titleEl = document.querySelector(".pbq-suite-header h1");
    var objEl = document.querySelector(".pbq-suite-objectives");
    var title = (item.shortTitle || item.title || (titleEl && titleEl.textContent) || "PBQ scenario").trim();
    var objectives = (item.objectives || "").trim();
    if (!objectives && objEl) {
      objectives = (objEl.textContent || "")
        .replace(/^covers sy0-701 objectives:\s*/i, "")
        .trim();
    }
    return { title: title, objectives: objectives };
  }

  function readPbqResultFromDom() {
    var passEl = document.querySelector(".result.pass, .result.is-pass, .is-pass[id$='result'], .actions .is-pass");
    var failEl = document.querySelector(".result.fail, .result.is-fail, .is-fail[id$='result'], .actions .is-fail");
    if (passEl) return { checked: true, passed: true };
    if (failEl) return { checked: true, passed: false };
    return { checked: false, passed: null };
  }

  function ensurePbqTimer(session, index) {
    var now = Date.now();
    if (!session.sampleStartedAt) session.sampleStartedAt = now;
    if (session.currentPbqIndex !== index || !session.currentPbqStartedAt) {
      session.currentPbqIndex = index;
      session.currentPbqStartedAt = now;
      writeSession(session);
    }
  }

  function capturePbqScore(session, index) {
    if (!isMultiPbqSample(session) || index < 0 || index >= session.order.length) return;
    ensurePbqTimer(session, index);
    var meta = pbqMetaFromPage(session, index);
    var result = readPbqResultFromDom();
    
    // Auto-check if the user didn't explicitly check their answer yet
    if (!result.checked) {
      var checkBtns = document.querySelectorAll(".actions button");
      for (var i = 0; i < checkBtns.length; i++) {
        if (checkBtns[i].textContent.indexOf("Check") !== -1) {
          checkBtns[i].click();
          break;
        }
      }
      result = readPbqResultFromDom();
    }

    var elapsed = Math.max(0, Date.now() - (session.currentPbqStartedAt || Date.now()));
    if (!Array.isArray(session[SCORES_KEY])) session[SCORES_KEY] = [];
    session[SCORES_KEY][index] = {
      index: index,
      title: meta.title,
      objectives: meta.objectives,
      checked: result.checked,
      passed: result.passed,
      ms: elapsed,
    };
    writeSession(session);
  }

  function formatDuration(ms) {
    var totalSec = Math.max(0, Math.round(ms / 1000));
    var min = Math.floor(totalSec / 60);
    var sec = totalSec % 60;
    if (min <= 0) return sec + "s";
    return min + "m " + sec + "s";
  }

  function pbqScoreRows(session) {
    var rows = [];
    var scores = session[SCORES_KEY] || [];
    for (var i = 0; i < session.order.length; i++) {
      var stored = scores[i];
      var item = session.order[i] || {};
      rows.push(
        stored || {
          index: i,
          title: item.shortTitle || item.title || "PBQ " + (i + 1),
          objectives: item.objectives || "",
          checked: false,
          passed: null,
          ms: 0,
        }
      );
    }
    return rows;
  }

  function pbqNeedsWorkRows(rows) {
    return rows.filter(function (row) {
      return !row.checked || row.passed !== true;
    });
  }

  function remainingPbqCount(session) {
    var tried = session.order.length;
    return Math.max(0, PBQ_LIBRARY_TOTAL - tried);
  }

  function usesMaskedNav(session) {
    return isQuestionsOnlySample(session) || isSimOnlySample(session);
  }

  function sampleMaskBase() {
    try {
      return sessionStorage.getItem("secplusUrlMaskPath") || "/secplus-sample";
    } catch (e) {
      return "/secplus-sample";
    }
  }

  function pathnameForMatch() {
    var path = normalizePath(location.pathname);
    if (path === "/secplus-sample" || path === "/secplus-sample/") {
      try {
        var remembered = sessionStorage.getItem("ccnaLastRealPath");
        if (remembered) return normalizePath(remembered);
      } catch (e) {}
    }
    return path;
  }

  function isSampleContentPage() {
    return document.body.classList.contains("secplus-sample-pbq");
  }

  function rememberRealPathForItem(item) {
    if (!item) return;
    try {
      var path = item.type === "sim" ? item.path : MCQ_BASE + item.slug + ".html";
      sessionStorage.setItem("ccnaLastRealPath", path);
    } catch (e) {}
  }

  function indexFromHashOrStored(session) {
    var hashIdx = hashIndex();
    if (hashIdx >= 0 && hashIdx < session.order.length) return hashIdx;
    return readStoredSampleIndex(session);
  }

  function realItemHref(item, index) {
    var hash = "#secplusHS=" + index;
    if (item.type === "sim") return item.path + hash;
    return MCQ_BASE + item.slug + ".html" + hash;
  }

  function navItemHref(session, item, index) {
    if (usesMaskedNav(session)) {
      return sampleMaskBase() + "#secplusHS=" + index;
    }
    return realItemHref(item, index);
  }

  function wireNavLink(el, session, item, index) {
    if (!el || !item) return;
    if (usesMaskedNav(session)) {
      el.href = navItemHref(session, item, index);
      el.onclick = function (ev) {
        ev.preventDefault();
        persistSampleIndex(index);
        location.assign(realItemHref(item, index));
      };
    } else {
      el.href = realItemHref(item, index);
      el.onclick = function () {
        persistSampleIndex(index);
      };
    }
  }

  function hashIndex() {
    var m = HASH_RE.exec(location.hash || "");
    return m ? parseInt(m[1], 10) : -1;
  }

  function persistSampleIndex(index) {
    if (typeof index !== "number" || index < 0) return;
    try {
      sessionStorage.setItem(INDEX_KEY, String(index));
    } catch (e) {}
  }

  function readStoredSampleIndex(session) {
    try {
      var raw = sessionStorage.getItem(INDEX_KEY);
      if (raw == null || raw === "") return -1;
      var n = parseInt(raw, 10);
      if (isNaN(n) || n < 0 || !session || n >= session.order.length) return -1;
      return n;
    } catch (e) {
      return -1;
    }
  }

  function normalizePath(path) {
    try {
      return decodeURIComponent(path || "").toLowerCase();
    } catch (e) {
      return (path || "").toLowerCase();
    }
  }

  function isSecplusSimStagingPath(path) {
    var p = normalizePath(path);
    return (
      p.indexOf("/sec+_sim_hot_spot/pbq_production/") !== -1 ||
      p.indexOf("/sec+_sim_hot_spot/pending/") !== -1
    );
  }

  function itemMatchesPath(item, path) {
    if (item.type === "sim") {
      var itemPath = normalizePath(item.path);
      if (path === itemPath) return true;
      var slug = itemPath.split("/").pop();
      return !!(slug && path.endsWith("/" + slug));
    }
    return !!(item.slug && path.endsWith("/" + item.slug.toLowerCase() + ".html"));
  }

  function indexForPath(session) {
    var path = pathnameForMatch();
    for (var i = 0; i < session.order.length; i++) {
      if (itemMatchesPath(session.order[i], path)) return i;
    }
    return -1;
  }

  function currentItemIndex(session) {
    var pathIndex = indexForPath(session);
    if (pathIndex >= 0) return pathIndex;

    var hashIdx = hashIndex();
    if (hashIdx >= 0 && hashIdx < session.order.length) return hashIdx;

    return readStoredSampleIndex(session);
  }

  function syncSampleHash(index) {
    if (typeof index !== "number" || index < 0) return;
    if (hashIndex() === index) return;
    try {
      var url = sampleMaskBase() + "#secplusHS=" + index;
      suppressHashNav = true;
      history.replaceState(null, "", url);
    } catch (e) {
      // ignore
    } finally {
      suppressHashNav = false;
    }
  }

  function clearSampleSession() {
    try {
      sessionStorage.removeItem(KEY);
      sessionStorage.removeItem(INDEX_KEY);
      sessionStorage.removeItem("secplusUrlMaskPath");
      sessionStorage.removeItem("secplusSampleKind");
    } catch (e) {}
  }

  function sampleKindLabel() {
    try {
      var kind = sessionStorage.getItem("secplusSampleKind") || "";
      if (kind === "sim-dark-web" || kind === "sim-malware") return "simulation";
      if (kind === "questions") return "questions";
    } catch (e) {}
    return "sample";
  }

  function navigateAfterSample(url) {
    clearSampleSession();
    location.href = url;
  }

  function shouldOfferPortalUpsell(session) {
    return usesMaskedNav(session) && (isQuestionsOnlySample(session) || isSimOnlySample(session));
  }

  function portalUpsellLead(session) {
    var kind = sampleKindLabel();
    var access =
      "Get <strong>30-day full access</strong> for <strong>$19.99</strong>: adaptive review, practice portal modes, and the full timed exam with domain scorecard review - all in your browser.";
    if (isMultiPbqSample(session)) {
      var remaining = remainingPbqCount(session);
      return (
        "You tried <strong>" +
        session.order.length +
        "</strong> of our <strong>" +
        PBQ_LIBRARY_TOTAL +
        " PBQ scenarios</strong>. <strong>" +
        remaining +
        " more are waiting for you to give them a try</strong> - plus <strong>1000+ SY0-701 questions</strong>. " +
        access
      );
    }
    var readiness =
      "<strong>1000+ SY0-701 questions</strong> and <strong>34 PBQ scenarios</strong> are waiting to see if you&rsquo;re ready.";
    if (kind === "simulation" && isDarkWebSampleSim(session)) {
      return (
        "You finished the dark web IR preview (case IR-2024-0847). " +
        readiness +
        " " +
        access
      );
    }
    if (kind === "simulation") {
      return "You finished the performance-based preview. " + readiness + " " + access;
    }
    return "You finished the sample questions. " + readiness + " " + access;
  }

  function showSampleScorecard(session, finishHome) {
    if (document.getElementById("secplusSamplePbqScorecard")) return;

    ensureSampleLeadAnalytics();
    logSecplusSampleEvent("sample_scorecard_shown");

    var rows = pbqScoreRows(session);
    var needsWork = pbqNeedsWorkRows(rows);
    var totalMs = rows.reduce(function (sum, row) {
      return sum + (row.ms || 0);
    }, 0);
    if (session.sampleStartedAt) {
      totalMs = Math.max(totalMs, Date.now() - session.sampleStartedAt);
    }

    var summaryHtml = rows
      .map(function (row) {
        var status;
        if (!row.checked) status = "Not checked";
        else if (row.passed) status = "Correct";
        else status = "Review needed";
        var statusClass = row.passed ? "secplus-sample-scorecard__status--pass" : "secplus-sample-scorecard__status--review";
        if (!row.checked) statusClass = "secplus-sample-scorecard__status--pending";
        return (
          "<li><span class=\"secplus-sample-scorecard__item-title\">" +
          row.title +
          "</span><span class=\"secplus-sample-scorecard__item-meta\">" +
          formatDuration(row.ms || 0) +
          " · SY0-701 " +
          (row.objectives || "objectives") +
          "</span><span class=\"secplus-sample-scorecard__status " +
          statusClass +
          "\">" +
          status +
          "</span></li>"
        );
      })
      .join("");

    var focusHtml;
    if (!needsWork.length) {
      focusHtml =
        "<p class=\"secplus-sample-scorecard-focus__lead\">Strong work on all three preview scenarios. Keep rehearsing under time pressure before exam day.</p>";
    } else {
      focusHtml =
        "<p class=\"secplus-sample-scorecard-focus__lead\">Focus next on these preview scenarios and objectives:</p><ul class=\"secplus-sample-scorecard-focus__list\">" +
        needsWork
          .map(function (row) {
            return (
              "<li><strong>" +
              row.title +
              "</strong>" +
              (row.objectives ? " - objectives " + row.objectives : "") +
              (!row.checked ? " · use Check Answer before moving on" : "") +
              "</li>"
            );
          })
          .join("") +
        "</ul>";
    }

    var root = document.createElement("div");
    root.id = "secplusSamplePbqScorecard";
    root.className = "secplus-sample-scorecard-root";
    root.setAttribute("role", "presentation");
    root.innerHTML =
      '<div class="secplus-sample-scorecard-backdrop" tabindex="-1"></div>' +
      '<div class="secplus-sample-scorecard-panel" role="dialog" aria-modal="true" aria-labelledby="secplusSamplePbqScorecardTitle" tabindex="-1">' +
      '<p class="secplus-sample-scorecard-eyebrow">PBQ preview · 3 of ' +
      PBQ_LIBRARY_TOTAL +
      "</p>" +
      '<h2 id="secplusSamplePbqScorecardTitle">Your sample scorecard</h2>' +
      '<p class="secplus-sample-scorecard-lead">Total time: <strong>' +
      formatDuration(totalMs) +
      "</strong></p>" +
      '<ul class="secplus-sample-scorecard-list">' +
      summaryHtml +
      "</ul>" +
      '<section class="secplus-sample-scorecard-focus" aria-label="Where to focus">' +
      "<h3>Where to focus</h3>" +
      focusHtml +
      "</section>" +
      '<button type="button" class="secplus-sample-scorecard-close">Close scorecard</button>' +
      "</div>";

    document.body.appendChild(root);
    document.body.classList.add("secplus-sample-scorecard-open");

    var panel = root.querySelector(".secplus-sample-scorecard-panel");
    var prevOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    function closeScorecard() {
      root.remove();
      document.body.classList.remove("secplus-sample-scorecard-open");
      document.body.style.overflow = prevOverflow;
      document.removeEventListener("keydown", onKey);
      showPortalUpsellModal(finishHome);
    }

    function onKey(ev) {
      if (ev.key === "Escape") {
        ev.preventDefault();
        closeScorecard();
      }
    }

    document.addEventListener("keydown", onKey);
    root.querySelector(".secplus-sample-scorecard-close").addEventListener("click", closeScorecard);
    if (panel) panel.focus();
  }

  function showPortalUpsellModal(finishHome) {
    if (document.getElementById("secplusSamplePortalUpsell")) return;

    ensureSampleLeadAnalytics();
    logSecplusSampleEvent("sample_finished");

    var session = readSession();
    var purchaseUrl = (finishHome || FINISH_HOME).split("#")[0] + "#purchase";
    var lead = portalUpsellLead(session);

    var root = document.createElement("div");
    root.id = "secplusSamplePortalUpsell";
    root.className = "secplus-sample-upsell-root";
    root.setAttribute("role", "presentation");
    root.innerHTML =
      '<div class="secplus-sample-upsell-backdrop" data-secplus-upsell-dismiss tabindex="-1"></div>' +
      '<div class="secplus-sample-upsell-panel" role="dialog" aria-modal="true" aria-labelledby="secplusSamplePortalUpsellTitle" tabindex="-1">' +
      '<button type="button" class="secplus-sample-upsell-close" data-secplus-upsell-dismiss aria-label="Close dialog">×</button>' +
      '<p class="secplus-sample-upsell-eyebrow">30-day full access · $19.99</p>' +
      '<h2 id="secplusSamplePortalUpsellTitle">Are you ready?</h2>' +
      '<p class="secplus-sample-upsell-lead">' +
      lead +
      "</p>" +
      '<div class="secplus-sample-upsell-actions">' +
      '<button type="button" class="secplus-sample-upsell-primary">Get 30-day access · $19.99</button>' +
      '<button type="button" class="secplus-sample-upsell-secondary" data-secplus-upsell-home>Return to Security+ home</button>' +
      "</div>" +
      "</div>";

    document.body.appendChild(root);
    document.body.classList.add("secplus-sample-upsell-open");

    var panel = root.querySelector(".secplus-sample-upsell-panel");
    var prevOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    function closeModal() {
      root.remove();
      document.body.classList.remove("secplus-sample-upsell-open");
      document.body.style.overflow = prevOverflow;
      document.removeEventListener("keydown", onKey);
    }

    function onKey(ev) {
      if (ev.key === "Escape") {
        ev.preventDefault();
        closeModal();
      }
    }

    document.addEventListener("keydown", onKey);

    root.querySelectorAll("[data-secplus-upsell-dismiss]").forEach(function (el) {
      el.addEventListener("click", closeModal);
    });

    root.querySelector("[data-secplus-upsell-home]").addEventListener("click", function () {
      navigateAfterSample(finishHome || FINISH_HOME);
    });

    root.querySelector(".secplus-sample-upsell-primary").addEventListener("click", function () {
      closeModal();
      navigateAfterSample(purchaseUrl);
    });

    if (panel) panel.focus();
  }

  function completeSample(session, finishHome) {
    if (isMultiPbqSample(session)) {
      var index = currentItemIndex(session);
      if (index < 0) index = session.order.length - 1;
      capturePbqScore(session, index);
      showSampleScorecard(session, finishHome);
      return;
    }
    if (shouldOfferPortalUpsell(session)) {
      showPortalUpsellModal(finishHome);
      return;
    }
    navigateAfterSample(finishHome || FINISH_HOME);
  }

  function logSecplusSampleEvent(event, extra) {
    if (typeof window.bccLogSampleLeadEvent !== "function") return;
    var payload = {
      event: event,
      product: "secplus",
      sampleKind: sampleKindLabel(),
      source: "secplusHomeSample",
    };
    if (extra) {
      for (var k in extra) {
        if (Object.prototype.hasOwnProperty.call(extra, k)) payload[k] = extra[k];
      }
    }
    window.bccLogSampleLeadEvent(payload);
  }

  function ensureSampleLeadAnalytics() {
    if (typeof window.bccLogSampleLeadEvent === "function") return;
    if (document.querySelector('script[src="/js/sample-lead-analytics.js"]')) return;
    var s = document.createElement("script");
    s.src = "/js/sample-lead-analytics.js";
    s.async = true;
    (document.head || document.body).appendChild(s);
  }

  function reconcileLocation(session) {
    var pathIndex = indexForPath(session);
    if (pathIndex >= 0) {
      persistSampleIndex(pathIndex);
      rememberRealPathForItem(session.order[pathIndex]);
      return pathIndex;
    }

    if (isSampleContentPage()) {
      var onPage = indexFromHashOrStored(session);
      if (onPage >= 0) {
        persistSampleIndex(onPage);
        rememberRealPathForItem(session.order[onPage]);
        return onPage;
      }
    }

    var hashIdx = hashIndex();
    if (hashIdx >= 0 && hashIdx < session.order.length) {
      persistSampleIndex(hashIdx);
      location.replace(realItemHref(session.order[hashIdx], hashIdx));
      return -2;
    }

    var stored = readStoredSampleIndex(session);
    if (stored >= 0) {
      persistSampleIndex(stored);
      location.replace(realItemHref(session.order[stored], stored));
      return -2;
    }

    location.replace(realItemHref(session.order[0], 0));
    return -2;
  }

  function itemHref(item, index) {
    return realItemHref(item, index);
  }

  function navigateToSampleItem(session, item, index) {
    if (isMultiPbqSample(session)) {
      var current = currentItemIndex(session);
      if (current >= 0) capturePbqScore(session, current);
    }
    persistSampleIndex(index);
    session.currentPbqIndex = index;
    writeSession(session);
    rememberRealPathForItem(item);
    location.assign(realItemHref(item, index));
  }

  function ensureSimNav(session, index) {
    var item = session.order[index];
    if (!item || item.type !== "sim") return null;

    var multiPbq = isMultiPbqSample(session);
    var nav = document.querySelector("nav.secplus-sample-sim-nav");
    if (!nav) {
      nav = document.createElement("nav");
      nav.className = "secplus-sample-sim-nav";
      nav.setAttribute("aria-label", "Sample navigation");
      var backLink =
        isDarkWebSampleSim(session) && !multiPbq
          ? ""
          : '<a class="secplus-sample-sim-nav__prev" href="#">Back</a>';
      nav.innerHTML =
        '<a class="secplus-sample-sim-nav__home" href="#">Home</a>' +
        backLink +
        '<span class="secplus-sample-sim-nav__progress" aria-live="polite"></span>' +
        '<a class="secplus-sample-sim-nav__next" href="#">Next</a>';
      document.body.appendChild(nav);
    } else if (isDarkWebSampleSim(session) && !multiPbq) {
      var staleBack = nav.querySelector(".secplus-sample-sim-nav__prev");
      if (staleBack) staleBack.remove();
    } else if (multiPbq && !nav.querySelector(".secplus-sample-sim-nav__prev")) {
      var homeEl = nav.querySelector(".secplus-sample-sim-nav__home");
      var progressEl = nav.querySelector(".secplus-sample-sim-nav__progress");
      var nextEl = nav.querySelector(".secplus-sample-sim-nav__next");
      var back = document.createElement("a");
      back.className = "secplus-sample-sim-nav__prev";
      back.href = "#";
      back.textContent = "Back";
      if (progressEl) nav.insertBefore(back, progressEl);
      else if (nextEl) nav.insertBefore(back, nextEl);
      else nav.appendChild(back);
    }

    var finishHome = session.finishHome || FINISH_HOME;
    var homeExit = document.querySelector("a.home-link");
    if (homeExit) {
      if (usesMaskedNav(session)) {
        homeExit.setAttribute("hidden", "");
        homeExit.style.display = "none";
      } else {
        homeExit.removeAttribute("hidden");
        homeExit.style.display = "";
        homeExit.textContent = "Exit sample";
        homeExit.href = finishHome;
        homeExit.classList.add("secplus-sample-exit");
        homeExit.onclick = function () {
          clearSampleSession();
        };
      }
    }

    var deepDiveBtn = document.getElementById("deepDiveBtn");
    if (deepDiveBtn) {
      deepDiveBtn.hidden = false;
      deepDiveBtn.style.display = "";
    }
    if (usesMaskedNav(session)) {
      document.body.classList.add("secplus-home-sample-sim");
    }

    document.querySelectorAll(".site-logo-corner").forEach(function (logo) {
      logo.href = finishHome;
      logo.setAttribute("aria-label", "Return to Security+ home");
      logo.onclick = function () {
        clearSampleSession();
      };
    });

    var portalFooter = document.getElementById("pbqPortalFooter");
    if (portalFooter) portalFooter.hidden = true;

    var homeBar = nav.querySelector(".secplus-sample-sim-nav__home");
    if (homeBar) {
      homeBar.href = finishHome;
      homeBar.onclick = function () {
        clearSampleSession();
      };
    }

    return {
      homeEl: homeBar,
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
        if (isMultiPbqSample(session)) {
          var label = item.shortTitle || item.title || "PBQ scenario";
          els.progressEl.textContent = "PBQ " + (index + 1) + " of " + order.length + " · " + label;
        } else if (isDarkWebSampleSim(session)) {
          els.progressEl.textContent = "BeCertifiedToday.com IR · guest sample";
        } else {
          els.progressEl.textContent = "Simulation - item " + (index + 1) + " of " + order.length;
        }
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

    persistSampleIndex(index);

    if (usesMaskedNav(session)) {
      syncSampleHash(index);
    } else {
      var hashNow = hashIndex();
      if (hashNow !== index) {
        try {
          history.replaceState(null, "", location.pathname + location.search + "#secplusHS=" + index);
        } catch (e) {}
      }
    }

    var finishHome = session.finishHome || FINISH_HOME;
    var maskedNav = usesMaskedNav(session);

    if (els.prevEl && !(isDarkWebSampleSim(session) && !isMultiPbqSample(session))) {
      if (index > 0) {
        if (isMultiPbqSample(session)) {
          els.prevEl.href = navItemHref(session, order[index - 1], index - 1);
          els.prevEl.onclick = function (ev) {
            ev.preventDefault();
            navigateToSampleItem(session, order[index - 1], index - 1);
          };
        } else {
          wireNavLink(els.prevEl, session, order[index - 1], index - 1);
        }
        els.prevEl.textContent = "Back";
        els.prevEl.classList.remove("nav-link--disabled");
        els.prevEl.removeAttribute("aria-hidden");
      } else if (maskedNav) {
        els.prevEl.href = "#";
        els.prevEl.textContent = "Back";
        els.prevEl.classList.add("nav-link--disabled");
        els.prevEl.setAttribute("aria-hidden", "true");
        els.prevEl.onclick = function (ev) {
          ev.preventDefault();
        };
      } else {
        els.prevEl.href = finishHome;
        els.prevEl.textContent = "Home";
        els.prevEl.onclick = function () {
          clearSampleSession();
        };
      }
    }

    if (els.nextEl) {
      if (index + 1 < order.length) {
        if (isMultiPbqSample(session)) {
          els.nextEl.href = navItemHref(session, order[index + 1], index + 1);
          els.nextEl.onclick = function (ev) {
            ev.preventDefault();
            navigateToSampleItem(session, order[index + 1], index + 1);
          };
        } else {
          wireNavLink(els.nextEl, session, order[index + 1], index + 1);
        }
        els.nextEl.textContent = "Next";
        els.nextEl.classList.remove("nav-link--disabled");
        els.nextEl.removeAttribute("aria-hidden");
      } else {
        els.nextEl.href = finishHome;
        els.nextEl.textContent = isMultiPbqSample(session) ? "View scorecard" : "Finish sample";
        els.nextEl.onclick = function (ev) {
          ev.preventDefault();
          completeSample(session, finishHome);
        };
      }
    }

    var home = document.querySelectorAll("a.nav-home");
    home.forEach(function (link) {
      link.href = finishHome;
      link.textContent = "Home";
      link.onclick = function () {
        clearSampleSession();
      };
    });

    document.querySelectorAll(".pbq-portal-footer__home").forEach(function (link) {
      link.href = finishHome;
      link.textContent = "Exit sample";
      link.onclick = function () {
        clearSampleSession();
      };
    });

    if (els.homeEl) {
      els.homeEl.href = finishHome;
      els.homeEl.onclick = function () {
        clearSampleSession();
      };
    }
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
      "body.secplus-home-sample-sim .pbq-suite-footer .question-nav--footer," +
      "body.secplus-home-sample-sim #pbqPortalFooter," +
      "body.secplus-sample-pbq .pbq-suite-footer .question-nav--footer{display:none!important}" +
      "a.home-link.secplus-sample-exit{right:auto;left:14px}" +
      ".secplus-sample-upsell-root{position:fixed;inset:0;z-index:20002;display:flex;align-items:center;justify-content:center;padding:16px}" +
      ".secplus-sample-upsell-backdrop{position:absolute;inset:0;background:rgba(8,12,24,.72);backdrop-filter:blur(4px)}" +
      ".secplus-sample-upsell-panel{position:relative;z-index:1;width:min(520px,100%);max-height:min(90vh,640px);overflow:auto;margin:0;padding:clamp(20px,4vw,28px) clamp(18px,3.5vw,26px) 22px;border-radius:16px;border:1px solid #7c3aed;background:linear-gradient(165deg,rgba(22,32,52,.98) 0%,rgba(14,20,36,.99) 100%);color:#e6edf3;box-shadow:0 24px 64px rgba(0,0,0,.45)}" +
      ".secplus-sample-upsell-close{position:absolute;top:10px;right:12px;border:0;background:transparent;color:#9fb0cc;font-size:1.6rem;line-height:1;cursor:pointer;padding:4px 8px}" +
      ".secplus-sample-upsell-eyebrow{margin:0 0 8px;font-size:.78rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#c4b5fd}" +
      ".secplus-sample-upsell-panel h2{margin:0 0 12px;font-size:clamp(1.15rem,3vw,1.45rem);line-height:1.25;color:#fff}" +
      ".secplus-sample-upsell-lead{margin:0 0 18px;font-size:.95rem;line-height:1.55;color:#cbd5e1}" +
      ".secplus-sample-upsell-actions{display:flex;flex-direction:column;gap:10px}" +
      ".secplus-sample-upsell-primary{display:inline-flex;justify-content:center;align-items:center;text-decoration:none;background:#5b21b6;border:1px solid #7c3aed;color:#f3e8ff;border-radius:10px;padding:12px 18px;font:inherit;font-weight:800;text-align:center;cursor:pointer;width:100%;box-sizing:border-box}" +
      ".secplus-sample-upsell-primary:hover{filter:brightness(1.08)}" +
      ".secplus-sample-upsell-secondary{border:1px solid rgba(159,176,204,.45);background:transparent;color:#e6edf3;border-radius:10px;padding:11px 18px;font:inherit;font-weight:700;cursor:pointer}" +
      ".secplus-sample-upsell-secondary:hover{background:rgba(255,255,255,.06)}" +
      ".secplus-sample-scorecard-root{position:fixed;inset:0;z-index:20001;display:flex;align-items:center;justify-content:center;padding:16px}" +
      ".secplus-sample-scorecard-backdrop{position:absolute;inset:0;background:rgba(8,12,24,.78);backdrop-filter:blur(4px)}" +
      ".secplus-sample-scorecard-panel{position:relative;z-index:1;width:min(560px,100%);max-height:min(92vh,720px);overflow:auto;margin:0;padding:clamp(20px,4vw,28px) clamp(18px,3.5vw,26px) 22px;border-radius:16px;border:1px solid #7c3aed;background:linear-gradient(165deg,rgba(22,32,52,.98) 0%,rgba(14,20,36,.99) 100%);color:#e6edf3;box-shadow:0 24px 64px rgba(0,0,0,.45)}" +
      ".secplus-sample-scorecard-eyebrow{margin:0 0 8px;font-size:.78rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#c4b5fd}" +
      ".secplus-sample-scorecard-panel h2{margin:0 0 10px;font-size:clamp(1.15rem,3vw,1.45rem);line-height:1.25;color:#fff}" +
      ".secplus-sample-scorecard-lead{margin:0 0 14px;font-size:.95rem;color:#cbd5e1}" +
      ".secplus-sample-scorecard-list{list-style:none;margin:0 0 16px;padding:0;display:flex;flex-direction:column;gap:10px}" +
      ".secplus-sample-scorecard-list li{display:grid;grid-template-columns:1fr auto;gap:4px 12px;padding:12px 14px;border:1px solid rgba(124,58,237,.35);border-radius:12px;background:rgba(255,255,255,.03)}" +
      ".secplus-sample-scorecard__item-title{grid-column:1;font-weight:800;color:#fff}" +
      ".secplus-sample-scorecard__item-meta{grid-column:1;font-size:.82rem;color:#9fb0cc}" +
      ".secplus-sample-scorecard__status{grid-column:2;grid-row:1 / span 2;align-self:center;font-size:.78rem;font-weight:800;text-transform:uppercase;letter-spacing:.04em;white-space:nowrap}" +
      ".secplus-sample-scorecard__status--pass{color:#86efac}" +
      ".secplus-sample-scorecard__status--review{color:#fcd34d}" +
      ".secplus-sample-scorecard__status--pending{color:#9fb0cc}" +
      ".secplus-sample-scorecard-focus{margin:0 0 18px;padding-top:4px;border-top:1px solid rgba(124,58,237,.25)}" +
      ".secplus-sample-scorecard-focus h3{margin:0 0 8px;font-size:1rem;color:#fff}" +
      ".secplus-sample-scorecard-focus__lead{margin:0;font-size:.9rem;line-height:1.5;color:#cbd5e1}" +
      ".secplus-sample-scorecard-focus__list{margin:8px 0 0;padding-left:1.1rem;color:#cbd5e1;font-size:.9rem;line-height:1.45}" +
      ".secplus-sample-scorecard-close{display:inline-flex;justify-content:center;align-items:center;width:100%;border:0;background:#5b21b6;border:1px solid #7c3aed;color:#f3e8ff;border-radius:10px;padding:12px 18px;font:inherit;font-weight:800;cursor:pointer;box-sizing:border-box}" +
      ".secplus-sample-scorecard-close:hover{filter:brightness(1.08)}";
    document.head.appendChild(s);
  }

  function isPbqSampleBundleSession(session) {
    if (!isSimOnlySample(session) || !session.order.length) return false;
    for (var i = 0; i < session.order.length; i++) {
      var item = session.order[i];
      if (!item || item.type !== "sim") return false;
      if (normalizePath(item.path).indexOf("/sec+_samples/pbq/") === -1) return false;
    }
    return true;
  }

  function stalePbqBundleSession(session) {
    if (!session || !Array.isArray(session.order)) return false;
    var expected = session.samplePbqBundleCount;
    if (typeof expected !== "number" || expected < 2) expected = 3;

    if (isPbqSampleBundleSession(session)) {
      return session.order.length < expected;
    }

    try {
      if (sessionStorage.getItem("secplusSampleKind") === "sim-dark-web") {
        return session.order.length < expected;
      }
    } catch (e) {}

    return false;
  }

  function run() {
    if (navBooted) return;
    if (isSecplusSimStagingPath(pathnameForMatch())) return;
    var session = readSession();
    if (!session) return;
    if (stalePbqBundleSession(session)) {
      clearSampleSession();
      location.replace("/secplus-sample?track=sim-dark-web");
      return;
    }
    injectStyles();
    var index = reconcileLocation(session);
    if (index < 0) return;
    navBooted = true;
    if (isMultiPbqSample(session)) ensurePbqTimer(session, index);
    applyNav(session, index);
    if (window.bccEnsurePageFeedback) {
      window.bccEnsurePageFeedback();
    } else if (!document.querySelector("script[data-bcc-page-feedback]")) {
      var pf = document.createElement("script");
      pf.src = "/js/page-feedback-widget.js";
      pf.defer = true;
      pf.setAttribute("data-bcc-page-feedback", "1");
      pf.onload = function () {
        if (window.bccEnsurePageFeedback) window.bccEnsurePageFeedback();
      };
      (document.head || document.body).appendChild(pf);
    }
  }

  function onHashChange() {
    if (suppressHashNav) return;
    if (!/^#secplusHS=\d+$/i.test(location.hash || "")) return;
    var session = readSession();
    if (!session || !usesMaskedNav(session)) return;

    var pathIndex = indexForPath(session);
    if (pathIndex >= 0) {
      persistSampleIndex(pathIndex);
      if (isMultiPbqSample(session)) ensurePbqTimer(session, pathIndex);
      applyNav(session, pathIndex);
      return;
    }

    if (isSampleContentPage()) {
      var onPage = indexFromHashOrStored(session);
      if (onPage >= 0) {
        persistSampleIndex(onPage);
        rememberRealPathForItem(session.order[onPage]);
        if (isMultiPbqSample(session)) ensurePbqTimer(session, onPage);
        applyNav(session, onPage);
      }
      return;
    }

    var hint = hashIndex();
    if (hint < 0 || hint >= session.order.length) return;
    persistSampleIndex(hint);
    location.replace(realItemHref(session.order[hint], hint));
  }

  function scheduleRuns() {
    run();
    window.addEventListener("hashchange", onHashChange);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", scheduleRuns, { once: true });
  } else {
    scheduleRuns();
  }
})();
