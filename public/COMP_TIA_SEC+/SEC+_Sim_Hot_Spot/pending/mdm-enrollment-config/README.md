# Mobile Device Management Enrollment

**SY0-701 PBQ · Acme Corporation**

Four-tab MDM console (HTTPS Certificate, iOS Compliance, Application Restrictions, Enrollment Settings). Paraphrased from common Security+ MDM enrollment PBQ patterns.

## Answer key

| Tab | Setting | Correct value |
|-----|---------|---------------|
| HTTPS | HTTPS Certificate | Enabled |
| HTTPS | Domain/Hostname | `mdm.acmecorp.com` |
| HTTPS | Certificate File | `/mnt/certs/AcmeMDMCertificate.pfx` |
| iOS | Minimum iOS Version | `17` (one major behind iOS 18) |
| iOS | Password Requirement | Enabled |
| iOS | Minimum Password Length | `6` |
| iOS | Password Reuse | Disabled |
| iOS | Auto-lock | Enabled |
| iOS | Auto-lock Timeout (seconds) | `60` |
| iOS | Jailbreak and Rooting Alerts | Enabled |
| iOS | Jailbreak Alert Email | `alerts@mdm.acmecorp.com` |
| Apps | Application Restrictions | Enabled |
| Apps | Allow App Store | Disabled |
| Apps | Allow Installing Unmanaged Apps | Disabled |
| Apps | Force Automatic App Updates | Enabled |
| Enrollment | Enrollment Method | Automated Device Enrollment (ADE) |
| Enrollment | ADE Server Token File | `/mnt/certs/AdeServerToken.p7m` |
| Enrollment | Device Supervision | Enabled |
| Enrollment | Allow Profile Removal | Disabled |

**Status:** Pending — not in `PBQ_Production` build chain.

## Pending chain

- **Previous:** [`../PBQ_Production/cloud-waf-setup/`](../PBQ_Production/cloud-waf-setup/cloud-waf-setup.html) *(production)*
- **Next:** [`../siem-alert-settings-config/`](../siem-alert-settings-config/)

## Preview

http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/pending/mdm-enrollment-config/mdm-enrollment-config.html
