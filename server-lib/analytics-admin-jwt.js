/**
 * Short-lived admin JWT for /admin dashboard API calls.
 */
import { signPortalMagicJwt, verifyPortalMagicJwt } from "./ccna-portal-magic-jwt.js";

const AUD = "analytics-admin";
const TTL_SEC = 60 * 60 * 8;

export function issueAnalyticsAdminToken(secret, email) {
  const exp = Math.floor(Date.now() / 1000) + TTL_SEC;
  const sub =
    typeof email === "string" && email.includes("@") ? email.trim().toLowerCase() : "admin";
  return signPortalMagicJwt({ aud: AUD, sub, exp }, secret);
}

export function verifyAnalyticsAdminToken(token, secret) {
  const payload = verifyPortalMagicJwt(token, secret);
  if (!payload || payload.aud !== AUD) return null;
  const now = Math.floor(Date.now() / 1000);
  if (typeof payload.exp !== "number" || payload.exp <= now) return null;
  return payload;
}
