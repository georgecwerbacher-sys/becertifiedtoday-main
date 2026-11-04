/**
 * GET /api/account-me
 * Returns learner profile summary when bcc_learner cookie is valid.
 * Optional query paid=ccna,encor (client-reported paid portal tracks for UI flags).
 */
import { learnerFromRequest } from "../server-lib/learner-auth.js";
import {
  FREE_DAILY_GENERATED_CAP,
  getDailyGeneratedUsage,
  getResultsAggregate,
  listExamSchedules,
  postgresConfigured,
  TRACKS,
} from "../server-lib/learner-db.js";

function parsePaidTracks(req) {
  const q = String(req.query?.paid || "").toLowerCase();
  const set = new Set();
  q.split(",")
    .map((s) => s.trim())
    .forEach((t) => {
      if (TRACKS.includes(t)) set.add(t);
    });
  return set;
}

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

    const paid = parsePaidTracks(req);
    const access = {};
    for (const t of TRACKS) {
      access[t] = {
        paidPortal: paid.has(t),
        limitedFree: true,
      };
    }

    const [results, schedules, used] = await Promise.all([
      getResultsAggregate(learner.id),
      listExamSchedules(learner.id),
      getDailyGeneratedUsage(learner.id),
    ]);

    return res.status(200).json({
      ok: true,
      learner: {
        id: learner.id,
        email: learner.email,
        createdAt: learner.created_at,
        lastLoginAt: learner.last_login_at,
      },
      access,
      results,
      schedules,
      freeUsage: {
        generatedToday: used,
        generatedDailyCap: FREE_DAILY_GENERATED_CAP,
        remaining: Math.max(0, FREE_DAILY_GENERATED_CAP - used),
      },
    });
  } catch (e) {
    console.error("[account-me]", e.message);
    return res.status(500).json({ ok: false, error: "Could not load account" });
  }
}
