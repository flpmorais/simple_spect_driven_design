# ssd_elicitation_selector

## Summary

- Name: `ssd_elicitation_selector`
- Description: Selects SSD advanced elicitation methods from the preserved BMAD-derived catalogue.
- Mode: subagent

## Purpose

Selects one or more advanced elicitation methods for `ssd-advanced-elicitation` internal mode. It preserves catalogue method fields and returns only compact JSON.

## When To Use

Use when `ssd-advanced-elicitation` runs in internal mode without exact caller-provided methods.

Do not use to execute elicitation, rewrite methods, or produce enhanced content.

## How It Is Used

The agent reads `.opencode/skills/ssd-advanced-elicitation/methods.md`, resolves exact preselected methods first, then selects missing methods based on target content, goal, context, constraints, risk level, stakeholder needs, and creative potential.

## Inputs

- `target_content`: Required. Content to improve.
- `goal`: Optional refinement goal.
- `initial_context`: Optional supporting context.
- `constraints`: Optional constraints.
- `required_methods`: Optional integer. Defaults to `1`.
- `preselected_methods`: Optional exact method names with optional caller purpose.

## Outputs

- `status`: `complete` or `needs_input`.
- `methods`: Selected methods with preserved `category`, `method_name`, `description`, and `output_pattern`, plus optional `caller_purpose`.
- `warnings`: Warning list.

## Permissions

- `read`: allow
- `glob`: allow
- `grep`: allow
- `bash`: deny
- `edit`: deny
- `task`: deny
- `todowrite`: deny
- `webfetch`: deny
- `websearch`: deny
- `lsp`: deny
- `skill`: deny

## Invocation

Invoke from `ssd-advanced-elicitation` internal mode when exact caller-provided methods are absent or insufficient.

Expected response: compact JSON containing only selected methods, preserving catalogue fields exactly.

## Related Files

- Source agent: `.opencode/agents/ssd_elicitation_selector.md`.
- Related skill: `.opencode/skills/ssd-advanced-elicitation/SKILL.md`.
- Method catalogue: `.opencode/skills/ssd-advanced-elicitation/methods.md`.

## Notes

- The selector does not execute elicitation.
- The selector does not write files.
- The selector does not add `covers`, `action`, aliases, tags, or normalized names.
