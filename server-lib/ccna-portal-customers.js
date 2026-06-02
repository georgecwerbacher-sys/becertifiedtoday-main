/**
 * List CCNA portal purchasers from Stripe Customer metadata (written at checkout).
 */

import {
  checkoutSessionIsPaid,
  inferProductIdFromCheckoutSession,
  isCcnaPortalProduct,
  isCcnaTestSimulationProduct,
  portalAccessExpiresAtMs,
} from "./ccna-portal-stripe.js";
import {
  enrichPortalRowsWithCheckout as enrichPortalRowsShared,
  listCcnaPortalSubscribersFromStripe,
} from "./portal-subscribers-stripe.js";
import {
  discoverCheckoutSessionsForEmail,
  SESSION_EXPAND,
} from "./portal-checkout-email-lookup.js";

const SESSION_EXPAND_LOCAL = SESSION_EXPAND;

function needsSessionExpand(session) {
  return (
    !session.line_items?.data?.length ||
    !session.payment_link ||
    typeof session.payment_link === "string"
  );
}

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
 * Scan Stripe for CCNA portal and timed-exam purchases for an email.
 * @param {import('stripe').Stripe} stripe
 * @param {string} email
 */
export async function scanCcnaCheckoutSessionsForEmail(stripe, email) {
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
      full = await stripe.checkout.sessions.retrieve(session.id, { expand: SESSION_EXPAND_LOCAL });
    }
    const productId = inferProductIdFromCheckoutSession(full);
    if (isCcnaPortalProduct(productId)) {
      considerPortal(full, productId, portalAccessExpiresAtMs(full, productId));
    } else if (isCcnaTestSimulationProduct(productId)) {
      considerTestSim(full, productId, portalAccessExpiresAtMs(full, productId));
    }
  }

  const customers = await stripe.customers.list({ email: normalized, limit: 10 });
  for (let i = 0; i < customers.data.length; i++) {
    const customer = customers.data[i];
    const m = customer.metadata || {};
    const csId = (m.ccna_portal_last_cs || "").trim();
    const expMs = parseInt(String(m.ccna_portal_access_expires_ms || ""), 10);
    if (csId.indexOf("cs_") === 0 && Number.isFinite(expMs)) {
      try {
        const session = await stripe.checkout.sessions.retrieve(csId, { expand: SESSION_EXPAND_LOCAL });
        const productId = inferProductIdFromCheckoutSession(session);
        if (isCcnaPortalProduct(productId)) {
          considerPortal(session, productId, expMs);
        }
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
    const discovered = await discoverCheckoutSessionsForEmail(stripe, normalized, { max: 40 });
    for (let k = 0; k < discovered.length; k++) {
      await evaluateSession(discovered[k]);
    }
  } catch (e) {
    console.warn("[ccna-portal] email session discovery skipped:", e.message);
  }

  return { bestPortal, hadExpiredPortal, bestTestSim };
}

/**
 * Find the best active CCNA portal checkout for an email (metadata, customer sessions, or Stripe search).
 * @param {import('stripe').Stripe} stripe
 * @param {string} email
 */
export async function findActivePortalSessionForEmail(stripe, email) {
  const { bestPortal } = await scanCcnaCheckoutSessionsForEmail(stripe, email);
  return bestPortal;
}

/**
 * @param {import('stripe').Stripe} stripe
 * @param {string} email
 */
export async function getCcnaPurchaseHintsForEmail(stripe, email) {
  const { bestPortal, hadExpiredPortal, bestTestSim } = await scanCcnaCheckoutSessionsForEmail(
    stripe,
    email
  );
  return {
    activePortal: bestPortal,
    portalExpired: !bestPortal && hadExpiredPortal,
    timedExamOnly: !bestPortal && !!bestTestSim,
  };
}
