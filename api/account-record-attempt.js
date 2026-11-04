/**
 * POST /api/account-record-attempt
 * Body: { attempts: [{ track, mode, item_id, domain, correct, meta? }] }
 */
import { learnerFromRequest } from "../server-lib/learner-auth.js";
import {
  insertPracticeAttempts,
  postgresConfigured,
} from "../server-lib/learner-db.js";

function readJsonBody(req) {
  try {
    if (req.body != null) {
      if (typeof req.body === "object" && !Buffer.isBuffer(req.body)) return req.body;
      if (typeof req.body === "string" && req.body.length) return JSON.parse(req.body);
    }
  } catch (_) {}
  return {};
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "Method not allowed" });
  }

  if (!postgresConfigured()) {
    return res.status(503).json({ ok: false, error: "Account storage is not configured" });
  }

  try {
    const learner = await learnerFromRequest(req);
    if (!learner) {
      return res.status(401).json({ ok: false, error: "Not signed in" });
    }

    const body = readJsonBody(req);
    let attempts = body.attempts;
    if (!Array.isArray(attempts) && body.track && body.item_id != null) {
      attempts = [body];
    }
    if (!Array.isArray(attempts) || !attempts.length) {
      return res.status(400).json({ ok: false, error: "Missing attempts" });
    }

    const inserted = await insertPracticeAttempts(learner.id, attempts);
    return res.status(200).json({ ok: true, inserted });
  } catch (e) {
    console.error("[account-record-attempt]", e.message);
    return res.status(500).json({ ok: false, error: "Could not save attempts" });
  }
}
