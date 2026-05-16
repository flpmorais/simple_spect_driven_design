# ssd_planner

## Summary

- Name: `ssd_planner`
- Description: Runs SSD planning workflows with setup preflight, memory-backed brainstorming, non-durable advanced elicitation, Product Brief flows, Product Blueprint creation, and Architecture Blueprint creation.
- Mode: all

## Purpose

Runs bounded SSD planning skills for this project. It runs `ssd-project-setup-status` before non-brainstorm planning, routes durable ideation and downstream idea-context work through `ssd-brainstorming`, routes pull-anytime critique or refinement through `ssd-advanced-elicitation`, routes Product Brief create/edit requests through the Product Brief skills, routes Product Blueprint creation through `ssd-product-blueprint-create`, and routes Architecture Blueprint creation through `ssd-architecture-blueprint-create`.

## When To Use

Use when a user or workflow asks to brainstorm, ideate, challenge assumptions, generate alternatives, create idea context for downstream SSD work, check required setup, apply advanced elicitation to refine current or recent content, create the first Product Brief, edit an existing Product Brief, create a Product Blueprint from Product Brief memory, or create an Architecture Blueprint to define expected architecture direction from Product Blueprint memory.

Do not use when the work requires BMad planning, story, development, review, refactor, deferred-work workflows, source code changes, tests, sprint status changes, planning tracker updates, kanban state changes, repository configuration changes, or commits.

## How It Is Used

Call this agent for one top-level planning skill run per invocation after setup preflight. It uses `ssd-project-setup-status` before non-brainstorm planning work. If setup is incomplete, it stops and asks for user acceptance before running the required setup skill. It uses `ssd-brainstorming` for memory-backed brainstorm creation, accepted idea appends, internal critique, finish, and memory handoff. It uses `ssd-advanced-elicitation` for non-durable refinement that returns enhanced content only. It uses `ssd-product-brief-create` for the first Product Brief, `ssd-product-brief-edit` for changes to an existing Product Brief, `ssd-product-blueprint-create` for Product Blueprint creation, and `ssd-architecture-blueprint-create` for Architecture Blueprint creation. It may run memory delete commands only when the user explicitly asks to delete the specific memory artifact.

## Inputs

- `planning_request`: required. A bounded SSD planning request for brainstorming, ideation, assumption-challenging, alternatives generation, downstream idea-context work, setup status, advanced elicitation, Product Brief create/edit work, Product Blueprint creation, or Architecture Blueprint creation.
- `target_content`: required for advanced elicitation unless current or recent content is obvious.

## Outputs

Returns a completion report with:

- `skill_run`: The skill that ran.
- For `ssd-project-setup-status`: setup status, must-do setup work, and whether user acceptance is required.
- For `ssd-brainstorming`: brainstorm ID, ideas captured, target ideas, and whether memory handoff was returned.
- For `ssd-advanced-elicitation`: methods used and enhanced content or concise summary.
- For Product Brief skills: artifact ID and whether the brief was created or updated.
- For Product Blueprint creation: artifact ID and whether the blueprint was created or skipped.
- For Architecture Blueprint creation: artifact ID and whether the blueprint was created or skipped.
- `blockers_or_user_decisions_required`: Blockers or user decisions required.

## Permissions

- `read`: allow
- `glob`: allow
- `grep`: allow
- `bash`: allow, for memory script commands
- `edit`: deny
- `task`: allow
- `todowrite`: allow
- `webfetch`: deny
- `websearch`: deny
- `lsp`: deny
- `skill`: allow only `ssd-project-setup-status`, `ssd-brainstorming`, `ssd-advanced-elicitation`, `ssd-product-brief-create`, `ssd-product-brief-edit`, `ssd-product-blueprint-create`, and `ssd-architecture-blueprint-create`; deny all other skills.

## Tools And Skills

Can read, glob, grep, use todos, run memory script commands, run `ssd-project-setup-status`, run `ssd-brainstorming`, run `ssd-advanced-elicitation`, run `ssd-product-brief-create`, run `ssd-product-brief-edit`, run `ssd-product-blueprint-create`, and run `ssd-architecture-blueprint-create`.

Cannot fetch or search the web, use LSP, edit files, run skills other than `ssd-project-setup-status`, `ssd-brainstorming`, `ssd-advanced-elicitation`, `ssd-product-brief-create`, `ssd-product-brief-edit`, `ssd-product-blueprint-create`, or `ssd-architecture-blueprint-create`, or modify `.agents/**`, `.opencode/**`, source code, tests, sprint status, planning trackers, kanban state, or repository configuration.

## Invocation

Invoke as a primary agent or subagent with the planning request and any target content needed for advanced elicitation, Product Brief work, Product Blueprint creation, or Architecture Blueprint creation. The setup preflight skill is `ssd-project-setup-status`. The allowed top-level planning skills are `ssd-brainstorming`, `ssd-advanced-elicitation`, `ssd-product-brief-create`, `ssd-product-brief-edit`, `ssd-product-blueprint-create`, and `ssd-architecture-blueprint-create`.

Expected response: completion report containing setup status when preflight ran, the skill run, brainstorming memory IDs and counts when brainstorming ran, elicitation methods and enhanced content when elicitation ran, Product Brief artifact ID when a Product Brief skill ran, Product Blueprint artifact ID when Blueprint creation ran, Architecture Blueprint artifact ID when Architecture Blueprint creation ran, and blockers or user decisions required.

## Related Files

- Source agent: `.opencode/agents/ssd_planner.md`.
- Related skill: `.opencode/skills/ssd-project-setup-status/SKILL.md`.
- Related skill: `.opencode/skills/ssd-brainstorming/SKILL.md`.
- Related skill: `.opencode/skills/ssd-advanced-elicitation/SKILL.md`.
- Related skill: `.opencode/skills/ssd-product-brief-create/SKILL.md`.
- Related skill: `.opencode/skills/ssd-product-brief-edit/SKILL.md`.
- Related skill: `.opencode/skills/ssd-product-blueprint-create/SKILL.md`.
- Related skill: `.opencode/skills/ssd-architecture-blueprint-create/SKILL.md`.
- Memory script: `.opencode/scripts/ssd_project_setup/memory.py`.
- Memory script: `.opencode/scripts/ssd_brainstorming/memory.py`.
- Memory script: `.opencode/scripts/ssd_product_brief/memory.py`.
- Memory script: `.opencode/scripts/ssd_product_blueprint/memory.py`.
- Memory script: `.opencode/scripts/ssd_architecture_blueprint/memory.py`.

## Notes

- Run `ssd-project-setup-status` before non-brainstorm planning work.
- If setup is incomplete, stop and ask for user acceptance before running required setup work.
- Run exactly one top-level skill per invocation after setup preflight.
- Brainstorming stores durable state in SSD memory.
- Advanced elicitation writes no files.
- Product Brief skills store durable state in SSD memory.
- Product Blueprint creation stores durable state in SSD memory.
- Architecture Blueprint creation stores durable state in SSD memory.
- Do not create raw Markdown brainstorm files.
- Do not run memory delete commands unless the user explicitly asks to delete the specific memory artifact.
- Do not commit changes.
