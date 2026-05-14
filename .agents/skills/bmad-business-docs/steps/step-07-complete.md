# Step 7: Complete Workflow

**Final Step**

## Step Goal

Summarize completed business documentation work, validation status, open questions, and discrepancies.

## Mandatory Execution Rules

- Read this complete step before taking action.
- Do not load additional step files after this step.
- Do not start another workflow automatically.
- Do not modify files unless completing configured `on_complete` explicitly requires it.

## Sequence Of Instructions

### 1. Summarize Outputs

Report:

- Workflow mode
- Domain scope
- Files created
- Files updated
- Audit report path, if any
- Business docs index path
- State file path

### 2. Summarize Business Status

Report:

- Approved rules added or updated
- Proposed rules added or updated
- Observed behaviors recorded
- Open questions recorded
- Discrepancies recorded

### 3. Summarize Validation

Report:

- Whether validation passed
- Any unresolved uncertainties
- Any docs intentionally left untouched

### 4. Maintenance Guidance

Tell the user:

- Update business docs when a domain decision changes.
- Use observed-behavior extraction when implementation exists but business policy is unclear.
- Use discrepancy resolution when approved rules and implementation disagree.

### 5. On Complete

Run: `python3 {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --key workflow.on_complete`

If the resolved `workflow.on_complete` is non-empty, follow it as the final terminal instruction before exiting.

### 6. Stop

Stop after the completion summary. Do not invoke another workflow unless the user asks.

## Success Metrics

- The user knows exactly what changed.
- Open questions and discrepancies are visible.
- Validation status is clear.
- The workflow terminates cleanly.

## Failure Modes

- Starting another workflow automatically.
- Hiding unresolved decisions.
- Summarizing without file paths.
