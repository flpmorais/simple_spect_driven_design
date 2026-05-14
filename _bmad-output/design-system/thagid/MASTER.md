# Design System Master File

> **LOGIC:** When building a specific page, first check `design-system/pages/[page-name].md`.
> If that file exists, its rules **override** this Master file.
> If not, strictly follow the rules below.

---

**Project:** Thagid
**Generated:** 2026-05-06
**Stack:** SvelteKit + shadcn-svelte
**Category:** Developer Tools / SDLC Automation
**Style:** AI-Native UI — minimal chrome, conversational, professional

---

## Layout Architecture

Desktop-only SPA. No responsive breakpoints needed for MVP.

```
┌─────────────────────────────────────────────────────────────┐
│  TOP BAR (fixed, h-14)                                      │
│  [Logo] [/ Org Dropdown] [/ Project Dropdown]     [Avatar]  │
├──────────┬──────────────────────────────────────────────────┤
│ SIDEBAR  │  MAIN CONTENT                                    │
│ (w-64)   │  (flex-1, overflow-y-auto)                       │
│          │                                                  │
│ Scope-   │  Page content renders here                       │
│ aware    │                                                  │
│ content  │                                                  │
│          │                                                  │
│          │                                                  │
│          │                                                  │
│          │                                                  │
└──────────┴──────────────────────────────────────────────────┘
```

- **Top bar:** Fixed, full-width, `h-14`, no border — uses `shadow-[0_1px_2px_rgba(0,0,0,0.06)]` for separation. Breadcrumbs left, avatar right.
- **Sidebar:** Fixed left, `w-64`, no border — background differentiation (white sidebar vs slate-50 content). Content changes per scope. `pt-14` to offset below fixed header.
- **Main content:** `flex-1`, `overflow-y-auto`, `p-6`. Padded below top bar (`pt-20`).
- **No sidebar** on org creation (first-time) screen — logo-only top bar.

---

## Color Palette

| Role | Hex | Usage |
|------|-----|-------|
| Primary | `#0A3B85` (navy) | CTA buttons, active states, links, focus rings |
| Primary hover | `#082D66` (navy-dark) | Primary hover state |
| Text primary | `#0F172A` (slate-900) | Headings, body text |
| Text secondary | `#475569` (slate-600) | Muted labels, descriptions, metadata |
| Text tertiary | `#94A3B8` (slate-400) | Disabled text, placeholders |
| Border | `#E2E8F0` (slate-200) | Card borders, dividers, input borders only |
| Surface | `#FFFFFF` | Cards, modals, sidebar, topbar |
| Muted surface | `#F1F5F9` (slate-100) | Hover backgrounds, muted fills, secondary buttons |
| Background | `#F8FAFC` (slate-50) | App background — neutral light gray |

### Structural Separation Strategy

**Do NOT use 1px solid borders between topbar, sidebar, and content.** Use:
- **Background differentiation**: White sidebar/topbar vs slate-50 content creates natural boundary
- **Subtle shadow** on topbar bottom edge: `shadow-[0_1px_2px_rgba(0,0,0,0.06)]`
- **No border** on sidebar right edge
- Borders are only for components: cards, inputs, dividers within content

### Status Colors (Packages)

| Status | Hex | Background |
|--------|-----|------------|
| New | `#6366F1` (indigo-500) | `#EEF2FF` (indigo-50) |
| Planning | `#F59E0B` (amber-500) | `#FFFBEB` (amber-50) |
| In Progress | `#2563EB` (blue-600) | `#EFF6FF` (blue-50) |
| Finished | `#22C55E` (green-500) | `#F0FDF4` (green-50) |
| Released | `#8B5CF6` (violet-500) | `#F5F3FF` (violet-50) |
| Cancelled | `#94A3B8` (slate-400) | `#F1F5F9` (slate-100) |

### Status Colors (Brainstorm Phases)

| Phase | Hex | Background |
|-------|-----|------------|
| Initiate | `#6366F1` (indigo-500) | `#EEF2FF` (indigo-50) |
| Facilitate | `#2563EB` (blue-600) | `#EFF6FF` (blue-50) |
| Extract | `#F59E0B` (amber-500) | `#FFFBEB` (amber-50) |
| Validate | `#8B5CF6` (violet-500) | `#F5F3FF` (violet-50) |
| Markdown | `#22C55E` (green-500) | `#F0FDF4` (green-50) |
| Concluded | `#94A3B8` (slate-400) | `#F1F5F9` (slate-100) |

---

## Typography

- **Font Family (UI):** Plus Jakarta Sans (single font, variable weight)
- **Font Family (Brand):** Michroma — used exclusively for the app name "Thagid" next to logos
- **Mood:** friendly, modern, clean, approachable, professional

**CSS Import:**
```css
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Michroma&display=swap');
```

**Tailwind token:** `font-brand` → Michroma

### Type Scale

| Element | Size | Weight | Color | Usage |
|---------|------|--------|-------|-------|
| Page title | `text-2xl` (24px) | 700 | `#0F172A` | Dashboard headings, page titles |
| Section title | `text-lg` (18px) | 600 | `#0F172A` | Card headings, section labels |
| Card title | `text-base` (16px) | 600 | `#0F172A` | Package names, project names |
| Body | `text-sm` (14px) | 400 | `#475569` | Descriptions, body copy |
| Caption | `text-xs` (12px) | 500 | `#94A3B8` | Status badges, metadata, timestamps |
| Sidebar item | `text-sm` (14px) | 500 | `#475569` | Nav items (active: `#0A3B85`, weight 600) |
| Breadcrumb | `text-sm` (14px) | 500 | `#0A3B85` | Top bar breadcrumb segments |
| Chat message | `text-sm` (14px) | 400 | `#0F172A` | Chat bubble text |
| Button | `text-sm` (14px) | 600 | — | All buttons |

---

## Spacing

| Token | Value | Usage |
|-------|-------|-------|
| `--space-xs` | `4px` | Tight gaps, icon-to-text |
| `--space-sm` | `8px` | Inline spacing, list item gaps |
| `--space-md` | `16px` | Standard padding, card internal |
| `--space-lg` | `24px` | Section padding, card padding |
| `--space-xl` | `32px` | Page padding, large gaps |
| `--space-2xl` | `48px` | Section margins |

---

## Shadows

| Level | Value | Usage |
|-------|-------|-------|
| `--shadow-sm` | `0 1px 2px rgba(0,0,0,0.05)` | Subtle lift on sidebar items |
| `--shadow-md` | `0 4px 6px rgba(0,0,0,0.07)` | Cards, dropdowns |
| `--shadow-lg` | `0 10px 15px rgba(0,0,0,0.1)` | Modals, popovers |

---

## Icon System

- **Library:** Lucide Icons (via `lucide-svelte`)
- **Default size:** `w-5 h-5` (20px)
- **Sidebar icons:** `w-5 h-5` with `text-secondary` color, active: `text-primary`
- **Inline icons:** `w-4 h-4` (16px) next to text
- **No emojis as icons.** Ever.

### Icon Usage Map

| Context | Icon | Lucide Name |
|---------|------|-------------|
| Dashboard | Grid | `layout-dashboard` |
| Projects | Folder | `folder` |
| Packages | Package | `package` |
| Settings | Gear | `settings` |
| Wiki (disabled) | Book | `book-open` |
| Roadmap (disabled) | Map | `map` |
| Search | Magnifying glass | `search` |
| Create/Add | Plus | `plus` |
| Expand | Chevron down | `chevron-down` |
| Collapse sidebar | Left arrow | `panel-left-close` |
| Expand sidebar | Right arrow | `panel-left-open` |
| Send message | Send | `send` |
| GitHub link | External link | `external-link` |
| User avatar | User circle | `circle-user` |
| Organisation | Building | `building-2` |
| Brief | File text | `file-text` |
| Status | Badge | `badge` |
| See more | Arrow right | `arrow-right` |
| Back | Arrow left | `arrow-left` |
| Edit | Pencil | `pencil` |
| Close | X | `x` |
| Attach file | Paperclip | `paperclip` |
| Share URL | Link | `link` |
| Lightbulb / Idea | Lightbulb | `lightbulb` |
| Technique | Wand | `wand-sparkles` |
| Theme group | Layers | `layers` |
| Brainstorm | Sparkles | `sparkles` |
| Remove / Delete | Trash | `trash-2` |
| File uploaded | File | `file` |
| Collapse | Chevrons up-down | `chevrons-up-down` |
| Expand detail | Chevrons down-up | `chevrons-down-up` |
| Swap / Refresh | Refresh cw | `refresh-cw` |
| Check / Confirm | Check | `check` |

---

## Component Specs

### Buttons

| Variant | Background | Text | Border | Usage |
|---------|-----------|------|--------|-------|
| Primary (CTA) | `#0A3B85` | `white` | none | Create, Save actions |
| Secondary | `#F1F5F9` | `#0F172A` | none | Cancel, non-primary actions |
| Ghost | `transparent` | `#475569` | none | Sidebar items, toolbar actions |
| Destructive | `#EF4444` | `white` | none | Delete actions (future) |

**Common button properties:**
- Height: `h-10` (40px)
- Padding: `px-4` (16px)
- Border-radius: `rounded-lg` (8px)
- Font: `text-sm font-semibold`
- Transition: `transition-colors duration-200`
- `cursor-pointer` on all buttons

**shadcn mapping:** Use `Button` component with corresponding variants.

### Cards

| Type | Usage | Border | Shadow | Hover |
|------|-------|--------|--------|-------|
| Project card | Org dashboard project grid | `1px solid #E2E8F0` | `--shadow-md` | `--shadow-lg`, `translateY(-2px)` |
| Package row | Project dashboard package list | `1px solid #E2E8F0` | none | background `#F8FAFC` |
| Brief card | Project dashboard brief section | `1px solid #E2E8F0` | `--shadow-sm` | no hover (static) |
| Empty state card | Empty list states | `1px dashed #E2E8F0` | none | no hover |

**Common card properties:**
- Background: `#FFFFFF`
- Border-radius: `rounded-xl` (12px) for project cards, `rounded-lg` (8px) for package rows
- Padding: `p-6` (24px)
- `cursor-pointer` on interactive cards

**shadcn mapping:** Use `Card`, `CardHeader`, `CardTitle`, `CardDescription`, `CardContent`.

### Inputs

- Height: `h-10` (40px)
- Padding: `px-3` (12px)
- Border: `1px solid #E2E8F0`
- Border-radius: `rounded-lg` (8px)
- Font: `text-sm`
- Focus: `border-primary`, `ring-2 ring-primary/20`
- Placeholder: `text-slate-400`
- Background: `#FFFFFF`

**shadcn mapping:** Use `Input`, `Textarea`, `Label` components.

### Dropdowns / Popovers

- Trigger: breadcrumb segment with `chevron-down` icon
- Panel: `#FFFFFF` background, `rounded-lg`, `--shadow-lg`
- Search bar at top: standard input with search icon
- List items: `p-3`, hover `bg-muted`, active `bg-muted`
- "Create new" button at bottom: full-width ghost button with `plus` icon
- Max height: `max-h-80` with overflow scroll

**shadcn mapping:** Use `Popover`, `PopoverTrigger`, `PopoverContent` with custom list content.

### Status Badges

- Height: `h-6` (24px)
- Padding: `px-2.5` (10px)
- Border-radius: `rounded-full`
- Font: `text-xs font-medium`
- Colors: Status text color + status background color (see Status Colors table)
- No border

**shadcn mapping:** Use `Badge` component with custom color variants.

### Chat Bubbles

| Role | Alignment | Background | Border |
|------|-----------|-----------|--------|
| User | Right-aligned | `#0A3B85` (primary) | none |
| Assistant (echo) | Left-aligned | `#F1F5F9` (slate-100) | none |
| Assistant (brainstorm) | Left-aligned | `#F1F5F9` (slate-100) | none |

- Border-radius: `rounded-2xl` with directional corner cut (user: bottom-right, assistant: bottom-left)
- Padding: `px-4 py-3`
- Max width: `max-w-[70%]`
- Text: `text-sm`, user text `white`, assistant text `#0F172A`
- Timestamp: `text-xs text-slate-400` below bubble
- Animation: `animate-in fade-in slide-in-from-bottom-2 duration-200` on new messages

**Brainstorm assistant messages may contain:**
- Inline idea cards (compact variant — title + description only)
- Technique recommendation cards (technique name + description + "Use this" button)
- Theme grouping presentation (list of theme cards with ideas)
- Embedded file/URL references (attachment chips inline)

**Rich content within assistant bubbles:**
- Use `marked` or similar for markdown rendering within chat bubbles
- Code blocks: `bg-slate-900 text-slate-100 rounded-lg p-3 text-xs font-mono`
- Lists: standard markdown list rendering
- Nested cards: reduced padding (`p-3`), `mt-2` spacing from bubble text

### Chat Input

- Full-width at bottom of chat area
- `rounded-xl` textarea, auto-growing, `min-h-[44px]`, `max-h-[200px]`
- Send button: primary CTA color, `send` icon, disabled state when empty
- Attached to bottom: `sticky bottom-0` with white background + top border
- **Attachment area** (above textarea, inside sticky container):
  - Shows file/URL chips for pending attachments
  - Chips stack horizontally with `gap-2 flex-wrap`
  - Each chip has remove (`x`) button
- **Action buttons** (left of textarea, inline):
  - `paperclip` icon button: opens file picker
  - `link` icon button: opens URL input popover
  - Style: ghost buttons, `w-9 h-9`, disabled state during brainstorm non-facilitate phases

### Modals / Dialogs

- Overlay: `bg-black/50`, `backdrop-blur-sm`
- Panel: `#FFFFFF`, `rounded-2xl`, `--shadow-xl`, `max-w-md`
- Padding: `p-6`
- Title: `text-lg font-semibold`
- Close button: ghost with `x` icon, top-right

**shadcn mapping:** Use `Dialog`, `DialogContent`, `DialogHeader`, `DialogTitle`, `DialogDescription`.

### Search Bars

- Standard input with `search` icon prefix
- Border-radius: `rounded-lg`
- Placeholder: "Search..."
- Clear button: ghost with `x` icon when input has value

### Technique Picker Modal

A modal for browsing and selecting brainstorming techniques (62 available).

- Overlay and panel: standard modal specs from MASTER.md
- Panel width: `max-w-2xl` (wider than standard modals)
- Layout: two-column — left column is a scrollable list, right column shows detail of selected technique

**Left column (technique list):**
- Search bar at top: standard search spec
- Filter chips: horizontal row of category chips, `rounded-full px-3 py-1 text-xs`
  - Active chip: `bg-primary text-white`
  - Inactive chip: `bg-slate-100 text-slate-600 hover:bg-slate-200`
- Technique items: `p-3 rounded-lg cursor-pointer hover:bg-slate-50`
  - Active/selected: `bg-primary/5 border-l-2 border-primary`
  - Technique name: `text-sm font-semibold text-slate-900`
  - Technique category: `text-xs text-slate-400`
- Max height: `max-h-[400px] overflow-y-auto`

**Right column (technique detail):**
- Technique name: `text-base font-semibold text-slate-900`
- Category badge: status badge style
- Description: `text-sm text-slate-600`
- Best for: `text-sm text-slate-500` with italic label
- "Select Technique" button: primary CTA, full-width at bottom

**shadcn mapping:** `Dialog` + `Command` (for searchable list) + custom two-column layout.

### Idea Card

Displays a single brainstorm idea within the chat or detail views.

- Background: `#FFFFFF`
- Border: `1px solid #E2E8F0`
- Border-radius: `rounded-lg` (8px)
- Padding: `p-4`
- Layout: vertical stack
  - Title row: `lightbulb` icon + idea title (`text-sm font-semibold text-slate-900`)
  - Description: `text-sm text-slate-600 mt-1`
  - Footer: category tag + novelty indicator
    - Category: `text-xs font-medium px-2 py-0.5 rounded-full bg-slate-100 text-slate-600`
    - Novelty: `text-xs text-slate-400`
- No hover effect (non-interactive in chat), interactive in detail view with hover shadow

### Theme Card

Displays a group of ideas under a theme label.

- Background: `#FFFFFF`
- Border: `1px solid #E2E8F0`
- Border-radius: `rounded-xl` (12px)
- Padding: `p-5`
- Header row: `layers` icon + theme name (`text-base font-semibold text-slate-900`) + idea count badge (`text-xs text-slate-400`)
- Ideas list: stacked idea cards inside, `gap-2`, each with compact layout (title + description only)
- Collapsible: click header to toggle idea list visibility
  - Collapsed: shows header row + idea count only
  - Expanded: shows all ideas

### File/URL Attachment Chips

Shown in chat input area and in message bubbles for uploaded files and shared URLs.

**File chip:**
- Background: `bg-slate-100`
- Border-radius: `rounded-lg`
- Padding: `px-3 py-1.5`
- Layout: `file` icon + filename (`text-sm text-slate-700 truncate max-w-[200px]`) + `x` remove button
- Max width: `max-w-[280px]`

**URL chip:**
- Background: `bg-blue-50`
- Border-radius: `rounded-lg`
- Padding: `px-3 py-1.5`
- Layout: `link` icon + domain name (`text-sm text-primary truncate max-w-[200px]`) + `x` remove button
- Max width: `max-w-[280px]`

### Streaming / Typing Indicator

Replaces the stub behavior. Shown when the LLM is streaming a response.

- Alignment: left (assistant side)
- Content: animated dots or streaming text
- Dot indicator: 3 circles `w-2 h-2 rounded-full bg-slate-400` with `animate-bounce` and staggered delays (0ms, 150ms, 300ms)
- Background: `bg-slate-100 rounded-2xl rounded-bl-md px-4 py-3`
- When streaming text: show partial text with a blinking cursor (`animate-pulse` on a `w-0.5 h-4 bg-slate-900` element at the end of text)
- Max width: `max-w-[70%]` (same as assistant bubble)

---

## Navigation Patterns

### Top Bar (Global)

Always present (except first-time org creation — logo only).

```
┌────────────────────────────────────────────────────────────┐
│  [Logo]  [/ Acme Dev Team ▾]  [/ Thagid Web App ▾]  [👤] │
└────────────────────────────────────────────────────────────┘
```

- Height: `h-14` (56px)
- Background: `#FFFFFF`
- No border-bottom — uses `shadow-[0_1px_2px_rgba(0,0,0,0.06)]` instead
- Layout: `flex items-center justify-between px-4`
- Logo: icon.svg (`h-6 w-6`) + `<span class="font-brand text-lg text-primary">Thagid</span>`, clickable → org dashboard
- Breadcrumb segments: clickable dropdown triggers, separated by `/` in `text-slate-300`
- Avatar: `w-8 h-8 rounded-full`, right side, Google profile image or fallback initial

### Sidebar — Organisation Scope

```
┌──────────────────┐
│ 📁 Projects      │  ← active state highlighted
│ ⚙️ Org Settings  │
└──────────────────┘
```

- Section label at top: none (flat list)
- Active item: `bg-muted text-primary font-semibold`
- Inactive item: `text-secondary`, hover `bg-muted`
- Icons: `w-5 h-5` left of text

### Sidebar — Project Scope

```
┌──────────────────┐
│ 📊 Dashboard     │  ← top section
│ 📖 Wiki          │  ← disabled
│ 🗺️ Roadmap       │  ← disabled
│ ⚙️ Settings      │
│                  │
│ ─── Packages ─── │  ← section divider
│ 📦 v1.0 API      │
│ 📦 Auth Module   │
│ 📦 + Add Package │
└──────────────────┘
```

- Top section: navigation items (Dashboard, Wiki, Roadmap, Settings)
- Bottom section: "Packages" label + list + add button
- Divider: `border-t` between sections
- Disabled items: `text-slate-300 cursor-not-allowed`, no hover
- Package items: same style as nav items, with status dot indicator
- "Add Package": ghost button style, `plus` icon + text

---

## Animation & Transitions

| Context | Animation | Duration |
|---------|-----------|----------|
| Page transitions | Fade in | `200ms ease` |
| Sidebar collapse/expand | Width transition | `200ms ease` |
| Hover states | Background/shadow change | `150ms ease` |
| Modal open | Scale + fade | `200ms ease` |
| Chat message appear | Slide up + fade | `200ms ease` |
| Dropdown open | Scale from trigger | `150ms ease` |
| Loading states | Skeleton pulse | `1.5s infinite` |

All animations must respect `prefers-reduced-motion: reduce` → instant/no animation.

---

## Anti-Patterns (Do NOT Use)

- Heavy chrome or decorative elements
- Slow or missing response/loading feedback
- Emojis as icons — use Lucide SVG icons exclusively
- Missing `cursor-pointer` on clickable elements
- Layout-shifting hover effects (no scale on cards that affect layout)
- Text below 4.5:1 contrast ratio
- Instant state changes without transitions
- Invisible focus states — all interactive elements need visible focus rings
- Custom sidebar implementations — use shadcn `Sidebar` component
- Horizontal scroll on any page

---

## Pre-Delivery Checklist

- [ ] No emojis used as icons (Lucide only)
- [ ] `cursor-pointer` on all clickable elements
- [ ] Hover states with transitions (150-200ms)
- [ ] Light mode text contrast 4.5:1 minimum
- [ ] Focus states visible for keyboard navigation
- [ ] `prefers-reduced-motion` respected
- [ ] No content hidden behind fixed top bar (`pt-14` on sidebar content, `pt-14` on main content)
- [ ] No 1px solid borders between topbar/sidebar/content — use shadows and background differentiation
- [ ] Scope-aware sidebar renders correct content per scope level
- [ ] Empty states display correctly (no org, no project, no package)
- [ ] Breadcrumb dropdowns work (org switch, project switch)
- [ ] All forms have proper labels and focus management
- [ ] Chat bubbles differentiate user vs assistant clearly
- [ ] Technique picker modal search and filtering works
- [ ] File upload and URL sharing in chat input functional
- [ ] Streaming indicator shows during LLM response generation
- [ ] Brainstorm phase badge updates correctly through state machine
- [ ] Idea cards render properly within chat and detail views
- [ ] Theme cards are collapsible and show idea counts
