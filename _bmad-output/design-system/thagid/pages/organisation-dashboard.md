# Organisation Dashboard

> Overrides MASTER.md for the organisation dashboard and org scope pages.

---

## Organisation Dashboard

**Route:** `/` or `/org/{orgId}`
**Sidebar:** Organisation scope (Projects, Org Settings)
**Top bar:** Logo / [Org Name] / no project dropdown

### Layout

```
┌─────────────────────────────────────────────────┐
│  Organisation Dashboard              [+ Create]  │
│  🔍 Search projects...                          │
│                                                 │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐         │
│  │ Project  │  │ Project  │  │ Project  │        │
│  │ Card     │  │ Card     │  │ Card     │        │
│  └─────────┘  └─────────┘  └─────────┘         │
└─────────────────────────────────────────────────┘
```

### Header Section

| Element | Spec |
|---------|------|
| Page title | `text-2xl font-bold text-slate-900` — "Organisation Dashboard" (or org name) |
| Create button | Primary CTA button, `plus` icon + "Create Project", top-right |
| Search bar | Below title, full-width `max-w-sm`, standard input with search icon |

### Project Cards Grid

- Grid: `grid grid-cols-3 gap-6` (3 columns on standard desktop)
- Card: standard card spec from MASTER.md
- Card content:
  - Title: project name, `text-base font-semibold`
  - Description: `text-sm text-slate-600 line-clamp-2`, max 2 lines
  - Footer: package count + last updated, `text-xs text-slate-400`
- Card click → navigates to project dashboard

**shadcn mapping:** `Card`, `CardHeader`, `CardTitle`, `CardDescription`, `CardContent`

### Empty State

```
┌─────────────────────────────────────────────┐
│                                             │
│           📁                                │
│                                             │
│     No projects yet                         │
│     Create your first project to get        │
│     started with Thagid.                    │
│                                             │
│     [+ Create Project]                      │
│                                             │
└─────────────────────────────────────────────┘
```

- Centered in main content area
- Icon: `folder` Lucide icon, `w-12 h-12 text-slate-300`
- Heading: `text-lg font-semibold text-slate-900`
- Description: `text-sm text-slate-500 max-w-sm text-center`
- CTA button: primary CTA, "Create Project"

---

## Organisation Settings

**Route:** `/org/{orgId}/settings`
**Sidebar:** Organisation scope (Projects, Org Settings active)

- Reuses the organisation name input field
- Simple form: name field + save button
- Save button: primary CTA, "Save Changes"
- On success: toast notification "Organisation updated"

---

## Organisation Creation (First-Time)

**Route:** `/org/new`
**Sidebar:** None
**Top bar:** Logo only, centered

```
┌─────────────────────────────────────────────────────┐
│  [Thagid]                                           │
├─────────────────────────────────────────────────────┤
│                                                     │
│                  Welcome to Thagid                   │
│     Start by creating your organisation.             │
│                                                     │
│     ┌──────────────────────────┐                    │
│     │ Organisation name        │                    │
│     └──────────────────────────┘                    │
│                                                     │
│          [Create Organisation]                       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

- Centered vertically and horizontally in viewport
- Max-width: `max-w-md`
- Title: `text-2xl font-bold text-slate-900`
- Subtitle: `text-sm text-slate-500`
- Input: standard input spec
- Button: primary CTA, full-width, "Create Organisation"
