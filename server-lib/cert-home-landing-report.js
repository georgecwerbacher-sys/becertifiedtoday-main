/**
 * Certification home landing pages — GA4 traffic + sample funnel (CSV) for /admin.
 */
import {
  aggregateSampleLeadReport,
  normalizeSampleEvent,
  normalizeSampleKind,
  normalizeSampleProduct,
} from "./sample-lead-analytics.js";
import {
  fetchCertHomeEventCounts,
  fetchCertHomeLandingSessions,
  fetchCertHomePageMetrics,
  filterRowsFromUtcStart,
  rangePresetLabel,
} from "./google-analytics.js";

export const CERT_HOME_PAGES = [
  {
    path: "/ccna-home.html",
    product: "ccna",
    label: "CCNA home",
    previewUrl: "https://becertifiedtoday.com/ccna-home.html",
  },
  {
    path: "/ccnp-home.html",
    product: "encor",
    label: "CCNP ENCOR home",
    previewUrl: "https://becertifiedtoday.com/ccnp-home.html",
  },
  {
    path: "/comptia-sec+-home.html",
    product: "secplus",
    label: "Security+ home",
    previewUrl: "https://becertifiedtoday.com/comptia-sec+-home.html",
  },
];

const TRACKED_GA4_EVENTS = [
  "begin_checkout",
  "home_offer_popup_shown",
  "home_offer_popup_click",
  "home_offer_popup_dismiss",
  "ccna_free_sim_start",
  "encor_free_sim_start",
  "secplus_free_sim_start",
  "generate_lead",
];

function mapByPath(rows, pathField) {
  const out = Object.create(null);
  for (const row of rows || []) {
    const key = row[pathField];
    if (key) out[key] = row;
  }
  return out;
}

function eventCountsForPage(eventRows, pagePath) {
  const out = Object.create(null);
  for (const row of eventRows || []) {
    if (row.pagePath !== pagePath) continue;
    out[row.eventName] = (out[row.eventName] || 0) + Number(row.eventCount || 0);
  }
  return out;
}

function freeSimStarts(events, product) {
  const key =
    product === "ccna"
      ? "ccna_free_sim_start"
      : product === "encor"
        ? "encor_free_sim_start"
        : "secplus_free_sim_start";
  return Number(events[key] || 0);
}

function aggregateSampleByProduct(rows) {
  const report = aggregateSampleLeadReport(rows);
  const byProduct = Object.create(null);
  for (const page of CERT_HOME_PAGES) {
    const s = report.summary[page.product] || {};
    const kinds = report.byKind[page.product] || {};
    byProduct[page.product] = {
      sampleCompletions: Number(s.sampleCompletions || 0),
      emailModalOpens: Number(s.emailModalOpens || 0),
      submitAttempts: Number(s.submitAttempts || 0),
      captureSuccesses: Number(s.captureSuccesses || 0),
      byKind: {
        questions: Number(kinds.questions || 0),
        dnd: Number(kinds.dnd || 0),
        lab: Number(kinds.lab || 0),
        simulation: Number(kinds.simulation || 0),
      },
    };
  }
  return byProduct;
}

/**
 * @param {import('@google-analytics/data').BetaAnalyticsDataClient} client
 * @param {string} propertyId
 * @param {{ startDate: string, endDate: string }} range
 * @param {string} rangePreset
 * @param {Record<string, string>[]} [sampleLeadRows]
 */
export async function buildCertHomeLandingReport(
  client,
  propertyId,
  range,
  rangePreset = "7d",
  sampleLeadRows = []
) {
  const paths = CERT_HOME_PAGES.map((p) => p.path);
  const sampleInRange = filterRowsFromUtcStart(sampleLeadRows, rangePreset);
  const sampleByProduct = aggregateSampleByProduct(sampleInRange);

  const [pageMetrics, landingSessions, eventRows] = await Promise.all([
    fetchCertHomePageMetrics(client, propertyId, range, paths),
    fetchCertHomeLandingSessions(client, propertyId, range, paths),
    fetchCertHomeEventCounts(client, propertyId, range, paths, TRACKED_GA4_EVENTS),
  ]);

  const pageByPath = mapByPath(pageMetrics, "pagePath");
  const landingByPath = mapByPath(landingSessions, "landingPage");

  const pages = CERT_HOME_PAGES.map((def) => {
    const page = pageByPath[def.path] || {};
    const landing = landingByPath[def.path] || {};
    const events = eventCountsForPage(eventRows, def.path);
    const sample = sampleByProduct[def.product] || {};

    return {
      ...def,
      screenPageViews: Number(page.screenPageViews || 0),
      activeUsers: Number(page.activeUsers || 0),
      userEngagementSeconds: Number(page.userEngagementSeconds || 0),
      avgSecondsOnPage: Number(page.avgSecondsOnPage || 0),
      landingSessions: Number(landing.sessions || 0),
      landingUsers: Number(landing.activeUsers || 0),
      avgSessionDurationSeconds: Number(landing.averageSessionDurationSeconds || 0),
      engagedSessions: Number(landing.engagedSessions || 0),
      checkoutClicks: Number(events.begin_checkout || 0),
      offerPopupShown: Number(events.home_offer_popup_shown || 0),
      offerPopupClick: Number(events.home_offer_popup_click || 0),
      offerPopupDismiss: Number(events.home_offer_popup_dismiss || 0),
      freeSimStarts: freeSimStarts(events, def.product),
      generateLead: Number(events.generate_lead || 0),
      sampleCompletions: Number(sample.sampleCompletions || 0),
      emailModalOpens: Number(sample.emailModalOpens || 0),
      emailSubmitAttempts: Number(sample.submitAttempts || 0),
      emailCaptureSuccesses: Number(sample.captureSuccesses || 0),
      sampleByKind: sample.byKind || {},
    };
  });

  const totals = pages.reduce(
    (acc, p) => {
      acc.screenPageViews += p.screenPageViews;
      acc.landingSessions += p.landingSessions;
      acc.sampleCompletions += p.sampleCompletions;
      acc.checkoutClicks += p.checkoutClicks;
      return acc;
    },
    { screenPageViews: 0, landingSessions: 0, sampleCompletions: 0, checkoutClicks: 0 }
  );

  return {
    rangeLabel: rangePresetLabel(rangePreset),
    pages,
    totals,
    note:
      "GA4: page views and time on page for ccna-home, ccnp-home, and comptia-sec+-home. " +
      "Landing sessions = visits that started on that URL. Sample/popup email metrics come from home-sample CSV logs. " +
      "10-day offer popup events (shown/click/dismiss) require this deploy — older visits won't include them.",
  };
}

/** Export sample event labels for admin tooltips. */
export { normalizeSampleEvent, normalizeSampleKind, normalizeSampleProduct };
