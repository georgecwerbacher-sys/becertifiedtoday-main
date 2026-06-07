/**
 * POST /api/admin-portal-bypass
 *
 * action "link" (default) — Authorization: Bearer <analytics admin JWT>
 *   Body: { "action": "link", "track": "ccna" | "encor" | "secplus" | "all" }
 *
 * action "redeem" — Body: { "action": "redeem", "token": "<JWT>", "track": optional hint }
 */
import { verifyAnalyticsAdminToken } from "../server-lib/analytics-admin-jwt.js";
import {
  PORTAL_ADMIN_ACCESS_MS,
  PORTAL_TRACKS,
  issuePortalAdminBypassToken,
  normalizePortalTrack,
  portalAdminBypassUrl,
  verifyPortalAdminBypassToken,
} from "../server-lib/portal-admin-bypass.js";

function readJsonBody(req) {
  try {
    if (req.body != null) {
      if (typeof req.body === "object" && !Buffer.isBuffer(req.body)) return req.body;
      if (typeof req.body === "string" && req.body.length) return JSON.parse(req.body);
    }
  } catch (_) {}
  return {};
}

function bearerToken(req) {
  const h = req.headers.authorization || req.headers.Authorization || "";
  const m = /^Bearer\s+(.+)$/i.exec(String(h).trim());
  return m ? m[1].trim() : "";
}

function siteOrigin() {
  const raw = (process.env.PUBLIC_SITE_URL || "https://becertifiedtoday.com").trim();
  return raw.replace(/\/$/, "");
}

async function handleLink(req, res, jwtSecret) {
  const admin = verifyAnalyticsAdminToken(bearerToken(req), jwtSecret);
  if (!admin) {
    return res.status(401).json({ ok: false, error: "Unauthorized" });
  }

  const adminEmail =
    typeof admin.sub === "string" && admin.sub.includes("@")
      ? admin.sub.trim().toLowerCase()
      : (process.env.ADMIN_ANALYTICS_EMAIL || "georgecwerbacher@gmail.com").trim().toLowerCase();

  const body = readJsonBody(req);
  const trackReq = typeof body.track === "string" ? body.track.trim().toLowerCase() : "all";
  const tracks =
    trackReq === "all" ? Object.keys(PORTAL_TRACKS) : [normalizePortalTrack(trackReq)].filter(Boolean);

  if (!tracks.length) {
    return res.status(400).json({ ok: false, error: "Invalid track" });
  }

  const origin = siteOrigin();
  const links = tracks.map(function (track) {
    const token = issuePortalAdminBypassToken(jwtSecret, adminEmail, track);
    const meta = PORTAL_TRACKS[track];
    return {
      track,
      label: meta.label,
      portalPath: meta.portalPath,
      url: portalAdminBypassUrl(origin, track, token),
      expiresInSeconds: 60 * 60 * 2,
    };
  });

  return res.status(200).json({
    ok: true,
    links,
    note:
      "Open each link in this browser to grant 90-day portal entitlement. Bypass links expire in 2 hours if not opened. This is the only supported credential bypass.",
    issuedAt: new Date().toISOString(),
  });
}

async function handleRedeem(req, res, jwtSecret) {
  const body = readJsonBody(req);
  const token = typeof body.token === "string" ? body.token.trim() : "";
  if (!token) {
    return res.status(400).json({ ok: false, error: "Missing token" });
  }

  const claim = verifyPortalAdminBypassToken(token, jwtSecret);
  if (!claim) {
    return res.status(401).json({ ok: false, error: "Invalid or expired bypass link" });
  }

  const trackHint = typeof body.track === "string" ? body.track.trim().toLowerCase() : "";
  if (trackHint && trackHint !== claim.track) {
    return res.status(400).json({ ok: false, error: "Bypass token does not match this portal" });
  }

  const meta = PORTAL_TRACKS[claim.track];
  const accessExpiresAtMs = Date.now() + PORTAL_ADMIN_ACCESS_MS;

  return res.status(200).json({
    ok: true,
    track: claim.track,
    productId: meta.productId,
    accessExpiresAtMs,
    checkoutSessionId: "admin-bypass",
    adminEmail: claim.email,
  });
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "Method not allowed" });
  }

  const jwtSecret = (process.env.ADMIN_ANALYTICS_JWT_SECRET || "").trim();
  if (!jwtSecret) {
    return res.status(503).json({ ok: false, error: "Admin is not configured" });
  }

  const body = readJsonBody(req);
  const action = typeof body.action === "string" ? body.action.trim().toLowerCase() : "link";

  if (action === "redeem") {
    return handleRedeem(req, res, jwtSecret);
  }
  if (action === "link") {
    return handleLink(req, res, jwtSecret);
  }

  return res.status(400).json({ ok: false, error: "Invalid action" });
}
