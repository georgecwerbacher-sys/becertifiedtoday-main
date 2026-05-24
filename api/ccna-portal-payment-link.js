/**
 * GET /api/ccna-portal-payment-link?plan=10d|30d
 *
 * Legacy paths rewrite here via vercel.json:
 *   /api/ccna-portal-10d-payment-link
 *   /api/ccna-portal-30d-payment-link
 */
const PLANS = {
  "10d": {
    envKey: "STRIPE_PAYMENT_LINK_CCNA_PORTAL_10D",
    defaultUrl: "https://buy.stripe.com/00wcN458x6Szglq6Ruc3m04",
  },
  "30d": {
    envKey: "STRIPE_PAYMENT_LINK_CCNA_PORTAL_30D",
    defaultUrl: "https://buy.stripe.com/14A7sK58xccT4CI8ZCc3m03",
  },
};

function resolvePlan(req) {
  const q = String(req.query?.plan || "")
    .trim()
    .toLowerCase();
  if (q === "10d" || q === "30d") return q;
  const path = String(req.url || "");
  if (path.includes("10d")) return "10d";
  if (path.includes("30d")) return "30d";
  return "";
}

export default async function handler(req, res) {
  if (req.method !== "GET") {
    res.setHeader("Allow", "GET");
    return res.status(405).json({ error: "Method not allowed" });
  }

  const plan = resolvePlan(req);
  if (!plan) {
    return res.status(400).json({ error: "Missing plan (10d or 30d)" });
  }

  const cfg = PLANS[plan];
  const fromEnv = (process.env[cfg.envKey] || "").trim();
  const url = fromEnv || cfg.defaultUrl;

  if (!/^https:\/\/buy\.stripe\.com\//i.test(url)) {
    console.error(`ccna-portal-payment-link (${plan}): invalid URL configured`);
    return res.status(503).json({
      error: "Payment link is misconfigured",
      hint: `${cfg.envKey} must be a https://buy.stripe.com/... URL.`,
    });
  }

  res.setHeader("Cache-Control", "private, max-age=300");
  return res.status(200).json({ url });
}
