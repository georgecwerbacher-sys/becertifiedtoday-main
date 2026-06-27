---
type: website
page: email-verification-setup
site: becertifiedtoday.com
status: v1-live-reuses-question-verification
tags:
  - marketing
  - becertifiedtoday
  - discounts
  - verification
  - email
related:
  - "[[Verified Learner Discounts]]"
  - "[[../Sec+ Campaign/Sec+ Phase 2 Institutional Targeting|Sec+ Phase 2 Institutional Targeting]]"
---

# Email verification setup

Purpose: set up a simple eligibility check for verified learner discounts without making the site feel complicated or suspicious.

V1 implementation: `/verified-learner-discounts.html` now has a visible verified discount request form. It reuses the existing Ask-a-question email verification/admin pipeline:

1. The form posts to `/api/sample-lead` with `action: "request_question_verification"` and `product: "secplus"`.
2. The existing Resend email sends the verification link to the eligibility email.
3. The existing `/verify-question.html` confirmation flow stores the verified request in the visitor-question admin queue.
4. Admin manually reviews the structured request and manually creates/sends the Stripe discount code if approved.

Stripe promotion-code creation is deliberately not automated in v1.

The public message should stay simple:

> Use your school, work, military, government, or partner email to verify eligibility. At checkout, use the email where you want to receive account and access links.

Do not over-explain why a learner may use a different checkout email. Keep it practical.

---

## Guiding rules

1. Verification is for discount eligibility only.
2. Standard checkout and access should stay familiar and low friction.
3. Discounts are not first-time visitor promos, welcome coupons, homepage banners, popups, or broad paid Search CTAs.
4. Each verified email or partner code should create a standing verified-learner discount tied to the checkout email.
5. Personal domains like Gmail, iCloud, Yahoo, and Outlook should not pass automated email verification unless paired with a valid partner code or manual approval.
6. Store only what is needed to verify and prevent abuse.

---

## Eligible verification methods

| Method | Groups | Notes |
|--------|--------|-------|
| `.edu` email | Students, educators | Ask learner to choose student or educator on the form. |
| `.mil` email | Active-duty military, Guard, Reserve | Use for military eligibility. |
| `.gov` email | Federal, state, local government, first responders | Include agency employees and eligible public safety users. |
| Government-issued contractor mailbox | DoD and federal contractors | Look for allowed domains and markers such as `.ctr`, `.civ`, or `v-`. |
| Approved contractor domain | Government contractors | Maintain a private allowlist. |
| Partner referral code | Workforce, veteran, transition, school, and job placement programs | Lets a coordinator verify learners who may not have an institutional email. |
| Manual review | Edge cases | Use only when automated checks are not enough. |

---

## User flow

1. Learner opens `/verified-learner-discounts.html`.
2. Learner selects an eligible group.
3. Learner enters a school, work, military, government, contractor, partner, or manual-review eligibility email.
4. Browser validation checks the selected method against the email pattern where possible.
5. If eligible, system sends a one-time verification link to that email.
6. Learner clicks the verification link.
7. The verified request enters the existing admin queue.
8. Admin manually creates and sends the Stripe discount code and access setup if approved.
9. Learner checks out using the email they want for account and access links.
10. The normal portal access flow continues from checkout.

Keep the public copy short. The page does not need to explain every backend step.

---

## Form fields

Required:

- Learner group
- Verification method
- Eligibility email
- Discount/access email
- Consent checkbox for eligibility check

Optional:

- Organization name
- Notes for manual review

Do not ask for documents in v1 unless manual review is active.

---

## Backend checks

### Domain check

Normalize the verification email:

1. Lowercase the domain.
2. Trim whitespace.
3. Reject disposable email domains.
4. Reject personal domains for automated email verification.
5. Match domain or mailbox pattern against the allowed rules.

Starter allow rules:

- Ends with `.edu`
- Ends with `.mil`
- Ends with `.gov`
- Matches approved contractor domains
- Matches approved government contractor mailbox patterns
- Has a valid partner code

### Contractor patterns

Examples to support:

```text
[firstname].[lastname].[identifier]@[domain].mil
[firstname].[initial].[lastname].[identifier]@[domain].mil
v-[name]@[agency.gov]
```

Common markers:

- `.ctr`
- `.civ`
- `v-`

Do not publish the full contractor allowlist on the public site.

---

## Verification token

V1 reuses the existing visitor-question verification token. When the form passes the first browser-side check:

1. Create the existing signed verification token.
2. Set expiration to 24 hours, matching Ask-a-question.
3. Send one verification link through the existing Resend setup.
4. Store the request only after the learner clicks the verification link.

Suggested email subject:

```text
Verify your Be Certified Today learner discount
```

Suggested email body:

```text
Click the link below to verify eligibility for a Be Certified Today learner discount.

This link expires soon and can only be used once.

[Verify eligibility]
```

---

## Stripe discount creation

V1 is manual. After verification succeeds:

1. Identify the discount category.
2. Review the structured admin message.
3. Manually create or retrieve the matching promotion code in Stripe.
4. Send the discount code and access setup to the discount/access email listed by the learner.
5. Tell the learner the code is tied to the email they use at Stripe checkout and should not be shared.
6. Tell the learner the approved discount is not one-time only. It can be used again for eligible Be Certified Today products added later, using the same verified checkout email.

Do not expose public codes. Reuse is for the verified learner, not for sharing.

### Active manual Stripe promotion codes

Use these only after the eligibility request is verified in the admin queue. Do not add these codes to public HTML, paid Search copy, homepage banners, or payment popups.
When sending a code, include: "Thank you for the service you provide. This verified learner discount is tied to the email you use at Stripe checkout. It is not a one-time offer, and you may use it again for eligible Be Certified Today products added later. Do not share it. Shared codes may fail checkout or be disabled."

| Product | Group | Coupon / promotion name | Code | Discount | Notes |
|---------|-------|-------------------------|------|----------|-------|
| Security+ 30-day access | Student | `Students_Sec+` | `SEC178936543128RANDOM` | 35% | Send only after student eligibility is verified. |
| Security+ 30-day access | Educator | `EDU_Sec+` | `SEC177966543128RANDOM` | 30% | Send only after educator eligibility is verified. |
| Security+ 30-day access | Military | `Mil_Sec+` | `SEC187966543128RANDOM` | 40% | Send only after military eligibility is verified. |
| CCNA access | Student | `Students_CCNA` | `CCNA178936549188RANDOM` | 35% | Send only after student eligibility is verified. |
| CCNA access | Educator | `EDU_CCNA` | `CCNA177966543128RANDOM` | 30% | Send only after educator eligibility is verified. |
| CCNA access | Military | `Mil_CCNA` | `CCNA187966543128RANDOM` | 40% | Send only after military eligibility is verified. |

---

## Abuse controls

- One active token per email at a time.
- Track redemptions by verification email and product so misuse can be reviewed without blocking legitimate repeat use.
- Rate limit by IP and domain.
- Block disposable email domains.
- Keep a manual review queue for mismatches.
- Log failed attempts without storing sensitive documents.
- Do not allow the same partner code to generate unlimited unchecked redemptions.

---

## Admin view needed

Minimum useful fields:

- Verification email domain
- Group selected
- Verification method
- Status: pending, verified, redeemed, rejected, expired
- Created date
- Redeemed date
- Stripe checkout/session ID
- Partner code if used
- Manual review notes

Avoid showing full raw tokens or unnecessary learner documents.

V1 stores these fields inside the structured message in the existing visitor-question admin queue rather than adding a new database table.

---

## Launch checklist

- [x] Build verification form
- [ ] Create allowed domain and partner code config
- [x] Reuse existing visitor-question email token flow
- [ ] Add dedicated rate limits
- [x] Send verification email through existing Resend setup
- [x] Keep Stripe discount code creation manual in v1
- [ ] Add Stripe metadata if automation is built later
- [ ] Add webhook to mark redemption if automation is built later
- [x] Add manual review path through existing admin queue
- [x] Test `.edu`, `.mil`, `.gov`, contractor pattern, partner/manual review, and rejected personal-domain cases at the client-validation level
- [ ] Keep `/verified-learner-discounts.html` out of paid Search sitelinks and homepage promo CTAs
- [x] Keep the informational page indexed and live in top navigation
- [x] Launch v1 verification form with manual Stripe handling

---

## Public copy rule

Use simple wording:

> Verify with your eligible school, work, military, government, or partner email. At checkout, use the email where you want to receive account and access links.

Avoid wording that sounds like a workaround, a privacy warning, or a reason not to trust the flow.
