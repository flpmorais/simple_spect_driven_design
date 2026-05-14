# ssd-product-brief-create

## Summary

- Name: ssd-product-brief-create
- Description: Create the first foundational product brief through focused discovery, optional ideation, inline review, and mandatory SSD distillation.

## Purpose

Creates a business/product definition for non-experts that explains why the product should exist, what is being built, how it solves the problem at a high level, and who it is for.

## When To Use

Use when the user asks to create the first product brief, define a new product at a high level, or produce the foundational product definition for a project.

Do not use when the user wants to edit an existing `ssd_docs/1_product_brief.md`, perform technical planning, create detailed requirements, define MVP scope, set success metrics, create epics or stories, plan delivery, or produce engineering tasks.

## How It Is Used

The skill applies the shared product-brief contract, gathers focused discovery context, optionally recommends one ideation pass through `ssd-brainstorming`, drafts a temporary brief, performs inline review, writes the final brief exactly once, and distills it.

## Inputs

- `product_or_problem_area`: required unless obvious.
- `initial_context`: optional seed context or user brain dump.

## Outputs

- `status`: `complete|blocked|failed`.
- `product_brief_draft`: temp draft path, `._ssd_docs_temp/_docs/1_product_brief.md`.
- `product_brief`: final brief path, `ssd_docs/1_product_brief.md`.
- `product_brief_distillate`: final brief distillate path, `._ssd_docs_distil/_docs/1_product_brief.md`.
- `ideation_used`: whether optional ideation ran.
- `product_brainstorm_raw`: optional raw product brainstorm path, or null.
- `product_brainstorm_distillate`: optional product brainstorm distillate path, or null.
- `warnings`: array of warnings.

## Defaults

- Always guided; no `headless`, `autonomous`, `yolo`, or `draft-first` modes.
- Focused discovery asks at most 3 questions only when drafting would otherwise be too speculative.
- Optional ideation uses `ssd-brainstorming` with `scope=quick`, `mode=guided`, and no fixed techniques.
- At most one optional ideation pass runs unless the user explicitly asks for more.

## Paths

- Optional product brainstorm folder: `_docs/1_product_brief/product`.
- Optional product brainstorm distillate: `._ssd_docs_distil/brainstorming/_docs/1_product_brief/product/<filename>`.
- Shared contract: `.opencode/shared/product-brief-contract.md`.
- Product brief template: `.opencode/skills/ssd-product-brief-create/templates/product-brief-template.md`.
- Temp draft: `._ssd_docs_temp/_docs/1_product_brief.md`.
- Final brief: `ssd_docs/1_product_brief.md`.
- Final brief distillate: `._ssd_docs_distil/_docs/1_product_brief.md`.

## Completion Criteria

Completes when focused discovery, optional ideation if accepted, temp draft creation, inline review, single final brief write, and final distillation have succeeded.

Stops or blocks when `ssd_docs/1_product_brief.md` already exists, appears before the final write, the inline review gate finds a misleading brief that cannot be resolved, or final distillation cannot complete.

## Invocation

Invoke with the product or problem area and optional initial context. If the product or problem area is missing, the skill asks only: "What product, project, or problem area should we explore for the product brief?"

Expected caller behavior: provide clarifications only when a strategic choice is needed, optionally accept or decline ideation, and expect the final brief to be written exactly once after inline review.

## Related Files

- Source skill: `.opencode/skills/ssd-product-brief-create/SKILL.md`.
- Shared contract: `.opencode/shared/product-brief-contract.md`.
- Template: `.opencode/skills/ssd-product-brief-create/templates/product-brief-template.md`.
- Related skills: `ssd-brainstorming`, `ssd_distillator`.

## Notes

- The final brief must exclude technology stack, architecture, implementation details, detailed requirements, MVP scope, success metrics, epics, stories, delivery plans, and engineering tasks.
- The skill must not scan project artifacts, use BMad config or step files, call `.agents/skills/bmad-product-brief`, overwrite the final brief, skip inline review, or hand-write final distillates unless explicitly asked for best-effort output after a distillator failure.
- Editing existing `ssd_docs/1_product_brief.md` belongs to `ssd-product-brief-edit`.
