/**
 * Marketing lead magnet delivery via Resend (optional when RESEND_API_KEY unset).
 */

const LEAD_MAGNETS = {
  "secplus-free-simulation": {
    logTag: "secplus-lead",
    subjectEnv: "RESEND_SECPLUS_FREE_SIM_SUBJECT",
    defaultSubject: "Your free Security+ simulation is ready",
    path: "/COMP_TIA_SEC+/test-simulation-runner.html?free=1",
    title: "free Security+ timed simulation",
    audienceEnv: "RESEND_SECPLUS_MARKETING_AUDIENCE_ID",
  },
  "ccna-free-simulation": {
    logTag: "ccna-lead",
    subjectEnv: "RESEND_CCNA_FREE_SIM_SUBJECT",
    defaultSubject: "Your free CCNA timed simulation is ready",
    path: "/CCNA_Sim_EXAM/free-assessment.html?welcome=1",
    title: "free CCNA timed simulation",
    audienceEnv: "RESEND_CCNA_MARKETING_AUDIENCE_ID",
  },
  "encor-free-simulation": {
    logTag: "encor-lead",
    subjectEnv: "RESEND_ENCOR_FREE_SIM_SUBJECT",
    defaultSubject: "Your free ENCOR timed simulation is ready",
    path: "/sample?track=encor-free-sim&welcome=1",
    title: "free ENCOR timed simulation",
    audienceEnv: "RESEND_ENCOR_MARKETING_AUDIENCE_ID",
  },
};

function escapeHtml(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function escapeAttr(s) {
  return String(s).replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");
}

export function resolveLeadMagnet(magnetId) {
  const id = String(magnetId || "").trim();
  return LEAD_MAGNETS[id] || null;
}

export async function addMarketingContact({ email, magnet }) {
  const key = (process.env.RESEND_API_KEY || "").trim();
  const audienceId = (process.env[magnet.audienceEnv] || "").trim();
  if (!key || !audienceId) return false;

  const res = await fetch(`https://api.resend.com/audiences/${encodeURIComponent(audienceId)}/contacts`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${key}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email,
      unsubscribed: false,
    }),
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    console.warn(`[${magnet.logTag}] Resend audience contact:`, res.status, text.slice(0, 300));
    return false;
  }
  return true;
}

export async function sendLeadMagnetEmail({ to, magnet, resourceUrl }) {
  const key = (process.env.RESEND_API_KEY || "").trim();
  if (!key) {
    console.warn(`[${magnet.logTag}] RESEND_API_KEY unset — skipping lead magnet email`);
    return false;
  }

  const from =
    (process.env.RESEND_FROM || "").trim() ||
    "Be Certified Today <onboarding@resend.dev>";

  const subject =
    (process.env[magnet.subjectEnv] || "").trim() || magnet.defaultSubject;

  const safeHref = resourceUrl.replace(/"/g, "%22");
  const plainUrl = escapeHtml(resourceUrl);

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
      html: `<p>Thanks for signing up for the <strong>${escapeHtml(magnet.title)}</strong> on Be Certified Today.</p>
<p>Start your free timed sample now:</p>
<p><a href="${escapeAttr(resourceUrl)}"><strong>Start free Security+ simulation</strong></a></p>
<p style="word-break:break-all;font-size:13px;color:#444">${plainUrl}</p>
<p>The sample includes multiple-choice items plus a performance-based simulation, with a <strong>study scorecard</strong> at the end. Email the scorecard to yourself from the results screen.</p>
<p style="font-size:13px;color:#666">Exam prep only — not affiliated with CompTIA. You received this because you opted in on our Security+ landing page.</p>`,
    }),
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    console.error(`[${magnet.logTag}] Resend error:`, res.status, text.slice(0, 500));
    throw new Error("Resend rejected email: HTTP " + res.status);
  }
  return true;
}
