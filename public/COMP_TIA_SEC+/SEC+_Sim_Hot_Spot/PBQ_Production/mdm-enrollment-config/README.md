# SEC+ MDM Enrollment Configuration

**SY0-701 PBQ · BeCertifiedToday MDM console**

Four-tab MDM console (HTTPS Certificate, iOS Compliance, Application Restrictions, Enrollment Settings). Configure TLS, iOS compliance, app lockdown, and Apple ADE for corporate-owned iOS devices.

## Answer key

| Tab | Setting | Correct value |
|-----|---------|---------------|
| HTTPS | HTTPS Certificate | Enabled |
| HTTPS | Domain/Hostname | `mdm.becertifiedtoday.com` |
| HTTPS | Certificate File | `/mnt/certs/BCTMDMCertificate.pfx` |
| iOS | Minimum iOS Version | `17` (one major behind iOS 18) |
| iOS | Password Requirement | Enabled |
| iOS | Minimum Password Length | `6` |
| iOS | Password Reuse | Disabled |
| iOS | Auto-lock | Enabled |
| iOS | Auto-lock Timeout (seconds) | `60` |
| iOS | Jailbreak and Rooting Alerts | Enabled |
| iOS | Jailbreak Alert Email | `alerts@mdm.becertifiedtoday.com` |
| Apps | Application Restrictions | Enabled |
| Apps | Allow App Store | Disabled |
| Apps | Allow Installing Unmanaged Apps | Disabled |
| Apps | Force Automatic App Updates | Enabled |
| Enrollment | Enrollment Method | Automated Device Enrollment (ADE) |
| Enrollment | ADE Server Token File | `/mnt/certs/AdeServerToken.p7m` |
| Enrollment | Device Supervision | Enabled |
| Enrollment | Allow Profile Removal | Disabled |

**Status:** Production — chain #28, linked on `SEC+_Training_Portal.html` (Hardening & Vulnerability Mgmt).

## Chain

- **Previous:** [`../public-wlan-guest-config/`](../public-wlan-guest-config/public-wlan-guest-config.html)
- **Next:** [`../network-protocols-matching/`](../network-protocols-matching/network-protocols-matching.html)

## Preview

http://localhost:3000/COMP_TIA_SEC+/SEC+_Sim_Hot_Spot/PBQ_Production/mdm-enrollment-config/mdm-enrollment-config.html

Rebuild after section edits: `npm run build:pbq-suite`
