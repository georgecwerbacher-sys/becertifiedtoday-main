import { normalizeEmail, requireEnv } from "../_lib/config.js";
import { getAccessRecord } from "../_lib/access-store.js";
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
  if (!email) {
    return res.status(400).json({ error: "Missing email in request body" });
  }

  try {
    const record = await getAccessRecord(email);
    if (!record) {
      return res.status(404).json({ error: "No access record found for email" });
    }

    if (!record.access_expires_at || Date.parse(record.access_expires_at) <= Date.now()) {
      return res.status(400).json({ error: "Access expired; renew is required before sending link" });
    }

    const token = await createMagicLinkToken(email);
    const baseUrl = getAppBaseUrl();
    const magicLink = `${baseUrl}/api/auth/magic-link/verify?token=${encodeURIComponent(token)}`;

    await sendMagicLinkEmail({
      toEmail: email,
      url: magicLink,
    });

    return res.status(200).json({
      sent: true,
      email,
      access_expires_at: record.access_expires_at,
    });
  } catch (error) {
    console.error("Failed sending admin magic link:", error);
    return res.status(500).json({ error: "Failed to send magic link" });
  }
}
