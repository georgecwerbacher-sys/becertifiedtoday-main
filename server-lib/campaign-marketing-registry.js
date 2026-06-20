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
 * @property {string} [redditFinalUrl] — Reddit Ads landing URL (utm_source=reddit)
 * @property {string} [redditAdsCampaignName] — label in ads.reddit.com
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
      "https://becertifiedtoday.com/ccna-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=portal-10d",
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
    redditAdsCampaignName: "CCNA_Wedge_Reddit",
    redditFinalUrl:
      "https://becertifiedtoday.com/ccna-home.html?utm_source=reddit&utm_medium=cpc&utm_campaign=ccna_wedge_lab&utm_content=reddit-labs",
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
      "https://becertifiedtoday.com/ccnp-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=encor_portal&utm_content=portal-30d",
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
    label: "Security+ SY0-701 · portal",
    googleAdsCampaignName: "Security+ SY0-701 · Exam prep · becertifiedtoday",
    utmCampaign: "secplus_portal",
    adGroup: "secplus_portal_10d",
    dailyBudgetUsd: 10,
    maxCpcUsd: 2.75,
    landingPath: "/comptia-sec+-home.html",
    landingHash: "#purchase",
    utmContentPrimary: "portal-10d",
    finalUrl:
      "https://becertifiedtoday.com/comptia-sec+-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=portal-10d",
    redditAdsCampaignName: "SEC+ timed sim Reddit",
    redditFinalUrl:
      "https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=reddit&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=reddit-timed-sim",
    primaryConversion: "begin_checkout",
    conversionItemIds: ["secplus_portal_10d", "secplus_portal_30d"],
    primaryOffer: "10-day $9.99 (portal-10d landing) · 30-day $19.99 on organic home",
    setupDoc: "scripts/secplus-portal-10d-google-ads.md",
    setupDocTxt: "scripts/secplus-portal-10d-google-ads.txt",
    sampleTracks: ["questions", "sim-dark-web"],
  },
  {
    id: "secplus_wedge_pbq",
    product: "secplus",
    label: "SEC+_Wedge_PBQ · browser PBQ practice",
    googleAdsCampaignName: "SEC+_Wedge_PBQ",
    utmCampaign: "secplus_wedge_pbq",
    adGroup: "SEC+_Wedge_PBQ",
    dailyBudgetUsd: 8,
    maxCpcUsd: 3.5,
    landingPath: "/secplus/pbq-practice-browser.html",
    landingHash: "",
    utmContentPrimary: "pbq-wedge",
    finalUrl:
      "https://becertifiedtoday.com/secplus/pbq-practice-browser.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=pbq-wedge",
    redditAdsCampaignName: "SEC+_Wedge_Reddit",
    redditFinalUrl:
      "https://becertifiedtoday.com/secplus/pbq-practice-browser.html?utm_source=reddit&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=reddit-pbq",
    primaryConversion: "begin_checkout",
    conversionItemIds: ["secplus_portal_10d", "secplus_portal_30d"],
    primaryOffer: "10-day $9.99 · 30-day $19.99 — wedge PBQ landing",
    setupDoc: "scripts/secplus-wedge-pbq-google-ads-checklist.csv",
    setupDocTxt: "scripts/secplus-wedge-pbq-google-ads-README.txt",
    sampleTracks: ["sim-dark-web", "questions"],
  },
];

export function getCampaignMarketingRegistry() {
  return CAMPAIGN_MARKETING_REGISTRY.map((c) => ({ ...c }));
}

export function utmCampaignNames() {
  return CAMPAIGN_MARKETING_REGISTRY.map((c) => c.utmCampaign);
}
