# Step 4: Full Validation

## Rules

- Speak in `{communication_language}`.
- Do not mark execution complete until all required validations pass.
- Run the validations listed in the plan. Add broader validations when the repository makes them available and they are relevant.
- Load and apply `./checklist.md` before completion.
- Validate the refactor objective against production integration, not just against new tests or newly added files.
- Architecture, PRD/FRs, implementation specifications, project context, and the approved refactor plan are binding. If they conflict, stop and ask. Do not choose a simpler implementation that violates any of them.
- Narrower passing tests do not override broader failing tests. Execution cannot complete while tests covering touched behavior are failing.
- Run this step only when all `execution/task-*.md` files already have `taskStatus: complete` at invocation start.
- Tool-generated logs and artifacts are valid evidence when they are workspace-local and accessible. Prefer preserving useful tool output in workspace-local logs over rerunning commands unnecessarily.
- Do not read or rely on validation artifacts outside the workspace. If a tool emits an external artifact path, rerun or configure the command so artifacts are written under the refactor execution directory or another gitignored workspace-local path. If validation cannot be completed, update `executionStatus: blocked` with the reason before exiting.
- When using tools that support artifact/output directories, configure them to write under a workspace-local ignored path such as `tmp/rtk-tee/` or the bundle's `execution/logs/`.

## Validation Requirements

Run:

- All task-level validations from the plan that have not already been run after the final changes.
- A checklist audit of `execution/checklist.md` and every `execution/task-*.md`: every checkbox must be checked, and every checked item must have concrete evidence.
- A task-status audit: every `execution/task-*.md` must have frontmatter `taskStatus: complete`.
- A production-path audit: identify the runtime entry points affected by the refactor and verify they now use the refactored code required by the plan.
- A scaffolding audit: identify newly added modules/helpers/adapters and verify they are either used by production paths or explicitly documented as approved extension points/non-goals.
- Relevant unit tests.
- Relevant integration tests when affected behavior crosses module/API boundaries.
- Relevant e2e tests when user flows are affected.
- Lint/type/static checks if configured and relevant.
- Any project-specific validation commands named in the plan.

If tests need updates discovered during validation, update tests and rerun.

If validation fails:

1. Diagnose the failure.
2. Fix source or tests according to the approved plan.
3. Rerun the failed validation.
4. Repeat until pass or a stop condition applies.

Do not lower test expectations just to pass. If a test expectation conflicts with intended refactor behavior, update the test with a clear note in the relevant task execution file and `execution/validation.md`.

If the production-path audit shows that the main refactor objective is not actually wired into runtime behavior, set `executionStatus: blocked`, record the failed acceptance check in `execution/validation.md`, and HALT. Do not mark execution complete.

## Record Validation

Append to `execution/validation.md`:

- commands run
- pass/fail result
- notable fixes after failures
- any validations not run and why
- production-path audit result
- scaffolding audit result

Update `executionLastUpdated`.

When all required validations pass, load `./step-05-complete.md`.
