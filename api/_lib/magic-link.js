import { MAGIC_LINK_TTL_MINUTES, SESSION_TTL_DAYS, normalizeEmail } from "./config.js";
import { createOpaqueToken, kvDel, kvGet, kvSetEx } from "./kv.js";

function magicTokenKey(token) {
  return `encor:magic:${token}`;
}

function sessionTokenKey(token) {
  return `encor:session:${token}`;
}

export async function createMagicLinkToken(emailInput) {
  const email = normalizeEmail(emailInput);
  if (!email) {
    throw new Error("Cannot create magic link token without email");
  }
  const token = createOpaqueToken();
  const ttlSeconds = Math.max(60, Math.floor(MAGIC_LINK_TTL_MINUTES * 60));
  await kvSetEx(magicTokenKey(token), ttlSeconds, email);
  return token;
}

export async function consumeMagicLinkToken(tokenInput) {
  const token = String(tokenInput || "").trim();
  if (!token) return null;
  const email = await kvGet(magicTokenKey(token));
  if (!email) return null;
  await kvDel(magicTokenKey(token));
  return email;
}

export async function createSessionToken(emailInput) {
  const email = normalizeEmail(emailInput);
  if (!email) return null;
  const token = createOpaqueToken();
  const ttlSeconds = Math.max(3600, Math.floor(SESSION_TTL_DAYS * 24 * 60 * 60));
  await kvSetEx(sessionTokenKey(token), ttlSeconds, email);
  return token;
}

export async function readSessionEmail(tokenInput) {
  const token = String(tokenInput || "").trim();
  if (!token) return null;
  return kvGet(sessionTokenKey(token));
}
