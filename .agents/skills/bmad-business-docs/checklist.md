# Business Docs Workflow - Validation Checklist

## Business Scope

- [ ] Documentation is business/domain focused, not technical implementation focused.
- [ ] Domains are split by business boundaries, not technical layers.
- [ ] Rules, workflows, policies, actors, and terminology are separated clearly.
- [ ] Cross-domain constraints are placed under `cross-domain/`.

## Source Quality

- [ ] Approved rules cite user decisions, PRD, accepted planning artifacts, or existing business docs.
- [ ] Proposed rules are marked `proposed` and not presented as approved.
- [ ] Observed implementation behavior is marked as implementation evidence, not business truth.
- [ ] Planned behavior is separated from current approved rules.
- [ ] Open questions are recorded instead of answered by speculation.

## Rule Quality

- [ ] Every rule has an ID with the domain prefix.
- [ ] Every rule has Statement, Scope, Actors, Trigger, Outcome, Exceptions, Examples, Source, Implementation Evidence, and Status.
- [ ] Conditional rules are represented in decision tables where useful.
- [ ] Lifecycle behavior is represented in workflow state/transition tables where useful.
- [ ] Contradictions are recorded as discrepancies.

## Maintenance Quality

- [ ] Targeted updates replace stale sections instead of appending duplicates.
- [ ] Unrelated user-authored content is preserved.
- [ ] `index.md` links all domain and cross-domain docs.
- [ ] `business-docs-state.json` is factual and small.
- [ ] No placeholders, TODOs, or empty generated sections remain.

## Audit Mode

- [ ] Audit findings distinguish missing docs, contradictions, observed behavior without approved rules, and open questions.
- [ ] Audit mode does not modify existing business docs.
- [ ] Recommendations are actionable and scoped.
