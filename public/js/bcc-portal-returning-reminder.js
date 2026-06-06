/**
 * Quick reminder for returning portal members (CCNA, ENCOR, Security+):
 * fresh content, cache clear, and how to request a new magic link.
 */
(function () {
  "use strict";

  var SHOW_DELAY_MS = 600;
  var ACCESS_POLL_MS = 120;
  var ACCESS_POLL_MAX = 50;

  var CONFIGS = [
    {
      pathMatch: "CCNA_Training_Portal",
      sessionKey: "bcc_portal_returning_reminder_v1_ccna",
      productLabel: "CCNA",
      hasAccess: function () {
        return typeof window.bccPortalAccessActive === "function" && window.bccPortalAccessActive();
      },
      restore: function () {
        if (typeof window.bccRestoreCcnaPortalAccess === "function") {
          return window.bccRestoreCcnaPortalAccess();
        }
        return Promise.resolve(false);
      },
      requestLinkHref: "/CCNA-Study/ccna-portal-request-link.html",
      restoreHref: "/CCNA-Study/ccna-portal-restore-access.html",
    },
    {
      pathMatch: "ENCOR_Training_Portal",
      sessionKey: "bcc_portal_returning_reminder_v1_encor",
      productLabel: "CCNP ENCOR",
      hasAccess: function () {
        return (
          typeof window.bccEncorPortalAccessActive === "function" && window.bccEncorPortalAccessActive()
        );
      },
      restore: function () {
        if (typeof window.bccRestoreEncorPortalAccess === "function") {
          return window.bccRestoreEncorPortalAccess();
        }
        return Promise.resolve(false);
      },
      requestLinkHref: "/CCNP-ENCOR-Study/encor-portal-request-link.html",
      restoreHref: null,
    },
    {
      pathMatch: "SEC+_Training_Portal",
      sessionKey: "bcc_portal_returning_reminder_v1_secplus",
      productLabel: "Security+",
      hasAccess: function () {
        return (
          typeof window.bccSecplusPortalAccessActive === "function" &&
          window.bccSecplusPortalAccessActive()
        );
      },
      restore: function () {
        if (typeof window.bccRestoreSecplusPortalAccess === "function") {
          return window.bccRestoreSecplusPortalAccess();
        }
        return Promise.resolve(false);
      },
      requestLinkHref: "/COMP_TIA_SEC+/secplus-portal-request-link.html",
      restoreHref: "/COMP_TIA_SEC+/secplus-portal-restore-access.html",
    },
  ];

  var hadCheckoutSessionId = false;
  try {
    var sid = new URLSearchParams(window.location.search).get("session_id");
    hadCheckoutSessionId = !!(sid && sid.indexOf("cs_") === 0);
  } catch (e) {}

  var cfg = null;
  var root = null;
  var shown = false;

  function detectConfig() {
    var path = window.location.pathname || "";
    for (var i = 0; i < CONFIGS.length; i++) {
      if (path.indexOf(CONFIGS[i].pathMatch) >= 0) return CONFIGS[i];
    }
    return null;
  }

  function isFreshCheckoutActivation() {
    if (hadCheckoutSessionId) return true;
    var banner = document.getElementById("portal-checkout-activated-banner");
    return !!(banner && !banner.hidden);
  }

  function alreadyShownThisSession() {
    try {
      return sessionStorage.getItem(cfg.sessionKey) === "1";
    } catch (e) {
      return false;
    }
  }

  function markShownThisSession() {
    try {
      sessionStorage.setItem(cfg.sessionKey, "1");
    } catch (e) {}
  }

  function waitForAccess() {
    return new Promise(function (resolve) {
      var tries = 0;
      function poll() {
        if (cfg.hasAccess()) {
          resolve(true);
          return;
        }
        tries += 1;
        if (tries >= ACCESS_POLL_MAX) {
          resolve(false);
          return;
        }
        setTimeout(poll, ACCESS_POLL_MS);
      }
      Promise.resolve()
        .then(function () {
          return cfg.restore();
        })
        .finally(poll);
    });
  }

  function buildStepsHtml() {
    var restoreStep = "";
    if (cfg.restoreHref) {
      restoreStep =
        "<li>Or paste your Stripe checkout session ID (<code>cs_…</code>) on " +
        '<a href="' +
        cfg.restoreHref +
        '">Restore access</a>.</li>';
    }
    return (
      "<ol class=\"bcc-portal-reminder-steps\">" +
      "<li><strong>See the latest questions:</strong> hard refresh this page " +
      "(<kbd>Cmd+Shift+R</kbd> on Mac, <kbd>Ctrl+Shift+R</kbd> on Windows) or clear site data / cache for " +
      "<strong>becertifiedtoday.com</strong> in your browser settings.</li>" +
      "<li><strong>New device or browser?</strong> Open " +
      '<a href="' +
      cfg.requestLinkHref +
      '">Email me a portal link</a>.</li>' +
      "<li>Enter the <strong>same email you used at Stripe checkout</strong> for " +
      cfg.productLabel +
      " access.</li>" +
      "<li>Open the <strong>magic link</strong> in the email we send (check spam if needed).</li>" +
      restoreStep +
      "</ol>"
    );
  }

  function closeModal() {
    if (!root) return;
    root.classList.remove("ccna-sim-promo-root--open");
    root.setAttribute("aria-hidden", "true");
    document.documentElement.classList.remove("bcc-portal-reminder-open");
  }

  function openModal() {
    if (!root || shown) return;
    shown = true;
    markShownThisSession();
    root.classList.add("ccna-sim-promo-root--open");
    root.setAttribute("aria-hidden", "false");
    document.documentElement.classList.add("bcc-portal-reminder-open");
    var closeBtn = root.querySelector(".ccna-sim-promo-close");
    if (closeBtn) closeBtn.focus();
  }

  function wireModal() {
    if (!root) return;
    root.querySelectorAll("[data-bcc-portal-reminder-dismiss]").forEach(function (el) {
      el.addEventListener("click", function () {
        closeModal();
      });
    });
    document.addEventListener("keydown", function (ev) {
      if (ev.key === "Escape" && root.classList.contains("ccna-sim-promo-root--open")) {
        closeModal();
      }
    });
  }

  function injectModal() {
    root = document.createElement("div");
    root.id = "bccPortalReturningReminder";
    root.className = "ccna-sim-promo-root";
    root.hidden = true;
    root.setAttribute("role", "presentation");
    root.setAttribute("aria-hidden", "true");
    root.innerHTML =
      '<div class="ccna-sim-promo-backdrop" data-bcc-portal-reminder-dismiss tabindex="-1" aria-hidden="true"></div>' +
      '<div class="ccna-sim-promo-panel" role="dialog" aria-modal="true" aria-labelledby="bccPortalReturningReminderTitle">' +
      '<button type="button" class="ccna-sim-promo-close" data-bcc-portal-reminder-dismiss aria-label="Close">&times;</button>' +
      '<p class="ccna-sim-promo-eyebrow">Welcome back</p>' +
      '<h2 id="bccPortalReturningReminderTitle">New questions and updates land often</h2>' +
      "<p class=\"ccna-sim-promo-lead\">" +
      "We add <strong>new practice questions, drag-and-drop sets, and portal updates</strong> regularly. " +
      "Clear cached pages so you always see the latest content." +
      "</p>" +
      buildStepsHtml() +
      '<div class="ccna-sim-promo-actions">' +
      '<a class="ccna-sim-promo-primary" href="' +
      cfg.requestLinkHref +
      '">Email me a new magic link</a>' +
      '<button type="button" class="ccna-sim-promo-secondary" data-bcc-portal-reminder-dismiss>Got it</button>' +
      "</div>" +
      "</div>";
    document.body.appendChild(root);
    root.hidden = false;
    wireModal();
  }

  function maybeShowReminder() {
    if (!cfg || shown) return;
    if (isFreshCheckoutActivation()) return;
    if (alreadyShownThisSession()) return;

    waitForAccess().then(function (active) {
      if (!active || shown || isFreshCheckoutActivation()) return;
      setTimeout(openModal, SHOW_DELAY_MS);
    });
  }

  function init() {
    cfg = detectConfig();
    if (!cfg) return;
    injectModal();
    maybeShowReminder();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
