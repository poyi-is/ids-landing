/**
 * Docs + landing theme: prefers-color-scheme default, persisted in localStorage.
 * Expects docs-shell.css :root[data-theme="light"|"dark"] tokens.
 */
(function () {
  var STORAGE_KEY = "ids-docs-theme";

  function systemTheme() {
    try {
      return window.matchMedia("(prefers-color-scheme: dark)").matches
        ? "dark"
        : "light";
    } catch (_) {
      return "dark";
    }
  }

  function readStored() {
    try {
      return localStorage.getItem(STORAGE_KEY);
    } catch (_) {
      return null;
    }
  }

  function effectiveTheme() {
    var s = readStored();
    if (s === "light" || s === "dark") return s;
    return systemTheme();
  }

  function labelFor(theme) {
    return theme === "dark" ? "Dark mode (click for light)" : "Light mode (click for dark)";
  }

  function iconSvg(theme) {
    if (theme === "dark") {
      return '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>';
    }
    return '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>';
  }

  function updateButtons(theme) {
    var nodes = document.querySelectorAll(".ids-theme-toggle");
    for (var i = 0; i < nodes.length; i++) {
      var b = nodes[i];
      b.setAttribute("aria-label", labelFor(theme));
      b.setAttribute("title", labelFor(theme));
      b.innerHTML =
        '<span class="ids-theme-toggle-inner">' + iconSvg(theme) + "</span>";
    }
  }

  function apply(theme) {
    if (theme !== "light" && theme !== "dark") theme = systemTheme();
    document.documentElement.setAttribute("data-theme", theme);
    updateButtons(theme);
    try {
      window.dispatchEvent(
        new CustomEvent("ids-theme-applied", { detail: { theme: theme } })
      );
    } catch (_) {}
  }

  /** Used by the landing tweaks panel and other shells to stay in sync with the nav toggle. */
  window.__idsApplyTheme = function (theme) {
    if (theme !== "light" && theme !== "dark") return;
    try {
      localStorage.setItem(STORAGE_KEY, theme);
    } catch (_) {}
    apply(theme);
  };

  apply(effectiveTheme());

  try {
    window
      .matchMedia("(prefers-color-scheme: dark)")
      .addEventListener("change", function () {
        var s = readStored();
        if (s !== "light" && s !== "dark") apply(systemTheme());
      });
  } catch (_) {}

  function toggle() {
    var cur =
      document.documentElement.getAttribute("data-theme") === "light"
        ? "light"
        : "dark";
    var next = cur === "dark" ? "light" : "dark";
    try {
      localStorage.setItem(STORAGE_KEY, next);
    } catch (_) {}
    apply(next);
  }

  function makeButton() {
    var b = document.createElement("button");
    b.type = "button";
    b.className = "lp-btn lp-btn-sm ids-theme-toggle";
    var t =
      document.documentElement.getAttribute("data-theme") === "light"
        ? "light"
        : "dark";
    b.setAttribute("aria-label", labelFor(t));
    b.innerHTML =
      '<span class="ids-theme-toggle-inner">' + iconSvg(t) + "</span>";
    b.addEventListener("click", toggle);
    return b;
  }

  function inject() {
    var wraps = document.querySelectorAll(".topbar-actions");
    for (var i = 0; i < wraps.length; i++) {
      var w = wraps[i];
      if (!w.querySelector(".ids-theme-toggle")) {
        w.insertBefore(makeButton(), w.firstChild);
      }
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", inject);
  } else {
    inject();
  }

  try {
    var obs = new MutationObserver(function () {
      inject();
    });
    obs.observe(document.documentElement, { childList: true, subtree: true });
  } catch (_) {
    window.setInterval(inject, 1500);
  }
})();
