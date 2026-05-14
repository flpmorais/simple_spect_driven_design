# Product Blueprint Skill Plan

Build a new OpenCode-native skill: `ssd-product-blueprint-create`.

It mirrors the structure of `ssd-product-brief-create`, but its artifact boundary is different: it expands the distilled Product Brief into the conceptual product shape, not requirements, architecture, MVP scope, roadmap, or delivery planning.

## Artifacts To Add

Create:

- `.opencode/skills/ssd-product-blueprint-create/SKILL.md`
- `.opencode/skills/ssd-product-blueprint-create/templates/product-blueprint-template.md`
- `.opencode/agents/ssd_product_blueprint_coverage.md`
- `.opencode/agents/ssd_product_blueprint_skeptic.md`
- `docs/catalog/ssd-product-blueprint-create.md`
- `docs/catalog/ssd_product_blueprint_coverage.md`
- `docs/catalog/ssd_product_blueprint_skeptic.md`

Update:

- `docs/catalog.md`

## Product Blueprint Template

Use this base structure, with SSD frontmatter added:

```markdown
---
docType: product-blueprint
status: draft
sourceMaterial:
  - "{{product_brief_distillate}}"
  - "{{product_shape_brainstorm_distillate}}"
  - "{{product_integrity_brainstorm_distillate}}"
createdBy: ssd-product-blueprint-create
---

# Product Blueprint

## Product Definition

Describe the product in plain language.
Explain what the product is intended to be at a conceptual level.

## Product Boundaries

Define what this product is and is not.

### In Scope

### Out Of Scope

## Major Capabilities

### <Capability Area>

#### Purpose

#### Capabilities

## Product Principles

List the principles that should guide product and technical decisions.

## Cross-Cutting Concerns

List concerns that affect multiple capability areas.

## Assumptions

List assumptions that materially shape the product.

## Major Unknowns

List unresolved questions or uncertainties that may significantly affect the product.
```

The generated blueprint removes guidance text and replaces placeholders with source-backed content.

## Skill Inputs

```json
{
  "product_brief_distillate": "optional, defaults to ._ssd_docs_distil/_docs/1_product_brief.md",
  "initial_context": "optional additional user context"
}
```

`product_brief_distillate` defaults to:

```text
._ssd_docs_distil/_docs/1_product_brief.md
```

## Hard Stops

These are not `blocked` statuses. The skill simply stops before producing outputs.

Hard stop if:

- Product brief distillate does not exist.
- Final blueprint already exists at `ssd_docs/2_product_blueprint.md`.

Behavior:

- No brainstorms.
- No temp draft.
- No final file.
- No distillation.
- No structured result object.

Message examples:

```text
Product brief distillate is required before creating a Product Blueprint.
Expected: ._ssd_docs_distil/_docs/1_product_brief.md
Run the product brief creation flow first.
```

```text
Product Blueprint already exists at ssd_docs/2_product_blueprint.md.
This create skill will not overwrite or edit it.
```

## Paths

- Product brief distillate: `._ssd_docs_distil/_docs/1_product_brief.md`
- Product shape brainstorm folder: `_docs/2_product_blueprint/product_shape`
- Product integrity brainstorm folder: `_docs/2_product_blueprint/product_integrity`
- Product shape brainstorm raw: `._ssd_docs_temp/brainstorming/_docs/2_product_blueprint/product_shape/<filename>`
- Product shape brainstorm distillate: `._ssd_docs_distil/brainstorming/_docs/2_product_blueprint/product_shape/<filename>`
- Product integrity brainstorm raw: `._ssd_docs_temp/brainstorming/_docs/2_product_blueprint/product_integrity/<filename>`
- Product integrity brainstorm distillate: `._ssd_docs_distil/brainstorming/_docs/2_product_blueprint/product_integrity/<filename>`
- Template: `.opencode/skills/ssd-product-blueprint-create/templates/product-blueprint-template.md`
- Temp draft: `._ssd_docs_temp/_docs/2_product_blueprint.md`
- Final blueprint: `ssd_docs/2_product_blueprint.md`
- Final blueprint distillate: `._ssd_docs_distil/_docs/2_product_blueprint.md`

## Product Boundary

The blueprint may include:

- Product definition
- Conceptual product boundaries
- In-scope and out-of-scope product areas
- Major capability areas
- Purpose of each capability area
- Conceptual capabilities
- Product principles
- Cross-cutting concerns
- Assumptions
- Major unknowns

The blueprint must not include:

- Requirements
- User stories
- Acceptance criteria
- Architecture
- Technology stack
- Data models
- API design
- MVP scope
- Roadmap
- Delivery sequencing
- Work packages
- Engineering tasks
- Success metrics unless already present as conceptual product concern and not used as planning criteria

## Workflow

### 1. Preflight

- Check that `._ssd_docs_distil/_docs/1_product_brief.md` exists.
- Check that `ssd_docs/2_product_blueprint.md` does not exist.
- If either check fails, hard stop.

### 2. Frame

- State that this creates a conceptual Product Blueprint from the distilled Product Brief.
- Explicitly state that it will avoid requirements, architecture, MVP, roadmap, and delivery planning.

### 3. Product Shape Brainstorm

Call `ssd-brainstorming` with:

```json
{
  "run_mode": "internal",
  "topic": "<product from brief>",
  "initial_context": "<product brief distillate plus optional user context>",
  "scope": "normal",
  "target_folder": "_docs/2_product_blueprint/product_shape",
  "downstream_consumer": "ssd-product-blueprint-create",
  "mode": "guided",
  "required_techniques": 3,
  "techniques": [
    {
      "name": "Mind Mapping",
      "purpose": "Branch from the product definition into major product areas, user-facing surfaces, supporting concepts, adjacent areas, and natural conceptual groupings."
    },
    {
      "name": "Morphological Analysis",
      "purpose": "Identify product dimensions such as actor types, information types, lifecycle stages, interaction modes, governance surfaces, and product states, then combine them to reveal missing or implicit capability areas."
    },
    {
      "name": "Ecosystem Thinking",
      "purpose": "Map the product's surrounding ecosystem of users, operators, affected parties, external dependencies, incentives, policies, and adjacent workflows without turning them into architecture."
    }
  ],
  "goal": "Expand the product brief into the product's intended conceptual surface, boundaries, and major capability areas without defining requirements, architecture, MVP, roadmap, or delivery scope.",
  "constraints": ["Apply Product Blueprint boundary."]
}
```

Expected output feeds:

- `Product Boundaries`
- `In Scope`
- `Out Of Scope`
- `Major Capabilities`
- Possible initial `Cross-Cutting Concerns`

### 4. Product Integrity Brainstorm

Read the product shape brainstorm distillate, then call `ssd-brainstorming` with:

```json
{
  "run_mode": "internal",
  "topic": "<product from brief>",
  "initial_context": "<product brief distillate plus product shape brainstorm distillate plus optional user context>",
  "scope": "normal",
  "target_folder": "_docs/2_product_blueprint/product_integrity",
  "downstream_consumer": "ssd-product-blueprint-create",
  "mode": "guided",
  "required_techniques": 3,
  "techniques": [
    {
      "name": "First Principles Thinking",
      "purpose": "Reduce the product to fundamental user and product truths, then derive principles that should guide future product and technical decisions."
    },
    {
      "name": "Role Playing",
      "purpose": "Inspect the proposed product shape from relevant stakeholder perspectives such as primary users, admins, operators, buyers, maintainers, skeptical adopters, and indirectly affected parties."
    },
    {
      "name": "Question Storming",
      "purpose": "Generate high-leverage unresolved questions that materially affect the product's conceptual structure but should not be answered prematurely as requirements or delivery plans."
    }
  ],
  "goal": "Challenge and stabilize the product shape by identifying guiding principles, cross-cutting concerns, assumptions, unknowns, and conceptual tensions that later work must respect.",
  "constraints": ["Apply Product Blueprint boundary."]
}
```

Expected output feeds:

- `Product Principles`
- `Cross-Cutting Concerns`
- `Assumptions`
- `Major Unknowns`
- Tensions between capability areas

### 5. Coverage Gate

Call new agent: `.opencode/agents/ssd_product_blueprint_coverage.md`.

Inputs:

- Product brief distillate path
- Product shape brainstorm distillate path
- Product integrity brainstorm distillate path
- Explicit user clarifications
- Product Blueprint boundary

Return contract:

```json
{
  "status": "sufficient|needs_clarification",
  "missing_or_weak_sections": [],
  "targeted_questions": [],
  "risks": [],
  "warnings": []
}
```

Coverage checks:

- Product Definition is source-backed.
- Boundaries are clear enough to distinguish product from adjacent areas.
- In-scope areas are represented.
- Out-of-scope areas are represented, or absence is explicitly handled.
- Major capability areas are coherent and not just requirements.
- Each major capability area has a purpose.
- Product principles are meaningful and decision-guiding.
- Cross-cutting concerns span multiple capabilities.
- Assumptions materially shape the product.
- Major unknowns are significant and not trivial.
- The material avoids requirements, architecture, MVP, roadmap, and delivery planning.

### 6. Clarification Loop

If coverage returns `needs_clarification`:

- Ask at most 3 targeted questions.
- Prefer questions that unlock multiple weak sections.
- Do not ask implementation, stack, MVP, roadmap, or delivery questions.
- If the user does not know, record `Unknown`, an explicit assumption, or a major unknown.
- Re-run coverage after meaningful clarification.
- Avoid infinite looping; after reasonable clarification, proceed by exposing uncertainty in the blueprint.

### 7. Draft Temp Blueprint

Create:

```text
._ssd_docs_temp/_docs/2_product_blueprint.md
```

Use the template exactly:

```text
.opencode/skills/ssd-product-blueprint-create/templates/product-blueprint-template.md
```

Rules:

- Preserve section order and headings.
- Remove guidance text.
- Use only source-backed content from brief, brainstorm distillates, and user clarifications.
- Use `Unknown` only when genuinely unknown.
- Prefer explicit assumptions over invented facts.
- Keep capability descriptions conceptual.
- Do not drift into requirements or architecture.

### 8. Skeptic Review

Call new agent: `.opencode/agents/ssd_product_blueprint_skeptic.md`.

Inputs:

- Temp blueprint
- Product brief distillate
- Product shape brainstorm distillate
- Product integrity brainstorm distillate
- Clarification notes
- Product Blueprint boundary

Review checks:

- Unsupported claims
- Vague or overlapping capability areas
- Accidental requirements
- Hidden architecture or implementation detail
- MVP or roadmap leakage
- Weak boundaries
- Generic principles
- Missing cross-cutting concerns
- Assumptions presented as facts
- Unknowns that are too low-level or not material

The reviewer returns findings only. It must not rewrite the blueprint.

### 9. Finalize Once

Apply clear, non-controversial improvements to the temp draft only.

Ask the user only if a review finding requires a strategic product choice.

Before final write, re-check that:

```text
ssd_docs/2_product_blueprint.md
```

does not exist.

Then create it exactly once from the final temp draft.

### 10. Distill Final Blueprint

Call `ssd_distillator` with:

```json
{
  "source_documents": ["ssd_docs/2_product_blueprint.md"],
  "downstream_consumer": "PRD creation, architectural analysis, MVP definition, roadmap creation, and work package decomposition",
  "output_path": "._ssd_docs_distil/_docs/2_product_blueprint.md",
  "audit": true,
  "max_fix_passes": 2,
  "fail_on_audit_findings": false
}
```

### 11. Return Successful Result

On success only:

```json
{
  "status": "complete",
  "product_blueprint_draft": "._ssd_docs_temp/_docs/2_product_blueprint.md",
  "product_blueprint": "ssd_docs/2_product_blueprint.md",
  "product_shape_brainstorm_raw": "._ssd_docs_temp/brainstorming/_docs/2_product_blueprint/product_shape/<filename>",
  "product_shape_brainstorm_distillate": "._ssd_docs_distil/brainstorming/_docs/2_product_blueprint/product_shape/<filename>",
  "product_integrity_brainstorm_raw": "._ssd_docs_temp/brainstorming/_docs/2_product_blueprint/product_integrity/<filename>",
  "product_integrity_brainstorm_distillate": "._ssd_docs_distil/brainstorming/_docs/2_product_blueprint/product_integrity/<filename>",
  "product_blueprint_distillate": "._ssd_docs_distil/_docs/2_product_blueprint.md",
  "warnings": []
}
```

## Blocked Behavior

Only tool/runtime failures produce `blocked`.

Examples:

- `ssd-brainstorming` fails.
- Expected brainstorm distillate is missing after a brainstorm run.
- Coverage agent fails or returns invalid JSON.
- Skeptic agent fails in a way the skill cannot safely ignore.
- File write fails.
- Final distillation fails.

Return:

```json
{
  "status": "blocked",
  "reason": "<specific failure>",
  "failed_step": "<step name>",
  "partial_outputs": {
    "product_shape_brainstorm_raw": "... or null",
    "product_shape_brainstorm_distillate": "... or null",
    "product_integrity_brainstorm_raw": "... or null",
    "product_integrity_brainstorm_distillate": "... or null",
    "product_blueprint_draft": "... or null",
    "product_blueprint": "... or null",
    "product_blueprint_distillate": "... or null"
  },
  "required_action": "Resolve the failed tool run and retry the skill.",
  "warnings": []
}
```

## Challenge To The Plan

### Risk 1: Two `normal` brainstorms may overproduce material.

Why it matters: A Product Blueprint should remain conceptual, not become a pseudo-PRD.

Mitigation: The skill must repeatedly enforce the Product Blueprint boundary and tell brainstorming to stop when enough section coverage exists, not chase exhaustive decomposition.

### Risk 2: `Major Capabilities` can easily become requirements.

Why it matters: Capability lists may drift into specific workflows, acceptance criteria, or implementation behavior.

Mitigation: The template should describe capabilities as conceptual product abilities, not `the system shall` statements. The skeptic agent should explicitly flag requirements language.

### Risk 3: `Product Principles` can become generic filler.

Why it matters: Principles like `simple`, `scalable`, or `user-friendly` are weak unless they guide tradeoffs.

Mitigation: Coverage should require principles to be decision-guiding. Example: `Prefer explainable workflows over hidden automation when user trust is at stake.`

### Risk 4: `Cross-Cutting Concerns` may become architecture concerns.

Why it matters: Security, privacy, governance, data quality, and reliability can be product concerns, but they can also trigger premature technical design.

Mitigation: The skill should allow product-level concerns but forbid solution mechanisms.

### Risk 5: The coverage loop could become annoying.

Why it matters: Asking repeated questions can slow the workflow and duplicate what brainstorming already surfaced.

Mitigation: Ask at most 3 questions per pass, prioritize high-leverage gaps, and proceed with assumptions/unknowns when the user cannot answer.

### Risk 6: A separate `coverage` agent and `skeptic` agent add complexity.

Why it matters: This is more machinery than a minimal skill.

Decision: Use the skeptic agent. Blueprint drift into requirements and architecture is likely enough to justify the extra review gate.

### Risk 7: Hard stop with no structured status is less machine-friendly.

Why it matters: Later automation might prefer a structured `skipped` or `precondition_failed` result.

Why it matches the intended behavior: Missing prerequisite and existing final file should produce no outputs and no status. The skill docs should make this intentional so future agents do not convert it into a structured result.

### Risk 8: The final distillate consumer is broad.

Why it matters: A distillate aimed at PRD, architecture, MVP, roadmap, and work packages may become too general.

Mitigation: The distillator should preserve the blueprint's conceptual structure and explicitly mark downstream relevance without adding downstream decisions.

## Recommendation

Proceed with the plan as written, with these decisions:

- Make the coverage agent status only `sufficient|needs_clarification`.
- Include the skeptic agent in v1.
