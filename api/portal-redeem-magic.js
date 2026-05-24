/**
 * POST /api/portal-redeem-magic
 * Body: { "token": "<JWT>" }
 *
 * Legacy paths rewrite here via vercel.json:
 *   /api/ccna-portal-redeem-magic
 *   /api/encor-portal-redeem-magic
 */
import Stripe from "stripe";
import { getStripeSecretKey } from "../server-lib/stripe-secret-key.js";
import {
  checkoutSessionIsPaid,
  inferProductIdFromCheckoutSession,
  isCcnaPortalProduct,
  isEncorPortalProduct,
  portalAccessExpiresAtMs,
} from "../server-lib/ccna-portal-stripe.js";
import { verifyPortalMagicJwt } from "../server-lib/ccna-portal-magic-jwt.js";

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

function resolveTrackFromAud(aud) {
  if (aud === "encor-portal-access") return "encor";
  if (aud === "ccna-portal-30d" || aud === "ccna-portal-access") return "ccna";
  return "";
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "Method not allowed" });
  }

  const sk = getStripeSecretKey(process.env.STRIPE_SECRET_KEY);
  const secret = (process.env.PORTAL_MAGIC_LINK_SECRET || "").trim();

  if (!sk.secret) {
    return res.status(503).json({ ok: false, error: sk.error });
  }
  if (!secret) {
    return res.status(503).json({
      ok: false,
      error: "Magic links are not configured",
      hint: "Set PORTAL_MAGIC_LINK_SECRET on Vercel.",
    });
  }

  const body = readJsonBody(req);
  const token = typeof body.token === "string" ? body.token.trim() : "";

  if (!token) {
    return res.status(400).json({ ok: false, error: "Missing token" });
  }

  const payload = verifyPortalMagicJwt(token, secret);
  const nowSec = Math.floor(Date.now() / 1000);
  const track = resolveTrackFromAud(payload?.aud);

  if (
    !payload ||
    !track ||
    typeof payload.cs !== "string" ||
    payload.cs.indexOf("cs_") !== 0 ||
    typeof payload.exp !== "number" ||
    payload.exp <= nowSec
  ) {
    return res.status(401).json({ ok: false, error: "Invalid or expired link" });
  }

  const stripe = new Stripe(sk.secret);
  const isProduct = track === "encor" ? isEncorPortalProduct : isCcnaPortalProduct;

  try {
    const session = await stripe.checkout.sessions.retrieve(payload.cs, {
      expand: ["payment_intent", "line_items.data.price"],
    });

    if (!checkoutSessionIsPaid(session)) {
      return res.status(403).json({ ok: false, error: "Payment is no longer active for this purchase" });
    }

    const productId = inferProductIdFromCheckoutSession(session);
    if (!isProduct(productId)) {
      return res.status(403).json({ ok: false, error: "This link is not valid for portal access" });
    }

    const accessExpiresAt = portalAccessExpiresAtMs(session, productId);
    if (accessExpiresAt <= Date.now()) {
      return res.status(403).json({ ok: false, error: "Access window has ended" });
    }

    return res.status(200).json({
      ok: true,
      productId,
      accessExpiresAt,
      checkoutSessionId: session.id,
      customer_email: session.customer_details?.email || null,
    });
  } catch (e) {
    console.error(`portal-redeem-magic (${track}):`, e.message);
    return res.status(400).json({ ok: false, error: "Could not verify purchase" });
  }
}
