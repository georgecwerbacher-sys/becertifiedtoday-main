/**
 * CCNP ENCOR portal access (localStorage). Used by ccnp-home, ENCOR_Training_Portal, and magic-link redeem.
 * Shape: { expiresAt: epochMs, productId?: string }
 *
 * Checkout session id (bcc_encor_portal_cs_v1) re-verifies with Stripe when local entitlement expired
 * but the paid window has not ended — same pattern as CCNA portal storage.
 */
(function () {
  var KEY = "bcc_encor_portal_v1";
  var KEY_CS = "bcc_encor_portal_cs_v1";
  var KEY_PENDING_TIER = "bcc_encor_pending_portal_tier";
  var KEY_PENDING_AT = "bcc_encor_pending_portal_at";
  var PENDING_MAX_MS = 86400000;

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

  function bccEncorPortalAccessActive() {
    return readActive(KEY);
  }

  function bccEncorPortalAccessActiveSync() {
    return bccEncorPortalAccessActive();
  }

  function isEncorPortalProductId(productId) {
    return productId === "encor-portal-30d" || productId === "encor-portal-10d";
  }

  function tierToProductId(tier) {
    if (tier === "10d") return "encor-portal-10d";
    if (tier === "30d") return "encor-portal-30d";
    return null;
  }

  function productIdFromAmountCentsEncor(amount) {
    if (amount === 999) return "encor-portal-10d";
    if (amount === 1999 || amount === 1499) return "encor-portal-30d";
    return null;
  }

  function bccSetEncorPendingPortalTier(tier) {
    if (tier !== "10d" && tier !== "30d") return false;
    try {
      localStorage.setItem(KEY_PENDING_TIER, tier);
      localStorage.setItem(KEY_PENDING_AT, String(Date.now()));
      return true;
    } catch (e) {
      return false;
    }
  }

  function readPendingPortalTier() {
    try {
      var tier = localStorage.getItem(KEY_PENDING_TIER);
      var at = parseInt(localStorage.getItem(KEY_PENDING_AT) || "0", 10);
      if (!tier || !Number.isFinite(at) || Date.now() - at > PENDING_MAX_MS) return null;
      return tier === "10d" || tier === "30d" ? tier : null;
    } catch (e) {
      return null;
    }
  }

  function clearPendingPortalTier() {
    try {
      localStorage.removeItem(KEY_PENDING_TIER);
      localStorage.removeItem(KEY_PENDING_AT);
    } catch (e) {}
  }

  function resolveEncorPortalProductId(data) {
    var productId = data && data.productId;
    if (isEncorPortalProductId(productId)) return productId;
    productId = tierToProductId(readPendingPortalTier());
    if (isEncorPortalProductId(productId)) return productId;
    var amt =
      data && typeof data.amount_subtotal === "number"
        ? data.amount_subtotal
        : data && typeof data.amount_total === "number"
          ? data.amount_total
          : null;
    return productIdFromAmountCentsEncor(amt);
  }

  function setExpiry(key, expiresAtMs, productId) {
    var t = Number(expiresAtMs);
    if (!Number.isFinite(t) || t <= Date.now()) return false;
    var payload = { expiresAt: t };
    if (typeof productId === "string" && productId.length) {
      payload.productId = productId;
    }
    try {
      localStorage.setItem(key, JSON.stringify(payload));
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

  function bccSetEncorPortalEntitlement(expiresAtMs, checkoutSessionId, productId) {
    var ok = setExpiry(KEY, expiresAtMs, productId);
    if (ok && checkoutSessionId) bccSaveEncorPortalCheckoutSessionId(checkoutSessionId);
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
    bccSaveEncorPortalCheckoutSessionId(checkoutSessionId);

    var productId = resolveEncorPortalProductId(data);
    if (!isEncorPortalProductId(productId)) {
      return false;
    }
    var exp =
      typeof data.accessExpiresAt === "number" && Number.isFinite(data.accessExpiresAt)
        ? data.accessExpiresAt
        : Date.now() +
          (productId === "encor-portal-10d" ? 10 : 30) * 86400000;
    if (exp <= Date.now()) {
      return false;
    }
    var ok = bccSetEncorPortalEntitlement(exp, checkoutSessionId, productId);
    if (ok) clearPendingPortalTier();
    return ok;
  }

  /**
   * Re-verify stored Stripe checkout session and refresh local portal entitlement (10d/30d).
   * Resolves true when active portal access is available after the call.
   */
  function bccRestoreEncorPortalAccess() {
    return new Promise(function (resolve) {
      if (bccEncorPortalAccessActive()) {
        resolve(true);
        return;
      }
      var cs = bccReadEncorPortalCheckoutSessionId();
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

  /**
   * Apply ?session_id= from Stripe return URL, persist entitlement + checkout id for later restores.
   */
  function bccApplyEncorPortalCheckoutFromUrl(searchParams, stripSessionQuery) {
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
    window.bccEncorPortalAccessActive = bccEncorPortalAccessActive;
    window.bccEncorPortalAccessActiveSync = bccEncorPortalAccessActiveSync;
    window.bccSetEncorPortalEntitlement = bccSetEncorPortalEntitlement;
    window.bccReadEncorPortalCheckoutSessionId = bccReadEncorPortalCheckoutSessionId;
    window.bccSaveEncorPortalCheckoutSessionId = bccSaveEncorPortalCheckoutSessionId;
    window.bccSetEncorPendingPortalTier = bccSetEncorPendingPortalTier;
    window.bccRestoreEncorPortalAccess = bccRestoreEncorPortalAccess;
    window.bccApplyEncorPortalCheckoutFromUrl = bccApplyEncorPortalCheckoutFromUrl;
  }
})();
