/**
 * CCNA Automation (200-901) portal access (localStorage). Admin bypass + future checkout.
 * Shape: { expiresAt: epochMs, productId?: string }
 */
(function () {
  var KEY = "bcc_ccnaauto_portal_v1";
  var KEY_CS = "bcc_ccnaauto_portal_cs_v1";
  var PRODUCT_ID = "ccnaauto-portal-30d";

  function readEntitlement(key) {
    try {
      var raw = localStorage.getItem(key);
      if (!raw) return null;
      return JSON.parse(raw);
    } catch (e) {
      return null;
    }
  }

  function readActive(key) {
    var o = readEntitlement(key);
    return !!(o && typeof o.expiresAt === "number" && o.expiresAt > Date.now());
  }

  function bccCcnaautoPortalAccessActive() {
    return readActive(KEY);
  }

  function bccSetCcnaautoPortalEntitlement(expiresAtMs, checkoutSessionId, productId) {
    if (typeof expiresAtMs !== "number" || !Number.isFinite(expiresAtMs) || expiresAtMs <= Date.now()) {
      return false;
    }
    try {
      localStorage.setItem(
        KEY,
        JSON.stringify({
          expiresAt: expiresAtMs,
          productId: productId || PRODUCT_ID,
        })
      );
      if (checkoutSessionId) {
        localStorage.setItem(KEY_CS, String(checkoutSessionId));
      }
      return true;
    } catch (e) {
      return false;
    }
  }

  if (typeof window !== "undefined") {
    window.bccCcnaautoPortalAccessActive = bccCcnaautoPortalAccessActive;
    window.bccSetCcnaautoPortalEntitlement = bccSetCcnaautoPortalEntitlement;
  }
})();
