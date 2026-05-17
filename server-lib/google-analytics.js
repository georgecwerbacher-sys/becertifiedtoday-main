/**
 * Google Analytics 4 — service account client and report helpers.
 */
import { BetaAnalyticsDataClient } from "@google-analytics/data";

function parseServiceAccountJson(raw) {
  const trimmed = (raw || "").trim();
  if (!trimmed) return null;
  try {
    return JSON.parse(trimmed);
  } catch {
    return null;
  }
}

const DEFAULT_MEASUREMENT_ID = "G-YTT6KBHX7V";

export function getGoogleAnalyticsEnv() {
  const measurementId = (process.env.GA_MEASUREMENT_ID || DEFAULT_MEASUREMENT_ID).trim();
  const propertyId = (process.env.GA_PROPERTY_ID || "").replace(/\D/g, "");
  const credentials = parseServiceAccountJson(process.env.GA_SERVICE_ACCOUNT_JSON);
  return { measurementId, propertyId, credentials };
}

export function analyticsApiReady(env = getGoogleAnalyticsEnv()) {
  return Boolean(env.propertyId && env.credentials && env.credentials.client_email);
}

let clientCache = null;

export function getAnalyticsDataClient(env = getGoogleAnalyticsEnv()) {
  if (!analyticsApiReady(env)) return null;
  if (!clientCache) {
    clientCache = new BetaAnalyticsDataClient({ credentials: env.credentials });
  }
  return clientCache;
}

function propertyName(propertyId) {
  return `properties/${propertyId}`;
}

/**
 * @param {import('@google-analytics/data').BetaAnalyticsDataClient} client
 * @param {string} propertyId
 * @param {{ startDate: string, endDate: string }} range
 */
export async function fetchAnalyticsSummary(client, propertyId, range) {
  const [response] = await client.runReport({
    property: propertyName(propertyId),
    dateRanges: [range],
    metrics: [
      { name: "activeUsers" },
      { name: "newUsers" },
      { name: "sessions" },
      { name: "screenPageViews" },
      { name: "averageSessionDuration" },
      { name: "engagementRate" },
    ],
  });

  const row = response.rows && response.rows[0];
  const vals = row ? row.metricValues || [] : [];
  const num = (i) => {
    const v = vals[i] && vals[i].value;
    const n = Number(v);
    return Number.isFinite(n) ? n : 0;
  };

  return {
    activeUsers: num(0),
    newUsers: num(1),
    sessions: num(2),
    screenPageViews: num(3),
    averageSessionDurationSeconds: num(4),
    engagementRate: num(5),
  };
}

export async function fetchTopPages(client, propertyId, range, limit = 15) {
  const [response] = await client.runReport({
    property: propertyName(propertyId),
    dateRanges: [range],
    dimensions: [{ name: "pagePath" }],
    metrics: [{ name: "screenPageViews" }, { name: "activeUsers" }],
    orderBys: [{ metric: { metricName: "screenPageViews" }, desc: true }],
    limit,
  });

  return (response.rows || []).map((row) => ({
    pagePath: row.dimensionValues?.[0]?.value || "(not set)",
    screenPageViews: Number(row.metricValues?.[0]?.value || 0),
    activeUsers: Number(row.metricValues?.[1]?.value || 0),
  }));
}

export async function fetchDailyTrend(client, propertyId, range) {
  const [response] = await client.runReport({
    property: propertyName(propertyId),
    dateRanges: [range],
    dimensions: [{ name: "date" }],
    metrics: [{ name: "activeUsers" }, { name: "screenPageViews" }, { name: "sessions" }],
    orderBys: [{ dimension: { dimensionName: "date" } }],
  });

  return (response.rows || []).map((row) => ({
    date: row.dimensionValues?.[0]?.value || "",
    activeUsers: Number(row.metricValues?.[0]?.value || 0),
    screenPageViews: Number(row.metricValues?.[1]?.value || 0),
    sessions: Number(row.metricValues?.[2]?.value || 0),
  }));
}

export async function fetchRealtimeActiveUsers(client, propertyId) {
  const [response] = await client.runRealtimeReport({
    property: propertyName(propertyId),
    metrics: [{ name: "activeUsers" }],
  });
  const row = response.rows && response.rows[0];
  return Number(row?.metricValues?.[0]?.value || 0);
}

export function rangeFromPreset(preset) {
  switch (preset) {
    case "today":
      return { startDate: "today", endDate: "today" };
    case "28d":
      return { startDate: "28daysAgo", endDate: "today" };
    case "90d":
      return { startDate: "90daysAgo", endDate: "today" };
    case "7d":
    default:
      return { startDate: "7daysAgo", endDate: "today" };
  }
}
