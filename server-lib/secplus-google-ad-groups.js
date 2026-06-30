/**
 * Security+ Google Search ad groups — shared by marketing docs, registry, and /admin GA4.
 * Obsidian source: marketing-research/Sec+ Campaign/Sec+ One-Campaign Ad Group Plan.md
 */

/** @typedef {object} SecplusGoogleAdGroupDef */
/**
 * @property {string} slug
 * @property {string} adGroupName
 * @property {string} utmContent
 * @property {string} displayPath
 * @property {string} pinH1
 * @property {string} intent
 * @property {string} rsaDoc — repo-relative Obsidian/markdown path + anchor hint
 * @property {string} keywordsDoc
 */

export const SECPLUS_GOOGLE_CAMPAIGN = {
  id: "secplus_portal",
  googleAdsCampaignName: "Security+ SY0-701 · US Search",
  /** Legacy GA4 / Ads names still seen in historical data */
  campaignAliases: [
    "secplus_portal",
    "Security+ SY0-701 · US Search",
    "Security+ SY0-701 · Exam prep · becertifiedtoday",
    "Security+ PBQ Practice",
  ],
  utmCampaign: "secplus_portal",
  utmSource: "google",
  utmMedium: "cpc",
  dailyBudgetUsd: 25,
  maxCpcUsd: 2.75,
  landingPath: "/comptia-sec+-home.html",
  primaryConversion: "begin_checkout",
  conversionItemIds: ["secplus_portal_30d"],
  primaryOffer: "30-day $19.99 — one US Search campaign, three ad groups, $25/day shared",
  planDoc: "marketing-research/Sec+ Campaign/Sec+ One-Campaign Ad Group Plan.md",
  rsaDoc: "marketing-research/Sec+ Campaign/Sec+ RSA Copy.md",
  keywordsDoc: "marketing-research/Sec+ Campaign/Sec+ Keywords.md",
  checklistDoc: "marketing-research/Sec+ Campaign/Sec+ Google Ads Build Checklist.md",
  adminAnalyticsPath: "/admin#section-secplus-ad-groups",
};

/** @type {SecplusGoogleAdGroupDef[]} */
export const SECPLUS_GOOGLE_AD_GROUPS = [
  {
    slug: "core-exam-prep",
    adGroupName: "Core Exam Prep",
    utmContent: "core-exam-prep",
    displayPath: "Security+ / Exam-Prep",
    pinH1: "SY0-701 Exam Prep Online",
    intent: "Timed sim, readiness, adaptive review, browser prep",
    rsaDoc: "marketing-research/Sec+ Campaign/Sec+ RSA Copy.md",
    keywordsDoc: "marketing-research/Sec+ Campaign/Sec+ Keywords.md",
  },
  {
    slug: "mil-gov-8140",
    adGroupName: "Military Gov 8140",
    utmContent: "mil-gov-8140",
    displayPath: "Security+ / DoD-8140",
    pinH1: "Security+ for DoD 8140",
    intent: "DoD 8140, federal, contractor, military job requirement",
    rsaDoc: "marketing-research/Sec+ Campaign/Sec+ RSA Copy - Military Gov 8140.md",
    keywordsDoc: "marketing-research/Sec+ Campaign/Sec+ Keywords.md",
  },
  {
    slug: "student-workforce",
    adGroupName: "Student Workforce",
    utmContent: "student-workforce",
    displayPath: "Security+ / Career-Prep",
    pinH1: "Security+ Career Prep",
    intent: "Students, educators, veterans, workforce / career transition",
    rsaDoc: "marketing-research/Sec+ Campaign/Sec+ RSA Copy - Student Workforce.md",
    keywordsDoc: "marketing-research/Sec+ Campaign/Sec+ Keywords.md",
  },
];

/** Legacy utm_content values — show in admin when still receiving traffic */
export const SECPLUS_LEGACY_UTM_CONTENT = [
  {
    slug: "pbq-wedge",
    adGroupName: "Legacy · PBQ Practice",
    utmContent: "pbq-wedge",
    displayPath: "—",
    pinH1: "Security+ PBQ Practice",
    intent: "Phase 1 wedge (replace RSA when ad group is migrated)",
    rsaDoc: "marketing-research/Sec+ Campaign/Sec+ RSA Copy.md",
    keywordsDoc: "marketing-research/Sec+ Campaign/Sec+ Keywords.md",
  },
];

export function normalizeUtmContent(raw) {
  return String(raw || "")
    .trim()
    .toLowerCase();
}

export function secplusFinalUrl(utmContent) {
  const content = String(utmContent || "").trim();
  return `https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=${encodeURIComponent(content)}`;
}

export function allSecplusAdGroupDefs() {
  return [...SECPLUS_GOOGLE_AD_GROUPS, ...SECPLUS_LEGACY_UTM_CONTENT];
}

export function getSecplusAdGroupByContent(utmContent) {
  const key = normalizeUtmContent(utmContent);
  return allSecplusAdGroupDefs().find((g) => normalizeUtmContent(g.utmContent) === key) || null;
}

function pct(num, den) {
  const n = Number(num) || 0;
  const d = Number(den) || 0;
  if (d <= 0) return null;
  return n / d;
}

/**
 * Merge GA4 sessionManualAdContent rows with registry ad groups (fixed order).
 * @param {{ adContent: string, sessions: number, users?: number, engagedSessions?: number }[]} sessionRows
 * @param {{ adContent: string, beginCheckout: number }[]} checkoutRows
 */
export function buildSecplusAdGroupMetrics(sessionRows, checkoutRows) {
  const sessionsByContent = Object.create(null);
  const checkoutByContent = Object.create(null);

  for (const row of sessionRows || []) {
    const key = normalizeUtmContent(row.adContent);
    if (!key || key === "(not set)") continue;
    if (!sessionsByContent[key]) {
      sessionsByContent[key] = { sessions: 0, users: 0, engagedSessions: 0 };
    }
    sessionsByContent[key].sessions += Number(row.sessions || 0);
    sessionsByContent[key].users += Number(row.users || 0);
    sessionsByContent[key].engagedSessions += Number(row.engagedSessions || 0);
  }

  for (const row of checkoutRows || []) {
    const key = normalizeUtmContent(row.adContent);
    if (!key || key === "(not set)") continue;
    checkoutByContent[key] = (checkoutByContent[key] || 0) + Number(row.beginCheckout || 0);
  }

  const seen = new Set();
  const primary = SECPLUS_GOOGLE_AD_GROUPS.map((def) => {
    const key = normalizeUtmContent(def.utmContent);
    seen.add(key);
    const s = sessionsByContent[key] || {};
    const beginCheckout = checkoutByContent[key] || 0;
    const sessions = Number(s.sessions || 0);
    return {
      ...def,
      campaignId: SECPLUS_GOOGLE_CAMPAIGN.id,
      utmCampaign: SECPLUS_GOOGLE_CAMPAIGN.utmCampaign,
      finalUrl: secplusFinalUrl(def.utmContent),
      sessions,
      users: Number(s.users || 0),
      engagedSessions: Number(s.engagedSessions || 0),
      beginCheckout,
      checkoutRate: pct(beginCheckout, sessions),
      isLegacy: false,
    };
  });

  const legacy = [];
  for (const def of SECPLUS_LEGACY_UTM_CONTENT) {
    const key = normalizeUtmContent(def.utmContent);
    const s = sessionsByContent[key];
    if (!s || Number(s.sessions || 0) <= 0) continue;
    seen.add(key);
    const beginCheckout = checkoutByContent[key] || 0;
    const sessions = Number(s.sessions || 0);
    legacy.push({
      ...def,
      campaignId: SECPLUS_GOOGLE_CAMPAIGN.id,
      utmCampaign: SECPLUS_GOOGLE_CAMPAIGN.utmCampaign,
      finalUrl: secplusFinalUrl(def.utmContent),
      sessions,
      users: Number(s.users || 0),
      engagedSessions: Number(s.engagedSessions || 0),
      beginCheckout,
      checkoutRate: pct(beginCheckout, sessions),
      isLegacy: true,
    });
  }

  const other = [];
  for (const [key, s] of Object.entries(sessionsByContent)) {
    if (seen.has(key)) continue;
    const beginCheckout = checkoutByContent[key] || 0;
    const sessions = Number(s.sessions || 0);
    if (sessions <= 0) continue;
    other.push({
      slug: key,
      adGroupName: `Other · ${key}`,
      utmContent: key,
      displayPath: "—",
      pinH1: "—",
      intent: "Untracked utm_content — fix Final URL in Google Ads",
      rsaDoc: SECPLUS_GOOGLE_CAMPAIGN.rsaDoc,
      keywordsDoc: SECPLUS_GOOGLE_CAMPAIGN.keywordsDoc,
      campaignId: SECPLUS_GOOGLE_CAMPAIGN.id,
      utmCampaign: SECPLUS_GOOGLE_CAMPAIGN.utmCampaign,
      finalUrl: secplusFinalUrl(key),
      sessions,
      users: Number(s.users || 0),
      engagedSessions: Number(s.engagedSessions || 0),
      beginCheckout,
      checkoutRate: pct(beginCheckout, sessions),
      isLegacy: true,
      isOther: true,
    });
  }

  return [...primary, ...legacy, ...other.sort((a, b) => b.sessions - a.sessions)];
}
