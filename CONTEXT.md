# CONTEXT.md -- Ionic Design System

> AI-readable design system context for generating consistent, well-designed UI.
> Import components from `ionic-design-system`. Link the stylesheet in your app entry.

```tsx
import 'https://ionic-design-system.github.io/ids-landing/styles/default.css';
import { Button, Text, Container } from 'ionic-design-system';
```

---

## 1. Overview

**Ionic Design System** is a typed, accessible React component library with CSS-driven theming. Components accept variant props that map to `data-*` attributes styled by an external CSS stylesheet exported from the design editor.

**Philosophy**: Clean, professional interfaces with strong visual hierarchy. Favor clarity over decoration. Every element should earn its place.

**Target audience**: SaaS dashboards, admin panels, internal tools, and content-rich applications.

---

## 2. Visual Theme & Atmosphere

- **Density**: Comfortable -- generous but not wasteful spacing (8px base unit)
- **Mood**: Professional and clean. Neutral surfaces, intentional color accents
- **Corners**: Softly rounded by default (8px `borderRadius`). Use `pill` for tags/badges, `sharp` for data-dense UIs
- **Hierarchy**: Achieved through typography weight/size, color contrast, and elevation -- not borders or heavy decoration
- **Font**: Inter (text), Geist (display headings), Geist Mono (code)

---

## 3. Color System

### 3.1 Intent Colors (when to use each)

| Intent | Base hex | Use for |
|-----------|-----------|---------|
| **primary** | `#3B82F6` | CTAs, active states, links, focus rings, brand emphasis |
| **danger** | `#DC2626` | Destructive actions, errors, required validation |
| **success** | `#16A34A` | Confirmations, completed states, positive metrics |
| **warning** | `#F59E0B` | Caution notices, approaching limits, pending states |
| **info** | `#0284C7` | Informational banners, help text, neutral highlights |
| **neutral** | `#6B7280` | Default/secondary actions, disabled states, borders |

Each intent has a full scale (50--950). Use 500 for solid fills, 50--100 for soft backgrounds, 600--700 for hover/pressed states.

### 3.2 Surfaces & Backgrounds

| Token | Value | Use for |
|-------|-------|---------|
| `surface.background` | `#F9FAFB` (neutral-50) | Page background |
| `surface.card` | `#FFFFFF` | Cards, panels, modals |
| `surface.elevated` | `#FFFFFF` | Popovers, dropdowns, tooltips |
| `surface.inverse` | `#111827` (neutral-900) | Dark banners, inverted sections |

### 3.3 Text Colors

| Token | Value | Use for |
|-------|-------|---------|
| `text.primary` | `#111827` (neutral-900) | Headings, body text, labels |
| `text.secondary` | `#4B5563` (neutral-600) | Descriptions, helper text |
| `text.tertiary` | `#6B7280` (neutral-500) | Placeholders, captions |
| `text.disabled` | `#9CA3AF` (neutral-400) | Disabled labels, inactive items |
| `text.inverse` | `#FFFFFF` | Text on dark/colored backgrounds |

### 3.4 Border Colors

| Token | Value | Use for |
|-------|-------|---------|
| `border.default` | `#E5E7EB` (neutral-200) | Card borders, dividers |
| `border.strong` | `#9CA3AF` (neutral-400) | Emphasized borders, input focus |
| `border.subtle` | `#F3F4F6` (neutral-100) | Subtle separators |
| `border.focus` | `#3B82F6` (primary-500) | Focus rings |

### 3.5 Full Palettes

**Primary**: `#eff0f2` `#e2e5eb` `#cad4e4` `#a5bce2` `#79a3e7` **#3B82F6** `#1669f1` `#1054c2` `#0f3f8e` `#0c2a5c` `#061123`

**Danger/Red**: `#FEF2F2` `#FEE2E2` `#FECACA` `#FCA5A5` `#F87171` **#DC2626** `#B91C1C` `#991B1B` `#7F1D1D` `#450A0A` `#2D0707`

**Success/Green**: `#F0FDF4` `#DCFCE7` `#BBF7D0` `#86EFAC` `#4ADE80` **#16A34A** `#15803D` `#166534` `#14532D` `#134E2A` `#052E16`

**Warning/Amber**: `#FFFBEB` `#FEF3C7` `#FDE68A` `#FCD34D` `#FBBF24` **#F59E0B** `#D97706` `#B45309` `#92400E` `#78350F` `#451A03`

**Info/Sky**: `#F0F9FF` `#E0F2FE` `#BAE6FD` `#7DD3FC` `#38BDF8` **#0284C7** `#0369A1` `#075985` `#0C4A6E` `#082F49` `#051E30`

**Neutral/Gray**: `#F9FAFB` `#F3F4F6` `#E5E7EB` `#D1D5DB` `#9CA3AF` **#6B7280** `#4B5563` `#374151` `#1F2937` `#111827` `#0A0A0A`

---

## 4. Typography

### 4.1 Type Scale

| Size token | Value | Use for |
|------------|-------|---------|
| `xs` | 12px | Captions, fine print, badge labels |
| `sm` | 14px | Secondary text, table cells, helper text |
| `base`/`md` | 16px | Body text, input values, default |
| `lg` | 18px | Subheadings, card titles, emphasis |
| `xl` | 20px | Section headings |
| `2xl` | 24px | Page section titles |
| `3xl` | 30px | Page titles, hero text |

> Text `size` prop accepts: `"xs"`, `"sm"`, `"base"`, `"lg"`, `"xl"`, `"2xl"`, `"3xl"`

### 4.2 Font Weights

| Weight | Value | Use for |
|--------|-------|---------|
| `normal` | 400 | Body text, descriptions |
| `medium` | 500 | Labels, nav items, subtle emphasis |
| `semibold` | 600 | Card titles, subheadings, button labels |
| `bold` | 700 | Page headings, strong emphasis |

### 4.3 Line Heights

| Token | Value | Use for |
|-------|-------|---------|
| `tight` | 1.25 | Headings, display text |
| `snug` | 1.375 | Compact UI, table rows |
| `normal` | 1.5 | Body text (default) |
| `relaxed` | 1.75 | Long-form content |

### 4.4 Heading Hierarchy

```tsx
<Text tag="h1" size="3xl" weight="bold" />    {/* Page title */}
<Text tag="h2" size="2xl" weight="semibold" /> {/* Section title */}
<Text tag="h3" size="xl" weight="semibold" />  {/* Subsection */}
<Text tag="h4" size="lg" weight="medium" />    {/* Card title */}
<Text tag="p" size="base" weight="normal" />   {/* Body text */}
<Text tag="p" size="sm" color="muted" />       {/* Helper text */}
```

---

## 5. Spacing & Layout

### 5.1 Spacing Scale (8px base grid)

Container `spacing` and `padding` props accept these values:

| Prop value | Pixels | Use for |
|------------|--------|---------|
| `"none"` | 0 | No spacing |
| `"sm"` | 8px | Compact spacing (within form fields, small gaps) |
| `"md"` | 16px | Standard spacing (between form fields, card padding) |
| `"lg"` | 24px | Between sections, generous card padding |

> **Do NOT use `"xs"`, `"xl"`, `"2xl"` etc. as spacing/padding prop values** — they are CSS variables only, not valid component props. For finer control, use inline `style={{ gap: '4px' }}`.

### 5.2 Common Layout Patterns

**Page layout:**
```tsx
<Container display="flex" direction="column" spacing="lg" padding="lg"
  style={{ maxWidth: '1280px', margin: '0 auto' }}>
  {/* page content */}
</Container>
```

**Card grid (2-column):**
```tsx
<Container display="grid" columns="2" spacing="md">
  <Container color="card" padding="lg" elevation="sm" shape="rounded">...</Container>
  <Container color="card" padding="lg" elevation="sm" shape="rounded">...</Container>
</Container>
```

**Form layout:**
```tsx
<Container display="flex" direction="column" spacing="md" padding="lg">
  <Label text="Email" htmlFor="email" required />
  <Input id="email" type="email" placeholder="you@example.com" />
  <Label text="Message" htmlFor="msg" />
  <Textarea id="msg" rows={4} />
  <Container display="flex" direction="row" spacing="sm" alignment="end">
    <Button label="Cancel" intent="neutral" appearance="ghost" />
    <Button label="Submit" intent="primary" appearance="solid" />
  </Container>
</Container>
```

**Sidebar + content:**
```tsx
<Container display="flex" direction="row" spacing="none">
  <Container display="flex" direction="column" spacing="sm" padding="md"
    style={{ width: '240px', borderRight: '1px solid #E5E7EB' }}>
    {/* nav items */}
  </Container>
  <Container display="flex" direction="column" spacing="lg" padding="lg"
    style={{ flex: 1 }}>
    {/* main content */}
  </Container>
</Container>
```

**Header/nav bar:**
```tsx
<Container display="flex" direction="row" alignment="center" padding="md"
  style={{ justifyContent: 'space-between' }}>
  <Text text="AppName" size="lg" weight="semibold" />
  <Container display="flex" direction="row" spacing="sm">
    <Button label="Settings" appearance="ghost" icon="Settings" />
    <Avatar src="/photo.jpg" size="sm" shape="circle" />
  </Container>
</Container>
```

---

## 6. Depth & Elevation

### 6.1 Shadow Scale

| Level | CSS value | Use for |
|-------|-----------|---------|
| `none` | none | Flat elements, inline content |
| `sm` | `0 1px 2px 0 rgb(0 0 0 / 0.05)` | Subtle lift: cards at rest, inputs |
| `md` | `0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)` | Cards, containers with content |
| `lg` | `0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)` | Popovers, dropdown menus |
| `xl` | `0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)` | Modals, dialogs |

### 6.2 Surface Hierarchy

```
Page background (neutral-50) -- no shadow
  Card (white, elevation="sm") -- sm shadow
    Popover/Dropdown (white, elevation="lg") -- lg shadow
      Modal/Dialog (white, elevation="xl") -- xl shadow + overlay
```

### 6.3 Border Radius Scale

| Token | Value | Use for |
|-------|-------|---------|
| `none` | 0 | Tables, data-dense elements |
| `sm` | 4px | Small controls (checkboxes, badges) |
| `md` / `default` | 8px | Buttons, inputs, cards (default) |
| `lg` | 12px | Larger cards, panels |
| `xl` | 16px | Hero cards, prominent containers |
| `full` | 9999px | Avatars, pills, circular buttons |

---

## 7. Components Quick Reference

### Form Components

| Component | Description | Key props | Default |
|-----------|-------------|-----------|---------|
| **Button** | Primary action element | `label`, `intent`, `appearance`, `size`, `icon` | `intent="primary" appearance="solid" size="md"` |
| **Input** | Single-line text field | `placeholder`, `type`, `size`, `shape` | `size="default" shape="rounded"` |
| **Textarea** | Multi-line text field | `placeholder`, `rows`, `resize`, `size` | `rows={3} size="default"` |
| **Select** | Dropdown selector | `options`, `label`, `placeholder`, `appearance` | `appearance="outline" size="md"` |
| **Checkbox** | Boolean toggle | `checked`, `onChange`, `size` | `size="md"` |
| **Radio** | Single selection from group | `checked`, `onChange`, `name`, `size` | `size="md"` |
| **Switch** | On/off toggle | `checked`, `onChange`, `color`, `size` | `color="primary" size="md"` |
| **Slider** | Range value selector | `value`, `min`, `max`, `onChange`, `mode` | `mode="single" size="md"` |
| **Label** | Form field label | `text`, `htmlFor`, `required` | -- |

**Valid prop values (form):**
- Button `intent`: `"primary"` `"danger"` `"success"` `"warning"` `"info"` `"neutral"` `"secondary"`
- Button `appearance`: `"solid"` `"soft"` `"outline"` `"ghost"`
- Button `size`: `"sm"` `"md"` `"lg"` · Button `shape`: `"rounded"` `"pill"` `"sharp"`
- Button/Tab `icon`: **string name** from Lucide icon registry (e.g., `"Plus"`, `"Settings"`, `"Trash"`). Do NOT pass JSX elements — pass the icon name as a string.
- Input/Textarea `size`: `"sm"` `"default"` `"lg"` · `shape`: `"rounded"` `"pill"` `"square"`
- Switch `color`: `"primary"` `"success"` `"danger"` `"warning"` `"info"` `"neutral"`
- Select `options`: array of `{ value: string, label: string }` objects:
  ```tsx
  <Select placeholder="Choose..." options={[
    { value: 'light', label: 'Light' },
    { value: 'dark', label: 'Dark' },
  ]} />
  ```

### Content Components

| Component | Description | Key props | Default |
|-----------|-------------|-----------|---------|
| **Text** | Typography element | `text`, `tag`, `size`, `weight`, `color` | `tag="span" size="base"` |
| **Badge** | Status/count label | `label`, `color`, `variant`, `size`, `shape` | `color="default" shape="rounded"` |
| **Icon** | Lucide SVG icon | `name`, `size`, `color` | `size="md" color="inherit"` |
| **Image** | Responsive image | `src`, `alt`, `fit`, `aspectRatio` | `fit="cover"` |
| **Avatar** | User profile image | `src`, `initials`, `size`, `shape` | `size="md" shape="circle"` |
| **Link** | Anchor with styling | `href`, `text`, `color` | `color="default"` |

### Feedback Components

| Component | Description | Key props | Default |
|-----------|-------------|-----------|---------|
| **Alert** | Notification banner | `title`, `description`, `intent`, `dismissible` | `intent="info"` |
| **Toast** | Popup notification | `title`, `variant`, `position`, `duration` | `position="bottom-right" duration={3000}` |
| **Spinner** | Loading indicator | `size`, `color`, `variant` | `variant="circular" color="primary"` |
| **Progress** | Progress bar | `value`, `max`, `color`, `indeterminate` | `max={100}` |
| **Skeleton** | Loading placeholder | `shape`, `animation`, `width`, `height` | `shape="rectangle" animation="pulse"` |
| **Tooltip** | Hover hint (primitive) | `content`, `color` | Use `TooltipRoot` composition instead |

**Valid prop values (content/feedback):**
- Text `size`: `"xs"` `"sm"` `"base"` `"lg"` `"xl"` `"2xl"` `"3xl"` · `color`: `"default"` `"muted"` `"primary"` `"success"` `"destructive"`
- Text `weight`: `"normal"` `"medium"` `"semibold"` `"bold"` · `tag`: `"span"` `"p"` `"h1"`..`"h6"` `"label"`
- Badge `color`: `"default"` `"primary"` `"success"` `"warning"` `"danger"` `"info"` `"muted"`
- Badge `variant`: `"solid"` `"soft"` `"outline"` · `shape`: `"rounded"` `"pill"` `"sharp"` · `size`: `"sm"` `"md"` `"lg"`
- Skeleton `shape`: `"rectangle"` `"circle"` `"text"` · `animation`: `"pulse"` `"wave"` `"none"`
- Toast `variant`: `"default"` `"success"` `"error"` `"warning"` `"info"` · `position`: `"top-right"` `"bottom-right"` `"top-left"` `"bottom-left"` `"top-center"` `"bottom-center"`
- Alert `intent`: `"info"` `"danger"` `"success"` `"warning"` `"neutral"`
- Avatar `size`: `"xs"` `"sm"` `"md"` `"lg"` `"xl"` · `shape`: `"circle"` `"square"`

### Layout Components

| Component | Description | Key props | Default |
|-----------|-------------|-----------|---------|
| **Container** | Flex/grid wrapper | `display`, `direction`, `spacing`, `padding`, `color`, `elevation` | `display="flex" direction="column"` |
| **Divider** | Line separator | `orientation`, `color`, `size` | `orientation="horizontal"` |
| **Tab** | Tab selector | `label`, `selected`, `appearance` | `appearance="line"` |
| **Table** | Data table | Sub-components: `TableHeader`, `TableBody`, `TableRow`, `TableHead`, `TableCell` | -- |

**Valid prop values (layout):**
- Container `display`: `"flex"` `"grid"` `"block"` · `direction`: `"row"` `"column"` `"row-reverse"` `"column-reverse"`
- Container `spacing`: `"none"` `"sm"` `"md"` `"lg"` · `padding`: `"none"` `"sm"` `"md"` `"lg"`
- Container `color`: `"neutral"` `"card"` `"muted"` `"primary"` `"secondary"` · `elevation`: `"none"` `"sm"` `"md"` `"lg"`
- Container `shape`: `"none"` `"rounded"` `"pill"` · `wrap`: `"wrap"` `"nowrap"`
- Divider `orientation`: `"horizontal"` `"vertical"`

### Interactive Components

| Component | Description | Key props | Default |
|-----------|-------------|-----------|---------|
| **ToggleButton** | Pressable toggle | `pressed`, `onPressedChange`, `label`, `icon` | `appearance="outline"` |
| **MenuItem** | Menu row | `label`, `icon`, `shortcut`, `color` | `size="md"` |

---

## 8. Composition Patterns

### Card with Action

```tsx
import { Container, Text, Button } from 'ionic-design-system';

<Container color="card" padding="lg" elevation="sm" shape="rounded">
  <Container display="flex" direction="column" spacing="sm">
    <Text tag="h3" text="Project Settings" size="lg" weight="semibold" />
    <Text text="Manage your project configuration and team access." color="muted" size="sm" />
  </Container>
  <Container display="flex" direction="row" spacing="sm" alignment="end"
    style={{ marginTop: '16px' }}>
    <Button label="Cancel" intent="neutral" appearance="ghost" size="sm" />
    <Button label="Save Changes" intent="primary" appearance="solid" size="sm" />
  </Container>
</Container>
```

### Form Group (Label + Input + Helper)

```tsx
import { Container, Label, Input, Text } from 'ionic-design-system';

<Container display="flex" direction="column" spacing="xs">
  <Label text="Email Address" htmlFor="email" required />
  <Input id="email" type="email" placeholder="you@example.com" />
  <Text text="We'll never share your email." size="xs" color="muted" />
</Container>
```

### Status Badge Row

```tsx
import { Container, Badge } from 'ionic-design-system';

<Container display="flex" direction="row" spacing="sm">
  <Badge label="Active" color="success" variant="soft" shape="pill" size="sm" />
  <Badge label="3 Pending" color="warning" variant="soft" shape="pill" size="sm" />
  <Badge label="1 Error" color="danger" variant="soft" shape="pill" size="sm" />
</Container>
```

### Confirmation Dialog

```tsx
import { DialogRoot, DialogTrigger, DialogOverlay, DialogContent, DialogClose,
         Button, Text, Container } from 'ionic-design-system';

<DialogRoot>
  <DialogTrigger>
    <Button label="Delete Account" intent="danger" appearance="outline" />
  </DialogTrigger>
  <DialogOverlay />
  <DialogContent>
    <Container display="flex" direction="column" spacing="md" padding="lg">
      <Text tag="h2" text="Are you sure?" size="xl" weight="semibold" />
      <Text text="This action cannot be undone. All data will be permanently deleted."
        color="muted" />
      <Container display="flex" direction="row" spacing="sm" alignment="end">
        <DialogClose><Button label="Cancel" intent="neutral" appearance="ghost" /></DialogClose>
        <Button label="Delete" intent="danger" appearance="solid" />
      </Container>
    </Container>
  </DialogContent>
</DialogRoot>
```

### Dropdown Menu

```tsx
import { DropdownMenuRoot, DropdownMenuTrigger, DropdownMenuContent,
         DropdownMenuItem, DropdownMenuSeparator, Button } from 'ionic-design-system';

<DropdownMenuRoot>
  <DropdownMenuTrigger>
    <Button label="Actions" appearance="outline" icon="ChevronDown" iconPosition="right" />
  </DropdownMenuTrigger>
  <DropdownMenuContent placement="bottom-start">
    <DropdownMenuItem onSelect={() => edit()}>Edit</DropdownMenuItem>
    <DropdownMenuItem onSelect={() => duplicate()}>Duplicate</DropdownMenuItem>
    <DropdownMenuSeparator />
    <DropdownMenuItem onSelect={() => remove()}>Delete</DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenuRoot>
```

### User Profile Row

```tsx
import { Container, Avatar, Text, Badge } from 'ionic-design-system';

<Container display="flex" direction="row" spacing="md" alignment="center">
  <Avatar src="/photo.jpg" alt="Jane Smith" size="lg" shape="circle" />
  <Container display="flex" direction="column" spacing="xs">
    <Text text="Jane Smith" weight="semibold" />
    <Text text="jane@company.com" size="sm" color="muted" />
  </Container>
  <Badge label="Admin" color="primary" variant="soft" shape="pill" size="sm" />
</Container>
```

### Tab Navigation

```tsx
import { Container, Tab } from 'ionic-design-system';

const [active, setActive] = useState(0);
const tabs = ['Overview', 'Members', 'Settings'];

<Container display="flex" direction="row" spacing="none"
  style={{ borderBottom: '1px solid #E5E7EB' }}>
  {tabs.map((t, i) => (
    <Tab key={i} label={t} selected={active === i}
      onClick={() => setActive(i)} appearance="line" />
  ))}
</Container>
```

### Accordion FAQ

```tsx
import { AccordionRoot, AccordionItem, AccordionTrigger,
         AccordionContent } from 'ionic-design-system';

<AccordionRoot type="single" defaultValue="q1">
  <AccordionItem value="q1">
    <AccordionTrigger>How do I reset my password?</AccordionTrigger>
    <AccordionContent>Go to Settings, then Security, then click Reset Password.</AccordionContent>
  </AccordionItem>
  <AccordionItem value="q2">
    <AccordionTrigger>Can I change my plan?</AccordionTrigger>
    <AccordionContent>Yes, visit the Billing page to upgrade or downgrade.</AccordionContent>
  </AccordionItem>
</AccordionRoot>
```

### Data Table with Status

```tsx
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell,
         Badge } from 'ionic-design-system';

<Table>
  <TableHeader>
    <TableRow>
      <TableHead>Name</TableHead>
      <TableHead>Status</TableHead>
      <TableHead>Role</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    <TableRow>
      <TableCell>Alice Johnson</TableCell>
      <TableCell><Badge label="Active" color="success" variant="soft" size="sm" /></TableCell>
      <TableCell>Engineer</TableCell>
    </TableRow>
    <TableRow>
      <TableCell>Bob Chen</TableCell>
      <TableCell><Badge label="Away" color="warning" variant="soft" size="sm" /></TableCell>
      <TableCell>Designer</TableCell>
    </TableRow>
  </TableBody>
</Table>
```

---

## 9. Do's and Don'ts

### Color Usage
- DO use `intent` prop on Button (not `color`) -- e.g., `intent="primary"`
- DO use `color` prop on Badge -- e.g., `color="success"`
- DO use semantic intent colors for meaning: danger=destructive, success=positive, warning=caution
- DON'T use danger/red for non-destructive actions
- DON'T mix intent meanings (e.g., green button that deletes)

### Buttons
- DO have one primary solid button per section/form (the main CTA)
- DO use `appearance="ghost"` or `appearance="outline"` for secondary actions
- DO use `intent="danger"` only for destructive actions (delete, remove, revoke)
- DON'T place multiple `appearance="solid" intent="primary"` buttons side by side
- DON'T use `intent="success"` for submit buttons -- use `intent="primary"`

### Spacing
- DO use the `spacing` and `padding` props on Container rather than custom CSS
- DO keep spacing consistent within a section (don't mix `sm` and `lg` between siblings)
- DO use `spacing="md"` (16px) as the default gap between form fields
- DON'T use pixel values in inline styles when a spacing token exists

### Typography
- DO use Text component with `tag` prop for semantic HTML (h1-h6, p, span)
- DO pair `size` with appropriate `weight` (larger text = bolder)
- DO use `color="muted"` for helper/secondary text
- DON'T skip heading levels (h1 then h3)
- DON'T use more than 3 different text sizes in a single view

### Accessibility
- DO add `htmlFor` on Label pointing to the input `id`
- DO add `required` prop on Label for required fields
- DO use `alt` text on Image and Avatar
- DO use TooltipRoot composition (not primitive Tooltip) for hover hints
- DON'T rely on color alone to convey information -- pair with text or icons
- DON'T use `color="muted"` for critical information

### Common Anti-patterns
- DON'T pass editor-only props: `nodeId`, `canvasId`, `resolvedProps`, `stateStyles`, `previewState`
- DON'T use `content` prop on Text (deprecated) -- use `text` or `children`
- DON'T forget `name` on Radio groups -- radios without a shared `name` won't be exclusive
- DON'T set variant values outside the valid union -- they are silently ignored

---

## 10. Responsive Behavior

### Breakpoints

| Name | Min-width | Typical use |
|------|-----------|-------------|
| Mobile | 0--767px | Single column, stacked layout, full-width cards |
| Tablet | 768px | 2-column grid, collapsible sidebar |
| Desktop | 1280px | 3--4 column grid, persistent sidebar |

### Guidelines

- **Mobile-first**: Design the single-column stacked layout first, then add columns at wider breakpoints
- **Touch targets**: Minimum 44px height/width for interactive elements on mobile. Use `size="lg"` for Button/Input in mobile contexts
- **Stacking**: Switch Container `direction` from `"row"` to `"column"` at mobile breakpoints
- **Max-width**: Content areas should max out at 1280px and center with auto margins
- **Container sizing**: Use Container `size="full"` for mobile, constrain at wider breakpoints

### Mobile-specific Patterns

```tsx
{/* Responsive card stack -- column on mobile, row on desktop */}
<Container display="flex"
  direction={isMobile ? 'column' : 'row'}
  spacing="md" padding="md">
  <Container color="card" padding="md" elevation="sm" shape="rounded">...</Container>
  <Container color="card" padding="md" elevation="sm" shape="rounded">...</Container>
</Container>
```

---

## 11. Accessibility

### Color Contrast
- Text on white: use neutral-700 (#374151) or darker for WCAG AA (4.5:1 ratio)
- Primary (#3B82F6) on white passes AA for large text only. Use white text on primary backgrounds
- All intent-500 colors meet AA contrast when used as fills with white text

### Focus Management
- Focus rings use `#3B82F6` (primary-500) with a 3px ring offset
- All interactive components have built-in `:focus-visible` styling
- DialogRoot traps focus within the dialog and restores focus on close
- DropdownMenuRoot supports arrow key navigation, Home, End

### ARIA (built-in)
- Switch: `role="switch"` + `aria-checked`
- Progress: `role="progressbar"` + `aria-valuenow/min/max`
- Dialog: `role="dialog"` + focus trap
- Accordion: `aria-expanded` on triggers
- Tooltip: `aria-describedby` auto-linked

### Keyboard
- All compositions (Tooltip, Popover, Dialog, Disclosure, Accordion, DropdownMenu) respond to Escape to dismiss
- DropdownMenu items navigable via arrow keys
- Tab components clickable via Enter/Space

---

## 12. Agent Prompt Guide

### Quick-start prompt

> Build a [page type] using the Ionic Design System. Import all components from `ionic-design-system`. Use Container for layout with flex/grid display. Use Text with appropriate tag/size/weight for headings. Use the intent color system: primary for CTAs, danger for destructive actions, success for confirmations, neutral for secondary actions. Default button is `intent="primary" appearance="solid" size="md"`. Default card is `Container color="card" padding="lg" elevation="sm" shape="rounded"`.

### Pattern prompts

**Settings form:**
> Create a settings form. Use Container direction="column" spacing="md" padding="lg". Each field is: Label (with htmlFor + required) then Input or Select. End with a row of Cancel (ghost neutral) and Save (solid primary) buttons.

**Dashboard with stats:**
> Create a dashboard with a 3-column card grid. Each card: Container color="card" padding="lg" elevation="sm" shape="rounded". Inside: Text size="sm" color="muted" for label, Text size="2xl" weight="bold" for metric, Badge variant="soft" shape="pill" size="sm" for status.

**Data table page:**
> Create a data table using Table with TableHeader/TableBody/TableRow/TableHead/TableCell. Add Badge components for status cells. Wrap in Container padding="lg". Add a header row with Text h2 and a Button for "Add New".

### Key rules for consistent output
1. Always import from `ionic-design-system`
2. Button uses `intent` (not `color`) for color selection
3. Badge uses `color` prop + `variant` for style (solid/soft/outline)
4. Toast uses `variant` prop (not `intent`)
5. Use Container for all layout -- never raw `<div>` with flexbox
6. Use Text for all typography -- never raw `<p>` or `<h1>`
7. Prefer compositions (TooltipRoot, DialogRoot) over InteractionProvider

---

## Motion

| Token | Value | Use for |
|-------|-------|---------|
| `duration-instant` | 0ms | Immediate state changes |
| `duration-fast` | 150ms | Micro-interactions (hover, focus) |
| `duration-normal` | 250ms | Standard transitions (expand, slide) |
| `duration-slow` | 400ms | Complex animations (modal enter) |
| `duration-slower` | 600ms | Dramatic transitions (page enter) |

Easing: `ease-out` (`cubic-bezier(0, 0, 0.2, 1)`) for enters, `ease-in` (`cubic-bezier(0.4, 0, 1, 1)`) for exits, `ease-in-out` for persistent animations.
