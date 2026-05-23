/**
 * List CCNA portal purchasers from Stripe Customer metadata (written at checkout).
 */

import {
  checkoutSessionIsPaid,
  inferProductIdFromCheckoutSession,
  isCcnaPortalProduct,
  portalAccessExpiresAtMs,
} from "./ccna-portal-stripe.js";

function parsePortalMetadata(customer) {
  const m = customer.metadata || {};
  const checkoutSessionId = (m.ccna_portal_last_cs || "").trim();
  const accessExpiresAtMs = parseInt(String(m.ccna_portal_access_expires_ms || ""), 10);
  if (checkoutSessionId.indexOf("cs_") !== 0 || !Number.isFinite(accessExpiresAtMs)) {
    return null;
  }
  const email = (customer.email || "").trim().toLowerCase();
  return {
    customerId: customer.id,
    email: email || "(no email on file)",
    checkoutSessionId,
    accessExpiresAtMs,
    accessExpiresAt: new Date(accessExpiresAtMs).toISOString(),
    active: accessExpiresAtMs > Date.now(),
  };
}

/**
 * Scan Stripe customers for portal metadata (no separate DB).
 * @param {import('stripe').Stripe} stripe
 * @param {{ maxScan?: number }} [opts]
 */
export async function listPortalCustomersFromStripe(stripe, opts = {}) {
  const maxScan = Math.min(Math.max(Number(opts.maxScan) || 2000, 100), 10000);
  const rows = [];
  const seen = new Set();
  let startingAfter;
  let scanned = 0;

  while (scanned < maxScan) {
    const page = await stripe.customers.list({
      limit: 100,
      ...(startingAfter ? { starting_after: startingAfter } : {}),
    });

    for (let i = 0; i < page.data.length; i++) {
      scanned++;
      const row = parsePortalMetadata(page.data[i]);
      if (!row || seen.has(row.customerId)) continue;
      seen.add(row.customerId);
      rows.push(row);
    }

    if (!page.has_more || !page.data.length) break;
    startingAfter = page.data[page.data.length - 1].id;
  }

  rows.sort((a, b) => b.accessExpiresAtMs - a.accessExpiresAtMs);

  const active = rows.filter((r) => r.active);
  const expired = rows.filter((r) => !r.active);

  return {
    active,
    expired,
    totalWithPortalMetadata: rows.length,
    customersScanned: scanned,
    scanTruncated: scanned >= maxScan,
  };
}

/**
 * Re-check checkout session + product for active rows (optional enrichment).
 * @param {import('stripe').Stripe} stripe
 * @param {ReturnType<typeof parsePortalMetadata>[]} rows
 */
export async function enrichPortalRowsWithCheckout(stripe, rows) {
  const out = [];
  for (let i = 0; i < rows.length; i++) {
    const row = { ...rows[i] };
    try {
      const session = await stripe.checkout.sessions.retrieve(row.checkoutSessionId, {
        expand: ["line_items.data.price"],
      });
      if (!checkoutSessionIsPaid(session)) {
        row.stripeNote = "checkout not paid";
      } else if (!isCcnaPortalProduct(inferProductIdFromCheckoutSession(session))) {
        row.stripeNote = "not ccna portal access";
      } else {
        const productId = inferProductIdFromCheckoutSession(session);
        const exp = portalAccessExpiresAtMs(session, productId);
        row.accessExpiresAtMs = exp;
        row.accessExpiresAt = new Date(exp).toISOString();
        row.active = exp > Date.now();
        if (typeof session.created === "number" && session.created > 0) {
          row.purchasedAt = new Date(session.created * 1000).toISOString();
        }
      }
    } catch (e) {
      row.stripeNote = e && e.message ? String(e.message).slice(0, 80) : "session lookup failed";
    }
    out.push(row);
  }
  return out;
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
    if (!full.line_items?.data?.length) {
      full = await stripe.checkout.sessions.retrieve(session.id, {
        expand: ["payment_intent", "line_items.data.price"],
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
    console.warn("[ccna-portal] checkout session search skipped:", e.message);
  }

  return best;
}
