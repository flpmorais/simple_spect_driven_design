# Step 1: Normalize Deferred Work

## Rules

- Speak in `{communication_language}` if available; otherwise English.
- Do not modify source code.
- Do not modify `deferred-work.md`.
- Create or update only the tracker and per-item deferred artifacts.

## Required Reads

Read fully:

- `{deferred_work_file}`
- `{project_context_file}`

If either is missing or unreadable, STOP and report the missing file.

If `{tracker_file}` exists, read it fully before normalizing to avoid duplicate IDs.

## Resume Pending Batch Response

If the latest user message is a response to a previously presented deferred triage batch, resume that batch before selecting new work:

- Identify the pending batch from the current conversation and tracker items with status `triaging` or `needs-user-decision`.
- Apply `approve all` or per-item overrides from the user's response.
- Update `{tracker_file}` with the approved statuses, decisions, notes, duplicate targets, and plan-work decisions.
- If any approved item is `plan-work`, load `./step-04-plan.md` for those items.
- If no approved item is `plan-work`, continue this step and select the next batch.
- Do not stop after applying a single response unless the user explicitly said to stop.

## Normalize Raw Items

Parse `deferred-work.md` by heading and bullet:

- Source heading: the `## Deferred from: ...` heading.
- Source item text: the bullet content exactly as written.
- Source references: any bracketed paths or line references in the bullet.

Assign stable IDs only to newly discovered raw bullets:

- Format: `DW-0001`, `DW-0002`, etc.
- Preserve existing IDs and statuses from `{tracker_file}`.
- Do not renumber existing items.

Create `{tracker_file}` if missing with this structure:

```markdown
# Deferred Work Tracker

_Tracks triage and execution state for items originally recorded in `deferred-work.md`. Do not delete raw source history from `deferred-work.md`._

## Status Definitions

<status list>

## Items

### DW-0001: <short title>

- Status: new
- Source: <source heading>
- Raw item: <exact bullet text>
- Plan artifact:
- Decision:
- Notes:
```

## Auto-Classify Obvious Obsolete And Duplicate Items

Before asking the user for decisions, scan all tracker items with status `new`, `triaging`, or `needs-user-decision` and auto-classify only obsolete and duplicate cases with clear evidence:

- `duplicate`: the item describes the same underlying issue, same affected behavior, or same required fix as an earlier tracker item.
- `obsolete`: current code, current project context, or later completed work clearly proves the item is already fixed or no longer relevant.

Duplicate rules:

- Use earliest-item-wins by tracker order.
- Keep the earliest matching item active.
- Mark only later items as `duplicate`.
- Record `Duplicate of DW-xxxx` in `Decision` and summarize the overlap in `Notes`.

Obsolete rules:

- Require concrete evidence from code, project context, or tracker state.
- Record the evidence in `Decision` and `Notes`.
- Do not auto-mark subjective low-priority, prototype-phase, intentional, or risk-acceptance items as obsolete.

Progress-count rules:

- Count how many items were auto-classified as `obsolete` during this pass.
- Count how many items were auto-classified as `duplicate` during this pass.
- Do not include auto-classified obsolete or duplicate items in the user validation batch.
- Summarize auto-classified obsolete/duplicate counts in the next batch prompt, not as items requiring approval.

Do not auto-classify ambiguous items. Leave them for the user validation batch.

## Select Batch

If the user provided explicit deferred item IDs, use those IDs as the batch, up to 10 items.

Otherwise select the first 10 items by tracker order whose status is `new`, `triaging`, or `needs-user-decision` after the auto-classification pass.

Before loading the next step, compute and carry forward these counts for the batch prompt:

- remaining items needing user validation before the batch
- items selected in the current batch
- estimated remaining items needing user validation after approving the batch
- auto-classified obsolete count from this pass
- auto-classified duplicate count from this pass

If no such item exists, report completion:

```text
Deferred work triage is complete. No item needs classification. Items are terminal, planned, blocked, in progress, or done.
```

Then HALT.

Set each selected item with status `new` to `triaging`. Preserve `needs-user-decision` so prior blockers remain visible.

Then load `./step-02-understand.md`.
