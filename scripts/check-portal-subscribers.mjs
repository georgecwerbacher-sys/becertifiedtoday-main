#!/usr/bin/env node
/**
 * Step 1 gate check before retiring CCNA / ENCOR tracks.
 *
 * Usage (from repo root):
 *   STRIPE_SECRET_KEY=sk_live_... node scripts/check-portal-subscribers.mjs
 *
 * Exits 0 only when CCNA and ENCOR have zero active subscribers
 * after filtering internal/test emails (GA_INTERNAL_EMAILS).
 */
import Stripe from "stripe";
import { getStripeSecretKey } from "../server-lib/stripe-secret-key.js";
import { listAllPortalSubscribersFromStripe } from "../server-lib/portal-subscribers-stripe.js";
import { filterPortalSubscriberRows } from "../server-lib/analytics-internal.js";

function summarizeTrack(track, block) {
  const active = filterPortalSubscriberRows(block.active);
  const expired = filterPortalSubscriberRows(block.expired);
  return { track, active, expired, activeEmails: active.map((r) => r.email) };
}

const sk = getStripeSecretKey(process.env.STRIPE_SECRET_KEY);
if (!sk.secret) {
  console.error("Set STRIPE_SECRET_KEY (live or test) and rerun.");
  console.error("Or verify in /admin → Active portal access (all time).");
  process.exit(2);
}

const stripe = new Stripe(sk.secret);
const listed = await listAllPortalSubscribersFromStripe(stripe);
const tracks = ["ccna", "encor", "secplus"].map((track) =>
  summarizeTrack(track, listed[track])
);

console.log("Portal subscribers (internal emails excluded)\n");
for (const row of tracks) {
  console.log(
    `${row.track.padEnd(8)} active=${row.active.length}  expired=${row.expired.length}`
  );
  if (row.activeEmails.length) {
    for (const email of row.activeEmails) {
      console.log(`  - ${email}`);
    }
  }
}
console.log(`\nStripe customers scanned: ${listed.customersScanned}`);
if (listed.scanTruncated) {
  console.warn("Warning: Stripe customer scan was truncated.");
}

const ccnaEncorActive = tracks
  .filter((t) => t.track === "ccna" || t.track === "encor")
  .reduce((sum, t) => sum + t.active.length, 0);

if (ccnaEncorActive === 0) {
  console.log("\nOK: No active CCNA or ENCOR portal subscribers.");
  process.exit(0);
}

console.error(`\nBLOCKED: ${ccnaEncorActive} active CCNA/ENCOR subscriber(s) remain.`);
process.exit(1);
