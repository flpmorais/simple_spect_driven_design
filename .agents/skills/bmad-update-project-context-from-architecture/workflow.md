---
architecture_file: '{project-root}/_bmad-output/planning-artifacts/architecture.md'
project_context_file: '{project-root}/_bmad-output/project-context.md'
max_project_context_lines: 300
---

# Update Project Context From Architecture Workflow

**Goal:** Incrementally merge durable architecture rules from the current work-package architecture into `_bmad-output/project-context.md` while preserving the whole-project rules already captured there.

**Your Role:** You are a technical rules curator. You maintain project context as the golden, concise, whole-project technical rule source for AI agents.

## Non-Negotiable Rules

- Only modify `_bmad-output/project-context.md`.
- Read `_bmad-output/planning-artifacts/architecture.md` and `_bmad-output/project-context.md` before proposing changes.
- Treat `architecture.md` as an incremental work-package input, not a full replacement for project context.
- Missing mention in `architecture.md` does not weaken, remove, or supersede an existing project-context rule.
- Remove or replace an existing project-context rule only when `architecture.md` explicitly says the old rule is replaced, deprecated, removed, or no longer used.
- If `architecture.md` conflicts with project context but does not explicitly supersede it, STOP and ask the user.
- Keep `_bmad-output/project-context.md` under 300 lines. If this cannot be done safely, STOP and ask the user what to compress or remove.
- Do not copy architecture rationale, diagrams, implementation sequence, or local work-package details unless they create durable rules for future agents.

## Workflow Architecture

This uses BMad-style micro-file architecture:

- Each step is self-contained and must be read fully before acting.
- Complete steps in order.
- Halt at user review gates.
- Persist only the final approved merge into `_bmad-output/project-context.md`.

## Configuration Loading

Load config from `{project-root}/_bmad/bmm/config.yaml` and resolve:

- `user_name`
- `communication_language`
- `document_output_language`
- `date` as system-generated current date

If config loading fails, continue with the paths defined in this workflow and communicate in English.

## Execution

Read fully and follow `./steps/step-01-load-and-validate.md`.
