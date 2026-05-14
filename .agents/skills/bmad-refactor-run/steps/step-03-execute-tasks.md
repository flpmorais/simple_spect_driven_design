# Step 3: Execute One Planned Task

## Rules

- Speak in `{communication_language}`.
- Implement only the one task selected during Step 2.
- Keep source changes directly traceable to the selected task contract.
- Update, add, or remove tests as needed with each task.
- Do not mark a task complete until its relevant validation passes.
- Do not mark a task complete until every done-when check for that task has evidence.
- Scaffolding-only completion is forbidden. If a task requires production integration, prove the production path uses the new/refactored code.
- Architecture, PRD/FRs, implementation specifications, project context, and the approved refactor plan are binding. If they conflict, stop and ask. Do not choose a simpler implementation that violates any of them.
- If the implementation must materially deviate from the plan or any binding source, STOP and ask the user.
- A task cannot be complete while tests covering behavior it touched are failing. Narrower passing tests do not override broader failing tests.
- Do not remove or de-productionize an old production path until the replacement path passes the behavior tests that covered the old path.
- Do not delegate task execution to subagents. Implement, test, and record evidence in this current visible session. Read-only exploration/audit subagents may be used when they improve coverage or reduce risk.
- Tool-generated logs and artifacts are valid evidence when they are workspace-local and accessible. Prefer preserving useful tool output in workspace-local logs over rerunning commands unnecessarily.
- Do not read or rely on validation artifacts outside the workspace. If a tool emits an external artifact path, rerun or configure the command so artifacts are written under the refactor execution directory or another gitignored workspace-local path. If validation cannot be completed, update the current task as blocked or in-progress with the reason before exiting.
- When using tools that support artifact/output directories, configure them to write under a workspace-local ignored path such as `tmp/rtk-tee/` or the bundle's `execution/logs/`.

## Task Execution Loop

For the one selected task file only:

1. Read the task file completely, including objective, subtasks, likely files, validation, and risks.
2. Confirm the matching execution file already has `taskStatus: in-progress` from Step 2, or set it immediately before doing anything else. Set `startedAt` if empty. Include or update:
   - task name
   - implementation contract summary
   - done-when checkboxes copied from the plan or derived during preflight
   - required evidence for each checkbox
   - forbidden shortcuts for the task
3. Read current relevant files before editing.
4. Execute exactly the selected task's `Implementation Contract`.
   - Move ownership from the named old owner to the named new owner when the task defines ownership transfer.
   - Wire the named production runtime path.
   - Remove or bypass forbidden implementation patterns.
   - Do not satisfy the task with wrappers, relocated monoliths, unused scaffolding, or evidence-only changes.
   - Do not implement anything outside the selected task contract.
5. Update tests to match the refactor:
   - preserve meaningful existing coverage
   - rewrite tests only when old tests encode obsolete structure or behavior
   - add tests for behavior that may regress
   - remove tests only when the covered behavior is intentionally removed and the plan says so
6. Run the task's targeted validations. Also run directly relevant adjacent validations when the task changes shared contracts, runtime entry points, or cross-boundary behavior.
7. Fix failures and rerun until targeted validations pass.
8. For every done-when checkbox, record evidence directly below it before checking it off. Evidence must be specific:
   - source references such as `path/to/file.py:function_name` or `path/to/file.py:line-range`
   - test names or test files proving the behavior
   - commands run and pass/fail result
   - manual verification notes only when automated validation is not practical
9. Re-read the changed production path and compare it to the task objective. If the task objective is not satisfied in production behavior, leave the checkbox unchecked and continue fixing.
10. Before marking complete, check whether any validation covering behavior touched by this task failed during this task or remains unresolved from an earlier task in this refactor. If yes, set the task `taskStatus: blocked` unless the user explicitly approved deferring that failure.
11. Mark the selected task execution file `taskStatus: complete`, set `completedAt`, and append validations run, files changed, and checklist evidence to that task execution file.
12. Update `refactor.md` task counts if present and update `executionLastUpdated`.
13. STOP after this one task. Report task completed and remaining task count. Do not load Step 4 unless Step 2 selected finalization because all tasks were already complete.

## Stop Conditions

STOP and ask the user if:

- The plan omits necessary work that changes scope materially.
- The plan requires a new dependency, framework, container, architecture component, API pattern, persistence pattern, or security behavior not already approved.
- Project context says X and implementation would require Y.
- Tests reveal behavior ambiguity that needs user intent.
- Dirty overlapping user changes block safe edits.
- Three consecutive attempts cannot make a validation pass.
- A done-when check cannot be proven with source/test evidence.
- The work implemented new scaffolding but did not wire it into the production path required by the plan.

When blocked, update the selected task execution file `taskStatus: blocked`, update refactor frontmatter `executionStatus: blocked`, update `executionLastUpdated`, record the blocker in the relevant task execution file and `execution/validation.md`, and HALT.

## Completion Gate

Do not proceed to another task in this invocation. Step 4 is loaded only by Step 2 when all task execution files are already complete at invocation start.
