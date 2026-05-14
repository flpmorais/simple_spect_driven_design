# Step 1: Select Refactor Bundle

## Rules

- Speak in `{communication_language}`.
- Do not modify source code in this step.
- Do not modify the refactor bundle until the user accepts an inferred bundle or explicitly provided bundle is validated.
- Incomplete planning bundles and completed executions must be ignored.
- Legacy top-level `refactor-*.md` files are not supported and must be ignored.

## Selection Order

1. If the user provided an explicit refactor bundle directory or `refactor.md` path, use that bundle.
2. Otherwise, inspect `{implementation_artifacts}/refactors/*/refactor.md` bundle indexes.
3. Find bundles with `executionStatus: in-progress` and planning complete. If any exist, suggest the most recently `executionLastUpdated` bundle.
4. If none are in progress, find bundles with planning complete and `executionStatus: not-started`. Suggest the oldest ready bundle by directory timestamp for FIFO execution.
5. If no eligible bundle exists, fail gracefully:

```text
No refactor bundle is ready to run.

Ignored bundles may be incomplete planning workflows, blocked plans, or already completed executions.
Run bmad_refactor_planner first, or provide a completed refactor bundle path.
```

Then HALT.

## User Acceptance For Inferred Artifact

If the bundle was inferred rather than explicitly provided, ask:

```text
I found this refactor bundle to run: <path>

[1] Run this refactor
[2] Choose another refactor bundle
[3] Stop
```

HALT and wait for selection.

- If `[1]`, continue.
- If `[2]`, list eligible bundles and ask the user to choose one. HALT for selection.
- If `[3]`, STOP.

## Validate Selected Bundle

Read the selected bundle index and task files completely. Verify:

- frontmatter has `workflow: bmad-refactor-plan`
- `status: complete`
- `phase: complete`
- `executionStatus: not-started` or `executionStatus: in-progress`
- the path is `{implementation_artifacts}/refactors/<refactor-id>/refactor.md`
- one or more task files exist under `{refactor_dir}/tasks/task-*.md`
- each task file contains Objective, Subtasks, Done when, Evidence required, Forbidden shortcuts, and Validation sections
- phase-shard files such as `context.md`, `exploration.md`, `analysis.md`, or `plan.md` are absent; bundles using those files instead of task files are invalid

If validation fails, STOP and explain why the bundle cannot be run.

## State Update

Update `{refactor_dir}/refactor.md` frontmatter:

- `executionStatus: in-progress`
- `executionStartedAt: <YYYY-MM-DD-HHMM>` if empty
- `executionLastUpdated: <YYYY-MM-DD-HHMM>`
- `executionBranch: <current git branch>`

Create `{refactor_dir}/execution/` if missing.

Create `{refactor_dir}/execution/checklist.md` if missing, initialized from `./checklist.md` plus links to each task execution file.

For every `{refactor_dir}/tasks/task-NN-<slug>.md`, create matching `{refactor_dir}/execution/task-NN-<slug>.md` if missing. Initialize each new execution task file with frontmatter:

```yaml
---
taskStatus: not-started
startedAt: ""
completedAt: ""
---
```

Create `{refactor_dir}/execution/validation.md`, `{refactor_dir}/execution/files-changed.md`, and `{refactor_dir}/execution/commits.md` if missing.

Add or update a compact execution section in `{refactor_dir}/refactor.md` if missing:

```markdown
## Execution

### Execution Status

In progress.

- Status: In progress.
- Checklist: `execution/checklist.md`
- Validation: `execution/validation.md`
- Files changed: `execution/files-changed.md`
- Commits: `execution/commits.md`
```

Then load `./step-02-preflight.md`.
