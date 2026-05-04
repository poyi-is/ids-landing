#!/usr/bin/env node
/**
 * Resolve ids-canonical.json + default.css from IDS (poyi-is/ids).
 *
 * Priority:
 *  1. Local checkout: IDS_REPO_PATH or ../ids
 *  2. Remote GitHub with GITHUB_TOKEN (Bearer raw URL, then Contents API)
 *  3. Public raw.githubusercontent.com (no token)
 *  4. Landing repo fallbacks (root ids-canonical.json, kept data/ files)
 *
 * Tokens are read only from process.env — never committed.
 */
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const DATA = path.join(ROOT, "data");
const STYLES = path.join(ROOT, "styles");
const OUT_CANONICAL = path.join(DATA, "ids-canonical.json");
const OUT_CSS = path.join(STYLES, "default.css");
const DOC_LINKS = path.join(DATA, "doc-links.json");

const GH_OWNER = "poyi-is";
const GH_REPO = "ids";
const GH_REF = (process.env.IDS_GIT_REF || "main").trim();

const RAW_BASE = `https://raw.githubusercontent.com/${GH_OWNER}/${GH_REPO}/${GH_REF}`;

const CANONICAL_CANDIDATES = ["ids-canonical.json", "exports/ids-canonical.json"];

const CSS_CANDIDATES = [
  // IDS: npx tsx scripts/generate-gh-pages-css.ts → gh-pages/styles/default.css
  "gh-pages/styles/default.css",
  "default.css",
  "styles/default.css",
  "exports/default.css",
  "exports/styles/default.css",
  "dist/default.css",
  "packages/ui/dist/default.css",
  "packages/ui/dist/styles/default.css",
  "packages/ui/default.css",
  "apps/editor/public/default.css",
  "apps/editor/public/styles/default.css",
  "apps/landing/public/styles/default.css",
  "public/default.css",
  "public/styles/default.css",
];

const LEGACY_CANONICAL = path.join(ROOT, "ids-canonical.json");

const SKILL_CANDIDATES = [
  "SKILL.md",
  "skills/SKILL.md",
  "docs/SKILL.md",
  ".github/SKILL.md",
];

const CHANGELOG_CANDIDATES = [
  "CHANGELOG.md",
  "CHANGELOG.markdown",
  "docs/CHANGELOG.md",
  "docs/changelog.md",
  "History.md",
];

function githubToken() {
  return process.env.GITHUB_TOKEN?.trim() || "";
}

function encodeGithubPathSegments(relPath) {
  return relPath
    .split("/")
    .filter(Boolean)
    .map(encodeURIComponent)
    .join("/");
}

function rawUrlFor(relPath) {
  const enc = encodeGithubPathSegments(relPath);
  return `${RAW_BASE}/${enc}`;
}

function githubBlobViewerUrl(relPath) {
  return `https://github.com/${GH_OWNER}/${GH_REPO}/blob/${encodeURIComponent(GH_REF)}/${encodeGithubPathSegments(relPath)}`;
}

function resolveLocalIdsRoot() {
  const envPath = process.env.IDS_REPO_PATH?.trim();
  const ordered = [];
  if (envPath) ordered.push(path.resolve(envPath));
  ordered.push(path.join(ROOT, "..", "ids"));
  for (const dir of ordered) {
    try {
      if (fs.existsSync(dir) && fs.statSync(dir).isDirectory()) {
        return dir;
      }
    } catch {
      /* ignore */
    }
  }
  return null;
}

/** Verbose filesystem scan — logs every CSS candidate path. */
function tryReadLocalCssCandidates(repoRoot, candidates) {
  console.log("[ids:sync] default CSS LOCAL scan:", repoRoot);

  let found = null;
  for (const rel of candidates) {
    const abs = path.join(repoRoot, ...rel.split("/"));
    let exists = false;
    try {
      exists = fs.existsSync(abs) && fs.statSync(abs).isFile();
    } catch {
      exists = false;
    }

    console.log(
      "[ids:sync] default CSS LOCAL:",
      exists ? "found   " : "missing ",
      abs,
    );

    if (exists && !found) {
      try {
        const text = fs.readFileSync(abs, "utf8");
        found = { rel, absPath: abs, idsRoot: repoRoot, text };
      } catch (e) {
        console.warn(
          "[ids:sync] default CSS LOCAL read failed:",
          abs,
          String(e.message || e),
        );
      }
    }
  }

  if (found) {
    console.log(
      "[ids:sync] default CSS LOCAL FINAL:",
      found.rel,
      "(" + repoRoot + ")",
    );
  }

  return found ?? null;
}

function tryReadLocalFileCandidates(candidates, label) {
  const root = resolveLocalIdsRoot();
  if (!root) return null;
  for (const rel of candidates) {
    const abs = path.join(root, ...rel.split("/"));
    try {
      if (!fs.existsSync(abs) || !fs.statSync(abs).isFile()) continue;
      const text = fs.readFileSync(abs, "utf8");
      console.log(
        "[ids:sync]",
        label,
        "LOCAL FINAL:",
        rel,
        "(" + root + ")",
      );
      return {
        rel,
        absPath: abs,
        idsRoot: root,
        text,
        usedAuth: false,
        fromLocalRepo: true,
      };
    } catch (e) {
      console.warn(
        "[ids:sync]",
        label + " LOCAL read failed:",
        abs,
        String(e.message || e),
      );
    }
  }
  return null;
}

async function fetchTextOk(url, labelForLog, useAuth = false) {
  const tok = githubToken();
  const headers = {};
  if (useAuth && tok) {
    headers.Authorization = `Bearer ${tok}`;
    headers.Accept = headers.Accept || "*/*";
  }
  const ac = new AbortController();
  const t = setTimeout(() => ac.abort(), 45_000);
  let res;
  try {
    res = await fetch(url, {
      redirect: "follow",
      signal: ac.signal,
      method: "GET",
      headers,
    });
  } finally {
    clearTimeout(t);
  }
  console.log("[ids:sync]", labelForLog, "attempt:", url);
  console.log(
    "[ids:sync]",
    labelForLog,
    "status:",
    res.status,
    res.statusText,
    useAuth && tok ? "(Bearer)" : "(no auth)",
  );
  if (!res.ok) {
    throw new Error(`${res.status} ${res.statusText}`);
  }
  return res.text();
}

async function fetchContentsApiRaw(relPath, labelForLog) {
  const tok = githubToken();
  if (!tok) return null;

  const p = encodeGithubPathSegments(relPath);
  const apiUrl = `https://api.github.com/repos/${GH_OWNER}/${GH_REPO}/contents/${p}?ref=${encodeURIComponent(GH_REF)}`;

  const ac = new AbortController();
  const t = setTimeout(() => ac.abort(), 45_000);
  let res;
  try {
    res = await fetch(apiUrl, {
      redirect: "follow",
      signal: ac.signal,
      method: "GET",
      headers: {
        Authorization: `Bearer ${tok}`,
        Accept: "application/vnd.github.v3.raw",
        "User-Agent": "ids-landing-sync-script",
      },
    });
  } finally {
    clearTimeout(t);
  }

  console.log("[ids:sync]", labelForLog, "attempt (Contents API):", apiUrl);
  console.log(
    "[ids:sync]",
    labelForLog,
    "API status:",
    res.status,
    res.statusText,
    "(Bearer)",
  );

  if (!res.ok) {
    const errBody =
      (
        await res.text().catch(() => "").then((x) =>
          typeof x === "string" ? x.trim().slice(0, 280) : "",
        )
      ).replace(/\s+/g, " ");
    if (errBody) {
      console.warn("[ids:sync]", labelForLog, "Contents API response:", errBody);
    }
    throw new Error(`${res.status} ${res.statusText}`);
  }
  return res.text();
}

/**
 * Fetch one logical file across remote strategies for a relative path candidate.
 */
async function fetchRemoteOne(relPath, label) {
  const urlPublic = rawUrlFor(relPath);
  let usedAuthRemote = false;

  if (githubToken()) {
    try {
      const text = await fetchTextOk(urlPublic, label, true);
      usedAuthRemote = true;
      return {
        text,
        rawUrl: urlPublic,
        usedAuthRemote,
        viewerUrl: githubBlobViewerUrl(relPath),
      };
    } catch (_) {
      /* try Contents API below */
    }
    try {
      const text = await fetchContentsApiRaw(relPath, label);
      usedAuthRemote = true;
      return {
        text,
        rawUrl: urlPublic,
        usedAuthRemote,
        viewerUrl: githubBlobViewerUrl(relPath),
      };
    } catch (_) {
      /* fall through public raw */
    }
  }

  const text = await fetchTextOk(urlPublic, label, false);
  usedAuthRemote = false;
  return {
    text,
    rawUrl: urlPublic,
    usedAuthRemote,
    viewerUrl: urlPublic,
  };
}

async function tryRemoteCandidates(candidates, label) {
  let lastWarn = "";

  if (githubToken()) {
    console.log(
      "[ids:sync]",
      `${label}: GITHUB_TOKEN is set → trying Bearer raw, then Contents API, then public raw`,
    );
  }

  for (const rel of candidates) {
    const urlPublic = rawUrlFor(rel);
    try {
      const { text, rawUrl, usedAuthRemote, viewerUrl } =
        await fetchRemoteOne(rel, label);
      console.log(
        "[ids:sync]",
        label + " REMOTE FINAL:",
        rel,
        "(" + rawUrl + ")",
      );
      return {
        rel,
        url: rawUrl,
        text,
        usedAuthRemote,
        canonicalViewerUrl: viewerUrl,
      };
    } catch (e) {
      lastWarn = String(e.message || e);
      console.warn(
        "[ids:sync]",
        label + ":",
        urlPublic,
        "→",
        lastWarn,
      );
    }
  }

  console.warn("[ids:sync]", label + ": no candidate returned 200 remotely");
  if (githubToken()) {
    console.warn(
      "[ids:sync]",
      `${label}: GITHUB_TOKEN was set but all remote attempts failed.`,
      "Check scopes (fine-grained: Contents read / classic: repo).",
      "Falling through to landing fallbacks if needed.",
    );
  }

  return null;
}

async function headFetch(url, useAuth, label) {
  const tok = githubToken();
  const headers = {};
  if (useAuth && tok) headers.Authorization = `Bearer ${tok}`;

  const ac = new AbortController();
  const t = setTimeout(() => ac.abort(), 15_000);
  let res;
  try {
    res = await fetch(url, {
      method: "HEAD",
      redirect: "follow",
      signal: ac.signal,
      headers,
    });
  } finally {
    clearTimeout(t);
  }

  console.log(
    "[ids:sync] probe",
    `${label}: ${url}`,
    useAuth ? "→ (Bearer HEAD)" : "→ (public HEAD)",
    res.status,
    res.statusText,
  );
  return res.ok;
}

async function probeRemoteFirstMatch(candidates, label) {
  for (const rel of candidates) {
    const url = rawUrlFor(rel);
    const tok = githubToken();
    if (tok) {
      if (await headFetch(url, true, label)) return rel;
    }
    if (await headFetch(url, false, label)) return rel;

    /** Some hosts mis-handle HEAD; quick GET fallback with auth only */
    if (tok) {
      try {
        await fetchContentsApiRaw(rel, `probe:${label}`);
        console.log("[ids:sync] probe", label + ": API GET ok →", rel);
        return rel;
      } catch {
        /* continue */
      }
    }
  }
  return null;
}

async function probeDocPresence(candidates, label) {
  const root = resolveLocalIdsRoot();
  if (root) {
    for (const rel of candidates) {
      const abs = path.join(root, ...rel.split("/"));
      if (fs.existsSync(abs) && fs.statSync(abs).isFile()) {
        console.log("[ids:sync] probe", label + ": LOCAL ok", abs);
        return rel;
      }
    }
  }
  return probeRemoteFirstMatch(candidates, label);
}

function copyFallbackCanonical() {
  if (fs.existsSync(LEGACY_CANONICAL)) {
    fs.copyFileSync(LEGACY_CANONICAL, OUT_CANONICAL);
    console.warn(
      "[ids:sync] FALLBACK: wrote data/ids-canonical.json from local root ids-canonical.json.",
    );
    return fs.readFileSync(OUT_CANONICAL, "utf8");
  }
  if (fs.existsSync(OUT_CANONICAL)) {
    console.warn(
      "[ids:sync] FALLBACK: keeping existing data/ids-canonical.json.",
    );
    return fs.readFileSync(OUT_CANONICAL, "utf8");
  }
  return null;
}

function copyFallbackCss() {
  if (fs.existsSync(OUT_CSS)) {
    console.warn(
      "[ids:sync] FALLBACK: keeping existing styles/default.css.",
    );
    return;
  }
  console.warn(
    "[ids:sync] WARNING: styles/default.css is missing locally and could not be resolved.",
  );
}

async function main() {
  if (!fs.existsSync(DATA)) fs.mkdirSync(DATA, { recursive: true });
  if (!fs.existsSync(STYLES)) fs.mkdirSync(STYLES, { recursive: true });

  const localIds = resolveLocalIdsRoot();

  console.log("[ids:sync] Branch/ref:", GH_REF);
  console.log("[ids:sync] Raw base:", RAW_BASE);
  console.log(
    "[ids:sync] Canonical candidates:",
    CANONICAL_CANDIDATES.join(", "),
  );
  console.log("[ids:sync] CSS_CANDIDATES:", CSS_CANDIDATES.join(", "));

  console.log(
    "[ids:sync] IDS_REPO_PATH:",
    process.env.IDS_REPO_PATH?.trim() || "(not set)",
  );
  if (localIds) {
    console.log("[ids:sync] Resolved local IDS checkout:", localIds);
  } else {
    console.log(
      "[ids:sync] No local IDS checkout (set IDS_REPO_PATH or clone to ../ids).",
    );
  }

  if (githubToken()) {
    console.log(
      "[ids:sync] GITHUB_TOKEN:",
      "(set → authenticated GitHub attempts enabled)",
    );
  } else {
    console.warn(
      "[ids:sync] GITHUB_TOKEN: not set → private repos need a PAT or IDS_REPO_PATH.",
    );
  }

  let canonicalPathUsed = null;
  let canonicalPayload = null;
  let canonicalUrlForLinks = null;
  let canonicalUsedRemoteAuth = false;
  /** @type {{ rel: string, text: string, usedAuthRemote?: boolean, canonicalViewerUrl?: string } | null } */
  let canonicalRemoteMeta = null;

  const canonLocal = tryReadLocalFileCandidates(
    CANONICAL_CANDIDATES,
    "canonical JSON",
  );
  if (canonLocal) {
    canonicalPayload = canonLocal.text;
    canonicalPathUsed =
      "LOCAL_REPO:" +
      canonLocal.rel +
      " @" +
      path.relative(ROOT, canonLocal.idsRoot);
    canonicalUrlForLinks = null;
    canonicalUsedRemoteAuth = false;
    console.log(
      "[ids:sync]",
      `canonical LOCAL_REPO (${path.relative(ROOT, canonLocal.idsRoot)})`,
    );
  } else {
    canonicalRemoteMeta = await tryRemoteCandidates(
      CANONICAL_CANDIDATES,
      "canonical JSON",
    );
    if (canonicalRemoteMeta) {
      canonicalPayload = canonicalRemoteMeta.text;
      canonicalPathUsed = canonicalRemoteMeta.rel;
      canonicalUsedRemoteAuth = canonicalRemoteMeta.usedAuthRemote;
      canonicalUrlForLinks =
        canonicalRemoteMeta.usedAuthRemote
          ? canonicalRemoteMeta.canonicalViewerUrl
          : canonicalRemoteMeta.url;
      console.log(
        "[ids:sync] canonical:",
        canonicalPathUsed,
        canonicalUsedRemoteAuth ? "(authenticated)" : "(public)",
      );
    }
  }

  if (!canonicalPayload) {
    console.error("[ids:sync] Canonical not resolved from IDS — using fallback.");
    canonicalPayload = copyFallbackCanonical();
    if (!canonicalPayload) {
      console.error(
        "No canonical JSON available. Provide IDS_REPO_PATH, GITHUB_TOKEN, or ids-canonical.json in project root.",
      );
      process.exitCode = 1;
      return;
    }
    if (fs.existsSync(LEGACY_CANONICAL)) {
      canonicalPathUsed = canonicalPathUsed || "LOCAL_ROOT:ids-canonical.json";
    } else {
      canonicalPathUsed =
        canonicalPathUsed ||
        `LOCAL_KEEP:${path.relative(ROOT, OUT_CANONICAL)}`;
    }
    canonicalUrlForLinks = null;
  }

  fs.writeFileSync(OUT_CANONICAL, canonicalPayload, "utf8");

  let cssPathUsed = null;
  let cssPayload = null;
  let stylesheetUrlGithub = null;
  let stylesheetUsedRemoteAuth = false;

  const cssLocal = localIds
    ? tryReadLocalCssCandidates(localIds, CSS_CANDIDATES)
    : null;
  if (cssLocal) {
    cssPayload = cssLocal.text;
    cssPathUsed = "LOCAL_REPO:" + cssLocal.rel;
    stylesheetUrlGithub = null;
    console.log(
      "[ids:sync]",
      `stylesheet LOCAL_REPO (${path.relative(ROOT, cssLocal.idsRoot)})`,
      "→ copied to styles/default.css",
    );
  } else {
    const cssRemote = await tryRemoteCandidates(
      CSS_CANDIDATES,
      "default CSS",
    );
    if (cssRemote) {
      cssPayload = cssRemote.text;
      cssPathUsed = cssRemote.rel;
      stylesheetUsedRemoteAuth = cssRemote.usedAuthRemote;
      stylesheetUrlGithub = cssRemote.usedAuthRemote
        ? cssRemote.canonicalViewerUrl
        : cssRemote.url;
    }
  }

  if (cssPayload) {
    fs.writeFileSync(OUT_CSS, cssPayload, "utf8");
  } else {
    if (localIds) {
      console.warn(
        "[ids:sync] No CSS found in IDS repo. Run the IDS CSS export/build step or add the correct path to CSS_CANDIDATES.",
      );
    }
    console.warn("[ids:sync] Stylesheet not resolved from IDS — using fallback.");
    copyFallbackCss();
    if (fs.existsSync(OUT_CSS)) {
      cssPathUsed =
        cssPathUsed || `LOCAL_KEEP:${path.relative(ROOT, OUT_CSS)}`;
    } else cssPathUsed = cssPathUsed || "MISSING";
    stylesheetUrlGithub = null;
  }

  let data;
  try {
    data = JSON.parse(canonicalPayload);
  } catch (e) {
    console.error("Invalid JSON in canonical:", e.message);
    process.exitCode = 1;
    return;
  }

  const reg = data?.componentRegistry?.components;
  if (!Array.isArray(reg)) {
    console.error("Missing componentRegistry.components in ids-canonical.json");
    process.exitCode = 1;
    return;
  }

  const skillPath = await probeDocPresence(SKILL_CANDIDATES, "SKILL");
  const changelogPath = await probeDocPresence(
    CHANGELOG_CANDIDATES,
    "changelog",
  );

  const canonicalStoredUrl =
    typeof canonicalUrlForLinks === "string" &&
    canonicalUrlForLinks.startsWith("http")
      ? canonicalUrlForLinks
      : null;

  const stylesheetStoredUrl =
    typeof stylesheetUrlGithub === "string" &&
    stylesheetUrlGithub.startsWith("http")
      ? stylesheetUrlGithub
      : !stylesheetUsedRemoteAuth &&
          cssPathUsed &&
          !String(cssPathUsed).startsWith("LOCAL_") &&
          cssPathUsed !== "MISSING"
        ? rawUrlFor(cssPathUsed)
        : null;

  fs.writeFileSync(
    DOC_LINKS,
    JSON.stringify(
      {
        skillPath,
        changelogPath,
        canonicalPath: canonicalPathUsed,
        canonicalUrl: canonicalStoredUrl,
        stylesheetPath: cssPathUsed,
        stylesheetUrlGithub: stylesheetStoredUrl,
        ghRef: GH_REF,
        localIdsRoot: localIds ? path.relative(ROOT, localIds) : null,
        usedGithubToken: githubToken().length > 0,
        repo: `https://github.com/${GH_OWNER}/${GH_REPO}`,
        probedAt: new Date().toISOString(),
      },
      null,
      2,
    ) + "\n",
    "utf8",
  );

  console.log("generatedAt:", data.generatedAt ?? "(none)");
  console.log("gitCommit:", data.gitCommit ?? "(none)");
  console.log("component count:", reg.length);
  console.log("");
  console.log("[ids:sync] ───────── selected sources ─────────");
  console.log("[ids:sync] canonical:", canonicalPathUsed ?? "(missing)");
  if (canonicalStoredUrl) {
    console.log("[ids:sync] canonical link:", canonicalStoredUrl);
  }
  console.log("[ids:sync] stylesheet:", cssPathUsed ?? "(missing)");
  if (stylesheetStoredUrl) {
    console.log("[ids:sync] stylesheet link:", stylesheetStoredUrl);
  }
  console.log("[ids:sync] SKILL:", skillPath ?? "(none)");
  console.log("[ids:sync] changelog:", changelogPath ?? "(none)");
  console.log("[ids:sync] ───────────────────────────────────");
  console.log("");
  console.log("Wrote:", path.relative(ROOT, OUT_CANONICAL));
  console.log("Wrote:", path.relative(ROOT, OUT_CSS));
  console.log("Wrote:", path.relative(ROOT, DOC_LINKS));
}

main();
