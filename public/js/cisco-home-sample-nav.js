(function () {
  "use strict";

  var ENCOR_DOMAIN_NAMES = {
    "1.0": "Architecture",
    "2.0": "Virtualization",
    "3.0": "Infrastructure",
    "4.0": "Network Assurance",
    "5.0": "Security",
    "6.0": "Automation and Artificial Intelligence",
  };

  var CCNA_DOMAIN_NAMES = {
    "1.0": "Network Fundamentals",
    "2.0": "Network Access",
    "3.0": "IP Connectivity",
    "4.0": "IP Services",
    "5.0": "Security Fundamentals",
    "6.0": "Automation and Programmability",
  };

  var SESSIONS = {
    ccna: {
      key: "ccnaHomeSample",
      hashRe: /^#ccnaHS=(\d+)$/,
      hashPrefix: "ccnaHS=",
      maskPath: "/sample",
      storageScript: "/js/ccna-free-assessment-storage.js",
      leadScript: "/js/ccna-lead-capture.js",
      showLeadModal: function () {
        return window.showCcnaFreeSimLeadModal;
      },
      productLabel: "CCNA",
      examLabel: "200-301",
    },
    encor: {
      key: "encorHomeSample",
      hashRe: /^#encorHS=(\d+)$/,
      hashPrefix: "encorHS=",
      maskPath: "/sample",
      storageScript: "/CCNP-ENCOR-Study/js/encor-test-sim-storage.js",
      leadScript: "/js/encor-lead-capture.js",
      showLeadModal: function () {
        return window.showEncorFreeSimLeadModal;
      },
      productLabel: "ENCOR",
      examLabel: "350-401",
    },
  };

  function readSession(cfg) {
    try {
      var raw = sessionStorage.getItem(cfg.key);
      if (!raw) return null;
      var s = JSON.parse(raw);
      if (!s || !Array.isArray(s.order) || !s.order.length) return null;
      s._cfg = cfg;
      return s;
    } catch (e) {
      return null;
    }
  }

  function sampleKindHint() {
    try {
      return sessionStorage.getItem("ccnpSampleKind") || "";
    } catch (e) {
      return "";
    }
  }

  function isCcnaSamplePath(path) {
    return (
      path.indexOf("/ccna-study/") !== -1 || path.indexOf("/ccna_sim_exam/") !== -1
    );
  }

  function isEncorSamplePath(path) {
    return path.indexOf("/ccnp-encor-study/") !== -1;
  }

  function isEncorSampleKind(kind) {
    return kind.indexOf("encor") === 0 || kind === "labs" || kind === "drag";
  }

  function resolveLeadConfig(session) {
    if (!session) return SESSIONS.ccna;
    if (session.product === "encor") return SESSIONS.encor;
    if (session.product === "ccna") return SESSIONS.ccna;

    var path = pathnameForMatch();
    if (isCcnaSamplePath(path)) return SESSIONS.ccna;
    if (isEncorSamplePath(path)) return SESSIONS.encor;

    var kind = sampleKindHint();
    if (kind.indexOf("ccna") === 0) return SESSIONS.ccna;
    if (isEncorSampleKind(kind)) return SESSIONS.encor;

    if (session._cfg) return session._cfg;
    if (isEncorSamplePath(path)) return SESSIONS.encor;
    return SESSIONS.ccna;
  }

  function activeSessionConfig() {
    var ccna = readSession(SESSIONS.ccna);
    var encor = readSession(SESSIONS.encor);
    var path = pathnameForMatch();
    var kind = sampleKindHint();

    if (isCcnaSamplePath(path) && ccna) return ccna;
    if (isEncorSamplePath(path) && encor) return encor;

    if (kind.indexOf("ccna") === 0 && ccna) return ccna;
    if (isEncorSampleKind(kind) && encor) return encor;

    if (isEncorSamplePath(path)) return encor || ccna;
    if (isCcnaSamplePath(path)) return ccna || encor;

    if (ccna) return ccna;
    return encor;
  }

  function isSingleTrackSample(session) {
    if (!session || !Array.isArray(session.order)) return false;
    var t = session.order[0] && session.order[0].type;
    for (var i = 0; i < session.order.length; i++) {
      if (session.order[i] && session.order[i].type !== t) return false;
    }
    return session.order.length > 0;
  }

  function sampleMaskBase(session) {
    try {
      return sessionStorage.getItem("ccnpUrlMaskPath") || session._cfg.maskPath;
    } catch (e) {
      return session._cfg.maskPath;
    }
  }

  function pathnameForMatch() {
    var path = normalizePath(location.pathname);
    if (path === "/sample" || path === "/sample/") {
      try {
        var remembered = sessionStorage.getItem("ccnaLastRealPath");
        if (remembered) return normalizePath(remembered);
      } catch (e) {}
    }
    return path;
  }

  function normalizePath(path) {
    try {
      return decodeURIComponent(path || "").toLowerCase();
    } catch (e) {
      return (path || "").toLowerCase();
    }
  }

  function realItemHref(session, item, index) {
    var hash = "#" + session._cfg.hashPrefix + index;
    if (item.type === "mcq" && item.slug) {
      return "/CCNA-Study/CCNA_questions/" + item.slug + ".html?sample=1" + hash;
    }
    if (item.type === "mcq" && item.id != null) {
      return (
        "/CCNP-ENCOR-Study/ENCOR_Questions/question-" +
        item.id +
        ".html?sample=1" +
        hash
      );
    }
    return item.path + (item.path.indexOf("?") >= 0 ? "&" : "?") + "sample=1" + hash;
  }

  function itemMatchesPath(item, path) {
    if (item.type === "lab" || item.type === "dnd") {
      return path === normalizePath(item.path);
    }
    if (item.slug) return path.endsWith("/" + item.slug.toLowerCase() + ".html");
    if (item.id != null) return path.endsWith("/question-" + item.id + ".html");
    return false;
  }

  function hashIndex(session) {
    var m = session._cfg.hashRe.exec(location.hash || "");
    return m ? parseInt(m[1], 10) : 0;
  }

  function currentItemIndex(session) {
    var path = pathnameForMatch();
    for (var i = 0; i < session.order.length; i++) {
      if (itemMatchesPath(session.order[i], path)) return i;
    }
    var hint = hashIndex(session);
    if (hint >= 0 && hint < session.order.length) return hint;
    return -1;
  }

  function saveSampleSession(session) {
    if (!session || !session._cfg) return;
    try {
      sessionStorage.setItem(session._cfg.key, JSON.stringify(session));
    } catch (e) {}
  }

  function clearSampleSession(session) {
    try {
      sessionStorage.removeItem(session._cfg.key);
      sessionStorage.removeItem("ccnpUrlMaskPath");
      sessionStorage.removeItem("ccnpSampleKind");
    } catch (e) {}
  }

  function ensureSampleResults(session) {
    if (!session.sampleResults || typeof session.sampleResults !== "object") {
      session.sampleResults = {};
    }
    return session.sampleResults;
  }

  function domainLabel(session, domainId, domainName) {
    if (domainName) return domainId + " " + domainName;
    var names = session.product === "ccna" ? CCNA_DOMAIN_NAMES : ENCOR_DOMAIN_NAMES;
    var label = names[domainId] || "";
    return domainId + (label ? " " + label : "");
  }

  function captureCurrentAnswer(session, index) {
    var item = session.order[index];
    if (!item || item.type !== "mcq") return;

    var results = ensureSampleResults(session);
    var box = document.getElementById("answerBox");
    var status = "unanswered";
    if (box && box.style.display !== "none") {
      if (box.classList.contains("correct")) status = "correct";
      else if (box.classList.contains("incorrect")) status = "incorrect";
    }

    results[String(index)] = {
      status: status,
      domain: item.domain || "",
      domainName: item.domainName || "",
    };
    saveSampleSession(session);
  }

  function finalizeSampleResults(session) {
    session.order.forEach(function (item, index) {
      if (!item || item.type !== "mcq") return;
      var results = ensureSampleResults(session);
      if (!results[String(index)]) {
        results[String(index)] = {
          status: "unanswered",
          domain: item.domain || "",
          domainName: item.domainName || "",
        };
      }
    });
    saveSampleSession(session);
  }

  function buildSampleScoreSummary(session) {
    var results = ensureSampleResults(session);
    var totals = { correct: 0, incorrect: 0, unanswered: 0, total: 0 };
    var byDomain = Object.create(null);

    session.order.forEach(function (item, index) {
      if (!item || item.type !== "mcq") return;
      totals.total++;
      var row = results[String(index)] || { status: "unanswered", domain: item.domain, domainName: item.domainName };
      if (row.status === "correct") totals.correct++;
      else if (row.status === "incorrect") totals.incorrect++;
      else totals.unanswered++;

      var domainId = row.domain || item.domain || "other";
      if (!byDomain[domainId]) {
        byDomain[domainId] = {
          domain: domainId,
          domainName: row.domainName || item.domainName || "",
          correct: 0,
          incorrect: 0,
          unanswered: 0,
          total: 0,
        };
      }
      byDomain[domainId].total++;
      if (row.status === "correct") byDomain[domainId].correct++;
      else if (row.status === "incorrect") byDomain[domainId].incorrect++;
      else byDomain[domainId].unanswered++;
    });

    var domainRows = Object.keys(byDomain)
      .map(function (k) {
        return byDomain[k];
      })
      .sort(function (a, b) {
        return parseFloat(a.domain) - parseFloat(b.domain);
      });

    return { totals: totals, domainRows: domainRows };
  }

  function showSampleScorecard(session, finishHome) {
    if (document.getElementById("ciscoSampleScorecard")) return;

    finalizeSampleResults(session);
    var summary = buildSampleScoreSummary(session);
    var totals = summary.totals;
    var pct = totals.total ? Math.round((totals.correct / totals.total) * 100) : 0;
    var examLabel = session.product === "ccna" ? "CCNA 200-301" : "ENCOR 350-401";

    var domainRowsHtml = summary.domainRows
      .map(function (row) {
        var rowPct = row.total ? Math.round((row.correct / row.total) * 100) : 0;
        return (
          "<tr><th scope=\"row\">" +
          domainLabel(session, row.domain, row.domainName) +
          "</th><td>" +
          row.correct +
          "/" +
          row.total +
          " (" +
          rowPct +
          "%)</td><td>" +
          (row.incorrect ? row.incorrect + " missed" : "—") +
          (row.unanswered ? (row.incorrect ? ", " : "") + row.unanswered + " unanswered" : "") +
          "</td></tr>"
        );
      })
      .join("");

    var root = document.createElement("div");
    root.id = "ciscoSampleScorecard";
    root.className = "cisco-sample-scorecard-root";
    root.innerHTML =
      '<div class="cisco-sample-scorecard-backdrop" data-cisco-scorecard-dismiss tabindex="-1"></div>' +
      '<div class="cisco-sample-scorecard-panel" role="dialog" aria-modal="true" aria-labelledby="ciscoSampleScorecardTitle" tabindex="-1">' +
      '<button type="button" class="cisco-sample-scorecard-close" data-cisco-scorecard-dismiss aria-label="Close scorecard">×</button>' +
      '<p class="cisco-sample-scorecard-eyebrow">Sample complete</p>' +
      '<h2 id="ciscoSampleScorecardTitle">' +
      examLabel +
      " sample scorecard</h2>" +
      '<p class="cisco-sample-scorecard-score"><strong>' +
      totals.correct +
      "/" +
      totals.total +
      "</strong> correct (" +
      pct +
      "%)</p>" +
      '<p class="cisco-sample-scorecard-lead">You answered ' +
      totals.total +
      " multiple-choice items across the exam domains. Use the breakdown below to see where to review next.</p>" +
      '<div class="cisco-sample-scorecard-table-wrap"><table><thead><tr><th scope="col">Domain</th><th scope="col">Score</th><th scope="col">Notes</th></tr></thead><tbody>' +
      domainRowsHtml +
      "</tbody></table></div>" +
      '<div class="cisco-sample-scorecard-actions">' +
      '<button type="button" class="cisco-sample-scorecard-primary" data-cisco-scorecard-home>Return to home</button>' +
      "</div></div>";

    document.body.appendChild(root);
    document.body.classList.add("cisco-sample-scorecard-open");

    var panel = root.querySelector(".cisco-sample-scorecard-panel");
    var prevOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    function closeScorecard(navigateHome) {
      root.remove();
      document.body.classList.remove("cisco-sample-scorecard-open");
      document.body.style.overflow = prevOverflow;
      document.removeEventListener("keydown", onKey);
      if (navigateHome) navigateAfterSample(finishHome, session);
    }

    function onKey(ev) {
      if (ev.key === "Escape") {
        ev.preventDefault();
        closeScorecard(false);
      }
    }

    document.addEventListener("keydown", onKey);
    root.querySelectorAll("[data-cisco-scorecard-dismiss]").forEach(function (el) {
      el.addEventListener("click", function () {
        closeScorecard(false);
      });
    });
    root.querySelector("[data-cisco-scorecard-home]").addEventListener("click", function () {
      closeScorecard(true);
    });
    if (panel) panel.focus();
  }

  function wireAnswerCapture(session, index) {
    var checkBtn = document.getElementById("checkBtn");
    if (!checkBtn || checkBtn.getAttribute("data-cisco-sample-wired") === "1") return;
    checkBtn.setAttribute("data-cisco-sample-wired", "1");
    checkBtn.addEventListener("click", function () {
      window.setTimeout(function () {
        captureCurrentAnswer(session, index);
      }, 0);
    });
  }

  function isMcqOnlySample(session) {
    return (
      session &&
      Array.isArray(session.order) &&
      session.order.length > 0 &&
      session.order.every(function (item) {
        return item && item.type === "mcq";
      })
    );
  }

  function navigateAfterSample(url, session) {
    clearSampleSession(session);
    location.href = url;
  }

  function loadScriptOnce(src, onLoad, onError) {
    var existing = document.querySelector('script[src="' + src + '"]');
    if (existing) {
      if (existing.getAttribute("data-bcc-loaded") === "1") {
        onLoad();
        return;
      }
      existing.addEventListener("load", onLoad, { once: true });
      existing.addEventListener("error", onError, { once: true });
      return;
    }
    var s = document.createElement("script");
    s.src = src;
    s.onload = function () {
      s.setAttribute("data-bcc-loaded", "1");
      onLoad();
    };
    s.onerror = onError;
    (document.body || document.head).appendChild(s);
  }

  function loadLeadCapture(session, callback) {
    var cfg = resolveLeadConfig(session);

    function invoke() {
      callback(cfg);
    }

    var show = cfg.showLeadModal();
    if (typeof show === "function") {
      invoke();
      return;
    }

    function loadLeadScript() {
      loadScriptOnce(
        cfg.leadScript,
        invoke,
        function () {
          navigateAfterSample(
            (session.finishHome || "/") + (session.leadCaptureHash || ""),
            session
          );
        }
      );
    }

    if (cfg.storageScript) {
      loadScriptOnce(cfg.storageScript, loadLeadScript, loadLeadScript);
      return;
    }

    loadLeadScript();
  }

  function openFreeSimLeadModal(session, finishHome) {
    logSampleEvent(session, "email_modal_open");
    loadLeadCapture(session, function (cfg) {
      var show = cfg.showLeadModal();
      if (typeof show !== "function") {
        navigateAfterSample(
          finishHome + (session.leadCaptureHash || ""),
          session
        );
        return;
      }
      var kind =
        session.order[0] && session.order[0].type === "lab"
          ? "lab"
          : session.order[0] && session.order[0].type === "dnd"
            ? "dnd"
            : "questions";
      show({
        finishHome: finishHome,
        method: cfg.key + "_sample_popup",
        sampleKind: kind,
        onBeforeNavigate: function () {
          clearSampleSession(session);
        },
      });
    });
  }

  function logSampleEvent(session, event, extra) {
    if (typeof window.bccLogSampleLeadEvent !== "function" || !session) return;
    var product = session.product === "encor" ? "encor" : "ccna";
    var kind =
      session.order[0] && session.order[0].type === "lab"
        ? "lab"
        : session.order[0] && session.order[0].type === "dnd"
          ? "dnd"
          : "questions";
    var payload = {
      event: event,
      product: product,
      sampleKind: kind,
      source: (session._cfg && session._cfg.key) || "",
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

  var CCNA_LIBRARY_STATS = {
    questions: "700+",
    labs: "9",
    dnd: "99",
  };

  var CCNA_PORTAL_CHECKOUT = {
    "10d": {
      url: "https://buy.stripe.com/00wcN458x6Szglq6Ruc3m04",
      id: "ccna_portal_10d",
      name: "CCNA 10-day access",
      value: "9.99",
      label: "Get 10-day access · $9.99",
      sub: "10 days · one-time",
    },
    "30d": {
      url: "https://buy.stripe.com/14A7sK58xccT4CI8ZCc3m03",
      id: "ccna_portal_30d",
      name: "CCNA 30-day access",
      value: "19.99",
      label: "Get 30-day access · $19.99",
      sub: "30 days · one-time",
    },
  };

  function hasCcnaPortalAccess() {
    return (
      typeof window.bccPortalAccessActive === "function" && window.bccPortalAccessActive()
    );
  }

  function detectCcnaSampleKind(session) {
    var kind = sampleKindHint();
    if (kind === "ccna-questions") return "questions";
    if (kind === "ccna-dnd") return "dnd";
    if (kind === "ccna-lab" || kind === "ccna-vlan" || kind === "ccna-trunk") return "lab";
    if (!session || !Array.isArray(session.order) || !session.order.length) return "questions";
    var t = session.order[0].type;
    if (t === "lab") return "lab";
    if (t === "dnd") return "dnd";
    return "questions";
  }

  function ccnaPortalOfferLead(session, kind) {
    var q = CCNA_LIBRARY_STATS.questions;
    var labs = CCNA_LIBRARY_STATS.labs;
    var dnd = CCNA_LIBRARY_STATS.dnd;
    if (kind === "lab") {
      return (
        "You finished the sample CLI lab. Unlock <strong>" +
        labs +
        " browser CLI lab simulations</strong>—the same interactive format you just used—plus <strong>" +
        q +
        " practice questions</strong> and <strong>" +
        dnd +
        " drag-and-drop</strong> items with verified explanations."
      );
    }
    if (kind === "dnd") {
      return (
        "You finished the sample drag-and-drop set. Unlock <strong>" +
        dnd +
        " performance-style drag-and-drop</strong> items plus <strong>" +
        q +
        " practice questions</strong> and <strong>" +
        labs +
        " CLI labs</strong>—all in your browser on phone, tablet, or desktop."
      );
    }
    return (
      "You finished the sample questions. Unlock <strong>" +
      q +
      " CCNA 200-301 practice questions</strong> with verified explanations, plus <strong>" +
      labs +
      " CLI labs</strong>, <strong>" +
      dnd +
      " drag-and-drop</strong> sets, and timed simulation practice."
    );
  }

  function wireCcnaPortalCheckoutBtn(btn, tier, session) {
    var product = CCNA_PORTAL_CHECKOUT[tier];
    if (!product || !btn) return;
    btn.type = "button";
    btn.className = "cisco-ccna-offer-tier-btn" + (tier === "10d" ? " cisco-ccna-offer-tier-btn--featured" : "");
    btn.textContent = product.label;
    btn.setAttribute("data-ccna-portal-checkout-tier", tier);
    btn.addEventListener("click", function (ev) {
      ev.preventDefault();
      if (btn.dataset.loading === "1") return;
      logSampleEvent(session, "ccna_portal_offer_checkout", { tier: tier });
      if (typeof window.bccTrackBeginCheckout === "function") {
        btn.setAttribute("data-bcc-item-id", product.id);
        btn.setAttribute("data-bcc-item-name", product.name);
        btn.setAttribute("data-bcc-value", product.value);
        btn.setAttribute("data-bcc-currency", "USD");
        window.bccTrackBeginCheckout(btn);
      }
      btn.dataset.loading = "1";
      btn.disabled = true;
      btn.textContent = "Redirecting…";
      clearSampleSession(session);
      window.location.href = product.url;
    });
  }

  function showCcnaPortalOfferModal(session, finishHome) {
    if (document.getElementById("ciscoCcnaPortalOffer")) return;

    ensureSampleLeadAnalytics();
    finalizeSampleResults(session);

    var kind = detectCcnaSampleKind(session);
    logSampleEvent(session, "ccna_portal_offer_shown", { sampleKind: kind });

    var lead = ccnaPortalOfferLead(session, kind);
    var scoreHtml = "";
    if (kind === "questions") {
      var summary = buildSampleScoreSummary(session);
      var totals = summary.totals;
      if (totals.total) {
        var pct = Math.round((totals.correct / totals.total) * 100);
        scoreHtml =
          '<p class="cisco-ccna-offer-score"><strong>' +
          totals.correct +
          "/" +
          totals.total +
          "</strong> correct on this sample (" +
          pct +
          "%)</p>";
      }
    }

    var title =
      kind === "lab"
        ? "Ready for the full CCNA lab library?"
        : kind === "dnd"
          ? "Ready for the full drag-and-drop bank?"
          : "Ready for the full CCNA question bank?";

    var root = document.createElement("div");
    root.id = "ciscoCcnaPortalOffer";
    root.className = "cisco-ccna-offer-root";
    root.setAttribute("role", "presentation");
    root.innerHTML =
      '<div class="cisco-ccna-offer-backdrop" data-cisco-ccna-offer-dismiss tabindex="-1"></div>' +
      '<div class="cisco-ccna-offer-panel" role="dialog" aria-modal="true" aria-labelledby="ciscoCcnaPortalOfferTitle" tabindex="-1">' +
      '<button type="button" class="cisco-ccna-offer-close" data-cisco-ccna-offer-dismiss aria-label="Close dialog">×</button>' +
      '<p class="cisco-ccna-offer-eyebrow">Sample complete · CCNA 200-301</p>' +
      '<h2 id="ciscoCcnaPortalOfferTitle">' +
      title +
      "</h2>" +
      scoreHtml +
      '<p class="cisco-ccna-offer-lead">' +
      lead +
      "</p>" +
      '<p class="cisco-ccna-offer-tagline">Practice like test day. Walk in ready.</p>' +
      '<div class="cisco-ccna-offer-tiers" aria-label="CCNA access options">' +
      '<div class="cisco-ccna-offer-tier cisco-ccna-offer-tier--featured">' +
      '<p class="cisco-ccna-offer-tier-label">10-day full access</p>' +
      '<p class="cisco-ccna-offer-tier-price">$9.99 <span>/ 10 days</span></p>' +
      '<p class="cisco-ccna-offer-tier-note">One-time · no subscription</p>' +
      '<button type="button" class="cisco-ccna-offer-tier-btn cisco-ccna-offer-tier-btn--featured" data-tier="10d"></button>' +
      "</div>" +
      '<div class="cisco-ccna-offer-tier">' +
      '<p class="cisco-ccna-offer-tier-label">30-day full access</p>' +
      '<p class="cisco-ccna-offer-tier-price">$19.99 <span>/ 30 days</span></p>' +
      '<p class="cisco-ccna-offer-tier-note">Same library · longer study window</p>' +
      '<button type="button" class="cisco-ccna-offer-tier-btn" data-tier="30d"></button>' +
      "</div>" +
      "</div>" +
      '<div class="cisco-ccna-offer-actions">' +
      '<button type="button" class="cisco-ccna-offer-secondary" data-cisco-ccna-offer-home>Return to CCNA home</button>' +
      "</div>" +
      "</div>";

    document.body.appendChild(root);
    document.body.classList.add("cisco-ccna-offer-open");

    wireCcnaPortalCheckoutBtn(root.querySelector('[data-tier="10d"]'), "10d", session);
    wireCcnaPortalCheckoutBtn(root.querySelector('[data-tier="30d"]'), "30d", session);

    var panel = root.querySelector(".cisco-ccna-offer-panel");
    var prevOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    var homeUrl = (finishHome || session.finishHome || "/ccna-home.html") + "#purchase";

    function closeModal(navigateHome) {
      root.remove();
      document.body.classList.remove("cisco-ccna-offer-open");
      document.body.style.overflow = prevOverflow;
      document.removeEventListener("keydown", onKey);
      if (navigateHome) navigateAfterSample(homeUrl, session);
    }

    function onKey(ev) {
      if (ev.key === "Escape") {
        ev.preventDefault();
        closeModal(false);
      }
    }

    document.addEventListener("keydown", onKey);
    root.querySelectorAll("[data-cisco-ccna-offer-dismiss]").forEach(function (el) {
      el.addEventListener("click", function () {
        closeModal(false);
      });
    });
    root.querySelector("[data-cisco-ccna-offer-home]").addEventListener("click", function () {
      logSampleEvent(session, "ccna_portal_offer_dismiss", { action: "home" });
      closeModal(true);
    });

    if (panel) panel.focus();
  }

  function isDragDropSampleItem(item) {
    return !!(item && item.type === "dnd");
  }

  function completeSample(session, finishHome) {
    var home = finishHome || session.finishHome;
    var index = currentItemIndex(session);
    if (index >= 0) captureCurrentAnswer(session, index);

    var isCcna =
      session.product === "ccna" ||
      resolveLeadConfig(session).key === SESSIONS.ccna.key ||
      sampleKindHint().indexOf("ccna") === 0;

    if (isCcna && !hasCcnaPortalAccess()) {
      showCcnaPortalOfferModal(session, home);
      return;
    }

    if (isMcqOnlySample(session)) {
      showSampleScorecard(session, home);
      return;
    }
    navigateAfterSample(home, session);
  }

  function wireNavLink(el, session, item, index) {
    if (!el || !item) return;
    if (isSingleTrackSample(session)) {
      el.href = sampleMaskBase(session) + "#" + session._cfg.hashPrefix + index;
      el.onclick = function (ev) {
        ev.preventDefault();
        location.assign(realItemHref(session, item, index));
      };
    } else {
      el.href = realItemHref(session, item, index);
      el.onclick = null;
    }
  }

  function ensureBottomNav(session, index) {
    var nav = document.querySelector("nav.cisco-home-sample-nav");
    if (!nav) {
      nav = document.createElement("nav");
      nav.className = "cisco-home-sample-nav";
      nav.setAttribute("aria-label", "Sample navigation");
      nav.innerHTML =
        '<span class="cisco-home-sample-nav__progress" aria-live="polite"></span>' +
        '<div class="cisco-home-sample-nav__actions">' +
        '<a class="cisco-home-sample-nav__home" href="#">Home</a>' +
        '<a class="cisco-home-sample-nav__prev" href="#">Back</a>' +
        '<a class="cisco-home-sample-nav__next" href="#">Next</a>' +
        "</div>";
      document.body.appendChild(nav);
      document.body.classList.add("cisco-home-sample-active");
    }

    var finishHome = session.finishHome;
    var homeExit = document.querySelector("a.home-link");
    if (homeExit) {
      homeExit.setAttribute("hidden", "");
      homeExit.style.display = "none";
    }

    var topNav = document.querySelector("nav.question-nav");
    if (topNav) topNav.style.display = "none";

    return {
      homeEl: nav.querySelector(".cisco-home-sample-nav__home"),
      prevEl: nav.querySelector(".cisco-home-sample-nav__prev"),
      nextEl: nav.querySelector(".cisco-home-sample-nav__next"),
      progressEl: nav.querySelector(".cisco-home-sample-nav__progress"),
    };
  }

  function findMcqNav() {
    return {
      prevEl: document.querySelector("a.nav-prev"),
      nextEl: document.querySelector("a.nav-next"),
      progressEl: document.querySelector(".cisco-sample-progress"),
    };
  }

  function ensureMcqProgress(host) {
    if (!host || host.querySelector(".cisco-sample-progress")) {
      return host && host.querySelector(".cisco-sample-progress");
    }
    var el = document.createElement("span");
    el.className = "cisco-sample-progress";
    el.setAttribute("aria-live", "polite");
    host.insertBefore(el, host.firstChild);
    return el;
  }

  function formatEncorDomainLabel(domainId) {
    var name = ENCOR_DOMAIN_NAMES[domainId] || "";
    return domainId + (name ? " " + name : "");
  }

  function domainsFromEncorOrder(order) {
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

  function ensureSampleSubjectsFooter(session) {
    var card = document.querySelector("main.card") || document.querySelector(".card");
    if (!card) return null;
    var footer = card.querySelector(".sample-subjects-footer");
    if (!footer) {
      footer = document.createElement("div");
      footer.className = "sample-subjects-footer";
      footer.setAttribute("aria-label", "350-401 domains in this sample");
      var title = document.createElement("p");
      title.className = "sample-subjects-footer__title";
      title.textContent = "350-401 domains in this sample";
      footer.appendChild(title);
      var list = document.createElement("ul");
      list.className = "sample-subjects-footer__list";
      footer.appendChild(list);
      card.appendChild(footer);
    }
    return footer.querySelector(".sample-subjects-footer__list");
  }

  function syncSampleSubjectsFooter(session) {
    if (!session || (session.product !== "encor" && session.product !== "ccna")) {
      var stale = document.querySelector(".sample-subjects-footer");
      if (stale) stale.remove();
      return;
    }
    if (
      !session.order ||
      !session.order.every(function (item) {
        return item && item.type === "mcq";
      })
    ) {
      return;
    }

    var listEl = ensureSampleSubjectsFooter(session);
    if (!listEl) return;

    var title = listEl.parentNode && listEl.parentNode.querySelector(".sample-subjects-footer__title");
    if (title) {
      title.textContent =
        session.product === "ccna"
          ? "200-301 domains in this sample"
          : "350-401 domains in this sample";
    }

    var domains =
      Array.isArray(session.sampleDomains) && session.sampleDomains.length
        ? session.sampleDomains
        : domainsFromEncorOrder(session.order);
    listEl.textContent = "";
    domains.forEach(function (domainId) {
      var li = document.createElement("li");
      if (session.product === "ccna") {
        li.textContent = domainLabel(session, domainId, CCNA_DOMAIN_NAMES[domainId]);
      } else {
        li.textContent = formatEncorDomainLabel(domainId);
      }
      listEl.appendChild(li);
    });
  }

  function applyNav(session, index) {
    var order = session.order;
    var isLabOrDnd = order[index] && (order[index].type === "lab" || order[index].type === "dnd");
    var els = isLabOrDnd ? ensureBottomNav(session, index) : findMcqNav();

    if (!els) return;

    if (!isLabOrDnd) {
      ensureMcqProgress(document.querySelector("nav.question-nav"));
      els.progressEl = document.querySelector(".cisco-sample-progress");
    }

    if (els.progressEl) {
      var item = order[index];
      if (item && (item.type === "lab" || item.type === "dnd")) {
        els.progressEl.textContent =
          (item.type === "lab" ? "Lab" : "Drag-and-drop") +
          " — item " +
          (index + 1) +
          " of " +
          order.length;
      } else {
        var mcqNum = 0;
        for (var p = 0; p <= index; p++) {
          if (order[p] && order[p].type === "mcq") mcqNum++;
        }
        els.progressEl.textContent = "Question " + mcqNum + " of " + session.mcqCount;
      }
      var encorFooterProgress = document.querySelector(".ccna-practice-progress");
      if (encorFooterProgress && els.progressEl) {
        encorFooterProgress.textContent = els.progressEl.textContent;
      }
    }

    if (index !== hashIndex(session)) {
      try {
        history.replaceState(
          null,
          "",
          sampleMaskBase(session) + "#" + session._cfg.hashPrefix + index
        );
      } catch (e) {}
    }

    var finishHome = session.finishHome;

    if (els.prevEl) {
      if (index > 0) {
        wireNavLink(els.prevEl, session, order[index - 1], index - 1);
        els.prevEl.textContent = "Back";
        els.prevEl.classList.remove("nav-link--disabled");
      } else {
        els.prevEl.href = "#";
        els.prevEl.textContent = "Back";
        els.prevEl.classList.add("nav-link--disabled");
        els.prevEl.onclick = function (ev) {
          ev.preventDefault();
        };
      }
    }

    if (els.nextEl) {
      var onDnd = isDragDropSampleItem(order[index]);
      if (index + 1 < order.length) {
        els.nextEl.style.display = "";
        wireNavLink(els.nextEl, session, order[index + 1], index + 1);
        els.nextEl.textContent = "Next";
        els.nextEl.classList.remove("nav-link--disabled");
        var nextItem = order[index + 1];
        var nextIndex = index + 1;
        els.nextEl.onclick = function (ev) {
          ev.preventDefault();
          captureCurrentAnswer(session, index);
          location.assign(realItemHref(session, nextItem, nextIndex));
        };
      } else {
        els.nextEl.style.display = "";
        els.nextEl.href = finishHome;
        els.nextEl.textContent = "Finish sample";
        els.nextEl.classList.remove("nav-link--disabled");
        els.nextEl.onclick = function (ev) {
          ev.preventDefault();
          completeSample(session, finishHome);
        };
      }
    }

    var home = document.querySelector("a.nav-home");
    if (home) {
      home.href = finishHome;
      home.textContent = "Home";
      home.onclick = function () {
        clearSampleSession(session);
      };
    }

    if (els.homeEl) {
      els.homeEl.href = finishHome;
      els.homeEl.onclick = function () {
        clearSampleSession(session);
      };
    }

    syncSampleSubjectsFooter(session);
    if (order[index] && order[index].type === "mcq") {
      wireAnswerCapture(session, index);
    }
  }

  function reconcileLocation(session) {
    var index = currentItemIndex(session);
    if (index >= 0) return index;
    var hint = hashIndex(session);
    if (hint >= 0 && hint < session.order.length) {
      location.replace(realItemHref(session, session.order[hint], hint));
      return -2;
    }
    location.replace(realItemHref(session, session.order[0], 0));
    return -2;
  }

  function injectStyles() {
    if (document.head.querySelector("style[data-cisco-home-sample-nav]")) return;
    var s = document.createElement("style");
    s.setAttribute("data-cisco-home-sample-nav", "1");
    s.textContent =
      ".cisco-sample-progress{font-size:.8rem;font-weight:700;color:#9fb0cc;margin:0 8px 0 0;white-space:nowrap}" +
      ".cisco-home-sample-nav{position:fixed;left:0;right:0;bottom:0;z-index:10001;display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:10px;padding:12px 16px calc(12px + env(safe-area-inset-bottom,0px));background:rgba(11,16,32,.94);border-top:1px solid #2d3b5a;backdrop-filter:blur(10px)}" +
      ".cisco-home-sample-nav__progress{font-size:.85rem;font-weight:700;color:#b8c3d6;white-space:nowrap;flex:0 1 auto;margin-right:auto}" +
      ".cisco-home-sample-nav__actions{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-left:auto}" +
      ".cisco-home-sample-nav a{text-decoration:none;background:#2f66bf;border:1px solid #4f84d8;color:#f4f7ff;border-radius:10px;padding:10px 18px;font-weight:700;min-width:5.5rem;text-align:center;box-sizing:border-box}" +
      ".cisco-home-sample-nav a:hover{filter:brightness(1.08)}" +
      ".cisco-home-sample-nav a.nav-link--disabled{opacity:.45;pointer-events:none}" +
      "body.cisco-home-sample-active{padding-bottom:calc(88px + env(safe-area-inset-bottom,0px))!important}" +
      "body.cisco-home-sample-active nav.sim-nav{display:none!important}" +
      ".cisco-sample-upsell-root{position:fixed;inset:0;z-index:20002;display:flex;align-items:center;justify-content:center;padding:16px}" +
      ".cisco-sample-upsell-backdrop{position:absolute;inset:0;background:rgba(8,12,24,.72);backdrop-filter:blur(4px)}" +
      ".cisco-sample-upsell-panel{position:relative;z-index:1;width:min(520px,100%);max-height:min(90vh,640px);overflow:auto;margin:0;padding:clamp(20px,4vw,28px) clamp(18px,3.5vw,26px) 22px;border-radius:16px;border:1px solid #4f84d8;background:linear-gradient(165deg,rgba(22,32,52,.98) 0%,rgba(14,20,36,.99) 100%);color:#e6edf3;box-shadow:0 24px 64px rgba(0,0,0,.45)}" +
      ".cisco-sample-upsell-close{position:absolute;top:10px;right:12px;border:0;background:transparent;color:#9fb0cc;font-size:1.6rem;line-height:1;cursor:pointer;padding:4px 8px}" +
      ".cisco-sample-upsell-eyebrow{margin:0 0 8px;font-size:.78rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#a8c4f0}" +
      ".cisco-sample-upsell-panel h2{margin:0 0 12px;font-size:clamp(1.15rem,3vw,1.45rem);line-height:1.25;color:#fff}" +
      ".cisco-sample-upsell-lead{margin:0 0 18px;font-size:.95rem;line-height:1.55;color:#cbd5e1}" +
      ".cisco-sample-upsell-actions{display:flex;flex-direction:column;gap:10px}" +
      ".cisco-sample-upsell-primary{display:inline-flex;justify-content:center;align-items:center;border:1px solid #4f84d8;background:#2f66bf;color:#f4f7ff;border-radius:10px;padding:12px 18px;font:inherit;font-weight:800;cursor:pointer;width:100%;box-sizing:border-box}" +
      ".cisco-sample-upsell-primary:hover{filter:brightness(1.08)}" +
      ".cisco-sample-upsell-secondary{border:1px solid rgba(159,176,204,.45);background:transparent;color:#e6edf3;border-radius:10px;padding:11px 18px;font:inherit;font-weight:700;cursor:pointer}" +
      ".cisco-sample-upsell-secondary:hover{background:rgba(255,255,255,.06)}" +
      ".sample-subjects-footer{margin-top:1.25rem;padding-top:1rem;border-top:1px solid rgba(159,176,204,.28)}" +
      ".sample-subjects-footer__title{margin:0 0 .5rem;font-size:.85rem;font-weight:700;color:#9fb0cc}" +
      ".sample-subjects-footer__list{margin:0;padding:0 0 0 1.25rem;font-size:.82rem;line-height:1.5;color:#b8c3d6}" +
      ".sample-subjects-footer__list li+li{margin-top:.2rem}" +
      ".cisco-sample-scorecard-root{position:fixed;inset:0;z-index:20003;display:flex;align-items:center;justify-content:center;padding:16px}" +
      ".cisco-sample-scorecard-backdrop{position:absolute;inset:0;background:rgba(8,12,24,.78);backdrop-filter:blur(4px)}" +
      ".cisco-sample-scorecard-panel{position:relative;z-index:1;width:min(640px,100%);max-height:min(92vh,720px);overflow:auto;margin:0;padding:clamp(20px,4vw,28px);border-radius:16px;border:1px solid #4f84d8;background:linear-gradient(165deg,#f8fafc 0%,#eff6ff 55%,#fff 100%);color:#1e293b;box-shadow:0 24px 64px rgba(0,0,0,.35)}" +
      ".cisco-sample-scorecard-close{position:absolute;top:10px;right:12px;border:0;background:transparent;color:#64748b;font-size:1.6rem;line-height:1;cursor:pointer;padding:4px 8px}" +
      ".cisco-sample-scorecard-eyebrow{margin:0 0 8px;font-size:.78rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#2f66bf}" +
      ".cisco-sample-scorecard-panel h2{margin:0 0 10px;font-size:clamp(1.15rem,3vw,1.45rem);line-height:1.25;color:#0f172a}" +
      ".cisco-sample-scorecard-score{margin:0 0 10px;font-size:1.05rem;color:#0f172a}" +
      ".cisco-sample-scorecard-lead{margin:0 0 16px;font-size:.92rem;line-height:1.55;color:#475569}" +
      ".cisco-sample-scorecard-table-wrap{overflow:auto;border:1px solid #cbd5e1;border-radius:10px;background:#fff}" +
      ".cisco-sample-scorecard-table-wrap table{width:100%;border-collapse:collapse;font-size:.88rem}" +
      ".cisco-sample-scorecard-table-wrap th,.cisco-sample-scorecard-table-wrap td{padding:10px 12px;text-align:left;border-bottom:1px solid #e2e8f0;vertical-align:top}" +
      ".cisco-sample-scorecard-table-wrap thead th{background:#f1f5f9;font-weight:800;color:#334155}" +
      ".cisco-sample-scorecard-table-wrap tbody tr:last-child th,.cisco-sample-scorecard-table-wrap tbody tr:last-child td{border-bottom:none}" +
      ".cisco-sample-scorecard-actions{margin-top:18px;display:flex;flex-direction:column;gap:10px}" +
      ".cisco-sample-scorecard-primary{border:1px solid #2f66bf;background:#2f66bf;color:#f8fafc;border-radius:10px;padding:12px 18px;font:inherit;font-weight:800;cursor:pointer;width:100%}" +
      ".cisco-sample-scorecard-primary:hover{filter:brightness(1.06)}" +
      ".cisco-ccna-offer-root{position:fixed;inset:0;z-index:20004;display:flex;align-items:center;justify-content:center;padding:16px}" +
      ".cisco-ccna-offer-backdrop{position:absolute;inset:0;background:rgba(8,12,24,.78);backdrop-filter:blur(4px)}" +
      ".cisco-ccna-offer-panel{position:relative;z-index:1;width:min(560px,100%);max-height:min(92vh,760px);overflow:auto;margin:0;padding:clamp(20px,4vw,28px);border-radius:16px;border:1px solid #4f84d8;background:linear-gradient(165deg,rgba(22,32,52,.98) 0%,rgba(14,20,36,.99) 100%);color:#e6edf3;box-shadow:0 24px 64px rgba(0,0,0,.45)}" +
      ".cisco-ccna-offer-close{position:absolute;top:10px;right:12px;border:0;background:transparent;color:#9fb0cc;font-size:1.6rem;line-height:1;cursor:pointer;padding:4px 8px}" +
      ".cisco-ccna-offer-eyebrow{margin:0 0 8px;font-size:.78rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#a8c4f0}" +
      ".cisco-ccna-offer-panel h2{margin:0 0 10px;font-size:clamp(1.15rem,3vw,1.45rem);line-height:1.25;color:#fff}" +
      ".cisco-ccna-offer-score{margin:0 0 10px;font-size:1rem;color:#dbeafe}" +
      ".cisco-ccna-offer-lead{margin:0 0 12px;font-size:.95rem;line-height:1.55;color:#cbd5e1}" +
      ".cisco-ccna-offer-lead strong{color:#f8fafc}" +
      ".cisco-ccna-offer-tagline{margin:0 0 18px;font-size:.9rem;font-style:italic;font-weight:700;color:#93c5fd}" +
      ".cisco-ccna-offer-tiers{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px;margin:0 0 16px}" +
      ".cisco-ccna-offer-tier{border:1px solid rgba(79,132,216,.35);border-radius:12px;padding:14px;background:rgba(13,21,40,.55)}" +
      ".cisco-ccna-offer-tier--featured{border-color:rgba(251,191,36,.55);box-shadow:0 0 0 1px rgba(251,191,36,.2) inset}" +
      ".cisco-ccna-offer-tier-label{margin:0 0 4px;font-size:.82rem;font-weight:800;letter-spacing:.04em;text-transform:uppercase;color:#9fb0cc}" +
      ".cisco-ccna-offer-tier-price{margin:0 0 4px;font-size:1.35rem;font-weight:800;color:#fff}" +
      ".cisco-ccna-offer-tier-price span{font-size:.82rem;font-weight:700;color:#94a3b8}" +
      ".cisco-ccna-offer-tier-note{margin:0 0 12px;font-size:.8rem;line-height:1.4;color:#94a3b8}" +
      ".cisco-ccna-offer-tier-btn{display:inline-flex;justify-content:center;align-items:center;border:1px solid #4f84d8;background:#2f66bf;color:#f4f7ff;border-radius:10px;padding:11px 14px;font:inherit;font-weight:800;cursor:pointer;width:100%;box-sizing:border-box}" +
      ".cisco-ccna-offer-tier-btn--featured{border-color:rgba(251,191,36,.65);background:linear-gradient(165deg,#3b82f6 0%,#2563eb 100%)}" +
      ".cisco-ccna-offer-tier-btn:hover{filter:brightness(1.08)}" +
      ".cisco-ccna-offer-tier-btn:disabled{opacity:.7;cursor:wait}" +
      ".cisco-ccna-offer-actions{display:flex;flex-direction:column;gap:10px}" +
      ".cisco-ccna-offer-secondary{border:1px solid rgba(159,176,204,.45);background:transparent;color:#e6edf3;border-radius:10px;padding:11px 18px;font:inherit;font-weight:700;cursor:pointer}" +
      ".cisco-ccna-offer-secondary:hover{background:rgba(255,255,255,.06)}";
    document.head.appendChild(s);
  }

  function run() {
    var session = activeSessionConfig();
    if (!session) return;
    injectStyles();
    var index = reconcileLocation(session);
    if (index < 0) return;
    applyNav(session, index);
  }

  function onHashChange() {
    var session = activeSessionConfig();
    if (!session || !isSingleTrackSample(session)) return;
    var hint = hashIndex(session);
    if (hint < 0 || hint >= session.order.length) return;
    if (!itemMatchesPath(session.order[hint], pathnameForMatch())) {
      location.replace(realItemHref(session, session.order[hint], hint));
    }
  }

  function scheduleRuns() {
    run();
    setTimeout(run, 0);
    window.addEventListener("load", run);
    window.addEventListener("hashchange", onHashChange);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", scheduleRuns);
  } else {
    scheduleRuns();
  }
})();
