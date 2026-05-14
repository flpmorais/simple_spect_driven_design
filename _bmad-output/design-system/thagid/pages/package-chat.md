# Package Chat

> Overrides MASTER.md for the package chat interface.

---

## Package Chat View

**Route:** `/project/{projectId}/package/{packageId}`
**Sidebar:** Project scope (package highlighted in packages list)
**Top bar:** Logo / [Org dropdown] / [Project dropdown]

### Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Package Title                      [Phase Badge]  [Status] │
│  Package description text                                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Welcome! I'm your AI assistant for this package.     │  │
│  │  How can I help?                                      │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│                     ┌──────────────────────────┐            │
│                     │  What should the API     │            │
│                     │  endpoints be?           │            │
│                     └──────────────────────────┘            │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Here are some techniques I recommend:                │  │
│  │  ┌─ Technique Card ─────────────────────────────┐     │  │
│  │  │  SCAMPER — Creative Problem Solving           │     │  │
│  │  │  Best for evolving existing concepts          │     │  │
│  │  │                                [Use this]     │     │  │
│  │  └───────────────────────────────────────────────┘     │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  📎 notes.md  🔗 example.com                     [x] [x]   │
│  [📎] [🔗]  [Type a message...                    ] [Send]  │
└─────────────────────────────────────────────────────────────┘
```

### Chat Header

- Sticky at top of content area
- Height: `h-16`
- Content: package title (`text-base font-semibold`) + status badge (right)
- Description: `text-sm text-slate-500` below title (if space allows)
- **Brainstorm phase badge:** shown when brainstorm session is active
  - Position: between title and status badge
  - Style: status badge using brainstorm phase colors from MASTER.md
  - Text: current phase name (Initiate, Facilitate, Extract, Validate, Markdown)
- Border-bottom: `border-b border-slate-200`

### Message Area

- `flex-1 overflow-y-auto p-6`
- Messages displayed vertically with `gap-4`
- Auto-scrolls to bottom on new message
- Welcome message: assistant message shown by default when chat is empty

### Chat Bubbles

**User message:**
- Alignment: `ml-auto` (right-aligned)
- Background: `bg-primary` (#0A3B85)
- Text color: `white`
- Border-radius: `rounded-2xl rounded-br-md` (bottom-right corner cut)
- Padding: `px-4 py-3`
- Max width: `max-w-[70%]`
- **File/URL attachments:** shown as chips above bubble text
  - File chip: `bg-white/20 text-white rounded-lg px-2.5 py-1 text-xs`
  - URL chip: `bg-white/20 text-white rounded-lg px-2.5 py-1 text-xs`

**Assistant message (echo):**
- Alignment: `mr-auto` (left-aligned)
- Background: `bg-slate-100`
- Border: `border border-slate-200`
- Text color: `#0F172A` (text-primary)
- Border-radius: `rounded-2xl rounded-bl-md` (bottom-left corner cut)
- Padding: `px-4 py-3`
- Max width: `max-w-[70%]`

**Assistant message (brainstorm agent):**
- Same base style as echo assistant message
- May contain rich content within the bubble:
  - **Technique recommendation card:** compact card with technique name, short description, "Use this" button (ghost button, `text-xs`)
  - **Inline idea card:** `bg-white border border-slate-200 rounded-lg p-3 mt-2` — shows idea title + description
  - **Theme grouping presentation:** multiple theme cards stacked vertically
    - Each theme: `bg-white border border-slate-200 rounded-lg p-3 mt-2`
    - Theme name: `text-sm font-semibold text-slate-900`
    - Ideas under theme: bulleted list, `text-sm text-slate-600`
  - **Markdown content:** rendered markdown within bubble
    - Headings: `text-sm font-semibold text-slate-900`
    - Lists: standard list rendering with `list-disc` / `list-decimal`
    - Code: `bg-slate-200 rounded px-1 text-xs font-mono`

**Message animation:** `animate-in fade-in slide-in-from-bottom-2 duration-200`

### Streaming Indicator

When the brainstorm agent is generating a response:
- Show 3-dot bounce animation: `w-2 h-2 rounded-full bg-slate-400` with `animate-bounce`
- Staggered delays: `delay-0`, `delay-150`, `delay-300`
- Background: same as assistant bubble (`bg-slate-100 rounded-2xl rounded-bl-md px-4 py-3`)
- Replace dots with streaming text as tokens arrive
- Blinking cursor at end of partial text: `w-0.5 h-4 bg-slate-900 animate-pulse`

### Empty Chat State

Before any messages, show a single assistant welcome message:

**Regular chat:**
> "Welcome! I'm your AI assistant for this package. How can I help you define your release?"

**Brainstorm agent (no active session):**
> "I'm your brainstorm facilitator. I can help you generate and organize ideas for this package. Want to start a brainstorm session?"

This message is pre-populated, not sent by user.

### Chat Input Area

- Sticky at bottom: `sticky bottom-0 bg-white border-t border-slate-200 p-4`
- **Attachment area** (above textarea, conditionally visible):
  - Shows when files or URLs are attached
  - Horizontal row of chips with `gap-2 flex-wrap`
  - File chip: `bg-slate-100 rounded-lg px-3 py-1.5` + `file` icon + filename + `x` remove
  - URL chip: `bg-blue-50 rounded-lg px-3 py-1.5` + `link` icon + domain + `x` remove
  - Max width per chip: `max-w-[280px]`
- **Input row:** `flex items-end gap-2`
  - `paperclip` button: ghost, `w-9 h-9`, opens native file picker
  - `link` button: ghost, `w-9 h-9`, opens URL input popover (small input + "Add" button)
  - Textarea: `rounded-xl border border-slate-200 focus:border-primary focus:ring-2 focus:ring-primary/20`
    - Auto-growing: `min-h-[44px] max-h-[200px]`
    - Placeholder: "Type a message..."
    - `resize-none`
    - `flex-1`
  - Send button:
    - Icon: `send` icon
    - Color: primary (`#0A3B85`) when input has text, slate-300 when empty
    - Disabled when input is empty or whitespace-only
    - `cursor-pointer`

### Keyboard Shortcuts

- `Enter` → send message
- `Shift+Enter` → new line in textarea

---

## Brainstorm-Specific Interactions

### Technique Picker (In-Chat)

The brainstorm agent recommends techniques in its opening message. The user can:
1. Accept a recommended technique via "Use this" button on technique card
2. Browse all techniques via technique picker modal

**Trigger:** `wand-sparkles` icon button in chat header (visible only during brainstorm) OR "Browse all techniques" link in agent message

**Technique picker modal:** See MASTER.md → Technique Picker Modal

### Technique Swap Mid-Session

- User can swap techniques during facilitation
- Agent shows a confirmation message: "Switching to [technique]. Your existing ideas will be kept."
- Triggered via technique picker modal or natural language ("let's try a different technique")
- Phase badge does not change (stays "Facilitate")

### File Upload

- User clicks `paperclip` icon or drags file onto chat input
- Accepted formats: `.md`, `.txt`, `.csv`, `.json` (text-based files for MVP)
- File appears as chip in attachment area
- On send: file content is ingested by the agent
- Agent acknowledges ingestion in response: "I've reviewed your file '[filename]'. [Summary of content]"

### URL Sharing

- User clicks `link` icon → URL input popover appears
- Popover: small input (`type="url"`) + "Add" button
- URL appears as chip in attachment area
- On send: URL content is fetched by the agent
- Agent acknowledges: "I've pulled content from [domain]. [Summary]"

### Theme Grouping (Conclude Phase)

When user says "done" or indicates completion:
1. Agent presents all ideas grouped into themes
2. Each theme is a collapsible card (see MASTER.md → Theme Card)
3. User can:
   - Drag ideas between themes (future — for MVP, text-based adjustments)
   - Reply with adjustments ("Move idea X to theme Y", "Rename theme Z")
   - Confirm by saying "looks good" or clicking a "Confirm" button
4. On confirmation, extraction begins (phase changes to "Extract")

---

## Package Creation

**Route:** `/project/{projectId}/package/new`
**Sidebar:** Project scope

See `forms.md` for form patterns.
