/**
 * POST /api/lead-capture
 * Body: {
 *   "email": "you@example.com",
 *   "magnet": "secplus-free-simulation",
 *   "product": "secplus",
 *   "consent": true,
 *   "company_website": ""  // honeypot — must be empty
 * }
 */
import { normalizePublicSiteUrl } from "../server-lib/normalize-public-site-url.js";
import {
  resolveLeadMagnet,
  sendLeadMagnetEmail,
  addMarketingContact,
} from "../server-lib/marketing-lead-resend.js";

function readJsonBody(req) {
  try {
    if (req.body != null) {
      if (typeof req.body === "object" && !Buffer.isBuffer(req.body)) {
        return req.body;
      }
      if (typeof req.body === "string" && req.body.length) {
        return JSON.parse(req.body);
      }
    }
  } catch (_) {}
  return {};
}

function normalizeEmail(raw) {
  const s = typeof raw === "string" ? raw.trim().toLowerCase() : "";
  if (!s || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s)) return "";
  if (s.length > 254) return "";
  return s;
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "method_not_allowed" });
  }

  const body = readJsonBody(req);
  if (body.company_website) {
    return res.status(200).json({ ok: true, redirectUrl: "/comptia-sec+-home.html" });
  }

  const email = normalizeEmail(body.email);
  if (!email) {
    return res.status(400).json({ ok: false, error: "invalid_email" });
  }

  if (!body.consent) {
    return res.status(400).json({ ok: false, error: "consent_required" });
  }

  const magnet = resolveLeadMagnet(body.magnet);
  if (!magnet) {
    return res.status(400).json({ ok: false, error: "unknown_magnet" });
  }

  const site = normalizePublicSiteUrl(process.env.PUBLIC_SITE_URL || "https://becertifiedtoday.com");
  const resourceUrl = site + magnet.path;

  try {
    await addMarketingContact({ email, magnet });
  } catch (err) {
    console.warn("[lead-capture] audience contact failed:", err?.message || err);
  }

  try {
    await sendLeadMagnetEmail({ to: email, magnet, resourceUrl });
  } catch (err) {
    console.error("[lead-capture] email failed:", err?.message || err);
  }

  const welcomeSep = magnet.path.indexOf("?") >= 0 ? "&" : "?";
  return res.status(200).json({
    ok: true,
    redirectUrl: magnet.path + welcomeSep + "welcome=1",
    resourceUrl,
    email,
  });
}
