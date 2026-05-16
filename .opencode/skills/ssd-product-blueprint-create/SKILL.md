---
name: ssd-product-blueprint-create
description: Creates a SQLite-backed Product Blueprint from Product Brief memory through collaborative product-dream ideation, user-validated section review, and memory storage.
---

# ssd-product-blueprint-create

Create Product Blueprint memory: the intended conceptual product shape expanded from Product Brief memory for later SSD work.

Act as a product-shaping sparring partner, not a blind document writer. Explore boundaries, capability shape, principles, assumptions, and unknowns before storage.

Do not use BMad config/steps, hidden workflow variables, artifact scanning, existing planning docs, or markdown Product Blueprint files.

## Contract

Input:

```json
{
  "initial_context": "optional additional user context"
}
```

Rules:

- Read and apply `.opencode/shared/product-blueprint-contract.md` first.
- Always run one internal guided product-dream brainstorm; no `headless`, `autonomous`, `yolo`, or `draft-first` modes.
- Return structured `precondition_failed` if Product Brief memory is missing.
- Return structured `skipped` if Product Blueprint memory already exists.
- Do not ask a questionnaire before mandatory brainstorming; use facilitation and focused follow-up.
- Ask once near the start whether to include existing stored memory or files as source material.
- Read files directly and include them as `source_files`; load stored artifacts through `.opencode/shared/recipes.md` plus the matching recipe, confirm selection, then include as `source_artifacts`.
- Run supplemental ideation only when inline review recommends it or the user explicitly asks. Repeat only when explicitly requested.
- Write Product Blueprint memory exactly once, after internal review and explicit approval, through `.opencode/scripts/ssd_product_blueprint/memory.py create`.
- Do not create Product Blueprint markdown or temp drafts.
- Return `blocked` only for tool or memory-command failure after start.

## Memory

- Product Brief memory adapter: `.opencode/scripts/ssd_product_brief/memory.py`
- Shared contract: `.opencode/shared/product-blueprint-contract.md`
- Artifact recipe index: `.opencode/shared/recipes.md`
- Product Blueprint memory adapter: `.opencode/scripts/ssd_product_blueprint/memory.py`
- Artifact kind: `product-blueprint`
- Artifact ID: UUID returned by memory command
- Brainstorm source material: execute `memory_handoff.command` returned by `ssd-brainstorming`
- Product Brief source brainstorms: load `cited_brainstorm_ids` from Product Brief memory with role `product_brief_source`
- Extra sources: persist artifact/file provenance through `source_artifacts` and `source_files`

## Artifact Boundary

Include product definition, in/out-of-scope boundaries, major capability areas and purposes, conceptual capabilities, product principles, cross-cutting concerns, assumptions, and major unknowns.

Exclude requirements, user stories, acceptance criteria, architecture, stack, data models, API design, MVP scope, roadmap, delivery sequencing, work packages, engineering tasks, and success metrics used as planning criteria. For technical tools, keep only product-level value, problem, audience, concept, boundaries, and capabilities.

## Required Sections

Use these exact section keys:

- `product-definition`
- `in-scope`
- `out-of-scope`
- `major-capabilities`
- `product-principles`
- `cross-cutting-concerns`
- `assumptions`
- `major-unknowns`

## Workflow

### 1. Preflight

Read Product Brief memory:

```text
python .opencode/scripts/ssd_product_brief/memory.py get
```

If missing, return only:

```json
{
  "status": "precondition_failed",
  "reason": "Product Brief memory is required before creating a Product Blueprint.",
  "expected": "Product Brief artifact with kind `product-brief` and current sections",
  "required_action": "Run ssd-product-brief-create first."
}
```

Check for existing Product Blueprint memory:

```text
python .opencode/scripts/ssd_product_blueprint/memory.py get
```

If it exists, return only:

```json
{
  "status": "skipped",
  "reason": "Product Blueprint already exists.",
  "artifact_kind": "product-blueprint",
  "artifact_id": "<uuid>"
}
```

If missing, ask:

```text
Any existing stored memory object or file you want to include as source material for this Product Blueprint?
```

For files, read directly and add `source_files` entries with `path`, optional `title`, and role `extra_source`; the adapter snapshots/cites them. For stored artifacts, use recipes, confirm selection, add sections to source context, and add `source_artifacts` entries with `artifact_id`, `kind`, and role `extra_source`.

If Product Brief memory returns `cited_brainstorm_ids`, load each before mandatory ideation:

```text
python .opencode/scripts/ssd_brainstorming/memory.py ideas --brainstorm-id <brainstorm_id>
```

Use loaded brainstorm metadata/ideas as source context with role `product_brief_source`. If one cannot load, warn and continue only if Product Brief sections remain usable.

### 2. Frame

State that Product Blueprint captures the product dream and conceptual definition, avoiding requirements, architecture, MVP scope, roadmap, delivery sequencing, and engineering tasks.

State that collaboration includes assumption challenges, options, and focused questions for strategic product choices, and memory is written only after section review and approval.

### 3. Mandatory Product Dream Brainstorm

Use Product Brief sections, loaded Product Brief source brainstorms, extra sources, and optional `initial_context`. Call `ssd-brainstorming`:

```json
{
  "run_mode": "internal",
  "topic": "product name or area from Product Brief memory",
  "initial_context": "Product Brief sections plus loaded Product Brief source brainstorms plus extra sources plus optional initial_context",
  "scope": "normal",
  "target_ideas": 50,
  "downstream_consumer": "ssd-product-blueprint-create",
  "mode": "guided",
  "goal": "Explore the product dream and conceptual product shape: definition, boundaries, major capabilities, principles, cross-cutting concerns, assumptions, and unknowns.",
  "constraints": "Stay within Product Blueprint boundary. Avoid requirements, stories, acceptance criteria, architecture, stack, data models, API design, MVP scope, roadmap, delivery sequencing, work packages, engineering tasks, and success metrics. Return memory references and memory_handoff, not markdown paths."
}
```

Do not pass `required_techniques` or fixed `techniques`; let `ssd-brainstorming` select. `run_mode=internal` remains interactive and user-led: do not generate the product dream silently, and capture only user input, user edits, or user-approved AI suggestions.

Execute `memory_handoff.command` and use returned brainstorm metadata/ideas as source material. Mandatory product-dream ideation is required even when Product Brief source brainstorms exist.

Record this source as:

```json
{
  "brainstorm_id": "<brainstorm_id>",
  "role": "product_dream",
  "handoff_command": ["<memory_handoff.command>"]
}
```

### 4. Draft Section Payload

Draft a JSON-compatible Product Blueprint section payload in working context from Product Brief memory, mandatory product-dream memory, direct user input, extra sources, and optional context. Use only source-backed content; use `Unknown` or explicit assumptions instead of invention. Keep capabilities conceptual.

### 5. Inline Review Gate

Review the payload inside this skill. Do not call Product Blueprint review subagents.

Apply shared contract blockers, especially: unsupported specificity, vague definition, weak/overlapping/contradictory boundaries, requirement-like capabilities, missing capability purposes, generic principles, implementation-prescribing concerns, assumptions as facts, trivial/technical unknowns, source contradictions, or MVP/roadmap/delivery/metric/architecture/engineering drift.

### 6. Optional Supplemental Ideation

Recommend supplemental ideation only if review finds the payload thin, vague, generic, conflicted, or assumption-heavy. The user may decline; this never replaces mandatory product-dream ideation.

Use:

```text
The Product Blueprint is still thin in a few important areas. I recommend one supplemental ideation pass to strengthen the product shape before finalizing. Do you want to run that now?
```

If accepted, call `ssd-brainstorming`:

```json
{
  "run_mode": "internal",
  "topic": "product name or area from Product Brief memory",
  "initial_context": "Product Brief sections plus product dream brainstorm output plus review notes plus optional initial_context",
  "scope": "quick",
  "downstream_consumer": "ssd-product-blueprint-create",
  "mode": "guided",
  "goal": "Strengthen weak, vague, conflicted, or assumption-heavy areas in the Product Blueprint while staying conceptual.",
  "constraints": "Stay within Product Blueprint boundary. Avoid requirements, stories, acceptance criteria, architecture, stack, data models, API design, MVP scope, roadmap, delivery sequencing, work packages, engineering tasks, and success metrics. Return memory references and memory_handoff, not markdown paths."
}
```

Execute `memory_handoff.command`, use returned metadata/ideas as source material, and append each supplemental brainstorm with role `supplemental`. Repeat only when the user explicitly asks for more.

### 7. Revise Section Payload

Apply inline review fixes directly in working context. Incorporate supplemental ideation only where source-backed.

Ask the user only when a strategic choice is required: product identity, boundary, capability grouping, principle tradeoff, source contradiction, or assumption include/remove. If unknown, record `Unknown`, an assumption, or a major unknown.

### 8. User Section Validation Gate

Present every proposed Product Blueprint section in human-readable Markdown before writing memory. Also show source Product Brief, source brainstorms, extra artifacts/files, assumptions to store, and major unknowns to keep unresolved.

Use this final prompt:

```text
Review these Product Blueprint sections. Reply with approval to create it, or tell me what to change by section.
```

Do not call `create` until explicit approval after review. Approval must be affirmative (`approved`, `create it`, `looks good`, or equivalent). Clarification, discussion, or source selection is not approval. If changes are requested, revise and repeat this gate.

### 9. Revise From User Review

If the user requests changes, apply clear fixes in working context and repeat the User Section Validation Gate. If approved, finalize.

### 10. Finalize Once

After approval, re-check Product Blueprint memory. If it exists, return `skipped`. Otherwise pass the approved payload on stdin:

```text
python .opencode/scripts/ssd_product_blueprint/memory.py create
```

Payload shape:

```json
{
  "change_summary": "Initial Product Blueprint",
  "product_brief_artifact_id": "<uuid>",
  "sections": {
    "product-definition": "...",
    "in-scope": "...",
    "out-of-scope": "...",
    "major-capabilities": "...",
    "product-principles": "...",
    "cross-cutting-concerns": "...",
    "assumptions": "...",
    "major-unknowns": "..."
  },
  "source_brainstorms": [],
  "source_artifacts": [],
  "source_files": [],
  "cited_idea_ids": []
}
```

### 11. Return

On success only:

```json
{
  "status": "complete",
  "artifact_kind": "product-blueprint",
  "artifact_id": "<uuid>",
  "product_brief_artifact_id": "<uuid>",
  "source_brainstorms": [],
  "cited_idea_ids": [],
  "ideation_used": true,
  "supplemental_ideation_count": 0,
  "warnings": []
}
```

On runtime failure only:

```json
{
  "status": "blocked",
  "reason": "specific failure",
  "failed_step": "step name",
  "partial_outputs": {
    "source_brainstorms": [],
    "section_payload_started": true
  },
  "required_action": "Resolve the failed tool run and retry the skill.",
  "warnings": []
}
```

## Hard Stops

- Do not read or use Product Brief markdown; use Product Brief memory only.
- Do not call BMad skills.
- Do not create, overwrite, edit, read, or depend on `ssd_docs/2_product_blueprint.md`.
- Do not create temp Product Blueprint markdown.
- Do not skip mandatory product-dream brainstorming or inline review.
- Do not skip user-facing section validation.
- Do not write Product Blueprint memory before explicit user approval.
- Do not output only JSON or a tool result as the user-facing review or final response.
