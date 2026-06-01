/**
 * Find active Security+ portal checkout sessions by email (Stripe Customer metadata + session search).
 */

import {
  checkoutSessionIsPaid,
  inferProductIdFromCheckoutSession,
  isSecplusPortalProduct,
  isSecplusTestSimulationProduct,
  portalAccessExpiresAtMs,
} from "./ccna-portal-stripe.js";

const SESSION_EXPAND = [
  "payment_intent",
  "payment_link",
  "line_items.data.price",
  "line_items.data.price.product",
];

function needsSessionExpand(session) {
  return (
    !session.line_items?.data?.length ||
    !session.payment_link ||
    typeof session.payment_link === "string"
  );
}

/**
 * Scan Stripe for Security+ portal and timed-exam purchases for an email.
 * @param {import('stripe').Stripe} stripe
 * @param {string} email
 */
export async function scanSecplusCheckoutSessionsForEmail(stripe, email) {
  const normalized = String(email || "")
    .trim()
    .toLowerCase();
  if (!normalized) {
    return { bestPortal: null, hadExpiredPortal: false, bestTestSim: null };
  }

  /** @type {{ session: import('stripe').Stripe.Checkout.Session, productId: string, accessExpiresAtMs: number } | null} */
  let bestPortal = null;
  let hadExpiredPortal = false;
  /** @type {{ session: import('stripe').Stripe.Checkout.Session, productId: string, accessExpiresAtMs: number } | null} */
  let bestTestSim = null;

  function considerPortal(session, productId, accessExpiresAtMs) {
    if (accessExpiresAtMs > Date.now()) {
      if (!bestPortal || accessExpiresAtMs > bestPortal.accessExpiresAtMs) {
        bestPortal = { session, productId, accessExpiresAtMs };
      }
    } else {
      hadExpiredPortal = true;
    }
  }

  function considerTestSim(session, productId, accessExpiresAtMs) {
    if (accessExpiresAtMs <= Date.now()) return;
    if (!bestTestSim || accessExpiresAtMs > bestTestSim.accessExpiresAtMs) {
      bestTestSim = { session, productId, accessExpiresAtMs };
    }
  }

  async function evaluateSession(session) {
    if (!checkoutSessionIsPaid(session)) return;
    let full = session;
    if (needsSessionExpand(session)) {
      full = await stripe.checkout.sessions.retrieve(session.id, { expand: SESSION_EXPAND });
    }
    const productId = inferProductIdFromCheckoutSession(full);
    if (isSecplusPortalProduct(productId)) {
      considerPortal(full, productId, portalAccessExpiresAtMs(full, productId));
    } else if (isSecplusTestSimulationProduct(productId)) {
      considerTestSim(full, productId, portalAccessExpiresAtMs(full, productId));
    }
  }

  const customers = await stripe.customers.list({ email: normalized, limit: 10 });
  for (let i = 0; i < customers.data.length; i++) {
    const customer = customers.data[i];
    const m = customer.metadata || {};
    const csId = (m.secplus_portal_last_cs || "").trim();
    const expMs = parseInt(String(m.secplus_portal_access_expires_ms || ""), 10);
    if (csId.indexOf("cs_") === 0 && Number.isFinite(expMs) && expMs > Date.now()) {
      try {
        const session = await stripe.checkout.sessions.retrieve(csId, { expand: SESSION_EXPAND });
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
      limit: 25,
    });
    for (let k = 0; k < searched.data.length; k++) {
      await evaluateSession(searched.data[k]);
    }
  } catch (e) {
    console.warn("[secplus-portal] checkout session search skipped:", e.message);
  }

  return { bestPortal, hadExpiredPortal, bestTestSim };
}

/**
 * @param {import('stripe').Stripe} stripe
 * @param {string} email
 */
export async function findActiveSecplusPortalSessionForEmail(stripe, email) {
  const { bestPortal } = await scanSecplusCheckoutSessionsForEmail(stripe, email);
  return bestPortal;
}

/**
 * @param {import('stripe').Stripe} stripe
 * @param {string} email
 */
export async function getSecplusPurchaseHintsForEmail(stripe, email) {
  const { bestPortal, hadExpiredPortal, bestTestSim } = await scanSecplusCheckoutSessionsForEmail(
    stripe,
    email
  );
  return {
    activePortal: bestPortal,
    portalExpired: !bestPortal && hadExpiredPortal,
    timedExamOnly: !bestPortal && !!bestTestSim,
  };
}
