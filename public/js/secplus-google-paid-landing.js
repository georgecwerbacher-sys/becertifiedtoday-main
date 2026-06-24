/**
 * CompTIA Security+ home — Google Ads paid traffic callout.
 * Detects utm_source=google or gclid; shows course-contrast note for Messer/Dion shoppers.
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
