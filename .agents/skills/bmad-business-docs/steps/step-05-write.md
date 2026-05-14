# Step 5: Write Business Docs Or Report

**Progress: Step 5 of 7** - Next: Validate Output

## Step Goal

Create or update business documentation according to the approved plan, or write an audit report in audit mode.

## Mandatory Execution Rules

- Read this complete step before taking action.
- Follow the approved plan exactly.
- Do not modify source code.
- Do not modify files outside the approved plan.
- Preserve unrelated user-authored content.
- Update frontmatter for created or updated business docs.

## Sequence Of Instructions

### 1. Ensure Output Directories Exist

Create only the approved required directories:

- `{businessArtifactsRoot}`
- `{domainsRoot}`
- `{crossDomainRoot}`
- Selected domain directories

### 2. Resolve Metadata

Capture:

- Current date/time for `verifiedAt` or `generatedAt`.
- Source categories reviewed.
- Rule statuses and domain prefixes.

### 3. Write Based On Mode

#### create-domain-map

Create or update:

- `{businessDocsIndex}` using `../templates/index-template.md`.
- `glossary.md` and `actors.md` if terms or actors were discovered.
- Approved domain overview docs.

#### capture-rules

Create or update selected domain `rules.md`, plus related workflows, decision tables, and open questions when required.

#### update-domain

Replace only the approved sections in the selected domain docs. Preserve unrelated sections and existing rule IDs.

#### extract-observed-behavior

Write observed behavior as one of:

- `observed` rule entries pending approval.
- Open questions.
- Discrepancies when observed behavior conflicts with approved intent.

Do not mark observed behavior as `approved`.

#### audit-business-docs

Write an audit report under `{businessArtifactsRoot}/audit-business-docs-{{date}}.md` using `../templates/audit-report-template.md`.

Do not modify existing business docs in audit mode.

#### resolve-discrepancies

Update `{crossDomainRoot}/discrepancies.md` using `../templates/discrepancies-template.md` if needed. Record each discrepancy with:

- ID
- Domain
- Conflict summary
- Approved-business source
- Observed/planned/legacy conflicting source
- Decision needed
- Status

### 4. Required Rule Entry Format

Every rule must follow `../templates/rule-entry-template.md` and include:

- Statement
- Scope
- Actors
- Trigger
- Outcome
- Exceptions
- Examples
- Source
- Implementation Evidence
- Status

Use `None documented` when an exception or implementation evidence is not known. Use open questions for unknown mandatory business meaning.

### 5. Index And State File

Update `{businessDocsIndex}` when domains or cross-domain docs are created or changed.

Create or update `{businessStateFile}` as compact JSON with:

- `lastUpdated`
- `lastMode`
- `lastDomains`
- `businessArtifactsRoot`
- `knownDomains`
- `knownRulePrefixes`
- `openQuestionCount`
- `activeDiscrepancyCount`

Keep the state file factual and small. Do not store large evidence dumps.

### 6. Continue To Validation

After all approved writes are complete, read fully and follow `./step-06-validate.md`.

## Success Metrics

- Only approved files were written.
- Rule statuses preserve business truth boundaries.
- Open questions and discrepancies are recorded explicitly.
- Domain docs are organized by business domain.

## Failure Modes

- Modifying source code.
- Marking observed behavior as approved.
- Creating empty docs.
- Appending duplicate stale sections.
