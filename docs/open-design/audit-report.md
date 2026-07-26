# Agent Studio UI/UX Audit

> Scope: `builder/src` React frontend (Vite + Tailwind + shadcn/ui)
> Auditor lens: senior product designer, desktop-web app, governance/workflow domain

## Executive summary

The current UI is functional but visually anonymous. It reads as a default shadcn/ui installation with a dark sidebar bolted on, not as a deliberate product for governed agent infrastructure. The biggest blockers are:

1. **No owned brand system** — default indigo primary, default radius, mixed accent colors per node type.
2. **Workflow builder dominates the viewport** — 62vh canvas feels like the whole app, not a contained tool.
3. **Card overload** — every section is a bordered card, creating visual noise instead of hierarchy.
4. **Inconsistent color semantics** — governance states (approve/reject/run) use ad-hoc palettes.
5. **Chat breaks the app frame** — negative margins escape the `AppShell` container and duplicate sidebar patterns.

The redesign moves to a single, disciplined design system (Stripe), treats the workflow canvas as a contained module, and replaces card walls with typographic hierarchy and intentional whitespace.

---

## 1. Brand & identity

### Current state
- Logo: `bg-gradient-to-br from-indigo-500 to-violet-600` + `Sparkles` icon.
- Primary: Tailwind indigo-500 (`#6366f1`) — the most common AI-generated UI tell.
- Sidebar: hard-coded slate (`#0f172a`-ish) with white/10 overlays.
- Accents vary by screen: indigo buttons, emerald/amber/rose/slate workflow nodes, blue/violet/red/yellow chat chips.
- Radius: `0.65rem` (~10px) default shadcn.

### Problems
- No single accent owns the product. The user cannot remember one color and associate it with Agent Studio.
- Indigo is so over-used in LLM tools that it signals "template" before the user reads a word.
- The Sparkles icon + gradient logo reads as a consumer AI toy, not enterprise governance infrastructure.

### Redesign direction
- Adopt Stripe's palette: deep navy (`#061b31`) for structure, vivid purple (`#533afd`) as the one accent, cool neutrals for surfaces.
- One type family (Sohne / SF Pro Display stack), one accent, one radius system (4px base).
- Replace Sparkles with a geometric mark built from the product initials / node metaphor.

---

## 2. Layout & density

### Current state
- `AppShell` centers content at `max-w-6xl` with `px-6 py-8`.
- `ChatPage` overrides this with `h-[calc(100vh-4rem)]` and negative margins, becoming a full-screen experience inside a contained app.
- `WorkflowBuilderPage` uses a 62vh canvas plus a 288px inspector, leaving little room for run output.

### Problems
- The workflow canvas is large enough to feel like the app *is* the canvas. Governance tools should feel precise, not sprawling.
- Chat breaks the consistent page gutter and creates two sidebars (global nav + conversation rail).
- Page headers are small (`text-2xl`) and get lost above dense card grids.

### Redesign direction
- Keep a uniform page canvas; no negative-margin breakouts.
- Workflow builder: contained workspace card (~520–600px canvas height), inspector beside or as a sliding panel, run output below as a timeline.
- Chat: integrate the conversation list as a page-level rail inside the standard layout, not as a second app chrome.
- Larger page titles (`text-3xl` / 36px+), tighter `PageHeader`, and fewer separator lines.

---

## 3. Typography

### Current state
- Everything uses the default system-ui / sans stack.
- Headings rely on `font-bold tracking-tight` but no negative tracking.
- Mono is used only for IDs and model names.

### Problems
- No display/body role split; headings look like boosted body text.
- Small labels in all-caps sidebar groups lack letter-spacing.

### Redesign direction
- Display face for H1/H2 (Sohne / SF Pro Display), negative tracking on large type.
- Body face same family, lighter weights for UI labels.
- Mono for code, IDs, and node handles with consistent scale.
- All-caps labels get `0.08em` tracking.

---

## 4. Component system

### Current state
- Buttons: default shadcn variants (`bg-primary`, `outline`, `ghost`, `secondary`).
- Cards: used for every section — stats, forms, lists, empty states.
- Badges: status, version, tags share the same component with different variants.
- Inputs: standard shadcn with 1px borders.

### Problems
- Cards as the only container create a "card wall" effect with no rhythm.
- Primary button is indigo everywhere; there is no secondary surface language.
- Badge variants are overloaded (status vs. count vs. tag).

### Redesign direction
- Flat sections with generous whitespace; reserve cards for genuinely distinct surfaces (stats, empty states, preview panels).
- One primary purple fill; secondary actions use subtle navy surface or ghost text.
- Separate status tokens (published/draft/running/waiting) from accent purple.
- Inputs: 4px radius, 1px cool borders, focus ring in purple.

---

## 5. Color semantics

### Current state
| Meaning | Current colors |
|---|---|
| Primary action | Indigo-500 fill, indigo-50 highlight |
| Success | Emerald/green shades (varying) |
| Warning | Amber/yellow shades (varying) |
| Error | Red/destructive shades (varying) |
| Agent node | Indigo |
| Condition node | Amber |
| Human approval node | Rose |
| Start node | Emerald |
| End node | Slate |

### Problems
- Rainbow nodes look like a generic flowchart, not a governed agent workflow.
- Semantic colors are not locked to tokens, so they drift between screens.

### Redesign direction
- One accent: purple (`#533afd`).
- Semantic palette mapped to explicit tokens: success green, warning amber, error red.
- Workflow nodes: neutral shells with one accent color for the active/selected state; node kind distinguished by icon + label, not a new color per node.

---

## 6. Specific screen notes

### Dashboard
- 4 stat cards in a row + 2-column lower grid is fine, but stats compete visually with the list below.
- "Workflows" and "Versioning" use static placeholder values (`—`, `on`).

### Agents list
- Empty state is good; card grid is dense and every card has identical weight.
- Status badge placement is correct but needs clearer published/draft semantics.

### Agent editor
- Long vertical stack of cards; no sticky actions, so the user scrolls past primary buttons.
- Governance sections (tools/models/RAG) repeat the same add/remove pattern without consolidation.
- Version history is a separate card instead of a side rail.

### Workflow builder
- Canvas height is arbitrary (`62vh`) and feels oversized on large monitors.
- Inspector is always visible, even when nothing is selected.
- Run output is appended below the fold.

### Chat
- Escapes the app shell; conversation rail duplicates sidebar logic.
- Mode toggle (Agent / Workflow) uses indigo-50 pills.
- User bubble is indigo-600; assistant bubble is card surface.

### Run panel
- Result sections are all separate cards; no hierarchy between answer, citations, tool calls, denials.

### Settings
- Four seam cards are fine but visually identical to every other card in the app.

---

## 7. Recommendations summary

1. **Lock one design system** (Stripe tokens) and remove all raw indigo/amber/rose/emerald fills from components.
2. **Contain the workflow builder** — fixed-height workspace, slide-out inspector, run timeline below.
3. **Reduce card usage** by 40–50%; use whitespace and typography to separate sections.
4. **Standardize page headers** with larger titles, crisp actions, and no competing sidebars.
5. **Unify semantic colors** across agent status, workflow status, chat states, and governance chips.
6. **Add product-specific microcopy** and an owned mark instead of Sparkles.
7. **Fix chat layout** so it lives inside the app canvas with a consistent gutter.

---

## Files reviewed

- `builder/src/App.tsx`
- `builder/src/index.css`
- `builder/src/components/layout/AppShell.tsx`
- `builder/src/components/layout/PageHeader.tsx`
- `builder/src/components/ui/button.tsx`
- `builder/src/components/workflow/nodes.tsx`
- `builder/src/pages/DashboardPage.tsx`
- `builder/src/pages/AgentsListPage.tsx`
- `builder/src/pages/AgentEditorPage.tsx`
- `builder/src/pages/WorkflowsPage.tsx`
- `builder/src/pages/WorkflowBuilderPage.tsx`
- `builder/src/pages/ChatPage.tsx`
- `builder/src/pages/RunPanelPage.tsx`
- `builder/src/pages/HistoryPage.tsx`
- `builder/src/pages/SettingsPage.tsx`
- `builder/tailwind.config.js`
