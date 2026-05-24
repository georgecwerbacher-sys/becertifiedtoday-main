/**
 * POST /api/portal-users-report
 * Authorization: Bearer <admin JWT>
 *
 * Lists CCNA 30-day portal purchasers from Stripe Customer metadata (email + access window).
 * Env: STRIPE_SECRET_KEY, ADMIN_ANALYTICS_JWT_SECRET
 */
import Stripe from "stripe";
import { verifyAnalyticsAdminToken } from "../server-lib/analytics-admin-jwt.js";
import {
  enrichPortalRowsWithCheckout,
  listPortalCustomersFromStripe,
} from "../server-lib/ccna-portal-customers.js";
import { getStripeSecretKey } from "../server-lib/stripe-secret-key.js";

function readJsonBody(req) {
  try {
    if (req.body != null) {
      if (typeof req.body === "object" && !Buffer.isBuffer(req.body)) return req.body;
      if (typeof req.body === "string" && req.body.length) return JSON.parse(req.body);
    }
  } catch (_) {}
  return {};
}

function bearerToken(req) {
  const h = req.headers.authorization || req.headers.Authorization || "";
  const m = /^Bearer\s+(.+)$/i.exec(String(h).trim());
  return m ? m[1].trim() : "";
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "Method not allowed" });
  }

  const jwtSecret = (process.env.ADMIN_ANALYTICS_JWT_SECRET || "").trim();
  const token = bearerToken(req) || (readJsonBody(req).token || "");

  if (!jwtSecret) {
    return res.status(503).json({
      ok: false,
      error: "Admin analytics is not configured",
    });
  }

  if (!verifyAnalyticsAdminToken(token, jwtSecret)) {
    return res.status(401).json({ ok: false, error: "Unauthorized" });
  }

  const sk = getStripeSecretKey(process.env.STRIPE_SECRET_KEY);
  if (!sk.secret) {
    return res.status(503).json({
      ok: false,
      error: "Stripe is not configured",
      hint: sk.error || "Set STRIPE_SECRET_KEY on Vercel.",
    });
  }

  const body = readJsonBody(req);
  const verifyCheckout = body.verifyCheckout === true;
  const stripe = new Stripe(sk.secret);

  try {
    const listed = await listPortalCustomersFromStripe(stripe);
    let active = listed.active;
    let expired = listed.expired;

    if (verifyCheckout && active.length > 0 && active.length <= 40) {
      active = await enrichPortalRowsWithCheckout(stripe, active);
    }

    return res.status(200).json({
      ok: true,
      active,
      expired,
      counts: {
        active: active.length,
        expired: expired.length,
        total: listed.totalWithPortalMetadata,
      },
      customersScanned: listed.customersScanned,
      scanTruncated: listed.scanTruncated,
      fetchedAt: new Date().toISOString(),
      note:
        "Emails come from Stripe checkout. This shows who has paid portal access, not who is browsing right now.",
    });
  } catch (err) {
    const message = err && err.message ? String(err.message) : "Stripe API error";
    return res.status(502).json({ ok: false, error: message });
  }
}
