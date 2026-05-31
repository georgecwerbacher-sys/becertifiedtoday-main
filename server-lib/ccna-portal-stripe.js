/**
 * Shared Stripe helpers for CCNA and ENCOR portal checkout sessions (verify API, webhook, magic-link redeem).
 */

/** buy.stripe.com URL slugs — used when price env vars or success_url metadata are missing. */
const PAYMENT_LINK_SLUG_TO_PRODUCT = {
  cNidR81Wlel13yEdfSc3m05: "encor-portal-10d",
  cNidR80Sh0ubc5aejWc3m00: "encor-portal-30d",
  "7sYcN4bwV1yf1qwb7Kc3m09": "encor-test-simulation",
  "3cIaEWbwVb8P8SYejWc3m01": "encor-test-simulation",
  "5kQ14mbwVgt93yEfo0c3m07": "secplus-portal-30d",
  "8x28wObwVfp54CIgs4c3m06": "secplus-portal-10d",
  "9B63cudF33Gnc5a1xac3m08": "secplus-test-simulation",
};

function productIdFromPaymentLinkSession(session) {
  const pl = session.payment_link;
  const urls = [];
  if (pl && typeof pl === "object" && pl.url) {
    urls.push(String(pl.url));
  }
  if (session.url) urls.push(String(session.url));
  for (let i = 0; i < urls.length; i++) {
    const url = urls[i];
    for (const slug of Object.keys(PAYMENT_LINK_SLUG_TO_PRODUCT)) {
      if (url.includes(slug)) {
        return PAYMENT_LINK_SLUG_TO_PRODUCT[slug];
      }
    }
  }
  return null;
}

function inferProductTrackFromSuccessUrl(session) {
  const url = String(session.success_url || "");
  if (/COMP_TIA_SEC\+/i.test(url)) return "secplus";
  if (/CCNP-ENCOR-Study/i.test(url)) return "encor";
  if (/CCNA-Study|CCNA_Sim_EXAM/i.test(url)) return "ccna";
  return null;
}

function productIdFromAmountCents(amount, track, session = null) {
  const urls = session
    ? `${session.success_url || ""} ${session.cancel_url || ""}`
    : "";
  const isTestSimUrl = /test-simulation-runner|begin-test-simulation|test-simulation\.html/i.test(urls);

  if (amount === 999 && isTestSimUrl) {
    if (track === "encor") return "encor-test-simulation";
    if (track === "secplus") return "secplus-test-simulation";
    return "ccna-test-simulation";
  }
  if (amount === 999) {
    if (track === "encor") return "encor-portal-10d";
    if (track === "secplus") return "secplus-portal-10d";
    return "ccna-portal-10d";
  }
  if (amount === 1999 || amount === 1499) {
    if (track === "encor") return "encor-portal-30d";
    if (track === "secplus") return "secplus-portal-30d";
    return "ccna-portal-30d";
  }
  if (amount === 499) {
    if (track === "encor") return "encor-test-simulation";
    if (track === "secplus") return "secplus-test-simulation";
    return "ccna-test-simulation";
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
    const secplusPortal30 = (env.STRIPE_PRICE_SECPLUS_PORTAL_30D || "").trim();
    const secplusPortal10 = (env.STRIPE_PRICE_SECPLUS_PORTAL_10D || "").trim();
    const secplusTestSim = (env.STRIPE_PRICE_SECPLUS_TEST_SIM || "").trim();
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
      if (secplusPortal30 && pid === secplusPortal30) {
        productId = "secplus-portal-30d";
        break;
      }
      if (secplusPortal10 && pid === secplusPortal10) {
        productId = "secplus-portal-10d";
        break;
      }
      if (secplusTestSim && pid === secplusTestSim) {
        productId = "secplus-test-simulation";
        break;
      }
    }
  }
  if (!productId && paid) {
    productId = productIdFromPaymentLinkSession(session);
  }
  if (!productId && paid) {
    const lines = session.line_items?.data || [];
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const name = String(line?.description || line?.price?.product?.name || "");
      if (/encor/i.test(name) && /10.?day|10 day/i.test(name)) {
        productId = "encor-portal-10d";
        break;
      }
      if (/security\+|secplus|sy0-701/i.test(name) && /10.?day|10 day/i.test(name)) {
        productId = "secplus-portal-10d";
        break;
      }
      if (/encor/i.test(name) && /30.?day|30 day|month/i.test(name)) {
        productId = "encor-portal-30d";
        break;
      }
      if (/security\+|secplus|sy0-701/i.test(name) && /30.?day|30 day|month/i.test(name)) {
        productId = "secplus-portal-30d";
        break;
      }
      if (/security\+|secplus|sy0-701/i.test(name) && /simulation|timed|exam/i.test(name)) {
        productId = "secplus-test-simulation";
        break;
      }
      if (/ccna/i.test(name) && /10.?day|10 day/i.test(name)) {
        productId = "ccna-portal-10d";
        break;
      }
      if (/ccna/i.test(name) && /30.?day|30 day|month/i.test(name)) {
        productId = "ccna-portal-30d";
        break;
      }
      if (/ccna/i.test(name) && /simulation|timed|exam sim/i.test(name)) {
        productId = "ccna-test-simulation";
        break;
      }
      if (/encor/i.test(name) && /simulation|timed|exam sim/i.test(name)) {
        productId = "encor-test-simulation";
        break;
      }
    }
  }
  if (!productId && paid && session.currency === "usd") {
    const amount = typeof session.amount_subtotal === "number" ? session.amount_subtotal : session.amount_total;
    let track = inferProductTrackFromSuccessUrl(session);
    if (!track) {
      const cancelUrl = String(session.cancel_url || "");
      if (/CCNP-ENCOR-Study/i.test(cancelUrl)) track = "encor";
      else if (/COMP_TIA_SEC\+/i.test(cancelUrl)) track = "secplus";
      else if (/CCNA-Study|CCNA_Sim_EXAM/i.test(cancelUrl)) track = "ccna";
    }
    const plProduct = productIdFromPaymentLinkSession(session);
    if (!track && plProduct) {
      if (plProduct.startsWith("encor-")) track = "encor";
      else if (plProduct.startsWith("secplus-")) track = "secplus";
      else if (plProduct.startsWith("ccna-")) track = "ccna";
    }
    if (plProduct) {
      productId = plProduct;
    } else if (typeof amount === "number") {
      productId = productIdFromAmountCents(amount, track, session);
    }
  }
  return productId;
}

export function isCcnaPortalProduct(productId) {
  return productId === "ccna-portal-30d" || productId === "ccna-portal-10d";
}

export function isEncorPortalProduct(productId) {
  return productId === "encor-portal-30d" || productId === "encor-portal-10d";
}

export function isSecplusPortalProduct(productId) {
  return productId === "secplus-portal-30d" || productId === "secplus-portal-10d";
}

export function isSecplusTestSimulationProduct(productId) {
  return productId === "secplus-test-simulation";
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
    productId === "ccna-portal-10d" || productId === "encor-portal-10d" || productId === "secplus-portal-10d"
      ? 10
      : productId === "ccna-portal-30d" ||
          productId === "encor-portal-30d" ||
          productId === "secplus-portal-30d"
        ? 30
        : 30;
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

/**
 * Remember Security+ portal purchase on a Stripe Customer for magic-link restore.
 * @param {import('stripe').Stripe} stripe
 * @param {import('stripe').Stripe.Checkout.Session} session
 */
export async function upsertSecplusCustomerPortalMetadata(stripe, session, accessExpiresAtMs) {
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
        metadata: { secplus_portal_customer: "1" },
      });
      customerId = c.id;
    }
  }

  await stripe.customers.update(customerId, {
    metadata: {
      secplus_portal_customer: "1",
      secplus_portal_last_cs: session.id,
      secplus_portal_access_expires_ms: String(accessExpiresAtMs),
    },
  });

  return customerId;
}
