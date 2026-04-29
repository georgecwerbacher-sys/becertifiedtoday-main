import { kvGet, kvIncr, kvSetNxEx } from "./kv.js";

const KNOWN_EVENTS = [
  "page_view",
  "purchase_clicked",
  "checkout_started",
  "checkout_session_completed",
  "magic_link_requested",
  "magic_link_verified",
  "renew_clicked",
];

function dayStamp(date = new Date()) {
  return date.toISOString().slice(0, 10);
}

function safeEventName(name) {
  return String(name || "")
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9_]/g, "");
}

export async function trackEvent(name, meta = {}) {
  const event = safeEventName(name);
  if (!event) return;

  const day = dayStamp();
  await kvIncr(`analytics:total:${event}`);
  await kvIncr(`analytics:day:${day}:${event}`);

  const path = typeof meta.path === "string" ? meta.path.slice(0, 120) : null;
  if (path) {
    const safePath = path.replace(/[^a-zA-Z0-9/_-]/g, "");
    if (safePath) {
      await kvIncr(`analytics:path:${safePath}:${event}`);
    }
  }
}

export async function shouldAcceptPageView(ip, path) {
  const safePath = String(path || "/").replace(/[^a-zA-Z0-9/_-]/g, "") || "/";
  const key = `analytics:pageview:ip:${ip}:${safePath}`;
  return kvSetNxEx(key, "1", 60 * 10);
}

export async function getSummary() {
  const day = dayStamp();
  const rows = await Promise.all(
    KNOWN_EVENTS.map(async (event) => {
      const [total, today] = await Promise.all([
        kvGet(`analytics:total:${event}`),
        kvGet(`analytics:day:${day}:${event}`),
      ]);
      return {
        event,
        total: Number(total || 0),
        today: Number(today || 0),
      };
    })
  );
  return {
    day,
    events: rows,
  };
}
