# Ionic Design System Skill

Use **IDS** (`ionic-design-system`) to build React UIs that stay aligned with the shipped tokens, variants, and components — not ad‑hoc CSS or invented props.

## What this skill does

- Composes screens from **documented** IDS components and variant values.
- Loads the **canonical stylesheet** so `data-*` variant attributes match real CSS.
- Defers to **CONTEXT.md** + **ai/llms.txt** for token lore and per-component APIs.
- Avoids one-off styling, random hex values, and wrapper components that duplicate system primitives.

## What IDS is

**Ionic Design System** is a typed React component library: components expose variant props that map to **`data-*` attributes** on the DOM. A single external CSS file (exported from the design system) applies layout, color, spacing, and states. Without that CSS, components fall back to minimal built-in styles — **always import the stylesheet** for on-brand UI.

## How agents should use IDS

1. **Read** `CONTEXT.md` (visual rules, tokens, do/don’t) and `ai/llms.txt` (props and enums per component).
2. **Install** `ionic-design-system` and **import the default theme CSS** (see below).
3. **Compose** with IDS primitives (`Button`, `Container`, `Text`, …). Prefer stacking layout via `Container` props over raw CSS Grid/Flex unless the design truly needs it.
4. **Map designs** to the closest existing component + `intent` / `appearance` / `size` (or equivalent) from llms.txt — do not invent new variant strings.
5. If something is not documented, **say it is unsupported** or use neutral/minimal styling — do not fabricate token names.

## Install

```bash
npm install ionic-design-system
```

Peer dependencies: `react` and `react-dom` (>= 18). `lucide-react` is optional (Icon registry names).

## Required stylesheet

Import the design system CSS **once** at app entry (before rendering IDS components).

**Published site (GitHub Pages):**

```tsx
import "https://ionic-design-system.github.io/ids-landing/styles/default.css";
import { Button, Container, Text } from "ionic-design-system";
```

**Local / vendored copy:**

```tsx
import "./styles/default.css"; // path to the IDS default theme
import { Button, Container, Text } from "ionic-design-system";
```

Plain HTML is fine for static shells:

```html
<link rel="stylesheet" href="https://ionic-design-system.github.io/ids-landing/styles/default.css" />
```

Do **not** skip the stylesheet and then compensate with Tailwind/colors on IDS nodes — that drifts from system behavior.

## Token and component usage rules

- **Variants** are constrained enums (e.g. `intent`, `appearance`, `size`). Use only values listed in **ai/llms.txt** or typings; invalid values are ignored at runtime.
- **Colors / spacing** for IDS surfaces should come from **semantic usage** in CONTEXT.md (e.g. intent colors, surface layering) — not arbitrary hex except when matching documented token hex for illustration.
- **Typography**: Prefer `Text` with `tag`, `size`, `weight` over bare `<p>`/`<h1>` with custom classes when the copy is part of the system UI.
- **Layout**: Prefer `Container` (`display`, `direction`, `spacing`, `padding`, …) over inventing BEM-style utility stacks for structure.

## Do / don’t

**Do**

- Import default CSS; mirror examples from `docs.html` and CONTEXT.md.
- Use flat props or `dimensionValues` (they are equivalent) as documented in llms.txt.
- Check **ai/llms.txt** for the exact prop name (`intent` vs legacy examples that say `color` — follow llms.txt for Button).

**Don’t**

- Don’t add inline styles or Tailwind classes to mimic IDS unless the user explicitly asks for non-system overrides.
- Don’t create parallel “design tokens” or CSS variables that aren’t in CONTEXT.md.
- Don’t invent components that mirror IDS — extend with app-specific **composition**, not clones of `Button`/`Input`.

## How to stay on-system

- Treat **https://ionic-design-system.github.io/ids-landing/CONTEXT.md** and **…/ai/llms.txt** as the source of truth for agents (plus this repo’s synced `styles/default.css` for actual values).
- When unsure about a variant, **grep llms.txt** or read the component section — do not guess.
- Prefer linking or quoting the exact prop names from llms.txt in plans and code.

## Example prompt (for tools that accept skill/context)

> Build a settings panel in React using `ionic-design-system`. Import the published default stylesheet from `ionic-design-system.github.io/ids-landing`. Use only components and props described in ai/llms.txt. Layout with `Container`; actions with `Button` (`intent`, `appearance`, `size` per docs). No custom hex colors — use IDS intents and surfaces only.

## Example React usage

```tsx
import "https://ionic-design-system.github.io/ids-landing/styles/default.css";
import {
  Button,
  Container,
  Text,
  Input,
} from "ionic-design-system";

export function SignInPreview() {
  return (
    <Container display="flex" direction="column" spacing="md" padding="lg">
      <Text text="Sign in" tag="h1" size="2xl" weight="bold" />
      <Input type="email" placeholder="you@example.com" size="default" />
      <Container display="flex" direction="row" spacing="sm">
        <Button label="Continue" intent="primary" appearance="solid" size="md" />
        <Button label="Cancel" intent="neutral" appearance="ghost" size="md" />
      </Container>
    </Container>
  );
}
```

## Guardrails

- **Never invent** component names or export paths — only what exists in `ionic-design-system` per llms.txt.
- **Never invent** variant values; if a Figma spec doesn’t map cleanly, choose the closest documented enum and note the gap.
- **Never replace** the IDS stylesheet with a trimmed subset unless the user’s pipeline explicitly requires it — missing rules break `data-*` styling.
- When the upstream **ids** repo adds its own `SKILL.md`, tooling may link there; this landing skill remains valid for **site-specific URLs and published CSS**.
