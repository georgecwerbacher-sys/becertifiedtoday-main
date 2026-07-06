/**
 * POST /api/portal-users-report
 * Authorization: Bearer <admin JWT>
 *
 * Lists Security+ portal purchasers from Stripe Customer metadata.
 * Env: STRIPE_SECRET_KEY, ADMIN_ANALYTICS_JWT_SECRET
 */
import Stripe from "stripe";
import { verifyAnalyticsAdminToken } from "../server-lib/analytics-admin-jwt.js";
import { filterPortalSubscriberRows } from "../server-lib/analytics-internal.js";
import { isSecplusPortalProduct } from "../server-lib/ccna-portal-stripe.js";
import { filterRowsFromUtcStart } from "../server-lib/google-analytics.js";
import {
  aggregateMagicLinkRequestsReport,
  enrichPortalBlockWithMagicLinkCounts,
  magicLinkCountsByEmail,
  readPortalMagicLinkRequests,
} from "../server-lib/portal-magic-link-requests.js";
import {
  enrichPortalRowsWithCheckout,
  listAllPortalSubscribersFromStripe,
} from "../server-lib/portal-subscribers-stripe.js";
import { buildStripePurchasesReport } from "../server-lib/stripe-purchases-report.js";
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

function filterProductBlock(block) {
  return {
    active: filterPortalSubscriberRows(block.active),
    expired: filterPortalSubscriberRows(block.expired),
    counts: {
      active: 0,
      expired: 0,
      total: 0,
    },
  };
}

function applyCounts(block) {
  block.counts = {
    active: block.active.length,
    expired: block.expired.length,
    total: block.active.length + block.expired.length,
  };
  return block;
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
  const rangePreset =
    typeof body.range === "string" && body.range.trim() ? body.range.trim() : "7d";
  const stripe = new Stripe(sk.secret);

  try {
    const [listed, purchasesInRange, magicLinkAllRows] = await Promise.all([
      listAllPortalSubscribersFromStripe(stripe),
      buildStripePurchasesReport(stripe, rangePreset).catch((err) => ({
        error: err?.message || "Stripe purchases report failed",
      })),
      readPortalMagicLinkRequests().catch((err) => ({
        error: err?.message || "Magic link requests read failed",
      })),
    ]);

    let magicLinkResets = null;
    let magicLinkResetsError = null;
    let magicLinkEmailCounts = null;
    if (magicLinkAllRows && !magicLinkAllRows.error) {
      const inRange = filterRowsFromUtcStart(magicLinkAllRows, rangePreset);
      magicLinkResets = aggregateMagicLinkRequestsReport(inRange);
      magicLinkEmailCounts = magicLinkCountsByEmail(inRange);
    } else {
      magicLinkResetsError = magicLinkAllRows?.error || "Magic link requests unavailable";
    }

    let secplus = applyCounts(filterProductBlock(listed.secplus));

    if (magicLinkEmailCounts) {
      enrichPortalBlockWithMagicLinkCounts(secplus, magicLinkEmailCounts);
    }

    if (verifyCheckout) {
      if (secplus.active.length > 0 && secplus.active.length <= 40) {
        secplus.active = await enrichPortalRowsWithCheckout(stripe, secplus.active, {
          isPortalProduct: isSecplusPortalProduct,
          notProductNote: "not security+ portal access",
        });
        applyCounts(secplus);
      }
    }

    return res.status(200).json({
      ok: true,
      secplus,
      purchasesInRange:
        purchasesInRange && !purchasesInRange.error ? purchasesInRange : null,
      purchasesInRangeError: purchasesInRange?.error || null,
      magicLinkResets,
      magicLinkResetsError,
      active: secplus.active,
      expired: secplus.expired,
      counts: secplus.counts,
      customersScanned: listed.customersScanned,
      scanTruncated: listed.scanTruncated,
      fetchedAt: new Date().toISOString(),
      note:
        "Security+ portal emails from Stripe checkout (10-day or 30-day access). One row per email.",
    });
  } catch (err) {
    const message = err && err.message ? String(err.message) : "Stripe API error";
    return res.status(502).json({ ok: false, error: message });
  }
}
