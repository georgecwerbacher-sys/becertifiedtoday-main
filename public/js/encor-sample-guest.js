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

      document.querySelectorAll("a.home-key, a.sim-nav-home").forEach(function (a) {
        a.href = HOME;
        a.textContent = "Home";
      });

      document.querySelectorAll("nav.sim-nav a.sim-nav-btn").forEach(function (a) {
        if (a.classList.contains("sim-nav-home")) return;
        a.remove();
      });

      if (document.querySelector("nav[data-encor-sample-nav]")) return;

      if (!document.getElementById("ccnp-sample-nav-style")) {
        var st = document.createElement("style");
        st.id = "ccnp-sample-nav-style";
        st.textContent =
          "body.ccnp-sample-guest a.home-key{display:none!important;}" +
          "body.ccnp-sample-guest .sim-nav .sim-nav-home{display:none!important;}" +
          "body.ccnp-sample-guest,body.ccnp-practice-ui{padding-bottom:calc(72px + env(safe-area-inset-bottom,0px))!important;}" +
          "nav[data-encor-sample-nav]{position:fixed;left:0;right:0;bottom:0;z-index:10000;display:flex;justify-content:center;padding:12px 16px calc(12px + env(safe-area-inset-bottom,0px));background:rgba(11,16,32,.94);border-top:1px solid #2d3b5a;backdrop-filter:blur(10px);}" +
          "nav[data-encor-sample-nav] a{text-decoration:none;background:#1a3d6e;border:1px solid #3d6dbb;color:#e6edf3;border-radius:10px;padding:10px 18px;font-weight:700;min-width:5.5rem;text-align:center;}";
        document.head.appendChild(st);
      }

      document.body.classList.add("ccnp-sample-guest");

      var nav = document.createElement("nav");
      nav.setAttribute("data-encor-sample-nav", "1");
      nav.setAttribute("aria-label", "Sample navigation");
      var homeTab = document.createElement("a");
      homeTab.href = HOME;
      homeTab.textContent = "Home";
      nav.appendChild(homeTab);
      document.body.appendChild(nav);
    };
  }
})();
