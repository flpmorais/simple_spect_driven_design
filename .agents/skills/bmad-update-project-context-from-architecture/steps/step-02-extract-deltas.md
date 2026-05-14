# Step 2: Extract Architecture Deltas

## Rules

- Speak in `{communication_language}`.
- Do not modify any file in this step.
- Extract durable rules, not implementation narrative.
- Preserve existing project-context rules unless explicitly superseded.

## Extract Durable Rule Candidates

From `architecture.md`, extract only rules that should guide future implementation across stories or work packages:

- Technology stack changes or additions.
- Architecture patterns and layer boundaries.
- Service/module ownership rules.
- API contract and data-shape rules.
- Data storage, migration, or persistence rules.
- Auth, security, and tenant-scoping rules.
- Frontend/backend integration rules.
- Testing and validation rules.
- Deployment, container, or runtime topology rules.
- Explicit anti-patterns or forbidden approaches.

Ignore unless they generalize into durable rules:

- Diagrams.
- Rationale paragraphs.
- Story sequencing.
- One-off file names.
- Work-package implementation checklist items.
- Local details that do not constrain future agents.

## Classify Each Finding

Classify each candidate into exactly one bucket:

- `add`: new durable rule not already represented in project context.
- `reinforce`: architecture restates an existing project-context rule.
- `replace`: architecture explicitly replaces an existing rule.
- `remove`: architecture explicitly removes or deprecates an existing rule.
- `local_only`: useful for the work package but not project-context material.
- `conflict`: contradicts project context without explicit supersession.

Replacement/removal evidence must be explicit, such as:

- "replace X with Y"
- "deprecate X"
- "remove X"
- "no longer use X"
- "X is superseded by Y"

## Prepare Proposed Merge

Prepare a concise proposed merge summary:

```markdown
## Proposed Project Context Update

### Add

### Reinforce

### Replace

### Remove

### Local Only / Ignored

### Conflicts Requiring Decision
```

For each item include:

- proposed concise rule text, when applicable
- existing project-context rule affected, when applicable
- source evidence from `architecture.md`

Then load `./step-03-review-changes.md`.
