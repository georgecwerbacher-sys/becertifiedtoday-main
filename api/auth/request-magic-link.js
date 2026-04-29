import { normalizeEmail } from "../_lib/config.js";
import { getAccessRecord } from "../_lib/access-store.js";
import { createMagicLinkToken } from "../_lib/magic-link.js";
import { getVerifyBaseUrl, sendMagicLinkEmail } from "../_lib/mailer.js";
import { kvSetNxEx } from "../_lib/kv.js";
import { trackEvent } from "../_lib/analytics.js";

function clientIp(req) {
  const forwarded = req.headers["x-forwarded-for"];
  if (typeof forwarded === "string" && forwarded.length > 0) {
    return forwarded.split(",")[0].trim();
  }
  return "unknown";
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method Not Allowed" });
  }

  const body = req.body && typeof req.body === "object" ? req.body : {};
  const email = normalizeEmail(body.email);

  // Always return generic success to avoid leaking account existence.
  const successResponse = { ok: true, message: "If access is active, a new magic link will be sent." };

  if (!email) {
    return res.status(200).json(successResponse);
  }

  try {
    const ip = clientIp(req);
    const emailRateKey = `encor:ratelimit:magic-email:${email}`;
    const ipRateKey = `encor:ratelimit:magic-ip:${ip}`;
    const allowedEmail = await kvSetNxEx(emailRateKey, "1", 60);
    const allowedIp = await kvSetNxEx(ipRateKey, "1", 30);
    if (!allowedEmail || !allowedIp) {
      return res.status(200).json(successResponse);
    }

    const access = await getAccessRecord(email);
    if (!access || !access.access_expires_at || Date.parse(access.access_expires_at) <= Date.now()) {
      return res.status(200).json(successResponse);
    }

    const token = await createMagicLinkToken(email);
    const verifyBaseUrl = getVerifyBaseUrl();
    const magicLink = `${verifyBaseUrl}/api/auth/magic-link/verify?token=${encodeURIComponent(token)}`;
    await sendMagicLinkEmail({ toEmail: email, url: magicLink });
    await trackEvent("magic_link_requested");
  } catch (error) {
    console.error("request-magic-link failed:", error);
  }

  return res.status(200).json(successResponse);
}
