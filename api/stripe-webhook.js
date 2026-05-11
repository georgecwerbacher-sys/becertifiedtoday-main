/**
 * POST /api/stripe-webhook
 * Configure in Stripe Dashboard → Developers → Webhooks → endpoint URL: https://<domain>/api/stripe-webhook
 * Events: checkout.session.completed (add others as needed).
 *
 * Env: STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET (whsec_…)
 */
import Stripe from "stripe";
import getRawBody from "raw-body";
import { getStripeSecretKey } from "./stripe-secret-key.js";

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).end("Method not allowed");
  }

  const sk = getStripeSecretKey(process.env.STRIPE_SECRET_KEY);
  const webhookSecret = (process.env.STRIPE_WEBHOOK_SECRET || "").trim();

  if (!sk.secret || !webhookSecret) {
    return res.status(503).json({ error: "Webhook not configured" });
  }

  const sig = req.headers["stripe-signature"];
  if (!sig) {
    return res.status(400).json({ error: "Missing stripe-signature" });
  }

  let buf;
  try {
    buf = await getRawBody(req);
  } catch (e) {
    console.error("raw body:", e);
    return res.status(400).json({ error: "Could not read body" });
  }

  const stripe = new Stripe(sk.secret);
  let event;

  try {
    event = stripe.webhooks.constructEvent(buf, sig, webhookSecret);
  } catch (err) {
    console.error("Webhook signature verification failed:", err.message);
    return res.status(400).json({ error: "Invalid signature" });
  }

  switch (event.type) {
    case "checkout.session.completed": {
      const session = event.data.object;
      const productId = session.metadata?.productId;
      console.info(
        "[stripe] checkout.session.completed",
        session.id,
        "productId=",
        productId,
        "payment_status=",
        session.payment_status
      );
      // TODO: grant entitlement (DB, signed JWT cookie, or email link) before launching the 120-minute test.
      break;
    }
    default:
      console.info("[stripe] unhandled event", event.type);
  }

  return res.status(200).json({ received: true });
}
