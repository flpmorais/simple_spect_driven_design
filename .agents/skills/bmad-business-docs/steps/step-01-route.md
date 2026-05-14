# Step 1: Route Business Documentation Work

**Progress: Step 1 of 7** - Next: Domain Scope

## Step Goal

Determine the business documentation mode and route the workflow without modifying files.

## Mandatory Execution Rules

- Read this complete step before taking action.
- Do not inspect implementation files yet except to check whether business artifacts already exist.
- Do not create or edit documentation in this step.
- If a menu is presented, stop and wait for user input.

## Sequence Of Instructions

### 1. Check Existing Business Docs State

Check whether these paths exist:

- `{businessArtifactsRoot}`
- `{businessDocsIndex}`
- `{businessStateFile}`
- `{domainsRoot}`
- `{crossDomainRoot}`

If `{businessStateFile}` exists, read it and summarize only high-level state:

- Last workflow mode
- Last updated timestamp
- Known domains
- Known open discrepancies

### 2. Detect Requested Mode

Infer mode from the user's request if clear:

- `create-domain-map`: establish the business documentation structure and domain map.
- `capture-rules`: capture business rules from user discussion or existing documents.
- `update-domain`: update one existing business domain or add a new domain.
- `extract-observed-behavior`: inspect code/docs and propose candidate business rules as observed behavior.
- `audit-business-docs`: report missing, contradictory, stale, or ambiguous business docs without editing.
- `resolve-discrepancies`: compare approved business docs, planning artifacts, and implementation evidence to produce discrepancy decisions.

If mode is clear, state the detected mode, set `workflowMode`, then read fully and follow `./step-02-domain-scope.md`.

If mode is not clear, present the menu in section 3.

### 3. Present Mode Menu If Needed

Display:

```text
Business Docs Workflow

Existing business docs state:
- Business artifacts root: {exists|missing}
- Business docs index: {exists|missing}
- Domains folder: {exists|missing}
- State file: {exists|missing}

Choose the work type:

[M] Create domain map - Establish business-artifacts with domain folders
[C] Capture rules - Convert discussion or existing docs into business rules
[U] Update domain - Update one domain's docs
[O] Extract observed behavior - Inspect code/docs and propose candidate business rules
[A] Audit business docs - Find missing, conflicting, stale, or ambiguous rules
[D] Resolve discrepancies - Compare approved intent vs observed implementation
[X] Exit - Stop without changes
```

### 4. Menu Handling Logic

- If `M`: set `workflowMode = create-domain-map`, then read fully and follow `./step-02-domain-scope.md`.
- If `C`: set `workflowMode = capture-rules`, then read fully and follow `./step-02-domain-scope.md`.
- If `U`: set `workflowMode = update-domain`, then read fully and follow `./step-02-domain-scope.md`.
- If `O`: set `workflowMode = extract-observed-behavior`, then read fully and follow `./step-02-domain-scope.md`.
- If `A`: set `workflowMode = audit-business-docs`, then read fully and follow `./step-02-domain-scope.md`.
- If `D`: set `workflowMode = resolve-discrepancies`, then read fully and follow `./step-02-domain-scope.md`.
- If `X`: exit without changes.
- If any other response: clarify briefly and redisplay the menu.

## Success Metrics

- Existing business docs state was checked.
- Workflow mode is known.
- No docs or code were modified.

## Failure Modes

- Creating or editing docs in this step.
- Treating implementation as business truth.
- Proceeding without a clear mode.
