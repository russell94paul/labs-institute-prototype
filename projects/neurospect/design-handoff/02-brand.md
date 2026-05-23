# NeuroSpect — Brand & Design System

## Color Palette

### Primary (Brand — Cyan/Teal)

| Token | Hex | Usage |
|---|---|---|
| brand-50 | #ecfeff | — |
| brand-100 | #cffafe | — |
| brand-200 | #a5f3fc | — |
| brand-300 | #67e8f9 | Gradient text highlights, accent text |
| brand-400 | #22d3ee | Primary CTA, badges, section labels, links |
| brand-500 | #06b6d4 | Buttons, logo, primary accent |
| brand-600 | #0891b2 | — |
| brand-700 | #0e7490 | — |
| brand-800 | #155e75 | — |
| brand-900 | #164e63 | — |
| brand-950 | #083344 | Subtle background tints |

### Component Colors

Each platform component has its own signature color:

| Component | Color | Hex | Usage |
|---|---|---|---|
| NeuroSpect Mentor | Cyan | #06b6d4 | AI coaching features |
| NeuroCore | Purple | #8b5cf6 | Knowledge/retrieval features |
| NSLM | Amber | #f59e0b | Language model features |
| EdgeLab | Emerald | #10b981 | Research/backtesting features |
| NeuroQuant | Rose | #ec4899 | Production model features |
| NeuroTrader | Red | #ef4444 | Trading agent features |

### Neutrals

| Token | Hex | Usage |
|---|---|---|
| black | #000000 | Page background |
| slate-950 | #020617 | Gradient mid-tones |
| slate-900 | #0f172a | — |
| slate-800 | #1e293b | — |
| slate-700 | #334155 | Subtle borders |
| slate-600 | #475569 | Tertiary text, labels |
| slate-500 | #64748b | Body text |
| slate-400 | #94a3b8 | Secondary text |
| slate-300 | #cbd5e1 | Primary body text |
| white | #ffffff | Headings, emphasis |

### Semantic

| Purpose | Color | Hex |
|---|---|---|
| Positive / win | Emerald-400 | #34d399 |
| Negative / loss | Red-400 | #f87171 |
| Warning / caution | Amber-400 | #fbbf24 |
| Neutral / info | Slate-400 | #94a3b8 |

## Typography

### Fonts

| Role | Font | Weight | Fallback |
|---|---|---|---|
| Headings | Inter | 700–900 (bold, extrabold, black) | system-ui, sans-serif |
| Body | Inter | 400–600 (regular, medium, semibold) | system-ui, sans-serif |
| Code/Data | JetBrains Mono | 400–500 | Fira Code, monospace |

### Scale

| Element | Size | Weight | Color |
|---|---|---|---|
| Hero H1 | 4xl → 7xl (responsive) | 900 (extrabold) | white |
| Section H2 | 3xl → 4xl | 700 (bold) | white |
| Section label | sm (14px) | 500 (medium) | brand-400, uppercase, tracking-wider |
| Body text | lg (18px) | 400 | slate-500 |
| Card title | sm (14px) | 600 (semibold) | white |
| Card body | sm (14px) | 400 | slate-500 |
| Badge/tag | 11px | 500 | varies by component color |
| Data values | sm (14px) | 500, mono | varies (semantic colors) |
| Legal/disclaimer | xs (12px) | 400 | slate-600 or slate-700 |

## Card System — "Neon Cards"

All content cards use a consistent treatment:

### Base Card (`.neon-card`)
- Background: `rgba(30, 30, 35, 0.85)` (charcoal)
- Border: `1px solid rgba(255, 255, 255, 0.06)`
- Border radius: 16px (`rounded-2xl`)
- Hover: border brightens to brand cyan, outer glow appears, subtle inner glow

### Color Variants

Each variant adds a colored border glow at rest and intensifies on hover:

| Variant | Rest Border | Hover Border | Glow Color |
|---|---|---|---|
| cyan | `rgba(6, 182, 212, 0.25)` | `rgba(6, 182, 212, 0.5)` | brand-500 |
| purple | `rgba(139, 92, 246, 0.25)` | `rgba(139, 92, 246, 0.5)` | purple-500 |
| amber | `rgba(245, 158, 11, 0.25)` | `rgba(245, 158, 11, 0.5)` | amber-500 |
| emerald | `rgba(16, 185, 129, 0.25)` | `rgba(16, 185, 129, 0.5)` | emerald-500 |
| rose | `rgba(236, 72, 153, 0.25)` | `rgba(236, 72, 153, 0.5)` | rose-500 |
| red | `rgba(239, 68, 68, 0.25)` | `rgba(239, 68, 68, 0.5)` | red-500 |

### Glow Formula (per variant)

```
Rest:
  box-shadow: 0 0 12px {color at 6%}, 0 0 30px {color at 3%}

Hover:
  box-shadow: 0 0 20px {color at 12%}, 0 0 50px {color at 6%}, inset 0 0 30px {color at 3%}
```

## Logo

- Mark: Rounded square (border-radius 6px) with brand-500 fill, white bold "N"
- Wordmark: "NeuroSpect" in Inter semibold, white
- Usage: Mark + wordmark in nav, mark only in footer

## Button System

| Type | Style |
|---|---|
| Primary | `bg-brand-500`, white text, `rounded-xl`, hover lifts 0.5px + glow shadow |
| Secondary/Ghost | transparent bg, `border-white/[0.08]`, slate-300 text, hover brightens border + text |
| Nav CTA | `bg-brand-400`, black text, `rounded-lg` |

## Section Background Formula

Every section follows this pattern:
1. Pure black base
2. Vertical gradient overlay (`from-black via-{color}/opacity to-black`)
3. 1-2 large blurred circles (`blur-[100-120px]`, low opacity 3-7%) for ambient glow
4. Optional: grid pattern overlay at 3% opacity (hero only)

## Spacing

- Section vertical padding: `py-24` (96px) to `py-32` (128px)
- Content max-width: `max-w-6xl` (1152px) for data sections, `max-w-4xl` (896px) for hero/CTA
- Card gap: `gap-3` (12px) to `gap-6` (24px) depending on density
- Inner card padding: `p-5` (20px) to `p-8` (32px)

## Animation

| Animation | Duration | Easing | Trigger |
|---|---|---|---|
| Scroll fade-in | 700ms | `cubic-bezier(0.16, 1, 0.3, 1)` | IntersectionObserver (threshold 0.1) |
| Stagger delay | 80ms between siblings | same | same |
| Float (ambient) | 6-8s | ease-in-out | infinite loop |
| Pulse ring | 2s | ease-out | infinite loop |
| Button hover lift | 150ms | default | hover |
| Card border glow | 400ms | ease | hover |
| Chart.js entrance | 1400ms | easeOutQuart | scroll into view |
| SVG line draw | varies | — | dash-offset animation |
| SVG particle flow | 2-3s | — | animateMotion along path |
