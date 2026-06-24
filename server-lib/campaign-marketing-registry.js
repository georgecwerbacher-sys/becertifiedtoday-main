/**
 * Google Ads / Reddit Ads / UTM campaign definitions for admin marketing dashboard.
 */

/** @typedef {object} CampaignMarketingDefinition */
/**
 * @property {string} id
 * @property {'google'|'reddit'} channel
 * @property {'ccna'|'encor'|'secplus'} product
 * @property {string} label
 * @property {string} [googleAdsCampaignName]
 * @property {string} [redditAdsCampaignName]
 * @property {string} utmCampaign — matches GA4 sessionCampaignName when tagged
 * @property {string} utmSource
 * @property {string} utmMedium
 * @property {string} adGroup
 * @property {number} dailyBudgetUsd
 * @property {number|null} [maxCpcUsd]
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
 * @property {string} [adsDashboardUrl]
 * @property {boolean} [trackInAdmin] — show on /admin campaign tracker (default false)
 * @property {number} [projectionWindowDays] — budget projection horizon (default 21)
 */

/** @type {CampaignMarketingDefinition[]} */
export const CAMPAIGN_MARKETING_REGISTRY = [
  {
    id: "ccna_portal",
    channel: "google",
    product: "ccna",
    label: "CCNA 200-301 · portal · 7-day test",
    googleAdsCampaignName: "CCNA 200-301 · Exam prep · becertifiedtoday",
    utmCampaign: "ccna_portal",
    utmSource: "google",
    utmMedium: "cpc",
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
    channel: "google",
    product: "ccna",
    label: "CCNA_Wedge_Lab · browser CLI labs",
    googleAdsCampaignName: "CCNA_Wedge_Lab",
    utmCampaign: "ccna_wedge_lab",
    utmSource: "google",
    utmMedium: "cpc",
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
    id: "ccna_wedge_reddit",
    channel: "reddit",
    product: "ccna",
    label: "CCNA_Wedge_Reddit · labs",
    redditAdsCampaignName: "CCNA_Wedge_Reddit",
    utmCampaign: "ccna_wedge_lab",
    utmSource: "reddit",
    utmMedium: "cpc",
    adGroup: "r/CCNA · r/Cisco",
    dailyBudgetUsd: 10,
    maxCpcUsd: null,
    landingPath: "/ccna-home.html",
    landingHash: "",
    utmContentPrimary: "reddit-labs",
    finalUrl:
      "https://becertifiedtoday.com/ccna-home.html?utm_source=reddit&utm_medium=cpc&utm_campaign=ccna_wedge_lab&utm_content=reddit-labs",
    primaryConversion: "begin_checkout",
    conversionItemIds: ["ccna_portal_10d", "ccna_portal_30d"],
    primaryOffer: "10-day $9.99 — Reddit image ad · Feed + Conversation",
    setupDoc: "marketing-research/Reddit/marketing/CCNA campaign — Reddit only.md",
    setupDocTxt: "marketing-research/Reddit/marketing/Ad setup checklist.md",
    sampleTracks: ["ccna-vlan", "ccna-questions", "ccna-dnd"],
    adsDashboardUrl: "https://ads.reddit.com",
  },
  {
    id: "encor_portal",
    channel: "google",
    product: "encor",
    label: "CCNP ENCOR 350-401 · portal · 7-day test",
    googleAdsCampaignName: "CCNP ENCOR 350-401 · Exam prep · becertifiedtoday",
    utmCampaign: "encor_portal",
    utmSource: "google",
    utmMedium: "cpc",
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
    channel: "google",
    product: "secplus",
    label: "Security+ SY0-701 · Exam prep · becertifiedtoday",
    googleAdsCampaignName: "Security+ SY0-701 · Exam prep · becertifiedtoday",
    utmCampaign: "secplus_portal",
    utmSource: "google",
    utmMedium: "cpc",
    adGroup: "Security+ PBQ Practice",
    dailyBudgetUsd: 15,
    maxCpcUsd: 2.75,
    landingPath: "/comptia-sec+-home.html",
    landingHash: "",
    utmContentPrimary: "pbq-wedge",
    finalUrl:
      "https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=google&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=pbq-wedge",
    primaryConversion: "begin_checkout",
    conversionItemIds: ["secplus_portal_30d"],
    primaryOffer: "30-day $19.99 — Security+ home · $15/day · Google Ads 30-day only",
    setupDoc: "marketing-research/Sec+ Campaign/secplus-campaign-checklist.csv",
    setupDocTxt: "marketing-research/Sec+ Campaign/secplus-campaign-checklist-README.txt",
    sampleTracks: ["sim-dark-web", "questions"],
    adsDashboardUrl:
      "https://ads.google.com/aw/overview?ocid=8235244277&euid=277397985&__u=6466314265&uscid=8235244277&__c=3900876173&authuser=0&workspaceId=0&subid=us-en-awhp-g-aw-c-home-signin-bgc!o2-aluminum%7Cib:2387565277%7Cib:8016481541%7Cib:6079319977%7C-ahpm-0000000209-0000000001%7C-ahpm-0000000179-0000000001",
    trackInAdmin: true,
    projectionWindowDays: 21,
  },
  {
    id: "secplus_wedge_pbq_reddit",
    channel: "reddit",
    product: "secplus",
    label: "SEC+_Wedge_Reddit · PBQ Reddit",
    redditAdsCampaignName: "SEC+_Wedge_Reddit",
    utmCampaign: "secplus_wedge_pbq",
    utmSource: "reddit",
    utmMedium: "cpc",
    adGroup: "r/CompTIA · r/SecurityPlus · PBQ",
    dailyBudgetUsd: 20,
    maxCpcUsd: 4.0,
    landingPath: "/comptia-sec+-home.html",
    landingHash: "",
    utmContentPrimary: "reddit-pbq",
    finalUrl:
      "https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=reddit&utm_medium=cpc&utm_campaign=secplus_wedge_pbq&utm_content=reddit-pbq",
    primaryConversion: "begin_checkout",
    conversionItemIds: ["secplus_portal_30d"],
    primaryOffer: "10-day $9.99 · 30-day $19.99 — Reddit PBQ · comptia-sec+-home",
    setupDoc: "marketing-research/Sec+ Campaign/secplus-reddit-checklist.csv",
    setupDocTxt: "marketing-research/Sec+ Campaign/secplus-reddit-checklist-README.txt",
    sampleTracks: ["sim-dark-web", "questions"],
    adsDashboardUrl: "https://ads.reddit.com",
  },
  {
    id: "secplus_portal_reddit_timed",
    channel: "reddit",
    product: "secplus",
    label: "SEC+_Wedge_Reddit · timed sim (phase 2)",
    redditAdsCampaignName: "SEC+_Wedge_Reddit",
    utmCampaign: "secplus_portal",
    utmSource: "reddit",
    utmMedium: "cpc",
    adGroup: "r/CompTIA · r/SecurityPlus",
    dailyBudgetUsd: 10,
    maxCpcUsd: null,
    landingPath: "/comptia-sec+-home.html",
    landingHash: "",
    utmContentPrimary: "reddit-timed-sim",
    finalUrl:
      "https://becertifiedtoday.com/comptia-sec+-home.html?utm_source=reddit&utm_medium=cpc&utm_campaign=secplus_portal&utm_content=reddit-timed-sim",
    primaryConversion: "begin_checkout",
    conversionItemIds: ["secplus_portal_30d"],
    primaryOffer: "Work-cert angle · 90-min timed sim — A/B after PBQ ad set",
    setupDoc: "marketing-research/Sec+ Campaign/Sec+ Reddit Copy.md",
    setupDocTxt: "marketing-research/Sec+ Campaign/Sec+ Reddit Notes.md",
    sampleTracks: ["sim-dark-web", "questions"],
    adsDashboardUrl: "https://ads.reddit.com",
  },
];

export function getCampaignMarketingRegistry() {
  return CAMPAIGN_MARKETING_REGISTRY.map((c) => ({ ...c }));
}

/** Campaigns shown on /admin (trackInAdmin: true). */
export function getAdminTrackedCampaignRegistry() {
  return CAMPAIGN_MARKETING_REGISTRY.filter((c) => c.trackInAdmin === true).map((c) => ({
    ...c,
  }));
}

/** Ad landing paths monitored on /admin (exact GA4 pagePath). */
export const AD_LANDING_MONITOR_PATHS = [
  "/ccna-home.html",
  "/ccnp-home.html",
  "/comptia-sec+-home.html",
  "/ccna/labs-without-gns3.html",
];

export function utmCampaignNames() {
  return [...new Set(CAMPAIGN_MARKETING_REGISTRY.map((c) => c.utmCampaign))];
}
