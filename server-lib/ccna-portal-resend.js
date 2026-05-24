/**
 * Send portal magic-link email via Resend REST API (optional — skips when RESEND_API_KEY unset).
 */

export async function sendCcnaPortalMagicEmail({ to, magicUrl }) {
  const key = (process.env.RESEND_API_KEY || "").trim();
  if (!key) {
    console.warn("[ccna-portal] RESEND_API_KEY unset — skipping magic-link email");
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
    (process.env.RESEND_CCNA_PORTAL_SUBJECT || "").trim() ||
    "Your CCNA training portal link";

  const safeHref = magicUrl.replace(/"/g, "%22");
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
      html: `<p>Open your CCNA training portal on any device during your paid access window:</p>
<p><a href="${escapeAttr(magicUrl)}"><strong>Open CCNA training portal</strong></a></p>
<p>If the button does not work, paste this URL into your browser:</p>
<p style="word-break:break-all;font-size:13px;color:#444">${plainUrl}</p>
<p>This link stops working when your paid access window ends. While access is still active, you can request another email from the CCNA portal restore page.</p>`,
    }),
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    console.error("[ccna-portal] Resend error:", res.status, text.slice(0, 500));
    throw new Error("Resend rejected email: HTTP " + res.status);
  }
  return true;
}

export async function sendEncorPortalMagicEmail({ to, magicUrl }) {
  const key = (process.env.RESEND_API_KEY || "").trim();
  if (!key) {
    console.warn("[encor-portal] RESEND_API_KEY unset — skipping magic-link email");
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
    (process.env.RESEND_ENCOR_PORTAL_SUBJECT || "").trim() ||
    "Your CCNP ENCOR training portal link";

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
      html: `<p>Open your CCNP ENCOR training portal on any device during your paid access window:</p>
<p><a href="${escapeAttr(magicUrl)}"><strong>Open ENCOR training portal</strong></a></p>
<p>If the button does not work, paste this URL into your browser:</p>
<p style="word-break:break-all;font-size:13px;color:#444">${plainUrl}</p>
<p>This link stops working when your paid access window ends. While access is still active, you can request another email from the ENCOR portal restore page.</p>`,
    }),
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    console.error("[encor-portal] Resend error:", res.status, text.slice(0, 500));
    throw new Error("Resend rejected email: HTTP " + res.status);
  }
  return true;
}
