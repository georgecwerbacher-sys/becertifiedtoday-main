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
    label: "CCNA 200-301 · portal",
    googleAdsCampaignName: "CCNA 200-301 · Exam prep · becertifiedtoday",
    utmCampaign: "ccna_portal",
    adGroup: "ccna_portal_10d",
    dailyBudgetUsd: 10,
    maxCpcUsd: 2.75,
    landingPath: "/ccna-home.html",
    landingHash: "#purchase",
    utmContentPrimary: "portal-10d",
    finalUrl:
      "https://becertifiedtoday.com/ccna-home.html#purchase?utm_source=google&utm_medium=cpc&utm_campaign=ccna_portal&utm_content=portal-10d",
    primaryConversion: "begin_checkout",
    conversionItemIds: ["ccna_portal_10d", "ccna_portal_30d"],
    primaryOffer: "10-day $9.99 (portal-10d landing shows 10d only)",
    setupDoc: "scripts/ccna-portal-10d-google-ads.md",
    setupDocTxt: "scripts/ccna-portal-10d-google-ads.md",
    sampleTracks: ["ccna-questions", "ccna-dnd", "ccna-vlan"],
  },
  {
    id: "encor_portal",
    product: "encor",
    label: "CCNP ENCOR 350-401 · portal",
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
    primaryOffer: "30-day $19.99 primary · $9.99/10d one-time popup only",
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
    primaryConversion: "begin_checkout",
    conversionItemIds: ["secplus_portal_10d", "secplus_portal_30d"],
    primaryOffer: "10-day $9.99 (portal-10d landing) · 30-day $19.99 on organic home",
    setupDoc: "scripts/secplus-portal-10d-google-ads.md",
    setupDocTxt: "scripts/secplus-portal-10d-google-ads.txt",
    sampleTracks: ["questions", "sim-dark-web"],
  },
];

export function getCampaignMarketingRegistry() {
  return CAMPAIGN_MARKETING_REGISTRY.map((c) => ({ ...c }));
}

export function utmCampaignNames() {
  return CAMPAIGN_MARKETING_REGISTRY.map((c) => c.utmCampaign);
}
