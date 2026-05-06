#!/usr/bin/env python3
"""
Inject SystemBenefitsSection into the IDS landing bundle (index.html).

Run after exporting or re-patching the bundler template so positioning copy survives
`python3 scripts/patch_landing_nav_bundle.py` (invoked automatically from that script).
"""

from __future__ import annotations

import base64
import gzip
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
BABEL_UUID = "e93a9179-2cce-400b-8145-f9595b4e5dc4"

# Inserted immediately before ProblemSection in the babel chunk; registered on window.

SYSTEM_BENEFITS_FN = """function SystemBenefitsSection({ copyTone }) {
  const eyebrow = copyTone === 'marketing' ? 'less bulk · sharper guardrails · ongoing ownership' : 'efficiency · enforcement · upkeep';
  const title = copyTone === 'marketing'
    ? 'Save tokens — don\\'t rewrite your system.'
    : 'Built to save tokens, not rewrite your system.';
  const lead = copyTone === 'marketing'
    ? 'IDS fronts tokens, primitives, rules, and guardrails so AI composes from shipped reality instead of regenerating stacks each session.'
    : 'IDS gives agents the system up front: tokens, primitives, components, usage rules, and guardrails. Instead of regenerating styles every time, agents can compose from what already exists.';

  const cards = [
    {
      tag: 'reuse',
      headline: 'Reuse what already exists',
      body: 'Agents don\\'t need to recreate your components or restate every style rule. They can work from the system you already ship.',
    },
    {
      tag: 'structure',
      headline: 'Spend tokens on structure',
      body: 'Use AI for the layout, intent, and composition decisions — then let IDS map that work back to approved components and tokens.',
    },
    {
      tag: 'drift',
      headline: 'Prevent design drift',
      body: 'Rules, tokens, and component metadata help generated UI stay aligned instead of slowly drifting away from the system.',
    },
    {
      tag: 'maintain',
      headline: 'Maintain the system over time',
      body: 'IDS is built for ongoing updates, governance, and sync — not one-off exports that go stale after the first generation.',
    },
  ];

  return (
    <section className="lp-grid-bg" style={{
      padding: '96px 48px',
      position: 'relative',
      borderTop: '1px solid var(--lp-border)',
      borderBottom: '1px solid var(--lp-border)',
      background: 'var(--lp-bg)',
    }}>
      <div style={{ maxWidth: 1120, margin: '0 auto' }}>
        <div className="reveal" style={{ marginBottom: 48, maxWidth: 800 }}>
          <div className="eyebrow" style={{ marginBottom: 16 }}>{eyebrow}</div>
          <h2 className="display" style={{ fontSize: 'clamp(32px, 3.8vw, 52px)', fontWeight: 600, lineHeight: 1.08, margin: '0 0 14px' }}>
            {title}
          </h2>
          <p style={{ fontSize: 17, color: 'var(--lp-fg-muted)', margin: 0, lineHeight: 1.6 }}>
            {lead}
          </p>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
          gap: 16,
          marginBottom: 40,
        }}>
          {cards.map((c, i) => (
            <div key={c.tag} className="reveal" style={{
              padding: '24px 22px',
              background: 'var(--lp-bg-elev)',
              border: '1px solid var(--lp-border)',
              borderRadius: 12,
              transitionDelay: `${i * 90}ms`,
            }}>
              <div className="mono" style={{ fontSize: 10, color: 'var(--lp-fg-subtle)', letterSpacing: '0.12em', textTransform: 'uppercase', marginBottom: 12 }}>
                {String(i + 1).padStart(2, '0')} · {c.tag}
              </div>
              <h3 className="display" style={{ fontSize: 18, fontWeight: 600, margin: '0 0 10px', lineHeight: 1.25 }}>
                {c.headline}
              </h3>
              <p style={{ fontSize: 13, color: 'var(--lp-fg-muted)', lineHeight: 1.62, margin: 0 }}>
                {c.body}
              </p>
            </div>
          ))}
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
          gap: 16,
        }}>
          <div className="reveal" style={{
            padding: '20px 22px',
            background: 'var(--lp-bg-elev)',
            border: '1px solid var(--lp-border)',
            borderRadius: 12,
          }}>
            <div className="mono" style={{ fontSize: 11, letterSpacing: '0.06em', textTransform: 'uppercase', color: 'var(--lp-fg-subtle)', marginBottom: 10 }}>
              Typical AI flow
            </div>
            <p className="mono" style={{ fontSize: 12, color: 'var(--lp-fg-muted)', margin: 0, lineHeight: 1.7 }}>
              Prompt → regenerate styles → rebuild components → inspect drift → fix manually
            </p>
          </div>
          <div className="reveal" style={{
            padding: '20px 22px',
            background: 'var(--lp-bg-elev)',
            border: '1px solid var(--lp-border)',
            borderRadius: 12,
            borderLeft: '3px solid var(--lp-accent)',
            boxShadow: '0 0 0 1px color-mix(in srgb, var(--lp-accent) 18%, transparent)',
          }}>
            <div className="mono" style={{ fontSize: 11, letterSpacing: '0.06em', textTransform: 'uppercase', color: 'var(--lp-accent)', marginBottom: 10 }}>
              IDS flow
            </div>
            <p className="mono" style={{ fontSize: 12, color: 'var(--lp-fg-muted)', margin: 0, lineHeight: 1.7 }}>
              Prompt → compose layout → apply tokens/components → ship on-system UI
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}


"""

APP_SNIPPET_BEFORE = """      <Hero motionOn={motionOn} copyTone={copyTone} key={`${t.hero}-${tick}`}/>
      <ProblemSection copyTone={copyTone}/>
"""

APP_SNIPPET_AFTER = """      <Hero motionOn={motionOn} copyTone={copyTone} key={`${t.hero}-${tick}`}/>
      <SystemBenefitsSection copyTone={copyTone}/>
      <ProblemSection copyTone={copyTone}/>
"""

OBJECT_LEGACY = (
    "Object.assign(window, { ProblemSection, HowItWorks, SiteFooter, useReveal });"
)
OBJECT_PATCHED = (
    "Object.assign(window, { SystemBenefitsSection, ProblemSection, HowItWorks, "
    "SiteFooter, useReveal });"
)


def _recompress_babel(manifest: dict, src: str) -> None:
    gz = gzip.compress(src.encode("utf-8"), compresslevel=9)
    manifest[BABEL_UUID]["data"] = base64.b64encode(gz).decode("ascii")
    manifest[BABEL_UUID]["compressed"] = True


def apply_landing_value_props_patch(html: str) -> str:
    tmpl_m = re.search(
        r'(<script type="__bundler/template">)\s*([\s\S]*?)\s*(</script>)',
        html,
    )
    if not tmpl_m:
        raise SystemExit("value_props: no __bundler/template in index.html")
    manifest_m = re.search(
        r'(<script type="__bundler/manifest">)\s*([\s\S]*?)\s*(</script>)',
        html,
    )
    if not manifest_m:
        raise SystemExit("value_props: no __bundler/manifest in index.html")

    template_inner = tmpl_m.group(2)
    template_obj = json.loads(template_inner)

    manifest_inner = manifest_m.group(2)
    manifest = json.loads(manifest_inner)

    if BABEL_UUID not in manifest:
        raise SystemExit("value_props: babel uuid missing from manifest")

    raw = base64.b64decode(manifest[BABEL_UUID]["data"])
    babel_src = (
        gzip.decompress(raw).decode("utf-8")
        if manifest[BABEL_UUID].get("compressed")
        else raw.decode("utf-8")
    )

    if "function SystemBenefitsSection" not in babel_src:
        needle = "function ProblemSection({ copyTone }) {"
        if needle not in babel_src:
            raise SystemExit(
                "value_props: babel anchor `function ProblemSection` missing "
                "(bundle layout changed)",
            )
        babel_src = babel_src.replace(
            needle,
            SYSTEM_BENEFITS_FN + "\n" + needle,
            1,
        )

    if OBJECT_PATCHED in babel_src:
        pass
    elif OBJECT_LEGACY in babel_src:
        babel_src = babel_src.replace(OBJECT_LEGACY, OBJECT_PATCHED, 1)
    elif "SystemBenefitsSection" not in babel_src:
        raise SystemExit("value_props: Object.assign(window export) anchor missing")

    if "<SystemBenefitsSection copyTone={copyTone}/>" in template_obj:
        pass
    elif APP_SNIPPET_BEFORE in template_obj:
        template_obj = template_obj.replace(APP_SNIPPET_BEFORE, APP_SNIPPET_AFTER, 1)
    else:
        raise SystemExit(
            "value_props: inline App JSX anchor missing "
            "(expected Hero + ProblemSection siblings)",
        )

    _recompress_babel(manifest, babel_src)

    new_template_json = json.dumps(template_obj, ensure_ascii=False)
    new_template_json = re.sub(
        r"(?i)</script>",
        r"\\u003c\\u002Fscript\\u003e",
        new_template_json,
    )
    new_manifest_json = json.dumps(manifest, separators=(",", ":"))

    html = html[: tmpl_m.start(2)] + new_template_json + html[tmpl_m.end(2) :]
    manifest_m2 = re.search(
        r'(<script type="__bundler/manifest">)\s*([\s\S]*?)\s*(</script>)',
        html,
    )
    html = (
        html[: manifest_m2.start(2)]
        + new_manifest_json
        + html[manifest_m2.end(2) :]
    )
    return html


def main() -> None:
    html = INDEX.read_text(encoding="utf-8")
    html = apply_landing_value_props_patch(html)
    INDEX.write_text(html, encoding="utf-8")
    print("Landing value props:", INDEX)


if __name__ == "__main__":
    main()
