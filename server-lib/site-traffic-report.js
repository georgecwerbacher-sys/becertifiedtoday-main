/**
 * Site traffic report for /admin → Site traffic (GA4).
 * Website metrics only — no paid-channel or Google Ads attribution.
 */
import {
  fetchCertHomeLandingSessions,
  fetchCertHomePageMetrics,
  fetchSiteEventCounts,
  fetchTopPages,
  rangePresetLabel,
} from "./google-analytics.js";

export const PRIMARY_LANDING_PATH =
  (process.env.BCC_GA_PRIMARY_LANDING_PATH || "/comptia-sec+-home.html").trim();

const PRIMARY_LANDING_LABEL = "Security+ home";

const SITE_CONVERSION_EVENTS = [
  { key: "begin_checkout", label: "Checkout clicks" },
  { key: "purchase", label: "Purchases (GA4)" },
  { key: "secplus_free_sim_start", label: "Free sim starts" },
  { key: "generate_lead", label: "Lead forms" },
];

/**
 * @param {import('@google-analytics/data').BetaAnalyticsDataClient} client
 * @param {string} propertyId
 * @param {{ startDate: string, endDate: string }} range
 * @param {string} rangePreset
 */
export async function buildSiteTrafficReport(client, propertyId, range, rangePreset = "7d") {
  const [topPages, primaryPageMetrics, primaryLandingSessions, siteEvents] = await Promise.all([
    fetchTopPages(client, propertyId, range, 20),
    fetchCertHomePageMetrics(client, propertyId, range, [PRIMARY_LANDING_PATH]),
    fetchCertHomeLandingSessions(client, propertyId, range, [PRIMARY_LANDING_PATH]),
    fetchSiteEventCounts(
      client,
      propertyId,
      range,
      SITE_CONVERSION_EVENTS.map((e) => e.key)
    ),
  ]);

  const page = primaryPageMetrics[0] || {};
  const landing = primaryLandingSessions[0] || {};
  const eventsByName = Object.create(null);
  for (const row of siteEvents || []) {
    eventsByName[row.eventName] = {
      eventCount: Number(row.eventCount || 0),
      activeUsers: Number(row.activeUsers || 0),
    };
  }

  const conversions = SITE_CONVERSION_EVENTS.map((def) => {
    const row = eventsByName[def.key] || {};
    return {
      eventName: def.key,
      label: def.label,
      eventCount: Number(row.eventCount || 0),
      activeUsers: Number(row.activeUsers || 0),
    };
  });

  const primary = {
    path: PRIMARY_LANDING_PATH,
    label: PRIMARY_LANDING_LABEL,
    screenPageViews: Number(page.screenPageViews || 0),
    activeUsers: Number(page.activeUsers || 0),
    avgSecondsOnPage: Number(page.avgSecondsOnPage || 0),
    landingSessions: Number(landing.sessions || 0),
    engagedSessions: Number(landing.engagedSessions || 0),
    avgSessionDurationSeconds: Number(landing.averageSessionDurationSeconds || 0),
  };

  return {
    rangeLabel: rangePresetLabel(rangePreset),
    primaryLanding: primary,
    conversions,
    topPages: topPages || [],
    note: "Completed purchases are also listed under Stripe checkout. GA4 purchase events may lag Stripe.",
  };
}
