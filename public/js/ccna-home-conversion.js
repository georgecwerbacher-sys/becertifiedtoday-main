/**
 * CCNA home landing — conversion-first headline matching + sticky mobile CTA.
 *
 * Conversion rules:
 * - Default hero: free-practice (no random rotation).
 * - Headline changes ONLY when ?hl=, utm_content, or utm_term maps to a pinned ad.
 * - Primary conversion: free assessment. Purchase is secondary ATF.
 *
 * Ad setup: scripts/ccna-google-ads-headline-suffixes.txt
 */
(function () {
  "use strict";

  var STORAGE_KEY = "bcc_ccna_home_hl_v1";
  var PRACTICE_TEST_PATH = "/ccna/practice-test";
  var DEFAULT_VARIANT = "free-practice";
  var FREE_ASSESSMENT_PATH = "/CCNA_Sim_EXAM/free-assessment.html";

  var BASE_LEAD =
    "CCNA assessment with scorecard. <strong>No PDFs.</strong> " +
    "Practice CCNA online with labs, drag-and-drop, and questions—<strong>runs entirely in your browser.</strong>";

  var VARIANTS = {
    "practice-test": {
      id: "practice-test",
      adHeadline: "CCNA Practice Test",
      eyebrow: "CCNA 200-301 · online practice test",
      headline: "CCNA Practice Test — practice CCNA online with labs & questions",
      lead: BASE_LEAD,
      ctaPrimary: "Start free CCNA practice test",
      stickyPrimary: "Free CCNA practice",
    },
    "prep-200-301": {
      id: "prep-200-301",
      adHeadline: "CCNA 200-301 Prep",
      eyebrow: "CCNA 200-301 prep · browser-based",
      headline: "CCNA 200-301 Prep — labs, drag-and-drop & practice questions",
      lead:
        "Full CCNA 200-301 prep online: interactive questions, CLI labs, and drag-and-drop in one browser session. " +
        "<strong>No PDFs.</strong> Start the free assessment in your browser—no additional apps.",
      ctaPrimary: "Begin free CCNA 200-301 prep",
      stickyPrimary: "Free 200-301 prep",
    },
    "free-practice": {
      id: "free-practice",
      adHeadline: "Free CCNA Practice",
      eyebrow: "Free CCNA practice · scorecard included",
      headline: "Free CCNA Practice Assessment With Scorecard",
      lead:
        "Take a free CCNA assessment in your browser and get a scorecard when you finish. " +
        "<strong>No PDFs</strong>, no membership, and no additional apps—just labs, drag-and-drop, and questions.",
      ctaPrimary: "Take free CCNA practice — start now",
      stickyPrimary: "Free CCNA practice",
    },
    "mock-exam": {
      id: "mock-exam",
      adHeadline: "CCNA Mock Exam",
      eyebrow: "CCNA mock exam · timed browser practice",
      headline: "CCNA Mock Exam — timed practice that mirrors test day",
      lead:
        "Run a CCNA mock exam in your browser with the same mix as test day: multiple-choice, drag-and-drop, and CLI-style items. " +
        "<strong>Scorecard included.</strong> No PDFs, membership, or extra apps.",
      ctaPrimary: "Start free CCNA mock exam",
      stickyPrimary: "Free mock exam",
    },
    "exam-qna": {
      id: "exam-qna",
      adHeadline: "CCNA Exam Question and Answers",
      eyebrow: "CCNA exam Q&A · interactive feedback",
      headline: "CCNA Exam Questions and Answers — interactive, not PDFs",
      lead:
        "Work through CCNA exam questions with instant feedback—not static PDF answer keys. " +
        "Labs and drag-and-drop included. <strong>Start the free assessment in your browser.</strong>",
      ctaPrimary: "Try free CCNA questions",
      stickyPrimary: "Free CCNA Q&A",
    },
    "cisco-prep": {
      id: "cisco-prep",
      adHeadline: "Cisco CCNA Prep",
      eyebrow: "Cisco CCNA prep · 200-301 aligned",
      headline: "Cisco CCNA Prep — official-format practice online",
      lead: BASE_LEAD,
      ctaPrimary: "Start Cisco CCNA prep free",
      stickyPrimary: "Free Cisco prep",
    },
    "study-for": {
      id: "study-for",
      adHeadline: "Study For CCNA",
      eyebrow: "Study for CCNA · questions, labs & D&D",
      headline: "Study for the CCNA — questions, labs & drag-and-drop online",
      lead:
        "Study for the CCNA with <strong>700+ interactive questions</strong>, CLI labs, and drag-and-drop—all in your browser. " +
        "Free assessment with scorecard. No PDFs or additional apps.",
      ctaPrimary: "Start studying free",
      stickyPrimary: "Study free",
    },
    "pass-exam": {
      id: "pass-exam",
      adHeadline: "Pass The CCNA Exam",
      eyebrow: "Pass the CCNA · practice with feedback",
      headline: "Pass the CCNA Exam — practice with scorecard feedback",
      lead:
        "Build exam-day confidence with timed CCNA practice and a scorecard that shows where to improve. " +
        "<strong>No PDFs.</strong> Runs entirely in your browser—labs, drag-and-drop, and timed practice.",
      ctaPrimary: "Take free practice exam",
      stickyPrimary: "Free practice exam",
    },
    "questions-online": {
      id: "questions-online",
      adHeadline: "CCNA Questions Online",
      eyebrow: "CCNA questions online · browser-based",
      headline: "CCNA Questions Online — 700+ items in your browser",
      lead:
        "Access CCNA questions online with topology exhibits, CLI labs, and drag-and-drop—no downloads. " +
        "Start with a free assessment and scorecard. <strong>Browser-only CCNA prep—no PDFs.</strong>",
      ctaPrimary: "Browse CCNA questions free",
      stickyPrimary: "Free questions",
    },
    "test-questions": {
      id: "test-questions",
      adHeadline: "CCNA Test Questions",
      eyebrow: "CCNA test questions · MCQ, D&D & labs",
      headline: "CCNA Test Questions — MCQ, drag-and-drop & CLI labs",
      lead: BASE_LEAD,
      ctaPrimary: "Try CCNA test questions free",
      stickyPrimary: "Free test questions",
    },
    "cert-prep": {
      id: "cert-prep",
      adHeadline: "CCNA Certification Prep",
      eyebrow: "CCNA certification prep · 200-301",
      headline: "CCNA Certification Prep — no membership required",
      lead:
        "CCNA certification prep with questions, labs, and drag-and-drop aligned to 200-301 v1.1. " +
        "<strong>No recurring membership.</strong> Free assessment with scorecard; pay once when you want full access.",
      ctaPrimary: "Start certification prep free",
      stickyPrimary: "Free cert prep",
    },
    "practice-questions": {
      id: "practice-questions",
      adHeadline: "Practice CCNA Questions",
      eyebrow: "Practice CCNA questions · instant feedback",
      headline: "Practice CCNA Questions — free assessment to start",
      lead: BASE_LEAD,
      ctaPrimary: "Practice CCNA questions free",
      stickyPrimary: "Practice free",
    },
    "exam-practice": {
      id: "exam-practice",
      adHeadline: "CCNA Exam Practice",
      eyebrow: "CCNA exam practice · timed & scored",
      headline: "CCNA Exam Practice — timed simulations from $9.99",
      lead:
        "CCNA exam practice with a free 30-minute assessment or a full <strong>120-minute simulation</strong> from $9.99. " +
        "Labs, drag-and-drop, and questions in your browser—no PDFs or extra apps.",
      ctaPrimary: "Start free exam practice",
      stickyPrimary: "Free exam practice",
    },
    "prep-questions": {
      id: "prep-questions",
      adHeadline: "CCNA Prep Questions",
      eyebrow: "CCNA prep questions · scorecard on free run",
      headline: "CCNA Prep Questions — scorecard on your free run",
      lead: BASE_LEAD,
      ctaPrimary: "Try prep questions free",
      stickyPrimary: "Free prep questions",
    },
  };

  var ALIASES = {
    a: "practice-test",
    b: "free-practice",
    c: "prep-200-301",
    "hl-practice-test": "practice-test",
    "practice-test": "practice-test",
    "ccna-practice-test": "practice-test",
    "hl-200-301-prep": "prep-200-301",
    "200-301-prep": "prep-200-301",
    "ccna-200-301-prep": "prep-200-301",
    "hl-free-practice": "free-practice",
    "free-practice": "free-practice",
    "hl-mock-exam": "mock-exam",
    "mock-exam": "mock-exam",
    "ccna-mock-exam": "mock-exam",
    "hl-exam-qna": "exam-qna",
    "exam-qna": "exam-qna",
    "exam-question-and-answers": "exam-qna",
    "hl-cisco-prep": "cisco-prep",
    "cisco-prep": "cisco-prep",
    "cisco-ccna-prep": "cisco-prep",
    "hl-study-for": "study-for",
    "study-for": "study-for",
    "study-for-ccna": "study-for",
    "hl-pass-exam": "pass-exam",
    "pass-exam": "pass-exam",
    "pass-the-ccna-exam": "pass-exam",
    "hl-questions-online": "questions-online",
    "questions-online": "questions-online",
    "ccna-questions-online": "questions-online",
    "hl-test-questions": "test-questions",
    "test-questions": "test-questions",
    "ccna-test-questions": "test-questions",
    "hl-cert-prep": "cert-prep",
    "cert-prep": "cert-prep",
    "certification-prep": "cert-prep",
    "hl-practice-questions": "practice-questions",
    "practice-questions": "practice-questions",
    "hl-exam-practice": "exam-practice",
    "exam-practice": "exam-practice",
    "hl-prep-questions": "prep-questions",
    "prep-questions": "prep-questions",
    free: "free-practice",
    "free-exam": "free-practice",
    sim: "exam-practice",
    simulation: "exam-practice",
    prep: "prep-200-301",
    practice: "practice-test",
  };

  var TERM_RULES = [
    { re: /\bfree ccna practice\b|\bfree ccna\b|\bfree practice\b/, id: "free-practice" },
    { re: /\bmock exam\b|\bccna mock\b/, id: "mock-exam" },
    { re: /\bquestion and answer\b|\bquestions and answers\b|\bexam q&a\b/, id: "exam-qna" },
    { re: /\bcisco ccna prep\b|\bcisco ccna\b/, id: "cisco-prep" },
    { re: /\bstudy for ccna\b|\bstudy ccna\b/, id: "study-for" },
    { re: /\bpass the ccna\b|\bpass ccna\b/, id: "pass-exam" },
    { re: /\bquestions online\b|\bonline questions\b/, id: "questions-online" },
    { re: /\btest questions\b/, id: "test-questions" },
    { re: /\bcertification prep\b|\bccna cert\b/, id: "cert-prep" },
    { re: /\bpractice ccna questions\b|\bpractice questions\b/, id: "practice-questions" },
    { re: /\bexam practice\b/, id: "exam-practice" },
    { re: /\bprep questions\b/, id: "prep-questions" },
    { re: /\bccna practice test\b|\bpractice test\b/, id: "practice-test" },
    { re: /\b200-301 prep\b|\bccna 200-301\b/, id: "prep-200-301" },
    { re: /\bsimul|\btimed exam\b/, id: "exam-practice" },
    { re: /\bfree\b/, id: "free-practice" },
    { re: /\bccna prep\b|\bccna practice\b/, id: "practice-test" },
  ];

  function readQueryParam(key) {
    try {
      return new URLSearchParams(window.location.search).get(key);
    } catch (e) {
      return null;
    }
  }

  function normalizedPath() {
    var p = location.pathname || "/";
    if (p.length > 1 && p.charAt(p.length - 1) === "/") p = p.slice(0, -1);
    return p;
  }

  function isPracticeTestLanding() {
    return normalizedPath() === PRACTICE_TEST_PATH;
  }

  function saveStoredVariant(id) {
    try {
      sessionStorage.setItem(STORAGE_KEY, id);
    } catch (e) {
      /* ignore */
    }
  }

  function normalizeVariantId(raw) {
    if (!raw) return null;
    var key = String(raw).toLowerCase().trim();
    if (VARIANTS[key]) return key;
    if (ALIASES[key]) return ALIASES[key];
    return null;
  }

  function mapUtmTerm(term) {
    if (!term) return null;
    var t = String(term).toLowerCase();
    for (var i = 0; i < TERM_RULES.length; i++) {
      if (TERM_RULES[i].re.test(t)) return TERM_RULES[i].id;
    }
    return null;
  }

  function resolveVariant() {
    var fromUrl = normalizeVariantId(readQueryParam("hl"));
    if (fromUrl) {
      saveStoredVariant(fromUrl);
      return { id: fromUrl, source: "url" };
    }

    var fromContent = normalizeVariantId(readQueryParam("utm_content"));
    if (fromContent) {
      saveStoredVariant(fromContent);
      return { id: fromContent, source: "utm_content" };
    }

    var fromTerm = mapUtmTerm(readQueryParam("utm_term"));
    if (fromTerm) {
      saveStoredVariant(fromTerm);
      return { id: fromTerm, source: "utm_term" };
    }

    return { id: DEFAULT_VARIANT, source: "default" };
  }

  function getVariant(id) {
    return VARIANTS[id] || VARIANTS[DEFAULT_VARIANT];
  }

  function campaignQueryString() {
    var attrs =
      typeof window.bccGetCampaignAttribution === "function" ? window.bccGetCampaignAttribution() : {};
    var parts = [];
    ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "gclid"].forEach(function (key) {
      if (attrs[key]) parts.push(encodeURIComponent(key) + "=" + encodeURIComponent(attrs[key]));
    });
    return parts.length ? "?" + parts.join("&") : "";
  }

  function appendCampaignHref(path) {
    var qs = campaignQueryString();
    if (!qs) return path;
    return path + (path.indexOf("?") >= 0 ? "&" + qs.slice(1) : qs);
  }

  function trackVariantImpression(variant, source) {
    if (typeof window.gtag !== "function") return;
    var attrs =
      typeof window.bccGetCampaignAttribution === "function" ? window.bccGetCampaignAttribution() : {};
    window.gtag(
      "event",
      "ccna_home_headline_impression",
      Object.assign(
        {
          headline_variant: variant.id,
          ad_headline: variant.adHeadline,
          assignment_source: source,
          landing_path: normalizedPath(),
        },
        attrs.utm_campaign ? { campaign_name: attrs.utm_campaign } : {},
        attrs.utm_content ? { campaign_content: attrs.utm_content } : {}
      )
    );
  }

  function trackFreeAssessmentClick(label) {
    if (typeof window.gtag !== "function") return;
    var variant = window.bccCcnaHomeHeadlineVariant || DEFAULT_VARIANT;
    var attrs =
      typeof window.bccGetCampaignAttribution === "function" ? window.bccGetCampaignAttribution() : {};
    window.gtag(
      "event",
      "ccna_free_assessment_click",
      Object.assign(
        {
          cta_label: label,
          headline_variant: variant,
          landing_path: normalizedPath(),
        },
        attrs.utm_campaign ? { campaign_name: attrs.utm_campaign } : {},
        attrs.utm_content ? { campaign_content: attrs.utm_content } : {}
      )
    );
  }

  function applyLandingMeta(variant) {
    if (!isPracticeTestLanding()) return;
    var canonical = document.querySelector('link[rel="canonical"]');
    if (canonical) canonical.href = "https://becertifiedtoday.com/ccna/practice-test";
    document.title = variant.adHeadline + " | CCNA 200-301 Prep | Be Certified Today";
  }

  function wireFreeAssessmentLinks() {
    var href = appendCampaignHref(FREE_ASSESSMENT_PATH);
    document.querySelectorAll("[data-bcc-free-assessment]").forEach(function (el) {
      if (el.tagName === "A") el.setAttribute("href", href);
    });
  }

  function bindConversionClicks() {
    document.querySelectorAll("[data-bcc-free-assessment]").forEach(function (el) {
      if (el.dataset.bccFreeCtaBound === "1") return;
      el.dataset.bccFreeCtaBound = "1";
      el.addEventListener("click", function () {
        trackFreeAssessmentClick(el.textContent ? el.textContent.trim() : "free assessment");
      });
    });
  }

  function applyHeadlineVariant() {
    var hero = document.querySelector(".hero-conversion");
    if (!hero) return;

    var picked = resolveVariant();
    var variant = getVariant(picked.id);
    var isDefault = picked.source === "default";

    var eyebrow = document.getElementById("hero-conversion-eyebrow");
    var title = document.getElementById("hero-conversion-title");
    var lead = document.getElementById("hero-conversion-lead");
    var ctaPrimary = document.getElementById("hero-conversion-cta-primary");

    if (!isDefault || hero.getAttribute("data-ccna-hl-pending") === "1") {
      if (eyebrow) eyebrow.textContent = variant.eyebrow;
      if (title) title.textContent = variant.headline;
      if (lead) lead.innerHTML = variant.lead;
      if (ctaPrimary) ctaPrimary.textContent = variant.ctaPrimary;
    }

    hero.setAttribute("data-ccna-hl-variant", variant.id);
    hero.removeAttribute("data-ccna-hl-pending");

    applyLandingMeta(variant);
    trackVariantImpression(variant, picked.source);
    window.bccCcnaHomeHeadlineVariant = variant.id;
    window.bccCcnaHomeHeadlineVariantData = variant;
  }

  function initStickyMobileCta() {
    var hero = document.querySelector(".hero-conversion");
    var purchase = document.getElementById("purchase");
    if (!hero || !purchase) return;

    var variant =
      window.bccCcnaHomeHeadlineVariantData ||
      getVariant(window.bccCcnaHomeHeadlineVariant || DEFAULT_VARIANT);
    var stickyPrimary = variant.stickyPrimary || "Free CCNA practice";
    var freeHref = appendCampaignHref(FREE_ASSESSMENT_PATH);

    var bar = document.createElement("div");
    bar.id = "ccnaMobileStickyCta";
    bar.className = "ccna-mobile-sticky-cta";
    bar.setAttribute("role", "region");
    bar.setAttribute("aria-label", "Start free CCNA practice");
    bar.setAttribute("aria-hidden", "true");
    bar.hidden = true;
    bar.innerHTML =
      '<a class="cta-main cta-main--free ccna-mobile-sticky-cta__primary" data-bcc-free-assessment href="' +
      freeHref +
      '">' +
      stickyPrimary +
      "</a>";
    document.body.appendChild(bar);

    var mq = window.matchMedia("(max-width: 767px)");
    var shown = false;

    function setVisible(next) {
      if (shown === next) return;
      shown = next;
      bar.hidden = !next;
      bar.setAttribute("aria-hidden", next ? "false" : "true");
      bar.classList.toggle("is-visible", next);
      document.body.classList.toggle("ccna-sticky-cta-visible", next);
    }

    function update() {
      if (!mq.matches) {
        setVisible(false);
        return;
      }
      var heroBottom = hero.getBoundingClientRect().bottom;
      var pastHero = heroBottom < 72;
      setVisible(pastHero);
    }

    var ticking = false;
    function onScroll() {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(function () {
        ticking = false;
        update();
      });
    }

    if (typeof mq.addEventListener === "function") {
      mq.addEventListener("change", update);
    } else if (typeof mq.addListener === "function") {
      mq.addListener(update);
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll, { passive: true });
    update();
    bindConversionClicks();
  }

  function init() {
    applyHeadlineVariant();
    wireFreeAssessmentLinks();
    bindConversionClicks();
    initStickyMobileCta();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
