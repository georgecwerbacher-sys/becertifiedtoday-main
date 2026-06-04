# Security+ PBQ — pending (staged)

Legacy staged PBQs (reference / copy patterns). **New work** goes in **`../PBQ_Production/`**. Publish to **`../../SEC+_PBQ/`**. Pages here are **noindex**.

## Chain (Back / Next order)

| File | Layout |
|------|--------|
| `security-control-map.html` | Token bank → layer blocks + drop slots |
| `log-timeline-forensics.html` | Token bank → numbered timeline |
| `pki-certificate-chain-browser-error.html` | Exhibit + multiple choice |
| `siem-security-alerts-dashboard.html` | SIEM exhibit + multiple choice |
| `phishing-email-analysis.html` | Email exhibit + fill-in drag-and-drop |
| `vulnerability-management.html` | Scanner exhibit + multiple choice |
| `incident-response.html` | NIST IR timeline + fill-in drag-and-drop |
| `quantitative-risk-ale.html` | ALE worksheet + multiple choice |
| `malware-ioc-analysis.html` | Malware IOC console + multiple choice |
| `data-protection.html` | Data classification exhibit + multiple choice |
| `governance.html` | Governance exhibit + multiple choice (end of chain) |
| `TEMPLATE-dragdrop.html` | Copy skeleton (not in nav) |

**Zero Trust (merged):** full 3-part scenario lives in [`../PBQ_Production/zero-trust-zta-migration/`](../PBQ_Production/zero-trust-zta-migration/) (exhibit + zone map + trade-offs). `pending/zero-trust.html` removed.

## Preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/pending/{slug}.html
```

## Publish

1. Move `{slug}.html` to `../../SEC+_PBQ/`.
2. Replace `/SEC+_Sim_Hot_Spot/pending/` with `/SEC+_PBQ/` in canonical and nav links.
3. Run lint and `npm run sync:sitemap`.
