/**
 * Defense-in-depth when Edge middleware is missing (e.g. misconfigured deployment).
 * No-op on marketing hostnames. On encor.* hosts, redirects if session/access is invalid.
 */
(function () {
  var h = "";
  try {
    h = String(location.hostname || "").toLowerCase();
  } catch (_e) {}

  var encorHost =
    h === "encor.becertifiedtoday.com" ||
    h.startsWith("encor.") ||
    h === "ccnp-study.vercel.app" ||
    h === "becertifiedtoday-encor.vercel.app";
  if (!encorHost) return;

  var renew =
    (function () {
      try {
        return location.origin + "/encor-renew.html";
      } catch (_e) {
        return "https://becertifiedtoday.com/encor-renew.html";
      }
    })();

  fetch("/api/auth/access-status", { credentials: "include" })
    .then(function (r) {
      return r.ok ? r.json() : Promise.reject(new Error("access-status not ok"));
    })
    .then(function (data) {
      if (data && data.has_access === true) return;
      location.replace(renew);
    })
    .catch(function () {
      location.replace(renew);
    });
})();
