/**
 * Visitor questions submitted from site footers → data/leads/visitor-questions.csv
 */
import fs from "fs";
import path from "path";

export const VISITOR_QUESTIONS_CSV_REL = "data/leads/visitor-questions.csv";

const CSV_HEADER = "captured_at_utc,email,product,page_path,message,status";

const VALID_PRODUCTS = new Set(["ccna", "encor", "secplus", "general"]);

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
    row.page_path,
    row.message,
    row.status,
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

function sanitizeRepoPart(value) {
  return String(value || "")
    .trim()
    .replace(/^["']+|["']+$/g, "");
}

export function resolveGithubRepo() {
  const combined = sanitizeRepoPart(process.env.GITHUB_LEADS_REPO || "");
  if (combined.includes("/")) {
    const [owner, name] = combined.split("/", 2).map(sanitizeRepoPart);
    if (owner && name) return { owner, repo: name };
  }
  const owner = sanitizeRepoPart(
    process.env.GITHUB_LEADS_REPO_OWNER || process.env.VERCEL_GIT_REPO_OWNER || ""
  );
  const repo = sanitizeRepoPart(
    process.env.GITHUB_LEADS_REPO_NAME || process.env.VERCEL_GIT_REPO_SLUG || ""
  );
  if (!owner || !repo) return null;
  return { owner, repo };
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
      "User-Agent": "becertifiedtoday-visitor-questions",
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

/** Public repos: read CSV without a token (admin report fallback). */
async function fetchGithubFilePublic({ owner, repo, filePath }) {
  const url = githubContentsUrl(owner, repo, filePath);
  const res = await fetch(url, {
    headers: {
      Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
      "User-Agent": "becertifiedtoday-visitor-questions",
    },
  });
  if (res.status === 404) {
    return { content: CSV_HEADER + "\n", sha: null };
  }
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`github_public_get_${res.status}:${text.slice(0, 200)}`);
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
      name: "Be Certified Today Visitor Questions",
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
      "User-Agent": "becertifiedtoday-visitor-questions",
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
  const repoInfo = resolveGithubRepo();
  if (!token || !repoInfo) return { ok: false, reason: "github_not_configured" };

  const file = await fetchGithubFile({ token, ...repoInfo, filePath: VISITOR_QUESTIONS_CSV_REL });
  let content = file.content || "";
  if (!content.trim()) content = CSV_HEADER + "\n";
  else if (!content.includes("captured_at_utc")) content = CSV_HEADER + "\n" + content.replace(/^\n+/, "");
  if (!content.endsWith("\n")) content += "\n";
  content += formatRow(row) + "\n";

  try {
    await putGithubFile({
      token,
      ...repoInfo,
      filePath: VISITOR_QUESTIONS_CSV_REL,
      content,
      sha: file.sha,
      message: `Visitor question: ${row.product} ${row.email}`,
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
  const filePath = path.join(process.cwd(), VISITOR_QUESTIONS_CSV_REL);
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

export function normalizeQuestionProduct(raw) {
  const p = String(raw || "")
    .trim()
    .toLowerCase();
  return VALID_PRODUCTS.has(p) ? p : "general";
}

export function buildVisitorQuestionRow(body) {
  return {
    captured_at_utc: new Date().toISOString(),
    email: String(body?.email || "")
      .trim()
      .toLowerCase(),
    product: normalizeQuestionProduct(body?.product),
    page_path: String(body?.page_path || body?.pagePath || "")
      .trim()
      .slice(0, 240),
    message: String(body?.message || "")
      .trim()
      .slice(0, 2000),
    status: "new",
  };
}

export async function appendVisitorQuestion(body) {
  const row = buildVisitorQuestionRow(body);
  if (!row.email || !row.message) {
    return { ok: false, reason: "invalid_email_or_message" };
  }

  try {
    const token = (process.env.GITHUB_LEADS_TOKEN || "").trim();
    const repoInfo = resolveGithubRepo();
    if (token && repoInfo) return await appendToGithub(row);
    if (canWriteLocal()) return appendToLocal(row);
    console.warn("[visitor-question] not persisted (GITHUB_LEADS_TOKEN or repo):", row.email);
    return { ok: false, reason: "not_configured" };
  } catch (err) {
    console.error("[visitor-question] append failed:", err?.message || err);
    return { ok: false, reason: "error", detail: String(err?.message || err).slice(0, 200) };
  }
}

export async function readVisitorQuestions() {
  const token = (process.env.GITHUB_LEADS_TOKEN || "").trim();
  const repoInfo = resolveGithubRepo();
  if (repoInfo) {
    if (token) {
      try {
        const file = await fetchGithubFile({
          token,
          ...repoInfo,
          filePath: VISITOR_QUESTIONS_CSV_REL,
        });
        const rows = parseCsvContent(file.content);
        if (rows.length) return rows;
      } catch (err) {
        console.warn("[visitor-question] token read failed, trying public:", err?.message || err);
      }
    }
    const publicFile = await fetchGithubFilePublic({
      ...repoInfo,
      filePath: VISITOR_QUESTIONS_CSV_REL,
    });
    return parseCsvContent(publicFile.content);
  }
  if (canWriteLocal()) {
    const filePath = path.join(process.cwd(), VISITOR_QUESTIONS_CSV_REL);
    if (!fs.existsSync(filePath)) return [];
    return parseCsvContent(fs.readFileSync(filePath, "utf8"));
  }
  const err = new Error("github_not_configured");
  err.code = "github_not_configured";
  throw err;
}

export function aggregateVisitorQuestionsReport(rows) {
  const items = [];
  for (const row of rows || []) {
    const email = String(row.email || "")
      .trim()
      .toLowerCase();
    if (!email) continue;
    items.push({
      capturedAt: row.captured_at_utc || "",
      email,
      product: normalizeQuestionProduct(row.product),
      pagePath: row.page_path || "",
      message: row.message || "",
      status: row.status || "new",
    });
  }
  items.sort((a, b) => (b.capturedAt || "").localeCompare(a.capturedAt || ""));
  const byProduct = { ccna: 0, encor: 0, secplus: 0, general: 0 };
  for (const item of items) {
    byProduct[item.product] = (byProduct[item.product] || 0) + 1;
  }
  return {
    items,
    total: items.length,
    byProduct,
    newCount: items.filter((i) => i.status === "new").length,
  };
}
