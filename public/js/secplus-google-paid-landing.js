/**
 * CompTIA Security+ home — Google Ads paid traffic: 30-day offer only.
 * Detects utm_source=google or gclid; disables 10-day purchase, popups, and sticky offers.
 */
(function () {
  "use strict";

  var HTML_CLASS = "secplus-landing-google-paid";

  function readQueryParam(key) {
    try {
      return new URLSearchParams(window.location.search).get(key);
    } catch (e) {
      return null;
    }
  }

  function readAttribution() {
    if (typeof window.bccGetCampaignAttribution === "function") {
      return window.bccGetCampaignAttribution() || {};
    }
    return {};
  }

  function isGooglePaidLanding() {
    var attrs = readAttribution();
    var source = (readQueryParam("utm_source") || attrs.utm_source || "").toLowerCase();
    var gclid = readQueryParam("gclid") || attrs.gclid || "";
    if (gclid) return true;
    return source === "google";
  }

  function applyDomState() {
    if (!isGooglePaidLanding()) return;
    document.documentElement.classList.add(HTML_CLASS);

    var callout = document.getElementById("secplusGooglePaidCallout");
    if (callout) {
      callout.hidden = false;
      callout.removeAttribute("hidden");
    }

    var defaultBlock = document.getElementById("secplusPurchaseDefault");
    var tenDayBlock = document.getElementById("secplusPurchase10d");
    var purchase = document.getElementById("purchase");
    if (defaultBlock) {
      defaultBlock.hidden = false;
      defaultBlock.removeAttribute("hidden");
    }
    if (tenDayBlock) {
      tenDayBlock.hidden = true;
      tenDayBlock.setAttribute("hidden", "");
    }
    if (purchase) {
      purchase.classList.remove("purchase-fold--single-offer");
    }

    ["secplus10dOfferRoot", "secplus10dLastChanceBar", "secplusLeadStickyCta"].forEach(function (id) {
      var el = document.getElementById(id);
      if (!el) return;
      el.hidden = true;
      el.setAttribute("hidden", "");
    });
  }

  window.bccIsSecplusGooglePaidLanding = isGooglePaidLanding;

  if (isGooglePaidLanding()) {
    document.documentElement.classList.add(HTML_CLASS);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", applyDomState);
  } else {
    applyDomState();
  }
})();
