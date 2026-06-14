/**
 * Email verification for footer Ask a question (proof of real inbox + bot timing).
 */
import { normalizePublicSiteUrl } from "./normalize-public-site-url.js";
import { signPortalMagicJwt, verifyPortalMagicJwt } from "./ccna-portal-magic-jwt.js";
import {
  appendVisitorQuestion,
  buildVisitorQuestionRow,
  normalizeQuestionProduct,
} from "./visitor-questions.js";
import { appendSampleLeadEvent } from "./sample-lead-analytics.js";
import { appendMarketingLeadCsv, buildLeadCsvRow } from "./append-marketing-lead-csv.js";

const VERIFY_AUD = "visitor-question-verify";
const VERIFY_TTL_SEC = 60 * 60 * 24;
const MIN_FORM_MS = 3000;

function verifySecret() {
  return (
    (process.env.VISITOR_QUESTION_VERIFY_SECRET || "").trim() ||
    (process.env.PORTAL_MAGIC_LINK_SECRET || "").trim() ||
    (process.env.ADMIN_ANALYTICS_JWT_SECRET || "").trim()
  );
}

function escapeHtml(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function escapeAttr(s) {
  return String(s).replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");
}

export function validateVisitorQuestionHumanSignals(body) {
  if (body.company_website) {
    return { ok: false, reason: "honeypot" };
  }
  if (!body.consent) {
    return { ok: false, reason: "consent_required" };
  }
  const openedAt = Number(body.form_opened_at || body.formOpenedAt);
  if (!Number.isFinite(openedAt)) {
    return { ok: false, reason: "timing_required" };
  }
  const elapsed = Date.now() - openedAt;
  if (elapsed < MIN_FORM_MS) {
    return { ok: false, reason: "too_fast" };
  }
  if (elapsed > VERIFY_TTL_SEC * 1000) {
    return { ok: false, reason: "form_expired" };
  }
  return { ok: true };
}

export function issueVisitorQuestionVerifyToken({ email, message, product, pagePath }) {
  const secret = verifySecret();
  if (!secret) {
    const err = new Error("verify_not_configured");
    err.code = "verify_not_configured";
    throw err;
  }
  const exp = Math.floor(Date.now() / 1000) + VERIFY_TTL_SEC;
  return signPortalMagicJwt(
    {
      aud: VERIFY_AUD,
      sub: email,
      exp,
      msg: message,
      product,
      pp: pagePath,
    },
    secret
  );
}

export function readVisitorQuestionVerifyToken(token) {
  const secret = verifySecret();
  if (!secret) return null;
  const payload = verifyPortalMagicJwt(token, secret);
  if (!payload || payload.aud !== VERIFY_AUD) return null;
  const now = Math.floor(Date.now() / 1000);
  if (!payload.exp || Number(payload.exp) < now) return null;
  const email = String(payload.sub || "")
    .trim()
    .toLowerCase();
  const message = String(payload.msg || "").trim();
  const product = normalizeQuestionProduct(payload.product);
  const pagePath = String(payload.pp || "").trim().slice(0, 240);
  if (!email || !message) return null;
  return { email, message, product, pagePath };
}

export async function sendVisitorQuestionVerifyEmail({ to, verifyUrl, product }) {
  const key = (process.env.RESEND_API_KEY || "").trim();
  if (!key) {
    const err = new Error("resend_not_configured");
    err.code = "resend_not_configured";
    throw err;
  }

  const from =
    (process.env.RESEND_FROM || "").trim() ||
    "Be Certified Today <onboarding@resend.dev>";

  const subject =
    (process.env.RESEND_VISITOR_QUESTION_VERIFY_SUBJECT || "").trim() ||
    "Confirm your question — Be Certified Today";

  const track =
    product === "ccna"
      ? "CCNA"
      : product === "encor"
        ? "ENCOR"
        : product === "secplus"
          ? "Security+"
          : "exam prep";

  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${key}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      from,
      to: [to],
      subject,
      html: `<p>Thanks for reaching out about <strong>${escapeHtml(track)}</strong> on Be Certified Today.</p>
<p>Confirm your email to send your question to our team:</p>
<p><a href="${escapeAttr(verifyUrl)}"><strong>Verify email and submit question</strong></a></p>
<p style="word-break:break-all;font-size:13px;color:#444">${escapeHtml(verifyUrl)}</p>
<p style="font-size:13px;color:#666">This link expires in 24 hours. If you did not request this, ignore this email.</p>`,
    }),
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    console.error("[visitor-question] verify email failed:", res.status, text.slice(0, 300));
    const err = new Error("resend_rejected");
    err.code = "resend_rejected";
    throw err;
  }
  return true;
}

export async function requestVisitorQuestionVerification(body) {
  const human = validateVisitorQuestionHumanSignals(body);
  if (!human.ok) return { ok: false, reason: human.reason };

  const row = buildVisitorQuestionRow(body);
  if (!row.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(row.email)) {
    return { ok: false, reason: "invalid_email_or_message" };
  }
  if (!row.message || row.message.length < 10) {
    return { ok: false, reason: "message_too_short" };
  }
  if (row.message.length > 2000) {
    return { ok: false, reason: "message_too_long" };
  }

  const site = normalizePublicSiteUrl(process.env.PUBLIC_SITE_URL || "https://becertifiedtoday.com");
  const token = issueVisitorQuestionVerifyToken({
    email: row.email,
    message: row.message,
    product: row.product,
    pagePath: row.page_path,
  });
  const verifyUrl = `${site}/verify-question.html?token=${encodeURIComponent(token)}`;

  await sendVisitorQuestionVerifyEmail({
    to: row.email,
    verifyUrl,
    product: row.product,
  });

  return {
    ok: true,
    pending: true,
    email: row.email,
    verifyUrlSent: true,
  };
}

export async function confirmVisitorQuestionVerification(token) {
  const payload = readVisitorQuestionVerifyToken(token);
  if (!payload) {
    return { ok: false, reason: "invalid_or_expired_token" };
  }

  const result = await appendVisitorQuestion({
    email: payload.email,
    message: payload.message,
    product: payload.product,
    page_path: payload.pagePath,
    status: "verified",
  });

  if (!result.ok) return result;

  try {
    await appendSampleLeadEvent({
      event: "email_capture_success",
      email: payload.email,
      product: payload.product === "general" ? "ccna" : payload.product,
      sample_kind: "visitor_question",
      source: "visitor_question_verify",
      success: true,
    });
  } catch (err) {
    console.warn("[visitor-question] sample lead log failed:", err?.message || err);
  }

  try {
    await appendMarketingLeadCsv(
      buildLeadCsvRow(
        { email: payload.email, product: payload.product, source: "visitor_question_verify" },
        {
          event: "visitor_question_verified",
          email: payload.email,
          magnet: "visitor-question",
          product: payload.product,
          source: "visitor_question_verify",
        }
      )
    );
  } catch (err) {
    console.warn("[visitor-question] marketing csv failed:", err?.message || err);
  }

  return { ok: true, verified: true, email: payload.email };
}
