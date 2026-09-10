/**
 * POST /api/create-checkout-session
 * Body (JSON, optional): {
 *   "productId": "ccna-test-simulation" | "ccna-portal-10d" | "ccna-portal-30d" | "secplus-portal-30d"
 *   "promoCode": "SEP50PERCENTOFF" (optional customer-facing promotion code)
 * }
 *
 * Env:
 *   STRIPE_SECRET_KEY              — sk_live_… / sk_test_… (or rk_* restricted key with Checkout)
 *   STRIPE_PRICE_CCNA_TEST_SIM     — price_… for one-time timed test simulation
 *   STRIPE_PRICE_CCNA_PORTAL_10D   — price_… for 10-day training portal / library access
 *   STRIPE_PRICE_CCNA_PORTAL_30D   — price_… for 30-day training portal / library access
 *   STRIPE_PRICE_SECPLUS_PORTAL_30D — optional price_… for Security+ 30-day; if unset, finds or creates $19.99
 *   PUBLIC_SITE_URL                — site origin (e.g. https://becertifiedtoday.com). Missing https:// is added;
 *                                    trailing slashes, paths, and stray quotes are stripped to avoid broken redirects.
 *
 * Checkout shows a promotion-code field when allow_promotion_codes is true, unless a promoCode
 * from the body was applied as a session discount.
 *
 * SEP50PERCENTOFF (and similar codes) are often limited to specific Stripe products. The Security+
 * 30-day line item is resolved onto a product that coupon actually applies to, so Apply works.
 */
import Stripe from "stripe";
import { getStripeSecretKey } from "../server-lib/stripe-secret-key.js";
import { normalizePublicSiteUrl } from "../server-lib/normalize-public-site-url.js";

const DEFAULT_PRODUCT = "ccna-test-simulation";
const SECPLUS_30D_AMOUNT = 1999;
const SECPLUS_30D_NAME = "CompTIA Security+ SY0-701 - 30-day all-access pass";
const SECPLUS_30D_DESCRIPTION =
  "30 days of SY0-701 exam prep on Be Certified Today: 1000+ interactive practice questions (SY0-701 objectives), PBQ-style hot-spot simulations, adaptive domain review, progress tracking, and a full 90-minute timed practice exam - all in your browser on phone, tablet, or desktop. One-time purchase; no subscription. Access starts at checkout on this device and browser.";
const SECPLUS_30D_LINK_SLUGS = ["5kQ14mbwVgt93yEfo0c3m07", "cNi28q6cB90H3yEdfSc3m0a"];

const PRODUCTS = {
  "ccna-test-simulation": {
    priceEnv: "STRIPE_PRICE_CCNA_TEST_SIM",
    successPath: "/CCNA_Sim_EXAM/test-simulation-runner.html?session_id={CHECKOUT_SESSION_ID}",
    cancelPath: "/CCNA_Sim_EXAM/begin-test-simulation.html",
    blueprint: "ccna-test-simulation-blueprint@v3",
  },
  "ccna-portal-30d": {
    priceEnv: "STRIPE_PRICE_CCNA_PORTAL_30D",
    successPath: "/CCNA-Study/CCNA_Training_Portal.html?session_id={CHECKOUT_SESSION_ID}",
    cancelPath: "/ccna-home.html#purchase",
    blueprint: "ccna-portal-30d@v1",
  },
  "ccna-portal-10d": {
    priceEnv: "STRIPE_PRICE_CCNA_PORTAL_10D",
    successPath: "/CCNA-Study/CCNA_Training_Portal.html?session_id={CHECKOUT_SESSION_ID}",
    cancelPath: "/ccna-home.html#purchase",
    blueprint: "ccna-portal-10d@v1",
  },
  "secplus-portal-30d": {
    priceEnv: "STRIPE_PRICE_SECPLUS_PORTAL_30D",
    successPath: "/COMP_TIA_SEC+/secplus-portal-checkout-success.html?session_id={CHECKOUT_SESSION_ID}",
    cancelPath: "/comptia-sec+-home.html#purchase",
    blueprint: "secplus-portal-30d@v1",
    fallbackUnitAmount: SECPLUS_30D_AMOUNT,
  },
};

function headerFirst(req, name) {
  const raw = req.headers?.[name];
  if (Array.isArray(raw)) return String(raw[0] || "").split(",")[0].trim();
  return String(raw || "").split(",")[0].trim();
}

function resolveSiteUrl(req) {
  const fromEnv = normalizePublicSiteUrl(process.env.PUBLIC_SITE_URL);
  if (fromEnv) return fromEnv;
  const host = headerFirst(req, "x-forwarded-host") || headerFirst(req, "host");
  const proto = headerFirst(req, "x-forwarded-proto") || "https";
  if (host) {
    const fromHost = normalizePublicSiteUrl(`${proto}://${host}`);
    if (fromHost) return fromHost;
  }
  return normalizePublicSiteUrl("https://becertifiedtoday.com");
}

function productNameLooksLikeSecplus30d(name) {
  const n = String(name || "");
  return /security\+|sy0-701|secplus/i.test(n) && /30.?day|all-access/i.test(n);
}

function isSecplus30dProduct(product) {
  if (!product || product.deleted || product.active === false) return false;
  return productNameLooksLikeSecplus30d(product.name);
}

function couponProductIds(coupon) {
  const ids = coupon?.applies_to?.products;
  return Array.isArray(ids) ? ids.filter(Boolean) : [];
}

async function findPromotion(stripe, code) {
  const c = String(code || "").trim();
  if (!c) return null;
  try {
    const list = await stripe.promotionCodes.list({
      code: c,
      active: true,
      limit: 1,
      expand: ["data.coupon"],
    });
    const promo = list.data[0] || null;
    if (!promo) return null;
    let coupon = promo.coupon;
    if (typeof coupon === "string") {
      coupon = await stripe.coupons.retrieve(coupon);
    }
    return { id: promo.id, coupon };
  } catch (e) {
    console.warn("promotion code lookup failed:", e.message);
    return null;
  }
}

async function oneTimeUsdPrices(stripe, productId) {
  const prices = await stripe.prices.list({
    product: productId,
    active: true,
    limit: 30,
  });
  return prices.data.filter((p) => p.currency === "usd" && p.type === "one_time" && !p.recurring);
}

async function priceOnProduct(stripe, productId, amount) {
  const usd = await oneTimeUsdPrices(stripe, productId);
  const match = usd.find((p) => p.unit_amount === amount);
  if (match) return match.id;
  const created = await stripe.prices.create({
    product: productId,
    currency: "usd",
    unit_amount: amount,
  });
  return created.id;
}

async function productIdFromKnownPaymentLink(stripe) {
  for (const active of [false, true]) {
    let startingAfter;
    for (let page = 0; page < 6; page++) {
      const params = { limit: 100, active };
      if (startingAfter) params.starting_after = startingAfter;
      const list = await stripe.paymentLinks.list(params);
      const match = list.data.find((link) =>
        SECPLUS_30D_LINK_SLUGS.some((slug) => String(link.url || "").includes(slug))
      );
      if (match) {
        const full = await stripe.paymentLinks.retrieve(match.id, {
          expand: ["line_items.data.price"],
        });
        const price = full.line_items?.data?.[0]?.price;
        const productId = typeof price?.product === "string" ? price.product : price?.product?.id;
        if (productId) return productId;
      }
      if (!list.has_more || !list.data.length) break;
      startingAfter = list.data[list.data.length - 1].id;
    }
  }
  return null;
}

async function resolveSecplus30dLineItems(stripe, cfg, promotion) {
  const restricted = couponProductIds(promotion?.coupon);
  const envPriceId = (process.env[cfg.priceEnv] || "").trim();

  if (restricted.length) {
    const named = [];
    for (const id of restricted) {
      try {
        const product = await stripe.products.retrieve(id);
        named.push(product);
      } catch (e) {
        console.warn("coupon product retrieve failed:", id, e.message);
      }
    }
    const product =
      named.find(isSecplus30dProduct) ||
      named.find((p) => /security\+|sy0-701|secplus/i.test(p?.name || "")) ||
      named[0];
    if (product?.id) {
      const priceId = await priceOnProduct(stripe, product.id, SECPLUS_30D_AMOUNT);
      console.log("secplus-portal-30d using coupon product", product.id, "price", priceId);
      return [{ price: priceId, quantity: 1 }];
    }
  }

  try {
    const fromLink = await productIdFromKnownPaymentLink(stripe);
    if (fromLink && (!restricted.length || restricted.includes(fromLink))) {
      const priceId = await priceOnProduct(stripe, fromLink, SECPLUS_30D_AMOUNT);
      console.log("secplus-portal-30d using payment-link product", fromLink, "price", priceId);
      return [{ price: priceId, quantity: 1 }];
    }
  } catch (e) {
    console.warn("payment link product lookup failed:", e.message);
  }

  if (envPriceId && !restricted.length) {
    try {
      const envPrice = await stripe.prices.retrieve(envPriceId, { expand: ["product"] });
      const productId =
        typeof envPrice.product === "string" ? envPrice.product : envPrice.product?.id;
      if (productId) {
        const priceId = await priceOnProduct(stripe, productId, SECPLUS_30D_AMOUNT);
        console.log("secplus-portal-30d using env product", productId, "price", priceId);
        return [{ price: priceId, quantity: 1 }];
      }
    } catch (e) {
      console.warn("secplus-portal-30d env price lookup failed:", e.message);
    }
  }

  try {
    const products = await stripe.products.list({ active: true, limit: 100 });
    const product = products.data.find(isSecplus30dProduct);
    if (product && (!restricted.length || restricted.includes(product.id))) {
      const priceId = await priceOnProduct(stripe, product.id, SECPLUS_30D_AMOUNT);
      console.log("secplus-portal-30d using named product", product.id, "price", priceId);
      return [{ price: priceId, quantity: 1 }];
    }
  } catch (e) {
    console.warn("secplus-portal-30d name lookup failed:", e.message);
  }

  if (restricted.length) {
    throw new Error(
      "SEP50PERCENTOFF is limited to specific Stripe products, and none of those products could be used for Security+ 30-day checkout."
    );
  }

  console.warn("secplus-portal-30d falling back to ad-hoc price_data");
  return [
    {
      price_data: {
        currency: "usd",
        unit_amount: SECPLUS_30D_AMOUNT,
        product_data: {
          name: SECPLUS_30D_NAME,
          description: SECPLUS_30D_DESCRIPTION,
          metadata: { productId: "secplus-portal-30d" },
        },
      },
      quantity: 1,
    },
  ];
}

async function resolveLineItems(stripe, productId, cfg, promotion) {
  if (productId === "secplus-portal-30d") {
    return resolveSecplus30dLineItems(stripe, cfg, promotion);
  }
  const priceId = (process.env[cfg.priceEnv] || "").trim();
  if (!priceId) return null;
  return [{ price: priceId, quantity: 1 }];
}

function buildSessionParams(site, cfg, productId, lineItems, promoId) {
  const sessionParams = {
    mode: "payment",
    line_items: lineItems,
    success_url: `${site}${cfg.successPath}`,
    cancel_url: `${site}${cfg.cancelPath}`,
    metadata: {
      productId,
      blueprint: cfg.blueprint,
    },
    payment_intent_data: {
      metadata: {
        productId,
      },
    },
  };
  if (promoId) {
    sessionParams.discounts = [{ promotion_code: promoId }];
  } else {
    sessionParams.allow_promotion_codes = true;
  }
  return sessionParams;
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
  }

  const sk = getStripeSecretKey(process.env.STRIPE_SECRET_KEY);
  const site = resolveSiteUrl(req);

  if (!sk.secret) {
    return res.status(503).json({
      error: "Checkout is not configured",
      hint: sk.error,
    });
  }
  if (!site) {
    return res.status(503).json({
      error: "Checkout is not configured",
      hint: "Set PUBLIC_SITE_URL on Vercel to your public origin (e.g. https://becertifiedtoday.com).",
    });
  }

  let body = {};
  try {
    if (req.body != null) {
      if (typeof req.body === "object" && !Buffer.isBuffer(req.body)) {
        body = req.body;
      } else if (typeof req.body === "string" && req.body.length) {
        body = JSON.parse(req.body);
      }
    }
  } catch (_) {
    body = {};
  }

  const rawPid = typeof body.productId === "string" ? body.productId.trim() : "";
  const productId = rawPid || DEFAULT_PRODUCT;

  if (productId === "secplus-portal-24h") {
    return res.status(410).json({
      error: "This offer is no longer available",
      hint: "Use 30-day Security+ access from the product page.",
    });
  }

  if (!PRODUCTS[productId]) {
    return res.status(400).json({
      error: "Unknown productId",
      hint: `Supported values: ${Object.keys(PRODUCTS).join(", ")}.`,
    });
  }

  const cfg = PRODUCTS[productId];
  const stripe = new Stripe(sk.secret);
  const promotion = await findPromotion(stripe, body.promoCode);

  let lineItems;
  try {
    lineItems = await resolveLineItems(stripe, productId, cfg, promotion);
  } catch (e) {
    return res.status(503).json({
      error: "Could not start checkout",
      detail: e.message,
    });
  }

  if (!lineItems) {
    return res.status(503).json({
      error: "Checkout is not configured",
      hint: `Set ${cfg.priceEnv} in Vercel (Stripe Dashboard → Products → Price API id). PUBLIC_SITE_URL must match the hostname customers use after checkout.`,
    });
  }

  const promoId = promotion?.id || null;
  const sessionParams = buildSessionParams(site, cfg, productId, lineItems, promoId);

  try {
    const session = await stripe.checkout.sessions.create(sessionParams);
    return res.status(200).json({
      url: session.url,
      amount_subtotal: session.amount_subtotal,
      amount_total: session.amount_total,
    });
  } catch (e) {
    const message = e?.message || String(e);
    const code = e?.code || e?.type || undefined;
    console.error("Stripe checkout session error:", message, code || "");
    const payload = {
      error: "Could not create checkout session",
      detail: message,
      code: code || undefined,
    };
    if (/expired api key/i.test(message)) {
      payload.hint =
        "This secret key is no longer valid. In Stripe → Developers → API keys, copy the current Secret key (sk_live_ / sk_test_) or Restricted key (rk_live_ / rk_test_) and update STRIPE_SECRET_KEY on Vercel.";
    } else if (/invalid api key/i.test(message) && /sk_/.test(message)) {
      payload.hint =
        "Confirm STRIPE_SECRET_KEY is the Secret key (sk_ or rk_) from Stripe → Developers → API keys, not publishable (pk_), webhook (whsec_), or another product.";
    }
    return res.status(500).json(payload);
  }
}
