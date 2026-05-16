# ssd-brainstorming Memory Contract

## Summary

- Unit: `ssd-brainstorming`
- Unit type: `skill`
- Source: `.opencode/skills/ssd-brainstorming/SKILL.md`
- Memory role: Creates non-versioned brainstorm metadata and sourceable accepted idea nodes, then exposes producer-owned read commands for listing and idea retrieval.
- Created memory contracts: `Brainstorm`, `BrainstormIdea`
- Used memory contracts: `Brainstorm`
- Memory script: `.opencode/scripts/ssd_brainstorming/memory.py`

## Creates Or Mutates

| Memory | Status | Action | Contract | Command / Step | Result |
| --- | --- | --- | --- | --- | --- |
| `Brainstorm` | `current` | `create` | `docs/memory/ssd-brainstorming.md` | `create` | Active brainstorm root node. |
| `Brainstorm` | `current` | `delete` | `docs/memory/ssd-brainstorming.md` | `delete --brainstorm-id <id> --confirm <id>` | Deletes the brainstorm root, child ideas, and attached relationships. |
| `Brainstorm` | `current` | `finalize` | `docs/memory/ssd-brainstorming.md` | `finish` | Status changes to `complete` or `complete_with_warnings`; `finished_at` is set. |
| `BrainstormIdea` | `current` | `append` | `docs/memory/ssd-brainstorming.md` | `append-ideas` | First-class accepted source idea nodes. |
| `BrainstormIdea` | `current` | `revise` | `docs/memory/ssd-brainstorming.md` | `revise-idea` | Creates a revised idea node for the same visible number and marks the prior version superseded. |

## Creation Details

| Created Memory | Input / Source | Stored As | Required | Rule |
| --- | --- | --- | --- | --- |
| `Brainstorm.constraints` | `constraints` input | `metadata` | `no` | Stored as JSON text; defaults to empty array. |
| `Brainstorm.downstream_consumer` | `downstream_consumer` input | `metadata` | `no` | Defaults to `general`. |
| `Brainstorm.goal` | `goal` input | `field` | `yes` | Required before memory creation. |
| `Brainstorm.id` | memory script | `field` | `yes` | UUID. |
| `Brainstorm.initial_context` | `initial_context` input | `field` | `no` | Defaults to empty string. |
| `Brainstorm.mode` | `mode` input | `metadata` | `no` | Defaults to `guided`. |
| `Brainstorm.scope` | `scope` input | `metadata` | `no` | Defaults to `normal`. |
| `Brainstorm.status` | workflow state | `field` | `yes` | Starts as `active`; finish sets `complete` or `complete_with_warnings`. |
| `Brainstorm.target_ideas` | scope resolution | `metadata` | `yes` | `quick=20`, `normal=50`, `deep=100` unless caller overrides through skill logic. |
| `Brainstorm.techniques` | selector output | `metadata` | `no` | Stored as JSON text; defaults to empty array. |
| `Brainstorm.title` | `topic` input | `field` | `yes` | Human-facing graph title; matches `topic`. |
| `Brainstorm.topic` | `topic` input | `field` | `yes` | Required before memory creation. |
| `BrainstormIdea` | accepted idea batch JSON | `node` | `yes` | Requires title, concept, rationale, hidden assumption, risk, domain, and positive idea number. Title is the human-facing graph title. JSON is internal persistence data, not user-facing output. Initial append sets `revision=1`, `revision_of=""`, and `superseded=false`. |
| `BrainstormIdea.revision` | `append-ideas` or `revise-idea` | `field` | `yes` | Starts at `1`; increments when a visible idea number is revised. |
| `BrainstormIdea.revision_of` | `revise-idea` | `field` | `no` | Points to the first idea node in the revision chain. Empty for original versions. |
| `BrainstormIdea.superseded` | `revise-idea` | `field` | `yes` | Current versions are `false`; prior revised versions are `true`. |

## Creation Rules

- Idempotency: appends new; revisions create a new node and supersede the prior current node
- Versioning: not_versioned
- Mutability: append_and_revise_until_finish; immutable_after_finish
- Evidence requirement: inherited
- Missing input behavior: block in `internal` mode; ask user in `interactive` mode
- Stale memory behavior: none
- Delete behavior: requires exact `--brainstorm-id` and matching `--confirm`; deletes brainstorm root, child ideas, and attached relationships only

## Uses Memory

| Memory Dependency | Status | Contract / Owner | Command / Access | Required | Purpose | Missing / Stale Behavior |
| --- | --- | --- | --- | --- | --- | --- |
| `Brainstorm` | `current` | `ssd-brainstorming` | `list` | `no` | Returns brainstorm summaries for browsing and navigation. | empty list |
| `Brainstorm` | `current` | `ssd-brainstorming` | `ideas` | `yes` | Producer-owned handoff returns brainstorm metadata and latest non-superseded ideas to consumers. | block |

Continuation rule: when resuming a brainstorm without an explicit ID, the skill must use `list` to find unfinished brainstorms, select automatically only when one candidate is unambiguous, then use `ideas` to load the selected brainstorm before asking new prompts. UUIDs are internal handles and should not be the first user-facing selection mechanism.

## Non-Owned Boundaries

- Critique is an internal capture-improvement process and is not stored in memory.
- Product brief memory is not created or modified by this skill.
- Product blueprint memory is not created or modified by this skill.
- Generic versioned artifact memory is defined in `docs/memory.md` and is not used for brainstorm runs.
- Raw Cypher is not used by this skill.

## Returned Memory References

| Output Field | Reference Type | Source Memory | Meaning |
| --- | --- | --- | --- |
| `brainstorm_id` | `id` | `Brainstorm` | Root brainstorm memory node ID. |
| `deleted` | `count` | `Brainstorm`, `BrainstormIdea` | Delete result with deleted brainstorm, idea, and total node counts. |
| `ideas_captured` | `count` | `BrainstormIdea` | Number of accepted idea nodes created. |
| `memory_handoff` | `command` | `Brainstorm` and `BrainstormIdea` | Producer-owned command for retrieving brainstorm metadata and ideas. |
| `brainstorms` | `list` | `Brainstorm` | Read-only summary list returned by `list`. |
| `target_ideas` | `count` | `Brainstorm` | Scope threshold used for completion status. |
| `revised_idea_id` | `id` | `BrainstormIdea` | New current idea node created by `revise-idea`. |
| `superseded_idea_id` | `id` | `BrainstormIdea` | Prior idea node marked superseded by `revise-idea`. |

## Invariants

- Brainstorm IDs are UUIDs.
- Brainstorm and BrainstormIdea nodes have non-empty human-facing titles.
- Brainstorms are not versioned.
- Brainstorm ideas are first-class accepted source nodes.
- A brainstorm must be `active` before ideas can be appended, revised, or before it can be finished.
- Current idea retrieval excludes superseded revisions by default; `--include-superseded` returns revision history.
- Finish only changes brainstorm status and `finished_at`.
- Finished brainstorms are immutable.
- Delete is an explicit operator action and may remove finished brainstorms when directly requested.
- Critiques and reviews are not stored.
- Consumers must execute `memory_handoff.command` instead of hardcoding brainstorm retrieval.
- The skill returns memory IDs and handoff commands, not Markdown paths.

## Gaps

| Gap | Affects | Status | Source | Notes |
| --- | --- | --- | --- | --- |
| None | `None` | `None` | `None` | None |
