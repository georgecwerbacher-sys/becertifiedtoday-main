export const ACCESS_WINDOW_DAYS = Number(process.env.ACCESS_WINDOW_DAYS || 30);
export const MAGIC_LINK_TTL_MINUTES = Number(process.env.MAGIC_LINK_TTL_MINUTES || 30);
export const SESSION_TTL_DAYS = Number(process.env.SESSION_TTL_DAYS || 30);

export function requireEnv(name) {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing required env var: ${name}`);
  }
  return value;
}

export function normalizeEmail(value) {
  return String(value || "").trim().toLowerCase();
}
