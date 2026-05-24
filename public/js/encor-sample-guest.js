/** ENCOR guest sample helpers (Home → /ccnp-home.html). Loaded by encor-sample-guest.js and practice-questions.js. */
(function () {
  "use strict";

  var HOME = "/ccnp-home.html";

  if (!window.isCcnpGuestSample) {
    window.isCcnpGuestSample = function () {
      try {
        if (new URLSearchParams(location.search).get("sample") === "1") return true;
        return sessionStorage.getItem("ccnpUrlMaskPath") === "/sample";
      } catch (e) {
        return false;
      }
    };
  }

  if (!window.applyEncorSampleGuestChrome) {
    window.applyEncorSampleGuestChrome = function () {
      if (!window.isCcnpGuestSample()) return;

      document.querySelectorAll("nav[data-encor-sample-nav]").forEach(function (nav) {
        nav.remove();
      });
      document.body.classList.remove("ccnp-sample-guest");

      document.querySelectorAll("a.home-key, a.sim-nav-home").forEach(function (a) {
        a.href = HOME;
        a.textContent = "Home";
      });

      document.querySelectorAll("nav.sim-nav a.sim-nav-btn").forEach(function (a) {
        if (a.classList.contains("sim-nav-home")) return;
        a.remove();
      });
    };
  }
})();
