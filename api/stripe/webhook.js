/**
 * POST /api/stripe/webhook
 *
 * Env (Vercel → Project → Settings → Environment Variables):
 *   STRIPE_WEBHOOK_SECRET   whsec_...   (Dashboard → Developers → Webhooks → your endpoint → Signing secret)
 *   STRIPE_SECRET_KEY       sk_live_... or sk_test_...  (required — used for SDK + session retrieve)
 *
 * Dashboard: add endpoint URL https://YOUR_DOMAIN/api/stripe/webhook
 * Events: checkout.session.completed (one-time Checkout / Payment Links / Buy Button)
 */

import Stripe from "stripe";

function getStripe() {
  const key = process.env.STRIPE_SECRET_KEY;
  if (!key) {
    return null;
  }
  return new Stripe(key);
}

async function readRawBody(req) {
  const chunks = [];
  for await (const chunk of req) {
    chunks.push(chunk);
  }
  return Buffer.concat(chunks);
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).send("Method Not Allowed");
  }

  const whSecret = process.env.STRIPE_WEBHOOK_SECRET;
  if (!whSecret) {
    console.error("STRIPE_WEBHOOK_SECRET is not set");
    return res.status(500).send("Webhook not configured");
  }

  const sigRaw = req.headers["stripe-signature"];
  const sig = Array.isArray(sigRaw) ? sigRaw[0] : sigRaw;
  if (!sig || typeof sig !== "string") {
    return res.status(400).send("Missing stripe-signature header");
  }

  let buf;
  try {
    buf = await readRawBody(req);
  } catch (e) {
    console.error("Failed to read body:", e);
    return res.status(400).send("Could not read body");
  }

  const stripe = getStripe();
  if (!stripe) {
    console.error("STRIPE_SECRET_KEY is not set");
    return res.status(500).send("Server misconfiguration");
  }

  let event;
  try {
    event = stripe.webhooks.constructEvent(buf, sig, whSecret);
  } catch (err) {
    console.error("Webhook signature verification failed:", err.message);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  try {
    if (event.type === "checkout.session.completed") {
      const session = event.data.object;

      let email =
        session.customer_details?.email ||
        session.customer_email ||
        null;

      if (!email && session.id) {
        try {
          const full = await stripe.checkout.sessions.retrieve(session.id, {
            expand: ["customer"],
          });
          email =
            full.customer_details?.email ||
            full.customer_email ||
            (typeof full.customer === "object" && full.customer && !full.customer.deleted
              ? full.customer.email
              : null);
        } catch (e) {
          console.error("Could not retrieve session for email:", e.message);
        }
      }

      const accessDays = Number(session.metadata?.access_days || 30);
      const productKey = session.metadata?.product || "encor";

      const accessUntil = new Date(Date.now() + accessDays * 24 * 60 * 60 * 1000).toISOString();

      console.log(
        JSON.stringify({
          event: "checkout.session.completed",
          sessionId: session.id,
          email,
          productKey,
          accessDays,
          accessUntil,
          amountTotal: session.amount_total,
          currency: session.currency,
          metadata: session.metadata,
        })
      );

      // TODO: upsert access_grants — email + productKey + access_until (see Membership/Checklist.md Phase 4)
    }
  } catch (e) {
    console.error("Handler error:", e);
    return res.status(500).send("Handler error");
  }

  return res.status(200).json({ received: true });
}
