import { consumeMagicLinkToken, createSessionToken } from "../../_lib/magic-link.js";
import { getAccessRecord } from "../../_lib/access-store.js";

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
    const email = await consumeMagicLinkToken(token);
    if (!email) {
      return res.status(400).send("Magic link invalid or expired");
    }

    const access = await getAccessRecord(email);
    if (!access || Date.parse(access.access_expires_at) <= Date.now()) {
      return res.redirect(302, "/encor-renew.html");
    }

    const sessionToken = await createSessionToken(email);
    if (!sessionToken) {
      return res.status(500).send("Could not create access session");
    }

    const maxAge = 60 * 60 * 24 * 30;
    res.setHeader(
      "Set-Cookie",
      `encor_access_token=${sessionToken}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${maxAge}`
    );
    return res.redirect(302, "/");
  } catch (error) {
    console.error("Magic link verification failed:", error);
    return res.status(500).send("Could not verify magic link");
  }
}
