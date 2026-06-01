/**
 * POST /api/stripe-webhook
 * Stripe Dashboard → Developers → Webhooks → Add endpoint.
 *
 * The endpoint URL must be the deployment that owns this codebase (same project as CCNA/ENCOR Checkout), e.g.
 *   https://becertifiedtoday.com/api/stripe-webhook
 * If you run multiple deployments against one Stripe account, use a separate webhook entry + signing secret per site.
 *
 * Events: checkout.session.completed (add others as needed).
 *
 * Env: STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET (whsec_… — copy from the endpoint that matches THIS deployment)
 *
 * CCNA portal access: on completed checkout we attach metadata to a Stripe Customer (see server-lib)
 * and optionally email a magic link via Resend (RESEND_API_KEY, PORTAL_MAGIC_LINK_SECRET, PUBLIC_SITE_URL).
 */
import Stripe from "stripe";
import getRawBody from "raw-body";
import { getStripeSecretKey } from "../server-lib/stripe-secret-key.js";
import { checkoutSessionIsPaid, inferProductIdFromCheckoutSession } from "../server-lib/ccna-portal-stripe.js";
import {
  CHECKOUT_SESSION_EXPAND,
  fulfillPortalCheckoutSession,
  trackForPortalProductId,
} from "../server-lib/portal-checkout-fulfillment.js";

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
      try {
        let session = event.data.object;

        if (!checkoutSessionIsPaid(session)) {
          console.info("[stripe] checkout.session.completed unpaid skip", session.id, session.payment_status);
          break;
        }

        if (!session.line_items?.data?.length) {
          session = await stripe.checkout.sessions.retrieve(session.id, {
            expand: CHECKOUT_SESSION_EXPAND,
          });
        }

        const productId = inferProductIdFromCheckoutSession(session);
        const track = trackForPortalProductId(productId);
        console.info("[stripe] checkout.session.completed", session.id, "productId=", productId, "track=", track);

        if (!track) {
          break;
        }

        const result = await fulfillPortalCheckoutSession(stripe, session, { sendEmail: true });
        if (result.ok && !result.emailSent) {
          console.warn(
            `[${track}-portal] webhook magic email not sent:`,
            result.emailSkippedReason || "unknown",
            { sessionId: session.id, hasEmail: !!result.email }
          );
        } else if (result.ok && result.emailSent) {
          console.info(`[${track}-portal] webhook magic email sent`, session.id);
        }
      } catch (err) {
        console.error("[stripe] checkout.session.completed portal handling:", err.message);
      }
      break;
    }
    default:
      console.info("[stripe] unhandled event", event.type);
  }

  return res.status(200).json({ received: true });
}
