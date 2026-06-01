/**
 * List CCNA / ENCOR / Security+ portal subscribers from Stripe Customer metadata (one scan).
 */

import {
  checkoutSessionIsPaid,
  inferProductIdFromCheckoutSession,
  isCcnaPortalProduct,
  isEncorPortalProduct,
  isSecplusPortalProduct,
  portalAccessExpiresAtMs,
} from "./ccna-portal-stripe.js";

const PRODUCT_CONFIGS = [
  {
    id: "ccna",
    lastCsKey: "ccna_portal_last_cs",
    expiresMsKey: "ccna_portal_access_expires_ms",
    isPortalProduct: isCcnaPortalProduct,
  },
  {
    id: "encor",
    lastCsKey: "encor_portal_last_cs",
    expiresMsKey: "encor_portal_access_expires_ms",
    isPortalProduct: isEncorPortalProduct,
  },
  {
    id: "secplus",
    lastCsKey: "secplus_portal_last_cs",
    expiresMsKey: "secplus_portal_access_expires_ms",
    isPortalProduct: isSecplusPortalProduct,
  },
];

function parsePortalMetadata(customer, config) {
  const m = customer.metadata || {};
  const checkoutSessionId = (m[config.lastCsKey] || "").trim();
  const accessExpiresAtMs = parseInt(String(m[config.expiresMsKey] || ""), 10);
  if (checkoutSessionId.indexOf("cs_") !== 0 || !Number.isFinite(accessExpiresAtMs)) {
    return null;
  }
  const email = (customer.email || "").trim().toLowerCase();
  return {
    product: config.id,
    customerId: customer.id,
    email: email || "(no email on file)",
    checkoutSessionId,
    accessExpiresAtMs,
    accessExpiresAt: new Date(accessExpiresAtMs).toISOString(),
    active: accessExpiresAtMs > Date.now(),
  };
}

function splitActiveExpired(rows) {
  const sorted = rows.slice().sort((a, b) => b.accessExpiresAtMs - a.accessExpiresAtMs);
  const active = sorted.filter((r) => r.active);
  const expired = sorted.filter((r) => !r.active);
  return {
    active,
    expired,
    counts: {
      active: active.length,
      expired: expired.length,
      total: sorted.length,
    },
  };
}

/**
 * @param {import('stripe').Stripe} stripe
 * @param {{ maxScan?: number }} [opts]
 */
export async function listAllPortalSubscribersFromStripe(stripe, opts = {}) {
  const maxScan = Math.min(Math.max(Number(opts.maxScan) || 2000, 100), 10000);
  const buckets = Object.fromEntries(PRODUCT_CONFIGS.map((c) => [c.id, []]));
  const seen = Object.fromEntries(PRODUCT_CONFIGS.map((c) => [c.id, new Set()]));
  let startingAfter;
  let scanned = 0;

  while (scanned < maxScan) {
    const page = await stripe.customers.list({
      limit: 100,
      ...(startingAfter ? { starting_after: startingAfter } : {}),
    });

    for (let i = 0; i < page.data.length; i++) {
      scanned++;
      const customer = page.data[i];
      for (let j = 0; j < PRODUCT_CONFIGS.length; j++) {
        const config = PRODUCT_CONFIGS[j];
        const row = parsePortalMetadata(customer, config);
        if (!row || seen[config.id].has(row.customerId)) continue;
        seen[config.id].add(row.customerId);
        buckets[config.id].push(row);
      }
    }

    if (!page.has_more || !page.data.length) break;
    startingAfter = page.data[page.data.length - 1].id;
  }

  const result = {};
  for (let k = 0; k < PRODUCT_CONFIGS.length; k++) {
    const id = PRODUCT_CONFIGS[k].id;
    result[id] = splitActiveExpired(buckets[id]);
  }

  return {
    ...result,
    customersScanned: scanned,
    scanTruncated: scanned >= maxScan,
  };
}

/**
 * @param {import('stripe').Stripe} stripe
 * @param {object[]} rows
 * @param {{ isPortalProduct: (productId: string) => boolean, notProductNote?: string }} config
 */
export async function enrichPortalRowsWithCheckout(stripe, rows, config) {
  const { isPortalProduct, notProductNote = "not portal access" } = config;
  const out = [];
  for (let i = 0; i < rows.length; i++) {
    const row = { ...rows[i] };
    try {
      const session = await stripe.checkout.sessions.retrieve(row.checkoutSessionId, {
        expand: ["line_items.data.price"],
      });
      if (!checkoutSessionIsPaid(session)) {
        row.stripeNote = "checkout not paid";
      } else if (!isPortalProduct(inferProductIdFromCheckoutSession(session))) {
        row.stripeNote = notProductNote;
      } else {
        const productId = inferProductIdFromCheckoutSession(session);
        const exp = portalAccessExpiresAtMs(session, productId);
        row.accessExpiresAtMs = exp;
        row.accessExpiresAt = new Date(exp).toISOString();
        row.active = exp > Date.now();
        row.productId = productId;
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

/** @param {import('stripe').Stripe} stripe */
export async function listCcnaPortalSubscribersFromStripe(stripe, opts) {
  const all = await listAllPortalSubscribersFromStripe(stripe, opts);
  return {
    active: all.ccna.active,
    expired: all.ccna.expired,
    totalWithPortalMetadata: all.ccna.counts.total,
    customersScanned: all.customersScanned,
    scanTruncated: all.scanTruncated,
  };
}
