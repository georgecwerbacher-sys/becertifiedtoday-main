/**
 * POST /api/stripe-webhook
 * Stripe Dashboard → Developers → Webhooks → Add endpoint.
 *
 * The endpoint URL must be the deployment that owns this codebase (same project as CCNA Checkout), e.g.
 *   https://becertifiedtoday.com/api/stripe-webhook
 * A different Vercel app (e.g. becertifiedtoday-encor.vercel.app) has its own /api/stripe-webhook — use a
 * separate Stripe webhook entry + signing secret per deployment if you use one Stripe account for multiple sites.
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
import { getStripeSecretKey } from "./stripe-secret-key.js";
import { normalizePublicSiteUrl } from "./normalize-public-site-url.js";
import {
  checkoutSessionIsPaid,
  inferProductIdFromCheckoutSession,
  isCcnaPortalProduct,
  portalAccessExpiresAtMs,
  upsertCustomerPortalMetadata,
} from "../server-lib/ccna-portal-stripe.js";
import { signPortalMagicJwt } from "../server-lib/ccna-portal-magic-jwt.js";
import { sendCcnaPortalMagicEmail } from "../server-lib/ccna-portal-resend.js";

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
            expand: ["payment_intent", "line_items.data.price"],
          });
        }

        const productId = inferProductIdFromCheckoutSession(session);
        console.info("[stripe] checkout.session.completed", session.id, "productId=", productId);

        if (!isCcnaPortalProduct(productId)) {
          break;
        }

        const accessExpiresAtMs = portalAccessExpiresAtMs(session, productId);
        await upsertCustomerPortalMetadata(stripe, session, accessExpiresAtMs);

        const jwtSecret = (process.env.PORTAL_MAGIC_LINK_SECRET || "").trim();
        const site = normalizePublicSiteUrl(process.env.PUBLIC_SITE_URL);
        const email = (session.customer_details?.email || "").trim().toLowerCase();

        if (jwtSecret && site && email) {
          const token = signPortalMagicJwt(
            {
              aud: "ccna-portal-access",
              cs: session.id,
              exp: Math.floor(accessExpiresAtMs / 1000),
            },
            jwtSecret
          );
          const magicUrl = `${site}/CCNA-Study/ccna-portal-magic.html#t=${encodeURIComponent(token)}`;
          await sendCcnaPortalMagicEmail({ to: email, magicUrl });
        } else {
          console.warn(
            "[ccna-portal] Magic email skipped (set PORTAL_MAGIC_LINK_SECRET + PUBLIC_SITE_URL + collect email at checkout)",
            { hasJwt: !!jwtSecret, hasSite: !!site, hasEmail: !!email }
          );
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
