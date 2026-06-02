/**
 * POST /api/portal-request-magic-link?track=ccna|encor|secplus
 * Body: { "email": "you@example.com", "track": "ccna"|"encor" (optional if query set) }
 *
 * Legacy paths rewrite here via vercel.json:
 *   /api/ccna-portal-request-magic-link
 *   /api/encor-portal-request-magic-link
 */
import Stripe from "stripe";
import { getStripeSecretKey } from "../server-lib/stripe-secret-key.js";
import { normalizePublicSiteUrl } from "../server-lib/normalize-public-site-url.js";
import {
  upsertCustomerPortalMetadata,
  upsertEncorCustomerPortalMetadata,
  upsertSecplusCustomerPortalMetadata,
} from "../server-lib/ccna-portal-stripe.js";
import {
  findActivePortalSessionForEmail,
  getCcnaPurchaseHintsForEmail,
} from "../server-lib/ccna-portal-customers.js";
import { findActiveEncorPortalSessionForEmail } from "../server-lib/encor-portal-customers.js";
import {
  findActiveSecplusPortalSessionForEmail,
  getSecplusPurchaseHintsForEmail,
} from "../server-lib/secplus-portal-customers.js";
import { signPortalMagicJwt } from "../server-lib/ccna-portal-magic-jwt.js";
import {
  sendCcnaPortalMagicEmail,
  sendEncorPortalMagicEmail,
  sendSecplusPortalMagicEmail,
} from "../server-lib/ccna-portal-resend.js";

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

function resolveTrack(req, body) {
  const q = String(req.query?.track || "")
    .trim()
    .toLowerCase();
  if (q === "ccna" || q === "encor" || q === "secplus") return q;
  const b = String(body?.track || "")
    .trim()
    .toLowerCase();
  if (b === "ccna" || b === "encor" || b === "secplus") return b;
  return "";
}

const TRACK_CONFIG = {
  ccna: {
    logTag: "ccna-portal",
    generic:
      "If this email has active CCNA portal access on file, we sent a login link. Check spam and wait a minute before trying again.",
    aud: "ccna-portal-access",
    magicPath: "/CCNA-Study/ccna-portal-magic.html",
    findSession: findActivePortalSessionForEmail,
    upsertMetadata: upsertCustomerPortalMetadata,
    sendEmail: sendCcnaPortalMagicEmail,
  },
  encor: {
    logTag: "encor-portal",
    generic:
      "If this email has active ENCOR portal access on file, we sent a login link. Check spam and wait a minute before trying again.",
    aud: "encor-portal-access",
    magicPath: "/CCNP-ENCOR-Study/encor-portal-magic.html",
    findSession: findActiveEncorPortalSessionForEmail,
    upsertMetadata: upsertEncorCustomerPortalMetadata,
    sendEmail: sendEncorPortalMagicEmail,
  },
  secplus: {
    logTag: "secplus-portal",
    generic:
      "If this email has active Security+ portal access on file, we sent a login link. Check spam and wait a minute before trying again.",
    aud: "secplus-portal-access",
    magicPath: "/COMP_TIA_SEC+/secplus-portal-magic.html",
    findSession: findActiveSecplusPortalSessionForEmail,
    upsertMetadata: upsertSecplusCustomerPortalMetadata,
    sendEmail: sendSecplusPortalMagicEmail,
  },
};

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "Method not allowed" });
  }

  const body = readJsonBody(req);
  const track = resolveTrack(req, body);
  if (!track) {
    return res.status(400).json({ ok: false, error: "Missing track (ccna, encor, or secplus)" });
  }

  const cfg = TRACK_CONFIG[track];
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

  const email = normalizeEmail(body.email);
  if (!email) {
    return res.status(400).json({ ok: false, error: "Enter a valid email address." });
  }

  const stripe = new Stripe(sk.secret);

  try {
    const found = await cfg.findSession(stripe, email);
    if (!found) {
      console.info(`[${cfg.logTag}] magic link request: no active portal purchase for email`);
      if (track === "ccna") {
        const hints = await getCcnaPurchaseHintsForEmail(stripe, email);
        if (hints.timedExamOnly) {
          return res.status(200).json({
            ok: true,
            sent: false,
            found: false,
            reason: "test-simulation-only",
            message:
              "We found an active $9.99 timed exam purchase for this email, not 10- or 30-day library access. Portal link emails only apply to library passes. Use Restore access with your checkout session ID (cs_…) from your Stripe receipt to unlock the timed exam on this device, or purchase 10-day / 30-day access from CCNA home.",
          });
        }
        if (hints.portalExpired) {
          return res.status(200).json({
            ok: true,
            sent: false,
            found: false,
            reason: "portal-expired",
            message:
              "CCNA library access for this email has expired. Purchase a new 10-day or 30-day pass from CCNA home if you want the training portal again.",
          });
        }
      }
      if (track === "secplus") {
        const hints = await getSecplusPurchaseHintsForEmail(stripe, email);
        if (hints.timedExamOnly) {
          return res.status(200).json({
            ok: true,
            sent: false,
            found: false,
            reason: "test-simulation-only",
            message:
              "We found an active $9.99 timed exam purchase for this email, not 10- or 30-day library access. The training portal link email only applies to all-access passes. Use Restore access with your checkout session ID (cs_…) from your Stripe receipt to unlock the timed exam on this device, or purchase 10-day / 30-day access from Security+ home.",
          });
        }
        if (hints.portalExpired) {
          return res.status(200).json({
            ok: true,
            sent: false,
            found: false,
            reason: "portal-expired",
            message:
              "Security+ library access for this email has expired. Purchase a new 10-day or 30-day pass from Security+ home if you want the training portal again.",
          });
        }
      }
      const noPortalMessage =
        track === "ccna"
          ? "No active CCNA library pass was found for that email. Use the exact address from your Stripe receipt. If you only bought the one-time timed exam, use Restore access with your checkout session ID (cs_…) instead. After checkout, open the training portal once so we can link your purchase for email restore."
          : track === "encor"
            ? "No active ENCOR library pass was found for that email. Use the same address you entered at Stripe checkout for a 10-day or 30-day purchase. If you only bought the one-time timed exam, use Restore access with your checkout session ID (cs_…) instead."
            : cfg.generic;
      return res.status(200).json({
        ok: true,
        sent: false,
        found: false,
        reason: "no-active-portal",
        message: noPortalMessage,
      });
    }

    const { session, accessExpiresAtMs } = found;

    await cfg.upsertMetadata(stripe, session, accessExpiresAtMs);

    const token = signPortalMagicJwt(
      {
        aud: cfg.aud,
        cs: session.id,
        exp: Math.floor(accessExpiresAtMs / 1000),
      },
      jwtSecret
    );

    const magicUrl = `${site}${cfg.magicPath}#t=${encodeURIComponent(token)}`;
    const sent = await cfg.sendEmail({ to: email, magicUrl });

    if (!sent) {
      console.error(`[${cfg.logTag}] Resend did not accept magic-link email`);
      return res.status(200).json({
        ok: true,
        found: true,
        sent: false,
        message:
          "We found active access for that email but could not deliver the message. Use Restore access with your Stripe checkout session ID (cs_…) from your receipt, or try again in a few minutes.",
      });
    }

    console.info(`[${cfg.logTag}] magic link email sent for active portal purchase`);
    return res.status(200).json({
      ok: true,
      sent: true,
      found: true,
      message: "We sent a login link to that email. Check your inbox and spam folder, then open the link on the device where you want to study.",
    });
  } catch (e) {
    console.error(`portal-request-magic-link (${track}):`, e.message);
    return res.status(500).json({
      ok: false,
      sent: false,
      error: "Something went wrong while sending the link. Try again in a few minutes or use Restore access with your Stripe checkout session ID.",
    });
  }
}
