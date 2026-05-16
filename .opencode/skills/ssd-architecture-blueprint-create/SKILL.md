---
name: ssd-architecture-blueprint-create
description: Creates a SQLite-backed Architecture Blueprint through interactive architecture recommendation discovery, review, and memory storage.
---

# ssd-architecture-blueprint-create

Create Architecture Blueprint memory: a compact, source-backed set of architecture recommendations for Phase 1 planning.

Act as an architecture sparring partner, not a blind document writer. Ask focused questions, create useful tension, propose concrete recommendations, and capture only user-shaped recommendations.

Do not use BMad config/steps, hidden workflow variables, project artifact scanning, existing architecture docs, or markdown architecture blueprint files.

## Contract

Input:

```json
{
  "initial_context": "optional additional user context"
}
```

Rules:

- Read and apply `.opencode/shared/architecture-blueprint-contract.md` before proceeding.
- Return structured `precondition_failed` if Product Blueprint memory is missing.
- Return structured `skipped` if Architecture Blueprint memory already exists.
- Use Product Blueprint memory as the required source. Read Product Brief memory when available, but do not fail if Product Brief memory is unavailable after Product Blueprint exists.
- Keep the flow token-lean: ask at most 3 questions at a time, avoid full-document restatements during discovery, and avoid repeated rationale.
- Do not ask a giant up-front questionnaire. Walk decision clusters progressively.
- For each cluster, propose concrete recommendations, alternatives, and tensions. The user must confirm, correct, reject, choose another alternative, or mark unknown before that recommendation is captured.
- Write Architecture Blueprint memory exactly once, after all required decision areas are covered, internal review passes, and the user approves the final four sections.
- Do not create Architecture Blueprint markdown files or temp markdown drafts.
- Return `blocked` only for tool or memory-command failure after start, or when approval cannot be obtained.

## Memory

- Product Blueprint memory adapter: `.opencode/scripts/ssd_product_blueprint/memory.py`
- Product Brief memory adapter: `.opencode/scripts/ssd_product_brief/memory.py`
- Shared contract: `.opencode/shared/architecture-blueprint-contract.md`
- Artifact recipe index: `.opencode/shared/recipes.md`
- Architecture Blueprint memory adapter: `.opencode/scripts/ssd_architecture_blueprint/memory.py`
- Architecture Blueprint artifact kind: `architecture-blueprint`
- Architecture Blueprint artifact ID: UUID returned by memory command

## Artifact Boundary

Include concrete architecture recommendations, confidence labels, source/user-backed rationale, ideal approaches, acceptable compromises, rejected alternatives, important dependencies, open risks, and Phase 1 validation needs.

Exclude generic principles, broad concern inventories, detailed design, data models, API specifications, deployment manifests, implementation tasks, release plans, work packages, and unsupported technology choices.

## Required Sections

Use these exact section keys in this order:

- `architecture-recommendations`
- `decision-coverage`
- `open-risks`
- `phase-1-validation`

## Required Decision Areas

Cover every area below. Expand relevant areas in `architecture-recommendations`; summarize every area in `decision-coverage` as `Recommended`, `Not needed`, or `Unknown`.

- Product surface
- Deployment model
- Data store
- Authentication
- Authorization
- User/account management
- Multi-tenancy
- Observability
- Background work
- AI/search
- Integrations
- File/media handling
- Security/compliance
- Payments/billing
- DevOps/release

## Recommendation Format

Use this compact structure:

```md
### <Decision Area>

- Recommendation: <specific architecture choice>
- Confidence: Strong recommendation | Likely right | Weak recommendation | Unknown
- Why: <source/user-backed rationale>
- Ideal approach: <best-fit long-term pattern/technology>
- Acceptable compromise: <v1-safe simplification>
- Rejected alternatives: <alternatives and why they lost>
- Dependencies: <only if this affects another decision>
- Phase 1 validation: <what must be verified>
```

## Workflow

### 1. Preflight

Read and apply `.opencode/shared/architecture-blueprint-contract.md`.

Read Product Blueprint memory:

```text
python .opencode/scripts/ssd_product_blueprint/memory.py get
```

If missing, return only:

```json
{
  "status": "precondition_failed",
  "reason": "Product Blueprint memory is required before creating an Architecture Blueprint.",
  "expected": "Product Blueprint artifact with kind `product-blueprint` and current sections",
  "required_action": "Run ssd-product-blueprint-create first."
}
```

Check for existing Architecture Blueprint memory:

```text
python .opencode/scripts/ssd_architecture_blueprint/memory.py get
```

If it exists, return only:

```json
{
  "status": "skipped",
  "reason": "Architecture Blueprint already exists.",
  "artifact_kind": "architecture-blueprint",
  "artifact_id": "<uuid>"
}
```

If the command reports that Architecture Blueprint does not exist, continue.

Attempt to read Product Brief memory for grounding:

```text
python .opencode/scripts/ssd_product_brief/memory.py get
```

If unavailable, continue with Product Blueprint memory and note the warning in the final return.

### 2. Frame

State that this creates an Architecture Blueprint made of concrete architecture recommendations for Phase 1 planning. It is not detailed design, implementation planning, or a release plan.

State that collaboration will be interactive and token-lean: the skill will walk decision clusters, propose recommendations and alternatives, ask focused questions, and capture only user-shaped recommendations.

### 3. Interactive Recommendation Discovery

Walk these clusters in order:

1. Surface and deployment: Product surface, Deployment model.
2. Data and intelligence: Data store, File/media handling, AI/search.
3. Identity and access: Authentication, Authorization, User/account management, Multi-tenancy.
4. Operations: Observability, Background work, DevOps/release.
5. External constraints: Integrations, Security/compliance, Payments/billing.

For each cluster:

1. Extract only the source-backed pressures relevant to the cluster.
2. Present the real tension in 2-4 bullets.
3. Propose concrete recommendations for relevant decision areas.
4. Mark irrelevant areas as likely `Not needed` with one-line rationale.
5. Ask at most 3 focused questions for the user to confirm, correct, reject, choose another alternative, or mark unknown.
6. Capture only accepted or user-shaped recommendations in working context.

Use concise prompts like:

```text
For deployment, I see two viable paths: managed/serverless for speed and low ops, or VPS for control and predictable infrastructure. I recommend managed/serverless unless you expect long-running local processes or strict infrastructure control.

Confirm managed/serverless, choose VPS, or tell me what context changes this.
```

### 4. Draft Four Sections

After all required decision areas are covered, draft the four required sections.

`architecture-recommendations` contains the compact recommendation blocks for every relevant or unknown decision area.

`decision-coverage` is a compact table:

```md
| Area | Status | Recommendation Summary | Rationale |
| --- | --- | --- | --- |
| Authentication | Recommended | Google-only auth | Internal employees use Google accounts |
| Payments/billing | Not needed | None | No monetization flow is in scope |
```

`open-risks` contains only risks that could overturn recommendations.

`phase-1-validation` contains only validation needed before downstream planning depends on the recommendations. It must not become an implementation plan.

### 5. Internal Review

Review the payload inside this skill. Do not call Architecture Blueprint review subagents.

Do not write while it has:

- missing required decision coverage;
- a `Recommended` area without a specific recommendation;
- a relevant decision area hidden in `open-risks` instead of recommended or marked unknown;
- confidence labels outside `Strong recommendation`, `Likely right`, `Weak recommendation`, or `Unknown`;
- generic principles or concern inventories;
- unsupported specificity;
- recommendations presented as facts when they are assumptions;
- repeated rationale across sections;
- open risks that are not capable of overturning recommendations;
- Phase 1 validation that becomes an implementation plan;
- unresolved contradiction with Product Blueprint, Product Brief, user input, or approved synthesis.

If review finds conflicts, revisit only affected decision areas, ask focused questions, revise, and rerun review.

### 6. Final User Write Gate

Present the four proposed sections in human-readable Markdown. Also show source Product Blueprint, source Product Brief if available, assumptions to store, unknowns, and open risks.

Use this prompt:

```text
Review these Architecture Blueprint sections. Reply with approval to create it, or tell me what to change by section or decision area.
```

Do not call `.opencode/scripts/ssd_architecture_blueprint/memory.py create` until the user explicitly approves the final write after seeing the sections. Approval must be affirmative (`approved`, `create it`, `looks good`, or equivalent). If the user requests changes, revise affected sections, rerun internal review, and repeat this gate.

### 7. Finalize Once

After explicit final approval, re-check Architecture Blueprint memory. If it exists, return `skipped`. Otherwise pass the approved payload on stdin:

```text
python .opencode/scripts/ssd_architecture_blueprint/memory.py create
```

Payload shape:

```json
{
  "change_summary": "Initial Architecture Blueprint",
  "product_blueprint_artifact_id": "<uuid>",
  "product_brief_artifact_id": "<uuid or omitted>",
  "sections": {
    "architecture-recommendations": "...",
    "decision-coverage": "...",
    "open-risks": "...",
    "phase-1-validation": "..."
  },
  "source_brainstorms": [],
  "cited_idea_ids": []
}
```

### 8. Return

On success only:

```json
{
  "status": "complete",
  "artifact_kind": "architecture-blueprint",
  "artifact_id": "<uuid>",
  "product_blueprint_artifact_id": "<uuid>",
  "product_brief_artifact_id": "<uuid or null>",
  "sections_approved": [
    "architecture-recommendations",
    "decision-coverage",
    "open-risks",
    "phase-1-validation"
  ],
  "source_brainstorms": [],
  "cited_idea_ids": [],
  "warnings": []
}
```

On runtime failure only:

```json
{
  "status": "blocked",
  "reason": "specific failure",
  "failed_step": "step name",
  "partial_outputs": {
    "sections_approved": [],
    "recommendations_started": true
  },
  "required_action": "Resolve the failed tool run and retry the skill.",
  "warnings": []
}
```

## Hard Stops

- Do not read or use Product Blueprint markdown; use Product Blueprint memory only.
- Do not call BMad skills.
- Do not create, overwrite, edit, read, or depend on architecture markdown artifacts.
- Do not create temp Architecture Blueprint markdown.
- Do not ask a giant up-front questionnaire.
- Do not generate recommendations without user interaction.
- Do not use percentage confidence.
- Do not skip required decision coverage.
- Do not skip final review.
- Do not write Architecture Blueprint memory before final write approval.
- Do not output only JSON or a tool result as the user-facing review or final response.
