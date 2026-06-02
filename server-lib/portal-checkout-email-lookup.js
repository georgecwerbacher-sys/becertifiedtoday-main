/**
 * Discover Stripe Checkout Sessions for an email (search + charge fallback).
 * Used by portal magic-link restore when Customer metadata was never written (e.g. webhook missed).
 */

const SESSION_EXPAND = [
  "payment_intent",
  "payment_link",
  "line_items.data.price",
  "line_items.data.price.product",
];

function escapeStripeSearchValue(value) {
  return String(value || "")
    .trim()
    .toLowerCase()
    .replace(/\\/g, "\\\\")
    .replace(/'/g, "\\'");
}

/**
 * @param {import('stripe').Stripe} stripe
 * @param {string} query
 * @param {Set<string>} seen
 * @param {import('stripe').Stripe.Checkout.Session[]} out
 * @param {number} max
 */
async function searchCheckoutQuery(stripe, query, seen, out, max) {
  let page = await stripe.checkout.sessions.search({
    query,
    limit: Math.min(25, max),
  });
  while (page.data.length) {
    for (let i = 0; i < page.data.length; i++) {
      const session = page.data[i];
      if (!session?.id || seen.has(session.id)) continue;
      seen.add(session.id);
      out.push(session);
      if (out.length >= max) return;
    }
    if (!page.has_more || out.length >= max) return;
    page = await stripe.checkout.sessions.search({
      query,
      limit: Math.min(25, max - out.length),
      page: page.next_page,
    });
  }
}

/**
 * @param {import('stripe').Stripe} stripe
 * @param {string} email
 * @param {{ max?: number }} [opts]
 * @returns {Promise<import('stripe').Stripe.Checkout.Session[]>}
 */
export async function discoverCheckoutSessionsForEmail(stripe, email, opts = {}) {
  const normalized = String(email || "")
    .trim()
    .toLowerCase();
  if (!normalized) return [];

  const max = Math.min(Math.max(Number(opts.max) || 40, 1), 100);
  const safe = escapeStripeSearchValue(normalized);
  /** @type {Set<string>} */
  const seen = new Set();
  /** @type {import('stripe').Stripe.Checkout.Session[]} */
  const out = [];

  const queries = [
    "customer_details.email:'" + safe + "' AND status:'complete'",
    "customer_email:'" + safe + "' AND status:'complete'",
  ];

  for (let q = 0; q < queries.length; q++) {
    try {
      await searchCheckoutQuery(stripe, queries[q], seen, out, max);
    } catch (e) {
      console.warn("[portal] checkout session search skipped:", e.message);
    }
    if (out.length >= max) break;
  }

  if (out.length < max) {
    try {
      const charges = await stripe.charges.search({
        query: "receipt_email:'" + safe + "' AND status:'succeeded'",
        limit: 20,
      });
      for (let i = 0; i < charges.data.length && out.length < max; i++) {
        const charge = charges.data[i];
        const pi =
          typeof charge.payment_intent === "string"
            ? charge.payment_intent
            : charge.payment_intent?.id;
        if (!pi || pi.indexOf("pi_") !== 0) continue;
        try {
          await searchCheckoutQuery(
            stripe,
            "payment_intent:'" + pi.replace(/'/g, "\\'") + "'",
            seen,
            out,
            max
          );
        } catch (e) {
          console.warn("[portal] checkout session search by payment_intent skipped:", e.message);
        }
      }
    } catch (e) {
      console.warn("[portal] charge search fallback skipped:", e.message);
    }
  }

  return out;
}

export { SESSION_EXPAND };
