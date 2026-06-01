/**
 * Shared portal checkout fulfillment: Stripe Customer metadata + optional magic-link email.
 * Used by stripe-webhook and checkout-success backup API.
 */

import { normalizePublicSiteUrl } from "./normalize-public-site-url.js";
import {
  checkoutSessionIsPaid,
  inferProductIdFromCheckoutSession,
  isCcnaPortalProduct,
  isEncorPortalProduct,
  isSecplusPortalProduct,
  portalAccessExpiresAtMs,
  upsertCustomerPortalMetadata,
  upsertEncorCustomerPortalMetadata,
  upsertSecplusCustomerPortalMetadata,
} from "./ccna-portal-stripe.js";
import { signPortalMagicJwt } from "./ccna-portal-magic-jwt.js";
import {
  sendCcnaPortalMagicEmail,
  sendEncorPortalMagicEmail,
  sendSecplusPortalMagicEmail,
} from "./ccna-portal-resend.js";

export const CHECKOUT_SESSION_EXPAND = [
  "payment_intent",
  "payment_link",
  "line_items.data.price",
  "line_items.data.price.product",
];

export function trackForPortalProductId(productId) {
  if (isEncorPortalProduct(productId)) return "encor";
  if (isSecplusPortalProduct(productId)) return "secplus";
  if (isCcnaPortalProduct(productId)) return "ccna";
  return "";
}

function magicPathForTrack(track) {
  if (track === "encor") return "/CCNP-ENCOR-Study/encor-portal-magic.html";
  if (track === "secplus") return "/COMP_TIA_SEC+/secplus-portal-magic.html";
  return "/CCNA-Study/ccna-portal-magic.html";
}

function audForTrack(track) {
  if (track === "encor") return "encor-portal-access";
  if (track === "secplus") return "secplus-portal-access";
  return "ccna-portal-access";
}

async function sendMagicEmailForTrack(track, { to, magicUrl }) {
  if (track === "encor") return sendEncorPortalMagicEmail({ to, magicUrl });
  if (track === "secplus") return sendSecplusPortalMagicEmail({ to, magicUrl });
  return sendCcnaPortalMagicEmail({ to, magicUrl });
}

/**
 * @param {import('stripe').Stripe} stripe
 * @param {import('stripe').Stripe.Checkout.Session} session
 * @param {{ sendEmail?: boolean, expectedTrack?: string }} [opts]
 */
export async function fulfillPortalCheckoutSession(stripe, session, opts = {}) {
  const sendEmail = opts.sendEmail !== false;
  const expectedTrack = opts.expectedTrack ? String(opts.expectedTrack).trim().toLowerCase() : "";

  if (!checkoutSessionIsPaid(session)) {
    return { ok: false, error: "unpaid", payment_status: session.payment_status };
  }

  const productId = inferProductIdFromCheckoutSession(session);
  const track = trackForPortalProductId(productId);
  if (!track) {
    return { ok: false, error: "not_portal_product", productId };
  }
  if (expectedTrack && track !== expectedTrack) {
    return { ok: false, error: "track_mismatch", productId, track, expectedTrack };
  }

  const accessExpiresAtMs = portalAccessExpiresAtMs(session, productId);
  if (accessExpiresAtMs <= Date.now()) {
    return { ok: false, error: "access_expired", productId, track, accessExpiresAtMs };
  }

  if (track === "encor") {
    await upsertEncorCustomerPortalMetadata(stripe, session, accessExpiresAtMs);
  } else if (track === "secplus") {
    await upsertSecplusCustomerPortalMetadata(stripe, session, accessExpiresAtMs);
  } else {
    await upsertCustomerPortalMetadata(stripe, session, accessExpiresAtMs);
  }

  const email = (session.customer_details?.email || "").trim().toLowerCase();
  const jwtSecret = (process.env.PORTAL_MAGIC_LINK_SECRET || "").trim();
  const site = normalizePublicSiteUrl(process.env.PUBLIC_SITE_URL);
  const resendKey = (process.env.RESEND_API_KEY || "").trim();

  let emailSent = false;
  let emailSkippedReason = null;

  if (!sendEmail) {
    emailSkippedReason = "disabled";
  } else if (!resendKey) {
    emailSkippedReason = "resend_not_configured";
  } else if (!jwtSecret) {
    emailSkippedReason = "magic_secret_not_configured";
  } else if (!site) {
    emailSkippedReason = "site_url_not_configured";
  } else if (!email) {
    emailSkippedReason = "no_checkout_email";
  } else {
    const token = signPortalMagicJwt(
      {
        aud: audForTrack(track),
        cs: session.id,
        exp: Math.floor(accessExpiresAtMs / 1000),
      },
      jwtSecret
    );
    const magicUrl = `${site}${magicPathForTrack(track)}#t=${encodeURIComponent(token)}`;
    try {
      emailSent = await sendMagicEmailForTrack(track, { to: email, magicUrl });
      if (!emailSent) emailSkippedReason = "resend_rejected";
    } catch (err) {
      emailSkippedReason = "resend_error";
      console.error(`[${track}-portal] magic email after checkout:`, err.message);
    }
  }

  return {
    ok: true,
    productId,
    track,
    accessExpiresAtMs,
    email,
    emailSent,
    emailSkippedReason,
  };
}

/**
 * @param {import('stripe').Stripe} stripe
 * @param {string} sessionId
 */
export async function retrievePaidCheckoutSession(stripe, sessionId) {
  return stripe.checkout.sessions.retrieve(sessionId, { expand: CHECKOUT_SESSION_EXPAND });
}
