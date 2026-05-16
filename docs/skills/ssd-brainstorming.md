# ssd-brainstorming

## Summary

- Name: `ssd-brainstorming`
- Description: Durable SSD brainstorming with facilitated, memory-backed idea capture and producer-owned memory handoff.
- Source: `.opencode/skills/ssd-brainstorming/SKILL.md`

## Purpose

Facilitates user-led ideation, alternatives, assumption challenge, and downstream idea context while storing accepted ideas in SSD memory.

## When To Use

Use when ideation needs durable, sourceable ideas. Do not use to modify source code, tests, repo config, downstream artifacts, or raw Markdown brainstorm files.

## How It Is Used

The skill gathers inputs, resolves techniques through `ssd_technique_selector`, facilitates prompts, presents grounded candidate batches, appends accepted ideas, critiques internally between batches, performs final revision review, finishes memory, and returns a producer-owned handoff.

It is a facilitator, not an autonomous idea generator. It stores only user input, user edits, user-approved AI suggestions, or accepted synthesis. Raw idea JSON is internal only.

On continuation, it lists unfinished brainstorms before asking for identifiers, lets the user choose by number/title/topic when needed, loads existing ideas, and resumes with that context.

## Inputs

- `run_mode`: optional, `interactive` or `internal`.
- `topic`: required unless obvious.
- `goal`: required unless obvious.
- `initial_context`: optional.
- `scope`: optional, `quick|normal|deep`.
- `target_folder`: ignored legacy field.
- `downstream_consumer`: optional.
- `constraints`: optional array.
- `mode`: optional, `guided|adversarial|progressive|random-catalyst`.
- `required_techniques`: optional integer.
- `excluded_techniques`: optional technique names.
- `techniques`: optional preselected `{name, purpose}` objects.

## Outputs

- `status`: `complete|complete_with_warnings|blocked|failed`.
- `brainstorm_id`: brainstorm memory ID.
- `ideas_captured`: accepted idea count.
- `target_ideas`: scope threshold.
- `scope`: selected scope.
- `downstream_consumer`: consumer or `general`.
- `memory_handoff`: command object for retrieving metadata and ideas.
- `warnings`: warning list.

## Defaults

- `run_mode=interactive`.
- `scope=normal`.
- `downstream_consumer=general`.
- `mode=guided`.
- Technique counts default to `quick=2`, `normal=3`, `deep=5`.

## Paths

- Memory script: `.opencode/scripts/ssd_brainstorming/memory.py`.
- Source skill: `.opencode/skills/ssd-brainstorming/SKILL.md`.

## Continuation Behavior

- On resume/continue, run `list` before asking for IDs.
- Prefer unfinished brainstorms: `status=active` or empty `finished_at`.
- Load one unambiguous candidate automatically; otherwise show numbered candidates and ask for number/title/topic.
- After selection, run `ideas --brainstorm-id <id>` and use existing ideas, techniques, scope, target, and goal before prompting.
- Do not create a new brainstorm unless the user explicitly starts over.

## Memory

- Status: creates_and_uses.
- Summary: Creates a non-versioned `Brainstorm`, appends/revises `BrainstormIdea` nodes, marks the brainstorm complete, and returns `memory_handoff`.
- Memory contract: `docs/memory/ssd-brainstorming.md`.

## Completion Criteria

Completes when the user/caller requests finish, proceed, synthesis, or stop after accepted capture and final revision review. Completion is `complete` at/above threshold and `complete_with_warnings` below threshold.

Stops or blocks when required inputs are missing in `internal`, selector blocks, memory commands fail, or an external limit prevents continuation.

## Invocation

Invoke with `topic` and `goal` unless obvious, plus optional context, scope, consumer, constraints, mode, technique count, and techniques.

In `interactive`, caller/user confirms or modifies technique selection. In `internal`, selection is automatic but execution remains interactive and user-led.

## Related Files

- Source skill: `.opencode/skills/ssd-brainstorming/SKILL.md`.
- Related agent: `.opencode/agents/ssd_technique_selector.md`.
- Memory contract: `docs/memory/ssd-brainstorming.md`.

## Notes

- Scope thresholds are `quick=20`, `normal=50`, `deep=100`; they are targets, not filler quotas.
- Candidate batches include next prompts; answering those prompts accepts the batch unless the user corrects/rejects/holds it first.
- Captured ideas are first-class memory nodes and can be revised with `revise-idea`; current retrieval excludes superseded versions.
- Final review checks contradictions, duplicates, vague entries, superseded versions, and drift unless explicitly skipped.
- Critique is internal only and not stored or returned.
- Consumers must use `memory_handoff.command`, not hardcoded retrieval.
- Do not create raw Markdown brainstorm files.
