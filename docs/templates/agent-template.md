# Agent Template

Template rules:

- Replace every `{{placeholder}}` with source-backed content.
- Preserve section order and headings.
- Use `None` only when the source explicitly has no value for a section.
- Use `Unknown` when the source should contain the value but does not.
- Remove template rows that do not apply after replacing placeholders.
- Do not leave unresolved `{{placeholder}}` text in the final document.
- Copy names, paths, commands, modes, permissions, allowed skills, and output field names exactly from source.
- Keep descriptions factual; do not add capabilities not present in permissions or instructions.
- Keep paragraphs to one short paragraph; use bullets for lists.
- Preserve source order for inputs, outputs, permissions, tools, and related files unless the source is unordered.
- Document memory behavior only when the source mentions memory commands, memory-backed state, memory IDs, graph nodes, or graph relationships.

## Summary

- Name: `{{agent_name}}`
- Description: {{one_sentence_description_from_agent_frontmatter}}
- Mode: {{all|primary|subagent}}
- Source: `{{source_agent_path}}`

## Purpose

{{one_short_paragraph_explaining_the_agent_goal}}

## When To Use

Use when {{specific_review_research_or_execution_condition}}.

Do not use when {{known_out_of_scope_or_wrong_use_case}}.

## How It Is Used

{{one_short_paragraph_describing_how_callers_invoke_or_delegate_to_the_agent}}

## Inputs

- `{{input_name}}`: {{required_or_optional}}. {{meaning_and_expected_format}}.

## Outputs

Returns {{format_or_artifact_type}} with:

- `{{field_name}}`: {{field_meaning}}.

## Permissions

- `read`: {{allow_or_deny}}
- `glob`: {{allow_or_deny}}
- `grep`: {{allow_or_deny}}
- `bash`: {{allow_or_deny}}
- `edit`: {{allow_or_deny_and_scope}}
- `task`: {{allow_or_deny}}
- `todowrite`: {{allow_or_deny}}
- `webfetch`: {{allow_or_deny}}
- `websearch`: {{allow_or_deny}}
- `lsp`: {{allow_or_deny}}
- `skill`: {{allow_or_deny_and_scope}}

## Tools And Skills

Can {{allowed_tool_summary}}.

Cannot {{denied_tool_summary}}.

## Memory

- Status: {{none|uses|creates|updates|creates_and_uses|unknown}}.
- Summary: {{one_sentence_memory_behavior_or_none}}.
- Memory contract: `{{docs/memory/<agent_name>.md|None|Unknown}}`.

## Invocation

Invoke as {{primary_agent_or_subagent}} with {{minimum_required_context}}.

Expected response: {{response_contract_or_artifact}}.

## Related Files

- Source agent: `{{source_agent_path}}`.
- Related skill: `{{related_skill_name_or_path}}`.
- Target artifact: `{{target_artifact_path}}`.
- Memory contract: `{{memory_contract_path_or_None}}`.

## Notes

- {{important_constraint_or_boundary}}.
