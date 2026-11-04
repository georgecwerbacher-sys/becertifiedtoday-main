/**
 * GET /api/account-schedule — list exam schedules
 * POST /api/account-schedule — body: { track, exam_date, notes? }
 */
import { learnerFromRequest } from "../server-lib/learner-auth.js";
import {
  isValidTrack,
  listExamSchedules,
  postgresConfigured,
  upsertExamSchedule,
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
  if (req.method !== "GET" && req.method !== "POST") {
    res.setHeader("Allow", "GET, POST");
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

    if (req.method === "GET") {
      const schedules = await listExamSchedules(learner.id);
      return res.status(200).json({ ok: true, schedules });
    }

    const body = readJsonBody(req);
    const track = String(body.track || "").toLowerCase();
    if (!isValidTrack(track)) {
      return res.status(400).json({ ok: false, error: "Invalid track" });
    }
    const examDate = body.exam_date || body.examDate;
    try {
      const row = await upsertExamSchedule(
        learner.id,
        track,
        examDate,
        body.notes || ""
      );
      return res.status(200).json({ ok: true, schedule: row });
    } catch (e) {
      if (e.message === "invalid_date") {
        return res.status(400).json({ ok: false, error: "Use exam_date as YYYY-MM-DD" });
      }
      throw e;
    }
  } catch (e) {
    console.error("[account-schedule]", e.message);
    return res.status(500).json({ ok: false, error: "Could not save schedule" });
  }
}
