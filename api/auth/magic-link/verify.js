import { consumeMagicLinkToken, createSessionToken } from "../../_lib/magic-link.js";
import { getAccessRecord } from "../../_lib/access-store.js";
import { trackEvent } from "../../_lib/analytics.js";
import { sessionCookieDomainDirective } from "../../_lib/cookie-domain.js";
import { createOpaqueToken, kvSetEx } from "../../_lib/kv.js";
import { getEncorAppBaseUrl } from "../../_lib/encor-app-url.js";

function bounceKey(id) {
  return `encor:bounce:${id}`;
}

/** *.vercel.app cannot receive Domain=.becertifiedtoday.com cookies; bounce via claim on ENCOR origin. */
function encorHostNeedsCookieBounce(redirectBaseUrl) {
  try {
    const urlStr = redirectBaseUrl.includes("://") ? redirectBaseUrl : `https://${redirectBaseUrl}`;
    const h = new URL(urlStr).hostname.toLowerCase();
    return h.endsWith(".vercel.app");
  } catch {
    return false;
  }
}

export default async function handler(req, res) {
  if (req.method !== "GET") {
    res.setHeader("Allow", "GET");
    return res.status(405).send("Method Not Allowed");
  }

  const token = typeof req.query?.token === "string" ? req.query.token : "";
  if (!token) {
    return res.status(400).send("Missing token");
  }

  try {
    const redirectBaseUrl = getEncorAppBaseUrl();

    const email = await consumeMagicLinkToken(token);
    if (!email) {
      return res.status(400).send("Magic link invalid or expired");
    }

    const access = await getAccessRecord(email);
    if (!access || Date.parse(access.access_expires_at) <= Date.now()) {
      const renewBaseUrl = String(process.env.PUBLIC_SITE_URL || "https://becertifiedtoday.com").replace(/\/+$/, "");
      return res.redirect(302, `${renewBaseUrl}/encor-renew.html`);
    }

    const sessionToken = await createSessionToken(email);
    if (!sessionToken) {
      return res.status(500).send("Could not create access session");
    }

    await trackEvent("magic_link_verified");

    if (encorHostNeedsCookieBounce(redirectBaseUrl)) {
      const bounceId = createOpaqueToken();
      await kvSetEx(bounceKey(bounceId), 300, sessionToken);
      const claimUrl = `${redirectBaseUrl}/api/auth/encor-claim-bounce?b=${encodeURIComponent(bounceId)}`;
      return res.redirect(302, claimUrl);
    }

    const maxAge = 60 * 60 * 24 * 30;
    const domainPart = sessionCookieDomainDirective();
    res.setHeader(
      "Set-Cookie",
      `encor_access_token=${sessionToken}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${maxAge}${domainPart}`
    );
    return res.redirect(302, `${redirectBaseUrl}/`);
  } catch (error) {
    console.error("Magic link verification failed:", error);
    return res.status(500).send("Could not verify magic link");
  }
}
