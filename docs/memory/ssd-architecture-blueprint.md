# ssd-architecture-blueprint Memory Contract

## Summary

- Unit: `ssd-architecture-blueprint-create`
- Unit type: `skill`
- Source: `.opencode/skills/ssd-architecture-blueprint-create/SKILL.md`
- Memory role: Creates and deletes SQLite-backed Architecture Blueprint artifact memory from Product Blueprint memory and optional Product Brief or brainstorm source memory, after interactive architecture recommendation discovery and final user approval.
- Created memory contracts: `Artifact`, `ArtifactSection` for kind `architecture-blueprint`
- Used memory contracts: `Artifact` and `ArtifactSection` kind `product-blueprint`, optional `Artifact` and `ArtifactSection` kind `product-brief`, optional `Brainstorm`, optional `BrainstormIdea`
- Memory script: `.opencode/scripts/ssd_architecture_blueprint/memory.py`

## Creates Or Mutates

| Memory | Status | Action | Contract | Command / Step | Result |
| --- | --- | --- | --- | --- | --- |
| `Artifact` | `current` | `create` | `docs/memory/ssd-architecture-blueprint.md` | `create` | Stable Architecture Blueprint root with kind `architecture-blueprint`. |
| `Artifact` | `current` | `delete` | `docs/memory/ssd-architecture-blueprint.md` | `delete --artifact-id <id> --confirm <id>` | Deletes the Architecture Blueprint artifact, owned child nodes, and attached relationships. |
| `ArtifactSection` | `current` | `create` | `docs/memory/ssd-architecture-blueprint.md` | `create` | Current canonical Architecture Blueprint section content. |

## Creation Details

| Created Memory | Input / Source | Stored As | Required | Rule |
| --- | --- | --- | --- | --- |
| `Artifact.kind` | memory adapter | `field` | `yes` | Always `architecture-blueprint`. |
| `Artifact.title` | memory adapter | `field` | `yes` | Always `Architecture Blueprint`. |
| `Artifact.id` | memory adapter | `field` | `yes` | UUID. Do not derive from `kind`. |
| `ArtifactSection.architecture-recommendations` | section payload | `section` | `yes` | Concrete recommendation blocks for relevant or unknown architecture decision areas. |
| `ArtifactSection.decision-coverage` | section payload | `section` | `yes` | Compact coverage table for all required decision areas with `Recommended`, `Not needed`, or `Unknown` status. |
| `ArtifactSection.open-risks` | section payload | `section` | `yes` | Only risks that could overturn recommendations. |
| `ArtifactSection.phase-1-validation` | section payload | `section` | `yes` | Validation needed before downstream planning depends on the recommendations. |
| `DERIVED_FROM` | Product Blueprint artifact ID | `relationship` | `yes` | Links Architecture Blueprint artifact to the Product Blueprint artifact used as source. |
| `DERIVED_FROM` | Product Brief artifact ID | `relationship` | `no` | Links Architecture Blueprint artifact to the Product Brief artifact when used as optional source. |
| `DERIVED_FROM` | `source_brainstorms` | `relationship` | `no` | Links Architecture Blueprint artifact to each brainstorm root that informed it, with `role` on the edge. |
| `CITES` | `cited_idea_ids` | `relationship` | `no` | Links Architecture Blueprint artifact to brainstorm ideas that informed it. |

## Creation Rules

- Idempotency: fails_if_exists.
- Mutability: immutable_after_create for this skill; no edit skill exists yet.
- Evidence requirement: inherited.
- User validation: create requires interactive recommendation discovery, required decision coverage, reviewed final sections, and final user approval.
- Missing input behavior: block when Product Blueprint memory or required section keys are absent; use `Unknown` inside sections when source material is insufficient.
- Delete behavior: requires exact Architecture Blueprint `artifact_id` and matching `--confirm`; deletes the architecture-blueprint artifact and owned children only.
- Stale memory behavior: none for this create-only skill.

## Uses Memory

| Memory Dependency | Status | Contract / Owner | Command / Access | Required | Purpose | Missing / Stale Behavior |
| --- | --- | --- | --- | --- | --- | --- |
| `Artifact` | `current` | `ssd-product-blueprint` | `.opencode/scripts/ssd_product_blueprint/memory.py get` | `yes` | Product Blueprint artifact source reference and current sections. | precondition_failed |
| `Artifact` | `current` | `ssd-product-brief` | `.opencode/scripts/ssd_product_brief/memory.py get` | `no` | Optional Product Brief source context. | warn and continue |
| `Brainstorm` | `current` | `ssd-brainstorming` | producer-owned `memory_handoff.command` | `no` | Optional supplemental source material. | skip if none are used |
| `BrainstormIdea` | `current` | `ssd-brainstorming` | producer-owned `memory_handoff.command` | `no` | Optional cited idea provenance for Architecture Blueprint content. | skip if no ideas are cited |

## Non-Owned Boundaries

- Product Blueprint and Product Brief memory are read but not created or modified by this skill.
- `Brainstorm` and `BrainstormIdea` memory are read through producer-owned handoff commands but not created directly by the Architecture Blueprint memory adapter.
- When a user asks to inspect, use, or delete stored Architecture Blueprint memory, callers use `.opencode/shared/recipes.md` and `.opencode/shared/recipes/architecture-blueprint.md` to discover commands.
- Generic current-state artifact shape is defined in `docs/memory.md`; this contract only defines Architecture Blueprint-specific section keys and commands.
- Architecture Blueprint skills do not write Architecture Blueprint markdown, temp markdown drafts, or downstream artifact memory.
- Raw Cypher is not used by this skill.

## Returned Memory References

| Output Field | Reference Type | Source Memory | Meaning |
| --- | --- | --- | --- |
| `artifact_id` | `id` | `Artifact` | UUID for the stable Architecture Blueprint root memory node. |
| `artifact_kind` | `kind` | `Artifact` | Architecture Blueprint artifact kind, `architecture-blueprint`. |
| `cited_idea_ids` | `id` | `BrainstormIdea` | Optional brainstorm ideas cited by the Architecture Blueprint. |
| `deleted` | `count` | Architecture Blueprint owned memory | Delete result with artifact ID, artifact kind, and total deleted node count. |
| `product_blueprint_artifact_id` | `id` | `Artifact` | UUID for the source Product Blueprint root memory node. |
| `product_brief_artifact_id` | `id` | `Artifact` | Optional UUID for the source Product Brief root memory node. |
| `sections_approved` | `kind` | section keys | Section keys approved during the guided skill run. |
| `source_brainstorms` | `id` | `Brainstorm` | Optional brainstorm roots and handoff commands used as source material. |

## Invariants

- Architecture Blueprint artifact kind is always `architecture-blueprint`.
- All created node IDs are UUIDs.
- All created graph nodes have non-empty human-facing titles.
- Consumers identify Architecture Blueprint through semantic commands and `artifact_kind=architecture-blueprint`, not by constructing IDs.
- Required section keys must all be present on create.
- Architecture Blueprint create requires Product Blueprint memory source references.
- Architecture Blueprint source brainstorms support multiple brainstorms with roles.
- Architecture Blueprint skills return memory references, not markdown paths.
- Architecture Blueprint create requires interactive recommendation discovery and final user approval before memory write.

## Gaps

| Gap | Affects | Status | Source | Notes |
| --- | --- | --- | --- | --- |
| None | `None` | `None` | `None` | None |
