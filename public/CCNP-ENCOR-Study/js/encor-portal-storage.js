/**
 * CCNP ENCOR portal access (localStorage). Used by ccnp-home, ENCOR_Training_Portal, and magic-link redeem.
 * Shape: { expiresAt: epochMs }
 */
(function () {
  var KEY = "bcc_encor_portal_v1";
  var KEY_CS = "bcc_encor_portal_cs_v1";

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

  function bccEncorPortalAccessActive() {
    return readActive(KEY);
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

  function bccSaveEncorPortalCheckoutSessionId(checkoutSessionId) {
    var cs = typeof checkoutSessionId === "string" ? checkoutSessionId.trim() : "";
    if (!cs || cs.indexOf("cs_") !== 0) return false;
    try {
      localStorage.setItem(KEY_CS, cs);
      return true;
    } catch (e) {
      return false;
    }
  }

  function bccReadEncorPortalCheckoutSessionId() {
    try {
      var s = localStorage.getItem(KEY_CS);
      return typeof s === "string" && s.indexOf("cs_") === 0 ? s : null;
    } catch (e) {
      return null;
    }
  }

  function bccSetEncorPortalEntitlement(expiresAtMs, checkoutSessionId) {
    var ok = setExpiry(KEY, expiresAtMs);
    if (ok && checkoutSessionId) bccSaveEncorPortalCheckoutSessionId(checkoutSessionId);
    return ok;
  }

  if (typeof window !== "undefined") {
    window.bccEncorPortalAccessActive = bccEncorPortalAccessActive;
    window.bccSetEncorPortalEntitlement = bccSetEncorPortalEntitlement;
    window.bccReadEncorPortalCheckoutSessionId = bccReadEncorPortalCheckoutSessionId;
    window.bccSaveEncorPortalCheckoutSessionId = bccSaveEncorPortalCheckoutSessionId;
  }
})();
