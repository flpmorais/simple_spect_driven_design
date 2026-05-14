# Brainstorm Detail

> Overrides MASTER.md for the brainstorm detail tab showing session results, themes, and ideas.

---

## Brainstorm Detail View

**Route:** `/project/{projectId}/package/{packageId}/brainstorm`
**Sidebar:** Project scope (package highlighted in packages list)
**Top bar:** Logo / [Org dropdown] / [Project dropdown]
**Entry:** From brainstorm summary card on project dashboard or package chat

### Layout

```
┌─────────────────────────────────────────────────────────────┐
│  ← Back to Package                                          │
│                                                             │
│  Brainstorm Session                        [Phase: Concluded]│
│  May 8, 2026 · 4 techniques · 47 ideas                     │
│                                                             │
│  ┌─── Session Summary ────────────────────────────────────┐ │
│  │  Key insights and summary text rendered here.          │ │
│  │  This is the extracted session summary from the agent. │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─── Theme: User Experience ───────────────── 12 ideas ──┐ │
│  │  ┌─ Idea ────────────────────────────────────────────┐ │ │
│  │  │  Mnemonic Title                          Category │ │ │
│  │  │  Concept description text goes here...            │ │ │
│  │  └──────────────────────────────────────────────────┘ │ │
│  │  ┌─ Idea ────────────────────────────────────────────┐ │ │
│  │  │  Another Idea                            Category │ │ │
│  │  │  Another concept description...                   │ │ │
│  │  └──────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─── Theme: Technical Architecture ────────── 8 ideas ───┐ │
│  │  (collapsed — click to expand)                         │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─── Theme: Data Strategy ────────────────── 6 ideas ───┐ │ │
│  │  (collapsed — click to expand)                         │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Header Section

| Element | Spec |
|---------|------|
| Back link | `arrow-left` icon + "Back to Package", `text-sm text-primary cursor-pointer hover:underline` |
| Page title | "Brainstorm Session", `text-2xl font-bold text-slate-900` |
| Phase badge | Brainstorm phase badge (see MASTER.md Status Colors — Brainstorm Phases) |
| Metadata row | Date · technique count · idea count, `text-sm text-slate-500` |

### Session Summary Card

- Card: standard card spec from MASTER.md, no hover (non-interactive)
- Label: `text-xs font-medium text-slate-400 uppercase tracking-wider` — "Session Summary"
- Content: `text-sm text-slate-600`, rendered markdown from structured summary
- Key insights: bulleted list with `lightbulb` icon prefix on each item
- Margins: `mt-6 mb-8`

**shadcn mapping:** `Card`, `CardHeader`, `CardContent`

### Themes Section

- Section title: `text-lg font-semibold text-slate-900` — "Themes"
- Themes stack vertically with `gap-4`
- Each theme: collapsible theme card (see MASTER.md → Theme Card)

### Theme Card (Detail View)

**Expanded state:**
- Header: `layers` icon + theme name (`text-base font-semibold text-slate-900`) + idea count badge + collapse chevron
- Idea count badge: `text-xs font-medium text-slate-500 bg-slate-100 rounded-full px-2 py-0.5`
- Collapse chevron: `chevrons-up-down` icon, ghost button
- Ideas list: `divide-y divide-slate-100 mt-3`
- Each idea row:
  - Title: `text-sm font-semibold text-slate-900`
  - Category: `text-xs font-medium text-slate-500` inline, right-aligned
  - Description: `text-sm text-slate-600 mt-0.5`
  - Padding: `py-3`
- Interactive: hover on idea rows shows subtle `bg-slate-50`

**Collapsed state:**
- Same header row but with `chevrons-down-up` icon
- No idea list visible
- Click header to expand

### Empty State (No Brainstorm Session)

```
┌─────────────────────────────────────────────┐
│                                             │
│           💡                                │
│                                             │
│     No brainstorm session yet               │
│     Start a brainstorm from the package     │
│     chat to generate and organize ideas.    │
│                                             │
│     [Go to Chat]                            │
│                                             │
└─────────────────────────────────────────────┘
```

- Centered in main content area
- Icon: `lightbulb` Lucide icon, `w-12 h-12 text-slate-300`
- Heading: `text-lg font-semibold text-slate-900`
- Description: `text-sm text-slate-500 max-w-sm text-center`
- CTA button: primary CTA, "Go to Chat" — navigates to package chat view

### Session In Progress State

When a brainstorm session exists but is not yet concluded:
- Show header with current phase badge (Initiate, Facilitate, Extract, etc.)
- Show "Session in Progress" card instead of summary:
  - `text-sm text-slate-500` — "This brainstorm session is still active."
  - "Continue Session" button: primary CTA — navigates to package chat
- Show any themes/ideas that have been extracted so far (if in Extract+ phase)
- If still in Initiate/Facilitate: show empty themes section with "Ideas will appear here as the session progresses."

---

## Navigation

### From Project Dashboard

Brainstorm summary card on project dashboard → click "View Details" → navigates to brainstorm detail view

### From Package Chat

- Chat header shows phase badge during active session
- When session concludes, agent message includes "View brainstorm results" link → navigates to brainstorm detail view

### Back Navigation

- "Back to Package" link returns to package chat view
