# documentation-maintainer

## Summary

- Name: `documentation-maintainer`
- Description: Maintain source-backed docs for skills, agents, commands, and per-unit memory contracts after source changes.
- Source: `.opencode/skills/documentation-maintainer/SKILL.md`

## Purpose

Maintains documentation for changed skills, agents, and commands using the shared docs templates, and updates per-unit memory docs when memory behavior changes.

## When To Use

Use when a builder agent or user creates or edits a skill, agent, or command and the matching documentation needs to be created or refreshed.

Do not use when the task is only to inspect docs without updating them, edit source units, edit global memory design, or change documentation templates.

## How It Is Used

The caller passes one explicit source path. The skill infers the unit type and name, applies the matching template from `docs/templates/`, updates the typed doc, updates a memory doc only when memory behavior exists or changed, and adds an index row only when a new typed doc is missing from `docs/index.md`.

## Inputs

- `source_path`: Required. Explicit path to a changed skill, agent, or command.
- `change_summary`: Optional. Short summary of the source change.

## Outputs

- `status`: `complete`, `blocked`, or `failed`.
- `source_path`: Source path that was documented.
- `docs_changed`: Documentation paths created or updated.
- `memory_doc_changed`: Memory doc path, or null.
- `index_updated`: Boolean indicating whether `docs/index.md` changed.
- `warnings`: Warning list.

## Defaults

- Memory docs are updated only when source-backed memory behavior exists or changed.
- Consumed memory is documented only at dependency level.
- Created or mutated memory is documented in detail.

## Paths

- Skill template: `docs/templates/skill-template.md`.
- Agent template: `docs/templates/agent-template.md`.
- Command template: `docs/templates/command-template.md`.
- Memory template: `docs/templates/memory-template.md`.
- Skill docs: `docs/skills/<name>.md`.
- Agent docs: `docs/agents/<name>.md`.
- Command docs: `docs/commands/<name>.md`.
- Memory docs: `docs/memory/<name>.md`.
- Docs index: `docs/index.md`.

## Memory

- Status: none.
- Summary: This skill writes Markdown documentation files and does not use SSD memory.
- Memory contract: `None`.

## Completion Criteria

Completes when the typed doc is created or updated, any source-backed memory doc change is applied, required index updates are applied, and warnings are returned for unclear source behavior.

Stops or blocks when `source_path` is missing, unreadable, not explicit, or not recognized as a skill, agent, or command source path.

## Invocation

Invoke with `source_path` and optional `change_summary` after creating or editing any skill, agent, or command.

Expected caller behavior: Builder agents should run this skill before finishing source-unit changes and should review returned warnings.

## Related Files

- Source skill: `.opencode/skills/documentation-maintainer/SKILL.md`.
- Related agent: `None`.
- Related skill: `None`.
- Memory contract: `None`.

## Notes

- Do not edit source units, `docs/memory.md`, or files under `docs/templates/`.
