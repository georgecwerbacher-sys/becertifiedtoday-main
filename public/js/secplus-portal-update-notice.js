/**
 * One-time Security+ portal update notice (SY0-701 refresh).
 * Shows on first visit to SEC+_Training_Portal until dismissed.
 */
(function () {
  "use strict";

  var SHOW_DELAY_MS = 600;
  var DISMISS_KEY = "bcc_secplus_sy0_701_update_notice_v1";
  var REQUEST_LINK_HREF = "/COMP_TIA_SEC+/secplus-portal-request-link.html";
  var PATH_MATCH = "SEC+_Training_Portal";

  var root = null;
  var shown = false;

  function isPortalPage() {
    return (window.location.pathname || "").indexOf(PATH_MATCH) >= 0;
  }

  function isFreshCheckoutActivation() {
    try {
      var sid = new URLSearchParams(window.location.search).get("session_id");
      if (sid && sid.indexOf("cs_") === 0) return true;
    } catch (e) {}
    var banner = document.getElementById("portal-checkout-activated-banner");
    return !!(banner && !banner.hidden);
  }

  function wasDismissed() {
    try {
      return localStorage.getItem(DISMISS_KEY) === "1";
    } catch (e) {
      return false;
    }
  }

  function markDismissed() {
    try {
      localStorage.setItem(DISMISS_KEY, "1");
    } catch (e) {}
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
    markDismissed();
    root.classList.add("ccna-sim-promo-root--open");
    root.setAttribute("aria-hidden", "false");
    document.documentElement.classList.add("bcc-portal-reminder-open");
    var closeBtn = root.querySelector(".ccna-sim-promo-close");
    if (closeBtn) closeBtn.focus();
  }

  function wireModal() {
    if (!root) return;
    root.querySelectorAll("[data-secplus-update-dismiss]").forEach(function (el) {
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
    root.id = "secplusPortalUpdateNotice";
    root.className = "ccna-sim-promo-root";
    root.hidden = true;
    root.setAttribute("role", "presentation");
    root.setAttribute("aria-hidden", "true");
    root.innerHTML =
      '<div class="ccna-sim-promo-backdrop" data-secplus-update-dismiss tabindex="-1" aria-hidden="true"></div>' +
      '<div class="ccna-sim-promo-panel" role="dialog" aria-modal="true" aria-labelledby="secplusPortalUpdateNoticeTitle">' +
      '<button type="button" class="ccna-sim-promo-close" data-secplus-update-dismiss aria-label="Close">&times;</button>' +
      '<p class="ccna-sim-promo-eyebrow">Portal update</p>' +
      '<h2 id="secplusPortalUpdateNoticeTitle">Security+ portal refreshed for SY0-701</h2>' +
      '<p class="ccna-sim-promo-lead ccna-sim-promo-lead--compact">' +
      "Outdated <strong>SY0-601</strong> questions were removed from active Random and Review pools. " +
      "The portal layout was updated to match <strong>SY0-701</strong>." +
      "</p>" +
      '<p class="ccna-sim-promo-lead ccna-sim-promo-lead--compact">' +
      "Still seeing the old version? Hard refresh " +
      "(<kbd>Cmd+Shift+R</kbd> on Mac, <kbd>Ctrl+Shift+R</kbd> on Windows), clear site data for this site, " +
      "or request a new magic link." +
      "</p>" +
      '<p class="ccna-sim-promo-hint ccna-sim-promo-hint--compact">' +
      "You are on the latest version when you see the green <strong>SY0-601 Outdated</strong> practice bank on this page." +
      "</p>" +
      '<div class="ccna-sim-promo-actions">' +
      '<a class="ccna-sim-promo-primary" href="' +
      REQUEST_LINK_HREF +
      '">Email me a portal link</a>' +
      '<button type="button" class="ccna-sim-promo-secondary" data-secplus-update-dismiss>Got it</button>' +
      "</div>" +
      "</div>";
    document.body.appendChild(root);
    root.hidden = false;
    wireModal();
  }

  function maybeShowNotice() {
    if (shown || wasDismissed() || isFreshCheckoutActivation()) return;
    setTimeout(openModal, SHOW_DELAY_MS);
  }

  function init() {
    if (!isPortalPage()) return;
    injectModal();
    maybeShowNotice();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
