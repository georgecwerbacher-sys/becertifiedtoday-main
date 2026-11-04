/**
 * GET /api/account-results
 * Aggregated practice results by track/domain for the signed-in learner.
 */
import { learnerFromRequest } from "../server-lib/learner-auth.js";
import { getResultsAggregate, postgresConfigured } from "../server-lib/learner-db.js";

export default async function handler(req, res) {
  if (req.method !== "GET") {
    res.setHeader("Allow", "GET");
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
    const results = await getResultsAggregate(learner.id);
    return res.status(200).json({ ok: true, results });
  } catch (e) {
    console.error("[account-results]", e.message);
    return res.status(500).json({ ok: false, error: "Could not load results" });
  }
}
