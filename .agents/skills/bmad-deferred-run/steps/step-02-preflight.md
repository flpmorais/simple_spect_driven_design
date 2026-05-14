# Step 2: Preflight

## Rules

- Speak in `{communication_language}` if available; otherwise English.
- Respect unrelated dirty worktree changes.
- Do not start edits until preflight passes.

## Required Reads

Read:

- selected deferred plan artifact
- `{tracker_file}`
- `{project_context_file}`
- referenced source/test files from the plan

If project context is missing or unreadable, mark the plan/tracker `blocked`, record the blocker, and HALT.

## Git Preflight

Inspect git status:

- Identify branch.
- Identify dirty files.
- Compare dirty files to planned touched files.

If dirty files overlap planned work and were not made by this workflow, STOP and ask the user.

If detached HEAD, STOP and ask the user to switch/create a branch.

## Plan Check

Confirm:

- plan is still relevant to current code
- plan does not violate project context
- validation commands are sufficient

If stale, unsafe, or incomplete, mark `blocked`, record why, and ask the user.

Then load `./step-03-execute.md`.
