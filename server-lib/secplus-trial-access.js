/**
 * Security+ 3-day free trial (email only — no Stripe Checkout).
 * Grants stored on Stripe Customer metadata for serverless restore / magic links.
 */
import { findActiveSecplusPortalSessionForEmail } from "./secplus-portal-customers.js";

export const SECPLUS_TRIAL_PRODUCT_ID = "secplus-portal-3d";
export const SECPLUS_TRIAL_DAYS = 3;

/** Set SECPLUS_TRIAL_3D_ENABLED=1 on Vercel to re-open the email-only 3-day promo. */
export function isSecplusTrial3dPromoEnabled() {
  return (process.env.SECPLUS_TRIAL_3D_ENABLED || "").trim() === "1";
}

export function normalizeTrialEmail(raw) {
  const s = typeof raw === "string" ? raw.trim().toLowerCase() : "";
  if (!s || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s)) return "";
  if (s.length > 254) return "";
  return s;
}

function trialExpiresMsFromCustomer(customer) {
  const meta = customer?.metadata || {};
  const exp = parseInt(meta.secplus_trial_3d_expires_ms || "0", 10);
  return Number.isFinite(exp) && exp > 0 ? exp : 0;
}

function trialWasUsed(customer) {
  return (customer?.metadata?.secplus_trial_3d_used || "") === "1";
}

/**
 * @param {import('stripe').Stripe} stripe
 * @param {string} email
 */
export async function getSecplusTrialAccessForEmail(stripe, email) {
  const normalized = normalizeTrialEmail(email);
  if (!normalized) return null;

  const customers = await stripe.customers.list({ email: normalized, limit: 10 });
  let bestExp = 0;
  for (let i = 0; i < customers.data.length; i++) {
    const exp = trialExpiresMsFromCustomer(customers.data[i]);
    if (exp > Date.now() && exp > bestExp) bestExp = exp;
  }
  if (!bestExp) return null;

  return {
    email: normalized,
    accessExpiresAtMs: bestExp,
    productId: SECPLUS_TRIAL_PRODUCT_ID,
  };
}

/**
 * @param {import('stripe').Stripe} stripe
 * @param {string} email
 * @returns {Promise<
 *   | { ok: true, email: string, accessExpiresAtMs: number, productId: string, alreadyActive?: boolean, renewed?: boolean }
 *   | { ok: false, reason: string, message: string }
 * >}
 */
export async function grantSecplusTrialAccess(stripe, email) {
  const normalized = normalizeTrialEmail(email);
  if (!normalized) {
    return { ok: false, reason: "invalid-email", message: "Enter a valid email address." };
  }

  const paid = await findActiveSecplusPortalSessionForEmail(stripe, normalized);
  if (paid) {
    return {
      ok: false,
      reason: "paid-portal-active",
      message:
        "This email already has active Security+ library access from a purchase. Open the training portal on this browser, or use Email me a portal link to sign in on another device.",
    };
  }

  const activeTrial = await getSecplusTrialAccessForEmail(stripe, normalized);
  if (activeTrial) {
    return { ok: true, ...activeTrial, alreadyActive: true };
  }

  if (!isSecplusTrial3dPromoEnabled()) {
    return {
      ok: false,
      reason: "promo-ended",
      message:
        "The free 3-day Security+ promotion has ended. Purchase 10-day or 30-day access from Security+ home, or try the free samples.",
    };
  }

  const customers = await stripe.customers.list({ email: normalized, limit: 10 });
  for (let i = 0; i < customers.data.length; i++) {
    if (trialWasUsed(customers.data[i])) {
      return {
        ok: false,
        reason: "trial-used",
        message:
          "This email already used the free 3-day Security+ access. Purchase 10-day or 30-day access from Security+ home if you want the full library again.",
      };
    }
  }

  const accessExpiresAtMs = Date.now() + SECPLUS_TRIAL_DAYS * 86400000;
  let customerId = customers.data[0]?.id || null;
  if (!customerId) {
    const created = await stripe.customers.create({
      email: normalized,
      metadata: { secplus_trial_customer: "1" },
    });
    customerId = created.id;
  }

  await stripe.customers.update(customerId, {
    metadata: {
      secplus_trial_customer: "1",
      secplus_trial_3d_used: "1",
      secplus_trial_3d_expires_ms: String(accessExpiresAtMs),
      secplus_trial_3d_granted_at: String(Date.now()),
      secplus_trial_3d_product_id: SECPLUS_TRIAL_PRODUCT_ID,
    },
  });

  return {
    ok: true,
    email: normalized,
    accessExpiresAtMs,
    productId: SECPLUS_TRIAL_PRODUCT_ID,
    renewed: false,
  };
}
