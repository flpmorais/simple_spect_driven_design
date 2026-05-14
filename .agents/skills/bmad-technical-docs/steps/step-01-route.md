# Step 1: Route The Documentation Work

**Progress: Step 1 of 7** - Next: Scope Definition

## Step Goal

Determine whether this run is creating, updating, auditing, or targeting technical documentation, then route to scope definition.

## Mandatory Execution Rules

- Read this complete step before taking action.
- Do not inspect source code yet except to check whether technical docs already exist.
- Do not create or edit documentation in this step.
- If a menu is presented, stop and wait for user input.
- Keep the workflow strictly technical.

## Context Boundaries

- Available variables: `technicalDocsRoot`, `technicalDocsIndex`, `stateFile`, `{project_knowledge}`, `{planning_artifacts}`, `{output_folder}`.
- This step may inspect whether `technicalDocsRoot` and `technicalDocsIndex` exist.
- This step may inspect the user's initial request for routing signals.

## Sequence Of Instructions

### 1. Check Existing Technical Docs State

Check whether these paths exist:

- `{technicalDocsRoot}`
- `{technicalDocsIndex}`
- `{stateFile}`

If `{stateFile}` exists, read it and summarize only high-level state:

- Last workflow mode
- Last updated timestamp
- Known technical docs
- Last verified commit if present

### 2. Detect Requested Mode

Infer mode from the user's request if clear:

- `create-docs-set`: user asks to create technical docs for the repo or establish maintained technical documentation.
- `document-target`: user asks to document a specific folder, module, feature, service, API, command, or flow.
- `update-docs`: user asks to update existing docs for an explicit path, topic, or described change.
- `update-from-git-diff`: user asks to update docs from current changes, a branch, a commit range, or git diff.
- `audit-docs`: user asks to check whether docs are stale, missing, or inaccurate.

If mode is clear, state the detected mode and continue to Step 2.

If mode is not clear, present the menu in section 3.

### 3. Present Mode Menu If Needed

Display:

```text
Technical Docs Workflow

Existing docs state:
- Technical docs folder: {exists|missing}
- Technical docs index: {exists|missing}
- Workflow state: {exists|missing}

Choose the work type:

[C] Create docs set - Establish docs/technical for this repo or subsystem
[D] Document target - Document a specific folder, module, feature, API, command, or flow
[U] Update docs - Update docs for an explicit path, topic, or described change
[G] Update from git diff - Map changed files to docs and update affected docs
[A] Audit docs - Report missing, stale, or inaccurate technical docs without editing
[X] Exit - Stop without changes
```

### 4. Menu Handling Logic

- If `C`: set `workflowMode = create-docs-set`, then read fully and follow `./step-02-scope.md`.
- If `D`: set `workflowMode = document-target`, then read fully and follow `./step-02-scope.md`.
- If `U`: set `workflowMode = update-docs`, then read fully and follow `./step-02-scope.md`.
- If `G`: set `workflowMode = update-from-git-diff`, then read fully and follow `./step-02-scope.md`.
- If `A`: set `workflowMode = audit-docs`, then read fully and follow `./step-02-scope.md`.
- If `X`: exit without changes.
- If any other response: clarify briefly and redisplay the menu.

## Success Metrics

- Existing technical docs state was checked.
- The workflow mode is known.
- No documentation was created or edited.
- The next step is loaded only after mode is known.

## Failure Modes

- Creating or editing docs in this step.
- Scanning source files before scope is defined.
- Proceeding without a clear workflow mode.
- Treating non-technical content as in scope.
