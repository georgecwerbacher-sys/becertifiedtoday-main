/**
 * Short-lived JWT for owner-only portal access from /admin (no Stripe checkout).
 */
import { signPortalMagicJwt, verifyPortalMagicJwt } from "./ccna-portal-magic-jwt.js";

export const PORTAL_ADMIN_BYPASS_AUD = "portal-admin-bypass";
export const PORTAL_ADMIN_BYPASS_TTL_SEC = 60 * 60 * 2; // 2 hours to open link
export const PORTAL_ADMIN_ACCESS_MS = 90 * 24 * 60 * 60 * 1000; // 90 days local entitlement after redeem

/** @type {Record<string, { label: string, portalPath: string, productId: string }>} */
export const PORTAL_TRACKS = {
  ccna: {
    label: "CCNA 200-301",
    portalPath: "/CCNA-Study/CCNA_Training_Portal.html",
    productId: "ccna-portal-30d",
  },
  encor: {
    label: "CCNP ENCOR 350-401",
    portalPath: "/CCNP-ENCOR-Study/ENCOR_Training_Portal.html",
    productId: "encor-portal-30d",
  },
  secplus: {
    label: "CompTIA Security+ SY0-701",
    portalPath: "/COMP_TIA_SEC+/SEC+_Training_Portal.html",
    productId: "secplus-portal-30d",
  },
};

export function normalizePortalTrack(track) {
  const t = String(track || "").trim().toLowerCase();
  return PORTAL_TRACKS[t] ? t : null;
}

export function issuePortalAdminBypassToken(secret, email, track) {
  const normalized = normalizePortalTrack(track);
  if (!normalized || !secret || !email) return null;
  const exp = Math.floor(Date.now() / 1000) + PORTAL_ADMIN_BYPASS_TTL_SEC;
  return signPortalMagicJwt(
    {
      aud: PORTAL_ADMIN_BYPASS_AUD,
      sub: String(email).trim().toLowerCase(),
      track: normalized,
      exp,
    },
    secret
  );
}

/** @returns {{ email: string, track: string, exp: number }|null} */
export function verifyPortalAdminBypassToken(token, secret) {
  const payload = verifyPortalMagicJwt(token, secret);
  if (!payload || payload.aud !== PORTAL_ADMIN_BYPASS_AUD) return null;
  const track = normalizePortalTrack(payload.track);
  if (!track) return null;
  const email = typeof payload.sub === "string" ? payload.sub.trim().toLowerCase() : "";
  if (!email) return null;
  const now = Math.floor(Date.now() / 1000);
  if (typeof payload.exp !== "number" || payload.exp <= now) return null;
  return { email, track, exp: payload.exp };
}

export function portalAdminBypassUrl(siteOrigin, track, token) {
  const meta = PORTAL_TRACKS[track];
  if (!meta || !token) return null;
  const base = String(siteOrigin || "").replace(/\/$/, "");
  return `${base}${meta.portalPath}?bcc_admin_bypass=${encodeURIComponent(token)}`;
}
