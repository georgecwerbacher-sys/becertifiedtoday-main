/**
 * In-page practice feedback → data/leads/page-feedback.csv
 */
import fs from "fs";
import path from "path";
import {
  DEFAULT_LEADS_REPO,
  isAdminCompleted,
  readGithubLeadsCsv,
  resolveGithubRepo,
} from "./visitor-questions.js";

export const PAGE_FEEDBACK_CSV_REL = "data/leads/page-feedback.csv";

const CSV_HEADER =
  "captured_at_utc,email,product,content_type,page_path,page_title,comment,admin_completed";

const VALID_PRODUCTS = new Set(["ccna", "encor", "secplus", "ccnaauto", "general"]);
const VALID_CONTENT_TYPES = new Set(["question", "drag_drop", "lab", "scenario", "pbq", "other"]);

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
    row.product,
    row.content_type,
    row.page_path,
    row.page_title,
    row.comment,
    isAdminCompleted(row.admin_completed) ? "yes" : "no",
  ]
    .map(csvCell)
    .join(",");
}

function serializePageFeedbackCsv(rows) {
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
  const url = githubContentsUrl(owner, repo, filePath);
  const res = await fetch(url, {
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
      "User-Agent": "becertifiedtoday-page-feedback",
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
      name: "Be Certified Today Page Feedback",
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
      "User-Agent": "becertifiedtoday-page-feedback",
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

export function normalizeFeedbackProduct(raw) {
  const p = String(raw || "")
    .trim()
    .toLowerCase();
  return VALID_PRODUCTS.has(p) ? p : "general";
}

export function normalizeContentType(raw) {
  const t = String(raw || "")
    .trim()
    .toLowerCase();
  return VALID_CONTENT_TYPES.has(t) ? t : "other";
}

export function pageFeedbackId(row) {
  const cap = String(row.captured_at_utc || row.capturedAt || "").trim();
  const path = String(row.page_path || row.pagePath || "").trim();
  const comment = String(row.comment || "").trim().slice(0, 80);
  return `${cap}|${path}|${comment}`;
}

export function buildPageFeedbackRow(body) {
  const commentRaw = String(body?.comment || "")
    .trim()
    .slice(0, 2000);
  const comment = commentRaw || "[Page flagged — no comment]";
  const email = String(body?.email || "")
    .trim()
    .toLowerCase();
  return {
    captured_at_utc: new Date().toISOString(),
    email,
    product: normalizeFeedbackProduct(body?.product),
    content_type: normalizeContentType(body?.content_type || body?.contentType),
    page_path: String(body?.page_path || body?.pagePath || "")
      .trim()
      .slice(0, 240),
    page_title: String(body?.page_title || body?.pageTitle || documentTitleFromBody(body))
      .trim()
      .slice(0, 200),
    comment,
    admin_completed: "no",
  };
}

function documentTitleFromBody(body) {
  return String(body?.page_title || body?.pageTitle || "").trim();
}

async function appendToGithub(row, attempt = 0) {
  const token = (process.env.GITHUB_LEADS_TOKEN || "").trim();
  const repoInfo = resolveGithubRepo();
  if (!token || !repoInfo) return { ok: false, reason: "github_not_configured" };

  const file = await fetchGithubFile({ token, ...repoInfo, filePath: PAGE_FEEDBACK_CSV_REL });
  let content = file.content || "";
  if (!content.trim()) content = CSV_HEADER + "\n";
  else if (!content.includes("captured_at_utc")) content = CSV_HEADER + "\n" + content.replace(/^\n+/, "");
  if (!content.endsWith("\n")) content += "\n";
  content += formatRow(row) + "\n";

  try {
    await putGithubFile({
      token,
      ...repoInfo,
      filePath: PAGE_FEEDBACK_CSV_REL,
      content,
      sha: file.sha,
      message: `Page feedback: ${row.product} ${row.page_path}`,
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
  const filePath = path.join(process.cwd(), PAGE_FEEDBACK_CSV_REL);
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  if (!fs.existsSync(filePath) || fs.statSync(filePath).size === 0) {
    fs.writeFileSync(filePath, CSV_HEADER + "\n", "utf8");
  }
  fs.appendFileSync(filePath, formatRow(row) + "\n", "utf8");
  return { ok: true, backend: "local" };
}

async function writePageFeedbackToGithub(rows, attempt = 0) {
  const token = (process.env.GITHUB_LEADS_TOKEN || "").trim();
  const repoInfo = resolveGithubRepo();
  if (!token || !repoInfo) return { ok: false, reason: "github_not_configured" };

  const file = await fetchGithubFile({ token, ...repoInfo, filePath: PAGE_FEEDBACK_CSV_REL });
  const content = serializePageFeedbackCsv(rows);

  try {
    await putGithubFile({
      token,
      ...repoInfo,
      filePath: PAGE_FEEDBACK_CSV_REL,
      content,
      sha: file.sha,
      message: "Admin: update page feedback status",
    });
    return { ok: true, backend: "github" };
  } catch (err) {
    const msg = String(err?.message || err);
    if (attempt < 2 && msg.includes("github_put_409")) {
      return writePageFeedbackToGithub(rows, attempt + 1);
    }
    throw err;
  }
}

function writePageFeedbackToLocal(rows) {
  const filePath = path.join(process.cwd(), PAGE_FEEDBACK_CSV_REL);
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, serializePageFeedbackCsv(rows), "utf8");
  return { ok: true, backend: "local" };
}

async function writePageFeedback(rows) {
  const token = (process.env.GITHUB_LEADS_TOKEN || "").trim();
  const repoInfo = resolveGithubRepo();
  if (token && repoInfo) return writePageFeedbackToGithub(rows);
  if (canWriteLocal()) return writePageFeedbackToLocal(rows);
  return { ok: false, reason: "not_configured" };
}

export async function appendPageFeedback(body) {
  if (body?.company_website) {
    return { ok: true, skipped: "honeypot" };
  }

  const row = buildPageFeedbackRow(body);
  if (!row.page_path) {
    return { ok: false, reason: "missing_page_path" };
  }

  try {
    const token = (process.env.GITHUB_LEADS_TOKEN || "").trim();
    const repoInfo = resolveGithubRepo();
    if (token && repoInfo) return await appendToGithub(row);
    if (canWriteLocal()) return appendToLocal(row);
    console.warn("[page-feedback] not persisted (GITHUB_LEADS_TOKEN or repo):", row.page_path);
    return { ok: false, reason: "not_configured" };
  } catch (err) {
    console.error("[page-feedback] append failed:", err?.message || err);
    return { ok: false, reason: "error", detail: String(err?.message || err).slice(0, 200) };
  }
}

export async function readPageFeedback() {
  const repoInfo = resolveGithubRepo();
  if (repoInfo) {
    try {
      return await readGithubLeadsCsv(PAGE_FEEDBACK_CSV_REL);
    } catch (err) {
      console.error("[page-feedback] github reads failed:", err?.message || err);
      throw err;
    }
  }
  if (canWriteLocal()) {
    const filePath = path.join(process.cwd(), PAGE_FEEDBACK_CSV_REL);
    if (!fs.existsSync(filePath)) return [];
    return parseCsvContent(fs.readFileSync(filePath, "utf8"));
  }
  const err = new Error("github_not_configured");
  err.code = "github_not_configured";
  throw err;
}

export async function updatePageFeedbackCompleted(feedbackId, completed) {
  const id = String(feedbackId || "").trim();
  if (!id) return { ok: false, reason: "missing_id" };

  const rows = await readPageFeedback();
  let found = false;
  const updated = rows.map((row) => {
    if (pageFeedbackId(row) !== id) return row;
    found = true;
    return {
      ...row,
      admin_completed: completed ? "yes" : "no",
    };
  });
  if (!found) return { ok: false, reason: "not_found" };

  try {
    const result = await writePageFeedback(updated);
    if (!result.ok) return result;
    return { ok: true, feedbackId: id, completed: Boolean(completed), backend: result.backend || null };
  } catch (err) {
    console.error("[page-feedback] update failed:", err?.message || err);
    return { ok: false, reason: "error", detail: String(err?.message || err).slice(0, 200) };
  }
}

export function aggregatePageFeedbackReport(rows) {
  const items = [];
  for (const row of rows || []) {
    const pagePath = String(row.page_path || "").trim();
    if (!pagePath) continue;
    items.push({
      id: pageFeedbackId(row),
      capturedAt: row.captured_at_utc || "",
      email: String(row.email || "")
        .trim()
        .toLowerCase(),
      product: normalizeFeedbackProduct(row.product),
      contentType: normalizeContentType(row.content_type),
      pagePath,
      pageTitle: row.page_title || "",
      comment: row.comment || "",
      adminCompleted: isAdminCompleted(row.admin_completed),
    });
  }
  items.sort((a, b) => (b.capturedAt || "").localeCompare(a.capturedAt || ""));
  const byProduct = { ccna: 0, encor: 0, secplus: 0, ccnaauto: 0, general: 0 };
  const byContentType = { question: 0, drag_drop: 0, lab: 0, scenario: 0, pbq: 0, other: 0 };
  for (const item of items) {
    byProduct[item.product] = (byProduct[item.product] || 0) + 1;
    byContentType[item.contentType] = (byContentType[item.contentType] || 0) + 1;
  }
  const completedCount = items.filter((i) => i.adminCompleted).length;
  return {
    items,
    total: items.length,
    byProduct,
    byContentType,
    completedCount,
    openCount: items.length - completedCount,
  };
}

export { DEFAULT_LEADS_REPO };
