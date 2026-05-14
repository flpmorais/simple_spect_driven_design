# Step 1b: Continue Refactor Planning Workflow

## Rules

- Speak in `{communication_language}`.
- Read the selected `{refactor_file}` completely.
- Resume from persisted frontmatter state. Do not repeat completed phases unless the user asks to revise them.
- Only modify files inside `{refactor_dir}`.

## Continuation Sequence

1. Load `{refactor_file}` and any existing `tasks/task-*.md` files.
2. Parse frontmatter fields: `workflow`, `status`, `phase`, `phasesCompleted`, `refactorName`, `decisions`, and `blockedIssues`.
3. Verify `workflow: bmad-refactor-plan`. If not, STOP and ask the user for a valid refactor bundle.
4. Verify `{refactor_file}` is named `refactor.md` and lives under `{implementation_artifacts}/refactors/<refactor-id>/`. If not, STOP; legacy top-level `refactor-*.md` files are not supported.
5. Summarize current progress:
   - Refactor name.
   - Current phase.
   - Completed phases.
   - Decisions already made.
   - Blocked issues.
6. Ask the user how to continue:

```text
How would you like to continue?

[1] Resume from current phase
[2] Revise context
[3] Revise analysis decisions
[4] Stop
```

HALT and wait for selection.

## Routing

- If current phase is `context`, load `./step-01-context.md` and continue context confirmation without creating a new bundle.
- If current phase is `exploration`, load `./step-02-exploration.md`.
- If current phase is `analysis`, load `./step-03-analysis.md`.
- If current phase is `plan`, load `./step-04-plan.md`.
- If current phase is `complete`, ask whether the user wants to revise or start a new refactor plan.
- If current phase is `blocked`, present blockers and ask whether any are resolved before routing.

## Success Criteria

- Existing workflow state is preserved.
- Completed phases are not repeated without user approval.
- User is routed to the correct next step.
