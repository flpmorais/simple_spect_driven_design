# Technical Docs Workflow - Validation Checklist

## Technical Scope

- [ ] Content is strictly technical.
- [ ] No product, marketing, onboarding, tutorial, or speculative planning prose was added.
- [ ] Current behavior is not mixed with planned behavior.
- [ ] Rationale is sourced or marked `Rationale not documented`.

## Evidence Quality

- [ ] Every substantial behavior claim is supported by source files, tests, config, architecture docs, ADRs, or explicit user input.
- [ ] All file paths referenced in docs exist or are clearly marked as historical/planned with a source.
- [ ] Source files are recorded in frontmatter `sourceFiles`.
- [ ] Rationale sources are recorded in frontmatter `rationaleSources` when used.
- [ ] Inferences are either removed or explicitly labeled as inferred.

## Maintenance Quality

- [ ] Update mode replaced targeted stale sections instead of appending duplicates.
- [ ] Unrelated user-authored content was preserved.
- [ ] The technical docs index links all created or updated docs.
- [ ] Changed docs have updated `verifiedAt`, `verifiedCommit`, and `lastUpdatedBy` frontmatter.

## Structure

- [ ] Topic docs include `What This Is`, `Where It Lives`, `How It Works`, `Patterns And Conventions`, `Why It Works This Way`, `Related Code`, and `Change Notes`.
- [ ] `docs/technical/index.md` exists after create mode or after the first generated topic doc.
- [ ] Links use relative paths and are not broken.
- [ ] Markdown has no placeholders, empty generated sections, or TODOs.

## Audit Mode

- [ ] Audit findings include severity and source evidence.
- [ ] Missing documentation is separated from stale documentation.
- [ ] Recommended updates are actionable and scoped.
- [ ] No docs were modified unless the user selected an update/write option.

## Git Diff Update Mode

- [ ] Diff range or working tree scope was stated.
- [ ] Changed source files were mapped to existing docs before edits.
- [ ] New docs were created only when no suitable existing doc covered the changed area.
- [ ] Code changes outside the selected scope were not documented.
