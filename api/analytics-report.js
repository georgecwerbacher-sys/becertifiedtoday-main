/**
 * POST /api/analytics-report
 * Authorization: Bearer <admin JWT>
 * Body: { "range": "7d" | "28d" | "90d" | "today" }
 */
import { verifyAnalyticsAdminToken } from "../server-lib/analytics-admin-jwt.js";
import {
  analyticsApiReady,
  fetchAnalyticsSummary,
  fetchDailyTrend,
  fetchRealtimeActiveUsers,
  fetchTopPages,
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
    const parts = [];
    if (!diagnostics.hasPropertyId) parts.push("GA_PROPERTY_ID is missing or not numeric (use 538156526).");
    if (!diagnostics.hasJsonEnv && !diagnostics.hasJsonB64Env && !diagnostics.hasSplitEnv) {
      parts.push("No service account env vars set (GA_SERVICE_ACCOUNT_JSON, GA_SERVICE_ACCOUNT_JSON_B64, or split CLIENT_EMAIL + PRIVATE_KEY).");
    } else if (!diagnostics.jsonParseOk) {
      if (diagnostics.jsonLooksTruncated) {
        parts.push(
          "Service account value looks truncated (multiline paste). Run: ./scripts/format-ga-service-account-for-vercel.sh key.json — use GA_SERVICE_ACCOUNT_JSON_B64 on Vercel."
        );
      } else {
        parts.push(
          "Invalid service account JSON. Run ./scripts/format-ga-service-account-for-vercel.sh key.json locally, set GA_SERVICE_ACCOUNT_JSON_B64 (recommended) or a single-line GA_SERVICE_ACCOUNT_JSON, then vercel --prod."
        );
      }
    } else if (!diagnostics.hasClientEmail || !diagnostics.hasPrivateKey) {
      parts.push("Credentials are missing client_email or private_key.");
    }
    return res.status(503).json({
      ok: false,
      error: "Google Analytics Data API is not configured",
      hint: parts.join(" ") || "Set GA_PROPERTY_ID and GA_SERVICE_ACCOUNT_JSON on Vercel, then redeploy.",
      diagnostics,
    });
  }

  const body = readJsonBody(req);
  const range = rangeFromPreset(typeof body.range === "string" ? body.range : "7d");
  const client = getAnalyticsDataClient(env);

  try {
    const [summary, topPages, dailyTrend, realtimeActiveUsers] = await Promise.all([
      fetchAnalyticsSummary(client, env.propertyId, range),
      fetchTopPages(client, env.propertyId, range, 20),
      fetchDailyTrend(client, env.propertyId, range),
      fetchRealtimeActiveUsers(client, env.propertyId),
    ]);

    return res.status(200).json({
      ok: true,
      propertyId: env.propertyId,
      measurementId: env.measurementId || null,
      range,
      summary,
      topPages,
      dailyTrend,
      realtimeActiveUsers,
      fetchedAt: new Date().toISOString(),
    });
  } catch (err) {
    const message = err && err.message ? String(err.message) : "Analytics API error";
    return res.status(502).json({ ok: false, error: message });
  }
}
