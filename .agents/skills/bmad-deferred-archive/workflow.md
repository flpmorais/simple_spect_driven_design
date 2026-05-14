---
tracker_file: '{project-root}/_bmad-output/implementation-artifacts/deferred-work-tracker.md'
archive_file: '{project-root}/_bmad-output/deferred-work.md'
---

# Deferred Work Archive Workflow

**Goal:** After deferred triage and deferred execution are complete, preserve validated deferred items that remain intentionally unfixed in `_bmad-output/deferred-work.md`.

**Your Role:** You are a deferred-work archive gatekeeper. You must prove the prior deferred workflows are complete before appending anything. You preserve local tracker IDs but use work-package-qualified keys so archives from multiple work packages do not collide.

## Non-Negotiable Rules

- This skill may run only after all deferred items are validated and all approved deferred work is done.
- Read `_bmad-output/implementation-artifacts/deferred-work-tracker.md` fully before writing.
- Create `_bmad-output/deferred-work.md` if it does not exist.
- Only append to `_bmad-output/deferred-work.md`.
- Do not modify source code, tests, tracker files, plan artifacts, sprint status, raw implementation deferred-work history, or project context.
- Exclude items with status `obsolete`, `duplicate`, or `done`.
- Include validated non-fixed items such as `accepted-risk` and `no-action`.
- Use a composite archive key `<workPackageId>/<localId>` to avoid ID clashes across work packages.
- Preserve the original tracker ID as `Local ID`.
- Be idempotent: do not append an item if its composite archive key already exists in `_bmad-output/deferred-work.md`.

## Completion Gate

Before appending anything, fail gracefully if any tracker item has one of these statuses:

- `new`
- `triaging`
- `needs-user-decision`
- `planned`
- `in-progress`
- `blocked`

Report the blocking item IDs and statuses, then HALT without writing.

## Execution

Read fully and follow `./steps/step-01-validate-complete.md`.
