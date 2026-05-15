/**
 * POST /api/create-checkout-session
 * Body (JSON, optional): { "productId": "ccna-test-simulation" | "ccna-portal-30d" }
 *
 * Env:
 *   STRIPE_SECRET_KEY              — sk_live_… / sk_test_… (or rk_* restricted key with Checkout)
 *   STRIPE_PRICE_CCNA_TEST_SIM     — price_… for one-time timed test simulation
 *   STRIPE_PRICE_CCNA_PORTAL_30D   — price_… for 30-day training portal / library access
 *   PUBLIC_SITE_URL                — site origin (e.g. https://becertifiedtoday.com). Missing https:// is added;
 *                                    trailing slashes, paths, and stray quotes are stripped to avoid broken redirects.
 *
 * Checkout shows a promotion-code field when allow_promotion_codes is true. Create
 * coupons + promotion codes in Stripe Dashboard (Product catalog → Coupons, or Billing → Coupons).
 */
import Stripe from "stripe";
import { getStripeSecretKey } from "./stripe-secret-key.js";
import { normalizePublicSiteUrl } from "./normalize-public-site-url.js";

const DEFAULT_PRODUCT = "ccna-test-simulation";

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
};

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
  }

  const sk = getStripeSecretKey(process.env.STRIPE_SECRET_KEY);
  const site = normalizePublicSiteUrl(process.env.PUBLIC_SITE_URL);

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

  if (!PRODUCTS[productId]) {
    return res.status(400).json({
      error: "Unknown productId",
      hint: `Supported values: ${Object.keys(PRODUCTS).join(", ")}.`,
    });
  }

  const cfg = PRODUCTS[productId];
  const priceId = (process.env[cfg.priceEnv] || "").trim();

  if (!priceId) {
    return res.status(503).json({
      error: "Checkout is not configured",
      hint: `Set ${cfg.priceEnv} in Vercel (Stripe Dashboard → Products → Price API id). PUBLIC_SITE_URL must match the hostname customers use after checkout.`,
    });
  }

  const stripe = new Stripe(sk.secret);

  try {
    const session = await stripe.checkout.sessions.create({
      mode: "payment",
      line_items: [{ price: priceId, quantity: 1 }],
      allow_promotion_codes: true,
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
    });

    return res.status(200).json({ url: session.url });
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
