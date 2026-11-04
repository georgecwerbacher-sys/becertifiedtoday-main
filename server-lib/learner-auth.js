/**
 * Learner session cookie + magic-link JWT helpers.
 */
import crypto from "crypto";
import {
  signPortalMagicJwt,
  verifyPortalMagicJwt,
} from "./ccna-portal-magic-jwt.js";
import {
  LEARNER_COOKIE,
  LEARNER_SESSION_DAYS,
  createLearnerSession,
  deleteLearnerSession,
  getLearnerBySessionHash,
  upsertLearnerByEmail,
} from "./learner-db.js";

export const LEARNER_AUD = "learner-account";

export function learnerMagicSecret() {
  return (
    (process.env.LEARNER_MAGIC_LINK_SECRET || "").trim() ||
    (process.env.PORTAL_MAGIC_LINK_SECRET || "").trim()
  );
}

export function hashSessionToken(token) {
  return crypto.createHash("sha256").update(String(token)).digest("hex");
}

export function createSessionToken() {
  return crypto.randomBytes(32).toString("base64url");
}

export function parseCookies(req) {
  const header = req.headers?.cookie || req.headers?.Cookie || "";
  const out = {};
  String(header)
    .split(";")
    .forEach((part) => {
      const i = part.indexOf("=");
      if (i < 0) return;
      const k = part.slice(0, i).trim();
      const v = part.slice(i + 1).trim();
      if (k) out[k] = decodeURIComponent(v);
    });
  return out;
}

export function learnerCookieOptions(maxAgeSec) {
  const secure =
    String(process.env.NODE_ENV || "").toLowerCase() === "production" ||
    Boolean((process.env.VERCEL || "").trim());
  const parts = [
    `${LEARNER_COOKIE}=`,
    "Path=/",
    "HttpOnly",
    "SameSite=Lax",
    `Max-Age=${Math.max(0, maxAgeSec | 0)}`,
  ];
  if (secure) parts.push("Secure");
  return parts;
}

export function setLearnerCookieHeader(token, maxAgeSec) {
  const base = learnerCookieOptions(maxAgeSec);
  base[0] = `${LEARNER_COOKIE}=${encodeURIComponent(token)}`;
  return base.join("; ");
}

export function clearLearnerCookieHeader() {
  const base = learnerCookieOptions(0);
  base[0] = `${LEARNER_COOKIE}=`;
  return base.join("; ");
}

export function signLearnerMagicToken(email, ttlMinutes = 30) {
  const secret = learnerMagicSecret();
  if (!secret) throw new Error("magic_secret_missing");
  const now = Math.floor(Date.now() / 1000);
  return signPortalMagicJwt(
    {
      aud: LEARNER_AUD,
      email: String(email).toLowerCase(),
      kind: "learner-login",
      iat: now,
      exp: now + Math.max(5, ttlMinutes) * 60,
    },
    secret
  );
}

export function verifyLearnerMagicToken(token) {
  const secret = learnerMagicSecret();
  if (!secret) return null;
  const payload = verifyPortalMagicJwt(token, secret);
  if (!payload || payload.aud !== LEARNER_AUD) return null;
  const now = Math.floor(Date.now() / 1000);
  if (typeof payload.exp !== "number" || payload.exp <= now) return null;
  if (payload.kind !== "learner-login") return null;
  const email = String(payload.email || "").toLowerCase();
  if (!email) return null;
  return { email, exp: payload.exp };
}

export async function redeemLearnerLogin(email) {
  const learner = await upsertLearnerByEmail(email);
  const token = createSessionToken();
  const tokenHash = hashSessionToken(token);
  const expiresAt = new Date(Date.now() + LEARNER_SESSION_DAYS * 24 * 60 * 60 * 1000);
  await createLearnerSession(learner.id, tokenHash, expiresAt);
  return {
    learner,
    token,
    expiresAt,
    cookie: setLearnerCookieHeader(token, LEARNER_SESSION_DAYS * 24 * 60 * 60),
  };
}

export async function learnerFromRequest(req) {
  const cookies = parseCookies(req);
  const token = cookies[LEARNER_COOKIE];
  if (!token) return null;
  const learner = await getLearnerBySessionHash(hashSessionToken(token));
  if (!learner) return null;
  return { ...learner, sessionToken: token };
}

export async function logoutLearnerRequest(req) {
  const cookies = parseCookies(req);
  const token = cookies[LEARNER_COOKIE];
  if (token) await deleteLearnerSession(hashSessionToken(token));
  return clearLearnerCookieHeader();
}
