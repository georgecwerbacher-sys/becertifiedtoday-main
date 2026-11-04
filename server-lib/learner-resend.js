/**
 * Learner account magic-link email via Resend.
 */

export async function sendLearnerLoginEmail({ to, magicUrl }) {
  const key = (process.env.RESEND_API_KEY || "").trim();
  if (!key) {
    console.warn("[learner-account] RESEND_API_KEY unset — skipping login email");
    return false;
  }

  const escapeHtml = (s) =>
    String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const escapeAttr = (s) =>
    String(s).replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");

  const from =
    (process.env.RESEND_FROM || "").trim() ||
    "Be Certified Today <onboarding@resend.dev>";

  const subject =
    (process.env.RESEND_LEARNER_LOGIN_SUBJECT || "").trim() ||
    "Your Be Certified Today account link";

  const plainUrl = escapeHtml(magicUrl);

  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${key}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      from,
      to: [to],
      subject,
      html: `<p>Sign in to your Be Certified Today learner profile to track results, schedule exams, and practice weak areas:</p>
<p><a href="${escapeAttr(magicUrl)}"><strong>Open my account</strong></a></p>
<p>If the button does not work, paste this URL into your browser:</p>
<p style="word-break:break-all;font-size:13px;color:#444">${plainUrl}</p>
<p>This link expires in about 30 minutes. You can request a new one from the account login page anytime.</p>`,
    }),
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    console.error("[learner-account] Resend error:", res.status, text.slice(0, 500));
    throw new Error("Resend rejected email: HTTP " + res.status);
  }
  return true;
}
