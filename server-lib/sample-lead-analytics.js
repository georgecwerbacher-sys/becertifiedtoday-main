/**
 * Homepage sample → email capture funnel (CCNA, ENCOR, Security+).
 * Persists to data/leads/home-sample-email-capture.csv (GitHub API or local).
 */
import fs from "fs";
import path from "path";
import { isInternalAnalyticsEmail } from "./analytics-internal.js";
import { readGithubLeadsCsv, resolveGithubRepo } from "./visitor-questions.js";

export const SAMPLE_LEAD_CSV_REL = "data/leads/home-sample-email-capture.csv";

const CSV_HEADER =
  "captured_at_utc,event,email,product,sample_kind,source,success,utm_source,utm_medium,utm_campaign,utm_content";

const VALID_PRODUCTS = new Set(["ccna", "encor", "secplus"]);
const VALID_EVENTS = new Set([
  "sample_finished",
  "email_modal_open",
  "email_submit_attempt",
  "email_capture_success",
  "email_capture_fail",
]);

function csvCell(value) {
  const s = value == null ? "" : String(value);
  if (/[",\n\r]/.test(s)) {
    return `"${s.replace(/"/g, '""')}"`;
  }
  return s;
}

function formatRow(row) {
  return [
    row.captured_at_utc,
    row.event,
    row.email,
    row.product,
    row.sample_kind,
    row.source,
    row.success,
    row.utm_source,
    row.utm_medium,
    row.utm_campaign,
    row.utm_content,
  ]
    .map(csvCell)
    .join(",");
}

function parseCsvLine(line) {
  const out = [];
  let cur = "";
  let inQuotes = false;
  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (inQuotes) {
      if (ch === '"' && line[i + 1] === '"') {
        cur += '"';
        i++;
      } else if (ch === '"') {
        inQuotes = false;
      } else {
        cur += ch;
      }
    } else if (ch === '"') {
      inQuotes = true;
    } else if (ch === ",") {
      out.push(cur);
      cur = "";
    } else {
      cur += ch;
    }
  }
  out.push(cur);
  return out;
}

function parseCsvContent(content) {
  const lines = (content || "").trim().split(/\n/).filter((l) => l.trim());
  if (lines.length < 2) return [];
  const headers = parseCsvLine(lines[0]);
  const rows = [];
  for (let i = 1; i < lines.length; i++) {
    const cells = parseCsvLine(lines[i]);
    if (cells.length < headers.length) continue;
    /** @type {Record<string, string>} */
    const row = {};
    for (let j = 0; j < headers.length; j++) {
      row[headers[j]] = cells[j] || "";
    }
    rows.push(row);
  }
  return rows;
}

function resolveGithubRepoForAppend() {
  return resolveGithubRepo();
}

function decodeGithubContent(data) {
  if (!data || !data.content) return "";
  return Buffer.from(data.content.replace(/\n/g, ""), "base64").toString("utf8");
}

function encodeGithubContent(text) {
  return Buffer.from(text, "utf8").toString("base64");
}

async function fetchGithubFile({ token, owner, repo, filePath }) {
  const url = `https://api.github.com/repos/${encodeURIComponent(owner)}/${encodeURIComponent(repo)}/contents/${filePath.split("/").map(encodeURIComponent).join("/")}`;
  const res = await fetch(url, {
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
      "User-Agent": "becertifiedtoday-sample-leads",
    },
  });
  if (res.status === 404) {
    return { content: CSV_HEADER + "\n", sha: null };
  }
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`github_get_${res.status}:${text.slice(0, 200)}`);
  }
  const data = await res.json();
  return { content: decodeGithubContent(data), sha: data.sha || null };
}

async function putGithubFile({ token, owner, repo, filePath, content, sha, message }) {
  const url = `https://api.github.com/repos/${encodeURIComponent(owner)}/${encodeURIComponent(repo)}/contents/${filePath.split("/").map(encodeURIComponent).join("/")}`;
  const body = {
    message,
    content: encodeGithubContent(content),
    committer: {
      name: "Be Certified Today Sample Analytics",
      email: "leads@becertifiedtoday.com",
    },
  };
  if (sha) body.sha = sha;
  const res = await fetch(url, {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: "application/vnd.github+json",
      "Content-Type": "application/json",
      "X-GitHub-Api-Version": "2022-11-28",
      "User-Agent": "becertifiedtoday-sample-leads",
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`github_put_${res.status}:${text.slice(0, 200)}`);
  }
  return true;
}

async function appendToGithub(row, attempt = 0) {
  const token = (process.env.GITHUB_LEADS_TOKEN || "").trim();
  const repoInfo = resolveGithubRepoForAppend();
  if (!token || !repoInfo) return { ok: false, reason: "github_not_configured" };

  const file = await fetchGithubFile({ token, ...repoInfo, filePath: SAMPLE_LEAD_CSV_REL });
  let content = file.content || "";
  if (!content.trim()) content = CSV_HEADER + "\n";
  else if (!content.includes("captured_at_utc")) content = CSV_HEADER + "\n" + content.replace(/^\n+/, "");
  if (!content.endsWith("\n")) content += "\n";
  content += formatRow(row) + "\n";

  try {
    await putGithubFile({
      token,
      ...repoInfo,
      filePath: SAMPLE_LEAD_CSV_REL,
      content,
      sha: file.sha,
      message: `Sample lead: ${row.event} ${row.product} ${row.email || "(no email)"}`,
    });
    return { ok: true, backend: "github" };
  } catch (err) {
    const msg = String(err?.message || err);
    if (attempt < 2 && msg.includes("github_put_409")) {
      return appendToGithub(row, attempt + 1);
    }
    throw err;
  }
}

function appendToLocal(row) {
  const filePath = path.join(process.cwd(), SAMPLE_LEAD_CSV_REL);
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  if (!fs.existsSync(filePath) || fs.statSync(filePath).size === 0) {
    fs.writeFileSync(filePath, CSV_HEADER + "\n", "utf8");
  }
  fs.appendFileSync(filePath, formatRow(row) + "\n", "utf8");
  return { ok: true, backend: "local" };
}

function canWriteLocal() {
  if ((process.env.LEADS_CSV_DISABLE_LOCAL || "").trim() === "1") return false;
  if ((process.env.GITHUB_LEADS_TOKEN || "").trim()) return false;
  if (process.env.VERCEL === "1") return false;
  return true;
}

export function normalizeSampleProduct(raw) {
  const p = String(raw || "")
    .trim()
    .toLowerCase();
  return VALID_PRODUCTS.has(p) ? p : "";
}

export function normalizeSampleEvent(raw) {
  const e = String(raw || "").trim();
  return VALID_EVENTS.has(e) ? e : "";
}

export function buildSampleLeadRow(body) {
  const utm = body && typeof body.utm === "object" && body.utm ? body.utm : {};
  return {
    captured_at_utc: new Date().toISOString(),
    event: normalizeSampleEvent(body?.event) || "",
    email: String(body?.email || "")
      .trim()
      .toLowerCase(),
    product: normalizeSampleProduct(body?.product),
    sample_kind: String(body?.sample_kind || body?.sampleKind || "").trim().slice(0, 64),
    source: String(body?.source || "").trim().slice(0, 120),
    success: body?.success === true || body?.success === "1" ? "1" : body?.success === false ? "0" : "",
    utm_source: utm.utm_source || body?.utm_source || "",
    utm_medium: utm.utm_medium || body?.utm_medium || "",
    utm_campaign: utm.utm_campaign || body?.utm_campaign || "",
    utm_content: utm.utm_content || body?.utm_content || "",
  };
}

export async function appendSampleLeadEvent(body) {
  const row = buildSampleLeadRow(body);
  if (!row.event || !row.product) {
    return { ok: false, reason: "invalid_event_or_product" };
  }
  if (row.email && isInternalAnalyticsEmail(row.email)) {
    return { ok: true, skipped: "internal_email" };
  }

  try {
    const token = (process.env.GITHUB_LEADS_TOKEN || "").trim();
    const repoInfo = resolveGithubRepoForAppend();
    if (token && repoInfo) return await appendToGithub(row);
    if (canWriteLocal()) return appendToLocal(row);
    console.warn("[sample-lead] not persisted (GITHUB_LEADS_TOKEN or repo):", row.event, row.product);
    return { ok: false, reason: "not_configured" };
  } catch (err) {
    console.error("[sample-lead] append failed:", err?.message || err);
    return { ok: false, reason: "error" };
  }
}

export async function readSampleLeadEvents() {
  try {
    return await readGithubLeadsCsv(SAMPLE_LEAD_CSV_REL);
  } catch (err) {
    if (err && err.code === "github_not_configured") throw err;
    console.error("[sample-lead] read failed:", err?.message || err);
    throw err;
  }
}

function isSampleCompletionEvent(event) {
  return event === "sample_finished" || event === "email_modal_open";
}

export function normalizeSampleKind(raw) {
  const k = String(raw || "")
    .trim()
    .toLowerCase();
  if (!k) return "unknown";
  if (k === "dnd" || k === "drag") return "dnd";
  if (k === "lab" || k === "labs" || k === "vlan" || k === "trunk") return "lab";
  if (k === "simulation" || k === "sim" || k.startsWith("sim-")) return "simulation";
  if (k === "questions" || k === "mcq") return "questions";
  return k;
}

function emptyKindCounts() {
  return { questions: 0, dnd: 0, lab: 0, simulation: 0, other: 0 };
}

function isSubmitEvent(event) {
  return (
    event === "email_submit_attempt" ||
    event === "email_capture_success" ||
    event === "email_capture_fail"
  );
}

function isSuccessEvent(event) {
  return event === "email_capture_success";
}

/**
 * @param {Record<string, string>[]} rows
 */
export function aggregateSampleLeadReport(rows) {
  const products = ["ccna", "encor", "secplus"];
  const summary = Object.fromEntries(
    products.map((p) => [
      p,
      {
        sampleCompletions: 0,
        emailModalOpens: 0,
        submitAttempts: 0,
        captureSuccesses: 0,
        uniqueEmails: 0,
      },
    ])
  );
  const byKind = Object.fromEntries(products.map((p) => [p, emptyKindCounts()]));

  /** @type {Map<string, { email: string, product: string, submitAttempts: number, successes: number, lastAt: string, sampleKind: string }>} */
  const byEmailProduct = new Map();

  for (const row of rows || []) {
    const product = normalizeSampleProduct(row.product);
    if (!product) continue;
    const event = normalizeSampleEvent(row.event);
    if (!event) continue;
    const email = String(row.email || "")
      .trim()
      .toLowerCase();
    if (email && isInternalAnalyticsEmail(email)) continue;

    const s = summary[product];
    const kind = normalizeSampleKind(row.sample_kind);
    if (isSampleCompletionEvent(event)) {
      s.sampleCompletions++;
      const bucket = byKind[product];
      if (kind === "questions") bucket.questions++;
      else if (kind === "dnd") bucket.dnd++;
      else if (kind === "lab") bucket.lab++;
      else if (kind === "simulation") bucket.simulation++;
      else bucket.other++;
    }
    if (event === "email_modal_open") s.emailModalOpens++;
    if (isSubmitEvent(event)) s.submitAttempts++;
    if (isSuccessEvent(event)) s.captureSuccesses++;

    if (!email) continue;
    const key = email + "|" + product;
    let rec = byEmailProduct.get(key);
    if (!rec) {
      rec = {
        email,
        product,
        submitAttempts: 0,
        successes: 0,
        lastAt: row.captured_at_utc || "",
        sampleKind: row.sample_kind || "",
      };
      byEmailProduct.set(key, rec);
    }
    if (row.sample_kind) rec.sampleKind = row.sample_kind;
    if (isSubmitEvent(event)) rec.submitAttempts++;
    if (isSuccessEvent(event)) rec.successes++;
    if (row.captured_at_utc && row.captured_at_utc > rec.lastAt) {
      rec.lastAt = row.captured_at_utc;
    }
  }

  const people = Array.from(byEmailProduct.values()).sort((a, b) => {
    if (b.submitAttempts !== a.submitAttempts) return b.submitAttempts - a.submitAttempts;
    return b.lastAt.localeCompare(a.lastAt);
  });

  for (const p of products) {
    summary[p].uniqueEmails = people.filter((r) => r.product === p).length;
  }

  const totals = {
    sampleCompletions: products.reduce((n, p) => n + summary[p].sampleCompletions, 0),
    captureSuccesses: products.reduce((n, p) => n + summary[p].captureSuccesses, 0),
  };

  return {
    summary,
    byKind,
    totals,
    people,
    rowCount: (rows || []).length,
  };
}

export function isSampleLeadSource(source) {
  const s = String(source || "").toLowerCase();
  return s.includes("sample") || s.includes("homesample");
}
