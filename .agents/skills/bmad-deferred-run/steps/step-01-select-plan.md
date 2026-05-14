# Step 1: Select Deferred Plan

## Rules

- Speak in `{communication_language}` if available; otherwise English.
- Do not modify source code until a valid plan is selected.
- Do not execute terminal items.

## Selection

If the user provided a deferred plan artifact path or ID, use it.

Otherwise:

1. Read `{tracker_file}`.
2. Prefer the first item with status `in-progress` and a plan artifact.
3. Else select the first item with status `planned` and a plan artifact.
4. If no eligible plan exists, fail gracefully and tell the user to run `bmad-deferred-triage` first.

If selection is inferred, ask:

```text
I found this deferred work plan to execute: <path>

[1] Execute this plan
[2] Choose another plan
[3] Stop
```

HALT and wait for user confirmation.

## Validate Plan

Read the plan artifact and validate:

- `workflow: bmad-deferred`
- `status: planned` or `status: in-progress`
- contains `## Plan`
- contains tests/validation requirements

If invalid, STOP and explain why it cannot be executed.

Update plan frontmatter `status: in-progress` and tracker item status `in-progress`.

Then load `./step-02-preflight.md`.
