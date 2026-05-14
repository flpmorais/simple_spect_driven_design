# Step 3: Classify And Decide Batch

## Rules

- Speak in `{communication_language}` if available; otherwise English.
- Do not create a plan until classification is clear.
- Ambiguous items require user decision.
- Present at most 10 items in one decision batch.
- Do not ask the user to validate items auto-classified as `obsolete` or `duplicate`.
- Keep going after decisions are applied; do not stop after one item.

## Classification Buckets

Recommend exactly one classification for each selected item:

- `no-action`: intentional behavior or no work needed.
- `obsolete`: already fixed or no longer relevant.
- `duplicate`: covered by another deferred item; link the duplicate target.
- `accepted-risk`: real issue, intentionally accepted for now.
- `needs-user-decision`: product, architecture, risk, or scope decision required.
- `plan-work`: concrete implementation/test work should be done.

## Batch User Review Gate

Before listing items, present progress counts:

- Items needing validation before this batch: <count>
- Items in this batch: <count>
- Estimated remaining after approving this batch: <count>
- Auto-classified since last batch: <obsolete count> obsolete, <duplicate count> duplicate

Then present a compact table or numbered list for the selected batch. For each item include:

- item ID and short title
- concise raw item summary, not the full tracker section
- evidence from current code or project context
- recommended classification
- rationale
- if `duplicate`, the canonical item ID
- if `plan-work`, the proposed solution/scope and validation approach
- if `needs-user-decision`, the exact question to answer

Ask:

```text
Review this deferred work batch.

Progress:
- Needs validation before batch: <count>
- Current batch: <count>
- Remaining after approval: <count>
- Auto-classified since last batch: <obsolete count> obsolete, <duplicate count> duplicate

[1] Approve all recommendations
[2] Approve with overrides
[3] Stop after recording no further changes

For overrides, reply with entries like:
DW-0007: obsolete, because <reason>
DW-0011: plan-work, solution: <scope>
DW-0014: duplicate of DW-0012
```

HALT and wait for the user's selection.

After the user responds, update `{tracker_file}` for every batch item based on the approved recommendations and overrides:

- `no-action`, `obsolete`, `duplicate`, `accepted-risk`: record decision and terminal status.
- `needs-user-decision`: record the question/blocker and status.
- `plan-work`: continue to `./step-04-plan.md` for those items.

If the user chooses to stop, report the current tracker state and HALT.

After applying the batch, report:

- item IDs updated in the batch
- plan-work item IDs, if any
- remaining items still needing validation

If no item in the approved batch is `plan-work`, immediately return to `./step-01-normalize.md` and continue with the next batch.
