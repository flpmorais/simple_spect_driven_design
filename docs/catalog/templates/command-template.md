# Command Template

Template rules:

- Replace every `{{placeholder}}` with source-backed content.
- Preserve section order and headings.
- Use `None` only when the source explicitly has no value for a section.
- Use `Unknown` when the source should contain the value but does not.
- Keep descriptions factual. Do not infer hidden command behavior.

## Summary

- Name: `{{command_name}}`
- Description: {{one_sentence_description_from_command_source}}

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

## Related Files

- Source command: `{{source_command_path}}`.
- Related agent: `{{agent_path}}`.
- Related skill: `{{skill_path}}`.

## Notes

- {{important_constraint_or_boundary}}.
