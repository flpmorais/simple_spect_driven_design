# Step 3: Analysis And Decisions

## Rules

- Speak in `{communication_language}`.
- Read `{refactor_file}` completely before analysis.
- Do not edit source code or any file outside `{refactor_dir}`.
- Do not proceed to final plan while unresolved `decision_needed` issues remain unless the user explicitly marks the plan as blocked or defers those decisions.

## Analyze Findings

Synthesize `## Context` and `## Exploration` from `{refactor_file}` into a clear explanation of:

- What needs to change.
- Where it likely needs to change.
- What must not change.
- Which existing behavior must be preserved.
- Which tests/validations matter.
- Which project context rules constrain the plan.

## Classify Flagged Issues

Classify every flagged issue into exactly one bucket:

- `decision_needed`: user choice required before planning can be correct.
- `risk`: material risk that can be mitigated in the plan.
- `constraint`: binding project context, compatibility, or operational constraint.
- `defer`: real issue that is outside this refactor and should not block the plan.
- `out_of_scope`: not relevant to this refactor.

Project context conflicts must become `decision_needed` unless the only safe action is to stop as blocked.

## User Decisions

If any `decision_needed` issues exist:

1. Present each issue with context, evidence, and concrete options.
2. Ask the user to choose.
3. Record the selected decision in `{refactor_file}` frontmatter `decisions` and in `## Analysis`.
4. If the user cannot decide, ask whether to mark it as blocked or deferred.

HALT for user decisions. Do not continue until decisions are resolved, blocked, or deferred.

## Write Analysis Section

Replace the `## Analysis` section in `{refactor_file}` with:

```markdown
## Analysis

### Required Changes

### Likely Files And Areas

### Behavior To Preserve

### Project Context Constraints

### Flagged Issues

#### Decision Needed

#### Risks

#### Constraints

#### Deferred

#### Out Of Scope

### User Decisions
```

Update frontmatter:

- `phase: plan` if no unresolved blockers remain.
- `phase: blocked` and `status: blocked` if unresolved blockers remain.
- append `analysis` to `phasesCompleted` once the analysis section is written.
- update `decisions` and `blockedIssues`.
- update `lastUpdated`.

If blocked, STOP and report the blockers. If not blocked, load `./step-04-plan.md`.

## Success Criteria

- User sees and resolves all ambiguous issues.
- Analysis explains change locations and constraints clearly.
- Blocked plans are honestly marked blocked.
- Only files inside `{refactor_dir}` are modified.
