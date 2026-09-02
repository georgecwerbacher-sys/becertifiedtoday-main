/**
 * Rule-based conversion recommendations from admin site-traffic metrics.
 */

/** @typedef {{ id: string, priority: 'high'|'medium'|'low'|'win', category: string, title: string, detail: string, action: string }} CampaignRecommendation */

function pctLabel(rate) {
  if (rate == null || !Number.isFinite(Number(rate))) return "—";
  return (Number(rate) * 100).toFixed(1) + "%";
}

function push(recs, item) {
  if (!item || !item.title) return;
  recs.push(item);
}

/**
 * @param {object} report — buildSiteTrafficReport() result (partial ok)
 * @returns {CampaignRecommendation[]}
 */
export function buildCampaignConversionRecommendations(report) {
  const recs = /** @type {CampaignRecommendation[]} */ ([]);
  if (!report) return recs;

  const primary = report.primaryLanding || {};
  const campaigns = report.campaigns || [];
  const adGroups = (report.secplusAdGroups || []).filter((g) => !g.isOther);
  const activeAdGroups = adGroups.filter((g) => Number(g.sessions) > 0);
  const siteCheckout = report.siteCheckout || {};
  const rangeLabel = report.rangeLabel || "this range";
  const channels = report.channelTotals || {};

  const paidCampaigns = campaigns.filter((c) => Number(c.sessions) > 0);
  const secplusPaid = paidCampaigns.filter((c) => c.product === "secplus");
  const topPaid = [...paidCampaigns].sort((a, b) => b.sessions - a.sessions)[0];
  const bestCheckoutCampaign = [...paidCampaigns]
    .filter((c) => Number(c.beginCheckout) > 0)
    .sort((a, b) => (b.checkoutRate || 0) - (a.checkoutRate || 0))[0];

  const googleSessions = Number(channels.googleCpc?.sessions || 0);
  const googleCheckout = Number(channels.googleCpc?.beginCheckout || 0);
  const redditSessions = Number(channels.redditCpc?.sessions || 0);
  const redditCheckout = Number(channels.redditCpc?.beginCheckout || 0);

  const landingViews = Number(primary.screenPageViews || 0);
  const landingCheckout = Number(primary.beginCheckout || 0);
  const landingCheckoutRate = primary.checkoutRate;
  const engaged = Number(primary.engagedSessions || 0);
  const landingSessions = Number(primary.landingSessions || 0);
  const engagementRate = landingSessions > 0 ? engaged / landingSessions : null;
  const popupShown = Number(primary.offerPopupShown || 0);
  const popupClick = Number(primary.offerPopupClick || 0);
  const freeSim = Number(primary.freeSimStarts || 0);
  const avgOnPage = Number(primary.avgSecondsOnPage || 0);

  // —— Measurement / volume ——
  if (landingViews < 30 && paidCampaigns.every((c) => Number(c.sessions) < 15)) {
    push(recs, {
      id: "low-volume",
      priority: "low",
      category: "measurement",
      title: "Low traffic — wait before big changes",
      detail: `Only ${landingViews} Security+ home views in ${rangeLabel}. Conversion rates swing wildly below ~50 paid sessions.`,
      action:
        "Keep ads running at current budget until you have more data, or widen the date range to 28d before judging creative.",
    });
  }

  // —— Primary landing funnel ——
  if (landingViews >= 40 && landingCheckout === 0) {
    push(recs, {
      id: "zero-checkout-landing",
      priority: "high",
      category: "landing",
      title: "Traffic but zero checkout clicks on Security+ home",
      detail: `${landingViews} page views on ${primary.path || "/comptia-sec+-home.html"} with no begin_checkout.`,
      action:
        "Put one purchase CTA above the fold (30-day $29.99). Test PBQ sample → scroll to #purchase. Confirm GA4 Realtime fires begin_checkout on click.",
    });
  } else if (landingViews >= 50 && landingCheckoutRate != null && landingCheckoutRate < 0.02) {
    push(recs, {
      id: "weak-landing-cvr",
      priority: "high",
      category: "landing",
      title: "Landing checkout rate is below 2%",
      detail: `${landingCheckout} checkouts / ${landingViews} views (${pctLabel(landingCheckoutRate)}) on Security+ home.`,
      action:
        "Tighten hero to one offer. Add social proof near CTA. Compare utm_content in admin (core-exam-prep vs mil-gov-8140 vs student-workforce). Log the change in Daily campaign log before refreshing.",
    });
  }

  if (avgOnPage > 0 && avgOnPage < 25 && landingViews >= 30) {
    push(recs, {
      id: "bounce-quick",
      priority: "medium",
      category: "landing",
      title: "Short time on page — message or speed mismatch",
      detail: `Average ${Math.round(avgOnPage)}s on Security+ home.`,
      action:
        "Match ad promise in first screen (PBQ practice, browser sim). Slow mobile? Test on phone. Consider leading with free sample hook before price.",
    });
  }

  if (engagementRate != null && landingSessions >= 20 && engagementRate < 0.45) {
    push(recs, {
      id: "low-engagement",
      priority: "medium",
      category: "ads",
      title: "Many sessions are not engaged",
      detail: `${pctLabel(engagementRate)} engaged sessions on Security+ landing (${engaged}/${landingSessions}).`,
      action:
        "Review search terms / Reddit placements for intent. Add negatives for job-seekers and brain-dump terms. Align headline with landing H1.",
    });
  }

  // —— Popup & free sim funnel ——
  if (popupShown >= 10 && popupClick === 0) {
    push(recs, {
      id: "popup-no-clicks",
      priority: "medium",
      category: "offer",
      title: "Offer popup shown but never clicked",
      detail: `${popupShown} popup impressions, 0 clicks.`,
      action: "Test shorter copy, stronger discount framing, or delay until after sample interaction. Dismiss rate may signal annoyance — try once per session only.",
    });
  }

  if (freeSim >= 5 && landingCheckout < Math.max(2, Math.floor(freeSim * 0.15))) {
    push(recs, {
      id: "sim-not-converting",
      priority: "high",
      category: "funnel",
      title: "Free sim starts without enough checkouts",
      detail: `${freeSim} secplus_free_sim_start vs ${landingCheckout} begin_checkout.`,
      action:
        "After sim completion, surface a single CTA (Continue studying — 30 days $29.99). Email capture if they abandon. Retarget sim starters in ads if volume allows.",
    });
  }

  // —— Paid channels ——
  if (googleSessions >= 10 && googleCheckout === 0) {
    push(recs, {
      id: "google-no-checkout",
      priority: "high",
      category: "ads",
      title: "Google Ads traffic not generating checkouts",
      detail: `${googleSessions} Google CPC sessions, 0 begin_checkout in ${rangeLabel}.`,
      action:
        "Verify Final URL is /comptia-sec+-home.html with utm_campaign=secplus_portal. Check Search terms report for irrelevant queries. Keep Manual CPC until 15–20 checkouts, then test Maximize conversions.",
    });
  }

  if (redditSessions >= 10 && redditCheckout === 0) {
    push(recs, {
      id: "reddit-no-checkout",
      priority: "high",
      category: "ads",
      title: "Reddit Ads traffic not generating checkouts",
      detail: `${redditSessions} Reddit CPC sessions, 0 begin_checkout.`,
      action:
        "Use PBQ creative that matches landing sample. Test r/CompTIA vs r/SecurityPlus. Lower daily cap until checkout rate proves out.",
    });
  }

  if (googleCheckout > 0 && redditSessions >= 15 && redditCheckout === 0 && googleSessions >= 15) {
    push(recs, {
      id: "shift-budget-google",
      priority: "medium",
      category: "ads",
      title: "Google is outperforming Reddit on checkout",
      detail: `Google: ${googleCheckout} checkouts · Reddit: 0 with ${redditSessions} sessions.`,
      action: "Pause or reduce Reddit spend temporarily; reallocate daily budget to secplus_portal Google campaign.",
    });
  }

  // —— Security+ Google ad groups (utm_content) ——
  for (const g of adGroups) {
    if (g.isLegacy || g.isOther) continue;
    if (Number(g.sessions) >= 12 && Number(g.beginCheckout) === 0) {
      push(recs, {
        id: `adgroup-zero-${g.slug}`,
        priority: "high",
        category: "ads",
        title: `${g.adGroupName}: traffic without checkout`,
        detail: `${g.sessions} Google CPC sessions on utm_content=${g.utmContent}, 0 begin_checkout in ${rangeLabel}.`,
        action: `Google Ads → ${g.adGroupName}: confirm Final URL uses utm_content=${g.utmContent}. Review RSA pin "${g.pinH1}" vs search terms. Update copy in Obsidian Sec+ RSA Copy, then log in Daily campaign log.`,
      });
    }
    if (
      Number(g.sessions) >= 15 &&
      g.checkoutRate != null &&
      g.checkoutRate >= 0.05 &&
      Number(g.beginCheckout) >= 2
    ) {
      push(recs, {
        id: `adgroup-scale-${g.slug}`,
        priority: "win",
        category: "ads",
        title: `${g.adGroupName}: strong checkout — protect spend`,
        detail: `${g.beginCheckout} checkouts / ${g.sessions} sessions (${pctLabel(g.checkoutRate)}) on ${g.utmContent}.`,
        action:
          "Let Google allocate more of the $25/day shared budget to this ad group. Do not change RSA pins for 7 days. Note win in Daily campaign log.",
      });
    }
  }

  const adGroupWithCheckout = [...activeAdGroups]
    .filter((g) => Number(g.beginCheckout) > 0 && !g.isLegacy)
    .sort((a, b) => (b.checkoutRate || 0) - (a.checkoutRate || 0));
  const topAdGroupVolume = [...activeAdGroups]
    .filter((g) => !g.isLegacy)
    .sort((a, b) => b.sessions - a.sessions)[0];
  const bestAdGroupCvr = adGroupWithCheckout[0];
  if (
    topAdGroupVolume &&
    bestAdGroupCvr &&
    topAdGroupVolume.utmContent !== bestAdGroupCvr.utmContent &&
    Number(topAdGroupVolume.sessions) >= 15 &&
    Number(bestAdGroupCvr.sessions) >= 10
  ) {
    push(recs, {
      id: "adgroup-volume-not-best-cvr",
      priority: "medium",
      category: "ads",
      title: "Security+ ad group spend may be misallocated",
      detail: `${topAdGroupVolume.adGroupName} has the most sessions (${topAdGroupVolume.sessions}); ${bestAdGroupCvr.adGroupName} converts better (${pctLabel(bestAdGroupCvr.checkoutRate)} checkout rate).`,
      action: `In Google Ads, tighten keywords/negatives in ${topAdGroupVolume.adGroupName} or pause weak RSAs. Favor ${bestAdGroupCvr.adGroupName} creative angle — do not split campaigns yet (see One-Campaign Ad Group Plan week-1 rule).`,
    });
  }

  if (activeAdGroups.some((g) => g.isLegacy && Number(g.sessions) >= 5)) {
    push(recs, {
      id: "legacy-utm-content",
      priority: "medium",
      category: "ads",
      title: "Legacy utm_content still receiving traffic",
      detail: "GA4 shows sessions on old utm_content (e.g. pbq-wedge) alongside the three-ad-group build.",
      action:
        "Google Ads → replace Final URLs with core-exam-prep, mil-gov-8140, or student-workforce. Pause legacy ad groups after URLs are updated.",
    });
  }

  // —— Per-campaign ——
  for (const c of secplusPaid) {
    if (Number(c.sessions) >= 15 && Number(c.beginCheckout) === 0) {
      push(recs, {
        id: `campaign-zero-${c.id}`,
        priority: "high",
        category: "ads",
        title: `${c.label || c.id}: sessions without checkout`,
        detail: `${c.sessions} sessions (${c.channel}), 0 begin_checkout. Landing: ${c.landingPath}.`,
        action: `Open ${c.channel === "reddit" ? "Reddit" : "Google"} Ads → compare ad copy to ${c.utmCampaign} landing. Pause weakest ad set until CTR and checkout improve.`,
      });
    }
    if (
      Number(c.sessions) >= 20 &&
      c.checkoutRate != null &&
      c.checkoutRate >= 0.05 &&
      Number(c.beginCheckout) >= 2
    ) {
      push(recs, {
        id: `campaign-scale-${c.id}`,
        priority: "win",
        category: "ads",
        title: `${c.label}: strong checkout rate — consider scaling`,
        detail: `${c.beginCheckout} checkouts / ${c.sessions} sessions (${pctLabel(c.checkoutRate)}).`,
        action:
          "Raise daily budget 10–20% if CPA in Ads is acceptable. Duplicate winning ad/keyword into a second ad group with new utm_content for clean GA4 comparison.",
      });
    }
  }

  if (topPaid && Number(topPaid.beginCheckout) > 0 && bestCheckoutCampaign && bestCheckoutCampaign.id !== topPaid.id) {
    push(recs, {
      id: "top-volume-not-best-cvr",
      priority: "medium",
      category: "ads",
      title: "Highest traffic campaign is not your best converter",
      detail: `${topPaid.label} has most sessions; ${bestCheckoutCampaign.label} has better checkout rate (${pctLabel(bestCheckoutCampaign.checkoutRate)}).`,
      action: `Shift budget toward ${bestCheckoutCampaign.utmCampaign}. Clone winning landing angle from ${bestCheckoutCampaign.primaryOffer || "that campaign"}.`,
    });
  }

  // —— Site-wide checkout vs Stripe (GA only here) ——
  if (Number(siteCheckout.checkoutClicks || 0) >= 5 && landingCheckout >= 3) {
    push(recs, {
      id: "compare-stripe",
      priority: "low",
      category: "funnel",
      title: "Compare GA checkouts to Stripe purchases",
      detail: `${siteCheckout.checkoutClicks} site-wide begin_checkout in range.`,
      action:
        "In Stripe checkout section above, check purchase count. Large gap = payment-page drop-off — test Payment Link on mobile, confirm success URL, simplify to one SKU in ads.",
    });
  }

  // —— Default tactical reminders when healthy ——
  if (recs.length === 0 || recs.every((r) => r.priority === "low" || r.priority === "win")) {
    push(recs, {
      id: "maintain-secplus",
      priority: "low",
      category: "funnel",
      title: "Maintain Security+ conversion loop",
      detail: `Security+ home: ${landingCheckout} checkouts / ${landingViews} views in ${rangeLabel}.`,
      action:
        "Weekly: compare the three utm_content rows in /admin, one RSA tweak per ad group max, log spend/copy in Daily campaign log, then refresh Recommendations.",
    });
  }

  const order = { high: 0, medium: 1, low: 2, win: 3 };
  recs.sort((a, b) => (order[a.priority] ?? 9) - (order[b.priority] ?? 9));

  return recs.slice(0, 12);
}
