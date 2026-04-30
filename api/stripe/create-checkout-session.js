import { ACCESS_WINDOW_DAYS } from "../_lib/config.js";
import { getEncorAppBaseUrl } from "../_lib/encor-app-url.js";
import { getStripe } from "../_lib/stripe.js";
import { trackEvent } from "../_lib/analytics.js";

const ALLOWED_PRODUCT = "encor";

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method Not Allowed" });
  }

  try {
    const body = req.body && typeof req.body === "object" ? req.body : {};
    const product = body.product || ALLOWED_PRODUCT;
    if (product !== ALLOWED_PRODUCT) {
      return res.status(400).json({ error: "Unsupported product" });
    }

    const stripe = getStripe();
    const marketingOrigin =
      process.env.PUBLIC_SITE_URL?.replace(/\/+$/, "") || "https://becertifiedtoday.com";
    const encorOrigin = getEncorAppBaseUrl();
    const renew = body.renew === true;
    const email = typeof body.email === "string" ? body.email.trim().toLowerCase() : undefined;

    const session = await stripe.checkout.sessions.create({
      mode: "payment",
      line_items: [
        {
          price: process.env.STRIPE_PRICE_ID_ENCOR,
          quantity: 1,
        },
      ],
      customer_email: email || undefined,
      success_url: `${encorOrigin}/checkout-success.html?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${marketingOrigin}/checkout-cancelled.html`,
      metadata: {
        product: ALLOWED_PRODUCT,
        access_days: String(ACCESS_WINDOW_DAYS),
        renew: renew ? "true" : "false",
      },
      payment_intent_data: {
        metadata: {
          product: ALLOWED_PRODUCT,
          access_days: String(ACCESS_WINDOW_DAYS),
        },
      },
    });

    await trackEvent("checkout_started");
    return res.status(200).json({ url: session.url });
  } catch (error) {
    console.error("create-checkout-session failed:", error);
    return res.status(500).json({ error: "Failed to create checkout session" });
  }
}
