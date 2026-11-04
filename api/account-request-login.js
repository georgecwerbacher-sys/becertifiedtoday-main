/**
 * POST /api/account-request-login
 * Body: { "email": "you@example.com" }
 * Sends a learner magic-link email (free account).
 */
import { normalizePublicSiteUrl } from "../server-lib/normalize-public-site-url.js";
import {
  learnerMagicSecret,
  signLearnerMagicToken,
} from "../server-lib/learner-auth.js";
import { normalizeEmail, postgresConfigured } from "../server-lib/learner-db.js";
import { sendLearnerLoginEmail } from "../server-lib/learner-resend.js";

function readJsonBody(req) {
  try {
    if (req.body != null) {
      if (typeof req.body === "object" && !Buffer.isBuffer(req.body)) return req.body;
      if (typeof req.body === "string" && req.body.length) return JSON.parse(req.body);
    }
  } catch (_) {}
  return {};
}

const GENERIC =
  "If that email can receive mail, we sent a sign-in link. Check spam and wait a minute before trying again.";

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "Method not allowed" });
  }

  if (!postgresConfigured()) {
    return res.status(503).json({
      ok: false,
      error: "Account storage is not configured",
      hint: "Set POSTGRES_URL (Vercel Postgres / Neon) and run scripts/sql/learner-account-schema.sql",
    });
  }

  if (!learnerMagicSecret()) {
    return res.status(503).json({
      ok: false,
      error: "Login links are not configured",
      hint: "Set LEARNER_MAGIC_LINK_SECRET or PORTAL_MAGIC_LINK_SECRET",
    });
  }

  const body = readJsonBody(req);
  const email = normalizeEmail(body.email);
  if (!email) {
    return res.status(400).json({ ok: false, error: "Enter a valid email address" });
  }

  const origin =
    normalizePublicSiteUrl(process.env.PUBLIC_SITE_URL) ||
    normalizePublicSiteUrl(req.headers?.origin) ||
    "https://becertifiedtoday.com";

  try {
    const token = signLearnerMagicToken(email, 30);
    const magicUrl = `${origin}/account/magic.html?token=${encodeURIComponent(token)}`;
    await sendLearnerLoginEmail({ to: email, magicUrl });
  } catch (e) {
    console.error("[account-request-login]", e.message);
    // Still return generic success to avoid email enumeration timing differences on Resend failures after sign.
    return res.status(200).json({ ok: true, message: GENERIC });
  }

  return res.status(200).json({ ok: true, message: GENERIC });
}
