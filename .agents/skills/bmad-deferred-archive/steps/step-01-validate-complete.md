# Step 1: Validate Deferred Work Is Complete

## Rules

- Speak in `{communication_language}` if available; otherwise English.
- Do not write anything until the completion gate passes.
- Do not modify tracker files or source files.

## Required Reads

Read fully:

- `{tracker_file}`

If `{tracker_file}` is missing or unreadable, STOP and report the missing file.

If `{archive_file}` exists, read it fully so existing archive keys can be detected later.

## Completion Gate

Inspect every tracker item status.

If any item has status `new`, `triaging`, `needs-user-decision`, `planned`, `in-progress`, or `blocked`:

- STOP without writing.
- Report each blocking item ID and status.
- Explain that `bmad-deferred-archive` can only run after `bmad-deferred-triage` has validated everything and `bmad-deferred-run` has completed all planned work.

If every item is terminal or fixed, continue.

Then load `./step-02-select-items.md`.
