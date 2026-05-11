/**
 * CCNA portal time-boxed access (localStorage). Used by the timed test runner and CCNA_Training_Portal.
 * Keys: 30-day and 90-day passes (same shape { expiresAt: epochMs }).
 *
 * From a trusted purchase success page (same origin), e.g.:
 *   bccSetPortal90DayEntitlement(Date.now() + 90 * 864e5);
 *   bccSetPortal30DayEntitlement(Date.now() + 30 * 864e5);
 */
(function () {
  var KEY_30 = "bcc_ccna_portal_30d_v1";
  var KEY_90 = "bcc_ccna_portal_90d_v1";

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
    return readActive(KEY_30) || readActive(KEY_90);
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

  function bccSetPortal30DayEntitlement(expiresAtMs) {
    return setExpiry(KEY_30, expiresAtMs);
  }

  function bccSetPortal90DayEntitlement(expiresAtMs) {
    return setExpiry(KEY_90, expiresAtMs);
  }

  if (typeof window !== "undefined") {
    window.bccPortalAccessActive = bccPortalAccessActive;
    window.bccSetPortal30DayEntitlement = bccSetPortal30DayEntitlement;
    window.bccSetPortal90DayEntitlement = bccSetPortal90DayEntitlement;
  }
})();
