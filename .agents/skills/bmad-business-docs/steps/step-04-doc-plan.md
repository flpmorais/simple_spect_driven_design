# Step 4: Create Business Documentation Plan

**Progress: Step 4 of 7** - Next: Write Or Report

## Step Goal

Convert discovered business evidence into an approved plan for creating, updating, auditing, or discrepancy reporting.

## Mandatory Execution Rules

- Read this complete step before taking action.
- Do not write or edit files until the user selects `C`.
- Name exact output files and whether each is created, updated, or reported only.
- For updates, identify exact sections to replace.
- Stop at the menu and wait for user input.

## Sequence Of Instructions

### 1. Build The Plan

Prepare a plan with:

- Mode
- Domain slugs and names
- Domain prefixes for rule IDs
- Files to create
- Files to update
- Sections to replace
- Rules to add or revise
- Workflow tables to add or revise
- Decision tables to add or revise
- Open questions to record
- Discrepancies to record
- Files to leave untouched

### 2. Default Domain File Set

For each selected domain, use:

- `{domainsRoot}/<domain-slug>/overview.md`
- `{domainsRoot}/<domain-slug>/rules.md`
- `{domainsRoot}/<domain-slug>/workflows.md`
- `{domainsRoot}/<domain-slug>/decision-tables.md`
- `{domainsRoot}/<domain-slug>/open-questions.md`

Create only the files needed by the evidence and approved plan. Do not create empty domain files just to fill a template.

### 3. Cross-Domain Files

Use cross-domain files only for content that applies across multiple domains:

- `{crossDomainRoot}/policies.md`
- `{crossDomainRoot}/invariants.md`
- `{crossDomainRoot}/discrepancies.md`

### 4. Rule ID Planning

Assign each domain a short prefix, such as:

- `WI` for work-intake
- `KL` for kanban-lifecycle
- `WD` for workflow-dispatch
- `AE` for agent-execution
- `AL` for artifact-lifecycle
- `RA` for review-and-approval
- `GV` for governance

If an existing prefix exists, preserve it. Number new rules sequentially without reusing deprecated IDs.

### 5. Present Plan

Display:

```text
Business documentation plan:
- Mode: {workflowMode}
- Domains: {domains}
- Rule prefixes: {prefixes}

Create:
{files_to_create}

Update:
{files_to_update_with_sections}

Record as open questions:
{open_questions}

Record as discrepancies:
{discrepancies}

Leave untouched:
{files_to_leave_untouched}

Proceed?

[C] Continue and write/report
[R] Revise plan
[A] Audit only instead of writing docs
[X] Exit without changes
```

### 6. Menu Handling Logic

- If `C`: lock the plan, then read fully and follow `./step-05-write.md`.
- If `R`: ask what to change, revise the plan, and redisplay the menu.
- If `A`: set `workflowMode = audit-business-docs`, convert the plan to audit-only, and redisplay the menu.
- If `X`: exit without changes.
- If any other response: clarify briefly and redisplay the menu.

## Success Metrics

- Exact files and sections are planned.
- User approved before writes.
- Rule IDs and statuses are clear.
- Discrepancies and open questions are not hidden.

## Failure Modes

- Writing before approval.
- Creating empty template docs without evidence.
- Reusing retired rule IDs.
- Omitting discrepancy handling.
