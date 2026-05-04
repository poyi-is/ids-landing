# Ionic Design System — Default Design System Context

> AI-readable context for design system tokens and component variants.
> For component API reference, see llms.txt

> IMPORTANT: Button uses `intent` (not `color`) for color selection.
> Appearance + intent combine: e.g., appearance="solid" intent="primary".
> Badge uses `color` prop (maps to intent in DB).
> Toast uses `variant` prop (maps to type in DB).

## Base Tokens

### borderRadius
- default: 8px
- full: 9999px
- lg: 12px
- md: 8px
- none: 0
- sm: 4px
- xl: 16px

### borderWidth
- default: 1px
- heavy: 3px
- medium: 2px
- none: 0
- thick: 4px
- thin: 1px

### color
- black: #000000
- blue-100: #dbeafe
- blue-200: #bfdbfe
- blue-300: #93c5fd
- blue-400: #60a5fa
- blue-50: #eff6ff
- blue-500: #3b82f6
- blue-600: #2563eb
- blue-700: #1d4ed8
- blue-800: #1e40af
- blue-900: #1e3a8a
- danger-100: #FEE2E2
- danger-200: #FECACA
- danger-300: #FCA5A5
- danger-400: #F87171
- danger-50: #FEF2F2
- danger-500: #DC2626
- danger-600: #B91C1C
- danger-700: #991B1B
- danger-800: #7F1D1D
- danger-900: #450A0A
- danger-950: #2D0707
- gray-100: #F3F4F6
- gray-200: #E5E7EB
- gray-300: #D1D5DB
- gray-400: #9CA3AF
- gray-50: #F9FAFB
- gray-500: #6B7280
- gray-600: #4B5563
- gray-700: #374151
- gray-800: #1F2937
- gray-900: #111827
- gray-950: #0A0A0A
- info-100: #E0F2FE
- info-200: #BAE6FD
- info-300: #7DD3FC
- info-400: #38BDF8
- info-50: #F0F9FF
- info-500: #0284C7
- info-600: #0369A1
- info-700: #075985
- info-800: #0C4A6E
- info-900: #082F49
- info-950: #051E30
- neutral-100: #F3F4F6
- neutral-200: #E5E7EB
- neutral-300: #D1D5DB
- neutral-400: #9CA3AF
- neutral-50: #F9FAFB
- neutral-500: #6B7280
- neutral-600: #4B5563
- neutral-700: #374151
- neutral-800: #1F2937
- neutral-900: #111827
- neutral-950: #0A0A0A
- primary: #3B82F6
- primary-100: #e2e5eb
- primary-200: #cad4e4
- primary-300: #a5bce2
- primary-400: #79a3e7
- primary-50: #eff0f2
- primary-500: #3B82F6
- primary-600: #1669f1
- primary-700: #1054c2
- primary-800: #0f3f8e
- primary-900: #0c2a5c
- primary-950: #061123
- red-100: #FEE2E2
- red-200: #FECACA
- red-300: #FCA5A5
- red-400: #F87171
- red-50: #FEF2F2
- red-500: #EF4444
- red-600: #DC2626
- red-700: #B91C1C
- red-800: #991B1B
- red-900: #7F1D1D
- red-950: #450A0A
- success-100: #DCFCE7
- success-200: #BBF7D0
- success-300: #86EFAC
- success-400: #4ADE80
- success-50: #F0FDF4
- success-500: #16A34A
- success-600: #15803D
- success-700: #166534
- success-800: #14532D
- success-900: #134E2A
- success-950: #052E16
- transparent: transparent
- warning-100: #FEF3C7
- warning-200: #FDE68A
- warning-300: #FCD34D
- warning-400: #FBBF24
- warning-50: #FFFBEB
- warning-500: #F59E0B
- warning-600: #D97706
- warning-700: #B45309
- warning-800: #92400E
- warning-900: #78350F
- warning-950: #451A03
- white: #FFFFFF
- white-alpha-30: rgba(255, 255, 255, 0.3)

### fontFamily
- display: Geist
- mono: Geist Mono
- text: Inter

### fontSize
- 2xl: 24px
- 3xl: 30px
- 4xl: 36px
- lg: 18px
- md: 16px
- sm: 14px
- tab-sm: 13px
- xl: 20px
- xs: 12px

### fontWeight
- bold: 700
- medium: 500
- normal: 400
- semibold: 600

### lineHeight
- compact: 1.4
- loose: 1.6
- normal: 1.5
- relaxed: 1.75
- snug: 1.375
- tight: 1.25

### menu
- accentPreset: subtle
- colorPreset: light

### motion
- duration-fast: 150ms
- duration-instant: 0ms
- duration-normal: 250ms
- duration-slow: 400ms
- duration-slower: 600ms
- easing-ease-in: cubic-bezier(0.4, 0, 1, 1)
- easing-ease-in-out: cubic-bezier(0.4, 0, 0.2, 1)
- easing-ease-out: cubic-bezier(0, 0, 0.2, 1)
- easing-linear: linear
- easing-sharp: cubic-bezier(0.4, 0, 0.6, 1)
- easing-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275)

### objectFit
- contain: contain
- cover: cover
- fill: fill
- none: none
- scaleDown: scale-down

### opacity
- 25: 0.25
- 50: 0.5
- 60: 0.6
- 75: 0.75
- opaque: 1
- transparent: 0

### outline
- focusDanger: 2px solid {semantic.status.danger}
- focusPrimary: 2px solid {semantic.focus.ring}
- none: none

### preset
- auto: auto
- border-bottom-none: none
- border-style-none: none
- contain: contain
- cover: cover
- fill: fill
- focus-danger: 2px solid {semantic.status.danger}
- focus-primary: 2px solid {semantic.focus.ring}
- none: none
- photo32: 3 / 2
- pointer-none: none
- pressed: scale(0.98)
- scaleDown: scale-down
- solid: solid
- square: 1 / 1
- standard43: 4 / 3
- video169: 16 / 9

### shadow
- button-focus-danger: 0 0 0 3px {semantic.intent.danger.layer200}
- button-focus-info: 0 0 0 3px {semantic.intent.info.layer200}
- button-focus-neutral: 0 0 0 3px {semantic.intent.neutral.layer200}
- button-focus-success: 0 0 0 3px {semantic.intent.success.layer200}
- button-focus-warning: 0 0 0 3px {semantic.intent.warning.layer200}
- focus-ring-ghost: 0 0 0 2px {semantic.focus.ring}
- focus-ring-neutral: 0 0 0 3px {semantic.intent.neutral.layer200}
- focus-ring-primary: 0 0 0 3px {semantic.focus.ring}
- focus-ring-primary-strong: 0 0 0 4px {semantic.focus.ring}
- focus-ring-soft: 0 0 0 2px {semantic.focus.ring}
- lg: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)
- md: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)
- none: none
- preset: sm
- radio-focus-neutral: 0 0 0 3px {semantic.intent.neutral.layer200}
- radio-focus-primary: 0 0 0 3px {semantic.intent.primary.layer200}
- radio-focus-primary-strong: 0 0 0 3px {semantic.intent.primary.layer200}
- radio-hover-neutral: 0 0 0 2px {semantic.intent.neutral.layer100}
- radio-hover-primary: 0 0 0 2px {semantic.intent.primary.layer100}
- radio-hover-primary-strong: 0 0 0 2px {semantic.intent.primary.layer100}
- sm: 0 1px 2px 0 rgb(0 0 0 / 0.05)
- switch-focus-danger: 0 0 0 3px {semantic.intent.danger.layer200}
- switch-focus-info: 0 0 0 3px {semantic.intent.info.layer200}
- switch-focus-neutral: 0 0 0 3px {semantic.intent.neutral.layer200}
- switch-focus-primary: 0 0 0 3px {semantic.focus.ring}
- switch-focus-success: 0 0 0 3px {semantic.intent.success.layer200}
- switch-focus-warning: 0 0 0 3px {semantic.intent.warning.layer200}
- xl: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)

### size
- alert.gap: 8px
- alert.paddingX: 16px
- alert.paddingY: 8px
- avatar.lg: 40px
- avatar.md: 32px
- avatar.sm: 24px
- avatar.xl: 56px
- badge.paddingX.lg: 10px
- badge.paddingX.md: 8px
- badge.paddingX.sm: 6px
- badge.paddingY.lg: 4px
- badge.paddingY.md: 3px
- badge.paddingY.sm: 2px
- checkbox.height.lg: 24px
- checkbox.height.md: 18px
- checkbox.height.sm: 14px
- checkbox.padding.lg: 3px
- checkbox.padding.md: 2px
- checkbox.padding.sm: 2px
- checkbox.width.lg: 24px
- checkbox.width.md: 18px
- checkbox.width.sm: 14px
- height.progressLg: 12px
- height.progressMd: 8px
- height.progressSm: 4px
- height.sliderTrackLg: 8px
- height.sliderTrackMd: 6px
- height.sliderTrackSm: 4px
- height.spinnerLg: 32px
- height.spinnerMd: 24px
- height.spinnerSm: 16px
- height.switchLg: 28px
- height.switchMd: 24px
- height.switchSm: 20px
- icon.lg: 24px
- icon.md: 20px
- icon.sm: 16px
- layout.minHeight.em: 1em
- layout.percent.full: 100%
- menuitem.gap.lg: 12px
- menuitem.gap.md: 10px
- menuitem.gap.sm: 8px
- menuitem.inset.lg: 10px 16px
- menuitem.inset.md: 8px 12px
- menuitem.inset.sm: 6px 12px
- menuitem.minHeight.lg: 44px
- menuitem.minHeight.md: 36px
- menuitem.minHeight.sm: 32px
- minHeight.controlLg: 48px
- minHeight.controlMd: 40px
- minHeight.controlSm: 32px
- modal.padding.lg: 48px
- modal.padding.md: 32px
- modal.padding.sm: 24px
- modal.width.lg: 720px
- modal.width.md: 560px
- modal.width.sm: 400px
- modal.width.xl: 900px
- outline.offset.menuInset: -2px
- outline.offset.tabDefault: 2px
- outline.offset.tabUnderline: -2px
- radio.height.lg: 24px
- radio.height.md: 20px
- radio.height.sm: 16px
- radio.width.lg: 24px
- radio.width.md: 20px
- radio.width.sm: 16px
- select.chevronInset.lg: 36px
- select.chevronInset.md: 32px
- select.chevronInset.sm: 28px
- select.paddingX.lg: 16px
- select.paddingX.md: 12px
- select.paddingX.sm: 10px
- select.paddingY.lg: 12px
- select.paddingY.md: 8px
- select.paddingY.sm: 6px
- tab.inset.lg: 10px 20px
- tab.inset.md: 8px 16px
- tab.inset.sm: 6px 12px
- textarea.minHeight.lg: 120px
- textarea.minHeight.md: 80px
- textarea.minHeight.sm: 60px
- toggle.gap.lg: 10px
- toggle.gap.md: 8px
- toggle.gap.sm: 6px
- toggle.inset.lg: 10px 20px
- toggle.inset.md: 8px 16px
- toggle.inset.sm: 6px 12px
- tooltip.maxWidth: 240px
- tooltip.paddingX: 8px
- tooltip.paddingY: 4px
- width.sliderLg: 280px
- width.sliderMd: 200px
- width.sliderSm: 150px
- width.spinnerLg: 32px
- width.spinnerMd: 24px
- width.spinnerSm: 16px
- width.switchLg: 52px
- width.switchMd: 44px
- width.switchSm: 36px

### spacing
- 2xl: 48px
- 3xl: 64px
- lg: 24px
- md: 16px
- md-sm: 12px
- none: 0
- sm: 8px
- xl: 32px
- xs: 4px

### typography
- fontsize-base: 16px
- fontsize-lg: 18px
- fontsize-sm: 14px
- fontweight-bold: 700
- fontweight-medium: 500
- fontweight-normal: 400

## Semantic Tokens

- action.primary.background: {base.color.primary.500}
- action.primary.border: {base.color.primary.500}
- action.primary.hover: {base.color.primary.600}
- action.primary.pressed: {base.color.primary.700}
- action.primary.text: {base.color.white}
- black: {color.black}
- border.default: {base.color.neutral.200}
- border.focus: {base.color.primary.500}
- border.strong: {base.color.neutral.400}
- border.subtle: {base.color.neutral.100}
- danger.500: {base.color.danger.500}
- danger.600: {color.red.600}
- focus.ring: {base.color.primary.500}
- focus.ringOffset: {base.color.white}
- fontsize.base: {base.typography.fontsize.base}
- fontsize.lg: {base.typography.fontsize.lg}
- fontsize.sm: {base.typography.fontsize.sm}
- fontweight.bold: {base.typography.fontweight.bold}
- fontweight.medium: {base.typography.fontweight.medium}
- fontweight.normal: {base.typography.fontweight.normal}
- gray.100: {base.color.gray.100}
- gray.300: {base.color.gray.300}
- gray.900: {base.color.gray.900}
- intent.danger.layer100: {base.color.danger.100}
- intent.danger.layer200: {base.color.danger.200}
- intent.danger.layer300: {base.color.danger.300}
- intent.danger.layer400: {base.color.danger.400}
- intent.danger.layer50: {base.color.danger.50}
- intent.danger.layer500: {base.color.danger.500}
- intent.danger.layer600: {base.color.danger.600}
- intent.danger.layer700: {base.color.danger.700}
- intent.danger.layer800: {base.color.danger.800}
- intent.danger.layer900: {base.color.danger.900}
- intent.danger.layer950: {base.color.danger.950}
- intent.info.layer100: {base.color.info.100}
- intent.info.layer200: {base.color.info.200}
- intent.info.layer300: {base.color.info.300}
- intent.info.layer400: {base.color.info.400}
- intent.info.layer50: {base.color.info.50}
- intent.info.layer500: {base.color.info.500}
- intent.info.layer600: {base.color.info.600}
- intent.info.layer700: {base.color.info.700}
- intent.info.layer800: {base.color.info.800}
- intent.info.layer900: {base.color.info.900}
- intent.info.layer950: {base.color.info.950}
- intent.neutral.layer100: {base.color.neutral.100}
- intent.neutral.layer200: {base.color.neutral.200}
- intent.neutral.layer300: {base.color.neutral.300}
- intent.neutral.layer400: {base.color.neutral.400}
- intent.neutral.layer50: {base.color.neutral.50}
- intent.neutral.layer500: {base.color.neutral.500}
- intent.neutral.layer600: {base.color.neutral.600}
- intent.neutral.layer700: {base.color.neutral.700}
- intent.neutral.layer800: {base.color.neutral.800}
- intent.neutral.layer900: {base.color.neutral.900}
- intent.neutral.layer950: {base.color.neutral.950}
- intent.primary.layer100: {base.color.primary.100}
- intent.primary.layer200: {base.color.primary.200}
- intent.primary.layer300: {base.color.primary.300}
- intent.primary.layer400: {base.color.primary.400}
- intent.primary.layer50: {base.color.primary.50}
- intent.primary.layer500: {base.color.primary.500}
- intent.primary.layer600: {base.color.primary.600}
- intent.primary.layer700: {base.color.primary.700}
- intent.primary.layer800: {base.color.primary.800}
- intent.primary.layer900: {base.color.primary.900}
- intent.primary.layer950: {base.color.primary.950}
- intent.red.layer100: {base.color.red.100}
- intent.red.layer200: {base.color.red.200}
- intent.red.layer300: {base.color.red.300}
- intent.red.layer400: {base.color.red.400}
- intent.red.layer50: {base.color.red.50}
- intent.red.layer500: {base.color.red.500}
- intent.red.layer600: {base.color.red.600}
- intent.red.layer700: {base.color.red.700}
- intent.red.layer800: {base.color.red.800}
- intent.red.layer900: {base.color.red.900}
- intent.red.layer950: {base.color.red.950}
- intent.success.layer100: {base.color.success.100}
- intent.success.layer200: {base.color.success.200}
- intent.success.layer300: {base.color.success.300}
- intent.success.layer400: {base.color.success.400}
- intent.success.layer50: {base.color.success.50}
- intent.success.layer500: {base.color.success.500}
- intent.success.layer600: {base.color.success.600}
- intent.success.layer700: {base.color.success.700}
- intent.success.layer800: {base.color.success.800}
- intent.success.layer900: {base.color.success.900}
- intent.success.layer950: {base.color.success.950}
- intent.warning.layer100: {base.color.warning.100}
- intent.warning.layer200: {base.color.warning.200}
- intent.warning.layer300: {base.color.warning.300}
- intent.warning.layer400: {base.color.warning.400}
- intent.warning.layer50: {base.color.warning.50}
- intent.warning.layer500: {base.color.warning.500}
- intent.warning.layer600: {base.color.warning.600}
- intent.warning.layer700: {base.color.warning.700}
- intent.warning.layer800: {base.color.warning.800}
- intent.warning.layer900: {base.color.warning.900}
- intent.warning.layer950: {base.color.warning.950}
- lg: {base.spacing.lg}
- lg: {base.borderRadius.lg}
- lg: {base.shadow.lg}
- md: {base.spacing.md}
- md: {base.shadow.md}
- md: {base.borderRadius.md}
- neutral.100: {color.gray.100}
- neutral.300: {color.gray.300}
- neutral.900: {color.gray.900}
- none: {base.shadow.none}
- primary.100: {base.color.primary.100}
- primary.50: {base.color.primary.50}
- primary.500: {base.color.primary.500}
- primary.600: {base.color.primary.600}
- primary.700: {base.color.primary.700}
- primary.900: {base.color.primary.900}
- sm: {base.borderRadius.sm}
- sm: {base.spacing.sm}
- sm: {base.shadow.sm}
- status.danger: {base.color.danger.500}
- status.info: {base.color.info.500}
- status.success: {base.color.success.500}
- status.warning: {base.color.warning.500}
- success.500: {base.color.success.500}
- surface.background: {base.color.neutral.50}
- surface.card: {base.color.white}
- surface.elevated: {base.color.white}
- surface.inverse: {base.color.neutral.900}
- text.disabled: {base.color.neutral.400}
- text.inverse: {base.color.white}
- text.primary: {base.color.neutral.900}
- text.secondary: {base.color.neutral.600}
- text.tertiary: {base.color.neutral.500}
- white: {base.color.white}
- xl: {base.borderRadius.xl}

## Component Variants

Each component accepts variant props. The prop name is listed below (may differ from internal DB name).

### Alert
- appearance: soft, solid, outline
- intent: info, danger, neutral, success, warning
- shape: sharp, rounded

### Avatar
- badge: busy, none, online, offline
- color: default, neutral, primary
- content: image, initials
- group: none, count, group
- shape: sharp, circle, rounded
- size: lg, md, sm, xl

### Badge
- variant: soft, solid, outline
- color: info, danger, default, primary, success, warning
- shape: pill, sharp, rounded
- size: lg, md, sm

### Button
- appearance: soft, ghost, solid, outline
- intent: info, danger, primary, success, warning, secondary
- shape: pill, sharp, rounded
- size: lg, md, sm

### Checkbox
- border: none, pill, sharp, rounded
- color: default
- label: none, right
- size: lg, md, sm
- state: checked, default, disabled

### Container
- alignment: end, start, center
- color: card, muted, neutral, primary, secondary, alert-info, alert-error, alert-default, alert-success, alert-warning
- columns: 1, 2, 3, 4
- direction: row, column
- display: flex, block
- elevation: lg, md, sm, xl, none
- padding: lg, md, sm, none
- shape: none, rounded
- size: lg, md, sm, xl, auto, full
- spacing: lg, md, sm, none
- wrap: wrap, nowrap

### Divider
- color: strong, subtle, default
- orientation: vertical, horizontal
- size: thin, thick, medium

### Icon
- color: muted, inherit, primary
- size: lg, md, sm
- state: hide, show

### Image
- aspectRatio: 1/1, 3/2, 4/3, 16/9, auto
- fit: fill, none, cover, contain, scale-down

### Input
- align: left, right, center
- color: default
- elevation: md, sm, none
- shape: pill, square, rounded
- size: lg, sm, default

### Link
- underline: subtle, default
- color: muted, default
- size: default
- weight: medium, normal, semibold

### MenuItem
- color: danger, default
- size: lg, md, sm

### Modal
- color: default
- shape: sharp, rounded
- size: lg, md, sm, xl

### Progress
- color: info, danger, neutral, primary, success, warning
- size: lg, md, sm

### Radio
- border: thin, thick, default
- color: default, neutral, primary
- size: lg, md, sm

### Select
- appearance: ghost, filled, outline
- color: muted, default, primary
- shape: pill, sharp, rounded
- size: lg, md, sm
- state: default, invalid, required

### Skeleton
- animation: none, wave, pulse
- color: dark, light, medium
- size: lg, md, sm, xl, xs
- shape: text, circle, rectangle

### Slider
- color: info, danger, neutral, primary, success, warning
- mode: range, single
- orientation: vertical, horizontal
- size: lg, md, sm

### Spinner
- color: info, white, danger, neutral, primary, success, warning, secondary
- size: lg, md, sm

### Switch
- color: info, danger, neutral, primary, success, warning
- size: lg, md, sm

### Tab
- appearance: line, pills, contained
- color: default, neutral, primary
- icon: none, leading
- orientation: vertical, horizontal
- size: lg, md, sm
- state: hover, default, disabled, selected

### Text
- align: left, right, center
- color: muted, default, primary, success, destructive
- size: lg, sm, xl, xs, 2xl, base
- weight: bold, medium, normal, semibold

### Textarea
- color: muted, default, primary
- shape: pill, sharp, rounded
- size: lg, md, sm

### Toast
- position: top-left, top-right, top-center, bottom-left, bottom-right, bottom-center
- size: lg, md, sm
- variant: info, error, default, success, warning

### ToggleButton
- appearance: ghost, filled, outline
- color: danger, default, primary, success, warning
- size: lg, md, sm

### Tooltip
- color: dark, light, danger, primary
- shape: sharp, rounded
- size: lg, md, sm
