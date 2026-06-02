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

  function fetchVerifyPortalPurchase(sessionId) {
    return fetch("/api/verify-checkout-session?session_id=" + encodeURIComponent(sessionId)).then(function (res) {
      return res.json().then(function (data) {
        return { res: res, data: data };
      });
    });
  }

  function grantPortalFromVerifyPair(pair, checkoutSessionId) {
    var res = pair.res;
    var data = pair.data || {};
    if (!res.ok || !data.ok) {
      return false;
    }
    if (data.productId !== "ccna-portal-30d" && data.productId !== "ccna-portal-10d") {
      return false;
    }
    var exp =
      typeof data.accessExpiresAt === "number" && Number.isFinite(data.accessExpiresAt)
        ? data.accessExpiresAt
        : Date.now() + (data.productId === "ccna-portal-10d" ? 10 : 30) * 86400000;
    if (exp <= Date.now()) {
      return false;
    }
    return bccSetPortal30DayEntitlement(exp, checkoutSessionId);
  }

  function bccRestoreCcnaPortalAccess() {
    return new Promise(function (resolve) {
      if (bccPortalAccessActive()) {
        resolve(true);
        return;
      }
      var cs = bccReadPortalCheckoutSessionId();
      if (!cs) {
        resolve(false);
        return;
      }
      fetchVerifyPortalPurchase(cs)
        .then(function (pair) {
          resolve(grantPortalFromVerifyPair(pair, cs));
        })
        .catch(function () {
          resolve(false);
        });
    });
  }

  function bccApplyCcnaPortalCheckoutFromUrl(searchParams, stripSessionQuery) {
    var sessionId = null;
    try {
      var params = searchParams || new URLSearchParams(window.location.search || "");
      sessionId = params.get("session_id");
    } catch (e) {
      sessionId = null;
    }
    if (!sessionId || sessionId.indexOf("cs_") !== 0) {
      return Promise.resolve(false);
    }
    return fetchVerifyPortalPurchase(sessionId).then(function (pair) {
      var ok = grantPortalFromVerifyPair(pair, sessionId);
      if (ok && stripSessionQuery) {
        try {
          var u = new URL(window.location.href);
          u.searchParams.delete("session_id");
          var clean = u.pathname + (u.search || "") + (u.hash || "");
          window.history.replaceState({}, "", clean || "/");
        } catch (e) {}
      }
      return ok;
    });
  }

  if (typeof window !== "undefined") {
    window.bccPortalAccessActive = bccPortalAccessActive;
    window.bccSetPortal30DayEntitlement = bccSetPortal30DayEntitlement;
    window.bccReadPortalCheckoutSessionId = bccReadPortalCheckoutSessionId;
    window.bccSavePortalCheckoutSessionId = bccSavePortalCheckoutSessionId;
    window.bccRestoreCcnaPortalAccess = bccRestoreCcnaPortalAccess;
    window.bccApplyCcnaPortalCheckoutFromUrl = bccApplyCcnaPortalCheckoutFromUrl;
  }
})();
