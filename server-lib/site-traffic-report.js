/**
 * Site traffic + campaign conversion report for /admin → Site traffic (GA4).
 */
import {
  adjustLandingBeginCheckoutCount,
  resolveGaAdjustments,
} from "./campaign-ga-adjustments.js";
import {
  AD_LANDING_MONITOR_PATHS,
  CAMPAIGN_MARKETING_REGISTRY,
} from "./campaign-marketing-registry.js";
import {
  fetchBeginCheckoutByAdContent,
  fetchBeginCheckoutByCampaign,
  fetchBeginCheckoutByItemId,
  fetchBeginCheckoutSummary,
  fetchCertHomeEventCounts,
  fetchCertHomeLandingSessions,
  fetchCertHomePageMetrics,
  fetchGoogleCpcByAdContent,
  fetchGoogleCpcByCampaign,
  fetchHomeLandingPageViews,
  fetchLandingPagesTrafficBySource,
  fetchRedditCpcByCampaign,
  fetchSessionsByCampaign,
  fetchTopPages,
  rangePresetLabel,
} from "./google-analytics.js";
import { buildCampaignConversionRecommendations } from "./campaign-conversion-recommendations.js";
import {
  buildSecplusAdGroupMetrics,
  SECPLUS_GOOGLE_CAMPAIGN,
} from "./secplus-google-ad-groups.js";

export const PRIMARY_LANDING_PATH =
  (process.env.BCC_GA_PRIMARY_LANDING_PATH || "/comptia-sec+-home.html").trim();

const PRIMARY_LANDING_LABEL = "Security+ home";

function campaignAliases(def) {
  return [def.utmCampaign, def.googleAdsCampaignName, def.redditAdsCampaignName]
    .map((s) => String(s || "").trim())
    .filter(Boolean);
}

function rowMatchesCampaign(rowCampaign, def) {
  const c = String(rowCampaign || "").trim();
  if (!c || c === "(not set)") return false;
  const lower = c.toLowerCase();
  return campaignAliases(def).some((alias) => alias.toLowerCase() === lower);
}

function sumCampaignMetric(rows, def, field) {
  let total = 0;
  for (const row of rows || []) {
    if (rowMatchesCampaign(row.campaign, def)) {
      total += Number(row[field] || 0);
    }
  }
  return total;
}

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
  const allItemIds = [
    ...new Set(CAMPAIGN_MARKETING_REGISTRY.flatMap((c) => c.conversionItemIds || [])),
  ];

  const [
    sessionsByCampaign,
    checkoutByCampaign,
    checkoutSummary,
    checkoutByItem,
    topPages,
    landingBySource,
    adLandingViews,
    googleCpc,
    redditCpc,
    secplusAdContentSessions,
    secplusAdContentCheckout,
    primaryPageMetrics,
    primaryLandingSessions,
    primaryEvents,
  ] = await Promise.all([
    fetchSessionsByCampaign(client, propertyId, range, 40),
    fetchBeginCheckoutByCampaign(client, propertyId, range, 40),
    fetchBeginCheckoutSummary(client, propertyId, range),
    fetchBeginCheckoutByItemId(client, propertyId, range, allItemIds, 20),
    fetchTopPages(client, propertyId, range, 20),
    fetchLandingPagesTrafficBySource(client, propertyId, range, AD_LANDING_MONITOR_PATHS, 80),
    fetchHomeLandingPageViews(client, propertyId, range, AD_LANDING_MONITOR_PATHS),
    fetchGoogleCpcByCampaign(client, propertyId, range, 20),
    fetchRedditCpcByCampaign(client, propertyId, range, 20),
    fetchGoogleCpcByAdContent(
      client,
      propertyId,
      range,
      SECPLUS_GOOGLE_CAMPAIGN.campaignAliases,
      20
    ),
    fetchBeginCheckoutByAdContent(
      client,
      propertyId,
      range,
      SECPLUS_GOOGLE_CAMPAIGN.campaignAliases,
      20
    ),
    fetchCertHomePageMetrics(client, propertyId, range, [PRIMARY_LANDING_PATH]),
    fetchCertHomeLandingSessions(client, propertyId, range, [PRIMARY_LANDING_PATH]),
    fetchCertHomeEventCounts(client, propertyId, range, [PRIMARY_LANDING_PATH], [
      "begin_checkout",
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

  let primaryCheckout = Number(eventsByName.begin_checkout || 0);
  const secplusAdj = resolveGaAdjustments("secplus_portal");
  if (secplusAdj) {
    primaryCheckout = adjustLandingBeginCheckoutCount(primaryCheckout, secplusAdj);
  }

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
    adjustmentNote: secplusAdj?.notes || "",
  };

  const campaigns = CAMPAIGN_MARKETING_REGISTRY.map((def) => {
    const sessions = sumCampaignMetric(sessionsByCampaign, def, "sessions");
    const users = sumCampaignMetric(sessionsByCampaign, def, "users");
    const engagedSessions = sumCampaignMetric(sessionsByCampaign, def, "engagedSessions");
    let beginCheckout = sumCampaignMetric(checkoutByCampaign, def, "beginCheckout");
    const adjustments = resolveGaAdjustments(def.id);
    if (adjustments) {
      beginCheckout = adjustLandingBeginCheckoutCount(beginCheckout, adjustments);
    }
    const landingViews =
      adLandingViews.find((r) => r.pagePath === def.landingPath)?.screenPageViews || 0;

    return {
      id: def.id,
      channel: def.channel,
      product: def.product,
      label: def.label,
      utmCampaign: def.utmCampaign,
      landingPath: def.landingPath,
      primaryOffer: def.primaryOffer,
      sessions,
      users,
      engagedSessions,
      beginCheckout,
      landingPageViews: Number(landingViews),
      checkoutRate: pct(beginCheckout, sessions),
      landingCheckoutRate: pct(beginCheckout, landingViews),
      conversionItemIds: def.conversionItemIds || [],
      adsDashboardUrl: def.adsDashboardUrl || null,
      adjustmentNote: adjustments?.notes || "",
    };
  }).sort((a, b) => b.sessions - a.sessions || b.beginCheckout - a.beginCheckout);

  const channelTotals = {
    googleCpc: {
      sessions: (googleCpc || []).reduce((s, r) => s + Number(r.sessions || 0), 0),
      beginCheckout: 0,
    },
    redditCpc: {
      sessions: (redditCpc || []).reduce((s, r) => s + Number(r.sessions || 0), 0),
      beginCheckout: 0,
    },
  };
  for (const row of checkoutByCampaign || []) {
    const checkout = Number(row.beginCheckout || 0);
    if ((googleCpc || []).some((g) => g.campaign === row.campaign)) {
      channelTotals.googleCpc.beginCheckout += checkout;
    }
    if ((redditCpc || []).some((g) => g.campaign === row.campaign)) {
      channelTotals.redditCpc.beginCheckout += checkout;
    }
  }

  const secplusAdGroups = buildSecplusAdGroupMetrics(secplusAdContentSessions, secplusAdContentCheckout);

  const reportCore = {
    rangeLabel: rangePresetLabel(rangePreset),
    primaryLanding: primary,
    siteCheckout: checkoutSummary,
    campaigns,
    secplusAdGroups,
    secplusGoogleCampaign: {
      id: SECPLUS_GOOGLE_CAMPAIGN.id,
      label: SECPLUS_GOOGLE_CAMPAIGN.googleAdsCampaignName,
      utmCampaign: SECPLUS_GOOGLE_CAMPAIGN.utmCampaign,
      dailyBudgetUsd: SECPLUS_GOOGLE_CAMPAIGN.dailyBudgetUsd,
      planDoc: SECPLUS_GOOGLE_CAMPAIGN.planDoc,
      adminPath: SECPLUS_GOOGLE_CAMPAIGN.adminAnalyticsPath,
    },
    checkoutByItem: checkoutByItem || [],
    topPages: topPages || [],
    landingBySource: landingBySource || [],
    adLandingViews: adLandingViews || [],
    gaCampaigns: (sessionsByCampaign || []).slice(0, 25),
    channelTotals,
  };

  const recommendations = buildCampaignConversionRecommendations(reportCore);

  return {
    ...reportCore,
    recommendations,
    note:
      "Use this section to tune ads and landing pages. begin_checkout = Stripe click (primary conversion). " +
      "Security+ Google ad groups break down by utm_content (core-exam-prep, mil-gov-8140, student-workforce). " +
      "Log spend and copy changes in Daily campaign log, then refresh and check Recommendations. " +
      "Spend and clicks: Google Ads / Reddit dashboards (links below).",
  };
}
