/**
 * POST /api/ccna-portal-request-magic-link
 * Body: { "email": "you@example.com" }
 *
 * If Stripe shows an active CCNA portal purchase for this email, sends a fresh magic link via Resend.
 * Uses Stripe Customer metadata written by checkout.session.completed webhook, with fallback lookup
 * when metadata was never written (e.g. webhook missed or purchase predates portal email setup).
 *
 * Env: STRIPE_SECRET_KEY, PORTAL_MAGIC_LINK_SECRET, PUBLIC_SITE_URL,
 *      RESEND_API_KEY, RESEND_FROM (optional)
 */
import Stripe from "stripe";
import { getStripeSecretKey } from "./stripe-secret-key.js";
import { normalizePublicSiteUrl } from "./normalize-public-site-url.js";
import { upsertCustomerPortalMetadata } from "../server-lib/ccna-portal-stripe.js";
import { findActivePortalSessionForEmail } from "../server-lib/ccna-portal-customers.js";
import { signPortalMagicJwt } from "../server-lib/ccna-portal-magic-jwt.js";
import { sendCcnaPortalMagicEmail } from "../server-lib/ccna-portal-resend.js";

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

function normalizeEmail(raw) {
  const s = typeof raw === "string" ? raw.trim().toLowerCase() : "";
  if (!s || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s)) return "";
  return s;
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "Method not allowed" });
  }

  const sk = getStripeSecretKey(process.env.STRIPE_SECRET_KEY);
  const jwtSecret = (process.env.PORTAL_MAGIC_LINK_SECRET || "").trim();
  const site = normalizePublicSiteUrl(process.env.PUBLIC_SITE_URL);
  const resendKey = (process.env.RESEND_API_KEY || "").trim();

  if (!sk.secret) {
    return res.status(503).json({ ok: false, error: sk.error });
  }
  if (!jwtSecret) {
    return res.status(503).json({
      ok: false,
      error: "Magic links are not configured",
      hint: "Set PORTAL_MAGIC_LINK_SECRET on Vercel.",
    });
  }
  if (!site) {
    return res.status(503).json({
      ok: false,
      error: "PUBLIC_SITE_URL is not configured",
    });
  }
  if (!resendKey) {
    return res.status(503).json({
      ok: false,
      error: "Email delivery is not configured",
      hint: "Set RESEND_API_KEY and RESEND_FROM on Vercel, then redeploy.",
    });
  }

  const body = readJsonBody(req);
  const email = normalizeEmail(body.email);

  /** Same response whether or not we sent mail — avoids email enumeration. */
  const generic =
    "If this email has active CCNA portal access on file, we sent a login link. Check spam and wait a minute before trying again.";

  if (!email) {
    return res.status(400).json({ ok: false, error: "Enter a valid email address." });
  }

  const stripe = new Stripe(sk.secret);

  try {
    const found = await findActivePortalSessionForEmail(stripe, email);
    if (!found) {
      console.info("[ccna-portal] magic link request: no active portal purchase for email");
      return res.status(200).json({ ok: true, message: generic });
    }

    const { session, accessExpiresAtMs } = found;

    await upsertCustomerPortalMetadata(stripe, session, accessExpiresAtMs);

    const token = signPortalMagicJwt(
      {
        aud: "ccna-portal-access",
        cs: session.id,
        exp: Math.floor(accessExpiresAtMs / 1000),
      },
      jwtSecret
    );

    const magicUrl = `${site}/CCNA-Study/ccna-portal-magic.html#t=${encodeURIComponent(token)}`;
    const sent = await sendCcnaPortalMagicEmail({ to: email, magicUrl });

    if (!sent) {
      console.error("[ccna-portal] Resend did not accept magic-link email");
    } else {
      console.info("[ccna-portal] magic link email sent for active portal purchase");
    }

    return res.status(200).json({ ok: true, message: generic });
  } catch (e) {
    console.error("ccna-portal-request-magic-link:", e.message);
    return res.status(200).json({ ok: true, message: generic });
  }
}
