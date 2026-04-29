import { getStripe } from "../_lib/stripe.js";
import { ACCESS_WINDOW_DAYS, requireEnv } from "../_lib/config.js";
import { grantAccess, revokeAccessByCustomerId } from "../_lib/access-store.js";
import { createMagicLinkToken } from "../_lib/magic-link.js";
import { getVerifyBaseUrl, sendMagicLinkEmail } from "../_lib/mailer.js";
import { kvSetNxEx } from "../_lib/kv.js";

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

  let whSecret;
  try {
    whSecret = requireEnv("STRIPE_WEBHOOK_SECRET");
  } catch (error) {
    console.error(error.message);
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

  let stripe;
  try {
    stripe = getStripe();
  } catch (error) {
    console.error(error.message);
    return res.status(500).send("Server misconfiguration");
  }

  let event;
  try {
    event = stripe.webhooks.constructEvent(buf, sig, whSecret);
  } catch (err) {
    console.error("Webhook signature verification failed:", err.message);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  const idempotencyKey = `encor:webhook:event:${event.id}`;
  const firstProcess = await kvSetNxEx(idempotencyKey, "1", 60 * 60 * 24 * 14);
  if (!firstProcess) {
    return res.status(200).json({ received: true, duplicate: true });
  }

  try {
    if (event.type === "checkout.session.completed") {
      const session = event.data.object;
      if (session.payment_status !== "paid") {
        return res.status(200).json({ received: true, ignored: "not_paid" });
      }

      const fullSession = await stripe.checkout.sessions.retrieve(session.id, {
        expand: ["customer"],
      });
      const customer = fullSession.customer;
      const stripeCustomerId = typeof customer === "string" ? customer : customer?.id || null;
      const email =
        fullSession.customer_details?.email ||
        fullSession.customer_email ||
        (typeof customer === "object" && customer && !customer.deleted ? customer.email : null);

      if (!email) {
        throw new Error(`No customer email on checkout.session.completed: ${session.id}`);
      }

      const record = await grantAccess({
        email,
        stripeCustomerId,
        checkoutSessionId: fullSession.id,
        accessDays: Number(fullSession.metadata?.access_days || ACCESS_WINDOW_DAYS),
      });

      const magicToken = await createMagicLinkToken(email);
      const verifyBaseUrl = getVerifyBaseUrl();
      const magicLink = `${verifyBaseUrl}/api/auth/magic-link/verify?token=${encodeURIComponent(magicToken)}`;
      await sendMagicLinkEmail({
        toEmail: email,
        url: magicLink,
      });

      console.log("Access granted after checkout", {
        email: record.email,
        sessionId: record.checkout_session_id,
        stripeCustomerId: record.stripe_customer_id,
        accessExpiresAt: record.access_expires_at,
      });
    } else if (event.type === "charge.refunded") {
      const charge = event.data.object;
      await revokeAccessByCustomerId(charge.customer || null);
      console.log("Access revoked after charge.refunded", {
        chargeId: charge.id,
        customerId: charge.customer || null,
      });
    } else if (event.type === "payment_intent.payment_failed") {
      const paymentIntent = event.data.object;
      console.warn("Payment failed for intent", {
        paymentIntentId: paymentIntent.id,
        customerId: paymentIntent.customer || null,
      });
    }
  } catch (error) {
    console.error("Webhook handler error:", error);
    return res.status(500).send("Handler error");
  }

  return res.status(200).json({ received: true });
}
