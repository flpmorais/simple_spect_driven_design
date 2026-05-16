# ssd-product-brief-create

## Summary

- Name: `ssd-product-brief-create`
- Description: Create the first foundational product brief through focused discovery, optional ideation, create-only validation, user approval, and SQLite memory storage.
- Source: `.opencode/skills/ssd-product-brief-create/SKILL.md`

## Purpose

Creates a non-technical business/product definition explaining why the product should exist, what is being built, how it solves the problem at a high level, and who it is for.

## When To Use

Use when the user asks to create the first product brief, define a new product at a high level, or produce the foundational product definition.

Do not use for editing an existing Product Brief, technical planning, detailed requirements, MVP scope, metrics, epics, stories, delivery planning, engineering tasks, or markdown brief files.

## How It Is Used

The skill applies the shared contract, checks for an existing Product Brief, gathers focused context, optionally loads confirmed source files or memory objects, optionally runs one `ssd-brainstorming` pass, drafts and audits a section payload, runs create-only validation, presents all sections for approval, and writes memory once after approval.

## Inputs

- `product_or_problem_area`: required unless obvious.
- `initial_context`: optional seed context or user brain dump.

## Outputs

- `status`: `complete|blocked|failed`.
- `artifact_kind`: `product-brief`.
- `artifact_id`: Product Brief artifact UUID.
- `ideation_used`: whether optional ideation ran.
- `cited_brainstorm_ids`: cited brainstorm IDs.
- `cited_idea_ids`: cited brainstorm idea IDs.
- `warnings`: array of warnings.

## Defaults

- Always guided; no `headless`, `autonomous`, `yolo`, or `draft-first` modes.
- Discovery asks at most 3 focused questions only when drafting would be speculative.
- Stored section content must be source-grounded, an approved assumption, or `Unknown`.
- Vague labels and yes/no answers must not become complete prose.
- Section text preserves readable newlines for bullets and paragraphs.
- Optional ideation uses `ssd-brainstorming` with `scope=quick`, `mode=guided`, and no fixed techniques.
- Matching unfinished create brainstorms are resumed before creating a new brainstorm.
- At most one optional ideation pass runs unless the user asks for more.
- Create validation always runs one internal `Challenge from Critical Perspective` pass before approval.
- Validation asks up to 3 questions; Socratic fallback runs only for blocking strategic gaps and is capped at 3 questions.
- Runtime state is SQLite memory only.

## Paths

- Source skill: `.opencode/skills/ssd-product-brief-create/SKILL.md`.
- Shared contract: `.opencode/shared/product-brief-contract.md`.
- Memory recipe index: `.opencode/shared/recipes.md`.
- Memory adapter: `.opencode/scripts/ssd_product_brief/memory.py`.

## Memory

- Status: creates_and_uses.
- Summary: Creates current Product Brief `Artifact` memory with required sections and provenance relationships.
- Memory contract: `docs/memory/ssd-product-brief.md`.

## Create Validation

After internal review and before approval, the skill runs internal `ssd-advanced-elicitation` with `Challenge from Critical Perspective` to catch unsupported claims, shallow assumptions, overconfident positioning, missing operational constraints, hallucinated specificity, verbose thin-evidence prose, flattened formatting, and unsupported core sections.

It asks up to 3 validation questions, avoiding implementation, architecture, roadmap, metrics, detailed requirements, MVP scope, epics, stories, and backlog questions. The brief is refined after answers.

Run one internal `Socratic Questioning` fallback only when unresolved choices would materially change audience, product-level problem, product definition, necessity versus existing tools/workflows, or core operating constraint. Cap at 3 questions, then represent remaining uncertainty as `Unknown`, assumptions, or open questions.

Before approval, audit every required section. Unsupported content becomes `Unknown`; partial support keeps only the supported part and moves the rest to `Assumption:` or Open Questions. Core sections cannot be mostly inferred.

## Completion Criteria

Completes when source objects are confirmed if used, discovery is done, accepted ideation is incorporated, section grounding and validation pass, the user approves all sections, and the single create command succeeds.

Stops or blocks when Product Brief memory already exists, review finds a misleading brief that cannot be resolved, approval is not obtained, or memory create fails.

## Invocation

Invoke with product/problem area and optional initial context. If missing, the skill asks only: "What product, project, or problem area should we explore for the product brief?"

The approval review shows the complete proposed brief, source memory objects, assumptions, open questions, and validation summary before the final approval/change instruction.

## Related Files

- Source skill: `.opencode/skills/ssd-product-brief-create/SKILL.md`.
- Related skill: `ssd-brainstorming`.
- Memory contract: `docs/memory/ssd-product-brief.md`.
- Memory recipe index: `.opencode/shared/recipes.md`.

## Notes

- Exclude technical stack, architecture, implementation details, detailed requirements, MVP scope, metrics, epics, stories, delivery plans, and engineering tasks.
- Do not store inferred section content as fact or flatten bullets/paragraphs.
- If a stored memory object is requested, use `.opencode/shared/recipes.md` and only the relevant recipe.
- Do not scan artifacts, use BMad config/steps, call `.agents/skills/bmad-product-brief`, create markdown/temp drafts, skip review or create validation, output only raw JSON/tool results, or write before approval.
- Editing existing Product Brief memory belongs to `ssd-product-brief-edit`.
