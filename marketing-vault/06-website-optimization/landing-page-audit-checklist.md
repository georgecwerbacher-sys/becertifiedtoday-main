---
type: checklist
use: before-deploy-and-weekly
---

# Landing page audit checklist

Run this for every URL used as a **Google Ads final URL**. Copy scores into the page note under `pages/`.

**Page URL:**  
**Date:**  
**Auditor:**  
**Campaign / utm_campaign:**

---

## A. Message match (Ad relevance + LP experience)

- [ ] H1 and hero copy match primary ad keywords for this ad group
- [ ] First screen mentions **Security+ / SY0-701** (or product-specific cert) where relevant
- [ ] Ad promise (free sample, pricing, no subscription) visible without scrolling on mobile
- [ ] No conflicting offers (e.g. “coming soon” blocking purchase if ads say “buy now”)
- [ ] CTA button text matches intent (“Get 30-day access”, “Try free sample”)

**Score (1–5):** ___  
**Notes:**

---

## B. Content quality

- [ ] Clear value proposition in first 2 paragraphs
- [ ] Benefits list (bullets) — specific, not generic filler
- [ ] Sample / demo path obvious for top-of-funnel ads
- [ ] Purchase section (`#purchase`) complete: prices, durations, what’s included
- [ ] Spelling and grammar pass
- [ ] Meta title + description match page content (search snippet sanity)

**Score (1–5):** ___  
**Notes:**

---

## C. Mobile & UX

- [ ] Readable font size on phone (no horizontal scroll)
- [ ] Primary CTA thumb-reachable
- [ ] Header/nav doesn’t hide main message
- [ ] Forms/buttons not broken on iOS Safari
- [ ] Images have alt text where meaningful

**Score (1–5):** ___  
**Notes:**

---

## D. Speed & technical

- [ ] PageSpeed Insights mobile score noted: ___
- [ ] Largest images lazy-loaded or reasonably sized
- [ ] GA4 + campaign-attribution scripts present on paid landing pages
- [ ] Checkout tracking wired (`begin_checkout` on purchase buttons)
- [ ] Canonical URL correct in `<head>`

**Score (1–5):** ___  
**Notes:**

---

## E. Trust & transparency

- [ ] Prices shown in USD before leaving site for Stripe
- [ ] Access duration clear (10-day / 30-day / one-time sim)
- [ ] “No subscription” or billing terms clear if claimed in ads
- [ ] Site branding (logo, name) visible
- [ ] No misleading certification claims

**Score (1–5):** ___  
**Notes:**

---

## F. Post-click behavior (GA4 — last 7 days)

Fill from weekly report or GA4:

| Metric | Value |
|--------|------:|
| Sessions | |
| Engagement rate | |
| Avg engagement time | |
| begin_checkout events | |

**Notes:**

---

## Summary

| Section | Score |
|---------|------:|
| A Message match | |
| B Content | |
| C Mobile/UX | |
| D Speed | |
| E Trust | |
| **Average** | |

### Top 3 fixes (implement in Cursor → `public/`)

1.
2.
3.

### Deployed?

- [ ] Changes committed
- [ ] Vercel production deploy
- [ ] Logged in [[content-change-log|content change log]]

### Re-check Ads (date + ~7 days later)

- [ ] Landing page experience: Below avg / Average / Above avg
- [ ] Quality Score movement noted in page file
