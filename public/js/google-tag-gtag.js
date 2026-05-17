/**
 * Google tag (gtag.js) — inline init per GA setup assistant.
 * Load immediately after https://www.googletagmanager.com/gtag/js?id=...
 */
(function () {
  "use strict";
  var id = window.__BCC_GA_MEASUREMENT_ID__ || "G-YTT6KBHX7V";
  if (!id || window.__bccGaConfigured) return;
  window.__bccGaConfigured = true;
  window.dataLayer = window.dataLayer || [];
  function gtag() {
    window.dataLayer.push(arguments);
  }
  window.gtag = gtag;
  gtag("js", new Date());
  gtag("config", id, { anonymize_ip: true });
})();
