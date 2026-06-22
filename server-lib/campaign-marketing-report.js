/**
 * Merge static campaign registry with GA4 metrics for /admin marketing section.
 */
import { getCampaignMarketingRegistry } from "./campaign-marketing-registry.js";
import {
  fetchBeginCheckoutByCampaign,
  fetchBeginCheckoutBySourceCampaign,
  fetchGoogleCpcByCampaign,
  fetchHomeLandingPageViews,
  fetchRedditCpcByCampaign,
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
  const landingPaths = [...new Set(registry.map((c) => c.landingPath))];

  const [
    sessionsByCampaign,
    checkoutByCampaign,
    checkoutGoogleCpc,
    checkoutRedditCpc,
    googleCpcByCampaign,
    redditCpcByCampaign,
    landingPages,
  ] = await Promise.all([
    fetchSessionsByCampaign(client, propertyId, range),
    fetchBeginCheckoutByCampaign(client, propertyId, range),
    fetchBeginCheckoutBySourceCampaign(client, propertyId, range, "google", "cpc"),
    fetchBeginCheckoutBySourceCampaign(client, propertyId, range, "reddit", "cpc"),
    fetchGoogleCpcByCampaign(client, propertyId, range),
    fetchRedditCpcByCampaign(client, propertyId, range),
    fetchHomeLandingPageViews(client, propertyId, range, landingPaths),
  ]);

  const sessionsMap = indexByCampaign(sessionsByCampaign);
  const checkoutMap = indexByCampaign(checkoutByCampaign);
  const checkoutGoogleMap = indexByCampaign(checkoutGoogleCpc);
  const checkoutRedditMap = indexByCampaign(checkoutRedditCpc);
  const googleCpcMap = indexByCampaign(googleCpcByCampaign);
  const redditCpcMap = indexByCampaign(redditCpcByCampaign);
  const landingMap = Object.create(null);
  for (const row of landingPages) {
    landingMap[row.pagePath] = row;
  }

  const campaigns = registry.map((def) => {
    const utm = def.utmCampaign;
    const isReddit = def.channel === "reddit";
    const paidMap = isReddit ? redditCpcMap : googleCpcMap;
    const checkoutChannelMap = isReddit ? checkoutRedditMap : checkoutGoogleMap;
    const sess = sessionsMap[utm] || {};
    const paid = paidMap[utm] || {};
    const checkout =
      checkoutChannelMap[utm] ||
      (isReddit ? {} : checkoutMap[utm]) ||
      {};
    const landing = landingMap[def.landingPath] || {};
    const paidSessions = Number(paid.sessions || 0);
    const beginCheckout = Number(checkout.beginCheckout || 0);

    return {
      ...def,
      platformCampaignName:
        def.redditAdsCampaignName || def.googleAdsCampaignName || def.label,
      metrics: {
        sessions: paidSessions || Number(sess.sessions || 0),
        users: Number(paid.users || sess.users || 0),
        engagedSessions: Number(sess.engagedSessions || 0),
        pageViews: Number(sess.pageViews || 0),
        beginCheckout,
        paidSessions,
        landingPageViews: Number(landing.screenPageViews || 0),
        landingPageUsers: Number(landing.activeUsers || 0),
        checkoutRate: paidSessions > 0 ? beginCheckout / paidSessions : null,
      },
    };
  });

  const otherRedditSessions = redditCpcByCampaign
    .filter((row) => !registry.some((d) => d.channel === "reddit" && d.utmCampaign === row.campaign))
    .slice(0, 5);

  const otherGoogleCpcSessions = googleCpcByCampaign
    .filter((row) => !registry.some((d) => d.channel === "google" && d.utmCampaign === row.campaign))
    .slice(0, 5);

  return {
    campaigns,
    otherRedditSessions,
    otherGoogleCpcSessions,
    allBeginCheckout: checkoutByCampaign,
    allGoogleCpc: googleCpcByCampaign,
    allRedditCpc: redditCpcByCampaign,
    landingPages,
  };
}
