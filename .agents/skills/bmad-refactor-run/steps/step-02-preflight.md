# Step 2: Preflight

## Rules

- Speak in `{communication_language}`.
- Read the selected refactor bundle completely.
- Do not start source edits until preflight passes.
- Respect existing worktree changes. Never revert unrelated user changes.
- Use direct reads/searches in this visible session by default. Read-only exploration/audit subagents may be used when they improve coverage or reduce risk, but do not delegate implementation or decisions.

## Required Reads

Load:

- Selected refactor bundle index and task files: `refactor.md` and `tasks/task-*.md`.
- `{project_context}` (`_bmad-output/project-context.md`).
- The one selected task file only after selection below.

If project context is missing or unreadable, fail gracefully: explain that `_bmad-output/project-context.md` is required as the golden technical rules source, set `executionStatus: blocked`, record the blocker in `execution/validation.md`, and HALT.

## Git Preflight

Inspect git status before edits:

- Identify current branch.
- Identify modified, staged, and untracked files.
- Compare dirty files with the plan's likely touched files.

If unrelated dirty files exist but do not overlap the plan, continue without touching them and note them in `execution/validation.md`.

If dirty files overlap planned changes and were not created by this workflow, STOP and ask the user how to proceed.

If detached HEAD, STOP and ask the user to switch/create a branch.

## Plan Alignment Check

Before editing, verify:

- The plan is still coherent with current code.
- The plan does not conflict with architecture, PRD/FRs, project context, implementation specifications, or the approved refactor plan.
- The planned tasks include validation.
- The planned tasks include concrete done-when acceptance checks or enough task detail to derive them before coding.
- The test strategy is adequate for the refactor.

If the plan is stale, incomplete, or conflicts with a binding source, update `execution/validation.md` with the issue, set `executionStatus: blocked`, and ask the user for a decision. Do not proceed silently.

## Select One Task

Select exactly one next action:

1. If any `execution/task-*.md` has frontmatter `taskStatus: in-progress`, select the numerically first such task.
2. Else select the numerically first `execution/task-*.md` whose frontmatter is not `taskStatus: complete`.
3. If every `execution/task-*.md` is complete, append the preflight entry below, update `executionLastUpdated`, then load `./step-04-validate.md` and do not execute source changes in this invocation.

Load only the selected task file and its matching execution file. If the selected task file lacks an `Implementation Contract` or `Completion Checks`, set that task `taskStatus: blocked`, record the missing contract in the task execution file and `execution/validation.md`, update `executionLastUpdated`, and HALT.

If a task file lacks concrete done-when checks, derive task-specific checks from its objective, subtasks, expected behavior, and validation before coding. Record those checks in the matching task execution file. If concrete checks cannot be derived without changing scope or guessing user intent, set `taskStatus: blocked`, record the reason, and HALT.

Before running validations, diagnostics, source reads beyond the selected task scope, or edits, update the selected task execution file to `taskStatus: in-progress` and set `startedAt` if empty. If this update cannot be made, HALT before attempting task work.

## State Update

Append a preflight entry to `execution/validation.md` summarizing:

- selected bundle
- selected task, if any
- branch
- dirty worktree notes
- project context loaded or missing
- preflight result

Update `executionLastUpdated`.

If a task was selected, load `./step-03-execute-tasks.md`. If all tasks were already complete, load `./step-04-validate.md`.
