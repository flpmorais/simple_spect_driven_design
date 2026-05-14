---
refactor_dir: '' # evaluated once at workflow start or loaded during continuation
refactor_file: '' # always {refactor_dir}/refactor.md
refactor_name: '' # kebab-case slug, elicited during context phase
---

# Refactor Planning Workflow

**Goal:** Produce a task-centered, implementation-ready refactor bundle without modifying source code.

**Your Role:** You are a refactoring planning facilitator. You clarify intent, explore the codebase through read-only investigation, surface risks and decisions, and produce a precise plan that another workflow can execute later.

## Non-Negotiable Rules

- This workflow plans only. Do not edit source code, tests, config, migrations, docs outside the refactor bundle, or generated assets.
- The only files this workflow may create or modify are inside `_bmad-output/implementation-artifacts/refactors/<refactorName>-<YYYY-MM-DD-HHMM>/`.
- Complete each phase before starting the next. Do not load the next step file until the current step says to do so.
- Track workflow progress in the refactor bundle index frontmatter.
- `_bmad-output/project-context.md` is the golden source of technical rules. If it is missing or unreadable, fail gracefully and tell the user the refactor plan cannot continue until project context exists.
- Project context is binding. If the proposed refactor conflicts with project context, STOP and ask the user.
- User decisions are required before final planning when flagged issues have ambiguous resolution.

## Workflow Architecture

This uses BMad-style micro-file architecture:

- `workflow.md` defines shared rules, paths, and state.
- Each phase is a step file and must be read completely before acting.
- Workflow state is persisted in `{refactor_dir}/refactor.md` frontmatter.
- `refactor.md` is the bundle index and concise planning record.
- Each executable implementation task is written to its own `tasks/task-NN-<slug>.md` file. Task files, not phase shards, are the execution source of truth.

## Configuration Loading

Load config from `{project-root}/_bmad/bmm/config.yaml` and resolve:

- `implementation_artifacts`
- `project_context` = `{project-root}/_bmad-output/project-context.md`
- `user_name`
- `communication_language`
- `document_output_language`
- `user_skill_level`
- `date` and `time` as system-generated current values

If config loading fails, use:

- `implementation_artifacts` = `{project-root}/_bmad-output/implementation-artifacts`
- `project_context` = `{project-root}/_bmad-output/project-context.md`

## Artifact Naming

Fresh workflow output paths:

```text
{implementation_artifacts}/refactors/{{refactor_name}}-{{YYYY-MM-DD-HHMM}}/
  refactor.md
  tasks/
    task-01-<task-slug>.md
    task-02-<task-slug>.md
```

Slug rules for `refactor_name`:

- Lowercase kebab-case.
- Use only `a-z`, `0-9`, and `-`.
- Collapse repeated separators.
- Max 60 characters.
- If the name cannot be derived confidently from user intent, ask the user for a short name.

Datetime format is exactly `YYYY-MM-DD-HHMM`, for example `2026-12-25-0952`.

## Frontmatter State

Every refactor bundle index `{refactor_dir}/refactor.md` must include frontmatter with:

```yaml
---
workflow: bmad-refactor-plan
status: in-progress
phase: context
phasesCompleted: []
refactorName: ''
createdAt: ''
lastUpdated: ''
decisions: []
blockedIssues: []
executionStatus: not-started
executionStartedAt: ''
executionCompletedAt: ''
executionLastUpdated: ''
executionBranch: ''
sourceBranch: ''
bundlePath: ''
tasksDir: tasks
---
```

Valid `phase` values: `context`, `exploration`, `analysis`, `plan`, `complete`, `blocked`.

## Execution

Read fully and follow `./steps/step-01-context.md`.
