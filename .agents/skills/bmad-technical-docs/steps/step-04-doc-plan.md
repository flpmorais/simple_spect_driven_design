# Step 4: Create Documentation Plan

**Progress: Step 4 of 7** - Next: Write Or Report

## Step Goal

Turn evidence into a concrete documentation plan and get approval before writing or producing an audit report.

## Mandatory Execution Rules

- Read this complete step before taking action.
- Do not write or edit files until the user selects `C`.
- The plan must name exact output files and whether each file is created, updated, or only reported on.
- For update mode, identify exact sections to replace.
- Stop at the menu and wait for user input.

## Context Boundaries

- Evidence exploration from Step 3 is available.
- The user-confirmed scope from Step 2 is still binding.

## Sequence Of Instructions

### 1. Build The Plan

Prepare a plan with these fields:

- Mode
- Target
- Files to create
- Files to update
- Sections to replace
- Files to leave untouched
- Audit report path, if audit mode
- Evidence sources that will be cited in frontmatter or related-code sections
- Open uncertainties

### 2. Apply Mode-Specific Planning Rules

#### create-docs-set

Prefer a minimal docs set:

- Always create or update `{technicalDocsIndex}`.
- Create `{technicalDocsRoot}/code-map.md` only if a repository or subsystem map is in scope.
- Create `{technicalDocsRoot}/patterns.md` only if cross-cutting implementation patterns are evidenced.
- Create topic docs only for distinct, non-trivial technical areas.

#### document-target

Prefer one focused topic doc. Do not split unless the target covers multiple independent technical areas.

#### update-docs

Prefer targeted section replacement inside existing docs. Create a new doc only when no existing doc has the right scope.

#### update-from-git-diff

Map each changed source file to:

- Existing doc to update
- New doc to create
- No doc update needed, with reason

#### audit-docs

Do not modify docs. Plan an audit report under `{technicalDocsRoot}/audit-technical-docs-{{date}}.md` unless the user requested a different path.

### 3. Present Plan

Display:

```text
Documentation plan:
- Mode: {workflowMode}
- Target: {target}

Create:
{files_to_create}

Update:
{files_to_update_with_sections}

Leave untouched:
{files_to_leave_untouched}

Evidence basis:
{source_summary}

Uncertainties:
{uncertainties_or_none}

Proceed?

[C] Continue and write/report
[R] Revise plan
[A] Audit only instead of writing
[X] Exit without changes
```

### 4. Menu Handling Logic

- If `C`: lock the plan, then read fully and follow `./step-05-write.md`.
- If `R`: ask what to change, revise the plan, and redisplay the menu.
- If `A`: set `workflowMode = audit-docs`, convert the plan to audit-only, and redisplay the menu.
- If `X`: exit without changes.
- If any other response: clarify briefly and redisplay the menu.

## Success Metrics

- Exact files and sections are planned.
- User approved before any writes.
- Update mode avoids duplicate stale sections.
- Audit mode remains read-only.

## Failure Modes

- Writing before approval.
- Planning broad docs that are not supported by evidence.
- Creating new docs when a targeted update would be sufficient.
- Omitting affected existing docs from the plan.
