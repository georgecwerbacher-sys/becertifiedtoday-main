/**
 * POST /api/account-logout
 * Clears learner session cookie.
 */
import { logoutLearnerRequest } from "../server-lib/learner-auth.js";

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "Method not allowed" });
  }

  try {
    const clear = await logoutLearnerRequest(req);
    res.setHeader("Set-Cookie", clear);
  } catch (e) {
    console.error("[account-logout]", e.message);
  }

  return res.status(200).json({ ok: true });
}
