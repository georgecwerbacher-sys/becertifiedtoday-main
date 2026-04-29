import { kvDel, kvGet } from "../_lib/kv.js";
import { readSessionEmail } from "../_lib/magic-link.js";
import { getEncorAppBaseUrl } from "../_lib/encor-app-url.js";

function bounceKey(id) {
  return `encor:bounce:${id}`;
}

function renewUrl() {
  const pub = String(process.env.PUBLIC_SITE_URL || "https://becertifiedtoday.com").replace(/\/+$/, "");
  return `${pub}/encor-renew.html`;
}

export default async function handler(req, res) {
  if (req.method !== "GET") {
    res.setHeader("Allow", "GET");
    return res.status(405).send("Method Not Allowed");
  }

  const b = typeof req.query?.b === "string" ? req.query.b.trim() : "";
  if (!b) {
    return res.status(400).send("Missing bounce token");
  }

  const sessionToken = await kvGet(bounceKey(b));
  await kvDel(bounceKey(b));

  if (!sessionToken) {
    return res.redirect(302, renewUrl());
  }

  const email = await readSessionEmail(sessionToken);
  if (!email) {
    return res.redirect(302, renewUrl());
  }

  const maxAge = 60 * 60 * 24 * 30;
  res.setHeader(
    "Set-Cookie",
    `encor_access_token=${sessionToken}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${maxAge}`
  );

  return res.redirect(302, `${getEncorAppBaseUrl()}/`);
}
