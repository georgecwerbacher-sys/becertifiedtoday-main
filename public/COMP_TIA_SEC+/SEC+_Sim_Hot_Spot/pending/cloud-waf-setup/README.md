# Cloud Web Application Firewall Setup

**SY0-701 PBQ · Ticket #983498**

Four-tab cloud WAF console (General Settings, Security Rules, Custom Rule, Logging & Monitoring). Paraphrased from common Security+ cloud WAF PBQ patterns.

## Answer key

| Tab | Setting | Correct value |
|-----|---------|---------------|
| General | Domain Name | `example.com` |
| General | Protocol | HTTPS |
| General | WAF Policy Name | `ProductionPolicy` |
| Security Rules | Baseline Rule Set | OWASP Top 10 |
| Custom Rule | Rule Name | `CrossSiteScripting` |
| Custom Rule | Match Condition | XSS |
| Custom Rule | Action | Block |
| Logging | Logging Level | Verbose |

**Status:** Pending — not in `PBQ_Production` build chain.

## Pending chain

- **Previous:** `../public-wlan-guest-config/`
- **Next:** [`../mdm-enrollment-config/`](../mdm-enrollment-config/)

## Preview

http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/pending/cloud-waf-setup/cloud-waf-setup.html
