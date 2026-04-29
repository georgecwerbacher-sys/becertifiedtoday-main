import { ACCESS_WINDOW_DAYS, normalizeEmail, requireEnv } from "../_lib/config.js";
import { grantAccess } from "../_lib/access-store.js";
import { createMagicLinkToken } from "../_lib/magic-link.js";
import { getAppBaseUrl, sendMagicLinkEmail } from "../_lib/mailer.js";

function isAuthorized(req) {
  const expected = process.env.ADMIN_ACCESS_TOKEN;
  if (!expected) {
    throw new Error("Missing required env var: ADMIN_ACCESS_TOKEN");
  }
  const provided = req.headers["x-admin-token"];
  return typeof provided === "string" && provided === expected;
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method Not Allowed" });
  }

  try {
    requireEnv("ADMIN_ACCESS_TOKEN");
    requireEnv("ENCOR_APP_URL");
  } catch (error) {
    console.error(error.message);
    return res.status(500).json({ error: "Admin endpoint not configured" });
  }

  if (!isAuthorized(req)) {
    return res.status(401).json({ error: "Unauthorized" });
  }

  const body = req.body && typeof req.body === "object" ? req.body : {};
  const email = normalizeEmail(body.email);
  const requestedDays = Number(body.days);
  const sendMagicLink = body.send_magic_link !== false;
  const days = Number.isFinite(requestedDays) && requestedDays > 0 ? Math.floor(requestedDays) : ACCESS_WINDOW_DAYS;

  if (!email) {
    return res.status(400).json({ error: "Missing email in request body" });
  }

  try {
    const record = await grantAccess({
      email,
      stripeCustomerId: null,
      checkoutSessionId: null,
      accessDays: days,
    });

    let magicLinkSent = false;
    if (sendMagicLink) {
      const token = await createMagicLinkToken(email);
      const baseUrl = getAppBaseUrl();
      const magicLink = `${baseUrl}/api/auth/magic-link/verify?token=${encodeURIComponent(token)}`;
      await sendMagicLinkEmail({ toEmail: email, url: magicLink });
      magicLinkSent = true;
    }

    return res.status(200).json({
      granted: true,
      email,
      access_expires_at: record.access_expires_at,
      days,
      magic_link_sent: magicLinkSent,
    });
  } catch (error) {
    console.error("Failed granting admin access:", error);
    return res.status(500).json({ error: "Failed to grant access" });
  }
}
