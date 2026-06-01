/**
 * POST /api/portal-users-report
 * Authorization: Bearer <admin JWT>
 *
 * Lists CCNA, ENCOR, and Security+ portal purchasers from Stripe Customer metadata.
 * Env: STRIPE_SECRET_KEY, ADMIN_ANALYTICS_JWT_SECRET
 */
import Stripe from "stripe";
import { verifyAnalyticsAdminToken } from "../server-lib/analytics-admin-jwt.js";
import { enrichPortalRowsWithCheckout as enrichCcnaRows } from "../server-lib/ccna-portal-customers.js";
import { getStripeSecretKey } from "../server-lib/stripe-secret-key.js";
import { filterPortalSubscriberRows } from "../server-lib/analytics-internal.js";
import {
  enrichPortalRowsWithCheckout,
  listAllPortalSubscribersFromStripe,
} from "../server-lib/portal-subscribers-stripe.js";
import {
  isEncorPortalProduct,
  isSecplusPortalProduct,
} from "../server-lib/ccna-portal-stripe.js";

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
  const stripe = new Stripe(sk.secret);

  try {
    const listed = await listAllPortalSubscribersFromStripe(stripe);

    let ccna = applyCounts(filterProductBlock(listed.ccna));
    let encor = applyCounts(filterProductBlock(listed.encor));
    let secplus = applyCounts(filterProductBlock(listed.secplus));

    if (verifyCheckout) {
      const enrichIfSmall = async (block, enrichFn) => {
        if (block.active.length > 0 && block.active.length <= 40) {
          block.active = await enrichFn(stripe, block.active);
          applyCounts(block);
        }
      };
      await enrichIfSmall(ccna, enrichCcnaRows);
      await enrichIfSmall(encor, (s, rows) =>
        enrichPortalRowsWithCheckout(s, rows, {
          isPortalProduct: isEncorPortalProduct,
          notProductNote: "not encor portal access",
        })
      );
      await enrichIfSmall(secplus, (s, rows) =>
        enrichPortalRowsWithCheckout(s, rows, {
          isPortalProduct: isSecplusPortalProduct,
          notProductNote: "not security+ portal access",
        })
      );
    }

    return res.status(200).json({
      ok: true,
      ccna,
      encor,
      secplus,
      active: ccna.active,
      expired: ccna.expired,
      counts: ccna.counts,
      customersScanned: listed.customersScanned,
      scanTruncated: listed.scanTruncated,
      fetchedAt: new Date().toISOString(),
      note:
        "Emails from Stripe checkout (10-day or 30-day portal access). Not live browsing — use GA4 Realtime for anonymous visitors.",
    });
  } catch (err) {
    const message = err && err.message ? String(err.message) : "Stripe API error";
    return res.status(502).json({ ok: false, error: message });
  }
}
