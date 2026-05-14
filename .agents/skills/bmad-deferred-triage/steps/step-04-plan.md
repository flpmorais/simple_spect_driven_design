# Step 4: Create Deferred Item Plans

## Rules

- Speak in `{communication_language}` if available; otherwise English.
- Create plan artifacts only for approved `plan-work` items.
- Do not modify source code.
- Include tests and validation in the plan.

## Plan Artifact

Create `{deferred_artifacts_dir}` if needed.

For each approved `plan-work` item, create:

`{deferred_artifacts_dir}/deferred-<id>-<slug>.md`

Use this structure:

```markdown
---
workflow: bmad-deferred
id: DW-0001
status: planned
source: <source heading>
createdAt: <YYYY-MM-DD-HHMM>
updatedAt: <YYYY-MM-DD-HHMM>
---

# Deferred Work Plan: DW-0001 <Title>

## Raw Item

## Understanding

## Decision

## Plan

### Tasks

#### 1. <Task>

- Objective:
- Likely files / areas:
- Subtasks:
- Tests to update/add:
- Validation:
- Risks / notes:

## Execution Record

_Pending execution by `bmad-deferred-run`._
```

## Tracker Update

Update `{tracker_file}` for each planned item:

- Status: `planned`
- Plan artifact: relative path to the created plan
- Decision: concise user-approved decision
- Notes: summary of planned scope

## Continue Triage

After creating plan artifacts for the approved batch:

- Report the planned item IDs and artifact paths.
- Report remaining items still needing validation.
- Immediately return to `./step-01-normalize.md` and continue with the next batch.
- Do not stop unless all items are terminal/planned, required context is missing, or the user explicitly said to stop.

## Completion Output

When all triage is complete, report:

- item IDs handled in the last batch
- tracker path
- plan artifact paths, if any
- summary of planned work, terminal classifications, and remaining blocked items
- tests/validations that execution must run for planned work
