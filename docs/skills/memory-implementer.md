# memory-implementer

## Summary

- Name: `memory-implementer`
- Description: Implement SSD memory scripts and adapters with real tests under tests/memory.
- Source: `.opencode/skills/memory-implementer/SKILL.md`

## Purpose

Implements changes to SSD memory scripts, shared memory helpers, and unit-specific memory adapters while requiring real behavior tests and passing memory test results.

## When To Use

Use when generic memory commands, shared memory kernel helpers, or unit-specific memory adapters need to be created or changed.

Do not use when the task is only to edit documentation, catalog pages, source skills, source agents, source commands, templates, or non-memory code.

## How It Is Used

The caller provides a memory behavior request and scope. The skill reads current implementation, tests, and memory contracts for context, writes or updates real tests under `tests/memory/`, implements the smallest memory code change, and runs the memory test suite until it passes.

## Inputs

- `request`: Required. Memory behavior change to implement.
- `scope`: Required. `generic` for `.opencode/scripts/ssd_memory/*` or `adapter` for `.opencode/scripts/<unit>/memory.py`.
- `unit`: Required when `scope=adapter`. Unit adapter name/path segment.

## Outputs

- `status`: `complete`, `blocked`, or `failed`.
- `changed_files`: Files changed by the skill.
- `tests`: Test command and pass/fail/not-run status.
- `warnings`: Warning list, including documentation-maintainer follow-up when behavior changed.

## Defaults

- Test command is `python -m pytest tests/memory`.
- Bug fixes should add or adjust a failing test first when feasible.
- Adapters stay thin; reusable storage helpers belong in `kernel.py` only when genuinely shared.

## Paths

- Generic memory script: `.opencode/scripts/ssd_memory/memory.py`.
- Shared memory kernel: `.opencode/scripts/ssd_memory/kernel.py`.
- Adapter scripts: `.opencode/scripts/<unit>/memory.py`.
- Memory tests: `tests/memory/`.
- Memory design reference: `docs/memory.md`.
- Unit memory contracts: `docs/memory/<unit>.md`.

## Memory

- Status: none.
- Summary: This skill changes memory implementation files and tests; it does not read or write SSD memory as durable workflow state.
- Memory contract: `None`.

## Completion Criteria

Completes when the requested memory behavior is implemented, real tests cover the behavior under `tests/memory/`, and `python -m pytest tests/memory` passes.

Stops or blocks when the request is ambiguous, adapter scope omits `unit`, required implementation files are missing without clear creation intent, or the memory tests cannot be made to pass.

## Invocation

Invoke with a memory behavior request, `scope`, and `unit` for adapter work.

Expected caller behavior: Run `documentation-maintainer` afterward when memory behavior changed and docs need to reflect the new contract.

## Related Files

- Source skill: `.opencode/skills/memory-implementer/SKILL.md`.
- Related agent: `None`.
- Related skill: `documentation-maintainer`.
- Memory contract: `None`.

## Notes

- Tests must not be stubs, import-only checks, placeholder assertions, broad skips, or unjustified xfails.
- Do not edit docs, source units, templates, or `docs/index.md`.
