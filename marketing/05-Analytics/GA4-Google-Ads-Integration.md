# GA4 ↔ Google Ads integration

**Property:** GA4 `G-YTT6KBHX7V` (site default in `public/js/ga-site-config.js`)

---

## 1. Link accounts

1. Google Ads → **Tools & settings** → **Linked accounts** → **Google Analytics (GA4)**  
2. Link the GA4 property for becertifiedtoday.com  
3. Enable **Import site metrics** and **Auto-tagging** (gclid)

## 2. Mark conversions (GA4 → Ads)

In **GA4 → Admin → Events**, toggle as conversions:

| Event | When it fires | Priority |
|-------|---------------|----------|
| `begin_checkout` | User clicks a purchase / Stripe CTA | Primary (proxy until purchase event) |
| `purchase` | Stripe return / confirmed payment (add when available) | Primary |
| `generate_lead` | Optional: email capture if added later | Secondary |

In **Google Ads → Goals → Conversions**, import from GA4.

## 3. Attribution script (repo)

Loaded on marketing pages after gtag:

```html
<script src="/js/campaign-attribution.js"></script>
```

Purchase buttons should use `data-bcc-track="begin_checkout"` (or class `bcc-track-checkout`).

## 4. Enhanced conversions (optional, later)

If you collect email at checkout, enable enhanced conversions in Ads + GA4 for better matching.

## 5. Audiences (week 4+)

GA4 audiences to create:

- Visited `/ccna-home.html` — no `begin_checkout` (7 days)  
- Started checkout — no purchase (if purchase event exists)  

Export to Ads for remarketing when traffic supports it.

## 6. Admin dashboard

Internal: `/admin/analytics.html` (Vercel analytics / portal metrics — not a substitute for Ads UI).

## 7. Weekly reconciliation

| Source | Metric |
|--------|--------|
| Google Ads | Clicks, cost, imported conversions |
| GA4 | Sessions by `utm_campaign`, `begin_checkout` count |
| Stripe | Successful payments $ |

Log discrepancies in [[../06-Content-Calendar/Weekly-Review-Template]].

#analytics #ga4 #google-ads
