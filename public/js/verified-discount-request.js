/**
 * Verified learner discount request form.
 * Reuses the visitor question email-verification pipeline so admin review only sees verified inboxes.
 */
(function () {
  "use strict";

  var formOpenedAt = Date.now();

  var PERSONAL_DOMAINS = {
    "aol.com": true,
    "gmail.com": true,
    "googlemail.com": true,
    "hotmail.com": true,
    "icloud.com": true,
    "live.com": true,
    "mac.com": true,
    "me.com": true,
    "msn.com": true,
    "outlook.com": true,
    "pm.me": true,
    "proton.me": true,
    "protonmail.com": true,
    "tutanota.com": true,
    "yahoo.com": true,
    "ymail.com": true,
    "zoho.com": true,
  };

  var METHOD_COPY = {
    edu: "School email (.edu)",
    mil: "Military email (.mil)",
    gov: "Government email (.gov)",
    contractor_mailbox: "Government-issued contractor mailbox",
    employer_domain: "Approved contractor/employer domain",
    partner_code: "Partner or program code",
    manual_review: "Manual review",
  };

  function emailParts(raw) {
    var email = String(raw || "").trim().toLowerCase();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || email.length > 254) {
      return null;
    }
    var at = email.lastIndexOf("@");
    return {
      email: email,
      local: email.slice(0, at),
      domain: email.slice(at + 1),
    };
  }

  function isPersonalDomain(domain) {
    return Boolean(PERSONAL_DOMAINS[String(domain || "").toLowerCase()]);
  }

  function endsWithSuffix(domain, suffix) {
    return String(domain || "").toLowerCase().endsWith(suffix);
  }

  function hasContractorMarker(parts) {
    var local = parts.local;
    var email = parts.email;
    return local.indexOf(".ctr") !== -1 || local.indexOf(".civ") !== -1 || local.indexOf("v-") === 0 || email.indexOf("v-") === 0;
  }

  function setStatus(statusEl, message, className) {
    if (!statusEl) return;
    statusEl.textContent = message;
    statusEl.className = "verified-discount-status" + (className ? " " + className : "");
  }

  function fieldValue(form, name) {
    var el = form.elements[name];
    return el ? String(el.value || "").trim() : "";
  }

  function validateEligibilityEmail(method, eligibilityEmail) {
    var parts = emailParts(eligibilityEmail);
    if (!parts) return "Enter a valid eligibility email address.";

    if (method === "partner_code" || method === "manual_review") {
      return "";
    }

    if (method === "edu") {
      if (!endsWithSuffix(parts.domain, ".edu")) return "School email verification requires an eligibility email ending in .edu.";
      return "";
    }

    if (method === "mil") {
      if (!endsWithSuffix(parts.domain, ".mil")) return "Military email verification requires an eligibility email ending in .mil.";
      return "";
    }

    if (method === "gov") {
      if (!endsWithSuffix(parts.domain, ".gov")) return "Government email verification requires an eligibility email ending in .gov.";
      return "";
    }

    if (method === "contractor_mailbox") {
      if (isPersonalDomain(parts.domain)) {
        return "Use partner or manual review for personal email domains.";
      }
      if ((endsWithSuffix(parts.domain, ".mil") || endsWithSuffix(parts.domain, ".gov")) && hasContractorMarker(parts)) {
        return "";
      }
      if (!endsWithSuffix(parts.domain, ".edu") && !endsWithSuffix(parts.domain, ".mil") && !endsWithSuffix(parts.domain, ".gov")) {
        return "";
      }
      return "Contractor mailbox verification needs a .mil/.gov contractor marker such as .ctr, .civ, or v-, or a non-personal employer domain for review.";
    }

    if (method === "employer_domain") {
      if (isPersonalDomain(parts.domain)) {
        return "Approved contractor/employer domain review cannot use a common personal email domain.";
      }
      return "";
    }

    return "Choose a verification method.";
  }

  function buildMessage(data) {
    var lines = [
      "Verified learner discount request",
      "",
      "Admin action: After this eligibility inbox is verified, review the request and manually create/send the appropriate Stripe discount code if approved. The verified learner discount is not one-time only; it may be reused by the approved learner for eligible products added later, using the same verified checkout email. Do not auto-create Stripe codes from this submission.",
      "",
      "Learner group: " + data.learnerGroup,
      "Verification method: " + (METHOD_COPY[data.verificationMethod] || data.verificationMethod),
      "Eligibility email verified by link: " + data.eligibilityEmail,
      "Discount/access email: " + data.accessEmail,
      "Organization/program: " + (data.organization || "Not provided"),
      "Notes: " + (data.notes || "Not provided"),
      "Page path: " + data.pagePath,
    ];
    return lines.join("\n").slice(0, 2000);
  }

  function init() {
    var form = document.getElementById("verifiedDiscountRequestForm");
    if (!form) return;

    var statusEl = document.getElementById("verifiedDiscountStatus");
    var methodEl = document.getElementById("verifiedDiscountMethod");
    var hintEl = document.getElementById("verifiedDiscountMethodHint");

    function refreshHint() {
      if (!hintEl || !methodEl) return;
      var method = methodEl.value;
      if (method === "partner_code" || method === "manual_review") {
        hintEl.textContent = "Personal domains are allowed for this method, but the request will be reviewed before any discount code is sent.";
      } else if (method === "contractor_mailbox") {
        hintEl.textContent = "Government contractor mailboxes can use .mil/.gov patterns with .ctr, .civ, or v-, or a non-personal employer domain for review.";
      } else if (method === "employer_domain") {
        hintEl.textContent = "Use a non-personal employer or contractor domain. Common personal domains are sent to manual review instead.";
      } else {
        hintEl.textContent = "Automated email checks require the matching .edu, .mil, or .gov suffix for the selected method.";
      }
    }

    if (methodEl) {
      methodEl.addEventListener("change", refreshHint);
      refreshHint();
    }

    form.addEventListener("submit", function (event) {
      event.preventDefault();

      var learnerGroup = fieldValue(form, "learner_group");
      var verificationMethod = fieldValue(form, "verification_method");
      var eligibilityEmail = fieldValue(form, "eligibility_email");
      var accessEmail = fieldValue(form, "access_email");
      var organization = fieldValue(form, "organization");
      var notes = fieldValue(form, "notes").slice(0, 700);
      var consent = form.elements.consent && form.elements.consent.checked;
      var hp = fieldValue(form, "company_website");
      var submitBtn = form.querySelector('button[type="submit"]');

      if (!learnerGroup || !verificationMethod) {
        setStatus(statusEl, "Choose a learner group and verification method.", "err");
        return;
      }

      var eligibilityError = validateEligibilityEmail(verificationMethod, eligibilityEmail);
      if (eligibilityError) {
        setStatus(statusEl, eligibilityError, "err");
        return;
      }

      if (!emailParts(accessEmail)) {
        setStatus(statusEl, "Enter a valid discount/access email address.", "err");
        return;
      }

      if (!consent) {
        setStatus(statusEl, "Please confirm you want a verification link emailed for eligibility review.", "err");
        return;
      }

      setStatus(statusEl, "Sending verification email...", "");
      if (submitBtn) submitBtn.disabled = true;

      fetch("/api/sample-lead", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          action: "request_question_verification",
          email: emailParts(eligibilityEmail).email,
          product: "secplus",
          message: buildMessage({
            learnerGroup: learnerGroup,
            verificationMethod: verificationMethod,
            eligibilityEmail: emailParts(eligibilityEmail).email,
            accessEmail: emailParts(accessEmail).email,
            organization: organization,
            notes: notes,
            pagePath: location.pathname + (location.search || ""),
          }),
          page_path: location.pathname + (location.search || ""),
          company_website: hp,
          consent: true,
          form_opened_at: formOpenedAt,
        }),
      })
        .then(function (response) {
          return response.json().then(function (body) {
            return { ok: response.ok, body: body };
          });
        })
        .then(function (result) {
          if (!result.ok || !result.body || result.body.ok === false) {
            var err = (result.body && (result.body.error || result.body.reason)) || "Could not send verification email.";
            throw new Error(err);
          }
          setStatus(
            statusEl,
            "Check your eligibility email. After you verify, your discount request is sent for review. If approved, we will send the discount code and access setup to the email you listed.",
            "ok"
          );
          form.reset();
          refreshHint();
        })
        .catch(function (err) {
          setStatus(statusEl, err.message || "Something went wrong. Try again in a moment.", "err");
        })
        .finally(function () {
          if (submitBtn) submitBtn.disabled = false;
        });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
