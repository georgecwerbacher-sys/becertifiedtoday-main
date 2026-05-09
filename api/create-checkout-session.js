/**
 * POST /api/create-checkout-session
 * Body (JSON, optional): { "productId": "ccna-test-simulation" }
 *
 * Env:
 *   STRIPE_SECRET_KEY           — sk_live_… or sk_test_…
 *   STRIPE_PRICE_CCNA_TEST_SIM  — price_… for one-time payment (create in Stripe Dashboard)
 *   PUBLIC_SITE_URL             — no trailing slash, e.g. https://becertifiedtoday.com
 */
import Stripe from "stripe";

const DEFAULT_PRODUCT = "ccna-test-simulation";

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
  }

  const secret = process.env.STRIPE_SECRET_KEY;
  const priceId = process.env.STRIPE_PRICE_CCNA_TEST_SIM;
  const site = process.env.PUBLIC_SITE_URL || "";

  if (!secret || !priceId || !site) {
    return res.status(503).json({
      error: "Checkout is not configured",
      hint: "Set STRIPE_SECRET_KEY, STRIPE_PRICE_CCNA_TEST_SIM, and PUBLIC_SITE_URL on Vercel.",
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

  const productId = body.productId || DEFAULT_PRODUCT;

  const stripe = new Stripe(secret);

  try {
    const session = await stripe.checkout.sessions.create({
      mode: "payment",
      line_items: [{ price: priceId, quantity: 1 }],
      success_url: `${site}/CCNA-Study/ccna-test-simulation.html?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${site}/CCNA-Study/CCNA_Training_Portal.html`,
      metadata: {
        productId,
        blueprint: "ccna-test-simulation-blueprint@v1",
      },
      payment_intent_data: {
        metadata: {
          productId,
        },
      },
    });

    return res.status(200).json({ url: session.url });
  } catch (e) {
    console.error("Stripe checkout session error:", e.message);
    return res.status(500).json({
      error: "Could not create checkout session",
      detail: process.env.NODE_ENV === "development" ? e.message : undefined,
    });
  }
}
