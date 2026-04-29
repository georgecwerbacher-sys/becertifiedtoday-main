import { requireEnv } from "./config.js";

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
      text: `Your ENCOR access is ready. Open this magic link: ${url}\n\nThis link expires soon. If it expires, complete checkout again from the Renew Access button.`,
      html: `<p>Your ENCOR access is ready.</p><p><a href="${url}">Open ENCOR with your magic link</a></p><p>This link expires soon. If it expires, use the Renew Access button to generate a new one after payment.</p>`,
    }),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Failed sending magic link email: ${response.status} ${text}`);
  }

  return { delivered: true, provider: "resend" };
}

function trimBaseUrl(value) {
  return String(value || "").replace(/\/+$/, "");
}

export function getVerifyBaseUrl() {
  return trimBaseUrl(process.env.MAGIC_LINK_VERIFY_BASE_URL || requireEnv("PUBLIC_SITE_URL"));
}

export { getEncorAppBaseUrl } from "./encor-app-url.js";
