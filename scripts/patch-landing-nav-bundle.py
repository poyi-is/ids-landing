#!/usr/bin/env python3
"""Patch index.html bundler template + inline SiteTopbar chunk for shared site header."""
import base64
import gzip
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
BABEL_UUID = "e93a9179-2cce-400b-8145-f9595b4e5dc4"
TERMINAL_HERO_UUID = "1cf7f706-65e2-47bd-96b0-9a78a75dc31c"

OLD_APPLY = """function applyTweaks() {
  document.documentElement.setAttribute('data-theme', window.__tweaks.theme);
  document.documentElement.setAttribute('data-motion', window.__tweaks.motion);
  document.querySelectorAll('.tweaks-panel .tweak-chip').forEach(chip => {
    const group = chip.parentElement.getAttribute('data-group');
    chip.setAttribute('data-active', String(window.__tweaks[group] === chip.getAttribute('data-val')));
  });
  window.dispatchEvent(new CustomEvent('tweaks-changed'));
}"""

NEW_APPLY = """function paintTweakChips() {
  document.querySelectorAll('.tweaks-panel .tweak-chip').forEach(chip => {
    const group = chip.parentElement.getAttribute('data-group');
    chip.setAttribute('data-active', String(window.__tweaks[group] === chip.getAttribute('data-val')));
  });
}

function syncLandingTweakThemeFromDocument() {
  var cur = document.documentElement.getAttribute('data-theme');
  if (cur === 'light' || cur === 'dark') window.__tweaks.theme = cur;
}

function applyTweaks() {
  if (window.__idsApplyTheme) {
    window.__idsApplyTheme(window.__tweaks.theme);
  } else {
    document.documentElement.setAttribute('data-theme', window.__tweaks.theme);
  }
  document.documentElement.setAttribute('data-motion', window.__tweaks.motion);
  paintTweakChips();
  window.dispatchEvent(new CustomEvent('tweaks-changed'));
}

window.addEventListener('ids-theme-applied', function (e) {
  var th = e.detail && e.detail.theme;
  if (th !== 'light' && th !== 'dark') return;
  window.__tweaks.theme = th;
  paintTweakChips();
});"""

SITE_TOPBAR_FN = """function SiteTopbar() {
  return (
    <header style={{
      position: 'sticky', top: 0, zIndex: 50,
      background: 'color-mix(in srgb, var(--lp-bg) 88%, transparent)',
      backdropFilter: 'blur(12px)',
      borderBottom: '1px solid var(--lp-border)',
      padding: '14px 48px', display: 'flex', alignItems: 'center', gap: 40,
    }}>
      <a href="./index.html" aria-label="Ionic DS — Home" style={{ display: 'flex', alignItems: 'center', gap: 10, color: 'inherit', textDecoration: 'none' }}>
        <div style={{ width: 24, height: 24, background: 'var(--lp-primary)', borderRadius: 5, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', fontFamily: 'Geist, sans-serif', fontWeight: 700, fontSize: 13, position: 'relative' }}>
          I
          <span className="pulse" style={{ position: 'absolute', top: -2, right: -2, width: 6, height: 6 }}/>
        </div>
        <span className="display" style={{ fontWeight: 600, fontSize: 15 }}>Ionic DS</span>
        <span className="mono" style={{ fontSize: 10, color: 'var(--lp-fg-subtle)', letterSpacing: '0.1em', padding: '2px 6px', background: 'var(--lp-bg-inset)', borderRadius: 4, marginLeft: 4 }}>v1.4</span>
      </a>
      <nav style={{ display: 'flex', gap: 24, flex: 1 }} aria-label="Primary">
        <a href="./docs.html" style={{ fontSize: 13, color: 'var(--lp-fg-muted)', cursor: 'pointer', textDecoration: 'none' }}>Docs</a>
        <a href="./components/alert.html" style={{ fontSize: 13, color: 'var(--lp-fg-muted)', cursor: 'pointer', textDecoration: 'none' }}>Components</a>
        <a href="#" hidden data-nav-doc="skill" style={{ fontSize: 13, color: 'var(--lp-fg-muted)', cursor: 'pointer', textDecoration: 'none' }}>SKILL.md</a>
      </nav>
      <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
        <a href="https://github.com/poyi-is/ids" className="lp-btn" data-variant="ghost" style={{ padding: '6px 12px', fontSize: 13 }}>GitHub</a>
        <a href="./docs.html#install" className="lp-btn" data-variant="accent" style={{ padding: '6px 14px', fontSize: 13 }}>Install</a>
      </div>
    </header>
  );
}

"""


VIEWPORT_FONTS = """<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/inter@5.2.5/index.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/inter@5.2.5/500.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/inter@5.2.5/600.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/inter@5.2.5/700.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/geist-sans@5.2.5/index.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/geist-sans@5.2.5/600.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/geist-mono@5.2.5/index.css">
<script src="./theme-toggle.js"></script>


<style>"""

TWEAK_END_MARKER = (
    '.tweak-chip[data-active="true"] { background: var(--lp-accent); color: #0A0D13; border-color: var(--lp-accent); }\n'
    "</style>\n\n"
    '<script src="1a56adc0'
)

TWEAK_END_WITH_SHELL = (
    '.tweak-chip[data-active="true"] { background: var(--lp-accent); color: #0A0D13; border-color: var(--lp-accent); }\n'
    "</style>\n\n"
    '<link rel="stylesheet" href="./docs-shell.css">\n\n'
    '<script src="1a56adc0'
)


def patch_template(t: str) -> str:
    t = t.replace(
        '<html lang="en" data-theme="dark" data-motion="on"><head>',
        '<html lang="en" data-motion="on"><head>',
    )

    if "./theme-toggle.js" not in t:
        t = t.replace(
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n\n\n<style>',
            VIEWPORT_FONTS,
        )

    if "./docs-shell.css" not in t:
        if TWEAK_END_MARKER not in t:
            raise SystemExit(
                "template: tweak/style marker missing (unexpected template head layout)"
            )
        t = t.replace(TWEAK_END_MARKER, TWEAK_END_WITH_SHELL, 1)

    if '<div id="ids-site-header"></div>' not in t:
        t = t.replace(
            "<body>\n<div id=\"root\"></div>",
            "<body>\n<div id=\"ids-site-header\"></div>\n<div id=\"root\"></div>",
        )

    if OLD_APPLY in t:
        t = t.replace(OLD_APPLY, NEW_APPLY, 1)

    wt_assign = "window.__tweaks = { ...TWEAK_DEFAULTS };"
    if wt_assign in t and "syncLandingTweakThemeFromDocument();" not in t:
        t = t.replace(
            wt_assign,
            wt_assign + "\nsyncLandingTweakThemeFromDocument();",
            1,
        )

    jsx_nav = (
        "    <div data-screen-label={`Landing · ${t.hero} · ${t.theme}`}>\n"
        "      <SiteTopbar/>\n"
        "      <Hero"
    )
    if jsx_nav in t:
        t = t.replace(
            jsx_nav,
            (
                "    <div data-screen-label={`Landing · ${t.hero} · ${t.theme}`}>\n"
                "      <Hero"
            ),
            1,
        )

    # Embedded `<style>` in the landing template re-declares :root `--lp-*` before
    # docs-shell.css; keep light-mode code surfaces in sync so `var(--lp-code-bg)`
    # (Hero panels + pre.code-pre) matches docs-shell tokens.
    stale_lp_code = "--lp-code-bg: #0A0A0A;\n  --lp-code-fg: #E5E7EB;"
    synced_lp_code = "--lp-code-bg: #f4f5f8;\n  --lp-code-fg: #1a1f28;"
    if stale_lp_code in t:
        t = t.replace(stale_lp_code, synced_lp_code, 1)

    return t


def patch_babel_source(src: str) -> str:
    if SITE_TOPBAR_FN in src:
        src = src.replace(SITE_TOPBAR_FN, "", 1)

    old = "Object.assign(window, { ProblemSection, HowItWorks, SiteTopbar, SiteFooter, useReveal });"
    new = "Object.assign(window, { ProblemSection, HowItWorks, SiteFooter, useReveal });"
    if old in src:
        src = src.replace(old, new, 1)
    elif "SiteTopbar" in src:
        raise SystemExit("babel: orphaned SiteTopbar reference")
    return src


def patch_terminal_hero_chunk(src: str) -> str:
    """Hero2 terminal demo: replace hard-coded dark hex with LP tokens (readable in light theme)."""
    repls = (
        (
            "background: '#131823', border: '1px solid #1E2533', borderRadius: 8,",
            "background: 'var(--lp-bg-elev)', border: '1px solid var(--lp-border)', borderRadius: 8,",
        ),
        (
            "borderBottom: '1px solid #1E2533'",
            "borderBottom: '1px solid var(--lp-border)'",
        ),
        (
            "color: '#6B7589', marginLeft: 12",
            "color: 'var(--lp-fg-subtle)', marginLeft: 12",
        ),
        (
            "lineHeight: 1.8, color: '#E5E7EB', minHeight: 280",
            "lineHeight: 1.8, color: 'var(--lp-code-fg)', minHeight: 280",
        ),
        (
            "<span style={{ color: '#E5E7EB' }}>{text}</span>",
            "<span style={{ color: 'var(--lp-code-fg)' }}>{text}</span>",
        ),
        (
            "fontSize: 11, color: '#9CA6B8', marginBottom: 4",
            "fontSize: 11, color: 'var(--lp-fg-muted)', marginBottom: 4",
        ),
        (
            "fontWeight: 600, color: '#F5F7FA', letterSpacing",
            "fontWeight: 600, color: 'var(--lp-fg)', letterSpacing",
        ),
    )
    for old, new in repls:
        if old in src:
            src = src.replace(old, new)
    src = src.replace("background: '#374151'", "background: 'var(--lp-fg-muted)'")
    return src


def main():
    html = INDEX.read_text(encoding="utf-8")

    tmpl_m = re.search(
        r'(<script type="__bundler/template">)\s*([\s\S]*?)\s*(</script>)',
        html,
    )
    if not tmpl_m:
        raise SystemExit("no template script")
    template_json_inner = tmpl_m.group(2)
    template_obj = json.loads(template_json_inner)
    template_obj = patch_template(template_obj)
    new_template_json = json.dumps(template_obj, ensure_ascii=False)
    # Break </script sequences so the host HTML <script type="__bundler/template"> stays intact.
    new_template_json = re.sub(
        r"(?i)</script>",
        r"\\u003c\\u002Fscript\\u003e",
        new_template_json,
    )

    manifest_m = re.search(
        r'(<script type="__bundler/manifest">)\s*([\s\S]*?)\s*(</script>)',
        html,
    )
    if not manifest_m:
        raise SystemExit("no manifest")
    manifest = json.loads(manifest_m.group(2))
    if BABEL_UUID not in manifest:
        raise SystemExit("missing babel uuid in manifest")

    raw = base64.b64decode(manifest[BABEL_UUID]["data"])
    if manifest[BABEL_UUID].get("compressed"):
        babel_src = gzip.decompress(raw).decode("utf-8")
    else:
        babel_src = raw.decode("utf-8")

    babel_src = patch_babel_source(babel_src)
    gz = gzip.compress(babel_src.encode("utf-8"), compresslevel=9)
    manifest[BABEL_UUID]["data"] = base64.b64encode(gz).decode("ascii")
    manifest[BABEL_UUID]["compressed"] = True

    if TERMINAL_HERO_UUID in manifest:
        th = manifest[TERMINAL_HERO_UUID]
        raw_th = base64.b64decode(th["data"])
        if th.get("compressed"):
            hero_src = gzip.decompress(raw_th).decode("utf-8")
        else:
            hero_src = raw_th.decode("utf-8")
        new_hero = patch_terminal_hero_chunk(hero_src)
        if new_hero != hero_src:
            gz_h = gzip.compress(new_hero.encode("utf-8"), compresslevel=9)
            th["data"] = base64.b64encode(gz_h).decode("ascii")
            th["compressed"] = True

    new_manifest_json = json.dumps(manifest, separators=(",", ":"))

    html = (
        html[: tmpl_m.start(2)]
        + new_template_json
        + html[tmpl_m.end(2) :]
    )
    # re-find manifest after template replace (positions shifted)
    manifest_m2 = re.search(
        r'(<script type="__bundler/manifest">)\s*([\s\S]*?)\s*(</script>)',
        html,
    )
    html = (
        html[: manifest_m2.start(2)]
        + new_manifest_json
        + html[manifest_m2.end(2) :]
    )

    vp_spec = importlib.util.spec_from_file_location(
        "_ids_landing_value_props",
        Path(__file__).resolve().parent / "patch_landing_value_props.py",
    )
    assert vp_spec and vp_spec.loader
    vp_mod = importlib.util.module_from_spec(vp_spec)
    vp_spec.loader.exec_module(vp_mod)
    html = vp_mod.apply_landing_value_props_patch(html)

    INDEX.write_text(html, encoding="utf-8")
    print("Wrote", INDEX)


if __name__ == "__main__":
    main()
