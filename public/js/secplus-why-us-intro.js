/**
 * Security+ home - one-time intro popup (session).
 * Pain-point CTA: not PDF/VCE/email-course funnels; browser prep via Stripe.
 */
(function () {
  "use strict";

  var STORAGE_KEY = "bcc_secplus_why_us_intro_v1";
  var ROOT_ID = "secplusWhyUsIntroRoot";
  var OPEN_DELAY_MS = 700;

  function isSecplusHome() {
    var p = (location.pathname || "").toLowerCase();
    return p.indexOf("comptia-sec+-home") >= 0;
  }

  function wasSeen() {
    try {
      return sessionStorage.getItem(STORAGE_KEY) === "1";
    } catch (_) {
      return false;
    }
  }

  function markSeen() {
    try {
      sessionStorage.setItem(STORAGE_KEY, "1");
    } catch (_) {}
  }

  function isPortalMember() {
    return (
      typeof window.bccSecplusPortalAccessActive === "function" &&
      window.bccSecplusPortalAccessActive()
    );
  }

  function close(root) {
    if (!root) return;
    root.classList.remove("secplus-why-us-intro--open");
    root.setAttribute("aria-hidden", "true");
    document.documentElement.classList.remove("secplus-why-us-intro-open");
    markSeen();
  }

  function open(root) {
    if (!root || wasSeen() || isPortalMember()) return;
    root.classList.add("secplus-why-us-intro--open");
    root.setAttribute("aria-hidden", "false");
    document.documentElement.classList.add("secplus-why-us-intro-open");
    var panel = root.querySelector(".secplus-why-us-intro__panel");
    if (panel) {
      try {
        panel.focus();
      } catch (_) {}
    }
  }

  function build() {
    if (document.getElementById(ROOT_ID)) return document.getElementById(ROOT_ID);

    var root = document.createElement("div");
    root.id = ROOT_ID;
    root.className = "secplus-why-us-intro";
    root.setAttribute("aria-hidden", "true");
    root.innerHTML =
      '<div class="secplus-why-us-intro__backdrop" data-why-us-dismiss></div>' +
      '<div class="secplus-why-us-intro__panel" role="dialog" aria-modal="true" aria-labelledby="secplusWhyUsIntroTitle" tabindex="-1">' +
      '<button type="button" class="secplus-why-us-intro__close" data-why-us-dismiss aria-label="Close">&times;</button>' +
      '<p class="secplus-why-us-intro__eyebrow">You found us</p>' +
      '<h2 id="secplusWhyUsIntroTitle" class="secplus-why-us-intro__title">Tired of expensive PDFs, VCE files, and course bait?</h2>' +
      '<p class="secplus-why-us-intro__lead">So were we. Here is the short version.</p>' +
      '<ul class="secplus-why-us-intro__list">' +
      "<li><strong>Expensive PDF downloads</strong> packed with irrelevant questions? Same frustration.</li>" +
      "<li><strong>VCE packs</strong> that cost too much and are not PBQ-friendly? Us too.</li>" +
      "<li><strong>Email gates</strong> that exist to spam you later? Skip that.</li>" +
      "<li><strong>Free samples</strong> that only push expensive courses? You do not need another course.</li>" +
      "<li><strong>AI sites</strong> inventing filler questions? Not here.</li>" +
      "</ul>" +
      '<p class="secplus-why-us-intro__body">' +
      "We pull strong practice from forum discussions and current study materials, then give you browser access " +
      "at about <strong>half the price of a typical PDF download</strong>. Mobile-friendly. PBQ scenarios. Adaptive review. " +
      "No AI-generated questions. No subscription. No email required for access - just one Stripe payment." +
      "</p>" +
      '<div class="secplus-why-us-intro__actions">' +
      '<a class="secplus-why-us-intro__primary" href="#purchase" data-secplus-portal-30d-checkout data-why-us-dismiss>Get 30-day access</a>' +
      '<a class="secplus-why-us-intro__secondary" href="#home-secplus-samples-title" data-why-us-dismiss>Preview free samples</a>' +
      "</div>" +
      "</div>";

    document.body.appendChild(root);

    root.querySelectorAll("[data-why-us-dismiss]").forEach(function (el) {
      el.addEventListener("click", function () {
        close(root);
      });
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && root.classList.contains("secplus-why-us-intro--open")) {
        close(root);
      }
    });

    return root;
  }

  function init() {
    if (!isSecplusHome() || wasSeen() || isPortalMember()) return;
    var root = build();
    window.setTimeout(function () {
      open(root);
    }, OPEN_DELAY_MS);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
