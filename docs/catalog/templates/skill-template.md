# Skill Template

Template rules:

- Replace every `{{placeholder}}` with source-backed content.
- Preserve section order and headings.
- Use `None` only when the source explicitly has no value for a section.
- Use `Unknown` when the source should contain the value but does not.
- Keep descriptions factual. Do not add marketing copy or inferred behavior.

## Summary

- Name: `{{skill_name}}`
- Description: {{one_sentence_description_from_skill_frontmatter}}

## Purpose

{{one_short_paragraph_explaining_the_skill_goal}}

## When To Use

Use when {{specific_user_intent_or_workflow_condition}}.

Do not use when {{known_out_of_scope_or_wrong_use_case}}.

## How It Is Used

{{one_short_paragraph_describing_the_execution_flow}}

## Inputs

- `{{input_name}}`: {{required_or_optional}}. {{meaning_and_expected_format}}.

## Outputs

- `{{output_name}}`: {{meaning_and_path_or_return_shape}}.

## Defaults

- {{default_behavior_or_mode}}.

## Paths

- {{path_label}}: `{{path}}`.

## Completion Criteria

Completes when {{observable_success_condition}}.

Stops or blocks when {{observable_stop_or_block_condition}}.

## Invocation

Invoke with {{minimum_required_arguments_or_context}}.

Expected caller behavior: {{what_the_caller_should_expect_or_do_next}}.

## Related Files

- Source skill: `{{source_skill_path}}`.
- Related agent: `{{agent_path}}`.
- Related skill: `{{related_skill_name_or_path}}`.

## Notes

- {{important_constraint_or_boundary}}.
