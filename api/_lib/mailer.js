import { requireEnv } from "./config.js";

function trimBaseUrl(value) {
  return String(value || "").replace(/\/+$/, "");
}

export function getVerifyBaseUrl() {
  return trimBaseUrl(process.env.MAGIC_LINK_VERIFY_BASE_URL || requireEnv("PUBLIC_SITE_URL"));
}

export async function sendMagicLinkEmail({ toEmail, url }) {
  const apiKey = process.env.RESEND_API_KEY;
  const sender = process.env.MAGIC_LINK_FROM_EMAIL;

  if (!apiKey || !sender) {
    console.warn(
      "Magic link email provider not configured. Set RESEND_API_KEY and MAGIC_LINK_FROM_EMAIL.",
      { toEmail, url }
    );
    return { delivered: false, provider: "none" };
  }

  const helpUrl = `${getVerifyBaseUrl()}/cert-access-help.html`;
  const textBody = [
    "Your ENCOR access is ready. Open this link once to sign in (it expires after a short time for security):",
    url,
    "",
    "Coming back later or using another device?",
    "That email link only works once. Anytime during your 30-day access, open this page and request a new sign-in link with the same email you used at checkout:",
    helpUrl,
    "",
    "Bookmark that page so you can always get back in without buying again.",
  ].join("\n");

  const htmlBody = `<p>Your ENCOR access is ready.</p>
<p><a href="${url}">Sign in to ENCOR (open this link once)</a></p>
<p><strong>Coming back later?</strong> The link in this email is one-time. To return on another browser or device, use our access help page—same email as checkout, no second payment:</p>
<p><a href="${helpUrl}">${helpUrl}</a></p>
<p>Bookmark that page so you can request a fresh sign-in link anytime during your active access period.</p>`;

  const response = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      from: sender,
      to: [toEmail],
      subject: "Your ENCOR access link",
      text: textBody,
      html: htmlBody,
    }),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Failed sending magic link email: ${response.status} ${text}`);
  }

  return { delivered: true, provider: "resend" };
}

export { getEncorAppBaseUrl } from "./encor-app-url.js";
