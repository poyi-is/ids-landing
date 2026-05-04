# ids-landing

Static site for Ionic DS / IDS docs and previews.

**Do not commit secrets.** Use environment variables such as `GITHUB_TOKEN` — never `.env` with real tokens in git (`.env*` is ignored; there is no example file committed by default).

## GitHub sync (`npm run ids:sync`)

The script **`scripts/sync-ids-canonical.js`** resolves:

- **`data/ids-canonical.json`** — component registry (+ metadata written by build)
- **`styles/default.css`** — IDS stylesheet

### Resolution order (same for JSON and CSS)

1. **Local IDS checkout** (fastest for private repos you already have cloned)  
   - If **`IDS_REPO_PATH`** points to an existing directory, that repo is checked first (any path).
   - Otherwise, if **`../ids`** exists next to `ids-landing`, it is used.
   - Under that root it looks for candidates in **order below** until a file exists on disk.

2. **Authenticated GitHub** (private `poyi-is/ids`)  
   - Set **`GITHUB_TOKEN`** (fine-grained: repository **Contents read** access, or classic PAT with **`repo`** for private repos).  
   - The script tries **GET** on `raw.githubusercontent.com` with **`Authorization: Bearer`**.
   - If that fails, it uses the **Repos Contents API** with **`Accept: application/vnd.github.v3.raw`**.
   - For authenticated fetches, `data/doc-links.json` prefers a **`github.com` /blob/ …** viewer link (raw URLs rarely work anonymously for private blobs).

3. **Public GitHub raw** — same URLs **without** a token.

4. **Landing fallbacks**  
   - Canonical: **`ids-canonical.json`** in landing **project root**, else keep existing **`data/ids-canonical.json`**.  
   - CSS: keep existing **`styles/default.css`** when nothing else resolves.

Logs show **each URL attempted**, **status codes**, **`GITHUB_TOKEN`** / **`IDS_REPO_PATH`** presence (never the token value), and a short **FINAL summary**.

Optional **`IDS_GIT_REF`** overrides the Git branch/ref (default **`main`**).

### Probed filenames (canonical + stylesheet)

Inside the chosen IDS root or on GitHub, candidates are tested **in order**:

**Canonical JSON**

1. `ids-canonical.json`
2. `exports/ids-canonical.json`

**Stylesheet**

1. **`gh-pages/styles/default.css`** — generated in **`poyi-is/ids`** by **`npx tsx scripts/generate-gh-pages-css.ts`** (reads **`ids-snapshot.json`** in the IDS repo root)
2. `default.css`
3. `styles/default.css`
4. `exports/default.css`
5. `exports/styles/default.css`
6. `dist/default.css`
7. `packages/ui/dist/default.css`
8. `packages/ui/dist/styles/default.css`
9. `packages/ui/default.css`
10. `apps/editor/public/default.css`
11. `apps/editor/public/styles/default.css`
12. `apps/landing/public/styles/default.css`
13. `public/default.css`
14. `public/styles/default.css`

For a local checkout, sync logs **`found`** / **`missing`** for **each absolute path**. If **`gh-pages/styles/default.css`** is missing in IDS, regenerate it with **`npx tsx scripts/generate-gh-pages-css.ts`** (from the IDS checkout, with **`ids-snapshot.json`** present). If none of the listed paths exist next to **`IDS_REPO_PATH`**, you’ll see **`No CSS found in IDS repo. Run the IDS CSS export/build step or add the correct path to CSS_CANDIDATES.`** Extend the **`CSS_CANDIDATES`** array in **`scripts/sync-ids-canonical.js`** when your layout differs.
### Setup examples

**Option A — Local repo**

Clone `poyi-is/ids` and point sync at your machine (same layout as `./ids-canonical.json` relative to checkout root):

```bash
IDS_REPO_PATH=/Users/joh/ids npm run ids:sync
```

Alternatively, clone **next to** this repo as **`../ids`** and run without **`IDS_REPO_PATH`**.

**Option B — GitHub token (private or when you have no checkout)**

Never paste tokens into tracked files:

```bash
GITHUB_TOKEN=your_token_here npm run ids:sync
```

If both **`IDS_REPO_PATH`** and **`GITHUB_TOKEN`** fail to produce files, sync **warns clearly** and uses the landing fallbacks when possible.

### `data/doc-links.json`

Emitted by sync: **`canonicalPath`**, **`canonicalUrl`** (when useful), stylesheet paths/links, **`ghRef`**, relative **`localIdsRoot`**, and **`usedGithubToken`** (boolean).

**Component pages** read this during **`python3 scripts/build_components_html.py`** to show badges (**Source: Local IDS repo**, **Local fallback**, or **GitHub**).

## Docs build

After sync:

```bash
npm run ids:sync
python3 scripts/build_components_html.py
```

## Local preview

```bash
npx serve .
```

## Theme toggle

Pages load **`theme-toggle.js`**: theme follows **`prefers-color-scheme`** unless **`localStorage`** (`ids-docs-theme`) differs. **`data-theme`** on `<html>` drives shell tokens in **`docs-shell.css`**; preview panels remap IDS semantics for light/dark readability.
