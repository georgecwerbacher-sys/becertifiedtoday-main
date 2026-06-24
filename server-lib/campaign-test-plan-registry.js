/**
 * Static 21-day campaign test plans for /admin calendar + checklist.
 */

/** @typedef {{ id: string, label: string, phaseId?: string }} PlanStep */
/** @typedef {{ id: string, title: string, steps: PlanStep[] }} PlanPhase */
/** @typedef {{ day: number, title: string, summary: string, actions: string[], pullKeywordCsv?: boolean, optional?: boolean }} PlanMilestone */
/** @typedef {{ id: string, label: string, source: 'manual'|'auto'|'mixed', fields: string[] }} TrackingSection */

/**
 * @typedef {object} CampaignTestPlan
 * @property {string} id
 * @property {string} campaignId
 * @property {string} title
 * @property {string} defaultStartDate — YYYY-MM-DD
 * @property {number} durationDays
 * @property {string} goal
 * @property {string[]} successCriteria
 * @property {PlanPhase[]} phases
 * @property {PlanMilestone[]} milestones
 * @property {TrackingSection[]} trackingSections
 */

/** @type {CampaignTestPlan} */
export const SECPLUS_PORTAL_21D_PLAN = {
  id: "secplus_portal_21d",
  campaignId: "secplus_portal",
  title: "Security+ Google Ads · 21-day conversion test",
  defaultStartDate: "2026-06-22",
  durationDays: 21,
  goal:
    "Validate $20/day Google Search ($2.75 max CPC) driving 30-day Security+ ($19.99) purchases with message match on PBQ + timed sim — not course-shopper traffic.",
  successCriteria: [
    "Paid session → begin_checkout ≥ 3% before judging purchase rate",
    "Ad spend ÷ Stripe Sec+ purchase ≤ $40 by day 21 (break-even on ads alone at ~$2 CPC)",
    "Search terms stay PBQ / sim / readiness intent — course terms negated",
    "RSA + landing show 30-day offer only for Google paid traffic",
  ],
  phases: [
    {
      id: "prep",
      title: "Before launch",
      steps: [
        { id: "prep-stripe", label: "Stripe $19.99 / 30-day product live" },
        { id: "prep-checkout", label: "Checkout works on cert home (desktop + mobile)" },
        { id: "prep-samples", label: "MCQ + dark web PBQ samples reachable from landing" },
        { id: "prep-ga4", label: "GA4 begin_checkout imported as Primary conversion" },
        { id: "prep-keywords", label: "Keyword list synced (secplus-keywords.csv)" },
        { id: "prep-rsa", label: "RSA reviewed — pin Timed 90-Min Exam Sim (not price)" },
      ],
    },
    {
      id: "shell",
      title: "Campaign shell",
      steps: [
        { id: "shell-name", label: "Campaign: Security+ SY0-701 · Exam prep · becertifiedtoday" },
        { id: "shell-budget", label: "Budget $20/day · Search only · partners off" },
        { id: "shell-bid", label: "Maximize clicks · max CPC $2.75" },
        { id: "shell-geo", label: "Geo US, CA, UK, AU · Presence only" },
        { id: "shell-utm", label: "utm_campaign secplus_portal on all ads" },
        { id: "shell-ai", label: "AI Max / URL expansion off" },
        { id: "shell-sitelinks", label: "6 sitelinks pasted (30-day lead sitelink)" },
      ],
    },
    {
      id: "adgroup",
      title: "Ad group · Security+ PBQ Practice",
      steps: [
        { id: "ag-name", label: "Single ad group enabled: Security+ PBQ Practice" },
        { id: "ag-url", label: "Final URL → comptia-sec+-home.html with UTMs" },
        { id: "ag-keywords", label: "Keywords pasted from checklist (rank 1–67)" },
        { id: "ag-rsa", label: "RSA live — H2 pinned Timed 90-Min Exam Sim" },
        { id: "ag-neg-campaign", label: "Campaign-level negatives pasted" },
        { id: "ag-neg-adgroup", label: "Ad group-level negatives pasted" },
      ],
    },
    {
      id: "launch",
      title: "Launch check",
      steps: [
        { id: "launch-url", label: "Final URL opens cert home with correct UTMs" },
        { id: "launch-ga4-test", label: "Test click fires begin_checkout in GA4" },
        { id: "launch-mobile", label: "Mobile checkout on cert home verified" },
        { id: "launch-ads-on", label: "Ads enabled (or note pause reason in daily log)" },
      ],
    },
  ],
  milestones: [
    {
      day: 3,
      title: "Day 3 · Search terms + delivery",
      summary: "First search terms pull; confirm Eligible vs rarely served keywords.",
      actions: [
        "Export Search terms → add negatives (course, video, bootcamp, instructor names)",
        "Optional: export keywords CSV → sync repo delivery status",
        "Log actual Google spend + clicks in daily tracker",
      ],
      pullKeywordCsv: true,
    },
    {
      day: 7,
      title: "Day 7 · Week-1 review",
      summary: "CTR, checkout rate, and CPA vs $20/day budget.",
      actions: [
        "Review admin funnel: paid sessions → begin_checkout → Stripe Sec+",
        "Hold $20/day or adjust max CPC based on checkout rate (not purchase alone yet)",
        "Refresh keyword delivery status if impressions flat",
      ],
      pullKeywordCsv: true,
    },
    {
      day: 14,
      title: "Day 14 · Mid-test (optional)",
      summary: "Only if spend or impressions look flat after week 1.",
      actions: [
        "Check scaled 21-day projection in campaign tracker",
        "Pause broad terms that click but never checkout",
      ],
      optional: true,
    },
    {
      day: 21,
      title: "Day 21 · Full test readout",
      summary: "Decide continue, pause, or change offer/bids before next cycle.",
      actions: [
        "Total ad spend vs Stripe Sec+ revenue in test window",
        "Export final search terms + keyword CSV",
        "Document decision: scale, hold, pivot RSA, or narrow keywords",
      ],
      pullKeywordCsv: true,
    },
  ],
  trackingSections: [
    {
      id: "google_ads",
      label: "Google Ads (manual daily)",
      source: "manual",
      fields: [
        "adsSpendUsd",
        "adsImpressions",
        "adsClicks",
        "adsAvgCpc",
        "adsCtr",
        "adsConversions",
      ],
    },
    {
      id: "ga4_funnel",
      label: "GA4 funnel (auto)",
      source: "auto",
      fields: ["paidSessions", "beginCheckout", "landingPageViews"],
    },
    {
      id: "stripe",
      label: "Stripe Sec+ (auto)",
      source: "auto",
      fields: ["secplusPurchases"],
    },
    {
      id: "ops",
      label: "Ops notes (manual)",
      source: "manual",
      fields: ["notes", "adsPaused", "keywordCsvUpdated", "negativesAdded"],
    },
  ],
};

const PLANS_BY_CAMPAIGN_ID = Object.freeze({
  secplus_portal: SECPLUS_PORTAL_21D_PLAN,
});

export function getCampaignTestPlan(campaignId) {
  const id = String(campaignId || "").trim();
  const plan = PLANS_BY_CAMPAIGN_ID[id];
  return plan ? { ...plan, phases: plan.phases.map((p) => ({ ...p, steps: [...p.steps] })) } : null;
}

export function listCampaignTestPlans() {
  return Object.values(PLANS_BY_CAMPAIGN_ID).map((p) => ({
    id: p.id,
    campaignId: p.campaignId,
    title: p.title,
    durationDays: p.durationDays,
  }));
}
