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

/** @typedef {{ id: string, label: string, hint?: string, syncField?: string, syncFields?: string[], milestone?: boolean }} DailyChecklistTask */
/** @typedef {{ heading: string, summary?: string, tasks: DailyChecklistTask[] }} DailyChecklist */

const EVERY_DAY_TASKS = /** @type {DailyChecklistTask[]} */ ([
  {
    id: "log-spend-clicks",
    label: "Log Google Ads spend + clicks (form below)",
    syncFields: ["adsSpendUsd", "adsClicks"],
  },
]);

/** @type {Record<number, DailyChecklistTask[]>} */
const SECPLUS_DAY_TASKS = {
  1: [
    {
      id: "d1-mobile-checkout",
      label: "Phone test: live ad URL → 30-day checkout → GA4 Realtime begin_checkout",
    },
    {
      id: "d1-ads-30d-only",
      label: "Ads: RSA + sitelinks 30-day only — remove any $9.99 / 10-day copy",
    },
    {
      id: "d1-promo-progress",
      label: "Confirm Google promo progress (~$256+ account spend toward $500)",
    },
  ],
  2: [
    {
      id: "d2-landing-rate",
      label: "Note landing checkout rate in ops notes if GA4 has sessions",
    },
  ],
  3: [
    {
      id: "d3-search-terms",
      label: "Export Search terms → add negatives (course, free, bootcamp, dump, Dion/PDF)",
      syncField: "negativesAdded",
    },
    {
      id: "d3-remove-practice-questions",
      label: "Remove generic *practice questions* positives; negate exam/test shopper terms (64-keyword list)",
      syncField: "keywordCsvUpdated",
    },
    {
      id: "d3-keyword-csv",
      label: "Sync secplus-keywords.csv + checklist (npm run sync:secplus-checklist)",
      syncField: "keywordCsvUpdated",
    },
    {
      id: "d3-overview-export",
      label: "Save Overview cards CSV zip → google-ads-overview-YYYY-MM-DD/",
    },
  ],
  4: [{ id: "d4-hold", label: "Hold budget, RSA, and keywords — no changes (week 1)" }],
  5: [{ id: "d5-hold", label: "Hold budget, RSA, and keywords — no changes (week 1)" }],
  6: [{ id: "d6-hold", label: "Hold budget, RSA, and keywords — no changes (week 1)" }],
  7: [
    {
      id: "d7-funnel-review",
      label: "Review funnel: landing views → landing checkout → Stripe purchases",
    },
    {
      id: "d7-landing-first",
      label: "If checkout < 2% with ≥ 50 paid sessions: landing/RSA before keyword cuts",
    },
    {
      id: "d7-pause-keywords",
      label: "If checkout OK: pause phrase keywords with ≥ 20 clicks / 0 checkout",
    },
  ],
  8: [{ id: "d8-log-only", label: "Continue daily log — no budget or RSA changes unless tier-1 cutback" }],
  9: [{ id: "d9-log-only", label: "Continue daily log — watch landing checkout trend" }],
  10: [{ id: "d10-log-only", label: "Continue daily log — promote any term with ≥ 3 clicks + checkout" }],
  11: [{ id: "d11-log-only", label: "Continue daily log" }],
  12: [{ id: "d12-log-only", label: "Continue daily log" }],
  13: [{ id: "d13-log-only", label: "Continue daily log — prep one landing test for day 14" }],
  14: [
    {
      id: "d14-landing-ship",
      label: "Ship one landing test (hero, sample CTA, purchase block, or mobile sticky)",
      syncField: "landingChange",
    },
    {
      id: "d14-exact-keywords",
      label: "Promote ≥ 3 converting search terms to [exact]",
    },
    {
      id: "d14-compare-weeks",
      label: "Compare week-2 vs week-1 landing checkout rate in notes",
    },
  ],
  15: [{ id: "d15-log-only", label: "Continue daily log — one change at a time" }],
  16: [{ id: "d16-log-only", label: "Continue daily log" }],
  17: [{ id: "d17-log-only", label: "Continue daily log" }],
  18: [{ id: "d18-log-only", label: "Continue daily log" }],
  19: [{ id: "d19-log-only", label: "Continue daily log — draft day-21 readout notes" }],
  20: [{ id: "d20-log-only", label: "Continue daily log — fill monthly scorecard if month-end" }],
  21: [
    {
      id: "d21-scorecard",
      label: "21-day decision: ≥ 5 checkouts OR ≥ 2 purchases → continue; else tier-1/2 cutback",
    },
    {
      id: "d21-monthly-csv",
      label: "Update secplus-monthly-scorecard.csv for the calendar month",
    },
    {
      id: "d21-document-winners",
      label: "Document keyword winners + landing changes in ops notes",
    },
  ],
};

/**
 * @param {number} dayNumber
 * @param {PlanMilestone|null|undefined} milestone
 * @returns {DailyChecklist}
 */
export function getDailyChecklistForDay(dayNumber, milestone) {
  const day = Math.max(1, Math.min(21, Number(dayNumber) || 1));
  const tasks = [
    ...EVERY_DAY_TASKS,
    ...(SECPLUS_DAY_TASKS[day] || []),
  ];
  if (milestone?.actions?.length) {
    milestone.actions.forEach((text, i) => {
      const exists = tasks.some((t) => t.label === text);
      if (!exists) {
        tasks.push({
          id: `milestone-${day}-${i}`,
          label: text,
          milestone: true,
        });
      }
    });
  }
  return {
    heading: milestone?.title || `Day ${day}`,
    summary: milestone?.summary || "",
    tasks,
  };
}

/** @type {CampaignTestPlan} */
export const SECPLUS_PORTAL_21D_PLAN = {
  id: "secplus_portal_21d",
  campaignId: "secplus_portal",
  title: "Security+ Google Ads · 21-day conversion test",
  defaultStartDate: "2026-06-23",
  durationDays: 21,
  goal:
    "Maximize qualified clicks within $15/day and $2.75 max CPC, then optimize post-click: landing → begin_checkout → purchase. Budget follows converting keywords and search terms — not raw volume alone.",
  successCriteria: [
    "Confirmed scorecard (Sec+ Phase 1 Scorecard): monthly loss ≤ 20% ($100 on $500 spend)",
    "21-day continue: ≥ 5 paid begin_checkout OR ≥ 2 all-in purchases; fail: ≥ $150 spend / 0 checkout",
    "Paid session → begin_checkout ≥ 2% month avg (≥ 3% healthy) — landing tracked hardest",
    "Landing begin_checkout ÷ landing page views trends up week over week",
    "Log Ads clicks daily — click → checkout rate improves as landing/RSA align",
    "Search terms stay PBQ / sim / readiness — course/free negated; promote converters to [exact]",
    "RSA + landing: 30-day $19.99 only · no 10-day · message match on PBQ + timed sim",
  ],
  phases: [
    {
      id: "prep",
      title: "Before launch",
      steps: [
        { id: "prep-stripe", label: "Stripe $19.99 / 30-day product live" },
        { id: "prep-checkout", label: "Checkout works on cert home (desktop + mobile)" },
        { id: "prep-samples", label: "MCQ + 3-scenario PBQ preview reachable from landing (dark web IR, WLAN, firewall ACL)" },
        { id: "prep-ga4", label: "GA4 begin_checkout imported as Primary conversion in Google Ads" },
        { id: "prep-keywords", label: "Keyword list synced (secplus-keywords.csv)" },
        { id: "prep-rsa", label: "RSA reviewed — pin Timed 90-Min Exam Sim (not price)" },
        { id: "prep-landing", label: "Landing conversion baseline — test click → checkout in GA4 Realtime" },
      ],
    },
    {
      id: "shell",
      title: "Campaign shell",
      steps: [
        { id: "shell-name", label: "Campaign: Security+ SY0-701 · Exam prep · becertifiedtoday" },
        { id: "shell-budget", label: "Budget $15/day · Search only · partners off" },
        { id: "shell-bid", label: "Maximize clicks · max CPC $2.75 (clicks feed landing tests)" },
        { id: "shell-geo", label: "Geo US, CA, UK, AU · Presence only" },
        { id: "shell-utm", label: "utm_campaign secplus_portal on all ads" },
        { id: "shell-ai", label: "AI Max / URL expansion off" },
        { id: "shell-sitelinks", label: "6 sitelinks pasted — incl. Try 3 PBQ Samples on landing" },
      ],
    },
    {
      id: "adgroup",
      title: "Ad group · Security+ PBQ Practice",
      steps: [
        { id: "ag-name", label: "Single ad group enabled: Security+ PBQ Practice" },
        { id: "ag-url", label: "Final URL → comptia-sec+-home.html with UTMs" },
        { id: "ag-keywords", label: "Keywords pasted from checklist (rank 1–64 · PBQ/sim/timed — no generic practice questions)" },
        { id: "ag-rsa", label: "RSA live — H2 pinned Timed 90-Min Exam Sim" },
        { id: "ag-neg-campaign", label: "Campaign-level negatives pasted" },
        { id: "ag-neg-adgroup", label: "Ad group-level negatives pasted" },
        {
          id: "ag-practice-q-cut",
          label: "Generic practice-questions tier removed; exam-shopper negatives added (2026-06-25)",
        },
      ],
    },
    {
      id: "launch",
      title: "Launch check",
      steps: [
        { id: "launch-url", label: "Final URL opens cert home with correct UTMs" },
        { id: "launch-ga4-test", label: "Test ad click → landing view → begin_checkout in GA4" },
        { id: "launch-mobile", label: "Mobile checkout on cert home verified" },
        { id: "launch-ads-on", label: "Ads enabled (or note pause reason in daily log)" },
      ],
    },
  ],
  milestones: [
    {
      day: 3,
      title: "Day 3 · Search terms + landing baseline",
      summary: "Negatives for junk intent; record landing checkout rate vs clicks logged.",
      actions: [
        "Export Search terms → add negatives (course, dump, Dion, PDF, generic practice test/exam)",
        "Remove comptia/sy0/security+ practice questions positives; paste pending campaign negatives",
        "Log spend + clicks; save Overview export to repo; note landing checkout rate",
      ],
      pullKeywordCsv: true,
    },
    {
      day: 7,
      title: "Day 7 · Conversion review (not CPC alone)",
      summary: "Prioritize landing + checkout rate; tune max CPC only if clicks lack checkout.",
      actions: [
        "Admin: paid sessions → landing views → landing checkout → Stripe",
        "If checkout < 2% with ≥ 50 paid sessions: fix landing/RSA before keyword cuts",
        "If checkout OK: pause phrase keywords with ≥ 20 clicks / 0 checkout",
        "Hold $15/day unless tier-1 cutback rules in Phase 1 Scorecard",
      ],
      pullKeywordCsv: true,
    },
    {
      day: 14,
      title: "Day 14 · Landing iteration",
      summary: "Double down on search terms that checkout; one landing improvement shipped.",
      actions: [
        "Promote ≥ 3 converting search terms to [exact]",
        "Ship one landing test (headline, sample CTA, purchase block, or mobile sticky)",
        "Compare week-2 vs week-1 landing checkout rate",
      ],
      optional: true,
    },
    {
      day: 21,
      title: "Day 21 · Scorecard readout",
      summary: "Apply Sec+ Phase 1 Scorecard continue / cutback decision.",
      actions: [
        "21-day: ≥ 5 checkouts OR ≥ 2 purchases → continue; else tier-1/2 cutback",
        "Monthly scorecard row for calendar month",
        "Document keyword winners + landing changes for next cycle",
      ],
      pullKeywordCsv: true,
    },
  ],
  trackingSections: [
    {
      id: "google_ads",
      label: "Google Ads (manual daily) — top of funnel",
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
      label: "GA4 funnel (auto) — post-click priority",
      source: "auto",
      fields: [
        "paidSessions",
        "landingPageViews",
        "landingBeginCheckout",
        "landingCheckoutRate",
        "beginCheckout",
        "checkoutRate",
        "clickToCheckoutRate",
      ],
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
      fields: ["notes", "adsPaused", "landingChange", "keywordCsvUpdated", "negativesAdded"],
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
