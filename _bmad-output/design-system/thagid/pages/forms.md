# Forms — Create & Edit Patterns

> Shared form patterns for all CRUD screens: org, project, and package creation/edit.

---

## Form Shell

All creation/edit forms share this structure:

```
┌─────────────────────────────────────┐
│  [Title]                            │
│  [Description]                      │
│                                     │
│  Field Label                        │
│  ┌─────────────────────────────────┐│
│  │ Input                           ││
│  └─────────────────────────────────┘│
│                                     │
│  Field Label                        │
│  ┌─────────────────────────────────┐│
│  │ Textarea                        ││
│  └─────────────────────────────────┘│
│                                     │
│       [Cancel]  [Create]            │
└─────────────────────────────────────┘
```

- Max width: `max-w-lg`
- Centered in main content area: `mx-auto py-12`
- No card wrapper — form sits directly on page background

### Form Title

- Create mode: `text-2xl font-bold text-slate-900` — "Create Project" / "Create Package" / "Create Organisation"
- Edit mode: `text-2xl font-bold text-slate-900` — "Edit Project" / "Organisation Settings"

### Form Description

- `text-sm text-slate-500 mt-1 mb-6`
- Create mode: Brief guidance text
- Edit mode: none or "Update your project details."

---

## Field Patterns

### Standard Input

```
Label
┌─────────────────────────────────┐
│ Placeholder text                │
└─────────────────────────────────┘
Helper text (optional)
```

- Label: `text-sm font-medium text-slate-700 mb-1.5`
- Input: standard input spec from MASTER.md
- Helper text: `text-xs text-slate-400 mt-1`
- Required: red asterisk on label (optional for MVP since all fields are required)
- Error state: `border-red-500 text-red-500` + error message below
- Field spacing: `mb-5` between fields

**shadcn mapping:** `Label` + `Input`

### Textarea

Same as standard input but with:
- `min-h-[80px]`
- `resize-none`
- Textarea element instead of input

**shadcn mapping:** `Label` + `Textarea`

### URL Input

Same as standard input with:
- `type="url"`
- Placeholder: `https://github.com/...`

---

## Button Bar

- Layout: `flex justify-end gap-3 mt-8`
- Cancel: secondary button variant
- Submit: primary CTA button variant
  - Create mode: "Create [Entity]" with `plus` icon
  - Edit mode: "Save Changes"
- Submit shows loading state during request: `disabled` + spinner or text change

---

## Specific Forms

### Organisation Create / Edit

| Field | Type | Required | Placeholder |
|-------|------|----------|-------------|
| Name | Input | Yes | "e.g., Acme Dev Team" |

### Project Create / Edit

| Field | Type | Required | Placeholder |
|-------|------|----------|-------------|
| Name | Input | Yes | "e.g., Thagid Web App" |
| Description | Textarea | Yes | "Describe your project..." |
| GitHub Project URL | URL Input | Yes | "https://github.com/orgs/.../projects/..." |
| GitHub Repo URL | URL Input | Yes | "https://github.com/org/repo" |

### Package Create

| Field | Type | Required | Placeholder |
|-------|------|----------|-------------|
| Title | Input | Yes | "e.g., v1.0 — Core API" |
| Description | Textarea | Yes | "Describe this package..." |

---

## Validation

- Client-side validation on blur and on submit
- Required fields: "This field is required"
- URL fields: "Please enter a valid URL"
- Error messages: `text-xs text-red-500 mt-1`
- Error styling: input border `border-red-500`
- Form does not submit with validation errors
