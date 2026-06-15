/**
 * Opt out of GA4 / Google Ads / Vercel analytics for:
 * - admin, local dev, internal testers
 * - member study library (unless active free-sample session)
 *
 * Marketing-only tagging policy: scripts/marketing-tag-minimal-list.md
 * Load synchronously after ga-site-config.js and before gtag/js.
 */
(function () {
  "use strict";

  var LS_EXCLUDE = "bcc_analytics_exclude_v1";
  var LS_EMAIL_KEYS = [
    "bcc_ccna_free_sim_v1",
    "bcc_encor_free_sim_v1",
    "bcc_secplus_free_sim_v1",
  ];
  var DEFAULT_INTERNAL = ["georgecwerbacher@gmail.com", "georeg.werbacher@gmail.com"];

  function pathLower() {
    return (location.pathname || "").toLowerCase();
  }

  function isMarketingConversionPath() {
    var p = pathLower();
    if (p === "/" || p === "/index.html") return true;
    if (p === "/ccna-home.html") return true;
    if (p === "/ccnp-home.html") return true;
    if (p === "/comptia-sec+-home.html") return true;
    if (p === "/ccna/labs-without-gns3.html") return true;
    if (p === "/sample" || p === "/sample.html") return true;
    if (p.indexOf("ccna-portal-30d-checkout-success") !== -1) return true;
    if (p.indexOf("ccna-portal-10d-checkout-success") !== -1) return true;
    if (p.indexOf("secplus-portal-checkout-success") !== -1) return true;
    return false;
  }

  function isFreeSampleSession() {
    try {
      if (/(?:\?|&)sample=1(?:&|$)/.test(location.search || "")) return true;
      if (sessionStorage.getItem("ccnaHomeSample")) return true;
      if (sessionStorage.getItem("encorHomeSample")) return true;
      if (sessionStorage.getItem("secplusHomeSample")) return true;
    } catch (_) {}
    return false;
  }

  function isMemberStudyPath() {
    var p = pathLower();
    if (p.indexOf("/ccna-study/") === 0) return true;
    if (p.indexOf("/ccnp-encor-study/") === 0) return true;
    if (p.indexOf("/comp_tia_sec+/") === 0) return true;
    if (p.indexOf("/ccna_sim_exam/") === 0) return true;
    if (p === "/practice-launcher.html") return true;
    return false;
  }

  function shouldLoadMarketingTag() {
    if (isMarketingConversionPath()) return true;
    if (isFreeSampleSession() && isMemberStudyPath()) return true;
    return false;
  }

  function normalizeEmail(email) {
    return String(email || "").trim().toLowerCase();
  }

  function internalEmails() {
    var list = window.__BCC_INTERNAL_EMAILS__;
    if (!Array.isArray(list) || !list.length) list = DEFAULT_INTERNAL;
    return list.map(normalizeEmail).filter(Boolean);
  }

  function isInternalEmail(email) {
    var em = normalizeEmail(email);
    if (!em) return false;
    return internalEmails().indexOf(em) >= 0;
  }

  function isLocalHost() {
    var h = (location.hostname || "").toLowerCase();
    return (
      h === "localhost" ||
      h === "127.0.0.1" ||
      h === "[::1]" ||
      h === "0.0.0.0" ||
      h.slice(-6) === ".local"
    );
  }

  function isAdminPath() {
    return pathLower().indexOf("/admin/") === 0;
  }

  function readOptOutFlag() {
    try {
      return localStorage.getItem(LS_EXCLUDE) === "1";
    } catch (_) {
      return false;
    }
  }

  function emailFromStorageKey(key) {
    try {
      var raw = localStorage.getItem(key);
      if (!raw) return "";
      var o = JSON.parse(raw);
      return normalizeEmail(o && o.email);
    } catch (_) {
      return "";
    }
  }

  function storedEmailIsInternal() {
    for (var i = 0; i < LS_EMAIL_KEYS.length; i++) {
      if (isInternalEmail(emailFromStorageKey(LS_EMAIL_KEYS[i]))) return true;
    }
    return false;
  }

  function hasAdminSession() {
    try {
      return Boolean(sessionStorage.getItem("bcc_admin_analytics_token"));
    } catch (_) {
      return false;
    }
  }

  function queryOptOut() {
    try {
      return new URLSearchParams(location.search).get("bcc_no_analytics") === "1";
    } catch (_) {
      return false;
    }
  }

  function applyGaDisable() {
    var id = window.__BCC_GA_MEASUREMENT_ID__ || "G-YTT6KBHX7V";
    var adsId = window.__BCC_GOOGLE_ADS_ID__ || "";
    try {
      window["ga-disable-" + id] = true;
      if (adsId) window["ga-disable-" + adsId] = true;
    } catch (_) {}
  }

  function computeExcludeReason() {
    if (isAdminPath()) return "admin_path";
    if (isLocalHost()) return "localhost";
    if (readOptOutFlag()) return "opt_out";
    if (hasAdminSession()) return "admin_session";
    if (storedEmailIsInternal()) return "internal_email";
    if (queryOptOut()) return "query_opt_out";
    if (!shouldLoadMarketingTag()) return "marketing_scope";
    return "";
  }

  window.bccIsMarketingConversionPath = isMarketingConversionPath;
  window.bccIsFreeSampleSession = isFreeSampleSession;
  window.bccIsMemberStudyPath = isMemberStudyPath;
  window.bccShouldLoadMarketingTag = shouldLoadMarketingTag;
  window.bccIsInternalAnalyticsEmail = isInternalEmail;

  window.bccSetAnalyticsExclude = function (on) {
    try {
      if (on) localStorage.setItem(LS_EXCLUDE, "1");
      else localStorage.removeItem(LS_EXCLUDE);
    } catch (_) {}
    if (on) {
      window.__bccAnalyticsExclude = true;
      window.__bccAnalyticsExcludeReason = "opt_out";
      applyGaDisable();
    } else {
      window.__bccAnalyticsExclude = false;
      window.__bccAnalyticsExcludeReason = "";
    }
  };

  var reason = computeExcludeReason();
  if (queryOptOut()) {
    window.bccSetAnalyticsExclude(true);
    reason = "opt_out";
  }

  window.__bccAnalyticsExclude = Boolean(reason);
  window.__bccAnalyticsExcludeReason = reason || "";
  if (window.__bccAnalyticsExclude) applyGaDisable();

  window.bccShouldTrackAnalytics = function () {
    return !window.__bccAnalyticsExclude;
  };
})();
