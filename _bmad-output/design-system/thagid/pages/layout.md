# Layout — Top Bar + Sidebar

> Overrides MASTER.md layout details with page-specific implementation guidance.

---

## Shell Layout (Root +layout.svelte)

```
<div class="flex h-screen overflow-hidden">
  <!-- Top Bar -->
  <header class="fixed top-0 left-0 right-0 h-14 bg-card z-50 flex items-center justify-between px-4 shadow-[0_1px_2px_rgba(0,0,0,0.06)]">
    <!-- Breadcrumbs left -->
    <!-- Avatar right -->
  </header>

  <div class="flex flex-1 pt-14">
    <!-- Sidebar -->
    <aside class="w-64 bg-card overflow-y-auto flex-shrink-0">
      <!-- Scope-aware content -->
    </aside>

    <!-- Main Content -->
    <main class="flex-1 overflow-y-auto p-6 bg-background">
      <!-- Page content -->
    </main>
  </div>
</div>
```

### shadcn Components

- Top bar: custom `Header` component (no shadcn equivalent needed)
- Sidebar: `SidebarProvider`, `Sidebar`, `SidebarContent`, `SidebarHeader`, `SidebarGroup`, `SidebarMenu`, `SidebarMenuItem`, `SidebarMenuButton`
- Layout: `SidebarProvider` wraps the entire shell

---

## Top Bar

### Standard (Authenticated)

```
┌──────────────────────────────────────────────────────────────┐
│  [Thagid]  /  [Acme Dev Team ▾]  /  [Thagid Web App ▾]  [👤]│
└──────────────────────────────────────────────────────────────┘
```

| Element | Spec |
|---------|------|
| Logo | icon.svg (`h-6 w-6`) + `<span class="font-brand text-lg text-primary">Thagid</span>` — navigates to org dashboard |
| Separator | `/` in `text-slate-300 mx-2` |
| Org dropdown | Breadcrumb segment style + `chevron-down` icon (12px). Opens popover. |
| Project dropdown | Same as org. Hidden when at org scope (no project selected). |
| Avatar | `w-8 h-8 rounded-full` — Google profile image. Fallback: user initial in `bg-primary text-white text-xs font-semibold`. Right-aligned. |

### First-Time (No Org)

```
┌──────────────────────────────────────────────────────────────┐
│  [Thagid]                                                   │
└──────────────────────────────────────────────────────────────┘
```

- Logo only, centered or left-aligned
- No breadcrumbs, no sidebar, no avatar

### Org Dropdown Popover

```
┌─────────────────────────────┐
│  🔍 Search organisations... │
│                             │
│  ✦ Acme Dev Team           │  ← current org, checkmark
│    Personal Workspace       │
│                             │
│  [+ Create Organisation]    │
└─────────────────────────────┘
```

- Width: `w-72`
- Max height: `max-h-80`
- Search: standard input with search icon, filters list
- Current org: `bg-slate-100` background, check icon
- "Create" button: full-width, ghost style, `plus` icon

### Project Dropdown Popover

Same structure as org dropdown but for projects.

---

## Sidebar

### Organisation Scope

```
┌──────────────────┐
│ □ Projects       │  ← icon: folder, active
│ ⚙ Org Settings   │  ← icon: settings
└──────────────────┘
```

**Active item:** `bg-muted text-primary font-semibold rounded-lg`
**Inactive item:** `text-muted-foreground hover:bg-muted rounded-lg`

### Project Scope

```
┌──────────────────┐
│ □ Dashboard      │  ← icon: layout-dashboard
│ 📖 Wiki          │  ← disabled: text-slate-300
│ 🗺️ Roadmap       │  ← disabled: text-slate-300
│ ⚙ Settings       │  ← icon: settings
│                  │
│ ──── Packages ───│  ← section label + divider
│ 📦 v1.0 Core API │  ← with status dot
│ 📦 Auth Module   │  ← with status dot
│ + New Package    │  ← ghost button
└──────────────────┘
```

**Section divider:** `border-t border-slate-200 my-3`
**Section label:** `text-xs font-medium text-muted-foreground uppercase tracking-wider px-3 mb-2`
**Package status dot:** `w-2 h-2 rounded-full` inline, color from status palette
**Disabled items:** `text-slate-300 cursor-not-allowed` — no hover, no click

### Sidebar Collapse

- Toggle button: ghost icon button at bottom of sidebar
- Collapsed state: `w-16`, icon-only with tooltip on hover
- Transition: `transition-all duration-200 ease-in-out`
