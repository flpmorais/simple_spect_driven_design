# ssd-project-setup-status

## Summary

- Name: `ssd-project-setup-status`
- Description: Reads SSD setup memory status and identifies required setup work before planning continues.
- Source: `.opencode/skills/ssd-project-setup-status/SKILL.md`

## Purpose

Reports current SSD project setup state and explains required setup work before non-brainstorm planning continues.

## When To Use

Use when `ssd_planner` needs a read-only setup preflight before routing non-brainstorm planning work.

Do not use when the caller wants to create, update, delete, or infer durable memory, or when the caller is running brainstorming that can happen anytime.

## How It Is Used

The skill runs the setup status memory adapter once, summarizes whether setup is complete, incomplete, or blocked, and asks for user acceptance before any required setup skill runs.

## Inputs

- `scope`: optional. `auto` or `root`; defaults to `auto`.

## Outputs

- `status`: Setup status, `complete`, `incomplete`, or `blocked`.
- `scope`: Scope object returned by setup memory.
- `must_do`: Available setup actions that must be accepted before non-brainstorm planning continues.
- `available_next_steps`: Available setup branches returned by setup memory.
- `blocked_steps`: Setup steps blocked by missing prerequisites or unavailable implementation.

## Defaults

- Runs `.opencode/scripts/ssd_project_setup/memory.py status --scope auto` when no scope is supplied.
- Read-only; does not run the next setup skill.

## Paths

- Source skill: `.opencode/skills/ssd-project-setup-status/SKILL.md`.
- Memory adapter: `.opencode/scripts/ssd_project_setup/memory.py`.

## Memory

- Status: uses.
- Summary: Reads existing `Artifact` memory through the setup status adapter and returns setup state without creating or mutating memory.
- Memory contract: `docs/memory/ssd-project-setup-status.md`.

## Completion Criteria

Completes when setup status has been read and the user-facing setup summary or blocker has been returned.

Stops or blocks when setup memory returns `blocked` or the setup memory command fails.

## Invocation

Invoke with optional `scope`; omit it for the current root-only setup behavior.

Expected caller behavior: If setup is incomplete, stop and ask the user to accept the required setup skill before running it.

## Related Files

- Source skill: `.opencode/skills/ssd-project-setup-status/SKILL.md`.
- Related agent: `.opencode/agents/ssd_planner.md`.
- Memory contract: `docs/memory/ssd-project-setup-status.md`.

## Notes

- Brainstorming is not setup completion and remains allowed anytime.
- Required setup artifacts currently proceed from Product Brief to Product Blueprint to Architecture Blueprint.
