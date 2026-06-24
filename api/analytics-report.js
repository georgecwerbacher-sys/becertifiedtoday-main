/**
 * POST /api/analytics-report
 *
 * action "login" — Body: { "action": "login", "email", "password" }
 * action "report" (default) — Authorization: Bearer <admin JWT>, Body: { "range": "7d"|... }
 */
import crypto from "crypto";
import Stripe from "stripe";
import { issueAnalyticsAdminToken, verifyAnalyticsAdminToken } from "../server-lib/analytics-admin-jwt.js";
import { buildCampaignPlanReport } from "../server-lib/campaign-plan-report.js";
import {
  saveCampaignPlanDailyEntry,
  setCampaignPlanStartDate,
  setCampaignPlanStepCompleted,
} from "../server-lib/campaign-plan-store.js";
import { getCampaignTestPlan } from "../server-lib/campaign-test-plan-registry.js";
import { buildCampaignMarketingReport } from "../server-lib/campaign-marketing-report.js";
import { buildCertHomeLandingReport } from "../server-lib/cert-home-landing-report.js";
import {
  analyticsApiReady,
  fetchAnalyticsSummary,
  fetchDailyTrend,
  fetchRealtimeActiveUsers,
  getAnalyticsDataClient,
  getAnalyticsDiagnostics,
  getGoogleAnalyticsEnv,
  rangeFromPreset,
} from "../server-lib/google-analytics.js";
import { readSampleLeadEvents } from "../server-lib/sample-lead-analytics.js";
import { getStripeSecretKey } from "../server-lib/stripe-secret-key.js";
import { resolveGithubRepo } from "../server-lib/visitor-questions.js";

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

function campaignIdFromBody(body) {
  const raw =
    typeof body.campaignId === "string"
      ? body.campaignId.trim()
      : typeof body.campaign_id === "string"
        ? body.campaign_id.trim()
        : "secplus_portal";
  return raw || "secplus_portal";
}

async function handleCampaignPlanSave(req, res, body) {
  const campaignId = campaignIdFromBody(body);
  const plan = getCampaignTestPlan(campaignId);
  if (!plan) {
    return res.status(404).json({ ok: false, error: "Campaign plan not found" });
  }

  if (typeof body.startDate === "string" && body.startDate.trim()) {
    const result = await setCampaignPlanStartDate(campaignId, body.startDate.trim(), plan.defaultStartDate);
    if (!result.ok) {
      const status = result.reason === "not_configured" ? 503 : 400;
      return res.status(status).json({
        ok: false,
        error: result.reason === "not_configured" ? "Campaign plan storage is not configured" : "Could not save start date",
        reason: result.reason,
        hint: "Set GITHUB_LEADS_TOKEN on Vercel (Contents read/write). Plan saves to data/reports/campaign-plan/ via GitHub API.",
        detail: result.detail || null,
      });
    }
    return res.status(200).json({ ok: true, ...result });
  }

  if (typeof body.stepId === "string" && body.stepId.trim()) {
    const completed =
      body.completed === true || body.completed === "true" || body.completed === 1 || body.completed === "1";
    const result = await setCampaignPlanStepCompleted(
      campaignId,
      body.stepId.trim(),
      completed,
      plan.defaultStartDate
    );
    if (!result.ok) {
      const status = result.reason === "not_configured" ? 503 : 502;
      return res.status(status).json({
        ok: false,
        error: result.reason === "not_configured" ? "Campaign plan storage is not configured" : "Could not save step",
        reason: result.reason,
        detail: result.detail || null,
      });
    }
    return res.status(200).json({ ok: true, ...result });
  }

  const date = typeof body.date === "string" ? body.date.trim() : "";
  if (!date) {
    return res.status(400).json({ ok: false, error: "Missing date (YYYY-MM-DD), stepId, or startDate" });
  }

  const daily = body.daily && typeof body.daily === "object" ? body.daily : body;
  const result = await saveCampaignPlanDailyEntry(campaignId, date, daily, plan.defaultStartDate);
  if (!result.ok) {
    const status =
      result.reason === "invalid_date"
        ? 400
        : result.reason === "not_configured"
          ? 503
          : 502;
    return res.status(status).json({
      ok: false,
      error:
        result.reason === "not_configured"
          ? "Campaign plan storage is not configured"
          : result.reason === "invalid_date"
            ? "Invalid date — use YYYY-MM-DD"
            : "Could not save daily entry",
      reason: result.reason,
      hint: "Set GITHUB_LEADS_TOKEN on Vercel. Daily metrics save to data/reports/campaign-plan/ via GitHub API.",
      detail: result.detail || null,
    });
  }
  return res.status(200).json({ ok: true, ...result });
}

async function handleCampaignPlan(req, res) {
  const body = readJsonBody(req);
  const campaignId = campaignIdFromBody(body);
  const env = getGoogleAnalyticsEnv();
  const client = analyticsApiReady(env) ? getAnalyticsDataClient(env) : null;

  let stripe = null;
  const sk = getStripeSecretKey(process.env.STRIPE_SECRET_KEY);
  if (sk.secret) {
    stripe = new Stripe(sk.secret);
  }

  try {
    const report = await buildCampaignPlanReport({
      client,
      propertyId: env.propertyId,
      stripe,
      campaignId,
    });

    if (report.error && !report.calendarDays) {
      const repoInfo = resolveGithubRepo();
      return res.status(report.code === "github_not_configured" ? 503 : 502).json({
        ok: false,
        error: report.error,
        hint:
          report.code === "github_not_configured"
            ? "Set GITHUB_LEADS_TOKEN on Vercel (Contents read/write on this repo)."
            : null,
        storageRepo: repoInfo ? `${repoInfo.owner}/${repoInfo.repo}` : null,
        plan: report.plan || getCampaignTestPlan(campaignId),
      });
    }

    return res.status(200).json({
      ok: true,
      campaignPlan: report,
      storagePath: report.storagePath,
      fetchedAt: report.fetchedAt,
    });
  } catch (err) {
    const message = err && err.message ? String(err.message) : "Campaign plan error";
    return res.status(502).json({ ok: false, error: message });
  }
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

  if (action === "campaign_plan_save") {
    return handleCampaignPlanSave(req, res, body);
  }

  if (action === "campaign_plan") {
    return handleCampaignPlan(req, res);
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

  const rangePreset = typeof body.range === "string" && body.range.trim() ? body.range.trim() : "7d";
  const range = rangeFromPreset(rangePreset);
  const client = getAnalyticsDataClient(env);

  try {
    const [summary, dailyTrend, realtimeActiveUsers, sampleLeadRows] = await Promise.all([
      fetchAnalyticsSummary(client, env.propertyId, range),
      fetchDailyTrend(client, env.propertyId, range),
      fetchRealtimeActiveUsers(client, env.propertyId),
      readSampleLeadEvents().catch((err) => ({
        error: err?.message || "Sample lead CSV read failed",
      })),
    ]);

    const sk = getStripeSecretKey(process.env.STRIPE_SECRET_KEY);
    const stripe = sk.secret ? new Stripe(sk.secret) : null;

    const [certHomeLanding, campaignMarketing, campaignPlan] = await Promise.all([
      buildCertHomeLandingReport(
        client,
        env.propertyId,
        range,
        rangePreset,
        sampleLeadRows && !sampleLeadRows.error ? sampleLeadRows : []
      ).catch((err) => ({
        error: err?.message || "Cert home landing report failed",
      })),
      buildCampaignMarketingReport(client, env.propertyId, range, rangePreset).catch((err) => ({
        error: err?.message || "Campaign marketing report failed",
      })),
      buildCampaignPlanReport({
        client,
        propertyId: env.propertyId,
        stripe,
        campaignId: "secplus_portal",
      }).catch((err) => ({
        error: err?.message || "Campaign plan failed",
      })),
    ]);

    return res.status(200).json({
      ok: true,
      propertyId: env.propertyId,
      measurementId: env.measurementId || null,
      range,
      rangePreset,
      summary,
      dailyTrend,
      realtimeActiveUsers,
      certHomeLanding:
        certHomeLanding && !certHomeLanding.error
          ? certHomeLanding
          : {
              pages: [],
              totals: {},
              error: certHomeLanding?.error || "Cert home landing unavailable",
            },
      campaignMarketing:
        campaignMarketing && !campaignMarketing.error
          ? campaignMarketing
          : {
              campaigns: [],
              error: campaignMarketing?.error || "Campaign tracker unavailable",
            },
      campaignPlan:
        campaignPlan && !campaignPlan.error
          ? campaignPlan
          : {
              error: campaignPlan?.error || "Campaign plan unavailable",
            },
      sampleLeadCsvError: sampleLeadRows?.error || null,
      fetchedAt: new Date().toISOString(),
    });
  } catch (err) {
    const message = err && err.message ? String(err.message) : "Analytics API error";
    return res.status(502).json({ ok: false, error: message });
  }
}
