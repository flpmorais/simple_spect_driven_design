# Step 5: Write Or Report

**Progress: Step 5 of 7** - Next: Validate Output

## Step Goal

Create or update technical documentation according to the approved plan, or write an audit report in audit mode.

## Mandatory Execution Rules

- Read this complete step before taking action.
- Follow the approved plan exactly.
- Do not modify source code.
- Do not modify docs outside the approved plan.
- Preserve unrelated user-authored content.
- Update frontmatter for every created or updated technical doc.

## Context Boundaries

- The documentation plan from Step 4 is locked.
- Evidence from Step 3 is available.
- This is the first step that may write files.

## Sequence Of Instructions

### 1. Ensure Output Root Exists

Ensure `{technicalDocsRoot}` exists before writing any docs.

If creating directories is required, do only the minimum directories needed for the approved outputs.

### 2. Resolve Verification Metadata

Capture:

- Current date/time for `verifiedAt` or `generatedAt`.
- Current git commit with `git rev-parse --short HEAD` if available.
- For git diff mode, the diff range or working-tree/staged scope.

If git metadata is unavailable, use `unknown` for `verifiedCommit`.

### 3. Write Based On Mode

#### create-docs-set

Create or update the approved docs using:

- `../templates/index-template.md` for `{technicalDocsIndex}`.
- `../templates/topic-template.md` for topic docs, including `code-map.md` and `patterns.md`.

#### document-target

Create the focused topic doc using `../templates/topic-template.md`, then update `{technicalDocsIndex}`.

#### update-docs

For each approved existing doc:

- Read the complete file.
- Replace only the approved sections.
- Preserve unapproved sections exactly unless frontmatter metadata must be updated.
- Update `sourceFiles`, `rationaleSources`, `verifiedAt`, `verifiedCommit`, and `lastUpdatedBy`.

Create a new doc only if the approved plan says to do so.

#### update-from-git-diff

For each changed source file mapping:

- Update the mapped doc sections that describe changed behavior, location, patterns, or rationale.
- Add change notes that mention the diff scope, not implementation history speculation.
- Update `{technicalDocsIndex}` if docs were created or renamed.

#### audit-docs

Write the audit report using `../templates/audit-report-template.md`.

Do not modify existing technical docs in audit mode.

### 4. Topic Doc Content Requirements

Every topic doc must include:

- `What This Is`: concise technical purpose.
- `Where It Lives`: concrete paths and ownership boundaries.
- `How It Works`: behavior and flow verified from code, tests, config, or schemas.
- `Patterns And Conventions`: actual observed conventions, not generic best practices.
- `Why It Works This Way`: sourced rationale or `Rationale not documented`.
- `Related Code`: paths and why each matters.
- `Change Notes`: what changed in this documentation update.

### 5. Index Requirements

`{technicalDocsIndex}` must include:

- Links to all maintained technical docs under `{technicalDocsRoot}`.
- A short, content-based description of each doc.
- A code map summary if code-map documentation exists.
- A patterns summary if patterns documentation exists.
- Maintenance notes that preserve strict evidence-backed documentation rules.

### 6. State File

Create or update `{stateFile}` as compact JSON with:

- `lastUpdated`
- `lastMode`
- `lastTarget`
- `lastVerifiedCommit`
- `docsRoot`
- `knownDocs`
- `lastSourcesReviewed`

Keep the state file factual and small. Do not store large evidence dumps.

### 7. Continue To Validation

After all approved writes are complete, read fully and follow `./step-06-validate.md`.

## Success Metrics

- Only approved files were written.
- Docs are evidence-backed and strictly technical.
- Existing unrelated content was preserved.
- Frontmatter and state file were updated.
- Index reflects created or updated docs.

## Failure Modes

- Modifying source code.
- Editing docs outside the approved plan.
- Appending duplicate sections instead of replacing stale ones.
- Adding unsourced rationale.
- Leaving placeholders or generic content.
