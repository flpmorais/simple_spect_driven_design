# ssd-product-blueprint-create

## Summary

- Name: `ssd-product-blueprint-create`
- Description: Creates a SQLite-backed Product Blueprint from Product Brief memory through product-dream ideation, user section review, and memory storage.
- Source: `.opencode/skills/ssd-product-blueprint-create/SKILL.md`

## Purpose

Expands Product Brief memory into conceptual product shape before delivery constraints, roadmap slicing, or implementation planning.

## When To Use

Use when the user asks to create a Product Blueprint, expand a Product Brief into product structure, or define major capabilities, boundaries, principles, cross-cutting concerns, assumptions, and unknowns.

Do not use when Product Brief memory is missing, Product Blueprint memory already exists, or the user wants requirements, implementation planning, downstream artifacts, or markdown blueprint files.

## How It Is Used

The skill applies the shared contract, reads Product Brief memory, optionally loads confirmed source files/artifacts, loads Product Brief-cited brainstorms, runs one mandatory normal user-led product-dream brainstorm, executes the handoff, drafts and reviews sections, optionally runs supplemental ideation, presents all sections for approval, and writes memory once after approval.

## Inputs

- `initial_context`: optional extra context.

## Outputs

- `status`: `complete|precondition_failed|skipped|blocked`.
- `artifact_kind`: `product-blueprint`.
- `artifact_id`: Product Blueprint artifact UUID.
- `product_brief_artifact_id`: source Product Brief UUID.
- `source_brainstorms`: brainstorm references and handoff commands.
- `source_artifacts`: extra artifact sources.
- `source_files`: snapshotted file sources.
- `cited_idea_ids`: cited brainstorm idea IDs.
- `ideation_used`: always true on success.
- `supplemental_ideation_count`: number of supplemental brainstorms.
- `warnings`: warning array.

## Defaults

- Always guided; no `headless`, `autonomous`, `yolo`, or `draft-first` modes.
- Mandatory product-dream brainstorm uses `scope=normal`, `target_ideas=50`, `mode=guided`, no fixed techniques, and remains interactive/user-led.
- Ask once near the start about stored memory or file sources.
- Load artifacts through `.opencode/shared/recipes.md`; read files directly.
- Persist extra source artifacts/files as graph citations.
- Product Brief-cited brainstorms are loaded first with role `product_brief_source`; they do not replace mandatory product-dream ideation.
- Supplemental ideation is recommended only for thin, vague, generic, conflicted, or assumption-heavy payloads, and repeats only on explicit request.
- Clarification asks only for strategic product choices, not implementation, stack, MVP, roadmap, delivery, metrics, or architecture.
- Runtime state is SQLite memory only.

## Paths

- Source skill: `.opencode/skills/ssd-product-blueprint-create/SKILL.md`.
- Shared contract: `.opencode/shared/product-blueprint-contract.md`.
- Memory recipe index: `.opencode/shared/recipes.md`.
- Product Brief memory adapter: `.opencode/scripts/ssd_product_brief/memory.py`.
- Product Blueprint memory adapter: `.opencode/scripts/ssd_product_blueprint/memory.py`.

## Memory

- Status: creates_and_uses.
- Summary: Reads Product Brief memory, consumes brainstorm handoff memory, and creates current Product Blueprint `Artifact` memory with required sections and provenance edges.
- Memory contract: `docs/memory/ssd-product-blueprint.md`.

## Completion Criteria

Completes when Product Brief memory exists, Product Blueprint memory does not, optional extra sources are handled, Product Brief source brainstorms are loaded when present, mandatory product-dream ideation succeeds, review passes, the user approves the human-readable section review, accepted supplemental ideation is incorporated, and create succeeds.

Returns `precondition_failed` if Product Brief memory is missing, `skipped` if Product Blueprint already exists, and `blocked` for tool/memory failure after start or missing approval.

## Invocation

Invoke after Product Brief memory exists, optionally with extra context. The user participates in product-dream facilitation, makes or defers strategic product-shape choices, considers supplemental ideation when recommended, and approves or revises proposed sections before memory write.

## Related Files

- Source skill: `.opencode/skills/ssd-product-blueprint-create/SKILL.md`.
- Related skill: `ssd-brainstorming`.
- Memory contract: `docs/memory/ssd-product-blueprint.md`.
- Shared contract: `.opencode/shared/product-blueprint-contract.md`.
- Memory recipe: `.opencode/shared/recipes/product-blueprint.md`.

## Notes

- Exclude requirements, stories, acceptance criteria, architecture, stack, data models, API design, MVP scope, roadmap, delivery sequencing, work packages, engineering tasks, and planning success metrics.
- Do not scan artifacts, use BMad config/steps, read Product Brief markdown, create Product Blueprint markdown/temp drafts, skip mandatory ideation or review, output only raw JSON/tool results for review, or write before approval.
