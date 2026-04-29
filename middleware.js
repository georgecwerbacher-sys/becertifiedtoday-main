const PUBLIC_PATH_PREFIXES = [
  "/api/stripe/",
  "/api/auth/magic-link/verify",
  "/api/auth/encor-claim-bounce",
  "/images/",
  "/js/",
  "/sample",
];
const PUBLIC_PATHS_STATIC = ["/favicon.ico", "/robots.txt"];

/**
 * Per-subdomain gate: add a row for each protected training host (e.g. secplus.).
 * KV prefixes must match access-store / magic-link keys for that product.
 */
const PROTECTED_PRODUCTS = [
  {
    hostPrefix: "encor.",
    /** Same ENCOR gate on the dedicated Vercel deployment hostname (not matched by encor.* prefix). */
    exactHosts: ["becertifiedtoday-encor.vercel.app"],
    cookieName: "encor_access_token",
    renewPath: "/encor-renew.html",
    sessionKvPrefix: "encor:session:",
    accessKvPrefix: "encor:access:",
    /** After auth on encor.* only: `/` was marketing index; send to ENCOR overview. Skip on exactHosts where `/` is already the portal. */
    portalHomePath: "/CCNP_Encor.html",
  },
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
      if (h.startsWith(p.hostPrefix)) return true;
      return Array.isArray(p.exactHosts) && p.exactHosts.some((eh) => eh === h);
    }) || null
  );
}

/** Renew page lives on the marketing origin; Vercel ENCOR hostname may not ship that HTML. */
function renewRedirectUrl(product, requestUrl) {
  let hostname;
  try {
    hostname = new URL(requestUrl).hostname.toLowerCase();
  } catch {
    return new URL(product.renewPath, requestUrl).href;
  }
  if (Array.isArray(product.exactHosts) && product.exactHosts.includes(hostname)) {
    const pub = String(process.env.PUBLIC_SITE_URL || "https://becertifiedtoday.com").replace(/\/+$/, "");
    return `${pub}${product.renewPath}`;
  }
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

  const h = host.toLowerCase();
  const skipPortalRedirect = Array.isArray(product.exactHosts) && product.exactHosts.includes(h);
  const portal = product.portalHomePath;
  if (!skipPortalRedirect && portal && (path === "/" || path === "/index.html")) {
    return Response.redirect(new URL(portal, url.origin), 302);
  }
}
