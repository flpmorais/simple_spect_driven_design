# Project Dashboard

> Overrides MASTER.md for the project dashboard and project scope pages.

---

## Project Dashboard

**Route:** `/project/{projectId}`
**Sidebar:** Project scope (Dashboard active, Wiki disabled, Roadmap disabled, Settings, Packages list)
**Top bar:** Logo / [Org dropdown] / [Project dropdown]

### Layout

```
┌─────────────────────────────────────────────────┐
│  Project Name                        [⚙️ Settings]│
│                                                 │
│  ┌─── Project Brief ──────────────────────────┐ │
│  │ Executive summary text goes here...         │ │
│  │ Lorem ipsum dolor sit amet...               │ │
│  │                                [See more →] │ │
│  └─────────────────────────────────────────────┘ │
│                                                 │
│  ┌─── GitHub ──────────────────────────────────┐ │
│  │ [📊 Kanban Board]  [📂 Repository]          │ │
│  └─────────────────────────────────────────────┘ │
│                                                 │
│  Packages                         [+ New Package]│
│  ┌─────────────────────────────────────────────┐│
│  │ 📦 v1.0 Core API          ● New            ││
│  │ 📦 Auth Module            ● In Progress    ││
│  │ 📦 Payment Integration    ● Planning       ││
│  └─────────────────────────────────────────────┘│
└─────────────────────────────────────────────────┘
```

### Header Section

| Element | Spec |
|---------|------|
| Page title | Project name, `text-2xl font-bold text-slate-900` |
| Settings link | Ghost button, `settings` icon, top-right → navigates to project settings |

### Brief Section

- Card: standard card spec, no hover (non-interactive)
- Label: `text-xs font-medium text-slate-400 uppercase tracking-wider` — "Project Brief"
- Executive summary: `text-sm text-slate-600 line-clamp-3`, max 3 lines visible
- "See more" link: `text-sm font-medium text-primary cursor-pointer` with `arrow-right` icon
  - Expands to show full brief template:
    - Executive Summary, The Problem, The Solution, What Makes This Different,
      Who This Serves, Success Criteria, Scope, Vision
  - Each section: `text-sm font-semibold text-slate-900` heading + `text-sm text-slate-600` body
  - "See less" link to collapse

**shadcn mapping:** `Card` with collapsible content area (use `Collapsible` component)

### GitHub Links Section

- Inline row of two link buttons
- Style: secondary button variant with `external-link` icon
- "Kanban Board" → opens GitHub project URL in new tab
- "Repository" → opens GitHub repo URL in new tab
- Spacing: `gap-3` between buttons

### Packages Section

| Element | Spec |
|---------|------|
| Section title | `text-lg font-semibold text-slate-900` — "Packages" |
| Create button | Primary CTA, `plus` icon + "New Package", right-aligned |

### Package List

- List: stacked rows, `divide-y divide-slate-200`
- Row: `flex items-center justify-between p-4 hover:bg-slate-50 cursor-pointer rounded-lg transition-colors duration-150`
- Row content:
  - Left: `package` icon + package title (`text-sm font-semibold text-slate-900`) + description snippet (`text-sm text-slate-500 ml-2`)
  - Right: status badge
- Click → navigates to package chat view

### Brainstorm Summary Card

Shown below each package row that has a concluded brainstorm session.

```
┌──────────────────────────────────────────────────────────────┐
│  💡 Brainstorm — May 8, 2026                                 │
│  4 techniques · 47 ideas · 5 themes                          │
│                                                              │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌───────┐ │
│  │ UX (12) │ │ Tech(8) │ │ Data(6) │ │ Mkt(11) │ │Ops(10)│ │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └───────┘ │
│                                               [View Details] │
└──────────────────────────────────────────────────────────────┘
```

- Background: `bg-white border border-slate-200 rounded-xl p-5 mt-2`
- Visible only when package has a concluded brainstorm session
- Header row: `lightbulb` icon + "Brainstorm" + date, `text-sm font-semibold text-slate-900`
- Stats row: technique count · idea count · theme count, `text-xs text-slate-500`
- Theme pills: horizontal row of compact chips, `gap-2 flex-wrap mt-3`
  - Each pill: `text-xs font-medium px-2.5 py-1 rounded-full bg-slate-100 text-slate-600`
  - Format: "{Theme Name} ({idea count})"
  - Max 5 pills shown, "+N more" pill if overflow
- "View Details" link: `text-sm font-medium text-primary cursor-pointer`, right-aligned
  - Click → navigates to brainstorm detail view

**shadcn mapping:** Custom card within the package row area.

### Empty State (No Packages)

```
┌─────────────────────────────────────────────┐
│                                             │
│           📦                                │
│                                             │
│     No packages yet                         │
│     Create your first package to start      │
│     defining your release.                  │
│                                             │
│     [+ New Package]                         │
│                                             │
└─────────────────────────────────────────────┘
```

Same pattern as org empty state but with `package` icon and package-specific copy.

---

## Project Settings

**Route:** `/project/{projectId}/settings`
**Sidebar:** Project scope (Settings active)

- Reuses project creation form in edit mode
- Fields: name, description, GitHub project URL, GitHub repo URL
- Save button: primary CTA, "Save Changes"
- On success: toast "Project updated"

---

## Project Creation

**Route:** `/project/new`
**Sidebar:** Organisation scope (on org page context)

See `forms.md` for form patterns.
