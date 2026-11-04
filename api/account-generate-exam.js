/**
 * POST /api/account-generate-exam
 * Body: { track, paid?: boolean, limit?: number }
 * Builds a weak-area practice set. Free users are capped and limited to sample pools
 * (except when client reports paid portal for a track that has a paid pool).
 */
import { learnerFromRequest } from "../server-lib/learner-auth.js";
import { buildGeneratedExam } from "../server-lib/learner-exam-pool.js";
import {
  FREE_DAILY_GENERATED_CAP,
  bumpDailyGeneratedUsage,
  getDailyGeneratedUsage,
  getWeakDomains,
  getWeakItemIds,
  isValidTrack,
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
    const track = String(body.track || "").toLowerCase();
    if (!isValidTrack(track)) {
      return res.status(400).json({ ok: false, error: "Invalid track" });
    }

    const paid = Boolean(body.paid);
    const used = await getDailyGeneratedUsage(learner.id);
    const remaining = Math.max(0, FREE_DAILY_GENERATED_CAP - used);
    if (remaining <= 0) {
      return res.status(429).json({
        ok: false,
        error: "Daily free practice limit reached",
        freeUsage: {
          generatedToday: used,
          generatedDailyCap: FREE_DAILY_GENERATED_CAP,
          remaining: 0,
        },
      });
    }

    const want = Math.min(
      Math.max(parseInt(String(body.limit || "10"), 10) || 10, 1),
      remaining,
      FREE_DAILY_GENERATED_CAP
    );

    const [weakItemIds, weakDomains] = await Promise.all([
      getWeakItemIds(learner.id, track, want),
      getWeakDomains(learner.id, track, 3),
    ]);

    const exam = buildGeneratedExam({
      track,
      paid,
      weakItemIds,
      weakDomains,
      limit: want,
    });

    if (!exam.items.length) {
      return res.status(400).json({
        ok: false,
        error: "No practice items available for this track yet",
      });
    }

    const newTotal = await bumpDailyGeneratedUsage(learner.id, exam.items.length);

    return res.status(200).json({
      ok: true,
      exam,
      freeUsage: {
        generatedToday: newTotal,
        generatedDailyCap: FREE_DAILY_GENERATED_CAP,
        remaining: Math.max(0, FREE_DAILY_GENERATED_CAP - newTotal),
      },
      hint: paid
        ? null
        : "Free accounts practice from the public sample pool. Unlock a portal for full-bank weak-area exams.",
    });
  } catch (e) {
    console.error("[account-generate-exam]", e.message);
    return res.status(500).json({ ok: false, error: "Could not generate practice exam" });
  }
}
