/**
 * Owner daily campaign log — supports GA4 analytics context (spend, changes, experiments).
 * Persists to data/analytics/campaign-daily-log.csv (GitHub API or local dev).
 */
import fs from "fs";
import path from "path";
import { resolveGithubRepo } from "./visitor-questions.js";

export const CAMPAIGN_DAILY_LOG_CSV_REL = "data/analytics/campaign-daily-log.csv";

const CSV_HEADER =
  "log_date,updated_at_utc,google_spend_usd,reddit_spend_usd,stripe_purchases,creative_changes,bid_targeting,site_changes,experiments,blockers,next_actions,notes";

const TEXT_FIELD_ALIASES = {
  creative_changes: ["creative_changes", "creativeChanges"],
  bid_targeting: ["bid_targeting", "bidTargeting"],
  site_changes: ["site_changes", "siteChanges"],
  experiments: ["experiments"],
  blockers: ["blockers"],
  next_actions: ["next_actions", "nextActions"],
  notes: ["notes"],
};

function pickBodyField(body, keys) {
  for (const key of keys) {
    if (body[key] != null && String(body[key]).trim() !== "") {
      return body[key];
    }
  }
  for (const key of keys) {
    if (body[key] != null) return body[key];
  }
  return "";
}

function csvCell(value) {
  const s = value == null ? "" : String(value);
  if (/[",\n\r]/.test(s)) {
    return `"${s.replace(/"/g, '""')}"`;
  }
  return s;
}

function formatRow(row) {
  return [
    row.log_date,
    row.updated_at_utc,
    row.google_spend_usd,
    row.reddit_spend_usd,
    row.stripe_purchases,
    row.creative_changes,
    row.bid_targeting,
    row.site_changes,
    row.experiments,
    row.blockers,
    row.next_actions,
    row.notes,
  ]
    .map(csvCell)
    .join(",");
}

function serializeCsv(rows) {
  const lines = [CSV_HEADER];
  for (const row of rows || []) {
    lines.push(formatRow(row));
  }
  return lines.join("\n") + "\n";
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

function decodeGithubContent(data) {
  if (!data || !data.content) return "";
  return Buffer.from(data.content.replace(/\n/g, ""), "base64").toString("utf8");
}

function encodeGithubContent(text) {
  return Buffer.from(text, "utf8").toString("base64");
}

function githubContentsUrl(owner, repo, filePath) {
  return `https://api.github.com/repos/${encodeURIComponent(owner)}/${encodeURIComponent(repo)}/contents/${filePath.split("/").map(encodeURIComponent).join("/")}`;
}

async function fetchGithubFile({ token, owner, repo, filePath }) {
  const res = await fetch(githubContentsUrl(owner, repo, filePath), {
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
      "User-Agent": "becertifiedtoday-campaign-daily-log",
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
  const body = {
    message,
    content: encodeGithubContent(content),
    committer: {
      name: "Be Certified Today Campaign Log",
      email: "leads@becertifiedtoday.com",
    },
  };
  if (sha) body.sha = sha;
  const res = await fetch(githubContentsUrl(owner, repo, filePath), {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: "application/vnd.github+json",
      "Content-Type": "application/json",
      "X-GitHub-Api-Version": "2022-11-28",
      "User-Agent": "becertifiedtoday-campaign-daily-log",
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`github_put_${res.status}:${text.slice(0, 200)}`);
  }
  return true;
}

function canWriteLocal() {
  if ((process.env.LEADS_CSV_DISABLE_LOCAL || "").trim() === "1") return false;
  if ((process.env.GITHUB_LEADS_TOKEN || "").trim()) return false;
  if (process.env.VERCEL === "1") return false;
  return true;
}

function readLocalRows() {
  const filePath = path.join(process.cwd(), CAMPAIGN_DAILY_LOG_CSV_REL);
  if (!fs.existsSync(filePath)) return [];
  return parseCsvContent(fs.readFileSync(filePath, "utf8"));
}

function writeLocalRows(rows) {
  const filePath = path.join(process.cwd(), CAMPAIGN_DAILY_LOG_CSV_REL);
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, serializeCsv(rows), "utf8");
  return { ok: true, backend: "local" };
}

async function readRows() {
  const token = (process.env.GITHUB_LEADS_TOKEN || "").trim();
  const repoInfo = resolveGithubRepo();
  if (token && repoInfo) {
    const file = await fetchGithubFile({ token, ...repoInfo, filePath: CAMPAIGN_DAILY_LOG_CSV_REL });
    return parseCsvContent(file.content);
  }
  if (canWriteLocal()) return readLocalRows();
  return [];
}

async function writeRows(rows, attempt = 0) {
  const token = (process.env.GITHUB_LEADS_TOKEN || "").trim();
  const repoInfo = resolveGithubRepo();
  const content = serializeCsv(rows);

  if (token && repoInfo) {
    const file = await fetchGithubFile({ token, ...repoInfo, filePath: CAMPAIGN_DAILY_LOG_CSV_REL });
    try {
      await putGithubFile({
        token,
        ...repoInfo,
        filePath: CAMPAIGN_DAILY_LOG_CSV_REL,
        content,
        sha: file.sha,
        message: "Admin: campaign daily log",
      });
      return { ok: true, backend: "github" };
    } catch (err) {
      const msg = String(err?.message || err);
      if (attempt < 2 && msg.includes("github_put_409")) {
        return writeRows(rows, attempt + 1);
      }
      throw err;
    }
  }
  if (canWriteLocal()) return writeLocalRows(rows);
  return { ok: false, reason: "not_configured" };
}

export function normalizeLogDate(raw) {
  const s = String(raw || "").trim();
  if (!/^\d{4}-\d{2}-\d{2}$/.test(s)) return "";
  const d = new Date(s + "T12:00:00.000Z");
  if (Number.isNaN(d.getTime())) return "";
  return s;
}

function normalizeMoney(raw) {
  const s = String(raw ?? "").trim();
  if (!s) return "";
  const n = Number(s.replace(/[$,]/g, ""));
  if (!Number.isFinite(n) || n < 0) return "";
  return n.toFixed(2);
}

function normalizeCount(raw) {
  const n = Math.floor(Number(raw));
  if (!Number.isFinite(n) || n < 0) return "";
  return String(n);
}

function normalizeText(raw, max = 1200) {
  return String(raw || "")
    .trim()
    .slice(0, max);
}

/** @param {Record<string, unknown>} body */
export function buildDailyLogRow(body) {
  const logDate = normalizeLogDate(body.log_date || body.logDate);
  if (!logDate) return null;

  /** @type {Record<string, string>} */
  const row = {
    log_date: logDate,
    updated_at_utc: new Date().toISOString(),
    google_spend_usd: normalizeMoney(body.google_spend_usd ?? body.googleSpendUsd),
    reddit_spend_usd: normalizeMoney(body.reddit_spend_usd ?? body.redditSpendUsd),
    stripe_purchases: normalizeCount(body.stripe_purchases ?? body.stripePurchases),
  };

  for (const field of Object.keys(TEXT_FIELD_ALIASES)) {
    row[field] = normalizeText(pickBodyField(body, TEXT_FIELD_ALIASES[field]));
  }
  return row;
}

export function rowToEntry(row) {
  return {
    logDate: row.log_date || "",
    updatedAt: row.updated_at_utc || "",
    googleSpendUsd: row.google_spend_usd || "",
    redditSpendUsd: row.reddit_spend_usd || "",
    stripePurchases: row.stripe_purchases || "",
    creativeChanges: row.creative_changes || "",
    bidTargeting: row.bid_targeting || "",
    siteChanges: row.site_changes || "",
    experiments: row.experiments || "",
    blockers: row.blockers || "",
    nextActions: row.next_actions || "",
    notes: row.notes || "",
  };
}

/** Map admin range preset to inclusive ISO log_date bounds (UTC). */
export function isoRangeFromPreset(preset) {
  const p = String(preset || "7d").trim().toLowerCase();
  const end = new Date();
  end.setUTCHours(0, 0, 0, 0);
  const start = new Date(end);
  if (p === "today") {
    // same day
  } else if (p === "21d") {
    start.setUTCDate(start.getUTCDate() - 21);
  } else if (p === "28d") {
    start.setUTCDate(start.getUTCDate() - 28);
  } else if (p === "90d") {
    start.setUTCDate(start.getUTCDate() - 90);
  } else {
    start.setUTCDate(start.getUTCDate() - 7);
  }
  return {
    startDate: start.toISOString().slice(0, 10),
    endDate: end.toISOString().slice(0, 10),
  };
}

/**
 * @param {{ startDate?: string, endDate?: string, limit?: number }} [opts]
 */
export async function listCampaignDailyLogs(opts = {}) {
  const start = normalizeLogDate(opts.startDate);
  const end = normalizeLogDate(opts.endDate);
  const limit = Math.min(120, Math.max(1, Number(opts.limit) || 60));

  let rows = await readRows();
  rows = rows.filter((r) => normalizeLogDate(r.log_date));

  if (start) rows = rows.filter((r) => r.log_date >= start);
  if (end) rows = rows.filter((r) => r.log_date <= end);

  rows.sort((a, b) => String(b.log_date).localeCompare(String(a.log_date)));
  return rows.slice(0, limit).map(rowToEntry);
}

/** @param {Record<string, unknown>} body */
export async function upsertCampaignDailyLog(body) {
  const row = buildDailyLogRow(body);
  if (!row) return { ok: false, reason: "invalid_log_date" };

  const rows = (await readRows()).filter((r) => normalizeLogDate(r.log_date));
  const idx = rows.findIndex((r) => r.log_date === row.log_date);
  if (idx >= 0) rows[idx] = row;
  else rows.push(row);

  rows.sort((a, b) => String(a.log_date).localeCompare(String(b.log_date)));

  try {
    const result = await writeRows(rows);
    if (!result.ok) return result;
    return { ok: true, entry: rowToEntry(row), backend: result.backend || null };
  } catch (err) {
    console.error("[campaign-daily-log] save failed:", err?.message || err);
    return { ok: false, reason: "error", detail: String(err?.message || err).slice(0, 200) };
  }
}
