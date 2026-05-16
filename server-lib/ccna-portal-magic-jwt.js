/**
 * HS256 JWT for CCNA portal magic links (short-lived claim mirrors portal window end).
 */
import crypto from "crypto";

function b64urlEncodeJson(obj) {
  return Buffer.from(JSON.stringify(obj))
    .toString("base64")
    .replace(/=/g, "")
    .replace(/\+/g, "-")
    .replace(/\//g, "_");
}

function b64urlDecodeToString(str) {
  let s = str.replace(/-/g, "+").replace(/_/g, "/");
  while (s.length % 4) s += "=";
  return Buffer.from(s, "base64").toString("utf8");
}

function signSegment(seg1, seg2, secret) {
  return crypto
    .createHmac("sha256", secret)
    .update(`${seg1}.${seg2}`)
    .digest("base64")
    .replace(/=/g, "")
    .replace(/\+/g, "-")
    .replace(/\//g, "_");
}

/**
 * @param {{ aud: string, cs: string, exp: number }} payloadObj — exp = unix seconds (JWT standard)
 */
export function signPortalMagicJwt(payloadObj, secret) {
  const header = { alg: "HS256", typ: "JWT" };
  const encHeader = b64urlEncodeJson(header);
  const encPayload = b64urlEncodeJson(payloadObj);
  const sig = signSegment(encHeader, encPayload, secret);
  return `${encHeader}.${encPayload}.${sig}`;
}

function base64UrlToBuffer(s) {
  let x = String(s).replace(/-/g, "+").replace(/_/g, "/");
  while (x.length % 4) x += "=";
  return Buffer.from(x, "base64");
}

/** @returns {Record<string, unknown>|null} */
export function verifyPortalMagicJwt(token, secret) {
  if (typeof token !== "string" || !token.includes(".")) return null;
  const parts = token.split(".");
  if (parts.length !== 3) return null;
  const [encHeader, encPayload, sigEnc] = parts;
  const expected = signSegment(encHeader, encPayload, secret);
  let sigBuf;
  let expBuf;
  try {
    sigBuf = base64UrlToBuffer(sigEnc);
    expBuf = base64UrlToBuffer(expected);
  } catch {
    return null;
  }
  if (sigBuf.length !== expBuf.length || !crypto.timingSafeEqual(sigBuf, expBuf)) return null;
  try {
    return JSON.parse(b64urlDecodeToString(encPayload));
  } catch {
    return null;
  }
}
