/**
 * GET /api/analytics-config
 * Public measurement ID for client-side gtag (not secret).
 */
import { getGoogleAnalyticsEnv } from "../server-lib/google-analytics.js";

export default function handler(req, res) {
  if (req.method !== "GET") {
    res.setHeader("Allow", "GET");
    return res.status(405).json({ ok: false, error: "Method not allowed" });
  }

  const { measurementId } = getGoogleAnalyticsEnv();
  res.setHeader("Cache-Control", "public, max-age=300");
  return res.status(200).json({
    ok: true,
    enabled: Boolean(measurementId),
    measurementId: measurementId || null,
  });
}
