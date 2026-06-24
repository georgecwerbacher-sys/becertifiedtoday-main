/**
 * Security+ home landing — conversion-first headline matching + sticky mobile CTA.
 *
 * Default hero: free samples. Headline changes when ?hl=, utm_content, or utm_term maps to a variant.
 *
 * Ad setup: marketing-research/Sec+ Campaign/ — Sec+ Notes.md · Sec+ RSA Copy.md · secplus-campaign-checklist.csv
 */
(function () {
  "use strict";

  var STORAGE_KEY = "bcc_secplus_home_hl_v1";
  var DEFAULT_VARIANT = "wedge-default";
  var SAMPLES_SECTION = "#home-secplus-samples-title";
  var SAMPLE_QUESTIONS = "/secplus-sample?track=questions";
  var SAMPLE_PBQ = "/secplus-sample?track=sim-dark-web";

  var PAID_30D_SUFFIX =
    "Try the free MCQ or PBQ samples below, then unlock <strong>30-day full access for $19.99</strong>—PBQs, timed sim, and scorecard included.";

  var WEDGE_LEAD =
    "Build Security+ readiness with <strong>34 PBQ scenarios</strong> (chain labs, drag-and-drop, IR exhibits) and a <strong>90-minute timed simulation with scorecard review</strong>—included with full access. " +
    PAID_30D_SUFFIX;

  var BASE_LEAD =
    "Practice Security+ SY0-701 online with 1000+ questions and performance-based scenarios in your browser. <strong>No PDFs.</strong> " +
    "Try free samples first—same UI as full access.";

  var GOOGLE_PAID_PURCHASE_CTA = "Get 30-day access";

  var PAID_VARIANT_OVERRIDES = {
    "pbq-wedge": {
      lead:
        "Rehearse performance-based items the way CompTIA tests them: <strong>drag-and-drop chain labs</strong>, hot spots, and IR report exhibits in your browser—no download or VM. " +
        "Try <strong>three free PBQ scenarios</strong> (dark web IR, WLAN configuration, firewall ACL), then unlock 34 PBQ scenarios, 1000+ questions, and the timed sim for <strong>$19.99 / 30 days</strong>.",
      ctaPrimary: GOOGLE_PAID_PURCHASE_CTA,
      stickyPrimary: GOOGLE_PAID_PURCHASE_CTA,
      ctaHref: "#purchase",
    },
    "timed-sim": {
      lead:
        "Rehearse test-day pacing with a <strong>90-minute timed Security+ simulation</strong>: multiple-choice and performance-based items in one session, plus a <strong>detailed domain scorecard</strong> when you finish. " +
        "Included with <strong>30-day full access for $19.99</strong>.",
      ctaPrimary: GOOGLE_PAID_PURCHASE_CTA,
      stickyPrimary: GOOGLE_PAID_PURCHASE_CTA,
      ctaHref: "#purchase",
    },
    "wedge-default": {
      ctaPrimary: GOOGLE_PAID_PURCHASE_CTA,
      stickyPrimary: GOOGLE_PAID_PURCHASE_CTA,
      ctaHref: "#purchase",
      lead:
        "Build Security+ readiness with <strong>34 PBQ scenarios</strong> (chain labs, drag-and-drop, IR exhibits) and a <strong>90-minute timed simulation with scorecard review</strong>—included with full access. " +
        PAID_30D_SUFFIX,
    },
    federal: {
      ctaPrimary: GOOGLE_PAID_PURCHASE_CTA,
      stickyPrimary: GOOGLE_PAID_PURCHASE_CTA,
      ctaHref: "#purchase",
    },
    "practice-test": {
      ctaPrimary: GOOGLE_PAID_PURCHASE_CTA,
      stickyPrimary: GOOGLE_PAID_PURCHASE_CTA,
      ctaHref: "#purchase",
    },
    "question-bank": {
      ctaPrimary: GOOGLE_PAID_PURCHASE_CTA,
      stickyPrimary: GOOGLE_PAID_PURCHASE_CTA,
      ctaHref: "#purchase",
    },
  };

  var VARIANTS = {
    "wedge-default": {
      id: "wedge-default",
      adHeadline: "Security+ Practice Test",
      eyebrow: "CompTIA Security+ SY0-701 · PBQ · timed simulation",
      headline: "Security+ Exam Prep — 1000+ Questions, 34 PBQs & Timed Sim with Scorecard",
      lead: WEDGE_LEAD,
      ctaPrimary: "Preview free Security+ samples",
      stickyPrimary: "Free samples",
    },
    "portal-10d": {
      id: "portal-10d",
      adHeadline: "Security+ Practice Test",
      eyebrow: "SY0-701 · 30-day access · $19.99",
      headline: "Security+ Practice Test — 1000+ SY0-701 Questions & PBQ Scenarios",
      lead: BASE_LEAD + " Unlock <strong>30-day full access for $19.99</strong> when you are ready.",
      ctaPrimary: "Preview free Security+ samples",
      stickyPrimary: "Get 30-day access",
      ctaHref: "#purchase",
    },
    "pbq-wedge": {
      id: "pbq-wedge",
      adHeadline: "Security+ PBQ Practice",
      eyebrow: "SY0-701 PBQ · browser · no download",
      headline: "Security+ PBQ Practice in Your Browser — Chain Labs & IR Scenarios",
      lead:
        "Rehearse performance-based items the way CompTIA tests them: <strong>drag-and-drop chain labs</strong>, hot spots, and IR report exhibits in your browser—no download or VM. " +
        "Try <strong>three free PBQ scenarios</strong> (dark web IR, WLAN configuration, firewall ACL), then unlock 34 PBQ scenarios + 1000+ questions for <strong>$19.99 / 30 days</strong>.",
      ctaPrimary: "Try free 3-scenario PBQ preview",
      ctaHref: SAMPLE_PBQ,
      stickyPrimary: "Free PBQ preview",
    },
    "timed-sim": {
      id: "timed-sim",
      adHeadline: "Security+ Timed Practice Test",
      eyebrow: "SY0-701 timed simulation · 90 minutes",
      headline: "90-Minute Security+ Timed Simulation — MCQ + PBQ + Scorecard Review",
      lead:
        "Rehearse test-day pacing with a <strong>90-minute timed Security+ simulation</strong>: multiple-choice and performance-based items in one session, plus a <strong>detailed domain scorecard</strong> when you finish. " +
        "Included with <strong>30-day full access for $19.99</strong>.",
      ctaPrimary: "Preview free Security+ samples",
      stickyPrimary: "Free samples",
    },
    "federal": {
      id: "federal",
      adHeadline: "Security+ DoD Exam Prep",
      eyebrow: "SY0-701 · federal & contractor roles",
      headline: "Security+ SY0-701 Prep — Browser Practice for DoD & Contractor Requirements",
      lead:
        "Many federal and defense-contractor roles expect Security+ before you start work. Practice <strong>1000+ SY0-701 questions</strong> and <strong>34 PBQ scenarios</strong> in your browser on duty laptop, CONUS, or TDY—no install. " +
        "Confirm your requirement with your manager. Try <strong>free samples</strong> first.",
      ctaPrimary: "Preview free Security+ samples",
      stickyPrimary: "Free samples",
    },
    "practice-test": {
      id: "practice-test",
      adHeadline: "Security+ Practice Test",
      eyebrow: "Security+ SY0-701 · online practice test",
      headline: "Security+ Practice Test — SY0-701 Questions & PBQs Online",
      lead: BASE_LEAD,
      ctaPrimary: "Start free Security+ sample questions",
      ctaHref: SAMPLE_QUESTIONS,
      stickyPrimary: "Free sample questions",
    },
    "question-bank": {
      id: "question-bank",
      adHeadline: "SY0-701 Question Bank",
      eyebrow: "Security+ question bank · v5.0 objectives",
      headline: "SY0-701 Question Bank — 1000+ Interactive Security+ Questions",
      lead:
        "Work through a large <strong>SY0-701 question bank</strong> with verified explanations—not static PDF answer keys. " +
        "Includes PBQ scenarios and adaptive review. <strong>Try free sample questions in your browser.</strong>",
      ctaPrimary: "Try free Security+ sample questions",
      ctaHref: SAMPLE_QUESTIONS,
      stickyPrimary: "Free sample questions",
    },
    "free-practice": {
      id: "free-practice",
      adHeadline: "Free Security+ Practice",
      eyebrow: "Free Security+ practice · browser samples",
      headline: "Free Security+ Practice — MCQ & 3-Scenario PBQ Preview",
      lead:
        "Try free Security+ samples in your browser: multiple-choice questions and a 3-scenario PBQ preview (dark web IR, WLAN, firewall ACL). " +
        "<strong>No PDFs</strong>, no membership, and no app install.",
      ctaPrimary: "Preview free Security+ samples",
      stickyPrimary: "Free samples",
    },
  };

  var ALIASES = {
    "portal-10d": "portal-10d",
    portal_10d: "portal-10d",
    "pbq-wedge": "pbq-wedge",
    pbq_wedge: "pbq-wedge",
    "sitelink-pbq": "pbq-wedge",
    "timed-sim": "timed-sim",
    "sitelink-sim": "timed-sim",
    federal: "federal",
    "federal-us": "federal",
    "8140": "federal",
    "dod-8140": "federal",
    "practice-test": "practice-test",
    "question-bank": "question-bank",
    "free-practice": "free-practice",
    "sitelink-sample": "free-practice",
    free: "free-practice",
  };

  var TERM_RULES = [
    { re: /\bpbq\b|\bperformance.based\b|\bchain lab\b|\bdark web\b/, id: "pbq-wedge" },
    { re: /\btimed practice\b|\btimed sim\b|\b90.minute\b|\btimed exam\b/, id: "timed-sim" },
    { re: /\bdod\b|\b8140\b|\b8570\b|\bfederal\b|\bcontractor\b|\bgovernment\b/, id: "federal" },
    { re: /\bquestion bank\b|\bsy0-701 question\b/, id: "question-bank" },
    { re: /\bfree security\+ practice\b|\bfree security\+ prep\b|\bfree practice\b/, id: "free-practice" },
    { re: /\bsecurity\+ practice test\b|\bpractice test\b/, id: "practice-test" },
    { re: /\bsy0-701 prep\b|\bsecurity\+ exam prep\b/, id: "portal-10d" },
    { re: /\bsecurity\+ prep\b|\bsecurity\+ practice\b/, id: "practice-test" },
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
    if (key.indexOf("federal") >= 0) return "federal";
    if (key.indexOf("pbq") >= 0) return "pbq-wedge";
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

  function isGooglePaidLanding() {
    return (
      typeof window.bccIsSecplusGooglePaidLanding === "function" &&
      window.bccIsSecplusGooglePaidLanding()
    );
  }

  function withPaidOverrides(variant) {
    if (!isGooglePaidLanding()) return variant;
    var patch = PAID_VARIANT_OVERRIDES[variant.id];
    if (!patch) return variant;
    return Object.assign({}, variant, patch);
  }

  function normalizeGooglePaidPurchaseCta(variant) {
    if (!isGooglePaidLanding()) return variant;
    var href = variant.ctaHref || SAMPLES_SECTION;
    if (href !== "#purchase") return variant;
    var label =
      variant.stickyPrimary && variant.stickyPrimary !== "Free samples" && variant.stickyPrimary !== "Free PBQ preview"
        ? variant.stickyPrimary
        : GOOGLE_PAID_PURCHASE_CTA;
    return Object.assign({}, variant, {
      ctaPrimary: label,
      stickyPrimary: label,
      ctaHref: "#purchase",
    });
  }

  function getVariant(id) {
    return normalizeGooglePaidPurchaseCta(withPaidOverrides(VARIANTS[id] || VARIANTS[DEFAULT_VARIANT]));
  }

  function syncHeroPrimaryCtaPresentation(ctaEl, variant) {
    if (!ctaEl || ctaEl.tagName !== "A") return;
    var href = variant.ctaHref || SAMPLES_SECTION;
    var isPurchaseCta = isGooglePaidLanding() && href === "#purchase";
    ctaEl.classList.toggle("cta-main--free", !isPurchaseCta);
    if (isPurchaseCta) {
      ctaEl.classList.add("cta-main");
    }
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
    if (typeof window.bccShouldTrackAnalytics === "function" && !window.bccShouldTrackAnalytics()) {
      return;
    }
    if (typeof window.gtag !== "function") return;
    var attrs =
      typeof window.bccGetCampaignAttribution === "function" ? window.bccGetCampaignAttribution() : {};
    window.gtag(
      "event",
      "secplus_home_headline_impression",
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

  function resolveCtaHref(path) {
    if (!path || path.charAt(0) === "#") return path;
    return appendCampaignHref(path);
  }

  function getHeroRoot() {
    return document.querySelector(".hero-conversion");
  }

  function applyHeadlineVariant() {
    var hero = getHeroRoot();
    if (!hero) return;

    var picked = resolveVariant();
    var variant = getVariant(picked.id);
    var isDefault = picked.source === "default";

    var eyebrow = document.getElementById("hero-conversion-eyebrow");
    var title = document.getElementById("hero-conversion-title");
    var lead = document.getElementById("hero-conversion-lead");
    var ctaPrimary = document.getElementById("hero-conversion-cta-primary");

    if (!isDefault || hero.getAttribute("data-secplus-hl-pending") === "1") {
      if (eyebrow) eyebrow.textContent = variant.eyebrow;
      if (title) title.textContent = variant.headline;
      if (lead) lead.innerHTML = variant.lead;
      if (ctaPrimary) ctaPrimary.textContent = variant.ctaPrimary;
    }

    if (ctaPrimary && ctaPrimary.tagName === "A") {
      ctaPrimary.setAttribute("href", resolveCtaHref(variant.ctaHref || SAMPLES_SECTION));
      syncHeroPrimaryCtaPresentation(ctaPrimary, variant);
    }

    hero.setAttribute("data-secplus-hl-variant", variant.id);
    hero.removeAttribute("data-secplus-hl-pending");

    trackVariantImpression(variant, picked.source);
    window.bccSecplusHomeHeadlineVariant = variant.id;
    window.bccSecplusHomeHeadlineVariantData = variant;
  }

  function initStickyMobileCta() {
    var hero = getHeroRoot();
    if (!hero) return;

    var variant =
      window.bccSecplusHomeHeadlineVariantData ||
      getVariant(window.bccSecplusHomeHeadlineVariant || DEFAULT_VARIANT);
    var stickyPrimary = variant.stickyPrimary || "Free samples";
    var stickyHref = resolveCtaHref(variant.ctaHref || SAMPLES_SECTION);

    if (document.getElementById("secplusMobileStickyCta")) return;

    var bar = document.createElement("div");
    bar.id = "secplusMobileStickyCta";
    bar.className = "secplus-mobile-sticky-cta";
    bar.setAttribute("role", "region");
    bar.setAttribute("aria-label", "Preview free Security+ samples");
    bar.setAttribute("aria-hidden", "true");
    bar.hidden = true;
    bar.innerHTML =
      '<a class="cta-main cta-main--free secplus-mobile-sticky-cta__primary" href="' +
      stickyHref +
      '">' +
      stickyPrimary +
      "</a>";
    if (isGooglePaidLanding() && stickyHref === "#purchase") {
      bar.querySelector("a").classList.remove("cta-main--free");
      bar.querySelector("a").classList.add("cta-main");
    }
    document.body.appendChild(bar);

    var mq = window.matchMedia("(max-width: 767px)");
    var shown = false;

    function setVisible(next) {
      if (shown === next) return;
      shown = next;
      bar.hidden = !next;
      bar.setAttribute("aria-hidden", next ? "false" : "true");
      bar.classList.toggle("is-visible", next);
      document.body.classList.toggle("secplus-sticky-cta-visible", next);
    }

    function update() {
      if (!mq.matches) {
        setVisible(false);
        return;
      }
      var heroBottom = hero.getBoundingClientRect().bottom;
      setVisible(heroBottom < 72);
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
  }

  function init() {
    applyHeadlineVariant();
    initStickyMobileCta();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
