/**
 * Build merged campaign test plan report for /admin calendar.
 */
import { getCampaignMarketingRegistry } from "./campaign-marketing-registry.js";
import { readCampaignPlanState } from "./campaign-plan-store.js";
import { getCampaignTestPlan } from "./campaign-test-plan-registry.js";
import {
  fetchDailyGoogleCpcCampaignBeginCheckout,
  fetchDailyGoogleCpcCampaignSessions,
  fetchDailyLandingPageViews,
  gaDateToIso,
} from "./google-analytics.js";
import { buildStripePurchasesReport } from "./stripe-purchases-report.js";

function addDaysIso(isoDate, days) {
  const d = new Date(`${isoDate}T12:00:00.000Z`);
  d.setUTCDate(d.getUTCDate() + Number(days || 0));
  return d.toISOString().slice(0, 10);
}

function indexByDate(rows, valueKey) {
  const map = Object.create(null);
  for (const row of rows || []) {
    const date = row.date;
    if (!date) continue;
    map[date] = row[valueKey] != null ? row[valueKey] : row;
  }
  return map;
}

function purchasesByUtcDate(purchases, track) {
  const map = Object.create(null);
  for (const p of purchases || []) {
    if (track && p.track !== track) continue;
    const iso = p.purchasedAt ? String(p.purchasedAt).slice(0, 10) : "";
    if (!iso) continue;
    map[iso] = (map[iso] || 0) + 1;
  }
  return map;
}

function sumManualSpend(dailyState) {
  let total = 0;
  for (const entry of Object.values(dailyState || {})) {
    if (!entry || typeof entry !== "object") continue;
    const n = Number(entry.adsSpendUsd);
    if (Number.isFinite(n)) total += n;
  }
  return total;
}

/**
 * @param {object} opts
 * @param {import('@google-analytics/data').BetaAnalyticsDataClient} [opts.client]
 * @param {string} [opts.propertyId]
 * @param {import('stripe').Stripe} [opts.stripe]
 * @param {string} [opts.campaignId]
 */
export async function buildCampaignPlanReport({ client, propertyId, stripe, campaignId = "secplus_portal" }) {
  const plan = getCampaignTestPlan(campaignId);
  if (!plan) {
    return { error: "Plan not found", campaignId };
  }

  const campaignDef =
    getCampaignMarketingRegistry().find((c) => c.id === campaignId) ||
    getCampaignMarketingRegistry().find((c) => c.id === plan.campaignId);

  let state;
  try {
    state = await readCampaignPlanState(campaignId, plan.defaultStartDate);
  } catch (err) {
    return {
      error: err?.message || "Could not load plan state",
      code: err?.code || null,
      plan,
      campaign: campaignDef || null,
    };
  }

  const startDate = state.startDate || plan.defaultStartDate;
  const endDate = addDaysIso(startDate, plan.durationDays - 1);
  const range = { startDate, endDate };

  /** @type {Record<string, object>} */
  const autoByDate = Object.create(null);

  let gaError = null;
  if (client && propertyId && campaignDef) {
    try {
      const [sessionsDaily, checkoutDaily, landingDaily] = await Promise.all([
        fetchDailyGoogleCpcCampaignSessions(client, propertyId, range, campaignDef.utmCampaign),
        fetchDailyGoogleCpcCampaignBeginCheckout(client, propertyId, range, campaignDef.utmCampaign),
        fetchDailyLandingPageViews(client, propertyId, range, campaignDef.landingPath),
      ]);

      const sessionsMap = indexByDate(sessionsDaily, "paidSessions");
      const checkoutMap = indexByDate(checkoutDaily, "beginCheckout");
      const landingMap = indexByDate(landingDaily, "landingPageViews");

      const allDates = new Set([
        ...Object.keys(sessionsMap),
        ...Object.keys(checkoutMap),
        ...Object.keys(landingMap),
      ]);

      for (const date of allDates) {
        autoByDate[date] = {
          paidSessions: Number(sessionsMap[date] || 0),
          beginCheckout: Number(checkoutMap[date] || 0),
          landingPageViews: Number(landingMap[date] || 0),
        };
      }
    } catch (err) {
      gaError = err?.message || "GA4 daily funnel failed";
    }
  }

  /** @type {Record<string, number>} */
  let stripeByDate = Object.create(null);
  let stripeError = null;
  if (stripe) {
    try {
      const stripeReport = await buildStripePurchasesReport(stripe, "90d");
      const inWindow = (stripeReport.purchases || []).filter((p) => {
        const day = p.purchasedAt ? String(p.purchasedAt).slice(0, 10) : "";
        return day >= startDate && day <= endDate;
      });
      stripeByDate = purchasesByUtcDate(inWindow, campaignDef?.product || "secplus");
    } catch (err) {
      stripeError = err?.message || "Stripe daily purchases failed";
    }
  }

  const milestonesByDay = Object.create(null);
  for (const m of plan.milestones || []) {
    milestonesByDay[m.day] = m;
  }

  const calendarDays = [];
  let runningSpend = 0;
  let runningPurchases = 0;
  let runningCheckouts = 0;
  let runningPaidSessions = 0;

  for (let i = 0; i < plan.durationDays; i += 1) {
    const date = addDaysIso(startDate, i);
    const dayNumber = i + 1;
    const manual = state.daily[date] && typeof state.daily[date] === "object" ? state.daily[date] : {};
    const auto = autoByDate[date] || {
      paidSessions: 0,
      beginCheckout: 0,
      landingPageViews: 0,
    };
    const secplusPurchases = Number(stripeByDate[date] || 0);

    runningSpend += Number(manual.adsSpendUsd || 0);
    runningPurchases += secplusPurchases;
    runningCheckouts += Number(auto.beginCheckout || 0);
    runningPaidSessions += Number(auto.paidSessions || 0);

    calendarDays.push({
      date,
      dayNumber,
      milestone: milestonesByDay[dayNumber] || null,
      manual,
      auto: { ...auto, secplusPurchases },
      running: {
        adsSpendUsd: runningSpend,
        secplusPurchases: runningPurchases,
        beginCheckout: runningCheckouts,
        paidSessions: runningPaidSessions,
      },
    });
  }

  const totalSteps = plan.phases.reduce((n, p) => n + (p.steps?.length || 0), 0);
  const completedSteps = (state.completedStepIds || []).length;

  return {
    plan,
    campaign: campaignDef || null,
    state: {
      startDate,
      endDate,
      completedStepIds: state.completedStepIds || [],
      updatedAt: state.updatedAt || null,
    },
    calendarDays,
    totals: {
      manualAdsSpendUsd: sumManualSpend(state.daily),
      autoPaidSessions: runningPaidSessions,
      autoBeginCheckout: runningCheckouts,
      stripeSecplusPurchases: runningPurchases,
      stepsCompleted: completedSteps,
      stepsTotal: totalSteps,
    },
    progress: {
      stepsCompleted: completedSteps,
      stepsTotal: totalSteps,
      daysElapsed: Math.min(
        plan.durationDays,
        Math.max(0, Math.floor((Date.now() - new Date(`${startDate}T00:00:00.000Z`).getTime()) / 86400000) + 1)
      ),
      daysTotal: plan.durationDays,
    },
    autoSources: {
      ga4: client && propertyId ? (gaError ? { error: gaError } : { ok: true }) : { skipped: true },
      stripe: stripe ? (stripeError ? { error: stripeError } : { ok: true }) : { skipped: true },
    },
    storagePath: `data/reports/campaign-plan/${campaignId}.json`,
    fetchedAt: new Date().toISOString(),
  };
}

export function formatGaDateForDisplay(isoDate) {
  return gaDateToIso(String(isoDate || "").replace(/-/g, ""));
}
