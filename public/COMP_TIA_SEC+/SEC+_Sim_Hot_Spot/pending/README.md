# Security+ PBQ — pending (reference only)

**New work** goes in **`../PBQ_Production/`**. Publish to **`../../SEC+_PBQ/`** when ready.

As of 2026-06-05, unique staged scenarios were **ported to production** (#13–#21). Duplicates were **removed** (see below). This folder keeps the drag-and-drop skeleton only.

## Removed (duplicates — covered in production)

| Removed pending file | Production replacement |
|----------------------|------------------------|
| `security-control-map.html` | `security-control-placement/` (three-zone control map) |
| `siem-security-alerts-dashboard.html` | `siem-ransomware-mitre/` (full SIEM + MITRE + containment) |
| `zero-trust.html` *(earlier)* | `zero-trust-zta-migration/` |

## Ported to production (#13–#21)

| Former pending file | Production folder |
|---------------------|-------------------|
| `log-timeline-forensics.html` | `log-timeline-forensics/` |
| `pki-certificate-chain-browser-error.html` | `pki-certificate-chain-browser-error/` |
| `phishing-email-analysis.html` | `phishing-email-analysis/` |
| `vulnerability-management.html` | `vulnerability-management/` |
| `incident-response.html` | `incident-response/` |
| `quantitative-risk-ale.html` | `quantitative-risk-ale/` |
| `malware-ioc-analysis.html` | `malware-ioc-analysis/` |
| `data-protection.html` | `data-protection/` |
| `governance.html` | `governance/` |

PBQ notes: `data/secplus-pbq/{slug}/`

## Remaining in this folder

| File | Role |
|------|------|
| `TEMPLATE-dragdrop.html` | Copy skeleton for new drag-and-drop PBQs (not in nav) |

## Preview (production)

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/acme-rag-hr-ai/acme-rag-hr-ai.html
```
