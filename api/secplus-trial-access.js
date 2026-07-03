/**
 * POST /api/secplus-trial-access
 * Body: { "email": "you@example.com" }
 *
 * Email-only 3-day Security+ portal trial (no Stripe Checkout).
 */
import Stripe from "stripe";
import { getStripeSecretKey } from "../server-lib/stripe-secret-key.js";
import { normalizePublicSiteUrl } from "../server-lib/normalize-public-site-url.js";
import { signPortalMagicJwt } from "../server-lib/ccna-portal-magic-jwt.js";
import { sendSecplusTrial3dEmail } from "../server-lib/ccna-portal-resend.js";
import { grantSecplusTrialAccess } from "../server-lib/secplus-trial-access.js";
import { appendMarketingLeadCsv, buildLeadCsvRow } from "../server-lib/append-marketing-lead-csv.js";

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

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "Method not allowed" });
  }

  const sk = getStripeSecretKey(process.env.STRIPE_SECRET_KEY);
  const jwtSecret = (process.env.PORTAL_MAGIC_LINK_SECRET || "").trim();
  const site = normalizePublicSiteUrl(process.env.PUBLIC_SITE_URL);

  if (!sk.secret) {
    return res.status(503).json({ ok: false, error: sk.error });
  }
  if (!jwtSecret) {
    return res.status(503).json({
      ok: false,
      error: "Trial access is not configured",
      hint: "Set PORTAL_MAGIC_LINK_SECRET on Vercel.",
    });
  }
  if (!site) {
    return res.status(503).json({
      ok: false,
      error: "PUBLIC_SITE_URL is not configured",
    });
  }

  const body = readJsonBody(req);
  const stripe = new Stripe(sk.secret);
  const grant = await grantSecplusTrialAccess(stripe, body.email);

  if (!grant.ok) {
    const status =
      grant.reason === "invalid-email"
        ? 400
        : grant.reason === "paid-portal-active" || grant.reason === "trial-used"
          ? 200
          : 400;
    return res.status(status).json({
      ok: false,
      reason: grant.reason,
      message: grant.message,
    });
  }

  const expSec = Math.floor(grant.accessExpiresAtMs / 1000);
  const token = signPortalMagicJwt(
    {
      aud: "secplus-portal-access",
      kind: "secplus-trial",
      email: grant.email,
      productId: grant.productId,
      exp: expSec,
    },
    jwtSecret
  );

  const magicUrl = `${site}/COMP_TIA_SEC+/secplus-portal-magic.html#t=${encodeURIComponent(token)}`;

  void appendMarketingLeadCsv(
    buildLeadCsvRow(body, {
      event: grant.alreadyActive ? "secplus_trial_3d_return" : "secplus_trial_3d_grant",
      email: grant.email,
      magnet: "secplus-trial-3d",
      product: "secplus",
      source: body.source || "secplus-trial-3d",
    })
  ).catch((err) => {
    console.warn("[secplus-trial] lead csv:", err?.message || err);
  });

  let emailSent = false;
  try {
    emailSent = await sendSecplusTrial3dEmail({ to: grant.email, magicUrl });
  } catch (err) {
    console.warn("[secplus-trial] email:", err?.message || err);
  }

  return res.status(200).json({
    ok: true,
    productId: grant.productId,
    accessExpiresAt: grant.accessExpiresAtMs,
    accessDays: 3,
    alreadyActive: !!grant.alreadyActive,
    emailSent,
    magicUrl,
    message: grant.alreadyActive
      ? "Your free 3-day access is still active on this email. Opening the portal on this device now."
      : emailSent
        ? "Your free 3-day access is active on this browser. We also emailed a link for other devices."
        : "Your free 3-day access is active on this browser. Save this tab or use the portal link we returned if you switch devices.",
  });
}
