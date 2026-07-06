/**
 * Vercel Web Analytics for /admin site traffic (no GA4 service account).
 * API: https://vercel.com/docs/analytics/web-analytics-api
 */
import { rangePresetLabel } from "./google-analytics.js";

const API_BASE = "https://api.vercel.com/v1/query/web-analytics";

export const PRIMARY_LANDING_PATH =
  (process.env.BCC_VERCEL_PRIMARY_LANDING_PATH || "/comptia-sec+-home.html").trim();

function isoDateUtc(d) {
  return d.toISOString().slice(0, 10);
}

/** @returns {{ since: string, until: string }} ISO dates; until is exclusive (next UTC day). */
export function vercelDateRangeFromPreset(preset = "7d") {
  const now = new Date();
  const until = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate() + 1));
  const start = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate()));
  switch (preset) {
    case "21d":
      start.setUTCDate(start.getUTCDate() - 20);
      break;
    case "28d":
      start.setUTCDate(start.getUTCDate() - 27);
      break;
    case "90d":
      start.setUTCDate(start.getUTCDate() - 89);
      break;
    case "7d":
      start.setUTCDate(start.getUTCDate() - 6);
      break;
    case "today":
    default:
      break;
  }
  return { since: isoDateUtc(start), until: isoDateUtc(until) };
}

export function getVercelAnalyticsEnv() {
  const token = (
    process.env.VERCEL_ACCESS_TOKEN ||
    process.env.VERCEL_TOKEN ||
    ""
  ).trim();
  const projectId = (
    process.env.VERCEL_PROJECT_ID ||
    process.env.BCC_VERCEL_PROJECT_ID ||
    ""
  ).trim();
  const teamId = (
    process.env.VERCEL_ORG_ID ||
    process.env.VERCEL_TEAM_ID ||
    process.env.BCC_VERCEL_TEAM_ID ||
    ""
  ).trim();
  return { token, projectId, teamId };
}

export function vercelAnalyticsReady(env = getVercelAnalyticsEnv()) {
  return Boolean(env.token && env.projectId && env.teamId);
}

async function vercelAnalyticsGet(path, params, env = getVercelAnalyticsEnv()) {
  const qs = new URLSearchParams({
    teamId: env.teamId,
    projectId: env.projectId,
    ...params,
  });
  const res = await fetch(`${API_BASE}/${path}?${qs.toString()}`, {
    headers: { Authorization: `Bearer ${env.token}` },
  });
  const body = await res.json().catch(() => ({}));
  if (!res.ok) {
    const msg =
      (body && (body.error?.message || body.error)) ||
      `Vercel Web Analytics API error (${res.status})`;
    throw new Error(typeof msg === "string" ? msg : "Vercel Web Analytics API error");
  }
  return body;
}

/**
 * @param {string} rangePreset
 */
export async function buildVercelSiteTrafficReport(rangePreset = "7d") {
  const env = getVercelAnalyticsEnv();
  if (!vercelAnalyticsReady(env)) {
    return {
      error: "Vercel Web Analytics is not configured",
      hint:
        "Set VERCEL_ACCESS_TOKEN on Vercel (Account → Tokens, read scope). VERCEL_PROJECT_ID and VERCEL_ORG_ID are set automatically on deploy.",
    };
  }

  const { since, until } = vercelDateRangeFromPreset(rangePreset);
  const rangeParams = { since, until };
  const homeFilter = `requestPath eq '${PRIMARY_LANDING_PATH.replace(/'/g, "''")}'`;

  const [totals, home, daily, topPages] = await Promise.all([
    vercelAnalyticsGet("visits/count", rangeParams, env),
    vercelAnalyticsGet(
      "visits/count",
      { ...rangeParams, filter: homeFilter },
      env
    ),
    vercelAnalyticsGet("visits/aggregate", { ...rangeParams, by: "day" }, env),
    vercelAnalyticsGet(
      "visits/aggregate",
      { ...rangeParams, by: "requestPath", limit: "20" },
      env
    ),
  ]);

  const summary = totals.data || {};
  const homeData = home.data || {};

  return {
    rangeLabel: rangePresetLabel(rangePreset),
    since,
    until,
    summary: {
      visitors: Number(summary.visitors || 0),
      pageviews: Number(summary.pageviews || 0),
    },
    primaryLanding: {
      path: PRIMARY_LANDING_PATH,
      label: "Security+ home",
      visitors: Number(homeData.visitors || 0),
      pageviews: Number(homeData.pageviews || 0),
    },
    dailyTrend: (daily.data || []).map((row) => ({
      date: (row.timestamp || "").slice(0, 10),
      visitors: Number(row.visitors || 0),
      pageviews: Number(row.pageviews || 0),
    })),
    topPages: (topPages.data || []).map((row) => ({
      pagePath: row.requestPath || row.route || "(not set)",
      visitors: Number(row.visitors || 0),
      pageviews: Number(row.pageviews || 0),
    })),
    note:
      "Vercel Web Analytics (production). Unique visitors = distinct visitors in the range, not GA4 “new users”.",
    dashboardUrl: "https://vercel.com/werby1s-projects/becertifiedtoday-main/analytics",
  };
}
