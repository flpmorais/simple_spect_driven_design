# Step 3: Discover Business Evidence

**Progress: Step 3 of 7** - Next: Documentation Plan

## Step Goal

Gather business evidence, identify domains, rules, workflows, decision tables, open questions, and discrepancies.

## Mandatory Execution Rules

- Read this complete step before taking action.
- Discover only within the confirmed scope.
- Do not write documentation in this step.
- Label each finding by source category and confidence.
- If code is inspected, classify it as observed implementation only.

## Sequence Of Instructions

### 1. Load Relevant Business Inputs

Load only relevant sources:

- Existing files under `{businessArtifactsRoot}` for selected domains.
- Legacy business docs such as `docs/business-rules.md` as input only.
- PRD, architecture, epics, or stories relevant to the domain.
- User-provided notes or decisions.
- Implementation evidence only when the mode requires observed behavior or discrepancy analysis.

### 2. Extract Domain Model Elements

For each domain, identify:

- Domain purpose
- In-scope business objects
- Out-of-scope adjacent areas
- Actors and responsibilities
- Core terms
- States and lifecycle events
- Business rules and invariants
- Conditional decisions
- Trigger-to-outcome mappings
- Open questions
- Possible discrepancies

### 3. Classify Each Finding

Classify every finding with:

- `findingType`: domain, actor, term, rule, workflow, decision-table, invariant, open-question, discrepancy.
- `sourceCategory`: approved-business, planned-intent, observed-implementation, legacy-input, user-input.
- `status`: approved, proposed, observed, planned, deprecated, disputed.
- `source`: file path, section, or user statement.
- `confidence`: high, medium, low.

### 4. Rule Extraction Standards

Each candidate rule must include:

- Statement
- Scope
- Actors
- Trigger
- Outcome
- Exceptions
- Examples
- Source
- Implementation evidence, if any
- Status

If any required field is unknown, record it as an open question rather than inventing it.

### 5. Discrepancy Detection

Create a discrepancy candidate when:

- Approved business docs and implementation behavior disagree.
- Planning artifacts describe behavior that implementation does not support.
- Legacy docs conflict with newer approved artifacts.
- Two approved-looking sources conflict.
- A workflow trigger is implied but not defined.

### 6. Present Discovery Summary

Summarize:

- Sources reviewed
- Candidate domains
- Candidate rules by status
- Workflows or decision tables found
- Open questions
- Discrepancy candidates

If blocked by missing business decisions, ask one focused question and wait.

If not blocked, read fully and follow `./step-04-doc-plan.md`.

## Success Metrics

- Findings are classified by source category and status.
- Business rules are not invented.
- Implementation evidence is treated as observed behavior.
- Open questions and discrepancies are explicit.

## Failure Modes

- Writing docs before plan approval.
- Promoting observed code behavior to approved business policy.
- Ignoring contradictions.
- Filling unknown rule fields with guesses.
