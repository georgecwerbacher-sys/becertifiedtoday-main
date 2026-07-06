/**
 * Paid Stripe checkout sessions in an admin date range (portal + timed sim).
 */
import {
  checkoutSessionIsPaid,
  inferProductIdFromCheckoutSession,
  isSecplusPortalProduct,
  isSecplusTestSimulationProduct,
} from "./ccna-portal-stripe.js";
import { rangePresetLabel, utcStartFromPreset } from "./google-analytics.js";

function productTrackFromId(productId) {
  const id = String(productId || "").toLowerCase();
  if (id.startsWith("ccna")) return "ccna";
  if (id.startsWith("encor")) return "encor";
  if (id.startsWith("secplus")) return "secplus";
  return "other";
}

function sessionEmail(session) {
  const details = session.customer_details || {};
  const email = (details.email || session.customer_email || "").trim().toLowerCase();
  return email || "";
}

/**
 * @param {import('stripe').Stripe} stripe
 * @param {string} rangePreset
 */
export async function buildStripePurchasesReport(stripe, rangePreset = "7d") {
  const preset = typeof rangePreset === "string" ? rangePreset.trim() : "7d";
  const createdGte = Math.floor(new Date(utcStartFromPreset(preset)).getTime() / 1000);
  const createdLte = Math.floor(Date.now() / 1000);

  const purchases = [];
  let startingAfter;
  let pages = 0;
  const maxPages = 15;

  while (pages < maxPages) {
    pages += 1;
    const page = await stripe.checkout.sessions.list({
      created: { gte: createdGte, lte: createdLte },
      limit: 100,
      ...(startingAfter ? { starting_after: startingAfter } : {}),
    });

      for (const session of page.data || []) {
      if (!checkoutSessionIsPaid(session)) continue;
      const productId = inferProductIdFromCheckoutSession(session);
      if (
        !productId ||
        (!isSecplusPortalProduct(productId) && !isSecplusTestSimulationProduct(productId))
      ) {
        continue;
      }
      purchases.push({
        checkoutSessionId: session.id,
        email: sessionEmail(session) || "(no email)",
        productId,
        track: productTrackFromId(productId),
        purchasedAt:
          typeof session.created === "number"
            ? new Date(session.created * 1000).toISOString()
            : null,
        amountTotal: typeof session.amount_total === "number" ? session.amount_total : null,
        currency: session.currency || "usd",
      });
    }

    if (!page.has_more || !page.data.length) break;
    startingAfter = page.data[page.data.length - 1].id;
  }

  const byTrack = { secplus: 0, other: 0 };
  const emails = new Set();
  for (const row of purchases) {
    if (row.email && row.email !== "(no email)") emails.add(row.email);
    const track = row.track in byTrack ? row.track : "other";
    byTrack[track] += 1;
  }

  purchases.sort((a, b) => String(b.purchasedAt || "").localeCompare(String(a.purchasedAt || "")));

  return {
    rangeLabel: rangePresetLabel(preset),
    totalPurchases: purchases.length,
    uniqueCustomers: emails.size,
    newRegister: emails.size,
    byProduct: {
      secplus: byTrack.secplus,
    },
    recentPurchases: purchases.slice(0, 50),
    truncated: pages >= maxPages,
    note:
      "Paid Security+ Stripe checkouts in the selected date range (UTC). New Register = distinct checkout emails in the range. " +
      "Unlike GA4 new visitors, this counts real purchases — same person on a new browser still counts once if same email. " +
      "Repeat purchases by the same email in the range count once for New Register.",
  };
}
