/**
 * GET /api/verify-checkout-session?session_id=cs_…
 * Confirms checkout completion for the success landing page (paid or $0 after coupon).
 *
 * POST /api/verify-checkout-session
 * Body: { "session_id": "cs_…", "send_magic_link": true, "track": "secplus"|"encor"|"ccna" (optional) }
 * Upserts portal metadata and emails a magic link (backup when Stripe webhooks do not run).
 *
 * Env: STRIPE_SECRET_KEY, RESEND_API_KEY, PORTAL_MAGIC_LINK_SECRET, PUBLIC_SITE_URL (for POST email)
 */
import Stripe from "stripe";
import { getStripeSecretKey } from "../server-lib/stripe-secret-key.js";
import {
  checkoutSessionIsPaid,
  inferProductIdFromCheckoutSession,
  portalAccessExpiresAtMs,
} from "../server-lib/ccna-portal-stripe.js";
import {
  fulfillPortalCheckoutSession,
  retrievePaidCheckoutSession,
} from "../server-lib/portal-checkout-fulfillment.js";

function readJsonBody(req) {
  try {
    if (req.body != null) {
      if (typeof req.body === "object" && !Buffer.isBuffer(req.body)) {
        return req.body;
      }
      if (typeof req.body === "string" && req.body.length) {
        return JSON.parse(req.body);
      }
    }
  } catch (_) {}
  return {};
}

function sessionIdFromReq(req) {
  try {
    const host = req.headers?.host || "localhost";
    const url = new URL(req.url || "/", `https://${host}`);
    const q = url.searchParams.get("session_id");
    if (q) return q;
  } catch (_) {}
  if (req.query && typeof req.query.session_id === "string") return req.query.session_id;
  return null;
}

function normalizeTrack(raw) {
  const t = String(raw || "")
    .trim()
    .toLowerCase();
  return t === "ccna" || t === "encor" || t === "secplus" ? t : "";
}

async function handleGet(req, res, stripe, sessionId) {
  const session = await stripe.checkout.sessions.retrieve(sessionId, {
    expand: [
      "payment_intent",
      "payment_link",
      "line_items.data.price",
      "line_items.data.price.product",
    ],
  });

  const paid = checkoutSessionIsPaid(session);
  const productId = inferProductIdFromCheckoutSession(session);
  const accessExpiresAt = paid ? portalAccessExpiresAtMs(session, productId) : null;

  return res.status(200).json({
    ok: paid,
    payment_status: session.payment_status,
    productId,
    amount_subtotal: session.amount_subtotal,
    amount_total: session.amount_total,
    customer_email: session.customer_details?.email || null,
    accessExpiresAt,
    accessExpired:
      paid && typeof accessExpiresAt === "number" ? Date.now() > accessExpiresAt : false,
  });
}

async function handlePostMagicLink(req, res, stripe) {
  const body = readJsonBody(req);
  const sessionId = typeof body.session_id === "string" ? body.session_id.trim() : "";
  const track = normalizeTrack(body.track);

  if (!sessionId || sessionId.indexOf("cs_") !== 0) {
    return res.status(400).json({ ok: false, error: "Missing or invalid session_id" });
  }
  if (!body.send_magic_link) {
    return res.status(400).json({ ok: false, error: "Set send_magic_link to true" });
  }

  const session = await retrievePaidCheckoutSession(stripe, sessionId);
  const result = await fulfillPortalCheckoutSession(stripe, session, {
    sendEmail: true,
    expectedTrack: track || undefined,
  });

  if (!result.ok) {
    const status =
      result.error === "unpaid" || result.error === "access_expired" || result.error === "not_portal_product"
        ? 403
        : 400;
    return res.status(status).json({ ok: false, ...result });
  }

  let message = null;
  if (result.emailSent && result.email) {
    message =
      "We emailed a portal link to " +
      result.email +
      ". Check spam if it does not arrive within a few minutes.";
  } else if (result.emailSkippedReason === "no_checkout_email") {
    message =
      "Payment recorded, but Stripe did not include an email on this checkout. Use Restore access with your session ID.";
  } else if (
    result.emailSkippedReason === "resend_error" ||
    result.emailSkippedReason === "resend_rejected" ||
    result.emailSkippedReason === "resend_not_configured"
  ) {
    message =
      "Portal access is active, but we could not send the email right now. Use Email me a portal link or Restore access with your checkout session ID.";
  }

  return res.status(200).json({
    ok: true,
    productId: result.productId,
    track: result.track,
    emailSent: result.emailSent,
    email: result.email || null,
    emailSkippedReason: result.emailSkippedReason,
    message,
  });
}

export default async function handler(req, res) {
  const sk = getStripeSecretKey(process.env.STRIPE_SECRET_KEY);
  if (!sk.secret) {
    return res.status(503).json({ ok: false, error: sk.error });
  }

  const stripe = new Stripe(sk.secret);

  if (req.method === "POST") {
    try {
      return await handlePostMagicLink(req, res, stripe);
    } catch (e) {
      console.error("verify-checkout-session POST:", e.message);
      return res.status(400).json({ ok: false, error: "Could not verify checkout session" });
    }
  }

  if (req.method !== "GET") {
    res.setHeader("Allow", "GET, POST");
    return res.status(405).json({ ok: false, error: "Method not allowed" });
  }

  const sessionId = sessionIdFromReq(req);
  if (!sessionId || typeof sessionId !== "string") {
    return res.status(400).json({ ok: false, error: "Missing session_id" });
  }

  try {
    return await handleGet(req, res, stripe, sessionId);
  } catch (e) {
    console.error("verify-checkout-session:", e.message);
    return res.status(400).json({ ok: false, error: "Invalid or expired session" });
  }
}
