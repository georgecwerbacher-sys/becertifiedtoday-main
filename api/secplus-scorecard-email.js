/**
 * POST /api/secplus-scorecard-email
 * Body: { "email": "...", "consent": true, "scorecard": { ... } }
 */
import { normalizePublicSiteUrl } from "../server-lib/normalize-public-site-url.js";
import { sendSecplusScorecardEmail } from "../server-lib/secplus-scorecard-email.js";
import { addMarketingContact, resolveLeadMagnet } from "../server-lib/marketing-lead-resend.js";
import { appendMarketingLeadCsv, buildLeadCsvRow } from "../server-lib/append-marketing-lead-csv.js";

function readJsonBody(req) {
  try {
    if (req.body != null) {
      if (typeof req.body === "object" && !Buffer.isBuffer(req.body)) {
        return req.body;
      }
      if (typeof req.body === "string" && req.body.length) {
        return JSON.parse(req.body);
      }
    }
  } catch (_) {}
  return {};
}

function normalizeEmail(raw) {
  const s = typeof raw === "string" ? raw.trim().toLowerCase() : "";
  if (!s || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s)) return "";
  if (s.length > 254) return "";
  return s;
}

function sanitizeScorecard(raw) {
  if (!raw || typeof raw !== "object") return null;
  const n = (v) => (typeof v === "number" && Number.isFinite(v) ? v : 0);
  const b = (v) => !!v;
  const s = (v) => (typeof v === "string" ? v.slice(0, 200) : "");

  const domains = Array.isArray(raw.domains)
    ? raw.domains.slice(0, 8).map((d) => ({
        id: s(d.id),
        title: s(d.title),
        correct: n(d.correct),
        total: n(d.total),
        pct: n(d.pct),
        priority: s(d.priority),
      }))
    : [];

  const weakObjectives = Array.isArray(raw.weakObjectives)
    ? raw.weakObjectives.slice(0, 12).map((o) => ({
        id: s(o.id),
        topic: s(o.topic),
        correct: n(o.correct),
        total: n(o.total),
        pct: n(o.pct),
      }))
    : [];

  return {
    reason: s(raw.reason),
    scaledScore: n(raw.scaledScore),
    scaledMax: n(raw.scaledMax) || 900,
    passingScore: n(raw.passingScore) || 750,
    passed: b(raw.passed),
    mcqCorrect: n(raw.mcqCorrect),
    mcqTotal: n(raw.mcqTotal),
    simCorrect: n(raw.simCorrect),
    simTotal: n(raw.simTotal),
    domains,
    weakObjectives,
    isFreeSample: b(raw.isFreeSample),
  };
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "method_not_allowed" });
  }

  const body = readJsonBody(req);
  const email = normalizeEmail(body.email);
  if (!email) {
    return res.status(400).json({ ok: false, error: "invalid_email" });
  }
  if (!body.consent) {
    return res.status(400).json({ ok: false, error: "consent_required" });
  }

  const scorecard = sanitizeScorecard(body.scorecard);
  if (!scorecard || !scorecard.mcqTotal) {
    return res.status(400).json({ ok: false, error: "invalid_scorecard" });
  }

  const site = normalizePublicSiteUrl(process.env.PUBLIC_SITE_URL || "https://becertifiedtoday.com");

  const magnet = resolveLeadMagnet("secplus-free-simulation");
  if (magnet) {
    try {
      await addMarketingContact({ email, magnet });
    } catch (err) {
      console.warn("[secplus-scorecard] audience contact failed:", err?.message || err);
    }
  }

  try {
    await appendMarketingLeadCsv(
      buildLeadCsvRow(body, {
        event: "scorecard_email",
        email,
        magnet: "secplus-free-simulation",
        product: "secplus",
        source: String(body.source || "scorecard_email_api"),
      })
    );
  } catch (err) {
    console.warn("[secplus-scorecard] csv append failed:", err?.message || err);
  }

  try {
    await sendSecplusScorecardEmail({ to: email, payload: scorecard, siteUrl: site });
  } catch (err) {
    console.error("[secplus-scorecard] send failed:", err?.message || err);
    return res.status(502).json({ ok: false, error: "email_failed" });
  }

  return res.status(200).json({ ok: true });
}
