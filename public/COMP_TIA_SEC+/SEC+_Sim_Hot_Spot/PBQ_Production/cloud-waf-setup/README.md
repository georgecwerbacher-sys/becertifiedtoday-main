# Sec+ Cloud Web Application Firewall Setup

**SY0-701 PBQ · Ticket #bct2026**

Four-tab cloud WAF console (General Settings, Security Rules, Custom Rule, Logging & Monitoring).

## Section

| File | Part |
|------|------|
| `sections/cloud-waf-setup.html` | Sample ticket + WAF console |

## Answer key

| Tab | Setting | Correct value |
|-----|---------|---------------|
| General | Domain Name | `BeCertifiedToday.com` |
| General | Protocol | HTTPS |
| General | WAF Policy Name | `ProductionPolicy` |
| Security Rules | Baseline Rule Set | OWASP Top 10 |
| Custom Rule | Rule Name | `CrossSiteScripting` |
| Custom Rule | Match Condition | XSS |
| Custom Rule | Action | Block |
| Logging | Logging Level | Verbose |

## Chain

- **Previous:** [`../governance/`](../governance/governance.html)
- **Next:** *(end of production chain)*

## Preview

```text
http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/cloud-waf-setup/cloud-waf-setup.html
```

See `../VERIFICATION.md` for answer audit.
