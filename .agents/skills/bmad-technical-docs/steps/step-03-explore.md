# Step 3: Explore Evidence

**Progress: Step 3 of 7** - Next: Documentation Plan

## Step Goal

Gather enough evidence to write or assess technical documentation accurately.

## Mandatory Execution Rules

- Read this complete step before taking action.
- Explore only the confirmed scope.
- Prefer targeted reads and searches over broad source loading.
- Record source evidence for every planned claim.
- Do not write documentation in this step.

## Context Boundaries

- Scope and mode were confirmed in Step 2.
- This step gathers evidence and produces an exploration summary in memory.
- This step may use subagents for large, independent exploration areas, but the final synthesis must remain evidence-backed.

## Sequence Of Instructions

### 1. Load Existing Docs Relevant To Scope

Read existing docs in this order when present:

- `{technicalDocsIndex}`
- Existing docs under `{technicalDocsRoot}` that mention the target, changed files, or referenced source files
- Existing `docs/**/*.md` relevant to the scope
- Architecture docs or ADRs relevant to rationale

Do not load unrelated docs just because they exist.

### 2. Discover Source Evidence

Use targeted file and content searches to find:

- Entry points
- Public interfaces and APIs
- Data models, schemas, migrations, or persistence boundaries
- Config and environment variables
- Tests that demonstrate behavior
- Shared utilities, conventions, and helper patterns
- Imports and dependents for target files
- Similar patterns elsewhere in the codebase

For git diff update mode, first list changed files, then map each changed source file to existing docs or a proposed new doc.

### 3. Extract Technical Facts

Build an evidence table in memory with these fields:

- Claim
- Source path
- Source type: code, test, config, existing-doc, architecture, ADR, user-input
- Confidence: verified, documented-intent, inferred
- Destination doc or audit finding

Rules:

- `verified` requires current code, tests, config, or schemas.
- `documented-intent` requires architecture docs, ADRs, planning artifacts, or explicit user input.
- `inferred` must be minimized and clearly labeled if used.

### 4. Identify Rationale Sources

For each meaningful `Why It Works This Way` claim, find one of:

- Architecture document section
- ADR or design decision
- Existing technical doc
- Code structure that clearly encodes a constraint
- Explicit user explanation

If none exists, use `Rationale not documented` in the eventual doc.

### 5. Detect Documentation Gaps

Identify gaps by mode:

- create-docs-set: major code areas with no docs, cross-cutting patterns, missing code map.
- document-target: target behavior, locations, patterns, rationale, and related code.
- update-docs: stale sections, missing changed behavior, sections safe to replace.
- update-from-git-diff: changed files with impacted docs, changed files with no docs, docs that no longer match changed code.
- audit-docs: missing docs, stale claims, broken paths, weak rationale, generic content.

### 6. Present Exploration Summary

Summarize findings concisely:

- Evidence reviewed
- Important implementation facts
- Existing docs affected
- Gaps or stale areas
- Any uncertainty that requires user input

If a blocker prevents accurate documentation, ask one focused question and wait.

If not blocked, read fully and follow `./step-04-doc-plan.md`.

## Success Metrics

- Relevant source evidence was gathered.
- Evidence distinguishes verified facts from documented intent.
- Existing docs affected by the work are known.
- Documentation gaps are identified.
- No docs were modified.

## Failure Modes

- Making claims without source evidence.
- Reading unrelated large areas instead of targeted sources.
- Using planning artifacts as proof of current behavior.
- Failing to identify stale docs before update mode.
