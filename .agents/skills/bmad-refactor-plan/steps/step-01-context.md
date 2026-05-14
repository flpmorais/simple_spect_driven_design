# Step 1: Context Clarification

## Rules

- Speak in `{communication_language}`.
- Do not inspect implementation files yet unless needed to understand a user-provided path or bundle name.
- Do not create the refactor bundle until the refactor name and initial intent are clear enough to name the directory.
- Do not proceed to exploration until the user confirms the context summary.
- If an existing refactor bundle should be continued, load `./step-01b-continue.md` instead of starting fresh.

## Continuation Detection

1. List files matching `{implementation_artifacts}/refactors/*/refactor.md` without reading contents.
2. If one or more exist, identify the most recent by timestamp in the parent directory name.
3. Ask the user:

```text
Found existing refactor planning bundle: <directory>.

[1] Continue this refactor bundle
[2] Start a new refactor bundle
[3] Choose from all refactor bundles
```

HALT and wait for the user's selection.

- If user selects `[1]`, set `{refactor_dir}` to the latest parent directory, set `{refactor_file}` to `{refactor_dir}/refactor.md`, and load `./step-01b-continue.md`.
- If user selects `[2]`, continue with Fresh Context Gathering.
- If user selects `[3]`, list all matching bundle directories and ask which to continue or whether to start new. HALT for selection.

If the user explicitly asked to start a new refactor plan, skip continuation detection.

## Fresh Context Gathering

Ask the user to explain what needs to change and why. Gather enough information to satisfy this clarity checklist:

- Objective: what should be different after the refactor.
- Motivation: why this refactor is worth doing now.
- Scope: modules, flows, files, packages, or behavior likely involved.
- Non-goals: what must not be changed.
- Constraints: compatibility, performance, deployment, data, UI, security, timeline, or team constraints.
- Desired behavior: externally visible behavior that must remain or change.
- Project context boundaries: technical rules, workflow rules, anti-patterns, or story constraints that must be respected.
- Risks: known fragile areas, previous failures, or expected hard parts.
- Success criteria: how the user will know the refactor is complete.

Ask concise follow-up questions until each checklist item is clear. Do not ask about items already answered.

## Refactor Name

Derive a short `refactor_name` slug from the confirmed objective. If ambiguous, ask the user for a short name.

Apply slug rules from `workflow.md`.

## Artifact Creation

Once initial intent and `refactor_name` are clear:

1. Create `{implementation_artifacts}/refactors` if needed.
2. Create `{refactor_dir}` using the required directory format.
3. Create `{refactor_file}` as `{refactor_dir}/refactor.md` from `template.md`.
4. Create `{refactor_dir}/tasks/`.
5. Set frontmatter:
   - `workflow: bmad-refactor-plan`
   - `status: in-progress`
   - `phase: context`
   - `phasesCompleted: []`
   - `refactorName: <refactor_name>`
   - `createdAt: <YYYY-MM-DD-HHMM>`
   - `lastUpdated: <YYYY-MM-DD-HHMM>`
   - `executionStatus: not-started`
   - `executionStartedAt: ''`
   - `executionCompletedAt: ''`
   - `executionLastUpdated: ''`
   - `executionBranch: ''`
   - `sourceBranch: <current git branch if available>`
   - `bundlePath: <refactor_dir>`
   - `tasksDir: tasks`

## Context Summary And Confirmation

Write a proposed `## Context` section in `{refactor_file}` containing:

```markdown
## Context

### Objective

### Motivation

### Scope

### Non-Goals

### Constraints

### Desired Behavior

### Project Context Boundaries

### Known Risks

### Success Criteria
```

Present the summary to the user and ask:

```text
Does this context accurately capture the refactor? Reply with:
[1] Confirm and continue to exploration
[2] Revise context
```

HALT and wait for the user's selection.

- If `[1]`, write the confirmed `## Context` section in `{refactor_file}`, update `{refactor_file}` frontmatter `phase: exploration`, `phasesCompleted: [context]`, `lastUpdated`, update the index summary if useful, then load `./step-02-exploration.md`.
- If `[2]`, ask what to revise, update the summary, and ask for confirmation again.

## Success Criteria

- Existing refactor bundles were detected before starting a duplicate.
- Context is explicit and confirmed by the user.
- Bundle directory follows `<refactorName>-<YYYY-MM-DD-HHMM>` under `{implementation_artifacts}/refactors/`.
- Frontmatter is initialized correctly.
- Only files inside the refactor bundle were created or modified.
