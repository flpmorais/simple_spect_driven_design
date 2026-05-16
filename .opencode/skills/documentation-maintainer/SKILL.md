---
name: documentation-maintainer
description: Maintain source-backed docs for skills, agents, commands, and per-unit memory contracts after source changes.
---

# documentation-maintainer

Use after creating or editing any skill, agent, or command. Builder agents should run this skill with the changed source path before finishing their work.

## Input

```json
{
  "source_path": "required explicit path to a skill, agent, or command",
  "change_summary": "optional short summary"
}
```

## Paths

- Skill template: `docs/templates/skill-template.md`
- Agent template: `docs/templates/agent-template.md`
- Command template: `docs/templates/command-template.md`
- Memory template: `docs/templates/memory-template.md`
- Skill docs: `docs/skills/<name>.md`
- Agent docs: `docs/agents/<name>.md`
- Command docs: `docs/commands/<name>.md`
- Memory docs: `docs/memory/<name>.md`
- Docs index: `docs/index.md`

## Workflow

1. Validate `source_path` is explicit and readable.
2. Infer type and name from path:
   - `.opencode/skills/<name>/SKILL.md` -> skill `<name>`.
   - `.opencode/agents/<name>.md` -> agent `<name>`.
   - command source path -> command `<name>`.
3. Read the matching template from `docs/templates/`.
4. Create or update the matching typed doc.
5. If the source creates, mutates, consumes, or changes memory behavior, create or update `docs/memory/<name>.md` from `docs/templates/memory-template.md`.
6. If the typed doc is new and missing from `docs/index.md`, add one row.
7. Return changed paths and warnings.

## Memory Documentation Rule

Update memory docs when the source mentions or changes memory commands, memory-backed state, memory IDs, graph nodes, graph relationships, or durable create/update/append/finalize/read behavior.

- Document created or mutated memory in detail.
- Document consumed memory only at dependency level.
- Do not restate shared memory schemas unless the source adds unit-specific rules.

## Hard Rules

- Do not edit the source skill, agent, or command.
- Do not edit `docs/memory.md`.
- Do not edit files under `docs/templates/`.
- Do not invent behavior not present in source.
- Do not deeply document memory this unit only consumes.
- Do not use the `ssd-` prefix for this skill.
- Do not commit changes.

## Result

Return:

```json
{
  "status": "complete|blocked|failed",
  "source_path": "<path>",
  "docs_changed": [],
  "memory_doc_changed": "<path or null>",
  "index_updated": "boolean",
  "warnings": []
}
```
