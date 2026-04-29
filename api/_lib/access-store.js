import { ACCESS_WINDOW_DAYS, normalizeEmail } from "./config.js";
import { kvDel, kvGet, kvSet, kvSAdd, kvSIsMember, kvSRem, kvSMembers } from "./kv.js";

function accessKey(email) {
  return `encor:access:${email}`;
}

function customerIndexKey(customerId) {
  return `encor:customer:${customerId}`;
}

function sessionIndexKey(sessionId) {
  return `encor:checkout:${sessionId}`;
}

function refundedSetKey() {
  return "encor:refunded-emails";
}

export async function getAccessRecord(emailInput) {
  const email = normalizeEmail(emailInput);
  if (!email) return null;
  const raw = await kvGet(accessKey(email));
  return raw ? JSON.parse(raw) : null;
}

export async function grantAccess({
  email: emailInput,
  stripeCustomerId,
  checkoutSessionId,
  accessDays = ACCESS_WINDOW_DAYS,
}) {
  const email = normalizeEmail(emailInput);
  if (!email) throw new Error("Cannot grant access without email");

  const now = Date.now();
  const current = await getAccessRecord(email);
  const currentExpiryMs = current?.access_expires_at ? Date.parse(current.access_expires_at) : 0;
  const baseMs = Number.isFinite(currentExpiryMs) && currentExpiryMs > now ? currentExpiryMs : now;
  const extendedMs = baseMs + accessDays * 24 * 60 * 60 * 1000;

  const record = {
    email,
    stripe_customer_id: stripeCustomerId || current?.stripe_customer_id || null,
    checkout_session_id: checkoutSessionId || current?.checkout_session_id || null,
    access_expires_at: new Date(extendedMs).toISOString(),
  };

  await kvSet(accessKey(email), JSON.stringify(record));
  if (stripeCustomerId) {
    await kvSet(customerIndexKey(stripeCustomerId), email);
  }
  if (checkoutSessionId) {
    await kvSet(sessionIndexKey(checkoutSessionId), email);
  }
  await kvSRem(refundedSetKey(), email);
  return record;
}

export async function revokeAccessByEmail(emailInput) {
  const email = normalizeEmail(emailInput);
  if (!email) return;
  const current = await getAccessRecord(email);
  if (current?.stripe_customer_id) {
    await kvDel(customerIndexKey(current.stripe_customer_id));
  }
  if (current?.checkout_session_id) {
    await kvDel(sessionIndexKey(current.checkout_session_id));
  }
  await kvDel(accessKey(email));
  await kvSAdd(refundedSetKey(), email);
}

export async function revokeAccessByCustomerId(customerId) {
  if (!customerId) return;
  const email = await kvGet(customerIndexKey(customerId));
  if (email) {
    await revokeAccessByEmail(email);
  }
}

export async function lookupEmailBySessionId(sessionId) {
  if (!sessionId) return null;
  return kvGet(sessionIndexKey(sessionId));
}

export async function getRefundedEmails() {
  return kvSMembers(refundedSetKey());
}

export async function isRefundedEmail(emailInput) {
  const email = normalizeEmail(emailInput);
  if (!email) return false;
  return kvSIsMember(refundedSetKey(), email);
}
