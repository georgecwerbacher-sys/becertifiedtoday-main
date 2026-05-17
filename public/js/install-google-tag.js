/**
 * Injects Google tag (gtag.js) into <head> when not already present (CCNA questions, labs, DnD).
 */
(function () {
  "use strict";

  var MEASUREMENT_ID = "G-YTT6KBHX7V";
  var path = (location.pathname || "").toLowerCase();
  if (path.indexOf("/admin/") === 0) return;
  try {
    if (new URLSearchParams(location.search).get("examSim") === "1") return;
  } catch (_) {}

  var head = document.head || document.getElementsByTagName("head")[0];
  if (!head || head.querySelector('script[data-bcc-gtag="1"]')) return;

  window.__BCC_GA_MEASUREMENT_ID__ = window.__BCC_GA_MEASUREMENT_ID__ || MEASUREMENT_ID;

  var loader = document.createElement("script");
  loader.async = true;
  loader.src =
    "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(MEASUREMENT_ID);
  loader.setAttribute("data-bcc-gtag", "1");
  head.appendChild(loader);

  var init = document.createElement("script");
  init.src = "/js/google-tag-gtag.js";
  init.setAttribute("data-bcc-gtag", "1");
  head.appendChild(init);
})();
