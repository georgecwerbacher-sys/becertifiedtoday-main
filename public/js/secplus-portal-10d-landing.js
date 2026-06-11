/**
 * CompTIA Security+ home — Google Ads `secplus_portal_10d` landing (`utm_content=portal-10d`).
 * Purchase fold shows 10-day $9.99 as the only primary CTA; scrolls to #purchase.
 */
(function () {
  "use strict";

  var UTM_RE = /portal-10d|portal_10d/i;

  function readUtmContent() {
    try {
      return new URLSearchParams(window.location.search).get("utm_content") || "";
    } catch (e) {
      return "";
    }
  }

  function readAttributionContent() {
    if (typeof window.bccGetCampaignAttribution === "function") {
      var attrs = window.bccGetCampaignAttribution() || {};
      if (attrs.utm_content) return attrs.utm_content;
    }
    return "";
  }

  function isPortal10dLanding() {
    var content = readUtmContent() || readAttributionContent();
    return UTM_RE.test(content);
  }

  function applyPurchaseVariant() {
    var defaultBlock = document.getElementById("secplusPurchaseDefault");
    var tenDayBlock = document.getElementById("secplusPurchase10d");
    var purchase = document.getElementById("purchase");
    if (!defaultBlock || !tenDayBlock || !purchase) return;

    defaultBlock.hidden = true;
    tenDayBlock.hidden = false;
    purchase.classList.add("purchase-fold--single-offer");
  }

  function scrollToPurchase() {
    var purchase = document.getElementById("purchase");
    if (!purchase) return;
    if (location.hash === "#purchase") {
      purchase.scrollIntoView({ behavior: "smooth", block: "start" });
      return;
    }
    window.requestAnimationFrame(function () {
      purchase.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }

  if (isPortal10dLanding()) {
    document.documentElement.classList.add("secplus-landing-portal-10d");
  }

  function init() {
    if (!isPortal10dLanding()) return;
    applyPurchaseVariant();
    scrollToPurchase();
  }

  window.bccIsSecplusPortal10dLanding = isPortal10dLanding;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
