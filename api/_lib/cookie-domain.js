/**
 * Optional "; Domain=..." so the ENCOR session cookie is visible on encor.* after
 * magic-link verification on the marketing origin (e.g. www).
 * Override with SESSION_COOKIE_DOMAIN=.becertifiedtoday.com if needed.
 */
export function sessionCookieDomainDirective() {
  const raw = String(process.env.SESSION_COOKIE_DOMAIN || "").trim();
  if (raw) {
    const d = raw.startsWith(".") ? raw : `.${raw}`;
    return `; Domain=${d}`;
  }

  const baseUrl = String(process.env.PUBLIC_SITE_URL || process.env.ENCOR_APP_URL || "").trim();
  if (!baseUrl) return "";

  let hostname;
  try {
    hostname = new URL(baseUrl.includes("://") ? baseUrl : `https://${baseUrl}`).hostname.toLowerCase();
  } catch {
    return "";
  }

  if (!hostname || hostname === "localhost" || hostname.endsWith(".local")) return "";
  if (hostname.endsWith(".vercel.app")) return "";

  const parts = hostname.split(".").filter(Boolean);
  if (parts.length < 2) return "";

  const parent = parts.slice(-2).join(".");
  return `; Domain=.${parent}`;
}
