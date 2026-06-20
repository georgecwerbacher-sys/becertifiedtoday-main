/**
 * Portal magic-link restore requests → data/leads/portal-magic-link-requests.csv
 */
import fs from "fs";
import path from "path";
import {
  readGithubLeadsCsv,
  resolveGithubRepo,
} from "./visitor-questions.js";

export const PORTAL_MAGIC_LINK_REQUESTS_CSV_REL =
  "data/leads/portal-magic-link-requests.csv";

const CSV_HEADER =
  "captured_at_utc,email,track,found,sent,reason,checkout_session_id";

const VALID_TRACKS = new Set(["ccna", "encor", "secplus"]);

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
    row.email,
    row.track,
    row.found,
    row.sent,
    row.reason,
    row.checkout_session_id,
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
  const url = githubContentsUrl(owner, repo, filePath);
  const res = await fetch(url, {
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
      "User-Agent": "becertifiedtoday-portal-magic-link",
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
  const url = githubContentsUrl(owner, repo, filePath);
  const body = {
    message,
    content: encodeGithubContent(content),
    committer: {
      name: "Be Certified Today Portal Magic Link",
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
      "User-Agent": "becertifiedtoday-portal-magic-link",
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

function appendToLocal(row) {
  const filePath = path.join(process.cwd(), PORTAL_MAGIC_LINK_REQUESTS_CSV_REL);
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  if (!fs.existsSync(filePath) || fs.statSync(filePath).size === 0) {
    fs.writeFileSync(filePath, CSV_HEADER + "\n", "utf8");
  }
  fs.appendFileSync(filePath, formatRow(row) + "\n", "utf8");
  return { ok: true, backend: "local" };
}

async function appendToGithub(row, attempt = 0) {
  const token = (process.env.GITHUB_LEADS_TOKEN || "").trim();
  const repoInfo = resolveGithubRepo();
  if (!token || !repoInfo) return { ok: false, reason: "github_not_configured" };

  const file = await fetchGithubFile({
    token,
    ...repoInfo,
    filePath: PORTAL_MAGIC_LINK_REQUESTS_CSV_REL,
  });
  let content = file.content || "";
  if (!content.trim()) content = CSV_HEADER + "\n";
  else if (!content.includes("captured_at_utc")) {
    content = CSV_HEADER + "\n" + content.replace(/^\n+/, "");
  }
  if (!content.endsWith("\n")) content += "\n";
  content += formatRow(row) + "\n";

  try {
    await putGithubFile({
      token,
      ...repoInfo,
      filePath: PORTAL_MAGIC_LINK_REQUESTS_CSV_REL,
      content,
      sha: file.sha,
      message: `Portal magic link: ${row.track} ${row.email}`,
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

export function normalizeMagicLinkTrack(raw) {
  const t = String(raw || "")
    .trim()
    .toLowerCase();
  return VALID_TRACKS.has(t) ? t : "ccna";
}

export function buildMagicLinkRequestRow(body) {
  return {
    captured_at_utc: new Date().toISOString(),
    email: String(body?.email || "")
      .trim()
      .toLowerCase(),
    track: normalizeMagicLinkTrack(body?.track),
    found: body?.found ? "yes" : "no",
    sent: body?.sent ? "yes" : "no",
    reason: String(body?.reason || "")
      .trim()
      .slice(0, 120),
    checkout_session_id: String(body?.checkoutSessionId || body?.checkout_session_id || "")
      .trim()
      .slice(0, 80),
  };
}

export async function appendPortalMagicLinkRequest(body) {
  const row = buildMagicLinkRequestRow(body);
  if (!row.email) return { ok: false, reason: "invalid_email" };

  try {
    const token = (process.env.GITHUB_LEADS_TOKEN || "").trim();
    const repoInfo = resolveGithubRepo();
    if (token && repoInfo) return await appendToGithub(row);
    if (canWriteLocal()) return appendToLocal(row);
    console.warn("[portal-magic-link] not persisted (GITHUB_LEADS_TOKEN or repo):", row.email);
    return { ok: false, reason: "not_configured" };
  } catch (err) {
    console.error("[portal-magic-link] append failed:", err?.message || err);
    return { ok: false, reason: "error", detail: String(err?.message || err).slice(0, 200) };
  }
}

export async function readPortalMagicLinkRequests() {
  const repoInfo = resolveGithubRepo();
  if (repoInfo) {
    try {
      return await readGithubLeadsCsv(PORTAL_MAGIC_LINK_REQUESTS_CSV_REL);
    } catch (err) {
      if (err && err.code === "github_not_configured") throw err;
      console.error("[portal-magic-link] github read failed:", err?.message || err);
      throw err;
    }
  }
  if (canWriteLocal()) {
    const filePath = path.join(process.cwd(), PORTAL_MAGIC_LINK_REQUESTS_CSV_REL);
    if (!fs.existsSync(filePath)) return [];
    return parseCsvContent(fs.readFileSync(filePath, "utf8"));
  }
  const err = new Error("github_not_configured");
  err.code = "github_not_configured";
  throw err;
}

export function aggregateMagicLinkRequestsReport(rows) {
  const items = [];
  for (const row of rows || []) {
    const email = String(row.email || "")
      .trim()
      .toLowerCase();
    if (!email) continue;
    items.push({
      capturedAt: row.captured_at_utc || "",
      email,
      track: normalizeMagicLinkTrack(row.track),
      found: String(row.found || "").toLowerCase() === "yes",
      sent: String(row.sent || "").toLowerCase() === "yes",
      reason: row.reason || "",
      checkoutSessionId: row.checkout_session_id || "",
    });
  }
  items.sort((a, b) => (b.capturedAt || "").localeCompare(a.capturedAt || ""));
  const byTrack = { ccna: 0, encor: 0, secplus: 0 };
  let sentCount = 0;
  let foundCount = 0;
  for (const item of items) {
    byTrack[item.track] = (byTrack[item.track] || 0) + 1;
    if (item.sent) sentCount += 1;
    if (item.found) foundCount += 1;
  }
  return {
    items,
    total: items.length,
    byTrack,
    sentCount,
    foundCount,
  };
}

/** @param {object[]} rows in date range */
export function magicLinkCountsByEmail(rows) {
  /** @type {Map<string, { count: number, lastAt: string, sentCount: number }>} */
  const map = new Map();
  for (const row of rows || []) {
    const email = String(row.email || "")
      .trim()
      .toLowerCase();
    if (!email) continue;
    const at = row.captured_at_utc || "";
    const prev = map.get(email) || { count: 0, lastAt: "", sentCount: 0 };
    prev.count += 1;
    if (String(row.sent || "").toLowerCase() === "yes") prev.sentCount += 1;
    if (!prev.lastAt || at > prev.lastAt) prev.lastAt = at;
    map.set(email, prev);
  }
  return map;
}

export function enrichPortalBlockWithMagicLinkCounts(block, countsByEmail) {
  if (!block || !countsByEmail) return block;
  for (const list of [block.active, block.expired]) {
    for (const row of list || []) {
      const email = String(row.email || "")
        .trim()
        .toLowerCase();
      if (!email || email === "(no email on file)") {
        row.magicLinkResetsInRange = 0;
        row.lastMagicLinkResetAt = null;
        continue;
      }
      const stats = countsByEmail.get(email);
      row.magicLinkResetsInRange = stats?.count || 0;
      row.lastMagicLinkResetAt = stats?.lastAt || null;
    }
  }
  return block;
}
