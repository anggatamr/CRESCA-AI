<design-context>
---
version: 1.2
name: cresca-design-system
description: A high-precision, mission-critical interface for CRESCA AI (Autonomous Demographic Sentinel & Spatiotemporal Nutrition Logistics Protocol). Combines authoritative enterprise data intelligence with an interactive Neo-Brutalist 3-panel autonomous workflow simulator. Built React-first (Tailwind CSS + shadcn/ui token conventions), powered by Public Sans typography, Phosphor bold/fill custom-outlined icons, and Google Maps JavaScript API for interactive geospatial epidemiologic risk analysis.
changelog:
  - "1.2: Fixed WCAG contrast failure on pink badge text (2.98:1 → 6.64:1). Separated tier-high from tier-moderate by hue + added non-color pattern differentiation. Declared explicit active/press state tokens for every brutalist component, not just icon badges. Corrected font-stack claims (Public Sans is the only font that actually renders cross-platform; SF Pro is a no-op fallback outside Apple devices — see Typography section)."
---

## Overview

**CRESCA AI** (*Autonomous Demographic Sentinel & Spatiotemporal Nutrition Logistics Protocol*) is a dual-tier design system engineered for high-stakes autonomous decision intelligence and public health intervention.

The design language reconciles two vital operational requirements:
1. **The Executive Sentinel & Audit Tier:** Clean, authoritative typography using **Public Sans**, razor-sharp contrast, and minimalist structural geometry designed for government health officers, epidemiologists, and supply-chain directors.
2. **The Interactive Neo-Brutalist Autonomous Flow (3-Panel Live Showcase / Simulator):** An unpolished, high-energy, raw neo-brutalist interaction surface demonstrating CRESCA's autonomous loop: **Onboarding / Ingestion Feed** → **AI Pipeline & Reasoning Engine (Gemma 2 + Gemini 3.5)** → **PO Generation & Action Dispatch**.

This system is implemented **React-first**: components are composed from shadcn/ui primitives (Radix UI + Tailwind CSS), with design tokens expressed as CSS variables so both the Enterprise tier and the Neo-Brutalist tier can co-exist in the same component tree without token collisions.

### Key System Characteristics
- **Typography:** **Public Sans** is the only typeface actually rendered on non-Apple devices and is therefore the system of record. See the *Typography Reality Check* section below before citing "SF Pro" anywhere in the README, video narration, or judge-facing docs.
- **Iconography:** **Phosphor Icons (`bold` & `fill` weight)** encased in custom neo-brutalist wrappers (`3px solid #0A0A0A`, `3px 3px 0px #0A0A0A` hard drop shadow, 0px border-radius) for an ultra-solid, tactile sticker aesthetic. No emoji icons anywhere (per accessibility/consistency rules).
- **Geospatial Mapping:** **Google Maps Platform JavaScript API** (`@vis.gl/react-google-maps`) leveraging Google Cloud Credits ($150) for high-performance vector tiles, risk polygons, and interactive hospital/Posyandu markers.
- **Neo-Brutalist Showcase Palette:** Lavender/Purple (`#B8A6E8`) base canvas, Acid Lime-Green (`#D4F547`) for CTAs and highlights, Hot Pink (`#F55FA3`) for critical urgency markers, Amber-Orange (`#F2762E`) for high-urgency markers (now hue-separated from moderate-tier yellow — see *Risk Tier Differentiation*), Pure Black (`#0A0A0A`) for heavy 3–5px borders and hard drop-shadows (6–8px offset, 0 blur), Cream (`#FFFDF7`) for card surfaces.
- **Zero Soft Elevation in Neo-Brutalist Panels:** Hard black offset shadows (`8px 8px 0px #0A0A0A`), 0px border-radius, asymmetric tilts (2–4°), and a fully declared press-in state on every interactive brutalist element (see *Interaction States*).
- **All text-on-color pairings in this document are WCAG-checked.** Ratios are listed inline next to each token so no combination ships unverified.

---

## Colors

### 1. Enterprise Sentinel & Audit Palette

| Token | Hex | Use | Contrast vs. paired text |
|---|---|---|---|
| `{colors.primary}` — Action Blue | `#0066cc` | Interactive triggers, primary protocol initiations, focus rings | 5.57:1 white-on-blue text (AA pass) |
| `{colors.primary-focus}` | `#0071e3` | Keyboard accessibility focus rings, active system markers | — (ring only, not a text surface) |
| `{colors.primary-on-dark}` | `#2997ff` | Inline indicators/links on dark telemetry surfaces | 5.1:1+ vs. `surface-tile-1` |
| `{colors.canvas}` | `#ffffff` | Base background for reports, tables, audit logs | 15.46:1 vs. `{colors.ink}` |
| `{colors.canvas-parchment}` | `#f5f5f7` | Neutral section breaks, sidebar panels | 15.46:1 vs. `{colors.ink}` |
| `{colors.surface-tile-1}` | `#1e1e24` | Primary dark background for live geospatial maps, model monitors | 12.7:1 vs. white text |
| `{colors.surface-tile-2}` | `#27272a` | Secondary container elevation | 11.9:1 vs. white text |
| `{colors.surface-tile-3}` | `#18181b` | Terminal/console background | 13.4:1 vs. white text |
| `{colors.ink}` | `#1d1d1f` | Primary readable text tone | 15.46:1 vs. white |

### 2. Neo-Brutalist Interactive Spectrum

Used for the 3-Section Agent Workflow Showcase / Live Demo Simulator. **Rule for this tier: every badge and card uses `{colors.brutalist-black}` as text color — never white — because every brutalist background swatch below is a light/mid-tone color where white text fails contrast.** This is a hard rule, not per-component discretion (it's what fixed the v1.1 badge bug — see *Fix Log*).

| Token | Hex | Use | Contrast w/ black text |
|---|---|---|---|
| `{colors.brutalist-bg}` — Lavender Canvas | `#B8A6E8` | High-energy base canvas for the interactive agent section | 9.11:1 |
| `{colors.brutalist-lime}` — Acid Lime-Green | `#D4F547` | High-contrast marker strokes, autonomous action CTAs, verified checkmarks | 15.98:1 |
| `{colors.brutalist-pink}` — Hot Pink/Magenta | `#F55FA3` | Critical-tier district tags, anomaly alerts | 6.64:1 |
| `{colors.brutalist-amber}` — **NEW** Amber-Orange | `#F2762E` | High-tier district tags (distinct from critical pink and moderate yellow) | 6.98:1 |
| `{colors.brutalist-card}` — Off-White/Cream | `#FFFDF7` | Sharp high-contrast card faces | 19.8:1 |
| `{colors.brutalist-black}` | `#0A0A0A` | 3–5px outlines, hard shadows, chunky display typography, **all badge/card text** | — |

### 3. Risk Classification Tiers (Choropleth & Badges) — Revised

> **Fix Log:** v1.1 used `tier-high: #FF9F43` and `tier-moderate: #FFD93D`, which sit only ~19° apart in hue and produce a contrast ratio of just **1.48:1 against each other** — functionally indistinguishable at a glance, especially at small badge sizes or on a compressed video export. This violates the `color-not-only` / distinguishable-tiers principle. v1.2 shifts `tier-high` to a deeper amber-orange (`#F2762E`), widening the hue gap to ~26° and the mutual contrast ratio to **2.06:1**, and — more importantly — adds a **non-color differentiator** (icon + pattern) so no one is reading risk tiers off hue alone.

| Tier | Color Token | Hex | Icon (Phosphor, `weight="fill"`) | Badge Pattern |
|---|---|---|---|---|
| **Critical** | `tier-critical` | `#F55FA3` | `<WarningOctagon />` | Solid fill + diagonal hazard stripe |
| **High** | `tier-high` (was `#FF9F43`, now amber) | `#F2762E` | `<WarningCircle />` | Solid fill, no stripe |
| **Moderate** | `tier-moderate` | `#FFD93D` | `<Info />` | Solid fill + dotted border |
| **Low** | `tier-low` | `#D4F547` | `<CheckCircle />` | Solid fill, thin border only |

This means every district marker, badge, and legend entry renders **shape + icon + color together**, so the CDVI choropleth map remains legible for colorblind judges and in low-quality video compression alike — directly satisfying the `color-not-only` and `pattern-texture` accessibility rules.

### 4. Ink & Monochromatic Typography

| Token | Hex |
|---|---|
| `{colors.body}` | `#1d1d1f` |
| `{colors.body-on-dark}` | `#ffffff` |
| `{colors.body-muted}` | `#cccccc` |
| `{colors.ink-muted-80}` | `#333333` |
| `{colors.ink-muted-48}` | `#7a7a7a` |

> Note: `body-on-dark` (`#ffffff`) is reserved **exclusively** for text on `surface-tile-*` / `surface-black` dark surfaces (12:1+ contrast). It must never be used on Neo-Brutalist badge backgrounds — see the hard rule in section 2.

### 5. Surfaces & Canvas

| Token | Hex |
|---|---|
| `{colors.divider-soft}` | `#f0f0f0` |
| `{colors.hairline}` | `#e0e0e0` |
| `{colors.border-brutalist}` | `#0A0A0A` |
| `{colors.surface-pearl}` | `#fafafc` |
| `{colors.surface-black}` | `#000000` |
| `{colors.surface-chip-translucent}` | `#d2d2d7` |
| `{colors.on-primary}` | `#ffffff` |
| `{colors.on-dark}` | `#ffffff` |

---

## Typography — Reality Check & Public Sans Specification

**Public Sans is the system of record.** The v1.1 doc listed `"Public Sans", "SF Pro Display", "SF Pro Text"` as a co-equal stack. Technically this is a fallback chain, not a multi-font system: `-apple-system` / `SF Pro` only resolves on Apple hardware, and since `Public Sans` is loaded first via a real web-font (Google Fonts) it will render everywhere, including macOS/iOS. **In practice 100% of users — judges included — see Public Sans, not SF Pro.** Keep the fallback in code (it's harmless), but do not claim "SF Pro" as a design decision in the README, the technical blog post, or the video narration — it never actually paints a pixel for anyone outside a no-webfont edge case.

```
Font Stacks:
- Display & UI: "Public Sans", -apple-system, BlinkMacSystemFont, sans-serif   /* fallback only, not a feature */
- Telemetry & Logs: "JetBrains Mono", "Fira Code", monospace
```

Load Public Sans via `next/font/google` or a `<link>` to Google Fonts with `font-display: swap` so text is never invisible during load (`font-loading` rule).

### Typographic Hierarchy

| Token | Size | Weight | Line Height | Letter Spacing | Use Case |
|---|---|---|---|---|---|
| `{typography.hero-display}` | 56px | 800 (ExtraBold) | 1.05 | -0.03em | Primary Hero & Neo-Brutalist Headlines |
| `{typography.display-lg}` | 40px | 700 (Bold) | 1.10 | -0.02em | Section Headlines & Major Module Headers |
| `{typography.display-md}` | 34px | 700 (Bold) | 1.25 | -0.02em | Metric Cards & Modal Titles |
| `{typography.lead}` | 28px | 400 (Regular) | 1.25 | -0.01em | Sub-headlines & Lead Statements |
| `{typography.lead-airy}` | 24px | 300 (Light) | 1.50 | 0 | Executive Summaries & PRD Quotes |
| `{typography.tagline}` | 21px | 600 (SemiBold) | 1.20 | -0.01em | Sub-navigation & Flow Section Labels |
| `{typography.body-strong}` | 17px | 600 (SemiBold) | 1.30 | -0.01em | Bold Data Points & Table Headers |
| `{typography.body}` | 17px | 400 (Regular) | 1.50 | -0.01em | Default Body Copy & Protocol Analysis |
| `{typography.dense-link}` | 17px | 400 (Regular) | 2.20 | 0 | Footer & Navigation Index Stacks |
| `{typography.caption}` | 14px | 400 (Regular) | 1.40 | 0 | Microcopy, Timestamps, Sub-labels |
| `{typography.caption-strong}` | 14px | 600 (SemiBold) | 1.30 | 0 | Status Badges, KPI Indicators |
| `{typography.button-large}` | 18px | 700 (Bold) | 1.00 | 0 | Primary Action Buttons & Brutalist CTAs |
| `{typography.button-utility}` | 14px | 600 (SemiBold) | 1.20 | 0 | Utility Buttons & Toolbar Actions |
| `{typography.code-mono}` | 14px | 600 (SemiBold) | 1.40 | 0 | Model Logs, Geohash IDs, PII Scrubbing |
| `{typography.fine-print}` | 12px | 400 (Regular) | 1.20 | 0 | Audit Checksums, Regulatory Footers |
| `{typography.micro-legal}` | 10px | 400 (Regular) | 1.30 | 0 | Security Disclaimers & Model Versioning |
| `{typography.nav-link}` | 13px | 600 (SemiBold) | 1.00 | 0 | Main Header Navigation Items |

All body text sits at 17px (above the 16px minimum floor for mobile auto-zoom avoidance). No token in this system goes below 12px for anything but legal fine print, matching the `readable-font-size` rule.

---

## Rounded / Spacing / Shadows

```yaml
rounded:
  none: 0px      # Neo-Brutalist tier only
  xs: 4px
  sm: 6px
  md: 10px
  lg: 16px
  pill: 9999px   # Enterprise tier buttons
  full: 9999px

spacing:          # 4/8pt rhythm, per spacing-scale rule
  xxs: 4px
  xs: 8px
  sm: 12px
  md: 16px
  lg: 24px
  xl: 32px
  xxl: 48px
  section: 80px

shadows:
  brutalist-icon: "3px 3px 0px #0A0A0A"
  brutalist-sm: "4px 4px 0px #0A0A0A"
  brutalist-md: "6px 6px 0px #0A0A0A"
  brutalist-lg: "8px 8px 0px #0A0A0A"
  brutalist-active: "0px 0px 0px #0A0A0A"   # only meaningful when paired with the translate() in Interaction States below
```

---

## Interaction States — Declared for Every Brutalist Component (Fix Log)

> **v1.1 gap:** only the icon badge had an explicit hover/active CSS example. Every other brutalist component (`brutalist-hero-box`, `brutalist-process-card`, `brutalist-action-dispatch-card`, `brutalist-button-cta`, `brutalist-progress-bar`) referenced `shadows.brutalist-active` in spirit but never paired it with a `transform`, so the "pressed" illusion wasn't guaranteed to actually fire in implementation. v1.2 declares the full press-state contract once, as a shared Tailwind utility pattern, and every component below inherits it explicitly.

**Shared press-state contract** (applies to all interactive brutalist elements — buttons, cards that act as triggers, badges that act as toggles):

```css
/* Base state */
.brutalist-interactive {
  border: 3px solid #0A0A0A;
  box-shadow: 6px 6px 0px #0A0A0A;
  transition: transform 150ms ease-out, box-shadow 150ms ease-out;
  cursor: pointer;
}

/* Hover: lift slightly, shadow grows — signals "liftable" before commit */
.brutalist-interactive:hover {
  transform: translate(-1px, -1px);
  box-shadow: 8px 8px 0px #0A0A0A;
}

/* Active/press: the component physically moves into its own shadow */
.brutalist-interactive:active,
.brutalist-interactive[data-state="pressed"] {
  transform: translate(6px, 6px);
  box-shadow: 0px 0px 0px #0A0A0A; /* shadows.brutalist-active — now correctly paired */
}

/* Focus-visible: required for keyboard users, brutalist tier must not lose this */
.brutalist-interactive:focus-visible {
  outline: 3px solid #0066cc;
  outline-offset: 2px;
}

/* Disabled: no press illusion, reduced emphasis, no pointer */
.brutalist-interactive:disabled,
.brutalist-interactive[aria-disabled="true"] {
  transform: none;
  box-shadow: 4px 4px 0px #0A0A0A;
  opacity: 0.5;
  cursor: not-allowed;
}
```

In React/Tailwind (shadcn/ui composition pattern), this becomes a reusable class applied via `cn()`:

```tsx
// components/ui/brutalist-button.tsx
import { cn } from "@/lib/utils"

export function BrutalistButton({ className, ...props }: React.ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      className={cn(
        "border-[3px] border-[#0A0A0A] bg-[#D4F547] font-bold text-[#0A0A0A]",
        "shadow-[6px_6px_0px_#0A0A0A] transition-transform duration-150 ease-out",
        "hover:-translate-x-px hover:-translate-y-px hover:shadow-[8px_8px_0px_#0A0A0A]",
        "active:translate-x-[6px] active:translate-y-[6px] active:shadow-[0px_0px_0px_#0A0A0A]",
        "focus-visible:outline focus-visible:outline-[3px] focus-visible:outline-[#0066cc] focus-visible:outline-offset-2",
        "disabled:opacity-50 disabled:shadow-[4px_4px_0px_#0A0A0A] disabled:translate-x-0 disabled:translate-y-0 disabled:cursor-not-allowed",
        className
      )}
      {...props}
    />
  )
}
```

**Per-component application:**

| Component | Idle shadow | Press-state behavior |
|---|---|---|
| `brutalist-button-cta` | `brutalist-md` (6px) | Presses per shared contract above |
| `brutalist-hero-box` (non-interactive) | `brutalist-lg` (8px), fixed | No press state — it's a display panel, not a control; do not attach `:active` |
| `brutalist-process-card` | `brutalist-lg` (8px) | Only if the card is clickable (e.g. "view step detail"); otherwise static like hero-box |
| `brutalist-action-dispatch-card` | `brutalist-lg` (8px) | Presses per shared contract if it triggers navigation/expansion |
| `brutalist-badge-lime` / new `brutalist-badge-amber` / `brutalist-badge-pink` | `none` (badges are flat, not shadowed) | Only apply press-state if the badge is a toggle/filter chip; static informational badges get no hover/active styling at all |
| `brutalist-icon-box` / `brutalist-icon-box-pink` | `brutalist-icon` (3px) | Presses per shared contract, scaled down (2px hover offset, not 6px, since the box is smaller) |

This distinction matters: a common brutalism mistake is bolting hover/press states onto purely informational elements (like a static risk badge), which makes static content look falsely interactive. Only attach `.brutalist-interactive` to elements that actually do something on click.

---

## Component Tokens (shadcn/ui composition reference)

```yaml
components:
  # Enterprise CRESCA Components
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-strong}"
    rounded: "{rounded.pill}"
    padding: 11px 24px
  button-primary-focus:
    backgroundColor: "{colors.primary-focus}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.pill}"
  button-secondary-pill:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.primary}"
    typography: "{typography.body-strong}"
    rounded: "{rounded.pill}"
    padding: 11px 24px
  button-dark-utility:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.on-dark}"
    typography: "{typography.button-utility}"
    rounded: "{rounded.sm}"
    padding: 8px 16px
  global-nav:
    backgroundColor: "{colors.surface-black}"
    textColor: "{colors.on-dark}"
    typography: "{typography.nav-link}"
    height: 48px
  sub-nav-frosted:
    backgroundColor: "{colors.canvas-parchment}"
    textColor: "{colors.ink}"
    typography: "{typography.tagline}"
    height: 54px

  # Phosphor Icon Brutalist Custom Wrappers
  brutalist-icon-box:
    backgroundColor: "{colors.brutalist-lime}"
    textColor: "{colors.brutalist-black}"
    border: "3px solid {colors.brutalist-black}"
    shadow: "{shadows.brutalist-icon}"
    rounded: "{rounded.none}"
    padding: "8px"
    interactive: true   # inherits .brutalist-interactive, scaled offsets
  brutalist-icon-box-pink:
    backgroundColor: "{colors.brutalist-pink}"
    textColor: "{colors.brutalist-black}"   # FIXED — was body-on-dark (white), now black per hard rule
    border: "3px solid {colors.brutalist-black}"
    shadow: "{shadows.brutalist-icon}"
    rounded: "{rounded.none}"
    padding: "8px"
    interactive: true

  # Google Maps Interactive Container
  google-maps-sentinel-frame:
    border: "4px solid {colors.brutalist-black}"
    shadow: "{shadows.brutalist-lg}"
    rounded: "{rounded.none}"
    height: "560px"
    backgroundColor: "{colors.surface-tile-1}"

  # Neo-Brutalist Interactive 3-Panel Simulator Components
  brutalist-hero-box:
    backgroundColor: "{colors.brutalist-card}"
    textColor: "{colors.brutalist-black}"
    border: "4px solid {colors.brutalist-black}"
    shadow: "{shadows.brutalist-lg}"
    rounded: "{rounded.none}"
    padding: 32px
    rotation: "-2deg"
    interactive: false   # display panel only
  brutalist-button-cta:
    backgroundColor: "{colors.brutalist-lime}"
    textColor: "{colors.brutalist-black}"
    typography: "{typography.button-large}"
    border: "3px solid {colors.brutalist-black}"
    shadow: "{shadows.brutalist-md}"
    rounded: "{rounded.none}"
    padding: 14px 28px
    interactive: true
  brutalist-badge-lime:
    backgroundColor: "{colors.brutalist-lime}"
    textColor: "{colors.brutalist-black}"
    typography: "{typography.code-mono}"
    border: "2px solid {colors.brutalist-black}"
    rounded: "{rounded.none}"
    padding: 4px 10px
    icon: "CheckCircle"
    interactive: false   # static tier badge by default
  brutalist-badge-amber:   # NEW — replaces ambiguous "tier-high = orange, tier-moderate = yellow" collision
    backgroundColor: "{colors.brutalist-amber}"
    textColor: "{colors.brutalist-black}"
    typography: "{typography.code-mono}"
    border: "2px solid {colors.brutalist-black}"
    rounded: "{rounded.none}"
    padding: 4px 10px
    icon: "WarningCircle"
    interactive: false
  brutalist-badge-pink:
    backgroundColor: "{colors.brutalist-pink}"
    textColor: "{colors.brutalist-black}"   # FIXED — was body-on-dark (white, 2.98:1 fail), now black (6.64:1 pass)
    typography: "{typography.code-mono}"
    border: "2px solid {colors.brutalist-black}"
    rounded: "{rounded.none}"
    padding: 4px 10px
    icon: "WarningOctagon"
    pattern: "diagonal-hazard-stripe"
    interactive: false
  brutalist-process-card:
    backgroundColor: "{colors.brutalist-card}"
    textColor: "{colors.brutalist-black}"
    border: "4px solid {colors.brutalist-black}"
    shadow: "{shadows.brutalist-lg}"
    rounded: "{rounded.none}"
    padding: 32px
    rotation: "1.5deg"
    interactive: false   # set true only if used as an expandable step
  brutalist-progress-bar:
    backgroundColor: "{colors.canvas}"
    border: "3px solid {colors.brutalist-black}"
    height: 24px
    fillColor: "{colors.brutalist-lime}"
    interactive: false
  brutalist-action-dispatch-card:
    backgroundColor: "{colors.brutalist-card}"
    textColor: "{colors.brutalist-black}"
    border: "4px solid {colors.brutalist-black}"
    shadow: "{shadows.brutalist-lg}"
    rounded: "{rounded.none}"
    padding: 32px
    rotation: "-1deg"
    interactive: false
  brutalist-dispatch-banner:
    backgroundColor: "{colors.brutalist-lime}"
    textColor: "{colors.brutalist-black}"
    border: "4px solid {colors.brutalist-black}"
    shadow: "{shadows.brutalist-md}"
    rounded: "{rounded.none}"
    padding: 24px
    interactive: false
```

---

## Iconography: Phosphor Icons (Custom Brutalist Outlines)

All UI glyphs use **Phosphor Icons** (`@phosphor-icons/react`, `weight="bold"` or `weight="fill"`). No emoji icons anywhere in the system — emoji fail the `no-emoji-icons` / cross-platform consistency rule and cannot be themed via design tokens.

```css
/* Custom CSS Wrapper for Neo-Brutalist Thick Theme (static, non-interactive badge use) */
.cresca-icon-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-brutalist-lime);
  border: 3px solid #0A0A0A;
  box-shadow: 3px 3px 0px #0A0A0A;
  padding: 8px;
  border-radius: 0px;
  color: #0A0A0A; /* always black text/icon on brutalist badges */
}

/* Interactive variant composes .brutalist-interactive from Interaction States section */
.cresca-icon-badge.is-interactive {
  cursor: pointer;
  transition: transform 150ms ease-out, box-shadow 150ms ease-out;
}
.cresca-icon-badge.is-interactive:hover {
  transform: translate(-1px, -1px);
  box-shadow: 4px 4px 0px #0A0A0A;
}
.cresca-icon-badge.is-interactive:active {
  transform: translate(2px, 2px);
  box-shadow: 0px 0px 0px #0A0A0A;
}

.cresca-icon-badge-pink {
  background-color: var(--color-brutalist-pink);
  border: 3px solid #0A0A0A;
  box-shadow: 3px 3px 0px #0A0A0A;
  color: #0A0A0A; /* FIXED — was #ffffff, failed contrast at 2.98:1 */
}

.cresca-icon-badge-amber {
  background-color: var(--color-brutalist-amber); /* #F2762E — new token, replaces ambiguous orange */
  border: 3px solid #0A0A0A;
  box-shadow: 3px 3px 0px #0A0A0A;
  color: #0A0A0A;
}
```

### Essential Phosphor Icons Mapping:
- **Sentinel & Watchdog:** `<Robot weight="fill" />`, `<ShieldCheck weight="bold" />`
- **Ingestion & Data:** `<Database weight="bold" />`, `<FileArrowDown weight="bold" />`
- **Mathematical Pipeline:** `<ChartBar weight="bold" />`, `<Graph weight="bold" />`
- **Strategic AI Reasoning:** `<Brain weight="fill" />`, `<Sparkle weight="fill" />`
- **Logistics & PO Dispatch:** `<Truck weight="fill" />`, `<FilePdf weight="fill" />`, `<CheckCircle weight="fill" />`
- **Geospatial Map Controls:** `<MapPin weight="fill" />`, `<NavigationArrow weight="bold" />`
- **Risk Tier Icons (NEW, mandatory alongside color):** `<WarningOctagon weight="fill" />` (Critical), `<WarningCircle weight="fill" />` (High), `<Info weight="fill" />` (Moderate), `<CheckCircle weight="fill" />` (Low)

---

## Interactive Geospatial Engine: Google Maps Platform API

CRESCA utilizes the **Google Maps JavaScript API** (`@vis.gl/react-google-maps`) under the $150 Google Cloud Credits program, wired into a React component tree.

### Key Capabilities & Map Customizations:
1. **Choropleth Multi-District Overlay:** GeoJSON layers rendering the 21 districts of North Sumatra (Medan Belawan, Medan Labuhan, Deli Serdang, etc.) colored dynamically by their real-time **Composite Demographic Vulnerability Index (CDVI)**, using the four-tier palette above (pink/amber/yellow/lime) — each tier also renders its assigned icon glyph in the InfoWindow, not color alone.
2. **Neo-Brutalist Pin Markers:** Custom HTML marker overlays (`OverlayView` in `@vis.gl/react-google-maps`) using Phosphor `<MapPin weight="fill" />` wrapped in thick-bordered boxes (`3px solid #0A0A0A`, hard drop shadow). Markers are interactive (`.brutalist-interactive`) since clicking opens the InfoWindow.
3. **Interactive District InfoWindow:** Upon clicking a district polygon, renders the Poisson 90-day incidence projection ($Y_i$), sanitation index, poverty rate, allocated F-75 formula quantity, and the tier badge (color + icon + pattern).
4. **Custom Styling Theme:** High-contrast subtle dark/light mode that prevents distraction from epidemiological cluster boundaries. Map tiles never rely on default Google styling — always pass a custom `styles` array so brutalist borders remain the sharpest element on screen.

---

## The CRESCA 3-Section Autonomous Flow (Neo-Brutalist Experience)

Integrated within the landing page / interactive simulator, CRESCA features a **single-scroll 3-panel autonomous workflow** executed in raw Neo-Brutalism. This interactive section showcases how CRESCA operates 24/7 without manual intervention.

### Layout Rule (avoiding the "everything centered" AI-slop trap)
Per `web-artifacts-builder` guidance against generic centered layouts: each of the 3 sections uses a **different horizontal anchor**, not a repeated center-stack:
- **Section 1** anchors content-left with the hero box offset toward the top-left, tilted `-2°`, leaving asymmetric negative space top-right for the ingestion feed list.
- **Section 2** anchors center-right, process card tilted `+1.5°`, with the progress bar spanning full-width beneath it (breaks the "everything is a centered card" pattern).
- **Section 3** anchors content full-width with the dispatch banner as a distinct horizontal band (`tilted -1°`) rather than another centered card, so the three sections read as visually distinct rhythms while scrolling, not three repeats of the same layout.

### Aesthetic Rules for the Interactive Section
- **Sharp Corners Only:** `border-radius: 0px` across all buttons, cards, tags, and progress bars.
- **Thick Outlines:** `3px` to `5px` solid `#0A0A0A` around every container.
- **Hard Drop Shadows:** `box-shadow: 6px 6px 0px #0A0A0A` or `8px 8px 0px #0A0A0A` with 0 blur. No gradients, no blur, anywhere in this tier.
- **Physical Press-in Micro-interaction:** per the *Interaction States* contract above — only on elements that are actually clickable.
- **Asymmetric Off-Axis Layout:** Cards and mascot badges tilted between `-2°` to `+3°`, with `transition: transform 200ms ease-out` on breakpoint changes so the flatten-to-0° mobile behavior doesn't snap abruptly.

```
┌────────────────────────────────────────────────────────────────────────┐
│ SECTION 1: SENTINEL INGESTION & DEMOGRAPHIC ONBOARDING                │
│ (Lavender Canvas #B8A6E8 | Tilted Mascot Box -2° | Acid Lime CTA)      │
│ Content anchored LEFT — asymmetric negative space top-right            │
│                                                                        │
│  "FROM SILOED DATA TO AUTONOMOUS REVELATIONS"                          │
│  [Posyandu Stream Ingestion] [Realtime Micro-Antropometry Feed]        │
│  [ SIMULATE AUTONOMOUS SENTINEL ] ➔  (interactive: true)               │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │
                                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│ SECTION 2: AUTONOMOUS AI PROCESSING & REASONING PIPELINE              │
│ (Tilted Process Box +1.5° | Chunky Striped Progress Bar)               │
│ Content anchored CENTER-RIGHT                                          │
│                                                                        │
│  [✓] 01. Privacy Scrubbing: Gemma 2 PII Redaction & Geohashing         │
│  [✓] 02. Spatiotemporal Risk Engine: CDVI & Poisson GLM Regression     │
│  [ ] 03. Strategic Logistics Reasoning: Gemini 3.5 Multi-Constraint... │
│  [████████████████████░░░░░░░░░] 78% COMPUTING ALLOCATION              │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │
                                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│ SECTION 3: DECISION MATRIX & AUTONOMOUS ACTION DISPATCH                │
│ (Stark Cream Block #FFFDF7 | Lime PO Dispatch Banner | Hard Shadows)   │
│ Full-width band layout — NOT another centered card                     │
│                                                                        │
│  TAGS: [CRITICAL: WarningOctagon+stripe] [HIGH: WarningCircle]         │
│        [ACTION PLAN: READY] [CONFIDENCE: 98.4%]                        │
│  Decision: "Dispatch 1,200kg F-75 Formula to Kec. Medan Belawan"       │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ ⚡ AUTONOMOUS PO & INTERVENTION DISPATCHED TO GOOGLE CLOUD        │  │
│  │ Target: Cloud Storage PDF + Webhook Triggered (Time: < 42s)      │  │
│  │ [ DOWNLOAD SIGNED PO DOCUMENT (.PDF) ]  (interactive: true)      │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## React Implementation Notes (shadcn/ui + Tailwind)

- **Token delivery:** express every color/spacing/shadow token above as a CSS variable in `globals.css` under `:root`, then map into `tailwind.config.ts` via `theme.extend.colors` — never hardcode hex values inside component files (`color-semantic` rule).
- **Two token namespaces, one file:** prefix Enterprise tokens with no prefix (`bg-canvas`, `text-ink`) and Neo-Brutalist tokens with `brutalist-` (`bg-brutalist-lime`, `border-brutalist-black`) so a component's tier is legible from its className alone.
- **Component boundary:** Enterprise-tier components (`<AuditTable>`, `<ReportCard>`, `<FirestoreLogRow>`) never import brutalist utility classes, and vice versa — this keeps the two visual languages from bleeding into each other by accident.
- **Dark mode:** the Enterprise tier supports dark mode via the `surface-tile-*` / `surface-black` tokens (already dark-mode-native). The Neo-Brutalist tier is intentionally **not** dark-mode-adaptive — it's a fixed high-energy showcase panel, not a persistent surface, so forcing it through a dark-mode toggle would fight its own aesthetic. Document this explicitly in the component so future contributors don't try to "fix" it.
- **Reduced motion:** wrap all `.brutalist-interactive` transitions in `@media (prefers-reduced-motion: reduce) { transition: none; }` — the press-in effect is decorative-adjacent, not meaning-critical, so it's safe to disable entirely per `reduced-motion` rule.

---

## Do's and Don'ts

### Do
- **Use Public Sans consistently** across all headers, body copy, and UI controls. Treat the `-apple-system` fallback as a safety net, not a design feature.
- **Use Phosphor Bold/Fill icons** wrapped in thick black outlines (`3px solid #0A0A0A`) with hard drop shadows (`3px 3px 0px #0A0A0A`).
- **Use `{colors.brutalist-black}` as text color on every brutalist badge/card**, regardless of background — this is now a hard rule, not per-instance judgment.
- **Pair every risk tier with an icon and pattern, not just a color**, so choropleth and badge meaning survives colorblind viewing and video compression.
- **Attach `.brutalist-interactive` only to elements that do something on click** — static badges and display panels stay static.
- **Use Google Maps Platform API** to render interactive geospatial data layers and district risk choropleths with custom (never default) tile styling.
- **Maintain sharp 0px corners and heavy 3–5px borders** in the Neo-Brutalist workflow simulator to highlight the contrast with the Enterprise tier.
- **Vary section anchoring (left / center-right / full-width band)** across the 3-panel flow so it doesn't read as three centered cards in a row.

### Don't
- **Do not use gradients, blurred drop-shadows, or rounded corners** inside the Neo-Brutalist interactive section.
- **Do not put white text on any brutalist badge/card background** — every brutalist swatch is light/mid-tone; white fails contrast every time.
- **Do not rely on `tier-high` vs `tier-moderate` color alone** — always pair with the assigned icon + pattern.
- **Do not claim "SF Pro" as a rendered design choice** in judge-facing copy — it's an inert fallback outside Apple devices.
- **Do not use generic font stacks** or default system fonts without the Public Sans web-font actually loaded.
- **Do not use thin line icons**; always use thick bold/fill Phosphor icons with custom brutalist frames.
- **Do not use unstyled map tiles**; format Google Maps tiles with high-contrast boundaries to emphasize stunting risk tiers.
- **Do not attach hover/press states to purely informational elements** (static tier badges, display-only hero boxes) — it implies false interactivity.

---

## Responsive Breakpoints

| Breakpoint | Width | Adjustments |
|---|---|---|
| Mobile | < 640px | Single-column vertical stack. Brutalist tilts flatten to 0° (with a 200ms ease-out transition, not a snap) to prevent horizontal overflow. Headlines scale from 56px to 32px. Buttons become full-width with `min-height: 44px` touch targets. Google Maps collapses to 380px height. |
| Tablet | 640px – 1024px | 2-column asymmetric grid. Brutalist tilts kept at ±1.5°. Progress checklist displays compact badges. Google Maps height 480px. |
| Desktop | > 1024px | Full 3-panel interactive horizontal layout with full ±3° tilts, 8px hard drop-shadows, and full-featured Google Maps Sentinel console. |

---

## Fix Log (v1.1 → v1.2)

| # | Issue | Root Cause | Fix |
|---|---|---|---|
| 1 | `brutalist-badge-pink` text unreadable | `textColor: {colors.body-on-dark}` (white, `#ffffff`) on `#F55FA3` background measured **2.98:1** — fails WCAG AA (4.5:1 minimum) | Changed to `{colors.brutalist-black}` — now **6.64:1**, passes AA and AAA |
| 2 | `tier-high` (`#FF9F43`) and `tier-moderate` (`#FFD93D`) nearly indistinguishable | Only ~19° hue apart, **1.48:1** mutual contrast — a colorblind judge or a compressed video frame could easily conflate the two risk tiers | Introduced `{colors.brutalist-amber}` (`#F2762E`) for `tier-high`, widening hue gap to ~26° and mutual contrast to **2.06:1**; additionally paired every tier with a unique icon (`WarningOctagon` / `WarningCircle` / `Info` / `CheckCircle`) and badge pattern so tier meaning never depends on color alone |
| 3 | Press/active state only defined for icon badges | `shadows.brutalist-active` (`0px 0px 0px`) was declared as a token but never paired with a `transform` for hero boxes, process cards, dispatch cards, or CTAs — meaning the "pressed into the page" illusion wasn't guaranteed anywhere but one component | Declared one shared `.brutalist-interactive` contract (hover / active / focus-visible / disabled) and explicitly marked `interactive: true/false` on every component token, so implementers know exactly which elements get press behavior and which stay static |
| 4 | Font stack implied SF Pro was in active use | `"Public Sans", "SF Pro Display", "SF Pro Text"` framed as a co-equal stack, but `SF Pro` only resolves via `-apple-system` on Apple hardware and Public Sans (loaded first as a real web font) wins everywhere, including macOS — so SF Pro never actually paints a pixel | Reframed Typography section to state Public Sans as the sole system of record; fallback kept in code but no longer described as a design decision judges will see |

</design-context>

Use the design system above for all UI and visual artifacts you generate for CRESCA AI. This is a React-first implementation reference — component tokens map directly to Tailwind/shadcn conventions described in the *React Implementation Notes* section.
