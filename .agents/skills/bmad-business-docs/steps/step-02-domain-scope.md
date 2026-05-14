# Step 2: Define Domain Scope

**Progress: Step 2 of 7** - Next: Evidence Discovery

## Step Goal

Define the business domain scope, candidate domain split, source materials, and output boundaries before detailed discovery.

## Mandatory Execution Rules

- Read this complete step before taking action.
- Do not write documentation in this step.
- Ask one focused clarification question if the domain boundary is ambiguous.
- Stop at the confirmation menu and wait for user input.

## Sequence Of Instructions

### 1. Define Scope By Mode

#### create-domain-map

Default scope is the product's business model and SDLC automation process. Identify candidate domains from known artifacts and user input.

Likely initial domains for this project may include:

- `work-intake`
- `kanban-lifecycle`
- `workflow-dispatch`
- `agent-execution`
- `artifact-lifecycle`
- `review-and-approval`
- `governance`

These are candidates only. Confirm with the user before writing them.

#### capture-rules

Ask which domain the rules belong to if not provided. If the user provides a mixed set of rules, split them by business domain and confirm the split.

#### update-domain

Ask for the domain slug or business area if not provided. Map the request to an existing domain folder if one exists.

#### extract-observed-behavior

Ask what source area to inspect if not provided. Observed behavior must become candidate rules, open questions, or discrepancies; it must not become approved rules without user approval.

#### audit-business-docs

Default scope is all existing business artifacts. If none exist, audit legacy business docs, PRD, architecture, and current implementation for missing business docs.

#### resolve-discrepancies

Default scope is active discrepancies plus related approved rules and implementation evidence. If none exist, discover likely discrepancies in the selected domain.

### 2. Source Priority

Use these source categories:

- `approved-business`: explicit user decisions, approved business docs, accepted PRD/business artifacts.
- `planned-intent`: PRD, architecture, epics, stories, or planning artifacts not yet approved as business rules.
- `observed-implementation`: current source code, tests, config, webhooks, schemas, API contracts.
- `legacy-input`: old docs such as `docs/business-rules.md` used as input only.

### 3. Status Semantics

Use these statuses for rules:

- `approved`: accepted business rule.
- `proposed`: plausible rule pending user approval.
- `observed`: behavior exists in implementation but is not approved business policy.
- `planned`: appears in planning artifacts but is not implemented or approved as current rule.
- `deprecated`: no longer valid.
- `disputed`: conflicts with another source or user decision.

### 4. Present Scope Confirmation

Display:

```text
Business docs scope:
- Mode: {workflowMode}
- Business domain(s): {domains or candidate domains}
- Output root: {businessArtifactsRoot}
- Expected outputs: {list}
- Source categories: approved-business, planned-intent, observed-implementation, legacy-input
- Out of scope: technical implementation docs, source code changes, unrelated domains

Continue with this scope?

[C] Continue to evidence discovery
[R] Revise scope
[X] Exit without changes
```

### 5. Menu Handling Logic

- If `C`: read fully and follow `./step-03-discover.md`.
- If `R`: ask for revised scope, update the summary, and redisplay the confirmation menu.
- If `X`: exit without changes.
- If any other response: clarify briefly and redisplay the menu.

## Success Metrics

- Mode, domains, expected outputs, and source categories are known.
- Domain split is business-oriented.
- User confirmed the scope before discovery.

## Failure Modes

- Splitting domains by technical components.
- Treating legacy docs or code as approved business truth.
- Proceeding without scope confirmation.
