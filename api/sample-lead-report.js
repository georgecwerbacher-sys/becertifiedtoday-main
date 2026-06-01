/**
 * POST /api/sample-lead-report
 * Authorization: Bearer <admin JWT>
 */
import { verifyAnalyticsAdminToken } from "../server-lib/analytics-admin-jwt.js";
import {
  aggregateSampleLeadReport,
  readSampleLeadEvents,
} from "../server-lib/sample-lead-analytics.js";

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

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "Method not allowed" });
  }

  const jwtSecret = (process.env.ADMIN_ANALYTICS_JWT_SECRET || "").trim();
  const token = bearerToken(req) || (readJsonBody(req).token || "");

  if (!jwtSecret) {
    return res.status(503).json({ ok: false, error: "Admin analytics is not configured" });
  }

  if (!verifyAnalyticsAdminToken(token, jwtSecret)) {
    return res.status(401).json({ ok: false, error: "Unauthorized" });
  }

  try {
    const rows = await readSampleLeadEvents();
    const report = aggregateSampleLeadReport(rows);
    return res.status(200).json({
      ok: true,
      ...report,
      fetchedAt: new Date().toISOString(),
      note:
        "Homepage sample questions → email capture for free timed simulation. Submit attempts count each form try; successes are completed unlocks.",
      csvPath: "marketing-vault/leads/home-sample-email-capture.csv",
    });
  } catch (err) {
    const message = err && err.message ? String(err.message) : "Sample lead report error";
    return res.status(502).json({ ok: false, error: message });
  }
}
