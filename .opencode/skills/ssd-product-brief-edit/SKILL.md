---
name: ssd-product-brief-edit
description: Edit an existing Product Brief, preserve the shared product-brief contract, regenerate its distillate, and warn about stale downstream artifacts.
---

# ssd-product-brief-edit

Use when the user asks to revise, update, correct, or pivot an existing `ssd_docs/1_product_brief.md`.

This is OpenCode-native. Do not use BMad config, BMad step files, hidden workflow variables, project artifact scanning beyond named SSD artifacts, or existing planning docs except the Product Brief and downstream staleness checks.

## Contract

Input:

```json
{
  "change_request": "required unless obvious",
  "additional_context": "optional"
}
```

Rules:

- Read and apply `.opencode/shared/product-brief-contract.md` before proceeding.
- If `change_request` is missing, ask only: "What change should we make to the Product Brief?"
- If `ssd_docs/1_product_brief.md` is missing, stop and tell the user to run `ssd-product-brief-create` first.
- This skill may overwrite `ssd_docs/1_product_brief.md` after inline review.
- Regenerate `._ssd_docs_distil/_docs/1_product_brief.md` after every successful edit.
- Run at most one optional ideation pass unless the user explicitly asks for more.

## Paths

- Shared contract: `.opencode/shared/product-brief-contract.md`
- Existing/final brief: `ssd_docs/1_product_brief.md`
- Existing/final brief distillate: `._ssd_docs_distil/_docs/1_product_brief.md`
- Temp edit draft: `._ssd_docs_temp/_docs/1_product_brief_edit.md`
- Optional edit brainstorm folder: `_docs/1_product_brief/edit`
- Optional edit brainstorm distillate: `._ssd_docs_distil/brainstorming/_docs/1_product_brief/edit/<filename>`
- Downstream artifacts to warn about: `ssd_docs/2_product_blueprint.md`, `._ssd_docs_distil/_docs/2_product_blueprint.md`

## Workflow

### 1. Preflight

Read and apply `.opencode/shared/product-brief-contract.md`.

If `ssd_docs/1_product_brief.md` is missing, stop with:

```text
Product Brief is required before editing.
Expected: ssd_docs/1_product_brief.md
Run ssd-product-brief-create first.
```

Read `ssd_docs/1_product_brief.md`. Optionally read `._ssd_docs_distil/_docs/1_product_brief.md` if it exists.

### 2. Classify Change

Classify the requested change as one of:

- minor wording cleanup;
- section update;
- positioning or audience change;
- major product pivot.

### 3. Clarify

Ask at most 3 questions only if the edit creates ambiguity, contradiction, or a strategic choice. If the user does not know, record `Unknown` or a named assumption and continue when safe.

### 4. Optional Ideation

Recommend a short ideation pass only for major pivots, unclear audience, weak positioning, or changed problem framing. The user may decline.

If accepted, call `ssd-brainstorming` once with:

```json
{
  "run_mode": "internal",
  "topic": "<product_or_problem_area from existing brief or change request>",
  "initial_context": "<existing brief plus change request plus clarifications>",
  "scope": "quick",
  "target_folder": "_docs/1_product_brief/edit",
  "downstream_consumer": "ssd-product-brief-edit",
  "mode": "guided",
  "goal": "Explore the requested product brief change at a product-definition level, including why it matters, audience impact, positioning, assumptions, and contradictions with the current brief.",
  "constraints": "Apply .opencode/shared/product-brief-contract.md. Avoid implementation details, architecture, MVP scope, success metrics, delivery planning, epics, stories, and engineering tasks."
}
```

Use the returned brainstorm distillate as edit source material.

### 5. Draft Edited Temp Brief

Create `._ssd_docs_temp/_docs/1_product_brief_edit.md` using the current brief as the base.

Apply only:

- requested changes;
- required consistency fixes;
- source-backed additions from clarification or optional ideation.

Preserve the current brief structure. Use the shared contract template path only to repair missing required sections or malformed structure.

### 6. Inline Review Gate

Apply the shared contract inline review gate to the temp edit draft.

If ideation has not been used and the edit remains too generic, conflicted, or assumption-heavy after review, recommend the single optional ideation pass. If declined, proceed with explicit `Unknown` or `Assumption` markers where acceptable, or block only if the edited brief would be misleading.

### 7. Apply Edit

Overwrite `ssd_docs/1_product_brief.md` with the reviewed temp edit draft.

### 8. Redistill

Run the shared contract final distillation call.

### 9. Downstream Staleness Warning

Check whether either downstream artifact exists:

- `ssd_docs/2_product_blueprint.md`
- `._ssd_docs_distil/_docs/2_product_blueprint.md`

If found, include those paths in `stale_downstream_artifacts`. Do not edit downstream artifacts automatically.

### 10. Return Result

Return:

```json
{
  "status": "complete|blocked|failed",
  "product_brief_edit_draft": "._ssd_docs_temp/_docs/1_product_brief_edit.md",
  "product_brief": "ssd_docs/1_product_brief.md",
  "product_brief_distillate": "._ssd_docs_distil/_docs/1_product_brief.md",
  "ideation_used": "boolean",
  "edit_brainstorm_raw": "._ssd_docs_temp/brainstorming/_docs/1_product_brief/edit/<filename> or null",
  "edit_brainstorm_distillate": "._ssd_docs_distil/brainstorming/_docs/1_product_brief/edit/<filename> or null",
  "stale_downstream_artifacts": [],
  "warnings": []
}
```

## Hard Stops

- Do not proceed if `ssd_docs/1_product_brief.md` is missing.
- Do not call BMad skills.
- Do not scan project artifacts beyond named SSD artifacts in this workflow.
- Do not skip inline review or final distillation.
- Do not run more than one optional ideation pass unless the user explicitly asks.
- Do not edit downstream artifacts automatically.
- Do not hand-write final distillates unless the caller explicitly asks for best-effort output after a distillator failure.
