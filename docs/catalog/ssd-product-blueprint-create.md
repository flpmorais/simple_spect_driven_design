# ssd-product-blueprint-create

## Summary

- Name: ssd-product-blueprint-create
- Description: Creates a Product Blueprint from the distilled Product Brief through mandatory product-dream ideation, inline review, optional supplemental ideation, and mandatory SSD distillation.

## Purpose

Expands the Product Brief into a structured view of the intended product shape before delivery constraints, roadmap slicing, or implementation planning are introduced.

## When To Use

Use when the user asks to create a Product Blueprint, expand the Product Brief into conceptual product structure, or define major product capabilities, boundaries, principles, cross-cutting concerns, assumptions, and unknowns.

## How It Is Used

The skill requires the distilled Product Brief, runs one normal product-dream brainstorm with 50 target ideas, drafts a temporary blueprint, reviews it inline, optionally recommends one supplemental ideation pass if the draft is still weak, writes the final blueprint exactly once, and distills it without audit. Missing Product Brief distillate returns `precondition_failed`; an existing final blueprint returns `skipped`.

## Inputs

- `product_brief_distillate`: Optional. Defaults to `._ssd_docs_distil/_docs/1_product_brief.md`.
- `initial_context`: Optional. Additional user context to include alongside the Product Brief distillate.

## Outputs

Returns user-facing structured output with `status`, `product_blueprint`, `ideation_used`, `supplemental_ideation_used`, and `warnings` on successful completion. Runtime/tool failures return `blocked` with partial outputs.

## Defaults

- Always guided through internal brainstorms; no `headless`, `autonomous`, `yolo`, or `draft-first` modes.
- Mandatory product-dream brainstorm uses `scope=normal`, `target_ideas=50`, `mode=guided`, and lets `ssd-brainstorming` choose techniques.
- Optional supplemental ideation is recommended only when the reviewed draft is thin, vague, generic, conflicted, or assumption-heavy. It also lets `ssd-brainstorming` choose techniques.
- Clarification asks only for strategic product choices and avoids implementation, stack, MVP, roadmap, delivery, success-metric, and architecture questions. Drafting may proceed with recorded uncertainty.
- Final distillation is mandatory with `audit=false`; audit fix passes are not used.

## Paths

- Product brief distillate: `._ssd_docs_distil/_docs/1_product_brief.md`.
- Product dream brainstorm folder: `_docs/2_product_blueprint/product_dream`.
- Product dream brainstorm distillate: `._ssd_docs_distil/brainstorming/_docs/2_product_blueprint/product_dream/<filename>`.
- Optional supplemental brainstorm folder: `_docs/2_product_blueprint/product_refinement`.
- Optional supplemental brainstorm distillate: `._ssd_docs_distil/brainstorming/_docs/2_product_blueprint/product_refinement/<filename>`.
- Product Blueprint template: `.opencode/skills/ssd-product-blueprint-create/templates/product-blueprint-template.md`.
- Temp draft: `._ssd_docs_temp/_docs/2_product_blueprint.md`.
- Final blueprint: `ssd_docs/2_product_blueprint.md`.
- Final blueprint distillate: `._ssd_docs_distil/_docs/2_product_blueprint.md`.

## Completion Criteria

Completes when mandatory product-dream brainstorming, inline draft review, any accepted supplemental ideation, single final blueprint write, and final distillation have succeeded.

Returns `precondition_failed` if the Product Brief distillate is missing. Returns `skipped` if `ssd_docs/2_product_blueprint.md` already exists.

## Invocation

Invoke after `._ssd_docs_distil/_docs/1_product_brief.md` exists. Optionally provide additional context to incorporate into the blueprint creation flow.

Expected caller behavior: allow the mandatory product-dream brainstorm and consider the optional supplemental ideation pass if the inline review finds weak product-shape areas.

## Related Files

- Source skill: `.opencode/skills/ssd-product-blueprint-create/SKILL.md`.
- Template: `.opencode/skills/ssd-product-blueprint-create/templates/product-blueprint-template.md`.
- Related skills: `ssd-brainstorming`, `ssd_distillator`.

## Notes

- The final blueprint must exclude requirements, user stories, acceptance criteria, architecture, technology stack, data models, API design, MVP scope, roadmap, delivery sequencing, work packages, engineering tasks, and success metrics used as planning criteria.
- The skill must not scan project artifacts, use BMad config or step files, read original source docs such as `ssd_docs/1_product_brief.md`, overwrite the final blueprint, skip the mandatory product-dream brainstorm, skip inline review, skip final distillation, or hand-write final distillates unless explicitly asked for best-effort output after a distillator failure.
