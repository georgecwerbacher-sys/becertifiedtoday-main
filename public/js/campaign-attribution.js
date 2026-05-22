/**
 * Captures Google Ads / UTM parameters and attaches them to GA4 events for the session.
 * Load after /js/google-tag-gtag.js on marketing landing pages.
 */
(function () {
  "use strict";

  var STORAGE_KEY = "bcc_campaign_attribution_v1";
  var PARAMS = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "gclid"];

  function readQuery() {
    var out = {};
    try {
      var qs = new URLSearchParams(window.location.search);
      PARAMS.forEach(function (key) {
        var val = qs.get(key);
        if (val) out[key] = val;
      });
    } catch (e) {
      /* ignore */
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
      campaign_source: attrs.utm_source || undefined,
      campaign_medium: attrs.utm_medium || undefined,
      campaign_name: attrs.utm_campaign || undefined,
      campaign_content: attrs.utm_content || undefined,
      campaign_term: attrs.utm_term || undefined,
      gclid: attrs.gclid || undefined,
    };
  }

  function gtagEvent(name, params) {
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
      "[data-bcc-track='begin_checkout'], .bcc-track-checkout, [data-ccna-portal-10d-checkout], [data-ccna-portal-30d-checkout]";
    document.querySelectorAll(selector).forEach(function (el) {
      if (el.dataset.bccCheckoutBound === "1") return;
      el.dataset.bccCheckoutBound = "1";
      el.addEventListener("click", function () {
        trackCheckout(el);
      });
    });
  }

  var attribution = mergeAttribution();
  if (typeof window.gtag === "function" && Object.keys(attribution).length) {
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
