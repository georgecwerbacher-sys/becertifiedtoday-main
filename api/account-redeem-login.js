/**
 * POST /api/account-redeem-login
 * Body: { "token": "<JWT>" }
 * Creates a learner session and sets HttpOnly bcc_learner cookie.
 */
import {
  redeemLearnerLogin,
  verifyLearnerMagicToken,
} from "../server-lib/learner-auth.js";
import { postgresConfigured } from "../server-lib/learner-db.js";

function readJsonBody(req) {
  try {
    if (req.body != null) {
      if (typeof req.body === "object" && !Buffer.isBuffer(req.body)) return req.body;
      if (typeof req.body === "string" && req.body.length) return JSON.parse(req.body);
    }
  } catch (_) {}
  return {};
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "Method not allowed" });
  }

  if (!postgresConfigured()) {
    return res.status(503).json({
      ok: false,
      error: "Account storage is not configured",
    });
  }

  const body = readJsonBody(req);
  const token = typeof body.token === "string" ? body.token.trim() : "";
  if (!token) {
    return res.status(400).json({ ok: false, error: "Missing token" });
  }

  const payload = verifyLearnerMagicToken(token);
  if (!payload) {
    return res.status(401).json({ ok: false, error: "Invalid or expired link" });
  }

  try {
    const result = await redeemLearnerLogin(payload.email);
    res.setHeader("Set-Cookie", result.cookie);
    return res.status(200).json({
      ok: true,
      email: result.learner.email,
      learnerId: result.learner.id,
      expiresAt: result.expiresAt.toISOString(),
      redirect: "/account/",
    });
  } catch (e) {
    console.error("[account-redeem-login]", e.message);
    return res.status(500).json({
      ok: false,
      error: "Could not complete sign-in",
      hint: "Confirm the learner schema is applied and POSTGRES_URL is set.",
    });
  }
}
