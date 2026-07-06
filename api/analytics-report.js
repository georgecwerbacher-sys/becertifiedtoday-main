/**
 * POST /api/analytics-report
 *
 * action "login" — Body: { "action": "login", "email", "password" }
 */
import crypto from "crypto";
import { issueAnalyticsAdminToken, verifyAnalyticsAdminToken } from "../server-lib/analytics-admin-jwt.js";

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

function safeEqual(a, b) {
  const aa = Buffer.from(String(a), "utf8");
  const bb = Buffer.from(String(b), "utf8");
  if (aa.length !== bb.length) return false;
  return crypto.timingSafeEqual(aa, bb);
}

async function handleLogin(req, res) {
  const expected = (process.env.ADMIN_ANALYTICS_PASSWORD || "").trim();
  const jwtSecret = (process.env.ADMIN_ANALYTICS_JWT_SECRET || "").trim();

  if (!expected || !jwtSecret) {
    return res.status(503).json({
      ok: false,
      error: "Admin analytics is not configured",
      hint: "Set ADMIN_ANALYTICS_PASSWORD and ADMIN_ANALYTICS_JWT_SECRET on Vercel.",
    });
  }

  const allowedEmail = (
    process.env.ADMIN_ANALYTICS_EMAIL || "georgecwerbacher@gmail.com"
  )
    .trim()
    .toLowerCase();

  const body = readJsonBody(req);
  const password = typeof body.password === "string" ? body.password : "";
  const email = typeof body.email === "string" ? body.email.trim().toLowerCase() : "";

  if (!email || email !== allowedEmail) {
    return res.status(401).json({ ok: false, error: "Unauthorized email" });
  }

  if (!password || !safeEqual(password, expected)) {
    return res.status(401).json({ ok: false, error: "Invalid password" });
  }

  const token = issueAnalyticsAdminToken(jwtSecret, email);
  return res.status(200).json({
    ok: true,
    token,
    expiresInSeconds: 60 * 60 * 8,
  });
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "Method not allowed" });
  }

  const body = readJsonBody(req);
  const action = typeof body.action === "string" ? body.action.trim().toLowerCase() : "";
  const hasLoginBody =
    typeof body.email === "string" &&
    typeof body.password === "string" &&
    !bearerToken(req);
  if (action === "login" || hasLoginBody) {
    return handleLogin(req, res);
  }

  const jwtSecret = (process.env.ADMIN_ANALYTICS_JWT_SECRET || "").trim();
  const token = bearerToken(req) || (body.token || "");

  if (!jwtSecret) {
    return res.status(503).json({
      ok: false,
      error: "Admin analytics is not configured",
    });
  }

  if (!verifyAnalyticsAdminToken(token, jwtSecret)) {
    return res.status(401).json({ ok: false, error: "Unauthorized" });
  }

  return res.status(200).json({ ok: true });
}
