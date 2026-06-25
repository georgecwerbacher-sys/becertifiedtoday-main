/**
 * Merge static campaign registry with GA4 metrics for /admin marketing section.
 */
import { getAdminTrackedCampaignRegistry } from "./campaign-marketing-registry.js";
import { adjustLandingBeginCheckoutCount } from "./campaign-ga-adjustments.js";
import {
  fetchBeginCheckoutByCampaign,
  fetchBeginCheckoutBySourceCampaign,
  fetchCertHomeEventCounts,
  fetchGoogleCpcByCampaign,
  fetchHomeLandingPageViews,
  fetchRedditCpcByCampaign,
  fetchSessionsByCampaign,
  rangeDaysFromPreset,
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
 * @param {string} [rangePreset]
 */
export async function buildCampaignMarketingReport(client, propertyId, range, rangePreset = "7d") {
  const registry = getAdminTrackedCampaignRegistry();
  const landingPaths = [...new Set(registry.map((c) => c.landingPath))];
  const rangeDays = rangeDaysFromPreset(rangePreset);

  const [
    sessionsByCampaign,
    checkoutByCampaign,
    checkoutGoogleCpc,
    checkoutRedditCpc,
    googleCpcByCampaign,
    redditCpcByCampaign,
    landingPages,
    landingEvents,
  ] = await Promise.all([
    fetchSessionsByCampaign(client, propertyId, range),
    fetchBeginCheckoutByCampaign(client, propertyId, range),
    fetchBeginCheckoutBySourceCampaign(client, propertyId, range, "google", "cpc"),
    fetchBeginCheckoutBySourceCampaign(client, propertyId, range, "reddit", "cpc"),
    fetchGoogleCpcByCampaign(client, propertyId, range),
    fetchRedditCpcByCampaign(client, propertyId, range),
    fetchHomeLandingPageViews(client, propertyId, range, landingPaths),
    fetchCertHomeEventCounts(client, propertyId, range, landingPaths, ["begin_checkout"]),
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

  const checkoutEventsByPath = Object.create(null);
  for (const row of landingEvents || []) {
    if (row.eventName !== "begin_checkout") continue;
    checkoutEventsByPath[row.pagePath] =
      (checkoutEventsByPath[row.pagePath] || 0) + Number(row.eventCount || 0);
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
    const projectionDays = def.projectionWindowDays || 21;
    const estimatedSpendInRangeUsd = def.dailyBudgetUsd * rangeDays;
    const estimatedSpendProjectionUsd = def.dailyBudgetUsd * projectionDays;
    const scaleToProjection =
      rangeDays > 0 && projectionDays !== rangeDays ? projectionDays / rangeDays : 1;

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
        landingBeginCheckout: Number(checkoutEventsByPath[def.landingPath] || 0),
        checkoutRate: paidSessions > 0 ? beginCheckout / paidSessions : null,
      },
      projection: {
        rangeDays,
        projectionDays,
        estimatedSpendInRangeUsd,
        estimatedSpendProjectionUsd,
        scaledPaidSessions: paidSessions * scaleToProjection,
        scaledBeginCheckout: beginCheckout * scaleToProjection,
        sessionToCheckoutRate: paidSessions > 0 ? beginCheckout / paidSessions : null,
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
    rangePreset,
    rangeDays,
    projectionWindowDays: 21,
    campaigns,
    otherRedditSessions,
    otherGoogleCpcSessions,
    allBeginCheckout: checkoutByCampaign,
    allGoogleCpc: googleCpcByCampaign,
    allRedditCpc: redditCpcByCampaign,
    landingPages,
  };
}

/**
 * Merge 21-day plan manual log into admin-tracked campaigns (running spend/clicks + next-day review).
 * @param {object|null|undefined} marketingReport
 * @param {object|null|undefined} planReport
 */
export function mergeCampaignPlanIntoMarketing(marketingReport, planReport) {
  if (!marketingReport || marketingReport.error || !planReport || planReport.error) {
    return marketingReport;
  }
  const planCampaignId = planReport.plan?.campaignId || planReport.campaign?.id || "secplus_portal";
  const totals = planReport.totals || {};
  const progress = planReport.progress || {};
  const nextDayReview = planReport.nextDayReview || null;
  const dailyBudget = Number(planReport.campaign?.dailyBudgetUsd || 15);
  const durationDays = Number(planReport.plan?.durationDays || 21);
  const daysElapsed = Number(progress.daysElapsed || 0);
  const daysRemaining = Math.max(0, durationDays - daysElapsed);
  const loggedSpend = Number(totals.manualAdsSpendUsd || 0);
  const loggedClicks = Number(totals.manualAdsClicks || 0);
  const projectedSpend21d = loggedSpend + daysRemaining * dailyBudget;

  const gaAdjustments = planReport.state?.gaAdjustments || null;
  const landingDeduction = Number(gaAdjustments?.landingBeginCheckout || 0);

  marketingReport.campaigns = (marketingReport.campaigns || []).map((c) => {
    if (c.id !== planCampaignId) return c;
    const rawLandingCheckout = Number(c.metrics?.landingBeginCheckout || 0);
    const adjustedLandingCheckout = adjustLandingBeginCheckoutCount(rawLandingCheckout, gaAdjustments);
    const metrics =
      landingDeduction > 0 && c.metrics
        ? { ...c.metrics, landingBeginCheckout: adjustedLandingCheckout }
        : c.metrics;
    return {
      ...c,
      metrics,
      gaAdjustments: gaAdjustments || undefined,
      planLog: {
        startDate: planReport.state?.startDate || null,
        endDate: planReport.state?.endDate || null,
        daysElapsed,
        daysTotal: durationDays,
        daysLogged: Number(totals.daysLogged || progress.daysLogged || 0),
        spendUsd: loggedSpend,
        clicks: loggedClicks,
        impressions: Number(totals.manualAdsImpressions || 0),
        avgCpc: totals.manualAdsAvgCpc != null ? totals.manualAdsAvgCpc : null,
        projectedSpend21d,
        landingCheckoutRate: totals.landingCheckoutRate,
        checkoutRate: totals.checkoutRate,
        clickToCheckoutRate: totals.clickToCheckoutRate,
      },
      nextDayReview,
      projection: {
        ...(c.projection || {}),
        estimatedSpendInRangeUsd: loggedSpend,
        estimatedSpendProjectionUsd: projectedSpend21d,
        planBased: true,
      },
    };
  });
  marketingReport.planLinked = true;
  marketingReport.planCampaignId = planCampaignId;
  return marketingReport;
}
