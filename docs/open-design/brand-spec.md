# Agent Studio Brand Specification

> Source: active Stripe design system, adapted for Agent Studio.
> Note: no external brand spec/reference file was found in the project, so the redesign binds to the active Stripe system rather than inventing colors.

## System sentence

Agent Studio is governed infrastructure for agents, RAG, and workflows. The interface is calm, precise, and builder-first: deep navy structure, one vivid purple accent, generous whitespace, and a single type family.

## Tokens

### Palette

| Role | Name | Hex | Usage |
|---|---|---|---|
| background | White | `#ffffff` | Page canvas, primary surfaces |
| surface | Neutral 25 | `#f8fafd` | Subdued cards, panels, section backgrounds |
| foreground | Neutral 990 | `#061b31` | Primary headings, body text, solid icons |
| muted | Neutral 500 | `#64748d` | Secondary text, captions, metadata, subdued icons |
| border | Neutral 50 | `#e5edf5` | Rules, dividers, quiet borders |
| accent | Brand 600 | `#533afd` | Primary buttons, links, focus rings, selected states |
| accent-secondary | Brand 500 | `#665efd` | Secondary accents, hover states, hero gradients |

### Semantic colors

| Meaning | Hex | Usage |
|---|---|---|
| success | `#16a34a` | Published status, completed runs, approved approvals |
| warning | `#d97706` | Waiting approval, draft status |
| danger | `#dc2626` | Errors, rejected approvals, failed runs |

### Typography

- **Display / Body:** Sohne — fallbacks: `SF Pro Display, system-ui, -apple-system, Segoe UI, Helvetica Neue, Arial, sans-serif`
- **Mono:** Source Code Pro — fallbacks: `SFMono-Regular, Consolas, Liberation Mono, Menlo, Courier, monospace`

Weights used: 400 (body), 500 (UI labels), 600 (headlines, buttons).

### Spacing & radii

- Base grid: 4px
- Section spacing: 8px increments (24px, 32px, 40px, 48px)
- Border radius: 4px base; 8px for large cards; 9999px for pills
- Border weight: 1px

## Layout posture rules

1. Use generous whitespace and clear content blocks; hierarchy is headline → support text → primary action.
2. Cards and panels use 4–8px radii; large hero cards can use 16px.
3. Borders are 1px, quiet, and cool-neutral.
4. Primary actions use the purple accent fill; secondary actions are ghost or subtle surface fills.
5. One decisive accent color per screen; purple is the only accent.
6. Maintain calm, engineering-first density: lots of air, precise alignment, readable line lengths.
7. Workflows are contained modules, not full-screen canvases.

## Iconography

- Use Lucide icons (consistent with current stack).
- No emoji.
- Feature icons sit in subtle neutral surfaces, not colored circles.

## Voice (inherits Agent Studio + Stripe)

- Confident, direct, technical-but-clear.
- Prefer: agents, workflows, governance, manifests, versioned, tenant, MCP, runtime.
- Avoid: generic superlatives, jargon without explanation, hype-driven language.

## Logo / mark

- No supplied logo. Use a geometric monogram mark ("AS") in navy/purple as the product mark.
- Do not use Sparkles or gradient blobs as the primary identity.
