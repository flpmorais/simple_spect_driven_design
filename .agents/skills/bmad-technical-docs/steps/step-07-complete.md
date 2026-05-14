# Step 7: Complete Workflow

**Final Step**

## Step Goal

Summarize completed technical documentation work, note validation status, and stop.

## Mandatory Execution Rules

- Read this complete step before taking action.
- Do not load additional step files after this step.
- Do not start another workflow automatically.
- Do not modify files unless completing the configured `on_complete` instruction explicitly requires it.

## Context Boundaries

- The approved plan has been written or reported.
- Validation has completed.

## Sequence Of Instructions

### 1. Summarize Outputs

Report:

- Workflow mode
- Target scope
- Files created
- Files updated
- Audit report path, if any
- Technical docs index path
- State file path

### 2. Summarize Evidence And Validation

Report:

- Main source evidence reviewed
- Whether validation passed
- Any unresolved uncertainties
- Any docs intentionally left untouched

### 3. Explain Maintenance Guidance

Tell the user:

- Update the affected technical docs when code behavior, location, patterns, or rationale changes.
- Use update-from-git-diff mode after implementation changes when doc impact is unclear.
- Use audit mode periodically to find stale or missing documentation.

### 4. On Complete

Run: `python3 {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --key workflow.on_complete`

If the resolved `workflow.on_complete` is non-empty, follow it as the final terminal instruction before exiting.

### 5. Stop

Stop after the completion summary. Do not invoke `bmad-help` or another workflow unless the user asks.

## Success Metrics

- The user knows exactly what changed.
- The user knows what evidence was used.
- Validation status and uncertainties are clear.
- The workflow terminates cleanly.

## Failure Modes

- Starting another workflow automatically.
- Hiding validation gaps.
- Summarizing without file paths.
- Making additional edits after completion.
