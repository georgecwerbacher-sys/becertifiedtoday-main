/**
 * POST /api/sample-lead
 * Sample events: { event, product, email?, ... }
 * Visitor question: { action: "submit_question", email, message, product?, page_path? }
 * Admin reports: { action: "report" | "questions_report" } + Bearer <admin JWT>
 */
import { verifyAnalyticsAdminToken } from "../server-lib/analytics-admin-jwt.js";
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
  appendVisitorQuestion,
  normalizeQuestionProduct,
  readVisitorQuestions,
  resolveGithubRepo,
} from "../server-lib/visitor-questions.js";

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

async function handleQuestionSubmit(req, res, body) {
  if (body.company_website) {
    return res.status(200).json({ ok: true, skipped: "honeypot" });
  }

  const email = normalizeEmail(body.email);
  const message = typeof body.message === "string" ? body.message.trim() : "";
  if (!email) {
    return res.status(400).json({ ok: false, error: "invalid_email" });
  }
  if (!message || message.length < 10) {
    return res.status(400).json({ ok: false, error: "message_too_short" });
  }
  if (message.length > 2000) {
    return res.status(400).json({ ok: false, error: "message_too_long" });
  }

  const result = await appendVisitorQuestion({
    email,
    message,
    product: normalizeQuestionProduct(body.product),
    page_path: body.page_path || body.pagePath || "",
  });

  if (!result.ok && result.reason === "not_configured") {
    return res.status(503).json({
      ok: false,
      error: "Questions are not configured on this server",
      hint: "Set GITHUB_LEADS_TOKEN (and GITHUB_LEADS_REPO if needed) on Vercel to persist visitor questions.",
    });
  }

  if (!result.ok) {
    return res.status(502).json({
      ok: false,
      error: "Could not save your question",
      reason: result.reason || "error",
      detail: result.detail || null,
      hint: "Check Vercel logs for /api/sample-lead and GitHub token permissions on data/leads/visitor-questions.csv.",
    });
  }

  return res.status(200).json({
    ok: true,
    backend: result.backend || null,
  });
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

  try {
    const rows = await readVisitorQuestions();
    const report = aggregateVisitorQuestionsReport(rows);
    const repoInfo = resolveGithubRepo();
    return res.status(200).json({
      ok: true,
      ...report,
      fetchedAt: new Date().toISOString(),
      note: "Visitor questions from site footers (replaces mailto). Stored in data/leads/visitor-questions.csv.",
      csvPath: "data/leads/visitor-questions.csv",
      storageRepo: repoInfo ? `${repoInfo.owner}/${repoInfo.repo}` : null,
      rawRowCount: rows.length,
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

  try {
    const rows = await readSampleLeadEvents();
    const report = aggregateSampleLeadReport(rows);
    return res.status(200).json({
      ok: true,
      ...report,
      fetchedAt: new Date().toISOString(),
      note:
        "Free sample completions (questions, drag-and-drop, labs, simulations) logged when visitors finish a sample track. " +
        "Email capture counts are timed-simulation unlocks after the sample funnel.",
      csvPath: "data/leads/home-sample-email-capture.csv",
      storageRepo: (() => {
        const repo = resolveGithubRepo();
        return repo ? `${repo.owner}/${repo.repo}` : null;
      })(),
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

  if (action === "submit_question") {
    return handleQuestionSubmit(req, res, body);
  }

  if (action === "questions_report") {
    return handleQuestionsReport(req, res, body);
  }

  const isReport =
    action === "report" || (Boolean(bearerToken(req) || body.token) && !body.event && !action);

  if (isReport) {
    return handleReport(req, res, body);
  }

  return handleEvent(req, res, body);
}
