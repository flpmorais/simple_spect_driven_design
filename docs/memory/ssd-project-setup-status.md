# ssd-project-setup-status Memory Contract

## Summary

- Unit: `ssd-project-setup-status`
- Unit type: `skill`
- Source: `.opencode/skills/ssd-project-setup-status/SKILL.md`
- Memory role: Reads existing Artifact memory and returns setup status for the current project scope.
- Created memory contracts: None
- Used memory contracts: `Artifact` from `docs/memory.md`, `Artifact` kind `product-brief` from `docs/memory/ssd-product-brief.md`, `Artifact` kind `product-blueprint` from `docs/memory/ssd-product-blueprint.md`, and `Artifact` kind `architecture-blueprint` from `docs/memory/ssd-architecture-blueprint.md`
- Memory script: `.opencode/scripts/ssd_project_setup/memory.py`

## Creates Or Mutates

| Memory | Status | Action | Contract | Command / Step | Result |
| --- | --- | --- | --- | --- | --- |
| None | `current` | none | None | `status` | No memory is created or mutated. |

## Creation Details

| Created Memory | Input / Source | Stored As | Required | Rule |
| --- | --- | --- | --- | --- |
| None | None | None | no | This adapter is read-only. |

## Creation Rules

- Idempotency: none
- Mutability: none
- Mutability: none
- Evidence requirement: not_required
- Missing input behavior: block
- Stale memory behavior: none

## Uses Memory

| Memory Dependency | Status | Contract / Owner | Command / Access | Required | Purpose | Missing / Stale Behavior |
| --- | --- | --- | --- | --- | --- | --- |
| `Artifact` | `current` | `docs/memory.md` | `.opencode/scripts/ssd_project_setup/memory.py status` queries all `Artifact` nodes | yes | Builds a root-scoped setup graph projection from existing artifacts. | Missing setup artifacts are returned as available or blocked setup steps. |
| `Artifact(kind=architecture-blueprint)` | `current` | `docs/memory/ssd-architecture-blueprint.md` | Artifact graph query by `kind` | yes | Determines whether Architecture Blueprint setup is complete. | Missing when Product Blueprint exists returns `ssd-architecture-blueprint-create` as required setup work. |
| `Artifact(kind=product-blueprint)` | `current` | `docs/memory/ssd-product-blueprint.md` | Artifact graph query by `kind` | yes | Determines whether Product Blueprint setup is complete. | Missing when Product Brief exists returns `ssd-product-blueprint-create` as required setup work. |
| `Artifact(kind=product-brief)` | `current` | `docs/memory/ssd-product-brief.md` | Artifact graph query by `kind` | yes | Determines whether Product Brief setup is complete. | Missing returns `ssd-product-brief-create` as required setup work. |

## Non-Owned Boundaries

- Product Brief, Product Blueprint, and Architecture Blueprint memory are read but not created, updated, or deleted by this adapter.
- Brainstorm memory is not part of setup completion and is not read by this adapter.
- Future setup artifacts must be represented by existing or future artifact contracts; this adapter only reports what its setup registry defines.

## Returned Memory References

| Output Field | Reference Type | Source Memory | Meaning |
| --- | --- | --- | --- |
| `all_artifacts[].artifact_id` | id | `Artifact` | Artifact ID for every returned artifact in the selected scope. |
| `all_artifacts[].kind` | kind | `Artifact` | Artifact kind for every returned artifact in the selected scope. |
| `artifacts[].artifact_id` | id | `Artifact` | Artifact ID for a completed setup artifact. |
| `artifacts[].kind` | kind | setup registry and `Artifact.kind` | Setup artifact kind. |
| `available_next_steps[].artifact_kind` | kind | setup registry | Missing setup artifact whose prerequisites are complete. |
| `available_next_steps[].skill` | skill name | setup registry | Skill to run after user acceptance. |
| `blocked_steps[].artifact_kind` | kind | setup registry | Missing setup artifact that cannot run yet. |
| `blocked_steps[].blocked_by` | kind list | setup registry | Missing prerequisite artifact kinds. |
| `must_do[].artifact_kind` | kind | setup registry | Setup work the planner must present for user acceptance. |

## Invariants

- The adapter is read-only.
- Current scope support is `root`; `auto` resolves to `root`.
- Existing unscoped Artifact memory is treated as root-scoped.
- Setup status is a graph projection over existing memory, not a durable memory object.
- Duplicate setup artifacts for the same kind block setup status instead of selecting one.
- Brainstorm memory does not affect setup completeness.

## Gaps

| Gap | Affects | Status | Source | Notes |
| --- | --- | --- | --- | --- |
| Package scope detection | `uses` | planned | User request for future multiple packages | Current adapter only supports `root` and `auto` resolving to `root`. |
