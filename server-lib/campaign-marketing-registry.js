/**
 * Google Ads / UTM campaign definitions for admin marketing dashboard.
 * Setup copy lives in scripts/*-google-ads.{txt,md} (not deployed to public/).
 */

/** @typedef {object} CampaignMarketingDefinition */
/**
 * @property {string} id
 * @property {'ccna'|'encor'|'secplus'} product
 * @property {string} label
 * @property {string} googleAdsCampaignName
 * @property {string} utmCampaign — matches GA4 sessionCampaignName when tagged
 * @property {string} adGroup
 * @property {number} dailyBudgetUsd
 * @property {number} maxCpcUsd
 * @property {string} landingPath
 * @property {string} landingHash
 * @property {string} utmContentPrimary
 * @property {string} finalUrl
 * @property {string} primaryConversion
 * @property {string[]} conversionItemIds
 * @property {string} primaryOffer
 * @property {string} setupDoc
 * @property {string} setupDocTxt
 * @property {string[]} sampleTracks
 */

/** @type {CampaignMarketingDefinition[]} */
export const CAMPAIGN_MARKETING_REGISTRY = [
  {
    id: "ccna_portal",
    product: "ccna",
    label: "CCNA 200-301 · portal · 7-day test",
    googleAdsCampaignName: "CCNA 200-301 · Exam prep · becertifiedtoday",
    utmCampaign: "ccna_portal",
    adGroup: "ccna_portal_10v1, ccna_browser_labs",
    dailyBudgetUsd: 25,
    maxCpcUsd: 3.0,
    landingPath: "/ccna-home.html",
    landingHash: "#purchase",
    utmContentPrimary: "portal-10d",
    finalUrl:
      "https://becertifiedtoday.com/ccna-home.html?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=portal-10d#purchase",
    primaryConversion: "begin_checkout",
    conversionItemIds: ["ccna_portal_10d", "ccna_portal_30d"],
    primaryOffer: "10-day $9.99 — initial AdWords test through 2026-06-21",
    setupDoc: "scripts/ccna-google-ads-campaign-checklist.csv",
    setupDocTxt: "scripts/ccna-google-ads-campaign-checklist-README.txt",
    sampleTracks: ["ccna-questions", "ccna-dnd", "ccna-vlan"],
  },
  {
    id: "ccna_wedge_lab",
    product: "ccna",
    label: "CCNA_Wedge_Lab · browser CLI labs",
    googleAdsCampaignName: "CCNA_Wedge_Lab",
    utmCampaign: "ccna_wedge_lab",
    adGroup: "CCNA_Wedge_Lab",
    dailyBudgetUsd: 15,
    maxCpcUsd: 4.5,
    landingPath: "/ccna-home.html",
    landingHash: "",
    utmContentPrimary: "exam-readiness",
    finalUrl:
      "https://becertifiedtoday.com/ccna-home.html?utm_source=google&utm_medium=cpc&utm_campaign=ccna_wedge_lab&utm_content=exam-readiness",
    primaryConversion: "begin_checkout",
    conversionItemIds: ["ccna_portal_10d", "ccna_portal_30d"],
    primaryOffer: "10-day $9.99 · 30-day $19.99 — ccna-home exam-ready funnel",
    setupDoc: "scripts/ccna-wedge-lab-google-ads-checklist.csv",
    setupDocTxt: "scripts/ccna-wedge-lab-google-ads-README.txt",
    sampleTracks: ["ccna-vlan", "ccna-questions", "ccna-dnd"],
  },
  {
    id: "encor_portal",
    product: "encor",
    label: "CCNP ENCOR 350-401 · portal · 7-day test",
    googleAdsCampaignName: "CCNP ENCOR 350-401 · Exam prep · becertifiedtoday",
    utmCampaign: "encor_portal",
    adGroup: "encor_portal",
    dailyBudgetUsd: 10,
    maxCpcUsd: 2.75,
    landingPath: "/ccnp-home.html",
    landingHash: "#purchase",
    utmContentPrimary: "portal-30d",
    finalUrl:
      "https://becertifiedtoday.com/ccnp-home.html?utm_source=google&utm_medium=cpc&utm_campaign=encor_portal&utm_content=portal-30d#purchase",
    primaryConversion: "begin_checkout",
    conversionItemIds: ["encor_portal_30d", "encor_portal_10d"],
    primaryOffer: "30-day $19.99 primary — initial AdWords test through 2026-06-21",
    setupDoc: "scripts/encor-portal-10d-google-ads.md",
    setupDocTxt: "scripts/encor-portal-10d-google-ads.txt",
    sampleTracks: ["encor-questions", "encor-dnd", "encor-lab"],
  },
  {
    id: "secplus_portal",
    product: "secplus",
    label: "Security+ SY0-701 · PBQ Practice · $20/day",
    googleAdsCampaignName: "Security+ SY0-701 · Exam prep · becertifiedtoday",
    utmCampaign: "secplus_portal",
    adGroup: "Security+ PBQ Practice",
    dailyBudgetUsd: 20,
    maxCpcUsd: 2.75,
    landingPath: "/secplus/pbq-practice-browser.html",
    landingHash: "",
    utmContentPrimary: "pbq-wedge",
    finalUrl:
      "https://becertifiedtoday.com/secplus/pbq-practice-browser.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=pbq-wedge",
    primaryConversion: "begin_checkout",
    conversionItemIds: ["secplus_portal_10d", "secplus_portal_30d"],
    primaryOffer: "10-day $9.99 · 30-day $19.99 — Security+ PBQ Practice · $20/day",
    setupDoc: "marketing-research/Sec+ Campaign/secplus-campaign-checklist.csv",
    setupDocTxt: "marketing-research/Sec+ Campaign/Sec+ Notes.md",
    sampleTracks: ["sim-dark-web", "questions"],
  },
];

export function getCampaignMarketingRegistry() {
  return CAMPAIGN_MARKETING_REGISTRY.map((c) => ({ ...c }));
}

/** Ad landing paths monitored on /admin (exact GA4 pagePath). */
export const AD_LANDING_MONITOR_PATHS = [
  "/ccna-home.html",
  "/ccnp-home.html",
  "/comptia-sec+-home.html",
  "/secplus/pbq-practice-browser.html",
  "/ccna/labs-without-gns3.html",
];

export function utmCampaignNames() {
  return CAMPAIGN_MARKETING_REGISTRY.map((c) => c.utmCampaign);
}
