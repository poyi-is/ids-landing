(function () {
  function docLinksHref() {
    try {
      return new URL("../data/doc-links.json", window.location.href).href;
    } catch (_) {
      return "./data/doc-links.json";
    }
  }

  var RAW_BASE = "https://raw.githubusercontent.com/poyi-is/ids/main";
  var REPO_BLOB_MAIN = "https://github.com/poyi-is/ids/blob/main";

  var pathsCache = null;
  var resolving = null;

  function blobHref(relPath) {
    return REPO_BLOB_MAIN + "/" + relPath.split("/").map(encodeURIComponent).join("/");
  }

  function headOk(url) {
    return fetch(url, { method: "HEAD", mode: "cors", cache: "no-store" })
      .then(function (r) {
        return r.ok;
      })
      .catch(function () {
        return false;
      });
  }

  async function probeSequential(paths) {
    for (var i = 0; i < paths.length; i++) {
      var rel = paths[i];
      var u =
        RAW_BASE + "/" + rel.split("/").map(encodeURIComponent).join("/");
      if (await headOk(u)) return rel;
    }
    return null;
  }

  async function resolvePathsOnce() {
    if (pathsCache) return pathsCache;
    if (resolving) return resolving;

    resolving = (async function () {
      var skillPath = null;
      try {
        var mr = await fetch(docLinksHref(), {
          cache: "no-store",
        });
        if (mr.ok) {
          var m = await mr.json();
          if (typeof m.skillPath === "string" && m.skillPath) skillPath = m.skillPath;
        }
      } catch (_) {}

      if (!skillPath) {
        skillPath = await probeSequential([
          "SKILL.md",
          "skills/SKILL.md",
          "docs/SKILL.md",
          ".github/SKILL.md",
        ]);
      }

      pathsCache = { skillPath: skillPath };
      resolving = null;
      return pathsCache;
    })();

    return resolving;
  }

  var appliedEl = typeof WeakSet !== "undefined" ? new WeakSet() : null;

  async function bindOptionalDocsLinks() {
    var els = []
      .slice.call(document.querySelectorAll("[data-nav-doc]"))
      .filter(function (el) {
        return !appliedEl || !appliedEl.has(el);
      });
    if (!els.length) return;

    var p = await resolvePathsOnce();

    els.forEach(function (el) {
      var kind = el.getAttribute("data-nav-doc");
      var resolved = kind === "skill" ? p.skillPath : null;

      if (appliedEl) appliedEl.add(el);

      if (!resolved) {
        el.parentNode && el.parentNode.removeChild(el);
        return;
      }

      el.setAttribute("href", blobHref(resolved));
      el.removeAttribute("hidden");
    });
  }

  function scheduleBind() {
    bindOptionalDocsLinks().catch(function () {});
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", scheduleBind);
  } else scheduleBind();

  var moScheduled;
  try {
    var mo = new MutationObserver(function () {
      clearTimeout(moScheduled);
      moScheduled = setTimeout(scheduleBind, 80);
    });
    mo.observe(document.documentElement, { childList: true, subtree: true });
  } catch (_) {}
})();
