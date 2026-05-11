/**
 * GET /api/verify-checkout-session?session_id=cs_…
 * Confirms checkout completion for the success landing page (paid or $0 after coupon).
 *
 * Env: STRIPE_SECRET_KEY
 */
import Stripe from "stripe";
import { getStripeSecretKey } from "./stripe-secret-key.js";

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

export default async function handler(req, res) {
  if (req.method !== "GET") {
    res.setHeader("Allow", "GET");
    return res.status(405).json({ ok: false, error: "Method not allowed" });
  }

  const sk = getStripeSecretKey(process.env.STRIPE_SECRET_KEY);
  if (!sk.secret) {
    return res.status(503).json({ ok: false, error: sk.error });
  }

  const sessionId = sessionIdFromReq(req);

  if (!sessionId || typeof sessionId !== "string") {
    return res.status(400).json({ ok: false, error: "Missing session_id" });
  }

  const stripe = new Stripe(sk.secret);

  try {
    const session = await stripe.checkout.sessions.retrieve(sessionId, {
      expand: ["payment_intent"],
    });

    const paid =
      session.payment_status === "paid" ||
      session.payment_status === "no_payment_required";
    const productId = session.metadata?.productId || null;

    return res.status(200).json({
      ok: paid,
      payment_status: session.payment_status,
      productId,
      customer_email: session.customer_details?.email || null,
    });
  } catch (e) {
    console.error("verify-checkout-session:", e.message);
    return res.status(400).json({ ok: false, error: "Invalid or expired session" });
  }
}
