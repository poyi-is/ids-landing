/**
 * Canonical site header for landing, Docs, and Components.
 * Mounts into #ids-site-header (replaces that node with <header class="site-topbar">…</header>).
 */
(function () {
  function pathPrefix() {
    var pathname = (window.location.pathname || "").replace(/\\/g, "/");
    if (pathname.indexOf("/components/") !== -1) return "../";
    return "./";
  }

  function componentsEntryHref(prefix) {
    return prefix === "../" ? "./alert.html" : "./components/alert.html";
  }

  function detectActiveNav() {
    var pathname = (window.location.pathname || "").replace(/\\/g, "/");
    var file = pathname.split("/").pop() || "";
    if (file === "docs.html") return { docs: true, comps: false };
    if (file === "components.html") return { docs: false, comps: true };
    if (pathname.indexOf("/components/") !== -1) return { docs: false, comps: true };
    return { docs: false, comps: false };
  }

  function mount() {
    var el = document.getElementById("ids-site-header");
    if (!el) return;

    var prefix = pathPrefix();
    var href = {
      home: prefix + "index.html",
      docs: prefix + "docs.html",
      components: componentsEntryHref(prefix),
      install: prefix + "docs.html#install",
    };

    var active = detectActiveNav();
    var docsAttr = active.docs ? ' aria-current="page"' : "";
    var compAttr = active.comps ? ' aria-current="page"' : "";

    var html =
      '<header class="site-topbar">' +
      '<a href="' +
      href.home +
      '" class="topbar-brand" aria-label="Ionic DS — Home">' +
      '<div class="topbar-logo">I<span class="topbar-logo-dot pulse" aria-hidden="true"></span></div>' +
      '<span class="display topbar-lockup-title">Ionic DS</span>' +
      '<span class="mono topbar-version">v1.4</span>' +
      "</a>" +
      '<nav class="topbar-nav" aria-label="Primary">' +
      '<a class="topbar-link" href="' +
      href.docs +
      '"' +
      docsAttr +
      ">Docs</a>" +
      '<a class="topbar-link" href="' +
      href.components +
      '"' +
      compAttr +
      ">Components</a>" +
      '<a class="topbar-link" data-nav-doc="skill" href="#" hidden>SKILL.md</a>' +
      '<a class="topbar-link" data-nav-doc="changelog" href="#" hidden>Changelog</a>' +
      "</nav>" +
      '<div class="topbar-actions">' +
      '<a class="lp-btn lp-btn-sm" data-variant="ghost" href="https://github.com/poyi-is/ids">GitHub</a>' +
      '<a class="lp-btn lp-btn-sm-accent" data-variant="accent" href="' +
      href.install +
      '">Install</a>' +
      "</div>" +
      "</header>";

    var tmpl = document.createElement("template");
    tmpl.innerHTML = html.trim();
    el.replaceWith(tmpl.content.firstChild);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount);
  } else {
    mount();
  }
})();
