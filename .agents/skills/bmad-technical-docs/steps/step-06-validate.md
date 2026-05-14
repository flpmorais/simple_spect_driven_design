# Step 6: Validate Technical Docs

**Progress: Step 6 of 7** - Next: Complete Workflow

## Step Goal

Validate that created, updated, or audited documentation is accurate, scoped, linked, and evidence-backed.

## Mandatory Execution Rules

- Read this complete step before taking action.
- Validate only files touched by the approved plan plus `{technicalDocsIndex}` and `{stateFile}` when relevant.
- Fix documentation defects created by this workflow.
- Do not alter source code.
- Do not broaden scope during validation.

## Context Boundaries

- Files were written or an audit report was produced in Step 5.
- The validation checklist is available at `../checklist.md`.

## Sequence Of Instructions

### 1. Reload Touched Files

Read each created or updated file completely, including frontmatter.

For audit mode, read the audit report completely.

### 2. Validate Structure

Check:

- Required sections are present.
- Frontmatter is valid and includes required fields.
- `sourceFiles` and `rationaleSources` contain relevant paths where applicable.
- `verifiedAt`, `verifiedCommit`, and `lastUpdatedBy` are updated for maintained docs.
- No placeholders, TODOs, or empty generated sections remain.

### 3. Validate Evidence

For every substantial claim, confirm it is supported by:

- Source code, tests, config, schemas, scripts, or migrations for current behavior.
- Architecture docs, ADRs, existing docs, or explicit user input for rationale.

If a rationale claim lacks evidence, replace it with `Rationale not documented`.

If a behavior claim lacks evidence, remove it or mark it as inferred only when useful and explicitly labeled.

### 4. Validate Links And Paths

Check:

- Relative links between technical docs resolve.
- Referenced source paths exist.
- Renamed or moved paths are not presented as current unless explicitly marked historical.
- The index links all maintained technical docs under the approved scope.

### 5. Validate Mode-Specific Requirements

#### create-docs-set

- The docs set is minimal and useful.
- Major documented areas have source evidence.

#### document-target

- The doc is focused on the target and does not become a broad repository scan.

#### update-docs

- Stale sections were replaced, not duplicated.
- Unrelated sections are preserved.

#### update-from-git-diff

- Changed files are mapped to docs or explicitly marked no-doc-update-needed.
- Diff scope is recorded in change notes or audit report.

#### audit-docs

- Report findings are actionable and evidence-backed.
- Existing docs were not modified.

### 6. Fix Or Report Issues

If validation finds defects in files this workflow wrote, fix them now.

If validation finds uncertainty that requires user input, record it in the final summary and do not invent a resolution.

### 7. Continue To Completion

When validation is complete, read fully and follow `./step-07-complete.md`.

## Success Metrics

- Documentation structure is valid.
- Claims are evidence-backed.
- Links and paths resolve.
- No stale duplicate sections were introduced.
- Any remaining uncertainties are explicit.

## Failure Modes

- Skipping validation because files were just written.
- Leaving unsourced rationale.
- Leaving generic or placeholder content.
- Modifying unrelated files during validation.
