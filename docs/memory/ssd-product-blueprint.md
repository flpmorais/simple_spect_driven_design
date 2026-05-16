# ssd-product-blueprint Memory Contract

## Summary

- Unit: `ssd-product-blueprint-create`
- Unit type: `skill`
- Source: `.opencode/skills/ssd-product-blueprint-create/SKILL.md`
- Memory role: Creates and deletes SQLite-backed Product Blueprint artifact memory from Product Brief memory and brainstorm source memory.
- Created memory contracts: `Artifact`, `ArtifactSection` for kind `product-blueprint`, `SourceFile` for snapshotted file sources
- Used memory contracts: `Artifact` and `ArtifactSection` kind `product-brief`, `Brainstorm`, `BrainstormIdea`
- Memory script: `.opencode/scripts/ssd_product_blueprint/memory.py`

## Creates Or Mutates

| Memory | Status | Action | Contract | Command / Step | Result |
| --- | --- | --- | --- | --- | --- |
| `Artifact` | `current` | `create` | `docs/memory/ssd-product-blueprint.md` | `create` | Stable Product Blueprint root with kind `product-blueprint`. |
| `Artifact` | `current` | `delete` | `docs/memory/ssd-product-blueprint.md` | `delete --artifact-id <id> --confirm <id>` | Deletes the Product Blueprint artifact, owned child nodes, and attached relationships. |
| `ArtifactSection` | `current` | `create` | `docs/memory/ssd-product-blueprint.md` | `create` | Current canonical Product Blueprint section content. |

## Creation Details

| Created Memory | Input / Source | Stored As | Required | Rule |
| --- | --- | --- | --- | --- |
| `Artifact.kind` | memory adapter | `field` | `yes` | Always `product-blueprint`. |
| `Artifact.title` | memory adapter | `field` | `yes` | Always `Product Blueprint`. |
| `Artifact.id` | memory adapter | `field` | `yes` | UUID. Do not derive from `kind`. |
| `ArtifactSection.title` | section heading | `field` | `yes` | Human-facing graph title, `Product Blueprint: <heading>`. |
| `ArtifactSection.assumptions` | section payload | `section` | `yes` | Material assumptions that shape the product. |
| `ArtifactSection.cross-cutting-concerns` | section payload | `section` | `yes` | Product-level concerns across capability areas; no architecture prescription. |
| `ArtifactSection.in-scope` | section payload | `section` | `yes` | What belongs inside the product boundary. |
| `ArtifactSection.major-capabilities` | section payload | `section` | `yes` | Conceptual capability areas, purposes, and capabilities. |
| `ArtifactSection.major-unknowns` | section payload | `section` | `yes` | Significant unresolved product-shaping unknowns. |
| `ArtifactSection.out-of-scope` | section payload | `section` | `yes` | What is explicitly outside the product boundary. |
| `ArtifactSection.product-definition` | section payload | `section` | `yes` | What the product is intended to be at a conceptual level. |
| `ArtifactSection.product-principles` | section payload | `section` | `yes` | Principles that guide product and technical tradeoffs. |
| `DERIVED_FROM` | Product Brief artifact ID | `relationship` | `yes` | Links Product Blueprint artifact to the Product Brief artifact used as source. |
| `DERIVED_FROM` | `source_artifacts` | `relationship` | `no` | Links Product Blueprint artifact to extra source artifacts used as source material, with `role` and `kind` on the edge. |
| `SourceFile` | `source_files` | `node` | `no` | Snapshotted source file metadata with original path, snapshot path, hash, and size. |
| `DERIVED_FROM` | `source_files` | `relationship` | `no` | Links Product Blueprint artifact to each snapshotted `SourceFile`, with `role` on the edge. |
| `DERIVED_FROM` | `source_brainstorms` | `relationship` | `yes` | Links Product Blueprint artifact to each brainstorm root that informed it, with `role` on the edge. |
| `CITES` | `cited_idea_ids` | `relationship` | `no` | Links Product Blueprint artifact to brainstorm ideas that informed it. |

## Creation Rules

- Idempotency: fails_if_exists.
- Mutability: immutable_after_create for this skill; no edit skill exists yet.
- Evidence requirement: inherited.
- User validation: create requires explicit user approval after all proposed sections are shown in human-readable form.
- Missing input behavior: block when Product Brief memory, product-dream brainstorm memory, or required section keys are absent; use_unknown inside sections when source material is insufficient.
- Delete behavior: requires exact Product Blueprint `artifact_id` and matching `--confirm`; deletes the product-blueprint artifact and owned children only.
- Stale memory behavior: none for this create-only skill.

## Uses Memory

| Memory Dependency | Status | Contract / Owner | Command / Access | Required | Purpose | Missing / Stale Behavior |
| --- | --- | --- | --- | --- | --- | --- |
| `Brainstorm` | `current` | `ssd-brainstorming` | producer-owned `memory_handoff.command` | `yes` | Mandatory product-dream source material and optional supplemental source material. | block |
| `BrainstormIdea` | `current` | `ssd-brainstorming` | producer-owned `memory_handoff.command` | `no` | Optional cited idea provenance for Product Blueprint content. | skip if no ideas are cited |
| `Artifact` | `current` | `ssd-product-brief` | `.opencode/scripts/ssd_product_brief/memory.py get` | `yes` | Product Brief artifact source reference. | precondition_failed |
| `ArtifactSection` | `current` | `ssd-product-brief` | `.opencode/scripts/ssd_product_brief/memory.py get` | `yes` | Product Brief section source for the Blueprint. | precondition_failed |
| `Artifact` | `current` | matching recipe owner | `.opencode/shared/recipes.md` and matching recipe | `no` | Extra stored artifact source material requested by the user. | skip if not requested; block or ask if requested artifact cannot be loaded |
| file | snapshot | filesystem | direct read, then snapshot under `.opencode/shared/memory/files/` | `no` | Extra user-provided file source material. | skip if not requested; block or ask if requested file cannot be read |

## Non-Owned Boundaries

- Product Brief memory is read but not created or modified by this skill.
- `Brainstorm` and `BrainstormIdea` memory are read through producer-owned handoff commands but not created directly by the Blueprint memory adapter.
- Extra source artifacts are read through recipes and cited but not modified.
- Extra source files are copied into `.opencode/shared/memory/files/` and cited through `SourceFile` nodes; original files are not modified.
- When a user asks to inspect, use, or delete stored Product Blueprint memory, callers use `.opencode/shared/recipes.md` and `.opencode/shared/recipes/product-blueprint.md` to discover commands.
- Generic current-state artifact shape is defined in `docs/memory.md`; this contract only defines Product Blueprint-specific section keys and commands.
- Product Blueprint skills do not write Product Blueprint markdown, temp markdown drafts, or downstream artifact memory.
- Raw Cypher is not used by this skill.

## Returned Memory References

| Output Field | Reference Type | Source Memory | Meaning |
| --- | --- | --- | --- |
| `artifact_id` | `id` | `Artifact` | UUID for the stable Product Blueprint root memory node. |
| `artifact_kind` | `kind` | `Artifact` | Product Blueprint artifact kind, `product-blueprint`. |
| `cited_idea_ids` | `id` | `BrainstormIdea` | Optional brainstorm ideas cited by the Product Blueprint. |
| `deleted` | `count` | Product Blueprint owned memory | Delete result with artifact ID, artifact kind, and total deleted node count. |
| `product_brief_artifact_id` | `id` | `Artifact` | UUID for the source Product Brief root memory node. |
| `source_artifacts` | `id` | `Artifact` | Extra artifact sources used as source material. |
| `source_files` | `id` | `SourceFile` | Snapshotted file sources used as source material. |
| `source_brainstorms` | `id` | `Brainstorm` | Brainstorm roots and handoff commands used as source material. |

## Invariants

- Product Blueprint artifact kind is always `product-blueprint`.
- All created node IDs are UUIDs.
- All created graph nodes have non-empty human-facing titles.
- Consumers identify Product Blueprint through semantic commands and `artifact_kind=product-blueprint`, not by constructing IDs.
- Required section keys must all be present on create.
- Product Blueprint create requires Product Brief memory source references.
- Product Blueprint source brainstorms support multiple brainstorms with roles.
- Product Blueprint source artifacts and source files support role `extra_source`.
- Source files are copied to `.opencode/shared/memory/files/` and cited by `SourceFile.snapshot_path`.
- Product Brief source brainstorms use role `product_brief_source`; mandatory product-dream brainstorms use role `product_dream`; supplemental brainstorms use role `supplemental`.
- Product Blueprint skills return memory references, not markdown paths.
- Product Blueprint create requires explicit user approval before memory write.

## Gaps

| Gap | Affects | Status | Source | Notes |
| --- | --- | --- | --- | --- |
| None | `None` | `None` | `None` | None |
