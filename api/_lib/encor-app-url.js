/**
 * Where subscribers land after magic-link verification (and Stripe bounce flow).
 * Default matches the ENCOR Vercel deployment. Override with ENCOR_APP_URL (e.g. encor.becertifiedtoday.com).
 */
const DEFAULT_ENCOR_APP_URL = "https://becertifiedtoday-encor.vercel.app";

export function getEncorAppBaseUrl() {
  const raw = String(process.env.ENCOR_APP_URL || "").trim();
  if (raw) return raw.replace(/\/+$/, "");
  return DEFAULT_ENCOR_APP_URL.replace(/\/+$/, "");
}
