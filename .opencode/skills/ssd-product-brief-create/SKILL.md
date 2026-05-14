---
name: ssd-product-brief-create
description: Create the first foundational product brief for a project through focused discovery, optional ideation, inline review, and mandatory SSD distillation.
---

# ssd-product-brief-create

Use when the user asks to create the first product brief, define a new product at a high level, or produce the foundational product definition for a project.

This is OpenCode-native. Do not use BMad config, BMad step files, hidden workflow variables, project artifact scanning, or existing planning docs.

## Contract

Input:

```json
{
  "product_or_problem_area": "required unless obvious",
  "initial_context": "optional seed context or user brain dump"
}
```

Rules:

- Read and apply `.opencode/shared/product-brief-contract.md` before proceeding.
- Always guided. Do not offer `headless`, `autonomous`, `yolo`, or `draft-first` modes.
- If `product_or_problem_area` is missing, ask only: "What product, project, or problem area should we explore for the product brief?"
- If `ssd_docs/1_product_brief.md` exists, stop. This skill creates only; editing belongs to `ssd-product-brief-edit`.
- Write final `ssd_docs/1_product_brief.md` exactly once, after inline review.
- Run at most one optional ideation pass unless the user explicitly asks for more.

## Paths

- Shared contract: `.opencode/shared/product-brief-contract.md`
- Optional product brainstorm folder: `_docs/1_product_brief/product`
- Optional product brainstorm distillate: `._ssd_docs_distil/brainstorming/_docs/1_product_brief/product/<filename>`
- Product brief template: `.opencode/skills/ssd-product-brief-create/templates/product-brief-template.md`
- Temp draft: `._ssd_docs_temp/_docs/1_product_brief.md`
- Final brief: `ssd_docs/1_product_brief.md`
- Final brief distillate: `._ssd_docs_distil/_docs/1_product_brief.md`

## Workflow

### 1. Frame

Briefly state that this creates a foundational product definition and will avoid technical planning, PRD requirements, MVP scope, roadmap, success metrics, epics, stories, delivery planning, and implementation detail.

### 2. Focused Discovery

Use `initial_context` first. Gather only enough information to draft the required sections from the shared contract.

Do not run a questionnaire by default. Ask at most 3 focused questions only when the brief would otherwise be too speculative. If the user does not know, record `Unknown` or a named assumption and continue.

### 3. Optional Ideation

Recommend a short ideation pass when the shared contract's optional ideation rule applies. The user may decline.

Use this style:

```text
The product direction is still thin. I recommend a short ideation pass before drafting so the brief has stronger problem, audience, and differentiation material. Do you want to run that now?
```

If accepted, call `ssd-brainstorming` once with:

```json
{
  "run_mode": "internal",
  "topic": "<product_or_problem_area>",
  "initial_context": "<initial_context plus focused discovery notes>",
  "scope": "quick",
  "target_folder": "_docs/1_product_brief/product",
  "downstream_consumer": "ssd-product-brief-create",
  "mode": "guided",
  "goal": "Explore why this product should exist, who it is for, what problem makes it necessary, how it solves the problem at a high level, and what would make it meaningfully different or well-positioned.",
  "constraints": "Apply .opencode/shared/product-brief-contract.md. Avoid implementation details, architecture, MVP scope, success metrics, delivery planning, epics, stories, and engineering tasks."
}
```

Use the returned brainstorm distillate as source material.

### 4. Draft Temp Brief

Draft `._ssd_docs_temp/_docs/1_product_brief.md` using the shared contract template path and required sections. Replace placeholders with source-backed content, preserve section order, and remove template guidance text.

Source material may include product/problem area, initial context, focused discovery notes, and the optional brainstorm distillate.

### 5. Inline Review Gate

Apply the shared contract inline review gate.

If ideation has not been used and the draft is too generic after review, recommend the single optional ideation pass. If declined, proceed with explicit `Unknown` or `Assumption` markers where acceptable, or block only if the brief would be misleading.

### 6. Revise Temp Brief

Apply clear review fixes directly to `._ssd_docs_temp/_docs/1_product_brief.md`.

### 7. Finalize Once

Create `ssd_docs/1_product_brief.md` exactly once from the reviewed temp draft. If the final file appears before this write, stop.

### 8. Distill Final

Run the shared contract final distillation call.

### 9. Return Result

Return:

```json
{
  "status": "complete|blocked|failed",
  "product_brief_draft": "._ssd_docs_temp/_docs/1_product_brief.md",
  "product_brief": "ssd_docs/1_product_brief.md",
  "product_brief_distillate": "._ssd_docs_distil/_docs/1_product_brief.md",
  "ideation_used": "boolean",
  "product_brainstorm_raw": "._ssd_docs_temp/brainstorming/_docs/1_product_brief/product/<filename> or null",
  "product_brainstorm_distillate": "._ssd_docs_distil/brainstorming/_docs/1_product_brief/product/<filename> or null",
  "warnings": []
}
```

## Hard Stops

- Do not scan project artifacts or existing docs.
- Do not call `.agents/skills/bmad-product-brief`.
- Do not overwrite or edit `ssd_docs/1_product_brief.md`.
- Do not skip inline review or final distillation.
- Do not run more than one optional ideation pass unless the user explicitly asks.
- Do not hand-write final distillates unless the caller explicitly asks for best-effort output after a distillator failure.
