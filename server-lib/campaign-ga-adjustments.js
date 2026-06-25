/**
 * Manual GA4 display adjustments stored on campaign plan state (e.g. owner test checkouts).
 * GA4 historical events cannot be deleted; these subtract from admin/tracker totals only.
 */

export function normalizeGaAdjustments(raw) {
  if (!raw || typeof raw !== "object") return null;
  const landingBeginCheckout = Number(raw.landingBeginCheckout);
  if (!Number.isFinite(landingBeginCheckout) || landingBeginCheckout <= 0) return null;
  return {
    landingBeginCheckout: Math.floor(landingBeginCheckout),
    notes: typeof raw.notes === "string" ? raw.notes.trim().slice(0, 500) : "",
  };
}

/**
 * Subtract test checkout counts from daily auto rows (newest days first).
 * @param {Record<string, { landingBeginCheckout?: number, landingPageViews?: number, landingCheckoutRate?: number|null }>} autoByDate
 * @param {string[]} dates ascending ISO dates in plan window
 * @param {number} deduction
 */
export function distributeLandingCheckoutDeduction(autoByDate, dates, deduction) {
  let remaining = Math.max(0, Math.floor(Number(deduction) || 0));
  if (!remaining || !autoByDate) return 0;

  const sorted = [...(dates || [])].sort().reverse();
  for (const date of sorted) {
    if (remaining <= 0) break;
    const row = autoByDate[date];
    if (!row) continue;
    const cur = Number(row.landingBeginCheckout || 0);
    if (cur <= 0) continue;
    const sub = Math.min(cur, remaining);
    row.landingBeginCheckout = cur - sub;
    remaining -= sub;
    const lpv = Number(row.landingPageViews || 0);
    row.landingCheckoutRate = lpv > 0 ? row.landingBeginCheckout / lpv : null;
  }
  return Math.max(0, Math.floor(Number(deduction) || 0) - remaining);
}

/**
 * @param {number} count
 * @param {{ landingBeginCheckout?: number }|null|undefined} adjustments
 */
export function adjustLandingBeginCheckoutCount(count, adjustments) {
  const raw = Number(count || 0);
  const deduction = Number(adjustments?.landingBeginCheckout || 0);
  if (!Number.isFinite(deduction) || deduction <= 0) return raw;
  return Math.max(0, raw - Math.floor(deduction));
}
