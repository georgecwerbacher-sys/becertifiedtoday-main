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

/** GA4 Data API standard property limit is 10 concurrent requests — stay under it. */
const GA_REPORT_CONCURRENCY = 5;
let gaReportInflight = 0;
/** @type {Array<{ run: () => Promise<unknown>, resolve: (v: unknown) => void, reject: (e: unknown) => void }>} */
const gaReportQueue = [];

function drainGaReportQueue() {
  while (gaReportInflight < GA_REPORT_CONCURRENCY && gaReportQueue.length) {
    const job = gaReportQueue.shift();
    if (!job) break;
    gaReportInflight += 1;
    Promise.resolve()
      .then(job.run)
      .then(job.resolve, job.reject)
      .finally(() => {
        gaReportInflight -= 1;
        drainGaReportQueue();
      });
  }
}

function enqueueGaReportTask(run) {
  return new Promise((resolve, reject) => {
    gaReportQueue.push({ run, resolve, reject });
    drainGaReportQueue();
  });
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function isGaQuotaError(err) {
  const msg = err && err.message ? String(err.message) : "";
  return msg.includes("RESOURCE_EXHAUSTED") || msg.includes("429");
}

async function runGaReport(client, request) {
  let lastErr;
  for (let attempt = 0; attempt < 4; attempt += 1) {
    try {
      return await enqueueGaReportTask(async () => {
        const [response] = await client.runReport(request);
        return response;
      });
    } catch (err) {
      lastErr = err;
      if (!isGaQuotaError(err) || attempt >= 3) throw err;
      await sleep(400 * (attempt + 1));
    }
  }
  throw lastErr;
}

async function runGaRealtimeReport(client, request) {
  let lastErr;
  for (let attempt = 0; attempt < 4; attempt += 1) {
    try {
      return await enqueueGaReportTask(async () => {
        const [response] = await client.runRealtimeReport(request);
        return response;
      });
    } catch (err) {
      lastErr = err;
      if (!isGaQuotaError(err) || attempt >= 3) throw err;
      await sleep(400 * (attempt + 1));
    }
  }
  throw lastErr;
}

/**
 * @param {import('@google-analytics/data').BetaAnalyticsDataClient} client
 */
async function runReportSafe(client, request) {
  try {
    return await runGaReport(client, request);
  } catch (err) {
    const msg = err && err.message ? String(err.message) : "";
    if (!request.dimensionFilter || !msg.includes("INVALID_ARGUMENT")) throw err;
    return runGaReport(client, { ...request, dimensionFilter: undefined });
  }
}

export async function fetchAnalyticsSummary(client, propertyId, range) {
  const response = await runReportSafe(client, {
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
  const response = await runReportSafe(client, {
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
  const response = await runReportSafe(client, {
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
  const response = await runGaRealtimeReport(client, {
    property: propertyName(propertyId),
    metrics: [{ name: "activeUsers" }],
  });
  const row = response.rows && response.rows[0];
  return Number(row?.metricValues?.[0]?.value || 0);
}

function mergeDimensionFilters(...filters) {
  const expressions = [];
  for (const f of filters) {
    if (!f) continue;
    if (f.andGroup && Array.isArray(f.andGroup.expressions)) {
      expressions.push(...f.andGroup.expressions);
    } else {
      expressions.push(f);
    }
  }
  if (!expressions.length) return undefined;
  return { andGroup: { expressions } };
}

/**
 * Sessions and users grouped by GA4 sessionCampaignName (utm_campaign).
 */
export async function fetchSessionsByCampaign(client, propertyId, range, limit = 25) {
  const response = await runReportSafe(client, {
    property: propertyName(propertyId),
    dateRanges: [range],
    dimensionFilter: gaCustomerTrafficDimensionFilter(),
    dimensions: [{ name: "sessionCampaignName" }],
    metrics: [
      { name: "sessions" },
      { name: "activeUsers" },
      { name: "engagedSessions" },
      { name: "screenPageViews" },
    ],
    orderBys: [{ metric: { metricName: "sessions" }, desc: true }],
    limit,
  });

  return (response.rows || []).map((row) => ({
    campaign: row.dimensionValues?.[0]?.value || "(not set)",
    sessions: Number(row.metricValues?.[0]?.value || 0),
    users: Number(row.metricValues?.[1]?.value || 0),
    engagedSessions: Number(row.metricValues?.[2]?.value || 0),
    pageViews: Number(row.metricValues?.[3]?.value || 0),
  }));
}

/** Event-scoped filter only — do not mix gaCustomerTrafficDimensionFilter with eventCount. */
function beginCheckoutEventFilter() {
  return {
    filter: {
      fieldName: "eventName",
      stringFilter: { matchType: "EXACT", value: "begin_checkout" },
    },
  };
}

export async function runBeginCheckoutEventReport(
  client,
  propertyId,
  range,
  { metrics, dimensions = [], extraFilter, orderBys, limit }
) {
  return runReportSafe(client, {
    property: propertyName(propertyId),
    dateRanges: [range],
    dimensionFilter: mergeDimensionFilters(beginCheckoutEventFilter(), extraFilter),
    dimensions,
    metrics,
    orderBys,
    limit,
  });
}

async function fetchBeginCheckoutEventCount(client, propertyId, range, extraFilter) {
  try {
    const response = await runBeginCheckoutEventReport(client, propertyId, range, {
      metrics: [{ name: "eventCount" }],
      extraFilter,
    });
    return Number(response.rows?.[0]?.metricValues?.[0]?.value || 0);
  } catch (err) {
    const msg = err && err.message ? String(err.message) : "";
    if (extraFilter && msg.includes("INVALID_ARGUMENT")) return 0;
    throw err;
  }
}

async function fetchBeginCheckoutActiveUsers(client, propertyId, range, extraFilter) {
  try {
    const response = await runBeginCheckoutEventReport(client, propertyId, range, {
      metrics: [{ name: "activeUsers" }],
      extraFilter,
    });
    return Number(response.rows?.[0]?.metricValues?.[0]?.value || 0);
  } catch (err) {
    const msg = err && err.message ? String(err.message) : "";
    if (extraFilter && msg.includes("INVALID_ARGUMENT")) return 0;
    throw err;
  }
}

/**
 * begin_checkout event counts by session campaign (Google Ads attribution).
 * eventCount is incompatible with sessionCampaignName — use sessions with an event filter.
 */
export async function fetchBeginCheckoutByCampaign(client, propertyId, range, limit = 25) {
  const response = await runReportSafe(client, {
    property: propertyName(propertyId),
    dateRanges: [range],
    dimensionFilter: mergeDimensionFilters(gaCustomerTrafficDimensionFilter(), beginCheckoutEventFilter()),
    dimensions: [{ name: "sessionCampaignName" }],
    metrics: [{ name: "sessions" }],
    orderBys: [{ metric: { metricName: "sessions" }, desc: true }],
    limit,
  });

  return (response.rows || []).map((row) => ({
    campaign: row.dimensionValues?.[0]?.value || "(not set)",
    beginCheckout: Number(row.metricValues?.[0]?.value || 0),
  }));
}

/** Total begin_checkout clicks and unique users (Stripe button → payment page). */
export async function fetchBeginCheckoutSummary(client, propertyId, range) {
  const [checkoutClicks, uniqueUsers] = await Promise.all([
    fetchBeginCheckoutEventCount(client, propertyId, range),
    fetchBeginCheckoutActiveUsers(client, propertyId, range),
  ]);
  return { checkoutClicks, uniqueUsers };
}

/** begin_checkout for itemIds matching a prefix (e.g. ccna, encor, secplus). */
export async function fetchBeginCheckoutByItemPrefix(client, propertyId, range, prefix) {
  const p = String(prefix || "").trim();
  if (!p) return { checkoutClicks: 0, uniqueUsers: 0 };

  const itemFilter = {
    filter: {
      fieldName: "itemId",
      stringFilter: { matchType: "BEGINS_WITH", value: p },
    },
  };

  const [checkoutClicks, uniqueUsers] = await Promise.all([
    fetchBeginCheckoutEventCount(client, propertyId, range, itemFilter),
    fetchBeginCheckoutActiveUsers(client, propertyId, range, itemFilter),
  ]);

  return { checkoutClicks, uniqueUsers };
}

/** begin_checkout by GA4 itemId (portal / simulation SKU from data-bcc-item-id). */
export async function fetchBeginCheckoutByItemId(client, propertyId, range, itemIds = [], limit = 30) {
  const ids = (Array.isArray(itemIds) ? itemIds : [])
    .map((id) => String(id || "").trim())
    .filter(Boolean)
    .slice(0, limit);
  if (!ids.length) return [];

  const itemFilter = {
    orGroup: {
      expressions: ids.map((itemId) => ({
        filter: {
          fieldName: "itemId",
          stringFilter: { matchType: "EXACT", value: itemId },
        },
      })),
    },
  };

  const response = await runBeginCheckoutEventReport(client, propertyId, range, {
    dimensions: [{ name: "itemId" }],
    metrics: [{ name: "eventCount" }, { name: "activeUsers" }],
    extraFilter: itemFilter,
    limit: ids.length,
  });

  const byId = Object.create(null);
  for (const row of response.rows || []) {
    const itemId = row.dimensionValues?.[0]?.value || "";
    if (!itemId) continue;
    byId[itemId] = {
      itemId,
      checkoutClicks: Number(row.metricValues?.[0]?.value || 0),
      uniqueUsers: Number(row.metricValues?.[1]?.value || 0),
    };
  }

  return ids
    .map((itemId) => byId[itemId] || { itemId, checkoutClicks: 0, uniqueUsers: 0 })
    .filter((row) => row.checkoutClicks > 0 || row.uniqueUsers > 0);
}

/**
 * Paid traffic for a source/medium pair, grouped by sessionCampaignName.
 */
export async function fetchPaidSessionsBySourceCampaign(
  client,
  propertyId,
  range,
  source,
  medium,
  limit = 25
) {
  const response = await runReportSafe(client, {
    property: propertyName(propertyId),
    dateRanges: [range],
    dimensionFilter: mergeDimensionFilters(
      gaCustomerTrafficDimensionFilter(),
      {
        filter: {
          fieldName: "sessionSource",
          stringFilter: { matchType: "EXACT", value: String(source || "").trim() },
        },
      },
      {
        filter: {
          fieldName: "sessionMedium",
          stringFilter: { matchType: "EXACT", value: String(medium || "").trim() },
        },
      }
    ),
    dimensions: [{ name: "sessionCampaignName" }],
    metrics: [{ name: "sessions" }, { name: "activeUsers" }],
    orderBys: [{ metric: { metricName: "sessions" }, desc: true }],
    limit,
  });

  return (response.rows || []).map((row) => ({
    campaign: row.dimensionValues?.[0]?.value || "(not set)",
    sessions: Number(row.metricValues?.[0]?.value || 0),
    users: Number(row.metricValues?.[1]?.value || 0),
  }));
}

/** Google Ads traffic: sessionSource = google, sessionMedium = cpc. */
export async function fetchGoogleCpcByCampaign(client, propertyId, range, limit = 25) {
  return fetchPaidSessionsBySourceCampaign(client, propertyId, range, "google", "cpc", limit);
}

/** Reddit Ads traffic: sessionSource = reddit, sessionMedium = cpc. */
export async function fetchRedditCpcByCampaign(client, propertyId, range, limit = 25) {
  return fetchPaidSessionsBySourceCampaign(client, propertyId, range, "reddit", "cpc", limit);
}

/**
 * begin_checkout sessions by campaign for a source/medium pair (Reddit vs Google split).
 */
export async function fetchBeginCheckoutBySourceCampaign(
  client,
  propertyId,
  range,
  source,
  medium,
  limit = 25
) {
  const response = await runReportSafe(client, {
    property: propertyName(propertyId),
    dateRanges: [range],
    dimensionFilter: mergeDimensionFilters(
      gaCustomerTrafficDimensionFilter(),
      beginCheckoutEventFilter(),
      {
        filter: {
          fieldName: "sessionSource",
          stringFilter: { matchType: "EXACT", value: String(source || "").trim() },
        },
      },
      {
        filter: {
          fieldName: "sessionMedium",
          stringFilter: { matchType: "EXACT", value: String(medium || "").trim() },
        },
      }
    ),
    dimensions: [{ name: "sessionCampaignName" }],
    metrics: [{ name: "sessions" }],
    orderBys: [{ metric: { metricName: "sessions" }, desc: true }],
    limit,
  });

  return (response.rows || []).map((row) => ({
    campaign: row.dimensionValues?.[0]?.value || "(not set)",
    beginCheckout: Number(row.metricValues?.[0]?.value || 0),
  }));
}

/** Organic Reddit links (replies, community posts): sessionSource = reddit, sessionMedium = organic. */
export async function fetchRedditOrganicByCampaign(client, propertyId, range, limit = 25) {
  return fetchPaidSessionsBySourceCampaign(client, propertyId, range, "reddit", "organic", limit);
}

/**
 * Page views for certification home landing paths.
 */
function pagePathExactFilter(pagePaths) {
  const paths = Array.isArray(pagePaths) ? pagePaths.filter(Boolean) : [];
  if (!paths.length) return undefined;
  return {
    orGroup: {
      expressions: paths.map((p) => ({
        filter: {
          fieldName: "pagePath",
          stringFilter: { matchType: "EXACT", value: p },
        },
      })),
    },
  };
}

function landingPageExactFilter(pagePaths) {
  const paths = Array.isArray(pagePaths) ? pagePaths.filter(Boolean) : [];
  if (!paths.length) return undefined;
  return {
    orGroup: {
      expressions: paths.map((p) => ({
        filter: {
          fieldName: "landingPage",
          stringFilter: { matchType: "EXACT", value: p },
        },
      })),
    },
  };
}

function eventNameExactFilter(eventNames) {
  const names = Array.isArray(eventNames) ? eventNames.filter(Boolean) : [];
  if (!names.length) return undefined;
  return {
    orGroup: {
      expressions: names.map((name) => ({
        filter: {
          fieldName: "eventName",
          stringFilter: { matchType: "EXACT", value: name },
        },
      })),
    },
  };
}

export async function fetchHomeLandingPageViews(client, propertyId, range, paths) {
  const pagePaths = Array.isArray(paths) ? paths.filter(Boolean) : [];
  if (!pagePaths.length) return [];

  const response = await runReportSafe(client, {
    property: propertyName(propertyId),
    dateRanges: [range],
    dimensionFilter: mergeDimensionFilters(
      gaCustomerTrafficDimensionFilter(),
      pagePathExactFilter(pagePaths)
    ),
    dimensions: [{ name: "pagePath" }],
    metrics: [{ name: "screenPageViews" }, { name: "activeUsers" }],
    orderBys: [{ metric: { metricName: "screenPageViews" }, desc: true }],
    limit: pagePaths.length,
  });

  return (response.rows || []).map((row) => ({
    pagePath: row.dimensionValues?.[0]?.value || "",
    screenPageViews: Number(row.metricValues?.[0]?.value || 0),
    activeUsers: Number(row.metricValues?.[1]?.value || 0),
  }));
}

/** Views, users, and engagement seconds per certification home path. */
export async function fetchCertHomePageMetrics(client, propertyId, range, paths) {
  const pagePaths = Array.isArray(paths) ? paths.filter(Boolean) : [];
  if (!pagePaths.length) return [];

  const response = await runReportSafe(client, {
    property: propertyName(propertyId),
    dateRanges: [range],
    dimensionFilter: mergeDimensionFilters(
      gaCustomerTrafficDimensionFilter(),
      pagePathExactFilter(pagePaths)
    ),
    dimensions: [{ name: "pagePath" }],
    metrics: [
      { name: "screenPageViews" },
      { name: "activeUsers" },
      { name: "userEngagementDuration" },
    ],
    limit: pagePaths.length,
  });

  return (response.rows || []).map((row) => {
    const views = Number(row.metricValues?.[0]?.value || 0);
    const engagementSeconds = Number(row.metricValues?.[2]?.value || 0);
    return {
      pagePath: row.dimensionValues?.[0]?.value || "",
      screenPageViews: views,
      activeUsers: Number(row.metricValues?.[1]?.value || 0),
      userEngagementSeconds: engagementSeconds,
      avgSecondsOnPage: views > 0 ? engagementSeconds / views : 0,
    };
  });
}

/** Sessions that started on a certification home page. */
export async function fetchCertHomeLandingSessions(client, propertyId, range, paths) {
  const pagePaths = Array.isArray(paths) ? paths.filter(Boolean) : [];
  if (!pagePaths.length) return [];

  const response = await runReportSafe(client, {
    property: propertyName(propertyId),
    dateRanges: [range],
    dimensionFilter: mergeDimensionFilters(
      gaCustomerTrafficDimensionFilter(),
      landingPageExactFilter(pagePaths)
    ),
    dimensions: [{ name: "landingPage" }],
    metrics: [
      { name: "sessions" },
      { name: "activeUsers" },
      { name: "averageSessionDuration" },
      { name: "engagedSessions" },
    ],
    limit: pagePaths.length,
  });

  return (response.rows || []).map((row) => ({
    landingPage: row.dimensionValues?.[0]?.value || "",
    sessions: Number(row.metricValues?.[0]?.value || 0),
    activeUsers: Number(row.metricValues?.[1]?.value || 0),
    averageSessionDurationSeconds: Number(row.metricValues?.[2]?.value || 0),
    engagedSessions: Number(row.metricValues?.[3]?.value || 0),
  }));
}

/**
 * GA4 custom/event counts on certification home paths (eventName × pagePath).
 */
export async function fetchCertHomeEventCounts(client, propertyId, range, paths, eventNames) {
  const pagePaths = Array.isArray(paths) ? paths.filter(Boolean) : [];
  const names = Array.isArray(eventNames) ? eventNames.filter(Boolean) : [];
  if (!pagePaths.length || !names.length) return [];

  try {
    const response = await runReportSafe(client, {
      property: propertyName(propertyId),
      dateRanges: [range],
      dimensionFilter: mergeDimensionFilters(
        gaCustomerTrafficDimensionFilter(),
        pagePathExactFilter(pagePaths),
        eventNameExactFilter(names)
      ),
      dimensions: [{ name: "pagePath" }, { name: "eventName" }],
      metrics: [{ name: "eventCount" }],
      limit: pagePaths.length * names.length,
    });

    return (response.rows || []).map((row) => ({
      pagePath: row.dimensionValues?.[0]?.value || "",
      eventName: row.dimensionValues?.[1]?.value || "",
      eventCount: Number(row.metricValues?.[0]?.value || 0),
    }));
  } catch (err) {
    const msg = err && err.message ? String(err.message) : "";
    if (msg.includes("INVALID_ARGUMENT")) return [];
    throw err;
  }
}

/**
 * Sessions on ad landing paths, split by session source + medium.
 * Uses landingPage (session scope) — do not mix pagePath with sessionSource in one report.
 */
export async function fetchLandingPagesTrafficBySource(
  client,
  propertyId,
  range,
  paths,
  limit = 60
) {
  const pagePaths = Array.isArray(paths) ? paths.filter(Boolean) : [];
  if (!pagePaths.length) return [];

  const response = await runReportSafe(client, {
    property: propertyName(propertyId),
    dateRanges: [range],
    dimensionFilter: mergeDimensionFilters(
      gaCustomerTrafficDimensionFilter(),
      {
        orGroup: {
          expressions: pagePaths.map((p) => ({
            filter: {
              fieldName: "landingPage",
              stringFilter: { matchType: "EXACT", value: p },
            },
          })),
        },
      }
    ),
    dimensions: [{ name: "landingPage" }, { name: "sessionSource" }, { name: "sessionMedium" }],
    metrics: [{ name: "sessions" }, { name: "activeUsers" }, { name: "engagedSessions" }],
    orderBys: [{ metric: { metricName: "sessions" }, desc: true }],
    limit,
  });

  return (response.rows || [])
    .map((row) => {
      const source = row.dimensionValues?.[1]?.value || "";
      const medium = row.dimensionValues?.[2]?.value || "";
      const sessions = Number(row.metricValues?.[0]?.value || 0);
      return {
        pagePath: row.dimensionValues?.[0]?.value || "",
        source: source || "(not set)",
        medium: medium || "(not set)",
        sourceUnavailable: source === "(data not available)" || medium === "(data not available)",
        sessions,
        users: Number(row.metricValues?.[1]?.value || 0),
        engagedSessions: Number(row.metricValues?.[2]?.value || 0),
      };
    })
    .filter((row) => row.sessions > 0 || row.users > 0);
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

const RANGE_PRESET_LABELS = {
  today: "Today",
  "7d": "Last 7 days",
  "28d": "Last 28 days",
  "90d": "Last 90 days",
};

/** UTC instant at start of the admin range preset (inclusive). */
export function utcStartFromPreset(preset) {
  const now = new Date();
  const start = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate()));
  switch (preset) {
    case "today":
      break;
    case "28d":
      start.setUTCDate(start.getUTCDate() - 27);
      break;
    case "90d":
      start.setUTCDate(start.getUTCDate() - 89);
      break;
    case "7d":
    default:
      start.setUTCDate(start.getUTCDate() - 6);
      break;
  }
  return start.toISOString();
}

export function rangePresetLabel(preset) {
  return RANGE_PRESET_LABELS[preset] || RANGE_PRESET_LABELS["7d"];
}

/** Filter CSV rows with ISO timestamps (e.g. captured_at_utc) to admin range. */
export function filterRowsFromUtcStart(rows, preset, field = "captured_at_utc") {
  const startIso = utcStartFromPreset(preset);
  return (rows || []).filter((row) => {
    const t = row && row[field];
    return typeof t === "string" && t.length >= 10 && t >= startIso;
  });
}
