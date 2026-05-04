#!/usr/bin/env python3
"""Emit components index + one HTML page per Ionic DS component (static, build-time canonical)."""

from __future__ import annotations

import html as htm
import json
import sys
from collections.abc import Callable
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPONENTS_OUT = ROOT / "components"

ORDER = [
    "Alert", "Avatar", "Badge", "Button", "Checkbox", "Container", "Divider", "Icon", "Image", "Input",
    "Label", "Link", "MenuItem", "Modal", "Progress", "Radio", "Select", "Skeleton", "Slider", "Spinner",
    "Switch", "Tab", "Table", "Text", "Textarea", "Toast", "ToggleButton", "Tooltip",
]


def slug(name: str) -> str:
    return name.lower()


def load_canonical_bundle() -> dict | None:
    for path in (ROOT / "data" / "ids-canonical.json", ROOT / "ids-canonical.json"):
        if path.exists():
            return json.loads(path.read_text())
    sys.stderr.write(
        "Note: No ids-canonical.json in data/ or project root.\n"
        "  Run: npm run ids:sync\n"
        "  (or copy the file to data/ids-canonical.json). Using static fallback.\n"
    )
    return None


def load_doc_links() -> dict | None:
    """Written by npm run ids:sync → data/doc-links.json (canonical + stylesheet provenance)."""
    path = ROOT / "data" / "doc-links.json"
    try:
        if path.exists():
            raw = json.loads(path.read_text(encoding="utf-8"))
            return raw if isinstance(raw, dict) else None
    except (OSError, json.JSONDecodeError):
        pass
    return None


def derive_page_order(reg: list[dict]) -> list[str]:
    handled = set(ORDER)
    canon_names = [c["name"] for c in reg]
    picked: list[str] = []
    seen: set[str] = set()
    for name in canon_names:
        if name in handled and name not in seen:
            picked.append(name)
            seen.add(name)
    for name in ORDER:
        if name in handled and name not in seen:
            picked.append(name)
            seen.add(name)
    return picked


def registry_by_name(bundle: dict | None) -> dict[str, dict]:
    if not bundle:
        return {}
    reg = bundle.get("componentRegistry", {}).get("components", [])
    if not isinstance(reg, list):
        return {}
    return {c["name"]: c for c in reg if isinstance(c, dict) and c.get("name")}


def canonical_props_li(entry: dict | None) -> list[str] | None:
    if not entry:
        return None
    props = entry.get("props")
    if not isinstance(props, dict):
        return None
    skip = {"children", "dimensionValues"}
    keys = sorted(k for k in props if k not in skip)
    if not keys:
        return None
    line = " · ".join(f"<code>{htm.escape(k)}</code>" for k in keys)
    return [line + ' <span style="opacity:.65">· from ids-canonical</span>']


def merged_description(
    component_name: str,
    desc_map: dict[str, str],
    registry_entry: dict | None,
    static_fallback: str,
) -> str:
    raw = ""
    if registry_entry and isinstance(registry_entry.get("description"), str):
        raw = registry_entry["description"].strip()
    if raw:
        return raw
    return (desc_map.get(component_name) or static_fallback).strip()


def merged_props(registry_entry: dict | None, static_li: list[str]) -> list[str]:
    canon = canonical_props_li(registry_entry)
    return canon if canon is not None else static_li


def code_panel(code: str, indent: str = "    ") -> str:
    esc = htm.escape(code.strip("\n"))
    return f"""{indent}<div class="code-panel">
{indent}  <button type="button" class="copy-btn" data-copy-btn>Copy</button>
{indent}  <pre class="code-pre"><code>{esc}</code></pre>
{indent}</div>"""


def props_box(items: list[str], indent: str = "    ") -> str:
    lis = "".join(f"<li>{x}</li>" for x in items)
    return f"""{indent}<div class="props-box">
{indent}  <strong style="color:var(--lp-fg)">Props / variants</strong>
{indent}  <ul>{lis}</ul>
{indent}</div>"""


def render_header_title(*, asset_prefix: str, page_title_full: str, extra_head: str = "") -> str:
    head_extra = ("\n  " + extra_head.strip()) if extra_head.strip() else ""
    return f"""<!DOCTYPE html>
<html lang="en" data-motion="on">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">{head_extra}
  <script src="{asset_prefix}theme-toggle.js"></script>
  <title>{htm.escape(page_title_full)}</title>
  <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/inter@5.2.5/index.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/inter@5.2.5/500.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/inter@5.2.5/600.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/inter@5.2.5/700.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/geist-sans@5.2.5/index.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/geist-sans@5.2.5/600.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/geist-mono@5.2.5/index.css">
  <link rel="stylesheet" href="{asset_prefix}docs-shell.css">
  <link rel="stylesheet" href="{asset_prefix}components-layout.css">
  <link rel="stylesheet" href="{asset_prefix}styles/default.css">
</head>
<body class="docs-preview">
"""


def render_sync_source_badge(doc_links: dict | None) -> str:
    """Prominent badge: GitHub vs local IDS checkout vs fallback (from ids:sync metadata)."""
    cu_link = ""
    if doc_links:
        cu_val = doc_links.get("canonicalUrl")
        if isinstance(cu_val, str) and cu_val.strip():
            esc_u = htm.escape(cu_val.strip(), quote=True)
            link_label = (
                "GitHub"
                if "github.com/" in cu_val and "/blob/" in cu_val
                else "Open link"
            )
            cu_link = (
                f' <a href="{esc_u}" class="comp-sync-url-link" target="_blank" '
                f'rel="noopener">{htm.escape(link_label)}</a>'
            )
    if not doc_links:
        badge = "Source: unknown"
        path_line = "Run npm run ids:sync · data/doc-links.json missing"
        state = "comp-sync-unknown"
    else:
        cp = doc_links.get("canonicalPath")
        spath = doc_links.get("stylesheetPath")
        cs = cp if isinstance(cp, str) else ""
        ss = spath if isinstance(spath, str) else ""
        ids_repo_touch = cs.startswith(
            "LOCAL_REPO:",
        ) or ss.startswith("LOCAL_REPO:")
        if ids_repo_touch:
            badge = "Source: Local IDS repo"
            state = "comp-sync-repo"
        elif cs.startswith("LOCAL_"):
            badge = "Source: Local fallback"
            state = "comp-sync-local"
        elif cs in ("MISSING", ""):
            badge = "Source: unknown"
            state = "comp-sync-unknown"
        else:
            badge = "Source: GitHub"
            state = "comp-sync-github"
        path_line = cs if cs else "—"
    esc_badge = htm.escape(badge)
    esc_path = htm.escape(path_line)
    return f"""      <div class="comp-sync-badge-row mono" aria-label="IDS canonical sync provenance">
        <span class="comp-sync-badge {state}">{esc_badge}</span>
        <span class="comp-sync-path-label doc-muted">Canonical path:</span>
        <span class="comp-sync-path-value doc-muted">{esc_path}</span>{cu_link}
      </div>
"""


def render_sidebar_links(
    page_order: list[str],
    *,
    link_prefix: str,
    active_file: str | None,
    count_line: str,
) -> str:
    lines: list[str] = []
    for nm in page_order:
        fname = slug(nm) + ".html"
        path = link_prefix + fname
        classes = ["side-rail-link"]
        extra = ""
        if active_file and fname == active_file:
            classes.append("is-active")
            extra = ' aria-current="page"'
        cls = " ".join(classes)
        lines.append(f'      <a class="{cls}" href="{path}"{extra}>{htm.escape(nm)}</a>')
    links = "\n".join(lines)
    return f"""    <aside class="side-rail" aria-label="Component index">
      <p class="side-rail-title">Components</p>
      <p class="side-rail-count mono doc-muted" aria-live="polite">{htm.escape(count_line)}</p>
      <nav class="side-rail-nav">
{links}
      </nav>
    </aside>
"""


def render_meta(metadata_ga: str, gc_short: str) -> str:
    ga = metadata_ga.strip() if metadata_ga else "—"
    cm = gc_short.strip() if gc_short else "—"
    return f"""      <div id="comp-meta-host" class="comp-source-meta mono doc-muted" aria-live="polite">
        <span>Source:
          <a href="https://github.com/poyi-is/ids">poyi-is/ids</a></span>
        <span id="comp-meta-generated">Generated: {htm.escape(ga)}</span>
        <span id="comp-meta-commit" title="">Commit: {htm.escape(cm)}</span>
      </div>
"""


def footer(script_prefix: str) -> str:
    return f"""  <p class="comp-foot">Registry: synced <code>data/ids-canonical.json</code> · <code>poyi-is/ids</code>. Stylesheet: <code>styles/default.css</code>.</p>
  <script src="{script_prefix}docs-shell-nav.js" defer></script>
  <script src="{script_prefix}components-page.js" defer></script>
</body>
</html>
"""


IMPORT_NOTE_SINGLE = '''    <div class="global-import-note doc-panel" style="padding:22px;margin-bottom:28px;">
      <p class="doc-muted" style="margin-bottom:12px;font-size:13px">Typical imports for this preview:</p>
      <div class="code-panel">
        <button type="button" class="copy-btn" data-copy-btn>Copy</button>
        <pre class="code-pre"><code>import { %NAME% } from 'ionic-design-system';
import '%STYLEPATH%';</code></pre>
      </div>
    </div>
'''

# Inline Lucide-compatible SVG paths for static HTML (IDS Icon maps name → glyphs at runtime).
CHEVRON_RIGHT_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" '
    'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="m9 18 6-6-6-6"/></svg>'
)
PLUS_ICON_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" '
    'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M12 5v14"/><path d="M5 12h14"/></svg>'
)
ATOM_ICON_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" '
    'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="12" cy="12" r="1"/>'
    '<path d="M20.2 20.2c2.04-2.03.02-7.36-4.5-11.9-4.54-4.52-9.87-6.54-11.9'
    '-4.5-2.03 2.04-.02 7.36 4.5 11.9 4.54 4.52 9.87 6.54 11.9 4.5Z"/>'
    '<path d="M3.8 3.8c-2.03 2.04-.02 7.36 4.5 11.9 4.54 4.52 9.87 6.54 11.9 '
    '4.5 2.03-2.04.02-7.36-4.5-11.9C11.16 3.28 5.83 1.26 3.8 3.8Z"/>'
    "</svg>"
)


def icon_markup(*, svg: str, size: str, color: str) -> str:
    return (
        f'<span class="ionic-icon" data-size="{htm.escape(size)}" '
        f'data-color="{htm.escape(color)}" aria-hidden="true">{svg}</span>'
    )


# —— Fragment builders return core preview + panels (no wrapping section / no h2) ——


def fb_alert(desc: dict[str, str], meta: dict | None) -> str:
    txt = merged_description("Alert", desc, meta, "Inline notification.")
    pb = merged_props(meta, ["<code>intent</code> · <code>appearance</code> · <code>shape</code> · <code>title</code> / <code>description</code>"])
    return f'''    <p class="comp-desc">{htm.escape(txt)}</p>
    <div class="preview-panel"><div class="preview-stack">
      <div class="ionic-alert" data-shape="rounded" data-appearance="outline" data-intent="info" role="status">
        Sandbox mode — drafts are local only.</div>
      <div class="ionic-alert" data-shape="rounded" data-appearance="solid" data-intent="success" role="status">
        Saved — workspace synced.</div>
      <div class="ionic-alert" data-shape="rounded" data-appearance="outline" data-intent="warning" role="status">
        Approaching quota for this billing period.</div>
      <div class="ionic-alert" data-shape="rounded" data-appearance="solid" data-intent="danger" role="alert">
        Publish failed — try again shortly.</div>
      <div class="ionic-alert" data-shape="rounded" data-appearance="outline" data-intent="neutral" role="status">
        Heads up — this action cannot be undone.</div>
    </div></div>
{code_panel("""import { Alert } from 'ionic-design-system';

<Alert title="Info" intent="info" appearance="outline" />
<Alert title="Saved" intent="success" appearance="outline" />
<Alert title="Warning" intent="warning" appearance="outline" />
<Alert title="Error" intent="danger" appearance="solid" />""")}
{props_box(pb)}'''


def fb_avatar(desc: dict[str, str], meta: dict | None) -> str:
    pb = merged_props(meta, ["<code>initials</code> / <code>src</code> · <code>size</code> · <code>shape</code> · <code>color</code>"])
    return f'''    <p class="comp-desc">{htm.escape(merged_description("Avatar", desc, meta, ""))}</p>
    <div class="preview-panel"><div class="preview-row">
      <div class="ionic-avatar" data-shape="circle" data-size="md" data-color="primary">AC</div>
      <div class="ionic-avatar" data-shape="rounded" data-size="lg" data-color="neutral">BZ</div>
    </div></div>
{code_panel("""import { Avatar } from 'ionic-design-system';

<Avatar initials="AC" size="md" shape="circle" color="primary" />""")}
{props_box(pb)}'''


def fb_badge(desc: dict[str, str], meta: dict | None) -> str:
    pb = merged_props(meta, ["<code>intent</code> · <code>appearance</code> (solid · soft · outline) · <code>size</code> · <code>shape</code>"])
    return f'''    <p class="comp-desc">{htm.escape(merged_description("Badge", desc, meta, ""))}</p>
    <div class="preview-panel"><div class="preview-inner">
      <span class="ionic-badge" data-appearance="solid" data-intent="primary" data-size="sm" data-shape="pill">Solid</span>
      <span class="ionic-badge" data-appearance="solid" data-intent="info" data-size="sm" data-shape="pill">Info</span>
      <span class="ionic-badge" data-appearance="soft" data-intent="success" data-size="sm" data-shape="pill">Soft</span>
      <span class="ionic-badge" data-appearance="outline" data-intent="warning" data-size="sm" data-shape="pill">Outline</span>
      <span class="ionic-badge" data-appearance="soft" data-intent="danger" data-size="sm" data-shape="rounded">Danger</span>
      <span class="ionic-badge" data-appearance="outline" data-intent="primary" data-size="sm" data-shape="rounded">Outline primary</span>
    </div></div>
{code_panel("""import { Badge } from 'ionic-design-system';

<Badge label="Stable" intent="primary" appearance="solid" shape="pill" size="sm" />
<Badge label="Beta" intent="success" appearance="soft" shape="pill" size="sm" />""")}
{props_box(pb)}'''


def fb_button(desc: dict[str, str], meta: dict | None) -> str:
    ich_l = icon_markup(svg=CHEVRON_RIGHT_SVG, size="sm", color="inherit")
    ich_plus = icon_markup(svg=PLUS_ICON_SVG, size="sm", color="inherit")
    icon_only = ich_plus
    pb = merged_props(meta, [
        'Static previews map React <code>intent</code> → <code>data-color</code> (IDS axis names). ',
        '<code>appearance</code> · <code>size</code> · <code>shape</code> · <code>icon</code> · ',
        '<code>iconPosition</code> · <code>iconOnly</code>.',
    ])
    txt = merged_description("Button", desc, meta, "")
    example_py = '''import { Button } from 'ionic-design-system';

<Button intent="primary" appearance="solid" size="md" shape="rounded" label="Primary solid" />

<Button intent="secondary" appearance="solid" size="md" shape="pill" label="Neutral" />

<Button intent="primary" appearance="outline" size="md" shape="rounded" label="Outline" />

<Button intent="primary" appearance="ghost" size="md" shape="rounded" label="Ghost" />

<Button intent="success" appearance="solid" size="sm" shape="rounded" label="Success" />

<Button intent="primary" appearance="solid" size="lg" shape="pill" icon="Plus" iconPosition="left" label="New" />

<Button intent="secondary" appearance="solid" size="md" shape="rounded" icon="ChevronRight" iconPosition="left"
  label="Continue" />

<Button intent="secondary" appearance="solid" size="md" shape="rounded" icon="ChevronRight" iconPosition="right"
  label="Continue" />

<Button intent="primary" appearance="solid" size="md" shape="rounded" icon="Plus" iconOnly aria-label="Add" />'''
    return (
        f"""    <p class="comp-desc">{htm.escape(txt)}</p>
    <div class="preview-panel"><div class="preview-stack">
      <div><div class="preview-label">Solid primary · neutral · outline · ghost</div><div class="preview-row">
        <button type="button" class="ionic-button" data-color="primary" data-size="md" data-shape="rounded">
          Solid primary</button>
        <button type="button" class="ionic-button" data-color="secondary" data-size="md" data-shape="rounded">
          Neutral</button>
        <button type="button" class="ionic-button" data-appearance="outline" data-color="primary" data-size="md"
          data-shape="rounded">Outline</button>
        <button type="button" class="ionic-button" data-appearance="ghost" data-color="primary" data-size="md"
          data-shape="rounded">Ghost</button>
      </div></div>
      <div><div class="preview-label">Sizes · pill shape</div><div class="preview-row">
        <button type="button" class="ionic-button" data-color="primary" data-size="sm" data-shape="pill">
          Small</button>
        <button type="button" class="ionic-button" data-color="primary" data-size="md" data-shape="pill">
          Medium</button>
        <button type="button" class="ionic-button" data-color="primary" data-size="lg" data-shape="pill">
          Large</button>
      </div></div>
      <div><div class="preview-label">Intent (solid)</div><div class="preview-row">
        <button type="button" class="ionic-button" data-color="primary" data-size="md" data-shape="rounded">
          Primary</button>
        <button type="button" class="ionic-button" data-color="success" data-size="md" data-shape="rounded">
          Success</button>
        <button type="button" class="ionic-button" data-color="warning" data-size="md" data-shape="rounded">
          Warning</button>
        <button type="button" class="ionic-button" data-color="danger" data-size="md" data-shape="rounded">
          Danger</button>
        <button type="button" class="ionic-button" data-color="info" data-size="md" data-shape="rounded">
          Info</button>
      </div></div>
      <div><div class="preview-label">Icon · iconPosition · iconOnly</div><div class="preview-row">
        <button type="button" class="ionic-button" data-color="primary" data-size="md" data-shape="rounded">
          {ich_plus}<span>New run</span></button>
        <button type="button" class="ionic-button" data-color="secondary" data-size="md" data-shape="rounded">
          {ich_l}<span>Continue</span></button>
        <button type="button" class="ionic-button" data-color="secondary" data-size="md" data-shape="rounded">
          <span>Continue</span>{ich_l}</button>
        <button type="button" class="ionic-button ionic-button-icon-only docs-btn-icon-only"
          data-color="primary" data-size="md" data-shape="rounded" aria-label="Add">{icon_only}</button>
      </div></div>
    </div></div>
"""
        + code_panel(example_py)
        + props_box(pb)
    )


def fb_checkbox(desc: dict[str, str], meta: dict | None) -> str:
    cb_code = '<Checkbox checked={v} onChange={setV} size="md" />'
    pb = merged_props(meta, ["<code>checked</code> · <code>size</code> · <code>color</code> · <code>border</code>"])
    return f'''    <p class="comp-desc">{htm.escape(merged_description("Checkbox", desc, meta, ""))}</p>
    <div class="preview-panel"><div class="preview-stack">
      <label style="display:flex;align-items:center;gap:8px;color:var(--lp-fg)">
        <input type="checkbox" class="ionic-checkbox" data-color="default" data-size="md" data-border="rounded" /> Terms</label>
      <label style="display:flex;align-items:center;gap:8px;color:var(--lp-fg)">
        <input type="checkbox" checked class="ionic-checkbox" data-color="neutral" data-size="md" /> Updates</label>
    </div></div>
{code_panel(cb_code)}
{props_box(pb)}'''


def fb_container(desc: dict[str, str], meta: dict | None) -> str:
    c_code = '<Container display="flex" spacing="md" color="card">{children}</Container>'
    pb = merged_props(meta, ["<code>display</code> · <code>spacing</code> · <code>columns</code> · <code>padding</code> · <code>color</code>"])
    return f'''    <p class="comp-desc">{htm.escape(merged_description("Container", desc, meta, ""))}</p>
    <div class="preview-panel"><div class="preview-inner">
      <div class="ionic-container" data-display="flex" data-direction="row" data-spacing="md" data-alignment="center" data-padding="md"
        data-color="card" data-shape="rounded" style="min-height:72px;width:min(100%,440px);border-style:solid;border-width:1px">
        <span class="ionic-text" data-size="sm" data-color="default">Flexible row</span>
      </div>
    </div></div>
{code_panel(c_code)}
{props_box(pb)}'''


def fb_divider(desc: dict[str, str], meta: dict | None) -> str:
    pb = merged_props(meta, ["<code>orientation</code> · <code>size</code> · <code>color</code>"])
    return f'''    <p class="comp-desc">{htm.escape(merged_description("Divider", desc, meta, ""))}</p>
    <div class="preview-panel"><div class="preview-stack">
      <p class="ionic-text" data-size="sm" data-color="muted">A</p>
      <hr class="ionic-divider" data-orientation="horizontal" data-color="default" data-size="thin" />
      <p class="ionic-text" data-size="sm" data-color="muted">B</p>
    </div></div>
{code_panel('<Divider orientation="horizontal" color="default" />')}
{props_box(pb)}'''


def fb_icon(desc: dict[str, str], meta: dict | None) -> str:
    pb = merged_props(meta, ["<code>name</code> · <code>size</code> · <code>color</code>"])
    atom = icon_markup(svg=ATOM_ICON_SVG, size="lg", color="primary")
    cog = icon_markup(svg=CHEVRON_RIGHT_SVG, size="md", color="muted")
    return f'''    <p class="comp-desc">{htm.escape(merged_description("Icon", desc, meta, ""))}</p>
    <div class="preview-panel"><div class="preview-inner">
      {atom}<span class="ionic-text" data-size="sm" data-color="muted">&nbsp;&nbsp;<code>&lt;Icon name=&quot;Atom&quot; /&gt;</code></span>
      <span style="opacity:.55" aria-hidden="true">&nbsp;—&nbsp;</span>
      {cog}<span class="ionic-text" data-size="xs" data-color="muted">&nbsp;(reference glyph)</span>
    </div></div>
{code_panel('<Icon name="Atom" size="lg" color="primary" />')}
{props_box(pb)}'''


def fb_image(desc: dict[str, str], meta: dict | None) -> str:
    src = (
        "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='640' height='360' "
        "%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0' x2='1' y1='0' y2='1'%3E"
        "%3Cstop stop-color='%233B82F6'/%3E%3Cstop offset='1' stop-color='%23B4FF3A'/%3E%3C/linearGradient%3E"
        "%3C/defs%3E%3Crect rx='14' fill='url(%23g)' width='640' height='360'/%3E%3C/svg%3E"
    )
    pb = merged_props(meta, ["<code>src</code> · <code>alt</code> · <code>fit</code> · <code>aspectRatio</code>"])
    return f'''    <p class="comp-desc">{htm.escape(merged_description("Image", desc, meta, ""))}</p>
    <div class="preview-panel"><div class="preview-inner">
      <img class="ionic-image" data-fit="cover" data-aspectRatio="16/9" alt="" src="{src}"
        style="max-width:min(100%,400px)" />
    </div></div>
{code_panel('<Image src="/hero.jpg" alt="Hero" fit="cover" aspectRatio="16/9" />')}
{props_box(pb)}'''


def fb_input(desc: dict[str, str], meta: dict | None) -> str:
    pb = merged_props(meta, ["<code>placeholder</code> · <code>size</code> · <code>shape</code> · <code>color</code>"])
    return f'''    <p class="comp-desc">{htm.escape(merged_description("Input", desc, meta, ""))}</p>
    <div class="preview-panel"><div class="preview-stack">
      <div>
        <span class="ionic-text preview-label-like" data-size="xs" data-weight="medium" data-color="default"
          style="display:block;margin-bottom:6px;text-transform:none;letter-spacing:0;font-family:inherit">Organization</span>
        <input class="ionic-input" type="text" placeholder="Acme"
          data-color="default" data-size="default" data-shape="rounded" data-elevation="none" />
      </div>
      <div>
        <span class="ionic-text preview-label-like" data-size="xs" data-weight="medium" data-color="default"
          style="display:block;margin-bottom:6px;text-transform:none;letter-spacing:0;font-family:inherit">Email</span>
        <input class="ionic-input" type="email" placeholder="you@ionic.dev"
          data-color="default" data-size="default" data-shape="rounded" data-elevation="none" />
      </div>
      <span class="preview-label">Search · small pill</span>
      <input class="ionic-input" type="search" placeholder="Find workspace…"
        data-color="default" data-size="sm" data-shape="pill" data-elevation="none" />
    </div></div>
{code_panel('<Input type="email" placeholder="you@ionic.dev" size="default" />')}
{props_box(pb)}'''


def fb_label(desc: dict[str, str], meta: dict | None) -> str:
    pb = merged_props(meta, ["<code>text</code> · <code>htmlFor</code> · <code>required</code>"])
    txt = merged_description("Label", desc, meta, "Form caption helper.")
    return f'''    <p class="comp-desc">{htm.escape(txt)}</p>
    <div class="preview-panel"><div class="preview-stack">
      <label class="ionic-text" data-size="sm" data-weight="medium" data-color="default" for="lbl-demo-api">API key</label>
      <input id="lbl-demo-api" class="ionic-input" type="text" placeholder="live_..."
        data-color="default" data-size="sm" data-shape="rounded" />
    </div></div>
{code_panel('<Label text="API key" htmlFor="key" required />')}
{props_box(pb)}'''


def fb_link(desc: dict[str, str], meta: dict | None) -> str:
    pb = merged_props(meta, ["<code>href</code> · <code>text</code> · <code>color</code> · <code>appearance</code> · <code>weight</code>"])
    return f'''    <p class="comp-desc">{htm.escape(merged_description("Link", desc, meta, ""))}</p>
    <div class="preview-panel"><div class="preview-row">
      <a class="ionic-link" href="#" onclick="return false" data-size="default"
        data-color="default" data-appearance="default" data-weight="medium">Documentation</a>
      <a class="ionic-link" href="#" onclick="return false" data-size="default"
        data-color="muted" data-appearance="subtle" data-weight="normal">Subtle muted</a>
    </div></div>
{code_panel('<Link href="../docs.html" text="Documentation" />')}
{props_box(pb)}'''


def fb_menuitem(desc: dict[str, str], meta: dict | None) -> str:
    menu_code = """<MenuItem label="Copy" shortcut="⌘C" />
<MenuItem label="Delete" color="danger" />"""
    pb = merged_props(meta, ["<code>label</code> · <code>shortcut</code> · <code>color</code> · <code>disabled</code>"])
    return f'''    <p class="comp-desc">{htm.escape(merged_description("MenuItem", desc, meta, ""))}</p>
    <div class="preview-panel"><div class="preview-stack" style="max-width:300px;margin:0 auto">
      <div class="ionic-menuitem" data-size="md" data-color="default" tabindex="0" role="menuitem">
        Copy <span style="opacity:.55;margin-left:auto">⌘C</span></div>
      <div class="ionic-menuitem" data-size="md" data-color="danger" tabindex="0" role="menuitem">Delete</div>
    </div></div>
{code_panel(menu_code)}
{props_box(pb)}'''


def fb_modal(_desc: dict[str, str], meta: dict | None) -> str:
    pb = merged_props(meta, ["<code>size</code> · <code>shape</code> · children content"])
    txt = "Dialog panel — stacking & focus trapping ship with React wrapper."
    if meta:
        txt = merged_description("Modal", _desc, meta, txt)
    return f'''    <p class="comp-desc">{htm.escape(txt)}</p>
    <div class="preview-panel"><div class="preview-inner">
      <div class="ionic-modal" data-size="sm" data-shape="rounded" data-color="default" role="dialog"
        aria-modal="true" style="max-width:100%;border-style:solid;border-width:1px;display:block">
        <p class="ionic-text" data-size="lg" data-weight="semibold" style="margin-bottom:6px">Title</p>
        <p class="ionic-text" data-size="sm" data-color="muted">Supporting copy.</p>
        <div style="margin-top:14px;display:flex;gap:8px">
          <button type="button" class="ionic-button" data-color="secondary" data-size="sm">Cancel</button>
          <button type="button" class="ionic-button" data-color="primary" data-size="sm">Save</button>
        </div>
      </div>
    </div></div>
{code_panel("<Modal>...</Modal> /* see compositions in package */")}
{props_box(pb)}'''


def fb_progress(desc: dict[str, str], meta: dict | None) -> str:
    pb = merged_props(meta, ["<code>value</code> · <code>max</code> · <code>indeterminate</code> · <code>color</code>"])
    return f'''    <p class="comp-desc">{htm.escape(merged_description("Progress", desc, meta, ""))}</p>
    <div class="preview-panel"><div class="preview-stack">
      <div class="ionic-progress" data-size="md" data-color="primary" role="progressbar" style="--ids-progress-pct:62%"
        aria-valuenow="62" aria-valuemin="0" aria-valuemax="100">
        <span class="ionic-progress-fill" aria-hidden="true"></span>
      </div>
      <div class="ionic-progress" data-size="sm" data-color="success" role="progressbar" style="--ids-progress-pct:88%"
        aria-valuenow="88" aria-valuemin="0" aria-valuemax="100">
        <span class="ionic-progress-fill" aria-hidden="true"></span>
      </div>
    </div></div>
{code_panel('<Progress value={62} max={100} color="primary" />')}
{props_box(pb)}'''


def fb_radio(desc: dict[str, str], meta: dict | None) -> str:
    pb = merged_props(meta, ["<code>name</code> · <code>checked</code> · <code>color</code>"])
    return f'''    <p class="comp-desc">{htm.escape(merged_description("Radio", desc, meta, ""))}</p>
    <div class="preview-panel"><div class="preview-row">
      <label style="display:flex;align-items:center;gap:6px;color:var(--lp-fg);font-size:13px">
        <input type="radio" name="idr" checked class="ionic-radio" data-color="primary" /> A</label>
      <label style="display:flex;align-items:center;gap:6px;color:var(--lp-fg);font-size:13px">
        <input type="radio" name="idr" class="ionic-radio" data-color="neutral" /> B</label>
    </div></div>
{code_panel('<Radio name="grp" value="a" checked onChange />')}
{props_box(pb)}'''


def fb_select(desc: dict[str, str], meta: dict | None) -> str:
    pb = merged_props(meta, ["<code>options</code> · <code>appearance</code> · <code>color</code> · <code>size</code>"])
    return f'''    <p class="comp-desc">{htm.escape(merged_description("Select", desc, meta, ""))}</p>
    <div class="preview-panel"><div class="preview-stack">
      <div>
        <span class="ionic-text" data-size="xs" data-weight="medium" data-color="muted"
          style="display:block;margin-bottom:6px">Team</span>
        <select class="ionic-select" data-appearance="outline" data-color="default" data-size="md"
          data-shape="rounded">
          <option>Mobile platform</option><option>Brand design</option><option>Infrastructure</option>
        </select>
      </div>
      <div>
        <span class="ionic-text" data-size="xs" data-weight="medium" data-color="muted"
          style="display:block;margin-bottom:6px">Region</span>
        <select class="ionic-select" data-appearance="outline" data-color="default" data-size="sm"
          data-shape="rounded">
          <option>EU Central</option><option>US East</option><option>AP Northeast</option>
        </select>
      </div>
    </div></div>
{code_panel('<Select label="Team" options={["Mobile","Design"]} />')}
{props_box(pb)}'''


def fb_skeleton(desc: dict[str, str], meta: dict | None) -> str:
    pb = merged_props(meta, ["<code>shape</code> vs <code>variant</code> · <code>animation</code> · <code>width</code> · <code>height</code>"])
    return f'''    <p class="comp-desc">{htm.escape(merged_description("Skeleton", desc, meta, ""))}</p>
    <div class="preview-panel"><div class="preview-stack">
      <div class="ionic-skeleton" data-variant="rectangle" data-size="md" data-animation="pulse" data-color="medium"
        style="width:240px;display:block">&nbsp;</div>
      <div class="ionic-skeleton" data-variant="circle" data-animation="pulse" data-color="dark"
        style="width:56px;height:56px;display:block;margin:0 auto">&nbsp;</div>
    </div></div>
{code_panel('<Skeleton shape="rectangle" animation="pulse" width="240px" height="22px" />')}
{props_box(pb)}'''


def fb_slider(desc: dict[str, str], meta: dict | None) -> str:
    pb = merged_props(meta, ["<code>value</code> · <code>color</code> · <code>orientation</code>"])
    return f'''    <p class="comp-desc">{htm.escape(merged_description("Slider", desc, meta, ""))}</p>
    <div class="preview-panel"><div class="preview-row">
      <div class="ionic-slider" data-orientation="horizontal" data-size="md" data-color="primary">
        <input type="range" min="0" max="100" value="54" aria-label="Level" /></div>
    </div></div>
{code_panel('<Slider value={gain} color="primary" onChange />')}
{props_box(pb)}'''


def fb_spinner(desc: dict[str, str], meta: dict | None) -> str:
    pb = merged_props(meta, ["<code>variant</code> · <code>color</code> · <code>size</code>"])
    return f'''    <p class="comp-desc">{htm.escape(merged_description("Spinner", desc, meta, ""))}</p>
    <div class="preview-panel docs-preview"><div class="preview-row">
      <span class="ionic-spinner" data-size="md" data-color="primary" aria-label="Loading" role="status"></span>
      <span class="ionic-spinner" data-size="sm" data-color="success" aria-hidden="true"></span>
    </div></div>
{code_panel('<Spinner size="md" color="primary" />')}
{props_box(pb)}'''


def fb_switch(desc: dict[str, str], meta: dict | None) -> str:
    pb = merged_props(meta, ["<code>checked</code> · <code>color</code> · <code>disabled</code>"])
    return f'''    <p class="comp-desc">{htm.escape(merged_description("Switch", desc, meta, ""))}</p>
    <div class="preview-panel"><div class="preview-row">
      <label style="display:flex;align-items:center;gap:8px;color:var(--lp-fg);font-size:13px">
        Off<input role="switch" type="checkbox" class="ionic-switch" data-color="primary" aria-checked="false" /></label>
      <label style="display:flex;align-items:center;gap:8px;color:var(--lp-fg);font-size:13px">
        On<input role="switch" type="checkbox" checked class="ionic-switch" data-color="primary" aria-checked="true" /></label>
    </div></div>
{code_panel('<Switch checked={on} color="primary" onChange />')}
{props_box(pb)}'''


def fb_tab(desc: dict[str, str], meta: dict | None) -> str:
    pb = merged_props(meta, ["<code>appearance</code> · <code>aria-selected</code> · <code>color</code>"])
    return f'''    <p class="comp-desc">{htm.escape(merged_description("Tab", desc, meta, ""))}</p>
    <div class="preview-panel"><div class="preview-row">
      <button type="button" class="ionic-tab" data-appearance="pills" data-size="sm" aria-selected="true">Overview</button>
      <button type="button" class="ionic-tab" data-appearance="pills" data-size="sm" aria-selected="false">Spec</button>
      <button type="button" class="ionic-tab" data-appearance="line" data-color="primary" data-size="sm"
        aria-selected="false">API</button>
    </div></div>
{code_panel('<Tab label="Overview" selected appearance="pills" />')}
{props_box(pb)}'''


def fb_table(desc: dict[str, str], meta: dict | None) -> str:
    pb = merged_props(
        meta,
        [
            'Use <code>TableHeader</code> · <code>TableBody</code> · etc. Exported CSS targets utility tokens, not a single <code>.ionic-table</code> skin.'
        ],
    )
    fallback = merged_description(
        "Table",
        desc,
        meta,
        "Composable table primitives (semantic HTML — no standalone table skin in exported CSS sheet).",
    )
    return f'''    <p class="comp-desc">{htm.escape(fallback)}</p>
    <div class="preview-panel"><div class="preview-inner" style="overflow:auto">
      <table style="width:100%;border-collapse:collapse;font-size:13px;color:var(--lp-fg)">
        <thead><tr style="border-bottom:1px solid var(--lp-border);text-align:left">
          <th style="padding:8px">Name</th><th style="padding:8px">Role</th></tr></thead>
        <tbody>
          <tr style="border-bottom:1px solid var(--lp-border)"><td style="padding:8px">Alex</td><td style="padding:8px">Staff</td></tr>
          <tr><td style="padding:8px">Jordan</td><td style="padding:8px">Contributor</td></tr>
        </tbody>
      </table>
    </div></div>
{code_panel("<Table>...</Table>")}
{props_box(pb)}'''


def fb_text(desc: dict[str, str], meta: dict | None) -> str:
    pb = merged_props(meta, ["<code>tag</code> · <code>size</code> · <code>weight</code> · <code>color</code>"])
    return f'''    <p class="comp-desc">{htm.escape(merged_description("Text", desc, meta, ""))}</p>
    <div class="preview-panel"><div class="preview-stack">
      <span class="ionic-text" data-size="xl" data-weight="bold">Eyebrow</span>
      <span class="ionic-text" data-size="sm" data-color="muted">Supporting prose.</span>
    </div></div>
{code_panel('<Text text="Hello" tag="p" size="lg" weight="medium" />')}
{props_box(pb)}'''


def fb_textarea(desc: dict[str, str], meta: dict | None) -> str:
    pb = merged_props(meta, ["<code>rows</code> · <code>resize</code> · <code>size</code>"])
    return f'''    <p class="comp-desc">{htm.escape(merged_description("Textarea", desc, meta, ""))}</p>
    <div class="preview-panel"><div class="preview-stack">
      <textarea class="ionic-textarea" rows="4" placeholder="Compose release notes…" data-size="md"
        data-color="default" data-shape="rounded"></textarea>
    </div></div>
{code_panel('<Textarea placeholder="Compose…" rows={4} />')}
{props_box(pb)}'''


def fb_toast(desc: dict[str, str], meta: dict | None) -> str:
    pb = merged_props(meta, ["<code>variant</code> · <code>duration</code> · <code>position</code> → maps to IDS <code>data-type</code>"])
    return f'''    <p class="comp-desc">{htm.escape(merged_description("Toast", desc, meta, ""))}</p>
    <div class="preview-panel"><div class="preview-inner" style="flex-direction:column;align-items:stretch">
      <div class="ionic-toast" data-type="info" data-size="sm">
        <p class="ionic-text" data-size="sm" data-weight="semibold">Heads up</p>
        <p class="ionic-text" data-size="xs" data-color="muted">Read-only workspace.</p>
      </div>
      <div class="ionic-toast" data-type="success" data-size="sm">
        <p class="ionic-text" data-size="sm" data-weight="semibold">Synced</p>
        <p class="ionic-text" data-size="xs" data-color="muted">Your branch is up to date.</p>
      </div>
      <div class="ionic-toast" data-type="warning" data-size="sm">
        <p class="ionic-text" data-size="sm" data-weight="semibold">Rate limit</p>
        <p class="ionic-text" data-size="xs" data-color="muted">Slow down retries.</p>
      </div>
      <div class="ionic-toast" data-type="error" data-size="sm">
        <p class="ionic-text" data-size="sm" data-weight="semibold">Failed</p>
        <p class="ionic-text" data-size="xs" data-color="muted">Could not complete request.</p>
      </div>
    </div></div>
{code_panel('<Toast title="Synced" variant="success" position="bottom-right" />')}
{props_box(pb)}'''


def fb_togglebutton(desc: dict[str, str], meta: dict | None) -> str:
    pb = merged_props(meta, ["<code>pressed</code> · <code>appearance</code> · <code>size</code>"])
    return f'''    <p class="comp-desc">{htm.escape(merged_description("ToggleButton", desc, meta, ""))}</p>
    <div class="preview-panel"><div class="preview-row">
      <button type="button" class="ionic-togglebutton" data-appearance="outline" data-size="sm" aria-pressed="true">Pin</button>
      <button type="button" class="ionic-togglebutton" data-appearance="ghost" data-size="sm" aria-pressed="false">Notes</button>
    </div></div>
{code_panel('<ToggleButton label="Pin" pressed onPressedChange />')}
{props_box(pb)}'''


def fb_tooltip(_desc: dict[str, str], meta: dict | None) -> str:
    pb = merged_props(meta, ["See <code>TooltipRoot</code> / <code>TooltipTrigger</code> / <code>TooltipContent</code> in package"])
    txt = "Primitive chip — TooltipRoot compositions handle portals & placement."
    if meta:
        txt = merged_description("Tooltip", _desc, meta, txt)
    return f'''    <p class="comp-desc">{htm.escape(txt)}</p>
    <div class="preview-panel"><div class="preview-row">
      <span class="ionic-tooltip" data-shape="rounded" data-size="md" data-color="dark">Dark chip</span>
      <span class="ionic-tooltip" data-shape="rounded" data-size="sm" data-color="primary">Primary chip</span>
    </div></div>
{code_panel("<TooltipRoot>...</TooltipRoot>")}
{props_box(pb)}'''


BUILDERS: dict[str, Callable[[dict[str, str], dict | None], str]] = {
    "Alert": fb_alert,
    "Avatar": fb_avatar,
    "Badge": fb_badge,
    "Button": fb_button,
    "Checkbox": fb_checkbox,
    "Container": fb_container,
    "Divider": fb_divider,
    "Icon": fb_icon,
    "Image": fb_image,
    "Input": fb_input,
    "Label": fb_label,
    "Link": fb_link,
    "MenuItem": fb_menuitem,
    "Modal": fb_modal,
    "Progress": fb_progress,
    "Radio": fb_radio,
    "Select": fb_select,
    "Skeleton": fb_skeleton,
    "Slider": fb_slider,
    "Spinner": fb_spinner,
    "Switch": fb_switch,
    "Tab": fb_tab,
    "Table": fb_table,
    "Text": fb_text,
    "Textarea": fb_textarea,
    "Toast": fb_toast,
    "ToggleButton": fb_togglebutton,
    "Tooltip": fb_tooltip,
}


def render_topbar(
    *,
    nested: bool,
    components_nav_current: bool,
    hub_stub: bool = False,
    top_level_component_slug: str | None = None,
) -> str:
    """Components always links to Alert (canonical first doc). aria-current only on that exact page or the hub stub."""
    if nested:
        index_href = "../index.html"
        docs_href = "../docs.html"
        comps_href = "./alert.html"
        install_href = "../docs.html#install"
    else:
        index_href = "./index.html"
        docs_href = "./docs.html"
        comps_href = "./components/alert.html"
        install_href = "./docs.html#install"

    comps_aria = ""
    if components_nav_current:
        if hub_stub or (nested and top_level_component_slug == "alert"):
            comps_aria = ' aria-current="page"'
    return f"""  <header class="site-topbar">
    <a href="{index_href}" class="topbar-brand" aria-label="Ionic DS — Home">
      <div class="topbar-logo">I<span class="topbar-logo-dot pulse" aria-hidden="true"></span></div>
      <span class="display topbar-lockup-title">Ionic DS</span>
      <span class="mono topbar-version">v1.4</span>
    </a>
    <nav class="topbar-nav" aria-label="Primary">
      <a class="topbar-link" href="{docs_href}">Docs</a>
      <a class="topbar-link" href="{comps_href}"{comps_aria}>Components</a>
      <a class="topbar-link" data-nav-doc="skill" href="#" hidden>SKILL.md</a>
      <a class="topbar-link" data-nav-doc="changelog" href="#" hidden>Changelog</a>
    </nav>
    <div class="topbar-actions">
      <a class="lp-btn lp-btn-sm" data-variant="ghost" href="https://github.com/poyi-is/ids">GitHub</a>
      <a class="lp-btn lp-btn-sm-accent" data-variant="accent" href="{install_href}">Install</a>
    </div>
  </header>
"""


def components_hub_stub_body() -> str:
    return '''  <script>
    window.location.replace('./components/alert.html');
  </script>
  <main class="docs-preview" style="padding:56px 40px;">
    <p class="doc-muted" style="margin-bottom:14px;font-size:15px;">Redirecting to Components...</p>
    <p style="margin:0"><a class="topbar-link" href="./components/alert.html" style="display:inline;color:var(--lp-accent);text-decoration:none">Open Alert component</a></p>
  </main>
'''


def patch_meta_commit_title(meta_html: str, full_sha: str) -> str:
    if not full_sha or len(full_sha) < 10:
        return meta_html
    esc = htm.escape(full_sha)
    return meta_html.replace('title=""', f'title="{esc}"', 1)


def main() -> None:
    bundle = load_canonical_bundle()
    if bundle:
        reg_list = bundle.get("componentRegistry", {}).get("components", [])
        desc = {c["name"]: (c.get("description") or "").strip() for c in reg_list}
        page_order = derive_page_order(reg_list)
        meta_ga = bundle.get("generatedAt") or ""
        meta_gc = bundle.get("gitCommit") or ""
    else:
        desc = {}
        page_order = list(ORDER)
        meta_ga = ""
        meta_gc = ""

    gc_short = meta_gc[:7] if len(meta_gc) >= 7 else meta_gc
    rb = registry_by_name(bundle)
    doc_links = load_doc_links()

    COMPONENTS_OUT.mkdir(parents=True, exist_ok=True)

    n_comp = len(page_order)
    count_line = f"{n_comp} components"

    meta_refresh = '<meta http-equiv="refresh" content="0; url=./components/alert.html">'
    stub_html = (
        render_header_title(
            asset_prefix="./",
            page_title_full="Ionic DS — Components",
            extra_head=meta_refresh,
        )
        + render_topbar(
            nested=False,
            components_nav_current=True,
            hub_stub=True,
        )
        + components_hub_stub_body()
        + footer("./")
    )

    (ROOT / "components.html").write_text(stub_html, encoding="utf-8")
    written = [ROOT / "components.html"]

    for nm in page_order:
        slug_f = slug(nm) + ".html"
        active = slug_f
        builder = BUILDERS.get(nm)
        if not builder:
            continue

        sidebar = render_sidebar_links(
            page_order,
            link_prefix="./",
            active_file=active,
            count_line=count_line,
        )

        body_inner = builder(desc, rb.get(nm))
        import_single = (
            IMPORT_NOTE_SINGLE.replace("%NAME%", nm).replace("%STYLEPATH%", "../styles/default.css")
        )

        page_html = (
            render_header_title(asset_prefix="../", page_title_full=f"Ionic DS — {nm}")
            + render_topbar(
                nested=True,
                components_nav_current=True,
                top_level_component_slug=slug(nm),
            )
            + "  <div class=\"comp-wrap\">\n"
            + sidebar
            + f'''    <div class="comp-main">
      <h1 class="comp-page-title display" id="comp-page-h1">{htm.escape(nm)}</h1>
'''
            + render_sync_source_badge(doc_links)
            + patch_meta_commit_title(render_meta(meta_ga, gc_short), meta_gc)
            + import_single
            + "      <section class=\"comp-section comp-single docs-preview\" aria-labelledby=\"comp-page-h1\">\n"
            + body_inner
            + "\n      </section>\n"
            + "    </div>\n  </div>\n"
            + footer("../")
        )

        outp = COMPONENTS_OUT / slug_f
        outp.write_text(page_html, encoding="utf-8")
        written.append(outp)

    print("Wrote:", len(written), "files")
    for w in written:
        print(" ", w.relative_to(ROOT))


if __name__ == "__main__":
    main()
