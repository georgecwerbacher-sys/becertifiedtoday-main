const RENEW_PATH = "/encor-renew.html";
const PUBLIC_PATH_PREFIXES = ["/api/stripe/", "/api/auth/magic-link/verify", "/images/", "/js/", "/sample"];
const PUBLIC_PATHS = [RENEW_PATH, "/favicon.ico", "/robots.txt"];

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

export default async function middleware(request) {
  const host = request.headers.get("host") || "";
  const url = new URL(request.url);
  const path = url.pathname;

  const isEncorHost = host.toLowerCase().startsWith("encor.");
  if (!isEncorHost) return;

  if (
    PUBLIC_PATHS.includes(path) ||
    PUBLIC_PATH_PREFIXES.some((prefix) => path.startsWith(prefix))
  ) {
    return;
  }

  const cookies = parseCookies(request.headers.get("cookie"));
  const sessionToken = cookies.encor_access_token;
  if (!sessionToken) {
    return Response.redirect(new URL(RENEW_PATH, url.origin), 302);
  }

  const kvUrl = process.env.KV_REST_API_URL;
  const kvToken = process.env.KV_REST_API_TOKEN;
  if (!kvUrl || !kvToken) {
    return Response.redirect(new URL(RENEW_PATH, url.origin), 302);
  }

  const email = await kvGet(kvUrl, kvToken, `encor:session:${sessionToken}`);
  if (!email) {
    return Response.redirect(new URL(RENEW_PATH, url.origin), 302);
  }

  const rawAccess = await kvGet(kvUrl, kvToken, `encor:access:${String(email).toLowerCase()}`);
  if (!rawAccess) {
    return Response.redirect(new URL(RENEW_PATH, url.origin), 302);
  }

  try {
    const access = JSON.parse(rawAccess);
    if (!access.access_expires_at || Date.parse(access.access_expires_at) <= Date.now()) {
      return Response.redirect(new URL(RENEW_PATH, url.origin), 302);
    }
  } catch (_error) {
    return Response.redirect(new URL(RENEW_PATH, url.origin), 302);
  }
}
