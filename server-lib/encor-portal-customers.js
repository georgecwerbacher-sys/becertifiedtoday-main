/**
 * Find active ENCOR portal checkout sessions by email (Stripe Customer metadata + session search).
 */

import {
  checkoutSessionIsPaid,
  inferProductIdFromCheckoutSession,
  isEncorPortalProduct,
  portalAccessExpiresAtMs,
} from "./ccna-portal-stripe.js";

/**
 * @param {import('stripe').Stripe} stripe
 * @param {string} email
 */
export async function findActiveEncorPortalSessionForEmail(stripe, email) {
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
    if (!full.line_items?.data?.length) {
      full = await stripe.checkout.sessions.retrieve(session.id, {
        expand: ["payment_intent", "line_items.data.price"],
      });
    }
    const productId = inferProductIdFromCheckoutSession(full);
    if (!isEncorPortalProduct(productId)) return;
    consider(full, productId, portalAccessExpiresAtMs(full, productId));
  }

  const customers = await stripe.customers.list({ email: normalized, limit: 10 });
  for (let i = 0; i < customers.data.length; i++) {
    const customer = customers.data[i];
    const m = customer.metadata || {};
    const csId = (m.encor_portal_last_cs || "").trim();
    const expMs = parseInt(String(m.encor_portal_access_expires_ms || ""), 10);
    if (csId.indexOf("cs_") === 0 && Number.isFinite(expMs) && expMs > Date.now()) {
      try {
        const session = await stripe.checkout.sessions.retrieve(csId, {
          expand: ["payment_intent", "line_items.data.price"],
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
    console.warn("[encor-portal] checkout session search skipped:", e.message);
  }

  return best;
}
