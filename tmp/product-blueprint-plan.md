# Architecture Blueprint Skill Plan

Build a new OpenCode-native skill: `ssd-architecture-blueprint-create`.

The Architecture Blueprint is not "the architecture." It is a pre-analysis artifact that captures architectural intent before release planning.

It answers:

```text
Given the product dream, what architectural shape seems necessary or desirable?
```

It works differently from Product Blueprint. Product Blueprint uses ideation to define the dream. Architecture Blueprint uses guided architectural decision coverage to map that dream into architectural intent.

## Artifacts To Add

Create:

- `.opencode/skills/ssd-architecture-blueprint-create/SKILL.md`
- `.opencode/skills/ssd-architecture-blueprint-create/templates/architecture-blueprint-template.md`
- `.opencode/agents/ssd_architecture_blueprint_coverage.md`
- `docs/skills/ssd-architecture-blueprint-create.md`
- `docs/agents/ssd_architecture_blueprint_coverage.md`

Update:

- `docs/index.md`

## Source Inputs

Required distillates:

- Product Brief distillate: `._ssd_docs_distil/_docs/1_product_brief.md`
- Product Blueprint distillate: `._ssd_docs_distil/_docs/2_product_blueprint.md`

Optional input:

- `initial_context`: additional user context or preferences.

Do not read original source docs such as `ssd_docs/1_product_brief.md` or `ssd_docs/2_product_blueprint.md` during the skill flow. Use distillates only.

## Outputs

Final user-facing document:

- `ssd_docs/3_architecture_blueprint.md`

Internal temp draft:

- `._ssd_docs_temp/_docs/3_architecture_blueprint.md`

Internal final distillate:

- `._ssd_docs_distil/_docs/3_architecture_blueprint.md`

The final distillate is required but internal. Do not return it to the user in the success result.

## Template

Create `.opencode/skills/ssd-architecture-blueprint-create/templates/architecture-blueprint-template.md`:

```markdown
---
docType: architecture-blueprint
status: draft
sourceMaterial:
  - "{{product_brief_distillate}}"
  - "{{product_blueprint_distillate}}"
createdBy: ssd-architecture-blueprint-create
---

# Architecture Blueprint

## Architecture Intent

Describe the intended architectural direction and why it fits the product.

## Architectural Principles

List the principles that should guide architectural decisions.

- 
- 
- 

## Major Architectural Concerns

List the major concerns the architecture must account for.

- Authentication
- Authorization
- Multi-tenancy
- Data ownership
- Integration
- Observability
- Scalability
- Deployment
- Cost control

## Candidate System Components

List the likely major components of the system.

| Component | Responsibility |
|---|---|
|  |  |

## Key Data / Control Flows

Describe the most important high-level flows.

Example:

- Document ingestion -> indexing -> retrieval -> AI response
- User authentication -> tenant resolution -> permission evaluation

## Dependency Considerations

Describe important architectural dependencies.

Example:

- AI chat depends on retrieval
- Retrieval depends on ingestion and indexing
- Authorization affects all user-facing capabilities

## Technology Direction

Capture likely technology choices or constraints.

This should be directional, not final.

Example:

- Prefer PostgreSQL for relational data
- Prefer object storage for documents
- Prefer vector/hybrid search for retrieval
- Prefer modular service boundaries

## Architectural Risks

List major risks or unknowns.

- 
- 
- 

## Deferred Decisions

List decisions that should not be finalized yet.

- 
- 
- 

## Planning Implications

Summarize what this architecture blueprint implies for release planning.

Example:

- Release 1 should validate ingestion/search before advanced AI generation
- Authentication should be designed for multiple providers even if only one provider is enabled first

## ADR Candidates

List architectural decisions that may need formal ADRs later.

| Candidate Decision | Current Direction | Status | Why It May Need An ADR |
|---|---|---|---|
|  |  | directional / proposed / deferred |  |
```

The generated blueprint removes guidance text and replaces placeholders with source-backed content.

## Artifact Boundary

The Architecture Blueprint may include:

- Architectural intent.
- Architectural principles.
- Major architectural concerns.
- Candidate system components.
- High-level data/control flows.
- Dependency considerations.
- Directional technology choices or constraints.
- Architectural risks.
- Deferred decisions.
- Planning implications for release planning.
- ADR candidates.

The Architecture Blueprint must not include:

- Final architecture.
- Detailed system design.
- Final ADRs.
- API specifications.
- Database schemas.
- Infrastructure manifests.
- Deployment pipeline design.
- Release plan.
- Roadmap.
- Work packages.
- Engineering tasks.
- User stories or acceptance criteria.

Technology direction is allowed, but it must stay directional and reversible unless the user explicitly confirms a settled constraint.

## ADR Policy

ADRs are separate from the Architecture Blueprint.

The Architecture Blueprint skill captures ADR candidates only. It does not create individual ADR files by default.

Decision classifications:

- `directional`: useful architectural direction, but not ADR-worthy yet.
- `adr_candidate`: likely needs a formal ADR later.
- `adr_now`: important and settled enough that a future ADR creation skill should prioritize it.
- `deferred`: intentionally not decided yet.

The Architecture Blueprint includes an `ADR Candidates` section so later ADR tooling can create separate ADR files.

Future ADR paths should use:

```text
ssd_docs/adrs/index.md
ssd_docs/adrs/0001-<short-title>.md
```

Do not create those ADR files in this skill unless the user explicitly asks for best-effort ADR generation.

## Skill Inputs

```json
{
  "product_brief_distillate": "optional; default ._ssd_docs_distil/_docs/1_product_brief.md",
  "product_blueprint_distillate": "optional; default ._ssd_docs_distil/_docs/2_product_blueprint.md",
  "initial_context": "optional additional user context or architecture preferences"
}
```

## Hard Stops

Return structured precondition results. Do not produce outputs when preconditions fail.

If Product Brief distillate is missing:

```json
{
  "status": "precondition_failed",
  "reason": "Product Brief distillate is required before creating an Architecture Blueprint.",
  "expected": "._ssd_docs_distil/_docs/1_product_brief.md",
  "required_action": "Run the product brief creation flow first."
}
```

If Product Blueprint distillate is missing:

```json
{
  "status": "precondition_failed",
  "reason": "Product Blueprint distillate is required before creating an Architecture Blueprint.",
  "expected": "._ssd_docs_distil/_docs/2_product_blueprint.md",
  "required_action": "Run the product blueprint creation flow first."
}
```

If final Architecture Blueprint already exists:

```json
{
  "status": "skipped",
  "reason": "Architecture Blueprint already exists.",
  "architecture_blueprint": "ssd_docs/3_architecture_blueprint.md"
}
```

## Workflow

### 1. Preflight

Resolve input paths or defaults.

Check that both prerequisite distillates exist:

- `._ssd_docs_distil/_docs/1_product_brief.md`
- `._ssd_docs_distil/_docs/2_product_blueprint.md`

Check that final output does not exist:

- `ssd_docs/3_architecture_blueprint.md`

If any check fails, return the structured precondition/skipped result and stop.

### 2. Frame

State that this creates a pre-analysis Architecture Blueprint.

It is not the final architecture. It captures architectural intent, recommended direction, major concerns, risks, deferred decisions, planning implications, and ADR candidates before release planning.

### 3. Read Source Distillates

Read both required distillates:

- Product Brief distillate.
- Product Blueprint distillate.

Use optional `initial_context` as additional source material.

Do not scan project artifacts. Do not read original source docs.

### 4. Build Architecture Coverage Checklist

Create an internal checklist from both source distillates.

Extract from Product Brief:

- Product purpose.
- Audience/users.
- Differentiation.
- Practical constraints.
- Assumptions.
- Open questions.

Extract from Product Blueprint:

- Product definition.
- Boundaries.
- In-scope and out-of-scope areas.
- Major capabilities.
- Capability purposes.
- Product principles.
- Cross-cutting concerns.
- Assumptions.
- Major unknowns.

Internal checklist shape:

```json
{
  "product_drivers": [],
  "capabilities_to_cover": [],
  "cross_cutting_concerns": [],
  "data_or_state_implications": [],
  "user_and_access_implications": [],
  "integration_implications": [],
  "operational_implications": [],
  "technology_direction_questions": [],
  "risks_or_unknowns": [],
  "planning_implications_to_resolve": []
}
```

This checklist is internal source material for guided decisions and coverage validation.

### 5. Guided Architect Decision Path

The skill acts as an architect and guides the user through decisions.

For each decision group:

- Explain what the source material implies.
- Present 2-4 viable options.
- Always recommend one option first.
- Give concise pros and cons.
- Ask the user to accept, adjust, choose another option, or defer.
- Record the selected direction and rationale.
- Classify significant decisions as `directional`, `adr_candidate`, `adr_now`, or `deferred`.

Decision groups:

- Overall architectural shape.
- Architectural principles.
- Authentication and identity.
- Authorization and permissions.
- Tenancy and data ownership.
- Core component boundaries.
- Key data/control flows.
- Integration strategy.
- Observability and operations.
- Scalability posture.
- Deployment direction.
- Cost-control posture.
- Technology direction.
- Architectural risks.
- Deferred decisions.
- Planning implications.
- ADR candidates.

The architect should not ask a generic questionnaire. Ask focused decision prompts derived from the coverage checklist.

Prompt style:

```text
The Product Blueprint implies <architectural pressure>. I recommend <option> because <reason>.

Options:
1. <Recommended option> — Pros: <short>. Cons: <short>.
2. <Alternative option> — Pros: <short>. Cons: <short>.
3. <Alternative option> — Pros: <short>. Cons: <short>.

Choose one, adjust the recommendation, or defer this decision.
```

### 6. Maintain Decision Notes

Maintain internal decision notes while guiding the user:

```json
{
  "accepted_recommendations": [],
  "user_overrides": [],
  "deferred_decisions": [],
  "explicit_risks": [],
  "adr_candidates": [],
  "coverage_notes": []
}
```

Decision notes are source material for the coverage subagent and final draft.

### 7. Coverage Subagent Pass

Call `.opencode/agents/ssd_architecture_blueprint_coverage.md`.

Inputs:

- Product Brief distillate path.
- Product Blueprint distillate path.
- Internal architecture coverage checklist.
- Guided decision notes.
- Architecture Blueprint artifact boundary.

The subagent checks whether every product driver, major capability, product concern, assumption, and major unknown has architectural treatment, an explicit deferred decision, or an explicit risk.

It must not draft the document.

It must not make architecture decisions.

It must not read original source docs.

Return contract:

```json
{
  "status": "sufficient|needs_more_decisions",
  "missing_or_weak_items": [
    {
      "source_area": "product_driver|capability|concern|principle|assumption|unknown|constraint|planning_implication|adr_candidate",
      "issue": "what is not covered, weak, contradictory, or over-decided",
      "decision_needed": "specific decision or clarification needed"
    }
  ],
  "targeted_questions": [],
  "warnings": []
}
```

### 8. Coverage Loop

If coverage returns `needs_more_decisions`:

- Return to guided architect mode.
- Cover only the missing or weak points.
- Architect always recommends an option.
- User can accept, adjust, choose another option, or defer.
- Re-run coverage after meaningful new decisions.

Run at most 2 coverage loops.

After that, unresolved items become explicit `Architectural Risks` or `Deferred Decisions`, unless the missing point would make the document misleading.

### 9. Draft Temp Architecture Blueprint

Create:

```text
._ssd_docs_temp/_docs/3_architecture_blueprint.md
```

Use the template exactly:

```text
.opencode/skills/ssd-architecture-blueprint-create/templates/architecture-blueprint-template.md
```

Rules:

- Preserve section order and headings.
- Remove guidance text.
- Use only source-backed content from distillates, decision notes, coverage findings, and user decisions.
- Keep architecture directional and pre-analysis.
- Do not present tentative choices as final architecture.
- Record uncertain items as risks or deferred decisions.
- Include ADR candidates, but do not create ADR files.

### 10. Inline Final Review

Review the temp draft inside the skill.

The temp draft cannot be finalized while it has:

- Final architecture claims.
- Detailed system design.
- Unsupported architectural decisions.
- Missing coverage for major Product Blueprint capabilities.
- Missing treatment for major concerns, unless marked not applicable or deferred.
- Technology direction presented as final when it is only directional.
- ADR candidates mixed into final ADR decisions.
- Planning implications that become release plans, work packages, stories, or engineering tasks.
- Contradictions with Product Brief or Product Blueprint distillates.

Apply clear, non-controversial fixes directly to the temp draft.

Ask the user only for strategic architecture choices that cannot be safely deferred.

### 11. Finalize Once

Before final write, re-check that:

```text
ssd_docs/3_architecture_blueprint.md
```

does not exist.

If it exists, return `skipped`.

Otherwise create it exactly once from the reviewed temp draft.

### 12. Distill Final Blueprint

Call `ssd_distillator` exactly with:

```json
{
  "source_documents": ["ssd_docs/3_architecture_blueprint.md"],
  "downstream_consumer": "release planning, final architecture creation, PRD refinement, MVP definition, roadmap creation, and work package decomposition",
  "output_path": "._ssd_docs_distil/_docs/3_architecture_blueprint.md",
  "audit": false
}
```

Final distillation is mandatory. Audit is disabled for this workflow, so audit fix passes are not used.

### 13. Return Successful Result

On success only:

```json
{
  "status": "complete",
  "architecture_blueprint": "ssd_docs/3_architecture_blueprint.md",
  "warnings": []
}
```

Do not return the final distillate path. It is internal supporting context.

## Blocked Behavior

Only tool/runtime failures produce `blocked`.

Examples:

- Coverage subagent fails or returns invalid JSON.
- File write fails.
- Final distillation fails.

Return:

```json
{
  "status": "blocked",
  "reason": "specific failure",
  "failed_step": "step name",
  "partial_outputs": {
    "coverage_checklist": "created or null",
    "decision_notes": "created or null",
    "architecture_blueprint_draft": "path or null",
    "architecture_blueprint": "path or null"
  },
  "required_action": "Resolve the failed tool run and retry the skill.",
  "warnings": []
}
```

## Coverage Agent Plan

Create `.opencode/agents/ssd_architecture_blueprint_coverage.md`.

Agent purpose:

```text
Checks whether Architecture Blueprint decision notes cover the Product Brief and Product Blueprint source material before drafting.
```

Agent boundary:

- Read only explicit inputs.
- Do not read original source docs.
- Do not draft or rewrite the Architecture Blueprint.
- Do not make architecture decisions.
- Return only JSON coverage findings.

Coverage standard:

- Every major product capability has architectural treatment.
- Every major Product Blueprint cross-cutting concern is addressed, marked not applicable, deferred, or risk-recorded.
- User/access implications are covered where relevant.
- Data/state implications are covered where relevant.
- Integration implications are covered where relevant.
- Operational implications are covered where relevant.
- Technology direction questions are addressed directionally or deferred.
- Major unknowns become architectural risks or deferred decisions.
- Planning implications follow from architecture decisions without becoming a release plan.
- Significant decisions are classified for ADR handling.

## Catalog Updates

Add to `docs/index.md`:

```markdown
| skill | [ssd-architecture-blueprint-create](skills/ssd-architecture-blueprint-create.md) | Creates a pre-analysis Architecture Blueprint from the Product Brief and Product Blueprint through guided architecture decisions, coverage validation, ADR candidate capture, and mandatory SSD distillation. |
| agent | [ssd_architecture_blueprint_coverage](agents/ssd_architecture_blueprint_coverage.md) | Checks whether guided Architecture Blueprint decisions cover Product Brief and Product Blueprint source material before drafting. |
```

Create `docs/skills/ssd-architecture-blueprint-create.md` summarizing:

- Purpose.
- Inputs.
- Outputs.
- Workflow.
- Paths.
- Completion criteria.
- Related files.

Create `docs/agents/ssd_architecture_blueprint_coverage.md` summarizing:

- Purpose.
- Inputs.
- Return contract.
- Boundary.
- Invocation guidance.

## Success Criteria

- Skill exists and describes the guided architect workflow.
- Template exists with the requested sections plus `ADR Candidates`.
- Coverage subagent exists and returns only JSON.
- Catalog includes skill and agent.
- Skill requires both Product Brief and Product Blueprint distillates.
- Skill does not use brainstorming.
- Skill does not create ADR files by default.
- Skill captures ADR candidates in the Architecture Blueprint.
- Final distillation is mandatory with `audit: false`.
- Success result returns only `architecture_blueprint` and user-facing metadata.
