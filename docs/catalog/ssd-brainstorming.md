# ssd-brainstorming

## Summary

- Name: `ssd-brainstorming`
- Description: Durable SSD brainstorming with raw capture, critique, review, and final distillation.

## Purpose

Supports ideation, alternatives, assumption challenge, and downstream context by preserving raw ideas, critiquing batches, reviewing the full session, and then invoking `ssd_distillator` for the final distillate.

## When To Use

Use when ideation, alternatives, assumption challenge, or downstream context need structured brainstorming with raw capture and final distillation.

Do not use when the task is to modify source code, tests, repo config, unrelated workflow artifacts, or final distillates directly.

## How It Is Used

The skill gathers required inputs, resolves techniques with `ssd_technique_selector`, writes a raw brainstorming file, captures self-contained ideas in batches, appends batch critiques, performs a full raw review when finishing, and calls `ssd_distillator` with one explicit raw file path.

## Inputs

- `run_mode`: Optional. `interactive` or `internal`.
- `topic`: Required unless obvious. Brainstorming topic.
- `goal`: Required unless obvious. Brainstorming goal.
- `initial_context`: Optional. Seed context or user brain dump.
- `scope`: Optional. `quick`, `normal`, or `deep`.
- `target_folder`: Optional. Subfolder under `brainstorming/`.
- `downstream_consumer`: Optional. Consumer skill or workflow.
- `constraints`: Optional. List of constraints.
- `mode`: Optional. `guided`, `adversarial`, `progressive`, or `random-catalyst`.
- `required_techniques`: Optional. Integer technique count.
- `techniques`: Optional. Preselected technique objects with `name` and `purpose`; purpose is preserved and applied as the run-specific focus for that technique.

## Outputs

- `status`: `complete`, `complete_with_warnings`, `blocked`, or `failed`.
- `raw_brainstorm`: Raw file path under `._ssd_docs_temp/brainstorming/<target_folder>/<filename>`.
- `distillate`: Final distillate path under `._ssd_docs_distil/brainstorming/<target_folder>/<filename>`.
- `ideas_generated`: Number of ideas generated.
- `target_ideas`: Scope threshold used for completion status.
- `scope`: Selected scope.
- `target_folder`: Selected target folder.
- `downstream_consumer`: Selected downstream consumer or `general`.
- `completion_reason`: Reason completion occurred.
- `warnings`: Warning list.

## Defaults

- `run_mode=interactive`.
- `scope=normal`.
- `target_folder=general`.
- `downstream_consumer=general`.
- `mode=guided`.
- Default technique counts are `quick=2`, `normal=3`, and `deep=5` when `required_techniques` is omitted.

## Paths

- Filename: `brainstorm-<yyyy-mm-dd-hh-mm>-<shorttopic>.md`.
- Raw file: `._ssd_docs_temp/brainstorming/<target_folder>/<filename>`.
- Final distillate: `._ssd_docs_distil/brainstorming/<target_folder>/<filename>`.
- `shorttopic`: Lowercase ASCII slug; use a neutral slug for sensitive or awkward topics.
- `target_folder` is treated as a subfolder name, not an arbitrary path.

## Completion Criteria

Completes when the user or invoking skill requests finish, proceed, synthesis, or stop after raw capture and `## Full Raw Review` exists before distillation. Completion is `complete` at or above the scope threshold and `complete_with_warnings` below threshold.

Stops or blocks when required inputs are missing in `internal` mode, `ssd_technique_selector` returns `blocked`, or an external limit or failure prevents continuing.

## Invocation

Invoke with `topic` and `goal` unless obvious, plus optional `initial_context`, `scope`, `target_folder`, `downstream_consumer`, `constraints`, `mode`, `required_techniques`, and `techniques`.

Expected caller behavior: In `interactive` mode, provide missing required fields when asked. In `internal` mode, expect a concise blocker if required inputs are missing; otherwise expect structured output with raw and distillate paths.

## Related Files

- Source skill: `.opencode/skills/ssd-brainstorming/SKILL.md`
- Related agent: `.opencode/agents/ssd_technique_selector.md`.
- Related agent: `.opencode/agents/ssd_distillator.md`.
- Related skill: None.
- Raw brainstorming output: `._ssd_docs_temp/brainstorming/<target_folder>/<filename>`.
- Final distillate output: `._ssd_docs_distil/brainstorming/<target_folder>/<filename>`.

## Notes

- Scope thresholds are `quick=20`, `normal=50`, and `deep=100` ideas; thresholds are enough-to-proceed targets, not hard caps.
- Each idea must be self-contained and every 10 ideas must include a batch critique.
- Caller-provided technique purposes are execution instructions, not display-only metadata.
- Distillation must not happen until `## Full Raw Review` exists in the raw file.
- The skill must not hand-write final distillates or pass a folder or glob to `ssd_distillator`.
