import { normalizeEmail, requireEnv } from "../_lib/config.js";
import { getAccessRecord, isRefundedEmail } from "../_lib/access-store.js";

function isAuthorized(req) {
  const expected = process.env.ADMIN_ACCESS_TOKEN;
  if (!expected) {
    throw new Error("Missing required env var: ADMIN_ACCESS_TOKEN");
  }
  const provided = req.headers["x-admin-token"];
  return typeof provided === "string" && provided === expected;
}

export default async function handler(req, res) {
  if (req.method !== "GET") {
    res.setHeader("Allow", "GET");
    return res.status(405).json({ error: "Method Not Allowed" });
  }

  try {
    requireEnv("ADMIN_ACCESS_TOKEN");
  } catch (error) {
    console.error(error.message);
    return res.status(500).json({ error: "Admin endpoint not configured" });
  }

  if (!isAuthorized(req)) {
    return res.status(401).json({ error: "Unauthorized" });
  }

  const email = normalizeEmail(req.query?.email);
  if (!email) {
    return res.status(400).json({ error: "Missing email query param" });
  }

  try {
    const [record, refunded] = await Promise.all([
      getAccessRecord(email),
      isRefundedEmail(email),
    ]);

    return res.status(200).json({
      email,
      found: Boolean(record),
      refunded,
      record: record || null,
    });
  } catch (error) {
    console.error("Failed loading admin access record:", error);
    return res.status(500).json({ error: "Failed loading access record" });
  }
}
