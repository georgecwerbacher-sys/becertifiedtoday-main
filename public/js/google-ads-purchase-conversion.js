/**
 * Google Ads purchase conversion (deduped by Stripe checkout session id).
 * Requires gtag + ga-site-config (AW-18158574148 + conversion label).
 */
(function (global) {
  "use strict";

  var ADS_ID = global.__BCC_GOOGLE_ADS_ID__ || "AW-18158574148";
  var LABEL =
    global.__BCC_GOOGLE_ADS_PURCHASE_CONVERSION_LABEL__ ||
    global.__BCC_GOOGLE_ADS_CCNA_SIM_CONVERSION_LABEL__ ||
    "";

  function trackPurchaseConversion(transactionId, opts) {
    opts = opts || {};
    if (!transactionId || typeof global.gtag !== "function" || !ADS_ID || !LABEL) {
      return false;
    }
    var tx = String(transactionId);
    var trackKey = "bcc_gads_purchase_" + tx;
    try {
      if (global.localStorage.getItem(trackKey) === "1") return false;
    } catch (e) {}

    var params = {
      send_to: ADS_ID + "/" + LABEL,
      transaction_id: tx,
    };
    if (typeof opts.value === "number" && Number.isFinite(opts.value)) {
      params.value = opts.value;
    }
    if (opts.currency) {
      params.currency = String(opts.currency);
    }

    global.gtag("event", "conversion", params);
    try {
      global.localStorage.setItem(trackKey, "1");
    } catch (e) {}
    return true;
  }

  global.bccTrackGoogleAdsPurchaseConversion = trackPurchaseConversion;
})(typeof window !== "undefined" ? window : this);
