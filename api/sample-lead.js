/**
 * POST /api/sample-lead
 * Sample events: { event, product, email?, ... }
 * Visitor question: { action: "request_question_verification" | "confirm_question", ... }
 * Admin reports: { action: "report" | "questions_report" } + Bearer <admin JWT>
 */
import { verifyAnalyticsAdminToken } from "../server-lib/analytics-admin-jwt.js";
import { filterRowsFromUtcStart, rangePresetLabel } from "../server-lib/google-analytics.js";
import {
  aggregateSampleLeadReport,
  appendSampleLeadEvent,
  buildSampleLeadRow,
  normalizeSampleEvent,
  normalizeSampleProduct,
  readSampleLeadEvents,
} from "../server-lib/sample-lead-analytics.js";
import {
  aggregateVisitorQuestionsReport,
  readVisitorQuestions,
  resolveGithubRepo,
  updateVisitorQuestionCompleted,
} from "../server-lib/visitor-questions.js";
import {
  confirmVisitorQuestionVerification,
  requestVisitorQuestionVerification,
} from "../server-lib/visitor-question-verify.js";

function readJsonBody(req) {
  try {
    if (req.body != null) {
      if (typeof req.body === "object" && !Buffer.isBuffer(req.body)) return req.body;
      if (typeof req.body === "string" && req.body.length) return JSON.parse(req.body);
    }
  } catch (_) {}
  return {};
}

function bearerToken(req) {
  const h = req.headers.authorization || req.headers.Authorization || "";
  const m = /^Bearer\s+(.+)$/i.exec(String(h).trim());
  return m ? m[1].trim() : "";
}

function normalizeEmail(raw) {
  const s = typeof raw === "string" ? raw.trim().toLowerCase() : "";
  if (!s || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s)) return "";
  if (s.length > 254) return "";
  return s;
}

async function handleEvent(req, res, body) {
  if (body.company_website) {
    return res.status(200).json({ ok: true, skipped: "honeypot" });
  }

  const event = normalizeSampleEvent(body.event);
  const product = normalizeSampleProduct(body.product);
  if (!event || !product) {
    return res.status(400).json({ ok: false, error: "invalid_event_or_product" });
  }

  const needsEmail =
    event === "email_submit_attempt" ||
    event === "email_capture_success" ||
    event === "email_capture_fail";
  const email = normalizeEmail(body.email);
  if (needsEmail && !email) {
    return res.status(400).json({ ok: false, error: "invalid_email" });
  }

  const row = buildSampleLeadRow({
    ...body,
    event,
    product,
    email: email || "",
    success: event === "email_capture_success",
  });

  const result = await appendSampleLeadEvent(row);
  return res.status(200).json({
    ok: result.ok !== false,
    skipped: result.skipped || null,
    backend: result.backend || null,
    reason: result.reason || null,
  });
}

async function handleQuestionVerifyRequest(req, res, body) {
  if (body.company_website) {
    return res.status(200).json({ ok: true, skipped: "honeypot" });
  }

  try {
    const result = await requestVisitorQuestionVerification(body);
    if (!result.ok) {
      const reason = result.reason || "error";
      if (reason === "honeypot") {
        return res.status(200).json({ ok: true, skipped: "honeypot" });
      }
      const status =
        reason === "verify_not_configured" || reason === "resend_not_configured" ? 503 : 400;
      return res.status(status).json({
        ok: false,
        error: mapQuestionVerifyReason(reason),
        reason,
      });
    }
    return res.status(200).json({
      ok: true,
      pending: true,
      verifyUrlSent: true,
      email: result.email,
    });
  } catch (err) {
    const code = err && err.code ? String(err.code) : "error";
    const status = code === "verify_not_configured" || code === "resend_not_configured" ? 503 : 502;
    return res.status(status).json({
      ok: false,
      error: mapQuestionVerifyReason(code),
      reason: code,
    });
  }
}

async function handleQuestionConfirm(req, res, body) {
  const token = typeof body.token === "string" ? body.token.trim() : "";
  if (!token) {
    return res.status(400).json({ ok: false, error: "Missing verification token", reason: "missing_token" });
  }

  try {
    const result = await confirmVisitorQuestionVerification(token);
    if (!result.ok) {
      if (result.reason === "not_configured") {
        return res.status(503).json({
          ok: false,
          error: "Questions are not configured on this server",
          hint: "Set GITHUB_LEADS_TOKEN (and GITHUB_LEADS_REPO if needed) on Vercel to persist visitor questions.",
        });
      }
      if (result.reason === "invalid_or_expired_token") {
        return res.status(400).json({
          ok: false,
          error: mapQuestionVerifyReason("invalid_or_expired_token"),
          reason: "invalid_or_expired_token",
        });
      }
      return res.status(502).json({
        ok: false,
        error: "Could not save your question",
        reason: result.reason || "error",
        detail: result.detail || null,
      });
    }
    return res.status(200).json({ ok: true, verified: true, email: result.email });
  } catch (err) {
    const message = err && err.message ? String(err.message) : "Verification failed";
    return res.status(502).json({ ok: false, error: message });
  }
}

function mapQuestionVerifyReason(reason) {
  const map = {
    consent_required: "Please confirm you are not a bot.",
    too_fast: "Please take a moment to complete the form, then try again.",
    timing_required: "Please reopen the form and try again.",
    form_expired: "This form expired. Please reopen Ask a question and try again.",
    invalid_email_or_message: "Enter a valid email and a message (at least 10 characters).",
    message_too_short: "Your message must be at least 10 characters.",
    message_too_long: "Your message is too long (max 2000 characters).",
    resend_not_configured: "Email verification is temporarily unavailable. Try again later.",
    resend_rejected: "We could not send the verification email. Check the address and try again.",
    verify_not_configured: "Email verification is not configured on this server.",
    invalid_or_expired_token: "This verification link is invalid or has expired. Submit your question again.",
    missing_token: "Missing verification token.",
  };
  return map[reason] || reason;
}

function normalizeRangePreset(raw) {
  const p = typeof raw === "string" ? raw.trim().toLowerCase() : "";
  if (p === "today" || p === "7d" || p === "28d" || p === "90d") return p;
  return "7d";
}

async function handleQuestionUpdate(req, res, body) {
  const jwtSecret = (process.env.ADMIN_ANALYTICS_JWT_SECRET || "").trim();
  const token = bearerToken(req) || (body.token || "");

  if (!jwtSecret) {
    return res.status(503).json({ ok: false, error: "Admin analytics is not configured" });
  }

  if (!verifyAnalyticsAdminToken(token, jwtSecret)) {
    return res.status(401).json({ ok: false, error: "Unauthorized" });
  }

  const questionId = typeof body.question_id === "string" ? body.question_id.trim() : "";
  const completed = body.completed === true || body.completed === "true" || body.completed === 1;

  if (!questionId) {
    return res.status(400).json({ ok: false, error: "Missing question_id" });
  }

  try {
    const result = await updateVisitorQuestionCompleted(questionId, completed);
    if (!result.ok) {
      const status = result.reason === "not_found" ? 404 : result.reason === "not_configured" ? 503 : 502;
      return res.status(status).json({
        ok: false,
        error: result.reason === "not_found" ? "Question not found" : "Could not save completed status",
        reason: result.reason || "error",
        detail: result.detail || null,
      });
    }
    return res.status(200).json({
      ok: true,
      questionId: result.questionId,
      completed: result.completed,
      backend: result.backend || null,
    });
  } catch (err) {
    const message = err && err.message ? String(err.message) : "Update failed";
    return res.status(502).json({ ok: false, error: message });
  }
}

async function handleQuestionsReport(req, res, body) {
  const jwtSecret = (process.env.ADMIN_ANALYTICS_JWT_SECRET || "").trim();
  const token = bearerToken(req) || (body.token || "");

  if (!jwtSecret) {
    return res.status(503).json({ ok: false, error: "Admin analytics is not configured" });
  }

  if (!verifyAnalyticsAdminToken(token, jwtSecret)) {
    return res.status(401).json({ ok: false, error: "Unauthorized" });
  }

  const range = normalizeRangePreset(body.range);

  try {
    const allRows = await readVisitorQuestions();
    const inRange = filterRowsFromUtcStart(allRows, range);
    const rows = inRange.filter((r) => String(r.status || "").toLowerCase() === "verified");
    const report = aggregateVisitorQuestionsReport(rows);
    const repoInfo = resolveGithubRepo();
    return res.status(200).json({
      ok: true,
      ...report,
      range,
      rangeLabel: rangePresetLabel(range),
      fetchedAt: new Date().toISOString(),
      note: `Verified visitor questions (${rangePresetLabel(range)}). Submitted after email confirmation from Ask a question.`,
      csvPath: "data/leads/visitor-questions.csv",
      storageRepo: repoInfo ? `${repoInfo.owner}/${repoInfo.repo}` : null,
      rawRowCount: rows.length,
      totalRowCount: allRows.length,
    });
  } catch (err) {
    const message = err && err.message ? String(err.message) : "Visitor questions report error";
    if (err && err.code === "github_not_configured") {
      return res.status(503).json({
        ok: false,
        error: "Visitor questions storage is not configured",
        hint: "Set GITHUB_LEADS_TOKEN on Vercel (Contents read/write on this repo). Questions save to data/leads/visitor-questions.csv via the GitHub API.",
      });
    }
    return res.status(502).json({ ok: false, error: message });
  }
}

async function handleReport(req, res, body) {
  const jwtSecret = (process.env.ADMIN_ANALYTICS_JWT_SECRET || "").trim();
  const token = bearerToken(req) || (body.token || "");

  if (!jwtSecret) {
    return res.status(503).json({ ok: false, error: "Admin analytics is not configured" });
  }

  if (!verifyAnalyticsAdminToken(token, jwtSecret)) {
    return res.status(401).json({ ok: false, error: "Unauthorized" });
  }

  const range = normalizeRangePreset(body.range);

  try {
    const allRows = await readSampleLeadEvents();
    const rows = filterRowsFromUtcStart(allRows, range);
    const report = aggregateSampleLeadReport(rows);
    return res.status(200).json({
      ok: true,
      ...report,
      range,
      rangeLabel: rangePresetLabel(range),
      fetchedAt: new Date().toISOString(),
      note:
        `Free sample completions (${rangePresetLabel(range)}). Logged when visitors finish a sample track.`,
      csvPath: "data/leads/home-sample-email-capture.csv",
      storageRepo: (() => {
        const repo = resolveGithubRepo();
        return repo ? `${repo.owner}/${repo.repo}` : null;
      })(),
      totalRowCount: allRows.length,
    });
  } catch (err) {
    const message = err && err.message ? String(err.message) : "Sample lead report error";
    return res.status(502).json({ ok: false, error: message });
  }
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "method_not_allowed" });
  }

  const body = readJsonBody(req);
  const action = typeof body.action === "string" ? body.action.trim().toLowerCase() : "";

  if (action === "submit_question" || action === "request_question_verification") {
    return handleQuestionVerifyRequest(req, res, body);
  }

  if (action === "confirm_question") {
    return handleQuestionConfirm(req, res, body);
  }

  if (action === "questions_report") {
    return handleQuestionsReport(req, res, body);
  }

  if (action === "update_question") {
    return handleQuestionUpdate(req, res, body);
  }

  const isReport =
    action === "report" || (Boolean(bearerToken(req) || body.token) && !body.event && !action);

  if (isReport) {
    return handleReport(req, res, body);
  }

  return handleEvent(req, res, body);
}
