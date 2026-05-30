/**
 * Email Security+ simulation scorecard summary via Resend.
 */

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function renderScorecardEmailHtml(payload, siteUrl) {
  var p = payload || {};
  var passLabel = p.passed ? "Pass" : "Did not pass";
  var domainRows = (p.domains || [])
    .map(function (d) {
      return (
        "<tr><td style=\"padding:8px 10px;border:1px solid #e2e8f0;\">" +
        escapeHtml(d.title) +
        "</td><td style=\"padding:8px 10px;border:1px solid #e2e8f0;\">" +
        d.correct +
        " / " +
        d.total +
        " (" +
        d.pct +
        "%)</td><td style=\"padding:8px 10px;border:1px solid #e2e8f0;\">" +
        escapeHtml(d.priority) +
        "</td></tr>"
      );
    })
    .join("");

  var weakItems = (p.weakObjectives || [])
    .slice(0, 8)
    .map(function (o) {
      return (
        "<li><strong>" +
        escapeHtml(o.id) +
        "</strong> — " +
        o.pct +
        "% (" +
        o.correct +
        "/" +
        o.total +
        ") · " +
        escapeHtml(o.topic) +
        "</li>"
      );
    })
    .join("");

  var sampleNote = p.isFreeSample
    ? "<p style=\"font-size:14px;color:#475569;\">This was a <strong>free sample simulation</strong> (shorter than the full 90-minute SY0-701 timed test on Be Certified Today).</p>"
    : "";

  var practiceUrl = siteUrl + "/comptia-sec+-home.html#purchase";

  return (
    "<div style=\"font-family:Inter,Arial,sans-serif;color:#0b1020;line-height:1.55;max-width:640px;\">" +
    "<h1 style=\"font-size:22px;margin:0 0 12px;\">Your Security+ SY0-701 scorecard</h1>" +
    sampleNote +
    "<p style=\"font-size:16px;margin:0 0 16px;\"><strong>Scaled score:</strong> " +
    p.scaledScore +
    " / " +
    p.scaledMax +
    " — " +
    passLabel +
    " (passing " +
    p.passingScore +
    ")</p>" +
    "<p style=\"font-size:14px;color:#475569;margin:0 0 20px;\">Multiple-choice: " +
    p.mcqCorrect +
    "/" +
    p.mcqTotal +
    " · Simulations &amp; hot spots: " +
    p.simCorrect +
    "/" +
    p.simTotal +
    "</p>" +
    "<h2 style=\"font-size:16px;margin:0 0 8px;\">Domain focus</h2>" +
    "<table style=\"width:100%;border-collapse:collapse;font-size:14px;margin:0 0 20px;\">" +
    "<thead><tr><th style=\"text-align:left;padding:8px 10px;border:1px solid #e2e8f0;background:#f8fafc;\">Domain</th>" +
    "<th style=\"text-align:left;padding:8px 10px;border:1px solid #e2e8f0;background:#f8fafc;\">Score</th>" +
    "<th style=\"text-align:left;padding:8px 10px;border:1px solid #e2e8f0;background:#f8fafc;\">Priority</th></tr></thead>" +
    "<tbody>" +
    domainRows +
    "</tbody></table>" +
    (weakItems
      ? "<h2 style=\"font-size:16px;margin:0 0 8px;\">Objectives to review</h2><ul style=\"margin:0 0 20px;padding-left:20px;font-size:14px;\">" +
        weakItems +
        "</ul>"
      : "") +
    "<p style=\"margin:0 0 16px;\"><a href=\"" +
    escapeHtml(practiceUrl) +
    "\" style=\"color:#2f66bf;font-weight:700;\">Continue SY0-701 exam prep →</a></p>" +
    "<p style=\"font-size:12px;color:#64748b;\">Be Certified Today — independent Security+ exam prep. Not affiliated with CompTIA.</p>" +
    "</div>"
  );
}

export async function sendSecplusScorecardEmail({ to, payload, siteUrl }) {
  const key = (process.env.RESEND_API_KEY || "").trim();
  if (!key) {
    console.warn("[secplus-scorecard] RESEND_API_KEY unset — skipping scorecard email");
    return false;
  }

  const from =
    (process.env.RESEND_FROM || "").trim() ||
    "Be Certified Today <onboarding@resend.dev>";

  const subject =
    (process.env.RESEND_SECPLUS_SCORECARD_SUBJECT || "").trim() ||
    "Your Security+ SY0-701 simulation scorecard";

  const html = renderScorecardEmailHtml(payload, siteUrl);

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
      html,
    }),
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    console.error("[secplus-scorecard] Resend error:", res.status, text.slice(0, 500));
    throw new Error("Resend rejected email: HTTP " + res.status);
  }
  return true;
}
