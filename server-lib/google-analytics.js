/**
 * Google Analytics 4 — service account client and report helpers.
 */
import { BetaAnalyticsDataClient } from "@google-analytics/data";
import { gaCustomerTrafficDimensionFilter } from "./analytics-internal.js";

function normalizePrivateKey(credentials) {
  if (credentials?.private_key && typeof credentials.private_key === "string") {
    credentials.private_key = credentials.private_key.replace(/\\n/g, "\n");
  }
  return credentials;
}

function decodeHtmlEntities(s) {
  return s
    .replace(/&quot;/gi, '"')
    .replace(/&#34;/g, '"')
    .replace(/&amp;/gi, "&")
    .replace(/&lt;/gi, "<")
    .replace(/&gt;/gi, ">");
}

function normalizeJsonText(s) {
  return decodeHtmlEntities(s)
    .replace(/[\u201c\u201d]/g, '"')
    .replace(/[\u2018\u2019]/g, "'")
    .replace(/\r\n/g, "\n")
    .trim();
}

function extractJsonObject(s) {
  const start = s.indexOf("{");
  const end = s.lastIndexOf("}");
  if (start >= 0 && end > start) return s.slice(start, end + 1);
  return s;
}

function readServiceAccountRawFromEnv() {
  const b64 = (process.env.GA_SERVICE_ACCOUNT_JSON_B64 || "").trim();
  if (b64) {
    try {
      const decoded = Buffer.from(b64, "base64").toString("utf8").trim();
      if (decoded) return decoded;
    } catch {
      /* fall through */
    }
  }
  return (process.env.GA_SERVICE_ACCOUNT_JSON || "").trim();
}

function credentialsFromSplitEnv() {
  const clientEmail = (process.env.GA_SERVICE_ACCOUNT_CLIENT_EMAIL || "").trim();
  let privateKey = process.env.GA_SERVICE_ACCOUNT_PRIVATE_KEY || "";
  if (!clientEmail || !privateKey.trim()) return null;
  privateKey = privateKey.replace(/\\n/g, "\n").trim();
  if (!privateKey.includes("BEGIN PRIVATE KEY")) return null;
  const projectId = (
    process.env.GA_SERVICE_ACCOUNT_PROJECT_ID ||
    process.env.GCP_PROJECT_ID ||
    ""
  ).trim();
  return normalizePrivateKey({
    type: "service_account",
    client_email: clientEmail,
    private_key: privateKey,
    project_id: projectId || undefined,
    private_key_id: (process.env.GA_SERVICE_ACCOUNT_PRIVATE_KEY_ID || "").trim() || undefined,
    client_id: (process.env.GA_SERVICE_ACCOUNT_CLIENT_ID || "").trim() || undefined,
  });
}

function parseServiceAccountJson(raw) {
  let trimmed = normalizeJsonText(raw || "");
  if (!trimmed) return null;
  if (trimmed.charCodeAt(0) === 0xfeff) trimmed = trimmed.slice(1);

  const attempts = [trimmed, extractJsonObject(trimmed)];
  if (
    (trimmed.startsWith("'") && trimmed.endsWith("'")) ||
    (trimmed.startsWith('"') && trimmed.endsWith('"') && trimmed.includes("{"))
  ) {
    const unquoted = normalizeJsonText(trimmed.slice(1, -1));
    attempts.push(unquoted, extractJsonObject(unquoted));
  }
  if (!trimmed.startsWith("{")) {
    try {
      const decoded = normalizeJsonText(Buffer.from(trimmed, "base64").toString("utf8"));
      if (decoded.startsWith("{")) {
        attempts.push(decoded, extractJsonObject(decoded));
      }
    } catch {
      /* not base64 */
    }
  }

  for (const candidate of attempts) {
    if (!candidate) continue;
    try {
      let parsed = JSON.parse(candidate);
      if (typeof parsed === "string") {
        parsed = JSON.parse(normalizeJsonText(parsed));
      }
      if (parsed && typeof parsed === "object" && parsed.type === "service_account") {
        return normalizePrivateKey(parsed);
      }
    } catch {
      /* try next */
    }
  }
  return null;
}

export function resolveServiceAccountCredentials() {
  return (
    parseServiceAccountJson(readServiceAccountRawFromEnv()) || credentialsFromSplitEnv()
  );
}

/** Safe status for admin UI (no secrets). */
export function getAnalyticsDiagnostics() {
  const rawJson = (process.env.GA_SERVICE_ACCOUNT_JSON || "").trim();
  const rawB64 = (process.env.GA_SERVICE_ACCOUNT_JSON_B64 || "").trim();
  const rawCombined = readServiceAccountRawFromEnv();
  const propertyId = (process.env.GA_PROPERTY_ID || "").replace(/\D/g, "");
  const credentials = resolveServiceAccountCredentials();
  const hasSplitEnv = Boolean(
    (process.env.GA_SERVICE_ACCOUNT_CLIENT_EMAIL || "").trim() &&
      (process.env.GA_SERVICE_ACCOUNT_PRIVATE_KEY || "").trim()
  );
  return {
    hasPropertyId: Boolean(propertyId),
    propertyIdLength: propertyId.length,
    hasJsonEnv: Boolean(rawJson),
    hasJsonB64Env: Boolean(rawB64),
    hasSplitEnv,
    jsonCharLength: rawJson.length,
    decodedCharLength: rawCombined.length,
    jsonStartsWithBrace: rawCombined.startsWith("{"),
    jsonLooksTruncated:
      rawCombined.length > 0 &&
      (!rawCombined.endsWith("}") || rawCombined.length < 180),
    jsonParseOk: Boolean(credentials),
    hasClientEmail: Boolean(credentials?.client_email),
    hasPrivateKey: Boolean(credentials?.private_key),
    projectId: credentials?.project_id || null,
    clientEmailHint: credentials?.client_email
      ? credentials.client_email.replace(/^[^@]+/, "…")
      : null,
  };
}

const DEFAULT_MEASUREMENT_ID = "G-YTT6KBHX7V";

export function getGoogleAnalyticsEnv() {
  const measurementId = (process.env.GA_MEASUREMENT_ID || DEFAULT_MEASUREMENT_ID).trim();
  const propertyId = (process.env.GA_PROPERTY_ID || "").replace(/\D/g, "");
  const credentials = resolveServiceAccountCredentials();
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
    dimensionFilter: gaCustomerTrafficDimensionFilter(),
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
    dimensionFilter: gaCustomerTrafficDimensionFilter(),
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
    dimensionFilter: gaCustomerTrafficDimensionFilter(),
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
    dimensionFilter: gaCustomerTrafficDimensionFilter(),
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
