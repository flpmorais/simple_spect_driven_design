# ssd-product-brief Memory Contract

## Summary

- Unit: `ssd-product-brief-create` and `ssd-product-brief-edit`
- Unit type: `skill`
- Source: `.opencode/skills/ssd-product-brief-create/SKILL.md`, `.opencode/skills/ssd-product-brief-edit/SKILL.md`
- Memory role: Creates, reads, and updates current SQLite-backed Product Brief artifact memory with required sections and provenance relationships.
- Created memory contracts: `Artifact`, `ArtifactSection` for kind `product-brief`
- Used memory contracts: `Brainstorm`, `BrainstormIdea` from `ssd-brainstorming` when optional ideation or user-requested artifact loading contributes source material
- Memory script: `.opencode/scripts/ssd_product_brief/memory.py`

## Creates Or Mutates

| Memory | Status | Action | Contract | Command / Step | Result |
| --- | --- | --- | --- | --- | --- |
| `Artifact` | `current` | `create` | `docs/memory/ssd-product-brief.md` | `create` | Stable Product Brief root with kind `product-brief`. |
| `Artifact` | `current` | `delete` | `docs/memory/ssd-product-brief.md` | `delete --artifact-id <id> --confirm <id>` | Deletes the Product Brief artifact, owned child nodes, and attached relationships. |
| `ArtifactSection` | `current` | `update` | `docs/memory/ssd-product-brief.md` | `create`, `update` | Current canonical Product Brief section content. |

## Creation Details

| Created Memory | Input / Source | Stored As | Required | Rule |
| --- | --- | --- | --- | --- |
| `Artifact.kind` | memory adapter | `field` | `yes` | Always `product-brief`. |
| `Artifact.title` | memory adapter | `field` | `yes` | Always `Product Brief`. |
| `Artifact.id` | memory adapter | `field` | `yes` | UUID. Do not derive from `kind`. |
| `ArtifactSection.title` | section heading | `field` | `yes` | Human-facing graph title, `Product Brief: <heading>`. |
| `ArtifactSection.audience` | section payload | `section` | `yes` | Required; use `Unknown` if source material does not support content. |
| `ArtifactSection.assumptions` | section payload | `section` | `yes` | Required; explicit assumptions only. |
| `ArtifactSection.high-level-solution` | section payload | `section` | `yes` | Required; excludes implementation detail. |
| `ArtifactSection.necessity-and-differentiation` | section payload | `section` | `yes` | Required; must be source-backed or marked `Unknown` / assumption. |
| `ArtifactSection.open-questions` | section payload | `section` | `yes` | Required; useful product-level open questions. |
| `ArtifactSection.positioning` | section payload | `section` | `yes` | Required; product/user/market framing. |
| `ArtifactSection.practical-constraints` | section payload | `section` | `yes` | Required; practical product constraints only. |
| `ArtifactSection.problem` | section payload | `section` | `yes` | Required; core product problem. |
| `ArtifactSection.product-definition` | section payload | `section` | `yes` | Required; what is being built at product level. |
| `ArtifactSection.why-this-exists` | section payload | `section` | `yes` | Required; why the product should exist. |
| `DERIVED_FROM` | `cited_brainstorm_ids` | `relationship` | `no` | Links Product Brief artifact to brainstorm roots that informed it. |
| `CITES` | `cited_idea_ids` | `relationship` | `no` | Links Product Brief artifact to brainstorm ideas that informed it. |

## Creation Rules

- Idempotency: fails_if_exists for `create`; `update` replaces current state.
- Mutability: current sections and provenance relationships are mutable by explicit update.
- Evidence requirement: inherited.
- User validation: create requires a create-only advanced elicitation validation gate before approval, then explicit user approval after all proposed sections are shown in human-readable form; edit requires explicit user approval after a focused human-readable review of changed sections only and skips the create validation gate. Approval/change instructions must appear after the reviewed content, as the final paragraph of the review response.
- Section grounding: stored Product Brief statements must be grounded in explicit user input, confirmed source memory, user-provided files, accepted brainstorm idea memory, explicit user-approved assumptions, or `Unknown`; inferred section prose is not valid memory content.
- Section formatting: stored `canonical_text` must preserve human-readable newlines. Bullet lists use one `- ` bullet per line; multi-paragraph sections preserve newline-separated paragraphs.
- Missing input behavior: use_unknown for unsupported required sections; block when required section keys are absent.
- Duplicate artifact behavior: more than one `Artifact(kind=product-brief)` is invalid memory state; semantic commands must fail instead of choosing one.
- Delete behavior: requires exact Product Brief `artifact_id` and matching `--confirm`; deletes the product-brief artifact and owned children only.

## Uses Memory

| Memory Dependency | Status | Contract / Owner | Command / Access | Required | Purpose | Missing / Stale Behavior |
| --- | --- | --- | --- | --- | --- | --- |
| `Brainstorm` | `current` | `ssd-brainstorming` | producer-owned memory handoff, memory recipe, or `ideas` command | `no` | Optional source material for Product Brief creation or edits. | skip when ideation declined or no memory object requested; block only if accepted ideation or user-requested memory loading cannot return usable memory. |
| `BrainstormIdea` | `current` | `ssd-brainstorming` | producer-owned memory handoff, memory recipe, or `ideas` command | `no` | Optional cited idea provenance for Product Brief content. | skip when ideation declined or no memory object requested; block only if accepted ideation or user-requested memory loading cannot return usable memory. |

## Non-Owned Boundaries

- `Brainstorm` and `BrainstormIdea` memory are read but not created or modified by product brief skills.
- When a user asks to include a stored memory object, product brief skills use `.opencode/shared/recipes.md` and the relevant memory recipe to discover browse and load commands.
- Generic current-state artifact shape is defined in `docs/memory.md`; this contract only defines Product Brief-specific section keys and commands.
- Product Brief skills do not write Product Brief markdown, temp markdown drafts, or downstream artifact memory.
- Raw Cypher is not used by these skills.

## Returned Memory References

| Output Field | Reference Type | Source Memory | Meaning |
| --- | --- | --- | --- |
| `artifact_id` | `id` | `Artifact` | UUID for the stable Product Brief root memory node. |
| `artifact_kind` | `kind` | `Artifact` | Product Brief artifact kind, `product-brief`. |
| `cited_brainstorm_ids` | `id` | `Brainstorm` | Optional brainstorm roots cited by the Product Brief. |
| `cited_idea_ids` | `id` | `BrainstormIdea` | Optional brainstorm ideas cited by the Product Brief. |
| `deleted` | `count` | Product Brief owned memory | Delete result with artifact ID, artifact kind, and total deleted node count. |

## Invariants

- Product Brief artifact kind is always `product-brief`.
- There must be zero or one `Artifact` with kind `product-brief`; multiple Product Brief artifacts are unsupported and treated as corrupt state.
- All created node IDs are UUIDs.
- All created graph nodes have non-empty human-facing titles.
- Consumers identify Product Brief through semantic commands and `artifact_kind=product-brief`, not by constructing IDs.
- Required section keys must all be present on create and update.
- Required section content must not present unsupported inference as fact.
- Required section content must not flatten bullet lists or paragraph breaks into one inline string.
- Product Brief skills return memory references, not markdown paths.
- Product Brief `get` returns cited brainstorm and idea IDs so downstream workflows can load source brainstorm memory.

## Gaps

| Gap | Affects | Status | Source | Notes |
| --- | --- | --- | --- | --- |
| None | `None` | `None` | `None` | None |
