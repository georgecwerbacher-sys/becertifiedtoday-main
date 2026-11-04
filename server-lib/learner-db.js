/**
 * Learner account storage.
 * Primary: Upstash Redis / Vercel KV (already on this project).
 * Optional fallback: Vercel Postgres when POSTGRES_URL is set.
 */
import crypto from "crypto";
import { Redis } from "@upstash/redis";

export const TRACKS = ["ccna", "encor", "secplus", "ccnaauto"];
export const FREE_DAILY_GENERATED_CAP = 20;
export const LEARNER_COOKIE = "bcc_learner";
export const LEARNER_SESSION_DAYS = 30;

let redisClient = null;

export function normalizeEmail(raw) {
  const s = typeof raw === "string" ? raw.trim().toLowerCase() : "";
  if (!s || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s)) return "";
  return s;
}

export function isValidTrack(track) {
  return TRACKS.includes(String(track || "").trim().toLowerCase());
}

export function kvConfigured() {
  return Boolean(
    ((process.env.KV_REST_API_URL || "").trim() &&
      (process.env.KV_REST_API_TOKEN || "").trim()) ||
      ((process.env.UPSTASH_REDIS_REST_URL || "").trim() &&
        (process.env.UPSTASH_REDIS_REST_TOKEN || "").trim())
  );
}

export function postgresConfigured() {
  // Kept for API compatibility — true when any backed store is ready.
  return kvConfigured() || Boolean(
    (process.env.POSTGRES_URL || "").trim() ||
      (process.env.DATABASE_URL || "").trim() ||
      (process.env.POSTGRES_PRISMA_URL || "").trim()
  );
}

function getRedis() {
  if (redisClient) return redisClient;
  const url =
    (process.env.KV_REST_API_URL || "").trim() ||
    (process.env.UPSTASH_REDIS_REST_URL || "").trim();
  const token =
    (process.env.KV_REST_API_TOKEN || "").trim() ||
    (process.env.UPSTASH_REDIS_REST_TOKEN || "").trim();
  if (!url || !token) throw new Error("kv_not_configured");
  redisClient = new Redis({ url, token });
  return redisClient;
}

function newId() {
  return crypto.randomUUID();
}

function emailKey(email) {
  return `bcc:learner:email:${normalizeEmail(email)}`;
}
function learnerKey(id) {
  return `bcc:learner:${id}`;
}
function sessionKey(tokenHash) {
  return `bcc:learner:session:${tokenHash}`;
}
function attemptsKey(learnerId) {
  return `bcc:learner:attempts:${learnerId}`;
}
function scheduleKey(learnerId, track) {
  return `bcc:learner:schedule:${learnerId}:${track}`;
}
function usageKey(learnerId, day) {
  return `bcc:learner:usage:${learnerId}:${day}`;
}

export async function upsertLearnerByEmail(email) {
  const e = normalizeEmail(email);
  if (!e) throw new Error("invalid_email");
  const redis = getRedis();
  let id = await redis.get(emailKey(e));
  const now = new Date().toISOString();
  if (id) {
    const existing = (await redis.get(learnerKey(id))) || {};
    const learner = {
      id,
      email: e,
      created_at: existing.created_at || now,
      last_login_at: now,
    };
    await redis.set(learnerKey(id), learner);
    return learner;
  }
  id = newId();
  const learner = {
    id,
    email: e,
    created_at: now,
    last_login_at: now,
  };
  await redis.set(emailKey(e), id);
  await redis.set(learnerKey(id), learner);
  return learner;
}

export async function createLearnerSession(learnerId, tokenHash, expiresAt) {
  const redis = getRedis();
  const ttlSec = Math.max(
    60,
    Math.floor((expiresAt.getTime() - Date.now()) / 1000)
  );
  await redis.set(
    sessionKey(tokenHash),
    { learner_id: learnerId, expires_at: expiresAt.toISOString() },
    { ex: ttlSec }
  );
}

export async function getLearnerBySessionHash(tokenHash) {
  if (!tokenHash) return null;
  const redis = getRedis();
  const sess = await redis.get(sessionKey(tokenHash));
  if (!sess || !sess.learner_id) return null;
  if (sess.expires_at && Date.parse(sess.expires_at) <= Date.now()) {
    await redis.del(sessionKey(tokenHash));
    return null;
  }
  const learner = await redis.get(learnerKey(sess.learner_id));
  if (!learner) return null;
  return {
    id: learner.id,
    email: learner.email,
    created_at: learner.created_at,
    last_login_at: learner.last_login_at,
    session_expires_at: sess.expires_at,
  };
}

export async function deleteLearnerSession(tokenHash) {
  if (!tokenHash) return;
  const redis = getRedis();
  await redis.del(sessionKey(tokenHash));
}

export async function deleteExpiredLearnerSessions() {
  // TTL on session keys handles expiry in Redis.
}

/**
 * @param {string} learnerId
 * @param {Array<{track:string,mode?:string,item_id:string,domain?:string,correct:boolean,meta?:object,answered_at?:string}>} attempts
 */
export async function insertPracticeAttempts(learnerId, attempts) {
  if (!Array.isArray(attempts) || !attempts.length) return 0;
  const redis = getRedis();
  let n = 0;
  for (const a of attempts.slice(0, 200)) {
    const track = String(a.track || "").toLowerCase();
    if (!isValidTrack(track)) continue;
    const itemId = String(a.item_id || a.itemId || "").trim();
    if (!itemId) continue;
    const mode = String(a.mode || "bank").toLowerCase();
    const safeMode = ["bank", "sim", "sample", "retry", "generated"].includes(mode)
      ? mode
      : "bank";
    const domain = a.domain != null ? String(a.domain).slice(0, 32) : null;
    const correct = Boolean(a.correct);
    const answeredAt =
      a.answered_at && !Number.isNaN(Date.parse(a.answered_at))
        ? new Date(a.answered_at).toISOString()
        : new Date().toISOString();
    const row = {
      track,
      mode: safeMode,
      item_id: itemId,
      domain,
      correct,
      answered_at: answeredAt,
      meta: a.meta && typeof a.meta === "object" ? a.meta : {},
    };
    await redis.lpush(attemptsKey(learnerId), JSON.stringify(row));
    n += 1;
  }
  // Keep a bounded history per learner.
  await redis.ltrim(attemptsKey(learnerId), 0, 4999);
  return n;
}

async function loadAttempts(learnerId) {
  const redis = getRedis();
  const raw = await redis.lrange(attemptsKey(learnerId), 0, 4999);
  const out = [];
  for (const item of raw || []) {
    if (!item) continue;
    if (typeof item === "object") {
      out.push(item);
      continue;
    }
    try {
      out.push(JSON.parse(item));
    } catch (_) {}
  }
  return out;
}

export async function getResultsAggregate(learnerId) {
  const attempts = await loadAttempts(learnerId);
  const tracks = {};
  for (const t of TRACKS) {
    tracks[t] = {
      attempts: 0,
      correct: 0,
      accuracy: null,
      weakDomains: [],
    };
  }
  const domainMap = {};
  for (const a of attempts) {
    const track = a.track;
    if (!tracks[track]) continue;
    tracks[track].attempts += 1;
    if (a.correct) tracks[track].correct += 1;
    const domain = a.domain && String(a.domain).trim() ? String(a.domain) : "unknown";
    const key = track + "::" + domain;
    if (!domainMap[key]) {
      domainMap[key] = { track, domain, attempts: 0, correct: 0 };
    }
    domainMap[key].attempts += 1;
    if (a.correct) domainMap[key].correct += 1;
  }
  for (const t of TRACKS) {
    const att = tracks[t].attempts;
    tracks[t].accuracy = att ? Math.round((1000 * tracks[t].correct) / att) / 10 : null;
  }
  const byTrackDomains = {};
  Object.values(domainMap).forEach((d) => {
    if (!byTrackDomains[d.track]) byTrackDomains[d.track] = [];
    byTrackDomains[d.track].push({
      domain: d.domain,
      attempts: d.attempts,
      correct: d.correct,
      accuracy: d.attempts ? Math.round((1000 * d.correct) / d.attempts) / 10 : 0,
    });
  });
  for (const t of TRACKS) {
    tracks[t].weakDomains = (byTrackDomains[t] || [])
      .sort((a, b) => a.accuracy - b.accuracy || b.attempts - a.attempts)
      .slice(0, 8);
  }
  return { tracks };
}

export async function upsertExamSchedule(learnerId, track, examDate, notes) {
  const t = String(track || "").toLowerCase();
  if (!isValidTrack(t)) throw new Error("invalid_track");
  const dateStr = String(examDate || "").trim();
  if (!/^\d{4}-\d{2}-\d{2}$/.test(dateStr)) throw new Error("invalid_date");
  const note = String(notes || "").slice(0, 500);
  const redis = getRedis();
  const now = new Date().toISOString();
  const existing = (await redis.get(scheduleKey(learnerId, t))) || {};
  const row = {
    id: existing.id || newId(),
    track: t,
    exam_date: dateStr,
    notes: note,
    created_at: existing.created_at || now,
    updated_at: now,
  };
  await redis.set(scheduleKey(learnerId, t), row);
  return row;
}

export async function listExamSchedules(learnerId) {
  const redis = getRedis();
  const out = [];
  for (const t of TRACKS) {
    const row = await redis.get(scheduleKey(learnerId, t));
    if (row) out.push(row);
  }
  out.sort((a, b) => String(a.exam_date).localeCompare(String(b.exam_date)));
  return out;
}

export async function getWeakItemIds(learnerId, track, limit = 20) {
  const t = String(track || "").toLowerCase();
  if (!isValidTrack(t)) return [];
  const attempts = await loadAttempts(learnerId);
  const map = {};
  for (const a of attempts) {
    if (a.track !== t) continue;
    const id = String(a.item_id || "");
    if (!id) continue;
    if (!map[id]) map[id] = { misses: 0, attempts: 0 };
    map[id].attempts += 1;
    if (!a.correct) map[id].misses += 1;
  }
  return Object.entries(map)
    .filter(([, v]) => v.misses > 0)
    .sort((a, b) => b[1].misses - a[1].misses || b[1].attempts - a[1].attempts)
    .slice(0, Math.min(Math.max(limit, 1), 50))
    .map(([id]) => id);
}

export async function getWeakDomains(learnerId, track, limit = 3) {
  const t = String(track || "").toLowerCase();
  if (!isValidTrack(t)) return [];
  const agg = await getResultsAggregate(learnerId);
  return (agg.tracks[t]?.weakDomains || [])
    .slice(0, Math.min(Math.max(limit, 1), 6))
    .map((d) => d.domain);
}

export async function bumpDailyGeneratedUsage(learnerId, count) {
  const day = new Date().toISOString().slice(0, 10);
  const add = Math.max(0, Math.min(Number(count) || 0, FREE_DAILY_GENERATED_CAP));
  const redis = getRedis();
  const key = usageKey(learnerId, day);
  const next = await redis.incrby(key, add);
  await redis.expire(key, 60 * 60 * 48);
  return Number(next) || add;
}

export async function getDailyGeneratedUsage(learnerId) {
  const day = new Date().toISOString().slice(0, 10);
  const redis = getRedis();
  const n = await redis.get(usageKey(learnerId, day));
  return Number(n) || 0;
}
