/**
 * Redeem ?bcc_admin_bypass= JWT from /admin dashboard on training portal pages only.
 * Sets normal portal localStorage entitlement — no other public bypass exists.
 */
(function () {
  "use strict";

  var PARAM = "bcc_admin_bypass";

  function trackFromPath() {
    var p = (location.pathname || "").toLowerCase();
    if (p.indexOf("/ccna-study/") === 0) return "ccna";
    if (p.indexOf("/ccnp-encor-study/") === 0) return "encor";
    if (p.indexOf("/comp_tia_sec+/") === 0) return "secplus";
    return "";
  }

  function stripBypassParam() {
    try {
      var u = new URL(location.href);
      if (!u.searchParams.has(PARAM)) return;
      u.searchParams.delete(PARAM);
      history.replaceState({}, "", u.pathname + (u.search || "") + (u.hash || ""));
    } catch (_) {}
  }

  function applyEntitlement(data) {
    var exp = data.accessExpiresAtMs;
    var cs = data.checkoutSessionId || "admin-bypass";
    if (data.track === "ccna" && typeof window.bccSetPortal30DayEntitlement === "function") {
      return window.bccSetPortal30DayEntitlement(exp, cs);
    }
    if (data.track === "encor" && typeof window.bccSetEncorPortalEntitlement === "function") {
      return window.bccSetEncorPortalEntitlement(exp, cs, data.productId || "encor-portal-30d");
    }
    if (data.track === "secplus" && typeof window.bccSetSecplusPortalEntitlement === "function") {
      return window.bccSetSecplusPortalEntitlement(exp, cs, data.productId || "secplus-portal-30d");
    }
    return false;
  }

  function redeem(token) {
    var hint = trackFromPath();
    return fetch("/api/admin-portal-bypass", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action: "redeem", token: token, track: hint || undefined }),
    })
      .then(function (r) {
        return r.json().then(function (j) {
          return { ok: r.ok, body: j };
        });
      })
      .then(function (res) {
        if (!res.ok || !res.body || !res.body.ok) return;
        applyEntitlement(res.body);
        stripBypassParam();
      })
      .catch(function () {});
  }

  function run() {
    var token = "";
    try {
      token = new URLSearchParams(location.search).get(PARAM) || "";
    } catch (_) {}
    if (!token) return;
    redeem(token);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();
