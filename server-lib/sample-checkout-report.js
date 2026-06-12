/**
 * GA4 begin_checkout metrics for /admin (Stripe payment page intent).
 */
import {
  fetchBeginCheckoutByItemId,
  fetchBeginCheckoutByItemPrefix,
  fetchBeginCheckoutSummary,
} from "./google-analytics.js";

const PRODUCT_LABELS = {
  ccna: "CCNA (200-301)",
  encor: "CCNP ENCOR (350-401)",
  secplus: "CompTIA Security+ (SY0-701)",
  other: "Other",
};

const ITEM_LABELS = {
  ccna_portal_10d: "CCNA 10-day portal",
  ccna_portal_30d: "CCNA 30-day portal",
  ccna_timed_simulation: "CCNA timed simulation",
  encor_portal_10d: "ENCOR 10-day portal",
  encor_portal_30d: "ENCOR 30-day portal",
  encor_timed_simulation: "ENCOR timed simulation",
  secplus_portal_10d: "Security+ 10-day portal",
  secplus_portal_30d: "Security+ 30-day portal",
};

function productKeyFromItemId(itemId) {
  const id = String(itemId || "").toLowerCase();
  if (id.startsWith("ccna")) return "ccna";
  if (id.startsWith("encor")) return "encor";
  if (id.startsWith("secplus")) return "secplus";
  return "other";
}

async function fetchByProduct(client, propertyId, range) {
  const keys = ["ccna", "encor", "secplus"];
  const rows = await Promise.all(
    keys.map(async (key) => {
      const metrics = await fetchBeginCheckoutByItemPrefix(client, propertyId, range, key);
      return {
        product: key,
        label: PRODUCT_LABELS[key] || key,
        checkoutClicks: metrics.checkoutClicks,
        uniqueUsers: metrics.uniqueUsers,
      };
    })
  );
  return rows.filter((r) => r.checkoutClicks > 0 || r.uniqueUsers > 0);
}

/**
 * @param {import('@google-analytics/data').BetaAnalyticsDataClient} client
 * @param {string} propertyId
 * @param {{ startDate: string, endDate: string }} range
 */
export async function buildSampleCheckoutReport(client, propertyId, range) {
  const [summary, byItemRaw, byProduct] = await Promise.all([
    fetchBeginCheckoutSummary(client, propertyId, range),
    fetchBeginCheckoutByItemId(client, propertyId, range, 30),
    fetchByProduct(client, propertyId, range),
  ]);

  const byItem = (byItemRaw || []).map((row) => ({
    itemId: row.itemId,
    label: ITEM_LABELS[row.itemId] || row.itemId,
    product: productKeyFromItemId(row.itemId),
    checkoutClicks: row.checkoutClicks,
    uniqueUsers: row.uniqueUsers,
  }));

  return {
    summary: {
      checkoutClicks: Number(summary.checkoutClicks || 0),
      uniqueUsers: Number(summary.uniqueUsers || 0),
    },
    byProduct,
    byItem,
    note:
      "GA4 begin_checkout fires when a visitor clicks a Stripe checkout button (portal or timed simulation). " +
      "Unique users reached the payment step; completed purchases appear under Portal subscribers after Stripe webhook.",
  };
}
