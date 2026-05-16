---
name: memory-implementer
description: Implement SSD memory scripts and adapters with real tests under tests/memory.
---

# memory-implementer

Use when changing SSD memory implementation: generic memory commands, shared memory helpers, or unit-specific memory adapters.

## Input

```json
{
  "request": "required memory behavior change",
  "scope": "generic|adapter",
  "unit": "required when scope=adapter"
}
```

## Read First

- Always read `.opencode/scripts/ssd_memory/kernel.py`.
- Always read `.opencode/scripts/ssd_memory/memory.py`.
- Always read relevant files under `tests/memory/`.
- Read `docs/memory.md` for contract context only.
- For adapter scope, also read `.opencode/scripts/<unit>/memory.py` and `docs/memory/<unit>.md` when present.

## Edit Scope

- `.opencode/scripts/ssd_memory/kernel.py`
- `.opencode/scripts/ssd_memory/memory.py`
- `.opencode/scripts/<unit>/memory.py`
- `tests/memory/**`

## Workflow

1. State the expected behavior in concise acceptance bullets.
2. For bug fixes, add or adjust a failing test first when feasible.
3. Write real tests under `tests/memory/`.
4. Implement the smallest code change.
5. Run `python -m pytest tests/memory`.
6. Fix code or tests until all memory tests pass.
7. Return changed files, test command, test result, and documentation warning if behavior changed.

## Implementation Boundaries

- `kernel.py` contains shared ID, time, file, JSON, and GraphQLite helpers only.
- `ssd_memory/memory.py` contains generic current artifact and graph semantic commands.
- `.opencode/scripts/<unit>/memory.py` contains unit adapter commands and validation.
- Keep adapters thin; move reusable storage helpers to `kernel.py` only when they are genuinely shared.
- Preserve JSON CLI contracts.
- Use semantic commands; raw Cypher is only for admin/debug paths.

## Test Rules

- Tests must assert real behavior, not imports or placeholders.
- Tests must use temp DB isolation and must not mock GraphQLite away.
- Cover success and failure paths for every new command or validation rule.
- Assert returned JSON, IDs, graph state, validation errors, or mutability behavior as applicable.
- Do not weaken existing tests.
- Do not add stub tests, trivial assertions, broad skips, or unjustified xfails.
- Do not finish unless `python -m pytest tests/memory` passes.

## Hard Rules

- Do not edit docs; use `documentation-maintainer` after behavior changes.
- Do not edit source skills, agents, commands, catalog docs, memory docs, templates, or `docs/index.md`.
- Do not broaden scope beyond the requested memory behavior.
- Do not commit changes.

## Result

Return:

```json
{
  "status": "complete|blocked|failed",
  "changed_files": [],
  "tests": {
    "command": "python -m pytest tests/memory",
    "status": "passed|failed|not_run"
  },
  "warnings": []
}
```
