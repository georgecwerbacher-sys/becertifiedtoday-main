const PUBLIC_PATH_PREFIXES = [
  "/api/stripe/",
  "/api/auth/magic-link/verify",
  "/api/auth/encor-claim-bounce",
  /** Allow browser gate + UI to check session without a prior cookie (returns JSON only). */
  "/api/auth/access-status",
  /** Help page POSTs here before the user has a session on this device. */
  "/api/auth/request-magic-link",
  "/images/",
  "/js/",
  "/sample",
];
/** Shown right after Stripe checkout (no session yet); must bypass gate on encor.* */
const PUBLIC_PATHS_STATIC = [
  "/favicon.ico",
  "/robots.txt",
  "/checkout-success.html",
  "/cert-access-help.html",
];

/**
 * Per-subdomain gate: add a row for each protected training host (e.g. secplus.).
 * KV prefixes must match access-store / magic-link keys for that product.
 */
const ENCOR_GATE = {
  cookieName: "encor_access_token",
  renewPath: "/encor-renew.html",
  sessionKvPrefix: "encor:session:",
  accessKvPrefix: "encor:access:",
};

const PROTECTED_PRODUCTS = [
  { ...ENCOR_GATE, hostPrefix: "encor." },
  /** Vercel default hostnames for this project (same KV/session as encor.*). */
  { ...ENCOR_GATE, hostExact: "ccnp-study.vercel.app" },
  { ...ENCOR_GATE, hostExact: "becertifiedtoday-encor.vercel.app" },
];

function parseCookies(value) {
  const out = {};
  String(value || "")
    .split(";")
    .map((part) => part.trim())
    .filter(Boolean)
    .forEach((item) => {
      const idx = item.indexOf("=");
      if (idx <= 0) return;
      const key = item.slice(0, idx);
      const val = item.slice(idx + 1);
      out[key] = decodeURIComponent(val);
    });
  return out;
}

async function kvGet(url, token, key) {
  const path = ["get", key].map((part) => encodeURIComponent(part)).join("/");
  const response = await fetch(`${url}/${path}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!response.ok) return null;
  const data = await response.json();
  return data.result;
}

function matchProtectedProduct(host) {
  const h = host.toLowerCase();
  return (
    PROTECTED_PRODUCTS.find((p) => {
      if (p.hostExact && h === p.hostExact) return true;
      if (p.hostPrefix && h.startsWith(p.hostPrefix)) return true;
      return false;
    }) || null
  );
}

function renewRedirectUrl(product, requestUrl) {
  return new URL(product.renewPath, requestUrl).href;
}

export default async function middleware(request) {
  const host = request.headers.get("host") || "";
  const url = new URL(request.url);
  const path = url.pathname;

  const product = matchProtectedProduct(host);
  if (!product) return;

  const publicPaths = new Set([...PUBLIC_PATHS_STATIC, ...PROTECTED_PRODUCTS.map((p) => p.renewPath)]);
  if (publicPaths.has(path) || PUBLIC_PATH_PREFIXES.some((prefix) => path.startsWith(prefix))) {
    return;
  }

  const cookies = parseCookies(request.headers.get("cookie"));
  const sessionToken = cookies[product.cookieName];
  if (!sessionToken) {
    return Response.redirect(renewRedirectUrl(product, request.url), 302);
  }

  const kvUrl = process.env.KV_REST_API_URL;
  const kvToken = process.env.KV_REST_API_TOKEN;
  if (!kvUrl || !kvToken) {
    return Response.redirect(renewRedirectUrl(product, request.url), 302);
  }

  const email = await kvGet(kvUrl, kvToken, `${product.sessionKvPrefix}${sessionToken}`);
  if (!email) {
    return Response.redirect(renewRedirectUrl(product, request.url), 302);
  }

  const rawAccess = await kvGet(kvUrl, kvToken, `${product.accessKvPrefix}${String(email).toLowerCase()}`);
  if (!rawAccess) {
    return Response.redirect(renewRedirectUrl(product, request.url), 302);
  }

  try {
    const access = JSON.parse(rawAccess);
    if (!access.access_expires_at || Date.parse(access.access_expires_at) <= Date.now()) {
      return Response.redirect(renewRedirectUrl(product, request.url), 302);
    }
  } catch (_error) {
    return Response.redirect(renewRedirectUrl(product, request.url), 302);
  }
}
