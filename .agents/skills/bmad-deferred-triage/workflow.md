---
deferred_work_file: '{project-root}/_bmad-output/implementation-artifacts/deferred-work.md'
tracker_file: '{project-root}/_bmad-output/implementation-artifacts/deferred-work-tracker.md'
deferred_artifacts_dir: '{project-root}/_bmad-output/implementation-artifacts/deferred'
project_context_file: '{project-root}/_bmad-output/project-context.md'
---

# Deferred Work Triage Workflow

**Goal:** Turn raw deferred review findings into explicit decisions and executable plans with minimal user friction: auto-classify obvious obsolete/duplicate items, then batch the remaining decisions 10 at a time until triage is complete.

**Your Role:** You are a deferred-work triage facilitator. You preserve the raw source history, normalize items into a tracker, inspect the current code, classify obvious obsolete/duplicate cases automatically, present concise 10-item decision batches for cases needing user judgment, apply user decisions, and continue until every item is terminal or planned.

## Non-Negotiable Rules

- Treat `_bmad-output/implementation-artifacts/deferred-work.md` as raw audit history. Do not modify it.
- Store workflow state in `_bmad-output/implementation-artifacts/deferred-work-tracker.md`.
- Store per-item plans in `_bmad-output/implementation-artifacts/deferred/deferred-<id>-<slug>.md`.
- Do not modify source code in this workflow.
- Read `_bmad-output/project-context.md` as the golden technical rules source. If missing or unreadable, fail gracefully.
- Do not ask the user to review the entire tracker or raw deferred file.
- Auto-classify obvious duplicates and obsolete items before asking the user. Do not ask the user to validate auto-classified obsolete or duplicate items.
- For duplicates, keep the earliest tracker item as canonical and mark only later duplicates as `duplicate`.
- Triage non-obvious items in batches of up to 10.
- Every batch prompt must report how many items still need user validation before the batch, how many are in the current batch, how many will remain if the user approves the batch, and how many items were auto-classified as obsolete or duplicate since the last batch.
- After each user response, apply decisions and immediately continue with the next batch.
- Stop only when every item is terminal or planned, when required context is missing, or when the user explicitly says to stop.
- Do not silently turn ambiguous items into work. Recommend a classification and proposed solution, then ask the user to approve or override.

## Status Values

- `new`: normalized, not triaged.
- `triaging`: currently under review.
- `needs-user-decision`: user decision required.
- `accepted-risk`: real issue intentionally accepted.
- `no-action`: no work needed.
- `obsolete`: already fixed or no longer relevant.
- `duplicate`: same as another tracked item.
- `planned`: executable plan exists.
- `in-progress`: execution started by deferred runner.
- `blocked`: execution or planning blocked.
- `done`: completed.

## Execution

Read fully and follow `./steps/step-01-normalize.md`.
