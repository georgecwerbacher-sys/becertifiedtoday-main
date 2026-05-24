/**
 * Normalize PUBLIC_SITE_URL for Stripe Checkout redirect URLs.
 * - Trims whitespace and accidental wrapping quotes
 * - Strips trailing slashes
 * - Prepends https:// when the scheme is missing (Stripe requires a valid absolute URL)
 */
export function normalizePublicSiteUrl(raw) {
  let s = String(raw || "")
    .trim()
    .replace(/^["']|["']$/g, "")
    .replace(/\/+$/, "");
  if (!s) return "";
  if (!/^https?:\/\//i.test(s)) {
    s = "https://" + s.replace(/^\/+/, "");
  }
  try {
    const u = new URL(s);
    return u.origin;
  } catch (_) {
    return "";
  }
}
