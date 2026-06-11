/**
 * POST /api/campaign-marketing-report
 * Authorization: Bearer <admin JWT>
 * Body: { "range": "7d"|"today"|"28d"|"90d" }
 */
import { verifyAnalyticsAdminToken } from "../server-lib/analytics-admin-jwt.js";
import { buildCampaignMarketingReport } from "../server-lib/campaign-marketing-report.js";
import {
  analyticsApiReady,
  getAnalyticsDataClient,
  getAnalyticsDiagnostics,
  getGoogleAnalyticsEnv,
  rangeFromPreset,
} from "../server-lib/google-analytics.js";

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
    return res.status(503).json({
      ok: false,
      error: "Admin analytics is not configured",
    });
  }

  if (!verifyAnalyticsAdminToken(token, jwtSecret)) {
    return res.status(401).json({ ok: false, error: "Unauthorized" });
  }

  const env = getGoogleAnalyticsEnv();
  const diagnostics = getAnalyticsDiagnostics();
  if (!analyticsApiReady(env)) {
    return res.status(503).json({
      ok: false,
      error: "Google Analytics Data API is not configured",
      diagnostics,
    });
  }

  const body = readJsonBody(req);
  const range = rangeFromPreset(typeof body.range === "string" ? body.range : "7d");
  const client = getAnalyticsDataClient(env);

  try {
    const report = await buildCampaignMarketingReport(client, env.propertyId, range);
    return res.status(200).json({
      ok: true,
      range,
      propertyId: env.propertyId,
      fetchedAt: new Date().toISOString(),
      ...report,
      note:
        "Sessions use GA4 sessionCampaignName (utm_campaign). begin_checkout counts are event totals in range. " +
        "Google Ads click data is not pulled via API yet — use Ads UI for spend/impressions. " +
        "Setup docs: scripts/*-google-ads.txt in the repo.",
    });
  } catch (err) {
    const message = err && err.message ? String(err.message) : "Campaign report error";
    return res.status(502).json({ ok: false, error: message });
  }
}
