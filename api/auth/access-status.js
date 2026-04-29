import { readSessionEmail } from "../_lib/magic-link.js";
import { getAccessRecord } from "../_lib/access-store.js";

export default async function handler(req, res) {
  if (req.method !== "GET") {
    res.setHeader("Allow", "GET");
    return res.status(405).json({ error: "Method Not Allowed" });
  }

  try {
    const token = req.cookies?.encor_access_token || null;
    if (!token) {
      return res.status(200).json({ has_access: false });
    }

    const email = await readSessionEmail(token);
    if (!email) {
      return res.status(200).json({ has_access: false });
    }

    const record = await getAccessRecord(email);
    if (!record || !record.access_expires_at || Date.parse(record.access_expires_at) <= Date.now()) {
      return res.status(200).json({ has_access: false });
    }

    return res.status(200).json({ has_access: true });
  } catch (error) {
    console.error("Failed checking access status:", error);
    return res.status(200).json({ has_access: false });
  }
}
