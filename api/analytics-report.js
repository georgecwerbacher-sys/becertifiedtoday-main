/**
 * POST /api/analytics-report
 *
 * action "login" — Body: { "action": "login", "email", "password" }
 * action "report" (default) — Authorization: Bearer <admin JWT>, Body: { "range": "7d"|... }
 */
import crypto from "crypto";
import { issueAnalyticsAdminToken, verifyAnalyticsAdminToken } from "../server-lib/analytics-admin-jwt.js";
import { buildCampaignMarketingReport } from "../server-lib/campaign-marketing-report.js";
import { buildSampleCheckoutReport } from "../server-lib/sample-checkout-report.js";
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

  const range = rangeFromPreset(typeof body.range === "string" ? body.range : "7d");
  const client = getAnalyticsDataClient(env);

  try {
    const [summary, topPages, dailyTrend, realtimeActiveUsers, campaignMarketing, sampleCheckout] =
      await Promise.all([
        fetchAnalyticsSummary(client, env.propertyId, range),
        fetchTopPages(client, env.propertyId, range, 20),
        fetchDailyTrend(client, env.propertyId, range),
        fetchRealtimeActiveUsers(client, env.propertyId),
        buildCampaignMarketingReport(client, env.propertyId, range),
        buildSampleCheckoutReport(client, env.propertyId, range),
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
      campaignMarketing: {
        ...campaignMarketing,
        note:
          "Sessions use GA4 sessionCampaignName (utm_campaign). begin_checkout counts are event totals in range. " +
          "Google Ads click data is not pulled via API yet — use Ads UI for spend/impressions. " +
          "Setup docs: scripts/*-google-ads.txt in the repo.",
      },
      sampleCheckout,
      fetchedAt: new Date().toISOString(),
    });
  } catch (err) {
    const message = err && err.message ? String(err.message) : "Analytics API error";
    return res.status(502).json({ ok: false, error: message });
  }
}
