# ssd-architecture-blueprint-create

## Summary

- Name: `ssd-architecture-blueprint-create`
- Description: Creates a SQLite-backed Architecture Blueprint through interactive architecture recommendation discovery, review, and memory storage.
- Source: `.opencode/skills/ssd-architecture-blueprint-create/SKILL.md`

## Purpose

Creates a compact Architecture Blueprint from Product Blueprint memory by guiding the user through concrete architecture recommendations, confidence labels, acceptable compromises, rejected alternatives, and Phase 1 validation needs.

## When To Use

Use when the user asks to create an Architecture Blueprint, define expected architecture direction, compare major technical choices, or prepare Phase 1 architecture planning from the Product Blueprint.

Do not use when Product Blueprint memory is missing, Architecture Blueprint memory already exists, or the user wants detailed design, API specs, data models, deployment manifests, release planning, work packages, or engineering tasks.

## How It Is Used

The skill applies the shared Architecture Blueprint contract, reads Product Blueprint memory, optionally reads Product Brief memory, walks decision clusters interactively, proposes concrete recommendations and alternatives, captures only user-shaped recommendations, reviews the four-section payload, asks for final approval, and writes Architecture Blueprint memory once.

## Inputs

- `initial_context`: optional. Additional user context to include alongside Product Blueprint memory.

## Outputs

- `status`: `complete|precondition_failed|skipped|blocked`.
- `artifact_kind`: `architecture-blueprint`.
- `artifact_id`: Architecture Blueprint artifact memory UUID.
- `product_blueprint_artifact_id`: source Product Blueprint artifact memory UUID.
- `product_brief_artifact_id`: optional source Product Brief artifact memory UUID.
- `sections_approved`: section keys approved during the guided run.
- `source_brainstorms`: optional brainstorm memory references and handoff commands used as source material.
- `cited_idea_ids`: optional brainstorm idea memory IDs cited by the blueprint.
- `warnings`: array of warnings.

## Defaults

- Guided only; no headless or blind generation mode.
- Uses Product Blueprint memory as the required source.
- Reads Product Brief memory when available for context but does not require it after Product Blueprint exists.
- Asks at most 3 focused questions at a time.
- Walks decision clusters instead of asking a giant up-front questionnaire.
- Uses confidence labels: `Strong recommendation`, `Likely right`, `Weak recommendation`, `Unknown`.
- Writes durable memory only once after final user approval.

## Paths

- Source skill: `.opencode/skills/ssd-architecture-blueprint-create/SKILL.md`.
- Shared contract: `.opencode/shared/architecture-blueprint-contract.md`.
- Memory recipe index: `.opencode/shared/recipes.md`.
- Product Blueprint memory adapter: `.opencode/scripts/ssd_product_blueprint/memory.py`.
- Product Brief memory adapter: `.opencode/scripts/ssd_product_brief/memory.py`.
- Architecture Blueprint memory adapter: `.opencode/scripts/ssd_architecture_blueprint/memory.py`.

## Memory

- Status: creates_and_uses.
- Summary: Reads Product Blueprint memory, optionally uses Product Brief and brainstorm source memory, and creates current Architecture Blueprint `Artifact` memory with four recommendation-focused sections and provenance edges.
- Memory contract: `docs/memory/ssd-architecture-blueprint.md`.

## Completion Criteria

Completes when Product Blueprint memory is available, Architecture Blueprint memory does not already exist, every required decision area is covered, the user shapes the recommendation set interactively, internal review passes, final user approval is obtained, and the Architecture Blueprint memory create command succeeds.

Returns `precondition_failed` if Product Blueprint memory is missing. Returns `skipped` if Architecture Blueprint memory already exists. Returns `blocked` for tool or memory-command failure after start or when approval cannot be obtained.

## Invocation

Invoke after Product Blueprint memory exists. Optionally provide additional context to incorporate into the guided architecture recommendation flow.

Expected caller behavior: participate in focused decision-cluster discussion, confirm/correct/reject recommendations or mark unknowns, review the final four sections, and approve the final memory write.

## Related Files

- Source skill: `.opencode/skills/ssd-architecture-blueprint-create/SKILL.md`.
- Related skill: `ssd-product-blueprint-create`.
- Memory contract: `docs/memory/ssd-architecture-blueprint.md`.
- Shared contract: `.opencode/shared/architecture-blueprint-contract.md`.
- Memory recipe: `.opencode/shared/recipes/architecture-blueprint.md`.

## Notes

- The final blueprint must exclude generic principles, broad concern inventories, detailed design, data models, API specifications, deployment manifests, implementation tasks, release plans, work packages, and unsupported technology choices.
- The skill must not read Product Blueprint markdown, use BMad config or step files, create Architecture Blueprint markdown, ask a giant up-front questionnaire, generate recommendations without interaction, use percentage confidence, skip required decision coverage, or write memory before final approval.
