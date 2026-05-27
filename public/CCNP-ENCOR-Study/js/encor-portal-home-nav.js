/**
 * Registered ENCOR practice pages: Home / logo links → ENCOR_Training_Portal.html
 * (guest sample mode keeps ccnp-home.html).
 */
(function () {
  "use strict";

  var PORTAL = "/CCNP-ENCOR-Study/ENCOR_Training_Portal.html";
  var GUEST_HOME = "/ccnp-home.html";

  function isGuestSample() {
    if (typeof window.isCcnpGuestSample === "function") {
      return window.isCcnpGuestSample();
    }
    try {
      if (new URLSearchParams(location.search).get("sample") === "1") return true;
      return sessionStorage.getItem("ccnpUrlMaskPath") === "/sample";
    } catch (e) {
      return false;
    }
  }

  function isRegisteredEncorPath() {
    var p = (location.pathname || "").toLowerCase();
    if (p.indexOf("/ccnp-encor-study/encor_samples/") >= 0) return false;
    return (
      p.indexOf("/ccnp-encor-study/encor_questions/") >= 0 ||
      p.indexOf("/ccnp-encor-study/ccnp-encor-drag-drop/") >= 0 ||
      p.indexOf("/ccnp-encor-study/ccnp-encor-labs/") >= 0
    );
  }

  function wireEncorPortalHomeLinks() {
    if (!isRegisteredEncorPath()) return;
    var target = isGuestSample() ? GUEST_HOME : PORTAL;
    document.querySelectorAll("a.home-key, a.sim-nav-home").forEach(function (a) {
      a.setAttribute("href", target);
    });
    if (!isGuestSample()) {
      document.querySelectorAll("a.site-logo-corner").forEach(function (a) {
        a.setAttribute("href", PORTAL);
        a.setAttribute("aria-label", "Go to ENCOR training portal");
      });
      document.querySelectorAll("#ccnpQToolbar a").forEach(function (a) {
        if ((a.textContent || "").trim() === "Home") {
          a.setAttribute("href", PORTAL);
        }
      });
    }
  }

  window.bccWireEncorPortalHomeLinks = wireEncorPortalHomeLinks;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", wireEncorPortalHomeLinks);
  } else {
    wireEncorPortalHomeLinks();
  }
})();
