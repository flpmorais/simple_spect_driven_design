# Product Blueprint Contract

Apply this contract for Product Blueprint creation.

## Interaction Model

The skill is a product-shaping partner, not a blind document generator.

- Explore product shape with prompts, challenges, tradeoff framing, and synthesis.
- Use AI suggestions as options/provocations, not accepted facts.
- Store only content grounded in Product Brief memory, accepted brainstorm ideas, direct user input, approved source artifacts/files, or explicit assumptions approved through review.
- Ask once at the start about extra stored memory or file sources.
- Load artifacts through `.opencode/shared/recipes.md` plus the matching recipe; read files directly.
- Cite extra artifacts and snapshot/cite source files used as material.
- Ask at most 3 focused questions at a time, only for strategic product choices.
- If unknown, record `Unknown`, a named assumption, or a major unknown.

## Artifact Boundary

The Product Blueprint expands the Product Brief into conceptual product shape before delivery planning.

Include product definition, in/out-of-scope boundaries, major capability areas and purposes, conceptual capabilities, product principles, cross-cutting concerns, assumptions, and major unknowns.

Exclude requirements, user stories, acceptance criteria, architecture, technology stack, data models, API design, MVP scope, roadmap, delivery sequencing, work packages, engineering tasks, and success metrics used as planning criteria. For technical products, discuss only product-level value, problem, audience, concept, boundaries, and capabilities.

## Required Sections

Store as SQLite-backed `Artifact` memory with kind `product-blueprint`. Use exact keys/headings:

| Section Key | Heading |
| --- | --- |
| `product-definition` | Product Definition |
| `in-scope` | In Scope |
| `out-of-scope` | Out Of Scope |
| `major-capabilities` | Major Capabilities |
| `product-principles` | Product Principles |
| `cross-cutting-concerns` | Cross-Cutting Concerns |
| `assumptions` | Assumptions |
| `major-unknowns` | Major Unknowns |

Unsupported sections must be `Unknown` or a clear assumption. Do not invent content.

## Mandatory Ideation

Run one product-dream brainstorm before drafting.

- Load Product Brief `cited_brainstorm_ids` first and use them as source context with role `product_brief_source`.
- Use `ssd-brainstorming` with `scope=normal`, `mode=guided`, `downstream_consumer=ssd-product-blueprint-create`, and no fixed techniques.
- Let `ssd-brainstorming` select techniques.
- Execution remains user-led and interactive, even with `run_mode=internal`.
- Use brainstorm memory handoff output as source material, not markdown paths.
- Do not satisfy the target with filler ideas.

## Optional Supplemental Ideation

Recommend one supplemental ideation pass when reviewed sections are thin, vague, generic, conflicted, or assumption-heavy. The user may decline. Repeat only when explicitly requested.

## Review And User Validation Gate

Review the payload before presenting it. Do not call Product Blueprint review subagents.

Do not write while the payload has invented specificity, vague definition, weak/missing/overlapping/contradictory boundaries, requirement-like capabilities, missing capability purposes, generic principles, architecture-prescribing concerns, assumptions as facts, trivial/technical/non-product unknowns, source contradictions, or MVP/roadmap/delivery/metric/architecture/stack/data/API/work-package/engineering drift.

After fixes, present every proposed section in human-readable Markdown. Also show source brainstorms, extra sources, assumptions to store, and major unknowns to keep unresolved.

Ask for explicit approval to create or section-level changes. Do not write until the user explicitly approves after seeing the reviewed payload. Discussion, clarification, or source selection is not approval. If changes are requested, revise and repeat this gate.

## Memory Write

After mandatory ideation, internal review, and explicit approval, write through `.opencode/scripts/ssd_product_blueprint/memory.py`.

```text
python .opencode/scripts/ssd_product_blueprint/memory.py create
```

Pass JSON on stdin:

```json
{
  "change_summary": "Initial Product Blueprint",
  "product_brief_artifact_id": "<uuid>",
  "sections": {
    "product-definition": "...",
    "in-scope": "...",
    "out-of-scope": "...",
    "major-capabilities": "...",
    "product-principles": "...",
    "cross-cutting-concerns": "...",
    "assumptions": "...",
    "major-unknowns": "..."
  },
  "source_artifacts": [],
  "source_files": [],
  "source_brainstorms": [],
  "cited_idea_ids": []
}
```

The adapter stores current `Artifact` and `ArtifactSection` memory with provenance to source Product Brief, extra artifacts, source file snapshots, source brainstorms, and cited ideas.

Do not create Product Blueprint markdown or temp drafts.
