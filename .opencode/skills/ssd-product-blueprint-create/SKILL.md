---
name: ssd-product-blueprint-create
description: Creates a Product Blueprint from the distilled Product Brief through mandatory product-dream ideation, inline review, and SSD distillation.
---

# ssd-product-blueprint-create

Create `ssd_docs/2_product_blueprint.md`: the intended conceptual product shape expanded from the Product Brief for later SSD work.

Do not use BMad config/steps, hidden workflow variables, project artifact scanning, or existing planning docs.

## Contract

Input:

```json
{
  "product_brief_distillate": "optional; default ._ssd_docs_distil/_docs/1_product_brief.md",
  "initial_context": "optional additional user context"
}
```

Rules:

- Always run one internal guided product-dream brainstorm; no `headless`, `autonomous`, `yolo`, or `draft-first` modes.
- Return structured `precondition_failed` if the Product Brief distillate is missing.
- Return structured `skipped` if `ssd_docs/2_product_blueprint.md` exists.
- Do not ask a questionnaire before the mandatory brainstorm.
- Run at most one optional supplemental ideation pass unless the user explicitly asks for more.
- Write final `ssd_docs/2_product_blueprint.md` exactly once, after inline review.
- Return `blocked` only for tool, distillation, or file-operation failure after start.

## Paths

- Brief distillate: `._ssd_docs_distil/_docs/1_product_brief.md`
- Product dream brainstorm folder: `_docs/2_product_blueprint/product_dream`
- Product dream brainstorm distillate: `._ssd_docs_distil/brainstorming/_docs/2_product_blueprint/product_dream/<filename>`
- Optional supplemental brainstorm folder: `_docs/2_product_blueprint/product_refinement`
- Optional supplemental brainstorm distillate: `._ssd_docs_distil/brainstorming/_docs/2_product_blueprint/product_refinement/<filename>`
- Template: `.opencode/skills/ssd-product-blueprint-create/templates/product-blueprint-template.md`
- Temp draft: `._ssd_docs_temp/_docs/2_product_blueprint.md`
- Final: `ssd_docs/2_product_blueprint.md`
- Final distillate: `._ssd_docs_distil/_docs/2_product_blueprint.md`

## Artifact Boundary

Include: product definition, boundaries, in/out scope, major capability areas, capability purposes, conceptual capabilities, product principles, cross-cutting concerns, assumptions, major unknowns.

Exclude: requirements, user stories, acceptance criteria, architecture, stack, data models, API design, MVP scope, roadmap, delivery sequencing, work packages, engineering tasks, and success metrics used as planning criteria.

If the product is a technical tool, allow only product-level value, problem, audience, concept, boundaries, and capabilities; no implementation detail.

## Workflow

### 1. Preflight

Resolve `product_brief_distillate` to input or default.

If missing, return only:

```json
{
  "status": "precondition_failed",
  "reason": "Product brief distillate is required before creating a Product Blueprint.",
  "expected": "._ssd_docs_distil/_docs/1_product_brief.md",
  "required_action": "Run the product brief creation flow first."
}
```

If `ssd_docs/2_product_blueprint.md` exists, return only:

```json
{
  "status": "skipped",
  "reason": "Product Blueprint already exists.",
  "product_blueprint": "ssd_docs/2_product_blueprint.md"
}
```

### 2. Frame

State that this creates the Product Blueprint: the product dream and conceptual definition of what is being built. It avoids requirements, architecture, MVP scope, roadmap, delivery sequencing, and engineering tasks.

### 3. Mandatory Product Dream Brainstorm

Read the brief distillate. Call `ssd-brainstorming`:

```json
{
  "run_mode": "internal",
  "topic": "product name or area from brief",
  "initial_context": "brief distillate content plus optional initial_context",
  "scope": "normal",
  "target_ideas": 50,
  "target_folder": "_docs/2_product_blueprint/product_dream",
  "downstream_consumer": "ssd-product-blueprint-create",
  "mode": "guided",
  "goal": "Explore the product dream and define what is being built at a conceptual level: product shape, boundaries, major capabilities, product principles, cross-cutting concerns, assumptions, and unknowns.",
  "constraints": "Stay within the Product Blueprint boundary. Avoid requirements, user stories, acceptance criteria, architecture, stack, data models, API design, MVP scope, roadmap, delivery sequencing, work packages, and engineering tasks."
}
```

Do not pass `required_techniques` or fixed `techniques`. Let `ssd-brainstorming` select techniques. Use the returned brainstorm distillate as source material.

### 4. Draft Temp Blueprint

Draft `._ssd_docs_temp/_docs/2_product_blueprint.md` from the Product Brief distillate, mandatory product dream brainstorm distillate, and optional user context. Preserve heading order, replace placeholders, remove guidance text, remove the optional source-material line if supplemental ideation was not used, use only source-backed content, and use `Unknown` or explicit assumptions instead of invention. Keep capabilities conceptual.

### 5. Inline Review Gate

Review the temp draft inside this skill. Do not call Product Blueprint review subagents.

The temp draft cannot be finalized while it has:

- invented unsupported specificity;
- vague product definition;
- weak, missing, overlapping, or contradictory boundaries;
- capability areas that are too granular, vague, overlapping, or written as requirements;
- missing capability purposes;
- generic principles that do not guide tradeoffs;
- cross-cutting concerns that prescribe architecture or implementation;
- assumptions presented as facts;
- trivial, overly technical, or non-product-shaping unknowns;
- unresolved contradiction with source material;
- MVP, roadmap, delivery, metric, architecture, stack, data model, API, work-package, or engineering-task drift.

### 6. Optional Supplemental Ideation

Recommend one supplemental ideation pass only if the reviewed draft is still thin, vague, generic, conflicted, or assumption-heavy. The user may decline. This does not replace the mandatory product dream brainstorm.

Use this style:

```text
The Product Blueprint is still thin in a few important areas. I recommend one supplemental ideation pass to strengthen the product shape before finalizing. Do you want to run that now?
```

If accepted, call `ssd-brainstorming` once with:

```json
{
  "run_mode": "internal",
  "topic": "product name or area from brief",
  "initial_context": "brief distillate plus product dream brainstorm distillate plus temp draft review notes plus optional initial_context",
  "scope": "quick",
  "target_folder": "_docs/2_product_blueprint/product_refinement",
  "downstream_consumer": "ssd-product-blueprint-create",
  "mode": "guided",
  "goal": "Strengthen weak, vague, conflicted, or assumption-heavy areas in the Product Blueprint while staying conceptual.",
  "constraints": "Stay within the Product Blueprint boundary. Avoid requirements, user stories, acceptance criteria, architecture, stack, data models, API design, MVP scope, roadmap, delivery sequencing, work packages, and engineering tasks."
}
```

Do not pass `required_techniques` or fixed `techniques`. Let `ssd-brainstorming` select techniques. Use the returned brainstorm distillate as additional source material.

### 7. Revise Temp Blueprint

Apply clear inline review fixes directly to `._ssd_docs_temp/_docs/2_product_blueprint.md`. If supplemental ideation was used, incorporate its distillate where source-backed.

Ask the user only when a finding requires a strategic choice: product identity, boundary, capability grouping, principle tradeoff, source contradiction, or assumption include/remove. If the user does not know, record `Unknown`, an explicit assumption, or a major unknown.

### 8. Finalize Once

Re-check `ssd_docs/2_product_blueprint.md`; if it exists, return `skipped`. Otherwise create it exactly once from the reviewed temp draft.

### 9. Distill Final

Call `ssd_distillator` exactly with:

```json
{
  "source_documents": ["ssd_docs/2_product_blueprint.md"],
  "downstream_consumer": "PRD creation, architectural analysis, MVP definition, roadmap creation, and work package decomposition",
  "output_path": "._ssd_docs_distil/_docs/2_product_blueprint.md",
  "audit": false
}
```

The caller provides the output path; the distillator must not guess. Final distillation is mandatory. Audit is disabled for this workflow, so audit fix passes are not used.

### 10. Return

On success only:

```json
{
  "status": "complete",
  "product_blueprint": "ssd_docs/2_product_blueprint.md",
  "ideation_used": true,
  "supplemental_ideation_used": false,
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
    "product_dream_brainstorm_raw": "path or null",
    "product_dream_brainstorm_distillate": "path or null",
    "supplemental_brainstorm_raw": "path or null",
    "supplemental_brainstorm_distillate": "path or null",
    "product_blueprint_draft": "path or null",
    "product_blueprint": "path or null"
  },
  "required_action": "Resolve the failed tool run and retry the skill.",
  "warnings": []
}
```

## Hard Stops

- Do not read or use original source docs such as `ssd_docs/1_product_brief.md`; use only the Product Brief distillate, this workflow's brainstorm distillates, clarification notes, temp draft, and final blueprint.
- Do not call BMad skills.
- Do not overwrite/edit `ssd_docs/2_product_blueprint.md`.
- Do not skip the mandatory product dream brainstorm, inline review, or final distillation.
- Do not run more than one optional supplemental ideation pass unless the user explicitly asks.
- Do not hand-write final distillates unless explicitly asked for best-effort output after distillator failure.
