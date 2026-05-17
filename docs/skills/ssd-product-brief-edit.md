# ssd-product-brief-edit

## Summary

- Name: `ssd-product-brief-edit`
- Description: Edit an existing SQLite-backed Product Brief while preserving the shared product-brief contract.
- Source: `.opencode/skills/ssd-product-brief-edit/SKILL.md`

## Purpose

Updates existing Product Brief memory while preserving the Product Brief boundary, classification rules, direct-input budget/team rules, and current required sections.

## When To Use

Use when the user asks to revise, update, correct, or pivot an existing Product Brief.

Do not use when Product Brief memory is missing; use `ssd-product-brief-create` first. Do not edit downstream artifacts or markdown brief files.

## How It Is Used

The skill applies the shared contract, bootstraps and reads the Product Classification reference list from SQLite memory, loads existing memory, classifies the change, asks only necessary clarifications, optionally runs one edit ideation pass, drafts an edited payload, performs focused inline review, and updates memory after approval.

It skips the create-only `Challenge from Critical Perspective` validation gate.

## Inputs

- `change_request`: required unless obvious.
- `additional_context`: optional.

## Outputs

- `status`: `complete|blocked|failed`.
- `artifact_kind`: `product-brief`.
- `artifact_id`: Product Brief artifact UUID.
- `ideation_used`: whether optional edit ideation ran.
- `cited_brainstorm_ids`: cited brainstorm IDs.
- `cited_idea_ids`: cited brainstorm idea IDs.
- `warnings`: array of warnings.

## Defaults

- Applies `.opencode/shared/product-brief-contract.md`.
- Clarification asks at most 3 questions for ambiguity, contradiction, strategic choice, or missing direct input for requested budget/team changes.
- Budget and team changes must come from direct user input only; otherwise they are stored as `Unknown`.
- Classification changes are selected from the `product-classifications` SQLite reference list and confirmed by user approval before storage.
- Optional ideation uses `ssd-brainstorming` with `scope=quick`, `mode=guided`, and no fixed techniques.
- At most one optional ideation pass runs unless the user asks for more.
- Review shows a concise change summary and changed sections only, with before/after bullets or equivalent deltas.
- Changed section text preserves readable newlines for bullets and paragraphs.
- Product Brief create validation is skipped.
- Runtime state is SQLite memory only.

## Paths

- Source skill: `.opencode/skills/ssd-product-brief-edit/SKILL.md`.
- Shared contract: `.opencode/shared/product-brief-contract.md`.
- Product classifications reference list: `.opencode/scripts/ssd_memory/memory.py reference bootstrap/get --list-key product-classifications`.
- Memory adapter: `.opencode/scripts/ssd_product_brief/memory.py`.

## Memory

- Status: updates_and_uses.
- Summary: Reads Product Brief `Artifact` memory, updates current required sections, and preserves or refreshes provenance relationships.
- Memory contract: `docs/memory/ssd-product-brief.md`.

## Completion Criteria

Completes when the edited payload passes inline review, the user approves the focused change review, any changed classification is confirmed, and memory update succeeds.

Stops or blocks when Product Brief memory is missing, the edit would produce a misleading brief, or memory update fails.

## Invocation

Invoke with the requested change and optional context.

The approval review shows a concise summary, changed sections with before/after bullets or equivalent deltas, changed classification with rationale and uncertainty when applicable, and affected assumptions, open questions, and sources before the final approval/change instruction. The user may ask to see the full final document or a specific section.

Before writing, changed sections are checked for flattened bullets or paragraphs and rewritten with newline-separated formatting when needed.

## Related Files

- Source skill: `.opencode/skills/ssd-product-brief-edit/SKILL.md`.
- Related skill: `ssd-brainstorming`.
- Memory contract: `docs/memory/ssd-product-brief.md`.
- Product classifications reference list: `.opencode/scripts/ssd_memory/memory.py reference bootstrap/get --list-key product-classifications`.

## Notes

- Updates only Product Brief memory and does not edit or warn about downstream artifacts automatically.
- Do not infer budget or team; use direct user input or `Unknown`.
- Do not store classification changes unless the reference-list-backed classification is shown and approved.
- Do not display unchanged sections unless the user asks.
- Do not create Product Brief markdown/temp drafts, skip inline review, or run the Product Brief create validation gate.
