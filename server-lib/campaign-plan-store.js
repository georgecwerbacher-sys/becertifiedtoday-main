/**
 * Persist campaign plan state (daily manual metrics + step checkboxes) to JSON.
 * Uses GitHub Contents API on Vercel (same token as visitor questions); local file in dev.
 */
import fs from "fs";
import path from "path";
import { resolveGithubRepo } from "./visitor-questions.js";

export const CAMPAIGN_PLAN_DIR_REL = "data/reports/campaign-plan";

function planStoreRel(campaignId) {
  const id = String(campaignId || "").trim();
  if (!id) throw new Error("missing_campaign_id");
  return `${CAMPAIGN_PLAN_DIR_REL}/${id}.json`;
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
      "User-Agent": "becertifiedtoday-campaign-plan",
    },
  });
  if (res.status === 404) return { content: "", sha: null };
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`github_get_${res.status}:${text.slice(0, 200)}`);
  }
  const data = await res.json();
  return { content: decodeGithubContent(data), sha: data.sha || null };
}

async function fetchGithubRawPublic({ owner, repo, filePath, ref = "main" }) {
  const url = `https://raw.githubusercontent.com/${encodeURIComponent(owner)}/${encodeURIComponent(repo)}/${ref}/${filePath.split("/").map(encodeURIComponent).join("/")}`;
  const res = await fetch(url, { headers: { "User-Agent": "becertifiedtoday-campaign-plan" } });
  if (res.status === 404) return { content: "", sha: null };
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`github_raw_get_${res.status}:${text.slice(0, 200)}`);
  }
  return { content: await res.text(), sha: null };
}

async function putGithubFile({ token, owner, repo, filePath, content, sha, message }) {
  const body = {
    message,
    content: encodeGithubContent(content),
    committer: { name: "Be Certified Today Campaign Plan", email: "leads@becertifiedtoday.com" },
  };
  if (sha) body.sha = sha;
  const res = await fetch(githubContentsUrl(owner, repo, filePath), {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: "application/vnd.github+json",
      "Content-Type": "application/json",
      "X-GitHub-Api-Version": "2022-11-28",
      "User-Agent": "becertifiedtoday-campaign-plan",
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

function defaultState(campaignId, defaultStartDate) {
  return {
    campaignId: String(campaignId || "").trim(),
    startDate: defaultStartDate || null,
    completedStepIds: [],
    daily: {},
    updatedAt: new Date().toISOString(),
  };
}

function normalizeState(raw, campaignId, defaultStartDate) {
  const base = defaultState(campaignId, defaultStartDate);
  if (!raw || typeof raw !== "object") return base;
  return {
    campaignId: String(raw.campaignId || campaignId || "").trim() || base.campaignId,
    startDate:
      typeof raw.startDate === "string" && /^\d{4}-\d{2}-\d{2}$/.test(raw.startDate.trim())
        ? raw.startDate.trim()
        : base.startDate,
    completedStepIds: Array.isArray(raw.completedStepIds)
      ? [...new Set(raw.completedStepIds.map((s) => String(s || "").trim()).filter(Boolean))]
      : [],
    daily: raw.daily && typeof raw.daily === "object" ? { ...raw.daily } : {},
    updatedAt: typeof raw.updatedAt === "string" ? raw.updatedAt : base.updatedAt,
  };
}

function serializeState(state) {
  return JSON.stringify(state, null, 2) + "\n";
}

function parseState(content, campaignId, defaultStartDate) {
  if (!content || !String(content).trim()) {
    return defaultState(campaignId, defaultStartDate);
  }
  try {
    return normalizeState(JSON.parse(content), campaignId, defaultStartDate);
  } catch (_) {
    return defaultState(campaignId, defaultStartDate);
  }
}

function readLocal(filePath, campaignId, defaultStartDate) {
  if (!fs.existsSync(filePath)) return defaultState(campaignId, defaultStartDate);
  return parseState(fs.readFileSync(filePath, "utf8"), campaignId, defaultStartDate);
}

function writeLocal(filePath, state) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, serializeState(state), "utf8");
  return { ok: true, backend: "local" };
}

async function readStateFromGithub(repoInfo, filePath, campaignId, defaultStartDate) {
  const token = (process.env.GITHUB_LEADS_TOKEN || "").trim();
  const readers = [];
  if (token) readers.push(() => fetchGithubFile({ token, ...repoInfo, filePath }));
  readers.push(() => fetchGithubRawPublic({ ...repoInfo, filePath }));

  let lastErr = null;
  for (const read of readers) {
    try {
      const file = await read();
      return { state: parseState(file.content, campaignId, defaultStartDate), sha: file.sha || null };
    } catch (err) {
      lastErr = err;
    }
  }
  if (lastErr) throw lastErr;
  return { state: defaultState(campaignId, defaultStartDate), sha: null };
}

async function writeStateToGithub(repoInfo, filePath, state, attempt = 0) {
  const token = (process.env.GITHUB_LEADS_TOKEN || "").trim();
  if (!token) return { ok: false, reason: "github_not_configured" };

  const file = await fetchGithubFile({ token, ...repoInfo, filePath });
  const content = serializeState(state);
  try {
    await putGithubFile({
      token,
      ...repoInfo,
      filePath,
      content,
      sha: file.sha,
      message: `Admin: update campaign plan ${state.campaignId}`,
    });
    return { ok: true, backend: "github" };
  } catch (err) {
    const msg = String(err?.message || err);
    if (attempt < 2 && msg.includes("github_put_409")) {
      return writeStateToGithub(repoInfo, filePath, state, attempt + 1);
    }
    throw err;
  }
}

async function persistState(state, defaultStartDate) {
  const campaignId = state.campaignId;
  const filePath = planStoreRel(campaignId);
  state.updatedAt = new Date().toISOString();
  const normalized = normalizeState(state, campaignId, defaultStartDate);

  const token = (process.env.GITHUB_LEADS_TOKEN || "").trim();
  const repoInfo = resolveGithubRepo();
  if (token && repoInfo) {
    const result = await writeStateToGithub(repoInfo, filePath, normalized);
    return { ...result, state: normalized };
  }
  if (canWriteLocal()) {
    const abs = path.join(process.cwd(), filePath);
    writeLocal(abs, normalized);
    return { ok: true, backend: "local", state: normalized };
  }
  return { ok: false, reason: "not_configured" };
}

/**
 * @param {string} campaignId
 * @param {string} [defaultStartDate]
 */
export async function readCampaignPlanState(campaignId, defaultStartDate) {
  const id = String(campaignId || "").trim();
  const filePath = planStoreRel(id);
  const token = (process.env.GITHUB_LEADS_TOKEN || "").trim();
  const repoInfo = resolveGithubRepo();

  if (canWriteLocal() && !token) {
    const state = readLocal(path.join(process.cwd(), filePath), id, defaultStartDate);
    if (!state.startDate && defaultStartDate) state.startDate = defaultStartDate;
    return state;
  }

  if (repoInfo) {
    try {
      const { state } = await readStateFromGithub(repoInfo, filePath, id, defaultStartDate);
      if (!state.startDate && defaultStartDate) state.startDate = defaultStartDate;
      return state;
    } catch (err) {
      console.error("[campaign-plan] github read failed:", err?.message || err);
      throw err;
    }
  }

  if (canWriteLocal()) {
    const state = readLocal(path.join(process.cwd(), filePath), id, defaultStartDate);
    if (!state.startDate && defaultStartDate) state.startDate = defaultStartDate;
    return state;
  }

  const err = new Error("github_not_configured");
  err.code = "github_not_configured";
  throw err;
}

function normalizeDailyPatch(patch) {
  /** @type {Record<string, unknown>} */
  const out = {};
  const numFields = [
    "adsSpendUsd",
    "adsImpressions",
    "adsClicks",
    "adsAvgCpc",
    "adsCtr",
    "adsConversions",
  ];
  for (const key of numFields) {
    if (patch[key] === undefined || patch[key] === null || patch[key] === "") continue;
    const n = Number(patch[key]);
    if (!Number.isFinite(n) || n < 0) continue;
    out[key] = n;
  }
  if (typeof patch.notes === "string") out.notes = patch.notes.trim().slice(0, 2000);
  if (patch.adsPaused === true || patch.adsPaused === "true" || patch.adsPaused === 1) {
    out.adsPaused = true;
  } else if (patch.adsPaused === false || patch.adsPaused === "false" || patch.adsPaused === 0) {
    out.adsPaused = false;
  }
  if (patch.keywordCsvUpdated === true || patch.keywordCsvUpdated === "true") {
    out.keywordCsvUpdated = true;
  } else if (patch.keywordCsvUpdated === false || patch.keywordCsvUpdated === "false") {
    out.keywordCsvUpdated = false;
  }
  if (patch.negativesAdded === true || patch.negativesAdded === "true") {
    out.negativesAdded = true;
  } else if (patch.negativesAdded === false || patch.negativesAdded === "false") {
    out.negativesAdded = false;
  }
  if (patch.landingChange === true || patch.landingChange === "true") {
    out.landingChange = true;
  } else if (patch.landingChange === false || patch.landingChange === "false") {
    out.landingChange = false;
  }
  if (Array.isArray(patch.completedDailyTaskIds)) {
    out.completedDailyTaskIds = [
      ...new Set(patch.completedDailyTaskIds.map((s) => String(s || "").trim()).filter(Boolean)),
    ];
  }
  out.savedAt = new Date().toISOString();
  return out;
}

export async function saveCampaignPlanDailyEntry(campaignId, date, patch, defaultStartDate) {
  const id = String(campaignId || "").trim();
  const day = String(date || "").trim();
  if (!/^\d{4}-\d{2}-\d{2}$/.test(day)) return { ok: false, reason: "invalid_date" };

  const state = await readCampaignPlanState(id, defaultStartDate);
  const prev = state.daily[day] && typeof state.daily[day] === "object" ? state.daily[day] : {};
  state.daily[day] = { ...prev, ...normalizeDailyPatch(patch || {}) };

  try {
    const result = await persistState(state, defaultStartDate);
    if (!result.ok) return result;
    return { ok: true, date: day, daily: state.daily[day], backend: result.backend || null };
  } catch (err) {
    return { ok: false, reason: "error", detail: String(err?.message || err).slice(0, 200) };
  }
}

export async function setCampaignPlanStepCompleted(campaignId, stepId, completed, defaultStartDate) {
  const id = String(campaignId || "").trim();
  const sid = String(stepId || "").trim();
  if (!sid) return { ok: false, reason: "missing_step_id" };

  const state = await readCampaignPlanState(id, defaultStartDate);
  const set = new Set(state.completedStepIds || []);
  if (completed) set.add(sid);
  else set.delete(sid);
  state.completedStepIds = [...set];

  try {
    const result = await persistState(state, defaultStartDate);
    if (!result.ok) return result;
    return {
      ok: true,
      stepId: sid,
      completed: Boolean(completed),
      completedStepIds: state.completedStepIds,
      backend: result.backend || null,
    };
  } catch (err) {
    return { ok: false, reason: "error", detail: String(err?.message || err).slice(0, 200) };
  }
}

export async function setCampaignPlanStartDate(campaignId, startDate, defaultStartDate) {
  const id = String(campaignId || "").trim();
  const day = String(startDate || "").trim();
  if (!/^\d{4}-\d{2}-\d{2}$/.test(day)) return { ok: false, reason: "invalid_start_date" };

  const state = await readCampaignPlanState(id, defaultStartDate);
  state.startDate = day;

  try {
    const result = await persistState(state, defaultStartDate);
    if (!result.ok) return result;
    return { ok: true, startDate: day, backend: result.backend || null };
  } catch (err) {
    return { ok: false, reason: "error", detail: String(err?.message || err).slice(0, 200) };
  }
}
