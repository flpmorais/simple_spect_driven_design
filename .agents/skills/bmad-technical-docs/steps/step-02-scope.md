# Step 2: Define Scope And Sources

**Progress: Step 2 of 7** - Next: Evidence Exploration

## Step Goal

Define the exact documentation scope, source evidence, and update boundaries before reading implementation details.

## Mandatory Execution Rules

- Read this complete step before taking action.
- Do not write documentation in this step.
- Ask one focused clarification question if scope is ambiguous.
- For update modes, protect unrelated docs and code from modification.
- Stop at the confirmation menu and wait for user input.

## Context Boundaries

- `workflowMode` was set in Step 1.
- Existing docs state from Step 1 is available.
- Source evidence may include source code, tests, config files, existing docs, architecture docs, ADRs, and explicit user input.

## Sequence Of Instructions

### 1. Define Scope By Mode

Use the active mode to define scope:

#### create-docs-set

Scope is the repository by default. Ask whether to document the full repo or a subsystem if the user did not already specify.

Default outputs are:

- `{technicalDocsIndex}`
- `{technicalDocsRoot}/code-map.md`
- `{technicalDocsRoot}/patterns.md`
- Additional topic docs only when the evidence shows distinct areas that deserve their own docs.

#### document-target

Ask for the target if not provided. Valid targets include folders, files, modules, features, APIs, services, commands, data flows, or named patterns.

The output should normally be one focused topic doc under `{technicalDocsRoot}` plus an index update.

#### update-docs

Ask for the existing doc path, source path, topic, or described change if not provided.

Map the requested change to existing docs before deciding to create new docs.

#### update-from-git-diff

Determine the diff scope:

- If the user provided a commit range or branch comparison, use that.
- Otherwise use the current working tree and staged changes.

Allowed commands are read-only git commands such as:

- `git diff --name-only`
- `git diff --cached --name-only`
- `git diff --stat`
- `git diff --cached --stat`
- `git diff <range> --name-only`
- `git diff <range> --stat`

Do not run destructive git commands.

#### audit-docs

Scope is existing technical docs plus the source files they reference by default.

If no technical docs exist, audit the repository for missing technical docs and recommend a docs set.

### 2. Establish Source Priority

Use this source priority for claims:

1. Current source code, tests, config, schemas, and scripts.
2. Existing technical docs that match current code.
3. Architecture docs, ADRs, planning artifacts, and explicit user input for rationale.
4. Inference only when explicitly labeled and validated against source evidence.

Never use planning artifacts to override current code behavior. Planning artifacts may explain intent or rationale, not current behavior unless code agrees.

### 3. Define Out Of Scope

State what will not be touched:

- Product requirements, UX specs, marketing copy, and tutorial content.
- Source code.
- Docs outside the selected scope.
- Reference files unless the user explicitly requested them.

### 4. Present Scope Confirmation

Display:

```text
Technical docs scope:
- Mode: {workflowMode}
- Target: {target or full repo}
- Output root: {technicalDocsRoot}
- Expected outputs: {list}
- Evidence sources: source code, tests, config, existing docs, architecture/ADR docs for rationale
- Out of scope: code changes, product/marketing/tutorial content, unrelated docs

Continue with this scope?

[C] Continue to evidence exploration
[R] Revise scope
[X] Exit without changes
```

### 5. Menu Handling Logic

- If `C`: read fully and follow `./step-03-explore.md`.
- If `R`: ask for the revised scope, update the scope summary, and redisplay the confirmation menu.
- If `X`: exit without changes.
- If any other response: clarify briefly and redisplay the menu.

## Success Metrics

- Mode, target, expected outputs, and evidence sources are known.
- User confirmed the scope before exploration.
- Update boundaries are explicit.
- No docs or code were modified.

## Failure Modes

- Reading broad source areas before scope confirmation.
- Letting planning artifacts define current behavior against code.
- Failing to protect unrelated docs from update mode.
- Proceeding without user confirmation.
