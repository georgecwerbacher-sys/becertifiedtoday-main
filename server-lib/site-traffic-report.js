/**
 * Site traffic report for /admin → Site traffic (GA4).
 */
import {
  fetchBeginCheckoutByItemId,
  fetchBeginCheckoutSummary,
  fetchCertHomeEventCounts,
  fetchCertHomeLandingSessions,
  fetchCertHomePageMetrics,
  fetchTopPages,
  rangePresetLabel,
} from "./google-analytics.js";

export const PRIMARY_LANDING_PATH =
  (process.env.BCC_GA_PRIMARY_LANDING_PATH || "/comptia-sec+-home.html").trim();

const PRIMARY_LANDING_LABEL = "Security+ home";

const CHECKOUT_ITEM_IDS = [
  "secplus_portal_10d",
  "secplus_portal_30d",
  "secplus_portal_3d",
];

function pct(num, den) {
  const n = Number(num) || 0;
  const d = Number(den) || 0;
  if (d <= 0) return null;
  return n / d;
}

/**
 * @param {import('@google-analytics/data').BetaAnalyticsDataClient} client
 * @param {string} propertyId
 * @param {{ startDate: string, endDate: string }} range
 * @param {string} rangePreset
 */
export async function buildSiteTrafficReport(client, propertyId, range, rangePreset = "7d") {
  const [checkoutSummary, checkoutByItem, topPages, primaryPageMetrics, primaryLandingSessions, primaryEvents] =
    await Promise.all([
      fetchBeginCheckoutSummary(client, propertyId, range),
      fetchBeginCheckoutByItemId(client, propertyId, range, CHECKOUT_ITEM_IDS, 20),
      fetchTopPages(client, propertyId, range, 20),
      fetchCertHomePageMetrics(client, propertyId, range, [PRIMARY_LANDING_PATH]),
      fetchCertHomeLandingSessions(client, propertyId, range, [PRIMARY_LANDING_PATH]),
      fetchCertHomeEventCounts(client, propertyId, range, [PRIMARY_LANDING_PATH], [
        "begin_checkout",
        "purchase",
        "secplus_free_sim_start",
        "home_offer_popup_shown",
        "home_offer_popup_click",
        "generate_lead",
      ]),
    ]);

  const page = primaryPageMetrics[0] || {};
  const landing = primaryLandingSessions[0] || {};
  const eventsByName = Object.create(null);
  for (const row of primaryEvents || []) {
    if (row.pagePath !== PRIMARY_LANDING_PATH) continue;
    eventsByName[row.eventName] = Number(row.eventCount || 0);
  }

  const primaryCheckout = Number(eventsByName.begin_checkout || 0);
  const primary = {
    path: PRIMARY_LANDING_PATH,
    label: PRIMARY_LANDING_LABEL,
    screenPageViews: Number(page.screenPageViews || 0),
    activeUsers: Number(page.activeUsers || 0),
    avgSecondsOnPage: Number(page.avgSecondsOnPage || 0),
    landingSessions: Number(landing.sessions || 0),
    engagedSessions: Number(landing.engagedSessions || 0),
    avgSessionDurationSeconds: Number(landing.averageSessionDurationSeconds || 0),
    beginCheckout: primaryCheckout,
    purchases: Number(eventsByName.purchase || 0),
    freeSimStarts: Number(eventsByName.secplus_free_sim_start || 0),
    offerPopupShown: Number(eventsByName.home_offer_popup_shown || 0),
    offerPopupClick: Number(eventsByName.home_offer_popup_click || 0),
    generateLead: Number(eventsByName.generate_lead || 0),
    checkoutRate: pct(primaryCheckout, Number(page.screenPageViews || 0)),
    purchaseRate: pct(Number(eventsByName.purchase || 0), primaryCheckout),
  };

  return {
    rangeLabel: rangePresetLabel(rangePreset),
    primaryLanding: primary,
    siteCheckout: checkoutSummary,
    checkoutByItem: checkoutByItem || [],
    topPages: topPages || [],
    note: "begin_checkout = Stripe purchase button click. Completed purchases appear under Stripe checkout.",
  };
}
