---
type: website
page: email-verification-setup
site: becertifiedtoday.com
status: planning
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

The public message should stay simple:

> Use your school, work, military, government, or partner email to verify eligibility. At checkout, use the email where you want to receive account and access links.

Do not over-explain why a learner may use a different checkout email. Keep it practical.

---

## Guiding rules

1. Verification is for discount eligibility only.
2. Standard checkout and access should stay familiar and low friction.
3. Discounts are not first-time visitor promos, welcome coupons, homepage banners, popups, or broad paid Search CTAs.
4. Each verified email or partner code should create one single-use discount.
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
3. Learner enters a school, work, military, government, contractor, or partner email.
4. System checks the domain or partner code.
5. If eligible, system sends a one-time verification link to that email.
6. Learner clicks the verification link.
7. System creates a single-use Stripe promotion code or checkout link.
8. Learner checks out using the email they want for account and access links.
9. Stripe metadata records the verification group and source.
10. The normal portal access flow continues from checkout.

Keep the public copy short. The page does not need to explain every backend step.

---

## Form fields

Required:

- Learner group
- Verification email or partner code
- Consent checkbox for eligibility check

Optional:

- Organization name
- Role selection for `.edu` users: student, educator, staff, program lead
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

When the email passes the first check:

1. Create a random one-time token.
2. Store a hash of the token, not the raw token.
3. Set expiration to 15 to 30 minutes.
4. Rate limit sends by email, IP, and domain.
5. Send a plain email with one verification link.
6. Mark token as used after click.

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

After verification succeeds:

1. Identify the discount category.
2. Create or retrieve the matching single-use promotion code.
3. Attach metadata:
   - `verification_group`
   - `verification_domain`
   - `verification_method`
   - `partner_code` when present
4. Redirect to Stripe Checkout or show the code.
5. Mark the verification record as redeemed after successful checkout webhook.

Do not expose reusable public codes.

---

## Abuse controls

- One active token per email at a time.
- One redeemed discount per verification email per product period.
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

---

## Launch checklist

- [ ] Build verification form
- [ ] Create allowed domain and partner code config
- [ ] Create email token table or storage
- [ ] Add rate limits
- [ ] Send verification email
- [ ] Connect verified result to Stripe promotion code or checkout link
- [ ] Add Stripe metadata
- [ ] Add webhook to mark redemption
- [ ] Add manual review path
- [ ] Test `.edu`, `.mil`, `.gov`, contractor pattern, partner code, and rejected personal-domain cases
- [ ] Keep `/verified-learner-discounts.html` out of paid Search sitelinks and homepage promo CTAs
- [x] Keep the informational page indexed and live in top navigation
- [ ] Launch the actual verification form only when email verification and Stripe discount handling are ready

---

## Public copy rule

Use simple wording:

> Verify with your eligible school, work, military, government, or partner email. At checkout, use the email where you want to receive account and access links.

Avoid wording that sounds like a workaround, a privacy warning, or a reason not to trust the flow.
