/**
 * Shared Stripe helpers for CCNA and ENCOR portal checkout sessions (verify API, webhook, magic-link redeem).
 */

function inferProductTrackFromSuccessUrl(session) {
  const url = String(session.success_url || "");
  if (/CCNP-ENCOR-Study/i.test(url)) return "encor";
  if (/CCNA-Study|CCNA_Sim_EXAM/i.test(url)) return "ccna";
  return null;
}

function productIdFromAmountCents(amount, track) {
  if (amount === 999) {
    return track === "encor" ? "encor-portal-10d" : "ccna-portal-10d";
  }
  if (amount === 1999 || amount === 1499) {
    return track === "encor" ? "encor-portal-30d" : "ccna-portal-30d";
  }
  if (amount === 499) {
    return track === "encor" ? "encor-test-simulation" : "ccna-test-simulation";
  }
  return null;
}

/** @param {import('stripe').Stripe.Checkout.Session} session */
export function inferProductIdFromCheckoutSession(session, env = process.env) {
  let productId = session.metadata?.productId || null;
  const paid =
    session.payment_status === "paid" || session.payment_status === "no_payment_required";

  if (!productId && paid) {
    const ccnaPortal30 = (env.STRIPE_PRICE_CCNA_PORTAL_30D || "").trim();
    const ccnaPortal10 = (env.STRIPE_PRICE_CCNA_PORTAL_10D || "").trim();
    const ccnaTestSim = (env.STRIPE_PRICE_CCNA_TEST_SIM || "").trim();
    const encorPortal30 = (env.STRIPE_PRICE_ENCOR_PORTAL_30D || "").trim();
    const encorPortal10 = (env.STRIPE_PRICE_ENCOR_PORTAL_10D || "").trim();
    const encorTestSim = (env.STRIPE_PRICE_ENCOR_TEST_SIM || "").trim();
    const lines = session.line_items?.data || [];
    for (let i = 0; i < lines.length; i++) {
      const pid = lines[i]?.price?.id;
      if (!pid) continue;
      if (ccnaPortal30 && pid === ccnaPortal30) {
        productId = "ccna-portal-30d";
        break;
      }
      if (ccnaPortal10 && pid === ccnaPortal10) {
        productId = "ccna-portal-10d";
        break;
      }
      if (ccnaTestSim && pid === ccnaTestSim) {
        productId = "ccna-test-simulation";
        break;
      }
      if (encorPortal30 && pid === encorPortal30) {
        productId = "encor-portal-30d";
        break;
      }
      if (encorPortal10 && pid === encorPortal10) {
        productId = "encor-portal-10d";
        break;
      }
      if (encorTestSim && pid === encorTestSim) {
        productId = "encor-test-simulation";
        break;
      }
    }
  }
  if (!productId && paid && session.currency === "usd") {
    const amount = typeof session.amount_subtotal === "number" ? session.amount_subtotal : session.amount_total;
    const track = inferProductTrackFromSuccessUrl(session);
    productId = productIdFromAmountCents(amount, track);
  }
  return productId;
}

export function isCcnaPortalProduct(productId) {
  return productId === "ccna-portal-30d" || productId === "ccna-portal-10d";
}

export function isEncorPortalProduct(productId) {
  return productId === "encor-portal-30d" || productId === "encor-portal-10d";
}

/** Fixed window from Stripe timestamps (not "now + 30d"). */
/** @param {import('stripe').Stripe.Checkout.Session} sess */
export function portalAccessExpiresAtMs(sess, productId = null) {
  let anchorSec =
    typeof sess.created === "number" && sess.created > 0 ? sess.created : Math.floor(Date.now() / 1000);
  try {
    const st = sess.status_transitions;
    if (st && typeof st.paid_at === "number" && st.paid_at > 0) {
      anchorSec = Math.max(anchorSec, st.paid_at);
    }
  } catch (_) {}
  try {
    const pi = sess.payment_intent;
    if (pi && typeof pi === "object" && typeof pi.created === "number" && pi.created > 0) {
      anchorSec = Math.max(anchorSec, pi.created);
    }
  } catch (_) {}
  const days =
    productId === "ccna-portal-10d" || productId === "encor-portal-10d" ? 10 : 30;
  return anchorSec * 1000 + days * 86400000;
}

export function checkoutSessionIsPaid(session) {
  return session.payment_status === "paid" || session.payment_status === "no_payment_required";
}

/**
 * Remember portal purchase on a Stripe Customer so learners can request a fresh magic link by email.
 * @param {import('stripe').Stripe} stripe
 * @param {import('stripe').Stripe.Checkout.Session} session
 */
export async function upsertCustomerPortalMetadata(stripe, session, accessExpiresAtMs) {
  const email = (session.customer_details?.email || "").trim().toLowerCase();
  if (!email) return null;

  let customerId = session.customer || null;
  if (!customerId) {
    const existing = await stripe.customers.list({ email, limit: 5 });
    if (existing.data.length > 0) {
      customerId = existing.data[0].id;
    } else {
      const c = await stripe.customers.create({
        email,
        metadata: { ccna_portal_customer: "1" },
      });
      customerId = c.id;
    }
  }

  await stripe.customers.update(customerId, {
    metadata: {
      ccna_portal_customer: "1",
      ccna_portal_last_cs: session.id,
      ccna_portal_access_expires_ms: String(accessExpiresAtMs),
    },
  });

  return customerId;
}

/**
 * Remember ENCOR portal purchase on a Stripe Customer for magic-link restore.
 * @param {import('stripe').Stripe} stripe
 * @param {import('stripe').Stripe.Checkout.Session} session
 */
export async function upsertEncorCustomerPortalMetadata(stripe, session, accessExpiresAtMs) {
  const email = (session.customer_details?.email || "").trim().toLowerCase();
  if (!email) return null;

  let customerId = session.customer || null;
  if (!customerId) {
    const existing = await stripe.customers.list({ email, limit: 5 });
    if (existing.data.length > 0) {
      customerId = existing.data[0].id;
    } else {
      const c = await stripe.customers.create({
        email,
        metadata: { encor_portal_customer: "1" },
      });
      customerId = c.id;
    }
  }

  await stripe.customers.update(customerId, {
    metadata: {
      encor_portal_customer: "1",
      encor_portal_last_cs: session.id,
      encor_portal_access_expires_ms: String(accessExpiresAtMs),
    },
  });

  return customerId;
}
