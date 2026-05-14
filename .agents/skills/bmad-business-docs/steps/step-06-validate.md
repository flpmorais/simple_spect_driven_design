# Step 6: Validate Business Docs

**Progress: Step 6 of 7** - Next: Complete Workflow

## Step Goal

Validate that business documentation is domain-oriented, sourced, status-correct, and free of hidden contradictions.

## Mandatory Execution Rules

- Read this complete step before taking action.
- Validate only files touched by the approved plan plus index and state file when relevant.
- Fix documentation defects created by this workflow.
- Do not modify source code.
- Do not broaden scope during validation.

## Sequence Of Instructions

### 1. Reload Touched Files

Read each created or updated business doc completely, including frontmatter.

For audit mode, read the audit report completely.

### 2. Validate Domain Structure

Check:

- Domains are business domains, not technical components.
- Domain docs live under `{domainsRoot}/<domain-slug>/`.
- Cross-domain content lives under `{crossDomainRoot}/`.
- Index links changed domain and cross-domain docs.

### 3. Validate Source And Status Boundaries

Check:

- Approved rules have approved-business or user-input sources.
- Proposed rules are marked `proposed`.
- Observed implementation behavior is marked `observed` or recorded as implementation evidence.
- Planned behavior is marked `planned` unless approved by the user.
- Conflicts are recorded as discrepancies.

### 4. Validate Rule Quality

For each rule, check:

- Rule ID uses the domain prefix.
- Required fields are present.
- Conditional logic has a decision table when useful.
- Lifecycle behavior has state/transition documentation when useful.
- Unknown decisions are open questions, not guessed answers.

### 5. Validate No Placeholders

Check that docs contain no unresolved placeholders, TODOs, empty generated sections, or generic content that could apply to any project.

### 6. Fix Or Report Issues

If validation finds defects in files this workflow wrote, fix them now.

If validation finds uncertainty that requires user input, record it in the final summary and do not invent a resolution.

### 7. Continue To Completion

When validation is complete, read fully and follow `./step-07-complete.md`.

## Success Metrics

- Business docs are sourced and status-correct.
- Domain boundaries are business-oriented.
- Discrepancies and open questions are visible.
- No placeholders or generic docs remain.

## Failure Modes

- Letting implementation behavior become approved policy.
- Hiding contradictions in prose.
- Leaving unknown fields as invented text.
- Editing unrelated files during validation.
