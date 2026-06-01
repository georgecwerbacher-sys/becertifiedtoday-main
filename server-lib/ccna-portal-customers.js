/**
 * List CCNA portal purchasers from Stripe Customer metadata (written at checkout).
 */

import {
  checkoutSessionIsPaid,
  inferProductIdFromCheckoutSession,
  isCcnaPortalProduct,
  portalAccessExpiresAtMs,
} from "./ccna-portal-stripe.js";
import {
  enrichPortalRowsWithCheckout as enrichPortalRowsShared,
  listCcnaPortalSubscribersFromStripe,
} from "./portal-subscribers-stripe.js";

/**
 * Scan Stripe customers for CCNA portal metadata (no separate DB).
 * @param {import('stripe').Stripe} stripe
 * @param {{ maxScan?: number }} [opts]
 */
export async function listPortalCustomersFromStripe(stripe, opts = {}) {
  return listCcnaPortalSubscribersFromStripe(stripe, opts);
}

/**
 * Re-check checkout session + product for active rows (optional enrichment).
 * @param {import('stripe').Stripe} stripe
 * @param {object[]} rows
 */
export async function enrichPortalRowsWithCheckout(stripe, rows) {
  return enrichPortalRowsShared(stripe, rows, {
    isPortalProduct: isCcnaPortalProduct,
    notProductNote: "not ccna portal access",
  });
}

/**
 * Find the best active CCNA portal checkout for an email (metadata, customer sessions, or Stripe search).
 * @param {import('stripe').Stripe} stripe
 * @param {string} email
 */
export async function findActivePortalSessionForEmail(stripe, email) {
  const normalized = String(email || "")
    .trim()
    .toLowerCase();
  if (!normalized) return null;

  /** @type {{ session: import('stripe').Stripe.Checkout.Session, productId: string, accessExpiresAtMs: number } | null} */
  let best = null;

  function consider(session, productId, accessExpiresAtMs) {
    if (accessExpiresAtMs <= Date.now()) return;
    if (!best || accessExpiresAtMs > best.accessExpiresAtMs) {
      best = { session, productId, accessExpiresAtMs };
    }
  }

  async function evaluateSession(session) {
    if (!checkoutSessionIsPaid(session)) return;
    let full = session;
    if (
      !full.line_items?.data?.length ||
      !full.payment_link ||
      typeof full.payment_link === "string"
    ) {
      full = await stripe.checkout.sessions.retrieve(session.id, {
        expand: [
          "payment_intent",
          "payment_link",
          "line_items.data.price",
          "line_items.data.price.product",
        ],
      });
    }
    const productId = inferProductIdFromCheckoutSession(full);
    if (!isCcnaPortalProduct(productId)) return;
    consider(full, productId, portalAccessExpiresAtMs(full, productId));
  }

  const customers = await stripe.customers.list({ email: normalized, limit: 10 });
  for (let i = 0; i < customers.data.length; i++) {
    const customer = customers.data[i];
    const m = customer.metadata || {};
    const csId = (m.ccna_portal_last_cs || "").trim();
    const expMs = parseInt(String(m.ccna_portal_access_expires_ms || ""), 10);
    if (csId.indexOf("cs_") === 0 && Number.isFinite(expMs) && expMs > Date.now()) {
      try {
        const session = await stripe.checkout.sessions.retrieve(csId, {
          expand: [
            "payment_intent",
            "payment_link",
            "line_items.data.price",
            "line_items.data.price.product",
          ],
        });
        await evaluateSession(session);
      } catch (_) {}
    }

    try {
      const listed = await stripe.checkout.sessions.list({
        customer: customer.id,
        limit: 20,
        status: "complete",
      });
      for (let j = 0; j < listed.data.length; j++) {
        await evaluateSession(listed.data[j]);
      }
    } catch (_) {}
  }

  try {
    const safeEmail = normalized.replace(/\\/g, "\\\\").replace(/'/g, "\\'");
    const searched = await stripe.checkout.sessions.search({
      query: "customer_details.email:'" + safeEmail + "' AND status:'complete'",
      limit: 15,
    });
    for (let k = 0; k < searched.data.length; k++) {
      await evaluateSession(searched.data[k]);
    }
  } catch (e) {
    console.warn("[ccna-portal] checkout session search skipped:", e.message);
  }

  return best;
}
