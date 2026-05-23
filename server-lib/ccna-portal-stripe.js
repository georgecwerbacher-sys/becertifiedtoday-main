/**
 * Shared Stripe helpers for CCNA portal checkout sessions (verify API, webhook, magic-link redeem).
 */

/** @param {import('stripe').Stripe.Checkout.Session} session */
export function inferProductIdFromCheckoutSession(session, env = process.env) {
  let productId = session.metadata?.productId || null;
  const paid =
    session.payment_status === "paid" || session.payment_status === "no_payment_required";

  if (!productId && paid) {
    const portalPrice = (env.STRIPE_PRICE_CCNA_PORTAL_30D || "").trim();
    const portal10dPrice = (env.STRIPE_PRICE_CCNA_PORTAL_10D || "").trim();
    const testSimPrice = (env.STRIPE_PRICE_CCNA_TEST_SIM || "").trim();
    const lines = session.line_items?.data || [];
    for (let i = 0; i < lines.length; i++) {
      const pid = lines[i]?.price?.id;
      if (!pid) continue;
      if (portalPrice && pid === portalPrice) {
        productId = "ccna-portal-30d";
        break;
      }
      if (portal10dPrice && pid === portal10dPrice) {
        productId = "ccna-portal-10d";
        break;
      }
      if (testSimPrice && pid === testSimPrice) {
        productId = "ccna-test-simulation";
        break;
      }
    }
  }
  if (!productId && paid && session.currency === "usd") {
    const amount = typeof session.amount_subtotal === "number" ? session.amount_subtotal : session.amount_total;
    if (amount === 999) {
      productId = "ccna-portal-10d";
    } else if (amount === 1999 || amount === 1499) {
      productId = "ccna-portal-30d";
    } else if (amount === 499) {
      productId = "ccna-test-simulation";
    }
  }
  return productId;
}

export function isCcnaPortalProduct(productId) {
  return productId === "ccna-portal-30d" || productId === "ccna-portal-10d";
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
  const days = productId === "ccna-portal-10d" ? 10 : 30;
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
