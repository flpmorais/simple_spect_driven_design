---
refactor_dir: '' # explicit bundle directory, if provided by user or agent invocation
refactor_file: '' # always {refactor_dir}/refactor.md
---

# Refactor Execution Workflow

**Goal:** Advance one deterministic step of a completed refactor bundle: initialize execution, execute exactly one task, or finalize when all tasks are complete.

**Your Role:** You are the refactor execution state machine. You do not execute the whole refactor in one OpenCode run. You advance exactly one task or one finalization step, then stop and report progress. The shell `--refactor --all` loop is responsible for invoking you again.

## Non-Negotiable Rules

- Use only `_bmad-output/implementation-artifacts/refactors/<refactor-id>/refactor.md` bundle indexes generated and completed by `bmad-refactor-plan`.
- Do not execute bundles where planning `status` is not `complete` or `phase` is not `complete`.
- Do not execute bundles with `executionStatus: complete`.
- Do not support legacy top-level `_bmad-output/implementation-artifacts/refactor-*.md` files.
- Execute implementation, validation, evidence recording, commits, and final decisions in the current visible session. Read-only exploration/audit subagents may be used when they improve coverage or reduce risk, but do not delegate implementation to another agent.
- If no explicit file is provided, infer the next candidate and ask the user to accept before modifying source code.
- `_bmad-output/project-context.md` is the golden source of technical rules. If it is missing or unreadable, fail gracefully and tell the user execution cannot continue until project context exists.
- Architecture, PRD/FRs, implementation specifications, project context, and the approved refactor plan are binding. If they conflict, stop and ask. Do not choose a simpler implementation that violates any of them.
- If execution discovers the plan is materially wrong, incomplete, unsafe, or conflicts with a binding source, STOP and ask the user before deviating.
- A task cannot be complete while tests covering behavior it touched are failing. Narrower passing tests do not override broader failing tests.
- Do not remove or de-productionize an old production path until the replacement path passes the behavior tests that covered the old path.
- Tests must be updated, added, or removed as needed to match the refactor. Do not blindly rewrite tests that still provide correct coverage.
- Run the selected task's targeted validations by default. Also run directly relevant adjacent validations when the selected task changes shared contracts, runtime entry points, or cross-boundary behavior. Run broader validations during finalization.
- Tool-generated logs and artifacts are valid evidence when they are workspace-local and accessible. Prefer preserving useful tool output in workspace-local logs over rerunning commands unnecessarily.
- Do not read or rely on validation artifacts outside the workspace. If a tool emits an external artifact path, rerun or configure the command so artifacts are written under the refactor execution directory or another gitignored workspace-local path. If validation cannot be completed, update the current task as blocked or in-progress with the reason before exiting.
- When using tools that support artifact/output directories, configure them to write under a workspace-local ignored path such as `tmp/rtk-tee/` or the bundle's `execution/logs/`.
- Do not complete scaffolding-only work. New files, wrappers, adapters, or tests are not sufficient unless the planned behavior is actually wired into the production path named by the plan.
- Every completed task must have evidence in the execution record: checked acceptance items, source references, validation commands/results, and any residual caveats.
- Commit and push only during the finalization step after every task execution file is complete. Never force push.

## Step Model

Each invocation performs exactly one of these actions:

1. Initialize the bundle execution files, select the first task, and execute that one task.
2. Resume the one task already marked `taskStatus: in-progress`, and execute only that task.
3. Select the first task whose execution file is not `taskStatus: complete`, mark it `taskStatus: in-progress`, and execute only that task.
4. If all tasks are complete, run final validation, commit, push, update the bundle, and stop.

Do not continue to the next task in the same invocation after completing a task.

## Configuration Loading

Load config from `{project-root}/_bmad/bmm/config.yaml` and resolve:

- `implementation_artifacts`
- `project_context` = `{project-root}/_bmad-output/project-context.md`
- `communication_language`
- `document_output_language`
- `user_skill_level`
- `date` and `time` as system-generated current values

If config loading fails, use:

- `implementation_artifacts` = `{project-root}/_bmad-output/implementation-artifacts`
- `project_context` = `{project-root}/_bmad-output/project-context.md`

## Artifact Eligibility

Eligible artifacts must match all of these:

- Path matches `{implementation_artifacts}/refactors/<refactor-id>/refactor.md`, or the user-provided path is the bundle directory containing `refactor.md`.
- Frontmatter `workflow: bmad-refactor-plan`.
- Frontmatter `status: complete`.
- Frontmatter `phase: complete`.
- Frontmatter `executionStatus` is `not-started` or `in-progress`.
- Required task files exist under `tasks/task-*.md`.

Invalid artifacts:

- Missing or malformed frontmatter.
- Planning status `in-progress` or `blocked`.
- Planning phase other than `complete`.
- `executionStatus: complete`.
- Top-level legacy `refactor-*.md` files.
- Phase-sharded bundles that contain `context.md`, `exploration.md`, `analysis.md`, or `plan.md` instead of task files.
- Any file or directory not matching the refactor bundle naming convention.

## Execution

Read fully and follow `./steps/step-01-select-artifact.md`.
