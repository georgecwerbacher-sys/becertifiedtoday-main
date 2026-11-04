/**
 * Unified learner account API (Hobby plan: one serverless function).
 * Paths (rewritten to this file):
 *   POST /api/account-request-login
 *   POST /api/account-redeem-login
 *   POST /api/account-logout
 *   GET  /api/account-me
 *   POST /api/account-record-attempt
 *   GET  /api/account-results
 *   GET|POST /api/account-schedule
 *   POST /api/account-generate-exam
 */
import { normalizePublicSiteUrl } from "../server-lib/normalize-public-site-url.js";
import {
  learnerFromRequest,
  learnerMagicSecret,
  logoutLearnerRequest,
  redeemLearnerLogin,
  signLearnerMagicToken,
  verifyLearnerMagicToken,
} from "../server-lib/learner-auth.js";
import { sendLearnerLoginEmail } from "../server-lib/learner-resend.js";
import { buildGeneratedExam } from "../server-lib/learner-exam-pool.js";
import {
  FREE_DAILY_GENERATED_CAP,
  TRACKS,
  bumpDailyGeneratedUsage,
  getDailyGeneratedUsage,
  getResultsAggregate,
  getWeakDomains,
  getWeakItemIds,
  insertPracticeAttempts,
  isValidTrack,
  listExamSchedules,
  normalizeEmail,
  postgresConfigured,
  upsertExamSchedule,
} from "../server-lib/learner-db.js";

const GENERIC =
  "If that email can receive mail, we sent a sign-in link. Check spam and wait a minute before trying again.";

function readJsonBody(req) {
  try {
    if (req.body != null) {
      if (typeof req.body === "object" && !Buffer.isBuffer(req.body)) return req.body;
      if (typeof req.body === "string" && req.body.length) return JSON.parse(req.body);
    }
  } catch (_) {}
  return {};
}

function routeOp(req) {
  const q = String(req.query?.op || "").trim().toLowerCase();
  if (q) return q;
  const url = String(req.url || "");
  const path = url.split("?")[0] || "";
  const m = /\/api\/account(?:-([a-z0-9-]+))?\/?$/i.exec(path);
  if (m && m[1]) return m[1].toLowerCase();
  return "";
}

function storageUnavailable(res) {
  return res.status(503).json({
    ok: false,
    error: "Account storage is not configured",
    hint: "Set KV_REST_API_URL + KV_REST_API_TOKEN (Vercel KV / Upstash Redis)",
  });
}

async function requestLogin(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "Method not allowed" });
  }
  if (!postgresConfigured()) return storageUnavailable(res);
  if (!learnerMagicSecret()) {
    return res.status(503).json({
      ok: false,
      error: "Login links are not configured",
      hint: "Set LEARNER_MAGIC_LINK_SECRET or PORTAL_MAGIC_LINK_SECRET",
    });
  }
  const body = readJsonBody(req);
  const email = normalizeEmail(body.email);
  if (!email) {
    return res.status(400).json({ ok: false, error: "Enter a valid email address" });
  }
  const origin =
    normalizePublicSiteUrl(process.env.PUBLIC_SITE_URL) ||
    normalizePublicSiteUrl(req.headers?.origin) ||
    "https://becertifiedtoday.com";
  try {
    const token = signLearnerMagicToken(email, 30);
    const magicUrl = `${origin}/account/magic.html?token=${encodeURIComponent(token)}`;
    await sendLearnerLoginEmail({ to: email, magicUrl });
  } catch (e) {
    console.error("[account-request-login]", e.message);
    return res.status(200).json({ ok: true, message: GENERIC });
  }
  return res.status(200).json({ ok: true, message: GENERIC });
}

async function redeemLogin(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "Method not allowed" });
  }
  if (!postgresConfigured()) return storageUnavailable(res);
  const body = readJsonBody(req);
  const token = typeof body.token === "string" ? body.token.trim() : "";
  if (!token) {
    return res.status(400).json({ ok: false, error: "Missing token" });
  }
  const payload = verifyLearnerMagicToken(token);
  if (!payload) {
    return res.status(401).json({ ok: false, error: "Invalid or expired link" });
  }
  try {
    const result = await redeemLearnerLogin(payload.email);
    res.setHeader("Set-Cookie", result.cookie);
    return res.status(200).json({
      ok: true,
      email: result.learner.email,
      learnerId: result.learner.id,
      expiresAt: result.expiresAt.toISOString(),
      redirect: "/account/",
    });
  } catch (e) {
    console.error("[account-redeem-login]", e.message);
    return res.status(500).json({
      ok: false,
      error: "Could not complete sign-in",
      hint: "Confirm KV_REST_API_URL and KV_REST_API_TOKEN are set.",
    });
  }
}

async function logout(req, res) {
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

async function me(req, res) {
  if (req.method !== "GET") {
    res.setHeader("Allow", "GET");
    return res.status(405).json({ ok: false, error: "Method not allowed" });
  }
  if (!postgresConfigured()) return storageUnavailable(res);
  try {
    const learner = await learnerFromRequest(req);
    if (!learner) {
      return res.status(401).json({ ok: false, error: "Not signed in" });
    }
    const paid = parsePaidTracks(req);
    const access = {};
    for (const t of TRACKS) {
      access[t] = { paidPortal: paid.has(t), limitedFree: true };
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

async function recordAttempt(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "Method not allowed" });
  }
  if (!postgresConfigured()) return storageUnavailable(res);
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

async function results(req, res) {
  if (req.method !== "GET") {
    res.setHeader("Allow", "GET");
    return res.status(405).json({ ok: false, error: "Method not allowed" });
  }
  if (!postgresConfigured()) return storageUnavailable(res);
  try {
    const learner = await learnerFromRequest(req);
    if (!learner) {
      return res.status(401).json({ ok: false, error: "Not signed in" });
    }
    const resultsAgg = await getResultsAggregate(learner.id);
    return res.status(200).json({ ok: true, results: resultsAgg });
  } catch (e) {
    console.error("[account-results]", e.message);
    return res.status(500).json({ ok: false, error: "Could not load results" });
  }
}

async function schedule(req, res) {
  if (req.method !== "GET" && req.method !== "POST") {
    res.setHeader("Allow", "GET, POST");
    return res.status(405).json({ ok: false, error: "Method not allowed" });
  }
  if (!postgresConfigured()) return storageUnavailable(res);
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

async function generateExam(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "Method not allowed" });
  }
  if (!postgresConfigured()) return storageUnavailable(res);
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

export default async function handler(req, res) {
  const op = routeOp(req);
  switch (op) {
    case "request-login":
      return requestLogin(req, res);
    case "redeem-login":
      return redeemLogin(req, res);
    case "logout":
      return logout(req, res);
    case "me":
      return me(req, res);
    case "record-attempt":
      return recordAttempt(req, res);
    case "results":
      return results(req, res);
    case "schedule":
      return schedule(req, res);
    case "generate-exam":
      return generateExam(req, res);
    default:
      return res.status(404).json({ ok: false, error: "Unknown account endpoint" });
  }
}
