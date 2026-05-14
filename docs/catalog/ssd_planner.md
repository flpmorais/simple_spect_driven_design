# ssd_planner

## Summary

- Name: `ssd_planner`
- Description: Runs SSD planning workflows, including durable brainstorming for downstream SSD skills.
- Mode: all

## Purpose

Runs bounded SSD planning skills for this project. Its current role is to route brainstorming, ideation, assumption-challenging, alternatives generation, and downstream idea-context work through `ssd-brainstorming`.

## When To Use

Use when a user or workflow asks to brainstorm, ideate, challenge assumptions, generate alternatives, or create idea context for downstream SSD work.

Do not use when the work requires BMad planning, story, development, review, refactor, deferred-work workflows, source code changes, tests, sprint status changes, planning tracker updates, kanban state changes, repository configuration changes, or commits.

## How It Is Used

Call this agent for one top-level planning skill run per invocation. It uses `ssd-brainstorming` for raw brainstorm creation, batch appends, batch critiques, and full raw review, then calls `ssd_distillator` through the `task` tool only after the raw brainstorm contains a `## Full Raw Review` section.

## Inputs

- `planning_request`: required. A bounded SSD planning request for brainstorming, ideation, assumption-challenging, alternatives generation, or downstream idea-context work.
- `raw_brainstorm_file_path`: required for distillation. An explicit raw brainstorm file path; folders and globs are not allowed.

## Outputs

Returns a completion report with:

- `skill_run`: The skill that ran.
- `raw_brainstorm_path`: The raw brainstorm file path.
- `final_distillate_path`: The final distillate path, if produced.
- `ideas_generated_and_target_ideas`: The ideas generated and target ideas.
- `audit_status_and_compression_ratio`: Audit status and compression ratio, if returned by `ssd_distillator`.
- `blockers_or_user_decisions_required`: Blockers or user decisions required.

## Permissions

- `read`: allow
- `glob`: allow
- `grep`: allow
- `bash`: deny
- `edit`: allow only under `._ssd_docs_temp/brainstorming/**`; deny all other paths.
- `task`: allow
- `todowrite`: allow
- `webfetch`: deny
- `websearch`: deny
- `lsp`: deny
- `skill`: allow only `ssd-brainstorming`; deny all other skills.

## Tools And Skills

Can read, glob, grep, use todos, edit raw brainstorm files under `._ssd_docs_temp/brainstorming/**`, run `ssd-brainstorming`, and call `ssd_distillator` through the `task` tool for final brainstorm distillates.

Cannot run bash, fetch or search the web, use LSP, edit outside `._ssd_docs_temp/brainstorming/**`, run skills other than `ssd-brainstorming`, write final distillates directly, or modify `._ssd_docs_distil/**`, `.agents/**`, `.opencode/**`, source code, tests, sprint status, planning trackers, kanban state, or repository configuration.

## Invocation

Invoke as a primary agent or subagent with the planning request and any required raw brainstorm file path. The only allowed top-level planning skill is `ssd-brainstorming`.

Expected response: completion report containing the skill run, raw brainstorm path, final distillate path if produced, ideas generated and target ideas, audit status and compression ratio if returned, and blockers or user decisions required.

## Related Files

- Source agent: `.opencode/agents/ssd_planner.md`.
- Related skill: `.opencode/skills/ssd-brainstorming/SKILL.md`.
- Target artifact: `._ssd_docs_temp/brainstorming/**`.
- Protected distillate area: `._ssd_docs_distil/**`.

## Notes

- Run exactly one top-level skill per invocation.
- Raw brainstorming files may be created or updated only under `._ssd_docs_temp/brainstorming/**`.
- Final brainstorm distillates must be produced by calling `ssd_distillator` through the `task` tool after the raw brainstorm contains a `## Full Raw Review` section.
- Do not call `ssd_distillator` with folders or globs; pass the explicit raw brainstorm file path only.
- Do not commit changes.
