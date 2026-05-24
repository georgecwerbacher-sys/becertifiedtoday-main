/**
 * Normalize and validate STRIPE_SECRET_KEY for Stripe SDK calls.
 * Common mistake: pasting the webhook signing secret (whsec_…) as the API key.
 *
 * @param {string | undefined} raw
 * @returns {{ secret: string } | { secret: null, error: string }}
 */
export function getStripeSecretKey(raw) {
  const secret = (raw || "").trim();
  if (!secret) {
    return { secret: null, error: "Missing STRIPE_SECRET_KEY" };
  }
  if (secret.startsWith("whsec_")) {
    return {
      secret: null,
      error:
        "STRIPE_SECRET_KEY is set to a webhook signing secret (whsec_…). Use sk_test_… or sk_live_… from Stripe Dashboard → Developers → API keys. Put whsec_… in STRIPE_WEBHOOK_SECRET only.",
    };
  }
  if (secret.startsWith("mk_")) {
    return {
      secret: null,
      error:
        "Stripe does not use mk_ for API authentication. Use the Secret key from Stripe Dashboard → Developers → API keys: sk_test_… / sk_live_… (or a Restricted key rk_test_… / rk_live_… with Checkout allowed).",
    };
  }
  if (secret.startsWith("pk_")) {
    return {
      secret: null,
      error:
        "STRIPE_SECRET_KEY cannot be a publishable key (pk_…). Use the Secret key (sk_…) from Developers → API keys.",
    };
  }
  const ok =
    secret.startsWith("sk_test_") ||
    secret.startsWith("sk_live_") ||
    secret.startsWith("rk_test_") ||
    secret.startsWith("rk_live_");
  if (!ok) {
    return {
      secret: null,
      error:
        "STRIPE_SECRET_KEY must be sk_test_, sk_live_, rk_test_, or rk_live_ (from Stripe → Developers → API keys).",
    };
  }
  return { secret };
}
