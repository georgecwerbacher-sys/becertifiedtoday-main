/**
 * Registered ENCOR practice pages: Home / logo links → ccnp-home.html only.
 * Portal entry is the top-right link on public/ccnp-home.html (not content pages).
 */
(function () {
  "use strict";

  var PUBLIC_HOME = "/ccnp-home.html";

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
    document.querySelectorAll("a.home-key, a.sim-nav-home, a.site-logo-corner").forEach(function (a) {
      a.setAttribute("href", PUBLIC_HOME);
    });
    document.querySelectorAll("#ccnpQToolbar a").forEach(function (a) {
      if ((a.textContent || "").trim() === "Home") {
        a.setAttribute("href", PUBLIC_HOME);
      }
    });
  }

  window.bccWireEncorPortalHomeLinks = wireEncorPortalHomeLinks;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", wireEncorPortalHomeLinks);
  } else {
    wireEncorPortalHomeLinks();
  }
})();
