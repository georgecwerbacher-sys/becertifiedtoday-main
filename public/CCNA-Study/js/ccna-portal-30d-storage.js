/**
 * 30-day CCNA portal entitlement for this origin (localStorage).
 * The timed test runner reads bcc_ccna_portal_30d_v1 and allows access when expiresAt > now.
 *
 * Call from your trusted 30-day purchase success flow (same site), e.g.:
 *   bccSetPortal30DayEntitlement(Date.now() + 30 * 864e5);
 *
 * @param {number} expiresAtMs Unix epoch milliseconds when access ends
 */
(function () {
  var KEY = "bcc_ccna_portal_30d_v1";

  function bccSetPortal30DayEntitlement(expiresAtMs) {
    var t = Number(expiresAtMs);
    if (!Number.isFinite(t) || t <= Date.now()) return false;
    try {
      localStorage.setItem(KEY, JSON.stringify({ expiresAt: t }));
      return true;
    } catch (e) {
      return false;
    }
  }

  if (typeof window !== "undefined") {
    window.bccSetPortal30DayEntitlement = bccSetPortal30DayEntitlement;
  }
})();
