const PUBLIC_PATH_PREFIXES = ["/api/stripe/", "/api/auth/magic-link/verify", "/images/", "/js/", "/sample"];
const PUBLIC_PATHS_STATIC = ["/favicon.ico", "/robots.txt"];

/**
 * Per-subdomain gate: add a row for each protected training host (e.g. secplus.).
 * KV prefixes must match access-store / magic-link keys for that product.
 */
const PROTECTED_PRODUCTS = [
  {
    hostPrefix: "encor.",
    cookieName: "encor_access_token",
    renewPath: "/encor-renew.html",
    sessionKvPrefix: "encor:session:",
    accessKvPrefix: "encor:access:",
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
  return PROTECTED_PRODUCTS.find((p) => h.startsWith(p.hostPrefix)) || null;
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
    return Response.redirect(new URL(product.renewPath, url.origin), 302);
  }

  const kvUrl = process.env.KV_REST_API_URL;
  const kvToken = process.env.KV_REST_API_TOKEN;
  if (!kvUrl || !kvToken) {
    return Response.redirect(new URL(product.renewPath, url.origin), 302);
  }

  const email = await kvGet(kvUrl, kvToken, `${product.sessionKvPrefix}${sessionToken}`);
  if (!email) {
    return Response.redirect(new URL(product.renewPath, url.origin), 302);
  }

  const rawAccess = await kvGet(kvUrl, kvToken, `${product.accessKvPrefix}${String(email).toLowerCase()}`);
  if (!rawAccess) {
    return Response.redirect(new URL(product.renewPath, url.origin), 302);
  }

  try {
    const access = JSON.parse(rawAccess);
    if (!access.access_expires_at || Date.parse(access.access_expires_at) <= Date.now()) {
      return Response.redirect(new URL(product.renewPath, url.origin), 302);
    }
  } catch (_error) {
    return Response.redirect(new URL(product.renewPath, url.origin), 302);
  }
}
