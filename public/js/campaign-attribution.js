/**
 * Captures Google Ads / UTM parameters and attaches them to GA4 events for the session.
 * Load after /js/google-tag-gtag.js on marketing landing pages.
 */
(function () {
  "use strict";

  var STORAGE_KEY = "bcc_campaign_attribution_v1";
  var PARAMS = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "gclid"];

  function paramsFromSearchString(search) {
    var out = {};
    if (!search) return out;
    try {
      var qs = new URLSearchParams(search.charAt(0) === "?" ? search.slice(1) : search);
      PARAMS.forEach(function (key) {
        var val = qs.get(key);
        if (val) out[key] = val;
      });
    } catch (e) {
      /* ignore */
    }
    return out;
  }

  function readQuery() {
    var out = paramsFromSearchString(window.location.search || "");
    if (Object.keys(out).length) return out;

    // Google Ads sitelinks often use ccna-home.html#purchase?utm_source=… — UTMs after # are not in location.search.
    var hash = window.location.hash || "";
    var qIndex = hash.indexOf("?");
    if (qIndex >= 0) {
      out = paramsFromSearchString(hash.slice(qIndex));
    }
    return out;
  }

  function loadStored() {
    try {
      var raw = sessionStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch (e) {
      return {};
    }
  }

  function saveStored(data) {
    try {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    } catch (e) {
      /* ignore */
    }
  }

  function mergeAttribution() {
    var stored = loadStored();
    var incoming = readQuery();
    var merged = Object.assign({}, stored, incoming);
    if (Object.keys(incoming).length) saveStored(merged);
    return merged;
  }

  function campaignFields(attrs) {
    return {
      source: attrs.utm_source || undefined,
      medium: attrs.utm_medium || undefined,
      campaign: attrs.utm_campaign || undefined,
      content: attrs.utm_content || undefined,
      term: attrs.utm_term || undefined,
      gclid: attrs.gclid || undefined,
    };
  }

  function gtagEvent(name, params) {
    if (typeof window.bccShouldTrackAnalytics === "function" && !window.bccShouldTrackAnalytics()) {
      return;
    }
    if (typeof window.gtag !== "function") return;
    window.gtag("event", name, params);
  }

  function parseMoney(raw, fallback) {
    var n = Number(raw);
    return Number.isFinite(n) ? n : fallback;
  }

  function trackCheckout(el) {
    var attrs = mergeAttribution();
    var fields = campaignFields(attrs);
    var itemId = el.getAttribute("data-bcc-item-id") || "ccna_portal";
    var itemName = el.getAttribute("data-bcc-item-name") || itemId;
    var value = parseMoney(el.getAttribute("data-bcc-value"), 0);
    var currency = el.getAttribute("data-bcc-currency") || "USD";
    gtagEvent("begin_checkout", Object.assign(
      {
        currency: currency,
        value: value,
        items: [{ item_id: itemId, item_name: itemName, price: value, quantity: 1 }],
      },
      fields
    ));
  }

  function bindCheckoutTracking() {
    var selector =
      "[data-bcc-track='begin_checkout'], .bcc-track-checkout, " +
      "[data-ccna-portal-10d-checkout], [data-ccna-portal-30d-checkout], " +
      "[data-encor-portal-10d-checkout], [data-encor-portal-30d-checkout], " +
      "[data-secplus-portal-10d-checkout], [data-secplus-portal-30d-checkout]";
    document.querySelectorAll(selector).forEach(function (el) {
      if (el.dataset.bccCheckoutBound === "1") return;
      el.dataset.bccCheckoutBound = "1";
      el.addEventListener("click", function () {
        trackCheckout(el);
      });
    });
  }

  var attribution = mergeAttribution();
  if (
    typeof window.gtag === "function" &&
    Object.keys(attribution).length &&
    (typeof window.bccShouldTrackAnalytics !== "function" || window.bccShouldTrackAnalytics())
  ) {
    var id = window.__BCC_GA_MEASUREMENT_ID__ || "G-YTT6KBHX7V";
    window.gtag("config", id, campaignFields(attribution));
  }

  window.bccGetCampaignAttribution = function () {
    return mergeAttribution();
  };
  window.bccTrackBeginCheckout = trackCheckout;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bindCheckoutTracking);
  } else {
    bindCheckoutTracking();
  }
})();
