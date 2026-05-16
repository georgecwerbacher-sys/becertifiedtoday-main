/**
 * GET /api/ccna-portal-30d-payment-link
 * Returns the Stripe Payment Link URL for CCNA 30-day portal access.
 *
 * Set STRIPE_PAYMENT_LINK_CCNA_PORTAL_30D on Vercel (full https://buy.stripe.com/… URL).
 * If unset, falls back to the default link shipped with the site.
 */
const DEFAULT_PAYMENT_LINK = "https://buy.stripe.com/14A7sK58xccT4CI8ZCc3m03";

export default async function handler(req, res) {
  if (req.method !== "GET") {
    res.setHeader("Allow", "GET");
    return res.status(405).json({ error: "Method not allowed" });
  }

  const fromEnv = (process.env.STRIPE_PAYMENT_LINK_CCNA_PORTAL_30D || "").trim();
  const url = fromEnv || DEFAULT_PAYMENT_LINK;

  if (!/^https:\/\/buy\.stripe\.com\//i.test(url)) {
    console.error("ccna-portal-30d-payment-link: invalid URL configured");
    return res.status(503).json({
      error: "Payment link is misconfigured",
      hint: "STRIPE_PAYMENT_LINK_CCNA_PORTAL_30D must be a https://buy.stripe.com/… URL.",
    });
  }

  res.setHeader("Cache-Control", "private, max-age=300");
  return res.status(200).json({ url });
}
