# Step 4: Final Refactor Plan

## Rules

- Speak in `{communication_language}`.
- Read `{refactor_file}` completely before planning.
- Do not edit source code or any file outside `{refactor_dir}`.
- The output is a plan only. Do not implement the plan.
- Every task must include validation.

## Plan Requirements

Create a thorough implementation plan based on confirmed context, exploration findings, analysis, and user decisions.

The plan must include:

- Ordered tasks and subtasks.
- Implementation Contract for each task, including runtime entrypoint, old owner, new owner, forbidden implementation patterns, required implementation patterns, compatibility allowed/forbidden, files allowed, and files forbidden where applicable.
- Likely files or areas for each task.
- Expected behavior change or preservation for each task.
- Done-when checklist items for each task. These must be concrete, inspectable statements, not vague intentions.
- Evidence required for each done-when item, including source references, test references, command results, or manual verification notes as applicable.
- Forbidden shortcuts for each task, especially scaffolding-only changes that would look complete without changing production behavior.
- Validation for each task: unit tests, integration tests, e2e tests, lint/type checks, manual checks, migrations, or UI checks as applicable.
- Completion Checks for each task: deterministic static checks, test commands, runtime-path evidence, expected changed files, and forbidden changed files.
- Risk mitigation notes where relevant.
- Rollback or safe sequencing notes where useful.
- Explicit non-goals and out-of-scope items.
- Remaining blockers if any exist.

Do not include speculative architecture changes. If a task would require a new architecture component, framework/library, container, API pattern, persistence pattern, or security behavior not approved in analysis, mark it as blocked instead of planning it as executable.

## Write Task Files

Create one task file per executable implementation task under `{refactor_dir}/tasks/` using this filename pattern:

```text
task-NN-<task-slug>.md
```

Each task file must use this structure:

```markdown
# Task NN: <Task Name>

## Implementation Contract

- Objective:
- Runtime entrypoint:
- Old owner:
- New owner:
- Forbidden implementation patterns:
- Required implementation patterns:
- Compatibility allowed:
- Compatibility forbidden:
- Files allowed:
- Files forbidden:

## Work Items

- Likely files / areas:
- Subtasks:

## Completion Checks

- Done when:
- Evidence required:
- Forbidden shortcuts:
- Static checks:
- Test commands:
- Runtime-path evidence:
- Validation:
- Risks / notes:
```

Then replace the `## Task Index` section in `{refactor_file}` with:

```markdown
## Task Index

### Planning Status

### Execution Principles

### Tasks

- `tasks/task-01-<task-slug>.md` - <Task Name>
- `tasks/task-02-<task-slug>.md` - <Task Name>

### Cross-Cutting Validation

### Rollback / Safety Notes

### Non-Goals And Deferred Work

### Remaining Blockers
```

Do not create `context.md`, `exploration.md`, `analysis.md`, or `plan.md`; those are phase shards and are not part of the refactor bundle model.

Update frontmatter:

- `phase: complete` and `status: complete` if no blockers remain.
- `phase: blocked` and `status: blocked` if blockers remain.
- append `plan` to `phasesCompleted`.
- keep `executionStatus: not-started` when planning completes without blockers.
- update `blockedIssues`.
- update `lastUpdated`.

## Completion Output

Report:

- Refactor bundle path.
- Planning status: complete or blocked.
- Number of tasks.
- Remaining blockers, if any.
- Reminder that implementation has not been performed.
- If planning is complete, tell the user: `Run the bmad_refactor_runner agent to execute this plan.`

## Success Criteria

- Bundle contains `refactor.md` and one or more `tasks/task-*.md` files.
- Task files are thorough enough for a separate implementation workflow.
- Every task file includes validation.
- Every task file includes `Implementation Contract` and `Completion Checks` sections.
- Every task file includes concrete `Done when`, `Evidence required`, and `Forbidden shortcuts` checks.
- The plan contains enough acceptance evidence requirements that a separate verifier could reject scaffolding-only or partially integrated work.
- No files outside the refactor bundle were modified.
