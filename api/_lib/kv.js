import crypto from "node:crypto";
import { requireEnv } from "./config.js";

function getKvConfig() {
  return {
    url: requireEnv("KV_REST_API_URL"),
    token: requireEnv("KV_REST_API_TOKEN"),
  };
}

async function kvRequest(parts) {
  const { url, token } = getKvConfig();
  const path = parts.map((part) => encodeURIComponent(String(part))).join("/");
  const response = await fetch(`${url}/${path}`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`KV request failed (${response.status}): ${text}`);
  }

  const payload = await response.json();
  return payload.result;
}

export async function kvGet(key) {
  return kvRequest(["get", key]);
}

export async function kvSet(key, value) {
  return kvRequest(["set", key, value]);
}

export async function kvSetEx(key, seconds, value) {
  return kvRequest(["setex", key, seconds, value]);
}

export async function kvDel(key) {
  return kvRequest(["del", key]);
}

export async function kvSAdd(key, member) {
  return kvRequest(["sadd", key, member]);
}

export async function kvSRem(key, member) {
  return kvRequest(["srem", key, member]);
}

export async function kvSMembers(key) {
  return kvRequest(["smembers", key]);
}

export async function kvSIsMember(key, member) {
  const result = await kvRequest(["sismember", key, member]);
  return result === 1;
}

export async function kvSetNxEx(key, value, seconds) {
  const result = await kvRequest(["set", key, value, "NX", "EX", seconds]);
  return result === "OK";
}

export function createOpaqueToken() {
  return crypto.randomBytes(24).toString("base64url");
}
