# ssd-product-brief-edit

## Summary

- Name: ssd-product-brief-edit
- Description: Edit an existing Product Brief, preserve the shared product-brief contract, regenerate its distillate, and warn about stale downstream artifacts.

## Purpose

Updates `ssd_docs/1_product_brief.md` while preserving the Product Brief boundary and keeping `._ssd_docs_distil/_docs/1_product_brief.md` in sync.

## When To Use

Use when the user asks to revise, update, correct, or pivot an existing Product Brief.

Do not use when the Product Brief does not exist; use `ssd-product-brief-create` first.

## How It Is Used

The skill applies the shared product-brief contract, reads the existing brief, classifies the requested change, asks only necessary clarification questions, optionally recommends one edit ideation pass, drafts an edited temp brief, performs inline review, overwrites the final brief, redistills it, and warns about stale downstream artifacts.

## Inputs

- `change_request`: required unless obvious.
- `additional_context`: optional.

## Outputs

- `status`: `complete|blocked|failed`.
- `product_brief_edit_draft`: temp edit draft path, `._ssd_docs_temp/_docs/1_product_brief_edit.md`.
- `product_brief`: final brief path, `ssd_docs/1_product_brief.md`.
- `product_brief_distillate`: final brief distillate path, `._ssd_docs_distil/_docs/1_product_brief.md`.
- `ideation_used`: whether optional edit ideation ran.
- `edit_brainstorm_raw`: optional raw edit brainstorm path, or null.
- `edit_brainstorm_distillate`: optional edit brainstorm distillate path, or null.
- `stale_downstream_artifacts`: downstream artifact paths that may need regeneration.
- `warnings`: array of warnings.

## Defaults

- Applies `.opencode/shared/product-brief-contract.md`.
- Clarification asks at most 3 questions only for ambiguity, contradiction, or strategic choices.
- Optional ideation uses `ssd-brainstorming` with `scope=quick`, `mode=guided`, and no fixed techniques.
- At most one optional ideation pass runs unless the user explicitly asks for more.

## Paths

- Shared contract: `.opencode/shared/product-brief-contract.md`.
- Existing/final brief: `ssd_docs/1_product_brief.md`.
- Existing/final brief distillate: `._ssd_docs_distil/_docs/1_product_brief.md`.
- Temp edit draft: `._ssd_docs_temp/_docs/1_product_brief_edit.md`.
- Optional edit brainstorm folder: `_docs/1_product_brief/edit`.
- Optional edit brainstorm distillate: `._ssd_docs_distil/brainstorming/_docs/1_product_brief/edit/<filename>`.
- Downstream staleness checks: `ssd_docs/2_product_blueprint.md`, `._ssd_docs_distil/_docs/2_product_blueprint.md`.

## Completion Criteria

Completes when the edited temp brief passes inline review, `ssd_docs/1_product_brief.md` is updated, the Product Brief distillate is regenerated, and stale downstream artifacts are reported.

Stops or blocks when the Product Brief is missing, the edit would produce a misleading brief, or final distillation cannot complete.

## Related Files

- Source skill: `.opencode/skills/ssd-product-brief-edit/SKILL.md`.
- Shared contract: `.opencode/shared/product-brief-contract.md`.
- Template: `.opencode/skills/ssd-product-brief-create/templates/product-brief-template.md`.
- Related skills: `ssd-brainstorming`, `ssd_distillator`.

## Notes

- This is the only Product Brief skill allowed to overwrite `ssd_docs/1_product_brief.md`.
- It must not edit downstream artifacts automatically.
