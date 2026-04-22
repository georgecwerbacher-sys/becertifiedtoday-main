import { next } from "@vercel/edge";

const ENCORE_HOST = "encor.becertifiedtoday.com";
const ENCORE_ORIGIN = `https://${ENCORE_HOST}`;
const LEGACY_ENCORE_HOST = "encore.becertifiedtoday.com";

/** Marketing site stays on apex; app content uses Encore */
const APEX_HOSTS = new Set(["becertifiedtoday.com", "www.becertifiedtoday.com"]);

/** Only these paths are served on apex (not redirected to Encore) */
const APEX_HOME_PATHS = new Set(["/", "/index.html"]);

export default function middleware(request) {
  const url = new URL(request.url);
  const host =
    request.headers.get("host")?.split(":")[0]?.toLowerCase() ?? "";

  // Preview / local: no apex→encore redirects (same deployment, any hostname)
  const isPreview = host.endsWith(".vercel.app") || host === "localhost";

  if (isPreview) {
    return next();
  }

  // ACME / domain verification
  if (url.pathname.startsWith("/.well-known/")) {
    return next();
  }

  // Legacy subdomain fallback: encore -> encor
  if (host === LEGACY_ENCORE_HOST) {
    const target = new URL(url.pathname + url.search, ENCORE_ORIGIN);
    return Response.redirect(target.toString(), 308);
  }

  // Apex domain: send everything except the marketing home to Encore
  if (APEX_HOSTS.has(host)) {
    if (APEX_HOME_PATHS.has(url.pathname)) {
      return next();
    }
    const target = new URL(url.pathname + url.search, ENCORE_ORIGIN);
    return Response.redirect(target.toString(), 308);
  }

  return next();
}

export const config = {
  matcher: [
    "/",
    "/((?!_next/static|_next/image|favicon.ico).*)",
  ],
};
