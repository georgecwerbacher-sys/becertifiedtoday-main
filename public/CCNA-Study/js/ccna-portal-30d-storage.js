/**
 * CCNA portal 30-day access (localStorage). Used by the timed test runner and CCNA_Training_Portal.
 * Shape: { expiresAt: epochMs }
 *
 * Checkout session id (bcc_ccna_portal_30d_cs_v1) lets the portal re-verify after local entitlement is cleared,
 * as long as Stripe still recognizes the session and the paid window has not ended.
 *
 * From a trusted purchase success page (same origin), e.g.:
 *   bccSetPortal30DayEntitlement(expiresAtMsFromApi, checkoutSessionId);
 */
(function () {
  var KEY_30 = "bcc_ccna_portal_30d_v1";
  var KEY_CS = "bcc_ccna_portal_30d_cs_v1";

  function readActive(key) {
    try {
      var raw = localStorage.getItem(key);
      if (!raw) return false;
      var o = JSON.parse(raw);
      return typeof o.expiresAt === "number" && o.expiresAt > Date.now();
    } catch (e) {
      return false;
    }
  }

  function bccPortalAccessActive() {
    return readActive(KEY_30);
  }

  function setExpiry(key, expiresAtMs) {
    var t = Number(expiresAtMs);
    if (!Number.isFinite(t) || t <= Date.now()) return false;
    try {
      localStorage.setItem(key, JSON.stringify({ expiresAt: t }));
      return true;
    } catch (e) {
      return false;
    }
  }

  function bccSavePortalCheckoutSessionId(checkoutSessionId) {
    var cs = typeof checkoutSessionId === "string" ? checkoutSessionId.trim() : "";
    if (!cs || cs.indexOf("cs_") !== 0) return false;
    try {
      localStorage.setItem(KEY_CS, cs);
      return true;
    } catch (e) {
      return false;
    }
  }

  function bccReadPortalCheckoutSessionId() {
    try {
      var s = localStorage.getItem(KEY_CS);
      return typeof s === "string" && s.indexOf("cs_") === 0 ? s : null;
    } catch (e) {
      return null;
    }
  }

  function bccSetPortal30DayEntitlement(expiresAtMs, checkoutSessionId) {
    var ok = setExpiry(KEY_30, expiresAtMs);
    if (ok && checkoutSessionId) bccSavePortalCheckoutSessionId(checkoutSessionId);
    return ok;
  }

  if (typeof window !== "undefined") {
    window.bccPortalAccessActive = bccPortalAccessActive;
    window.bccSetPortal30DayEntitlement = bccSetPortal30DayEntitlement;
    window.bccReadPortalCheckoutSessionId = bccReadPortalCheckoutSessionId;
    window.bccSavePortalCheckoutSessionId = bccSavePortalCheckoutSessionId;
  }
})();
