/**
 * POST /api/sample-lead-event
 * Body: { event, product, email?, sample_kind?, source?, utm?, company_website? }
 */
import {
  appendSampleLeadEvent,
  buildSampleLeadRow,
  normalizeSampleEvent,
  normalizeSampleProduct,
} from "../server-lib/sample-lead-analytics.js";

function readJsonBody(req) {
  try {
    if (req.body != null) {
      if (typeof req.body === "object" && !Buffer.isBuffer(req.body)) return req.body;
      if (typeof req.body === "string" && req.body.length) return JSON.parse(req.body);
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

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "method_not_allowed" });
  }

  const body = readJsonBody(req);
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
