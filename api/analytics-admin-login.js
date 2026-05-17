/**
 * POST /api/analytics-admin-login
 * Body: { "password": "..." }
 */
import crypto from "crypto";
import { issueAnalyticsAdminToken } from "../server-lib/analytics-admin-jwt.js";

function readJsonBody(req) {
  try {
    if (req.body != null) {
      if (typeof req.body === "object" && !Buffer.isBuffer(req.body)) return req.body;
      if (typeof req.body === "string" && req.body.length) return JSON.parse(req.body);
    }
  } catch (_) {}
  return {};
}

function safeEqual(a, b) {
  const aa = Buffer.from(String(a), "utf8");
  const bb = Buffer.from(String(b), "utf8");
  if (aa.length !== bb.length) return false;
  return crypto.timingSafeEqual(aa, bb);
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "Method not allowed" });
  }

  const expected = (process.env.ADMIN_ANALYTICS_PASSWORD || "").trim();
  const jwtSecret = (process.env.ADMIN_ANALYTICS_JWT_SECRET || "").trim();

  if (!expected || !jwtSecret) {
    return res.status(503).json({
      ok: false,
      error: "Admin analytics is not configured",
      hint: "Set ADMIN_ANALYTICS_PASSWORD and ADMIN_ANALYTICS_JWT_SECRET on Vercel.",
    });
  }

  const body = readJsonBody(req);
  const password = typeof body.password === "string" ? body.password : "";

  if (!password || !safeEqual(password, expected)) {
    return res.status(401).json({ ok: false, error: "Invalid password" });
  }

  const token = issueAnalyticsAdminToken(jwtSecret);
  return res.status(200).json({
    ok: true,
    token,
    expiresInSeconds: 60 * 60 * 8,
  });
}
