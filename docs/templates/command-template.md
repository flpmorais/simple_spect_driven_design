# Command Template

Template rules:

- Replace every `{{placeholder}}` with source-backed content.
- Preserve section order and headings.
- Use `None` only when the source explicitly has no value for a section.
- Use `Unknown` when the source should contain the value but does not.
- Remove template rows that do not apply after replacing placeholders.
- Do not leave unresolved `{{placeholder}}` text in the final document.
- Copy names, paths, commands, arguments, delegated agents/skills, and output field names exactly from source.
- Keep descriptions factual; do not infer hidden command behavior.
- Keep paragraphs to one short paragraph; use bullets for lists.
- Preserve source order for inputs, outputs, invocation details, and delegated agents/skills unless the source is unordered.
- Document memory behavior only when the source mentions memory commands, memory-backed state, memory IDs, graph nodes, or graph relationships.

## Summary

- Name: `{{command_name}}`
- Description: {{one_sentence_description_from_command_source}}
- Source: `{{source_command_path}}`

## Purpose

{{one_short_paragraph_explaining_the_command_goal}}

## When To Use

Use when {{specific_user_intent_or_workflow_condition}}.

Do not use when {{known_out_of_scope_or_wrong_use_case}}.

## How It Is Used

{{one_short_paragraph_describing_what_the_command_runs_or_delegates_to}}

## Inputs

- `{{input_name}}`: {{required_or_optional}}. {{meaning_and_expected_format}}.

## Outputs

- `{{output_name}}`: {{meaning_and_path_or_return_shape}}.

## Invocation

Run `{{command_invocation}}` with {{minimum_required_arguments_or_context}}.

Expected result: {{observable_result_or_next_action}}.

## Agent Or Skill Used

- {{agent_or_skill_name}}: {{how_the_command_uses_it}}.

## Memory

- Status: {{none|uses|creates|updates|creates_and_uses|unknown}}.
- Summary: {{one_sentence_memory_behavior_or_none}}.
- Memory contract: `{{docs/memory/<command_name>.md|None|Unknown}}`.

## Related Files

- Source command: `{{source_command_path}}`.
- Related agent: `{{agent_path}}`.
- Related skill: `{{skill_path}}`.
- Memory contract: `{{memory_contract_path_or_None}}`.

## Notes

- {{important_constraint_or_boundary}}.
