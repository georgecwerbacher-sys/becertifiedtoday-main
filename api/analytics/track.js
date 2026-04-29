import { trackEvent, shouldAcceptPageView } from "../_lib/analytics.js";

function clientIp(req) {
  const forwarded = req.headers["x-forwarded-for"];
  if (typeof forwarded === "string" && forwarded.length > 0) {
    return forwarded.split(",")[0].trim();
  }
  return "unknown";
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method Not Allowed" });
  }

  try {
    const body = req.body && typeof req.body === "object" ? req.body : {};
    const event = body.event;
    const path = typeof body.path === "string" ? body.path : "/";

    if (event === "page_view") {
      const accepted = await shouldAcceptPageView(clientIp(req), path);
      if (!accepted) return res.status(200).json({ tracked: false });
    }

    await trackEvent(event, { path });
    return res.status(200).json({ tracked: true });
  } catch (error) {
    console.error("analytics track failed:", error);
    return res.status(200).json({ tracked: false });
  }
}
