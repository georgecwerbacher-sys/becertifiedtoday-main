/**
 * Merge static campaign registry with GA4 metrics for /admin marketing section.
 */
import { getCampaignMarketingRegistry } from "./campaign-marketing-registry.js";
import {
  fetchBeginCheckoutByCampaign,
  fetchGoogleCpcByCampaign,
  fetchHomeLandingPageViews,
  fetchSessionsByCampaign,
} from "./google-analytics.js";

function indexByCampaign(rows) {
  const map = Object.create(null);
  for (const row of rows || []) {
    const key = String(row.campaign || "").trim();
    if (!key) continue;
    map[key] = row;
  }
  return map;
}

/**
 * @param {import('@google-analytics/data').BetaAnalyticsDataClient} client
 * @param {string} propertyId
 * @param {{ startDate: string, endDate: string }} range
 */
export async function buildCampaignMarketingReport(client, propertyId, range) {
  const registry = getCampaignMarketingRegistry();
  const landingPaths = registry.map((c) => c.landingPath);

  const [sessionsByCampaign, checkoutByCampaign, cpcByCampaign, landingPages] =
    await Promise.all([
      fetchSessionsByCampaign(client, propertyId, range),
      fetchBeginCheckoutByCampaign(client, propertyId, range),
      fetchGoogleCpcByCampaign(client, propertyId, range),
      fetchHomeLandingPageViews(client, propertyId, range, landingPaths),
    ]);

  const sessionsMap = indexByCampaign(sessionsByCampaign);
  const checkoutMap = indexByCampaign(checkoutByCampaign);
  const cpcMap = indexByCampaign(cpcByCampaign);
  const landingMap = Object.create(null);
  for (const row of landingPages) {
    landingMap[row.pagePath] = row;
  }

  const campaigns = registry.map((def) => {
    const utm = def.utmCampaign;
    const sess = sessionsMap[utm] || {};
    const checkout = checkoutMap[utm] || {};
    const cpc = cpcMap[utm] || {};
    const landing = landingMap[def.landingPath] || {};
    const sessions = Number(sess.sessions || 0);
    const beginCheckout = Number(checkout.beginCheckout || 0);

    return {
      ...def,
      metrics: {
        sessions,
        users: Number(sess.users || 0),
        engagedSessions: Number(sess.engagedSessions || 0),
        pageViews: Number(sess.pageViews || 0),
        beginCheckout,
        googleCpcSessions: Number(cpc.sessions || 0),
        googleCpcUsers: Number(cpc.users || 0),
        landingPageViews: Number(landing.screenPageViews || 0),
        landingPageUsers: Number(landing.activeUsers || 0),
        checkoutRate: sessions > 0 ? beginCheckout / sessions : null,
      },
    };
  });

  const otherCampaignSessions = sessionsByCampaign
    .filter((row) => !registry.some((d) => d.utmCampaign === row.campaign))
    .slice(0, 10);

  return {
    campaigns,
    otherCampaignSessions,
    allBeginCheckout: checkoutByCampaign,
    allGoogleCpc: cpcByCampaign,
    landingPages,
  };
}
