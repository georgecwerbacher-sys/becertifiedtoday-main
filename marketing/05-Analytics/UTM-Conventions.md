# UTM conventions (Google Ads)

Use the same pattern on every final URL so GA4 reports stay readable.

## Standard parameters

| Parameter | Value | Example |
|-----------|-------|---------|
| `utm_source` | `google` | google |
| `utm_medium` | `cpc` | cpc |
| `utm_campaign` | campaign slug (lowercase, hyphens) | `ccna-search-exam-intent` |
| `utm_content` | ad group slug | `exam-simulation` |
| `utm_term` | keyword (optional in URL; Ads can auto-fill) | `{keyword}` ValueTrack |

## Final URL template

```
https://becertifiedtoday.com/ccna-home.html?utm_source=google&utm_medium=cpc&utm_campaign=ccna-search-exam-intent&utm_content=exam-simulation&utm_term={keyword}
```

In Google Ads, set **Account → Settings → Auto-tagging** = ON (adds `gclid`). Keep UTMs anyway for reporting clarity in GA4.

## Campaign slug registry

| Google Ads campaign | `utm_campaign` |
|---------------------|----------------|
| CCNA Brand | `ccna-search-brand` |
| CCNA Exam intent | `ccna-search-exam-intent` |
| CCNP Exam intent | `ccnp-search-exam-intent` |

## Site behavior

`public/js/campaign-attribution.js`:

1. Reads `utm_*` and `gclid` on landing  
2. Stores in `sessionStorage` for the session  
3. Sends GA4 events with campaign params on checkout clicks  

## Stripe note

Payment Links do not automatically receive UTMs. Conversion truth = GA4 events + Stripe dashboard until checkout API passes metadata.

#analytics #utm
