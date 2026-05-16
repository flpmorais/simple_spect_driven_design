# Unit Memory Contract Template

Template rules:

- Replace every `{{placeholder}}` with source-backed content.
- Preserve section order and headings.
- Use `None` only when explicitly not applicable.
- Use `Unknown` when expected but undocumented.
- This document is unit-scoped: detail what this skill, agent, or command creates or mutates.
- For memory this unit only reads, document dependency-level usage only; do not repeat another unit's memory shape.
- Do not restate shared memory schemas unless this unit adds unit-specific fields, rules, or constraints.
- Use source-backed memory names and contract references instead of closed domain enums.
- Mark behavior as `current`, `planned`, or `proposed`.
- Use `proposed` only for source-backed gaps or explicitly requested future memory.
- Sort rows alphabetically by memory name unless lifecycle order is required.
- Keep node labels in `PascalCase`, relationship types in `UPPER_SNAKE_CASE`, properties in `snake_case`, and node IDs as opaque UUIDs. Document type, kind, and lookup semantics as properties, not encoded IDs.
- Keep commands semantic; raw Cypher belongs only in admin/debug rows.
- Do not add inferred durable facts without evidence.

## Summary

- Unit: `{{unit_name}}`
- Unit type: `{{skill|agent|command}}`
- Source: `{{source_path}}`
- Memory role: {{short_statement_of_create_update_read_behavior}}
- Created memory contracts: {{contract_refs_or_none}}
- Used memory contracts: {{contract_refs_or_none}}
- Memory script: `.opencode/scripts/ssd_memory/memory.py`

## Creates Or Mutates

| Memory | Status | Action | Contract | Command / Step | Result |
| --- | --- | --- | --- | --- | --- |
| `{{memory_object_or_context}}` | `{{current|planned|proposed}}` | `{{create|update|append|finalize|derive|return-reference}}` | `{{contract_ref}}` | `{{command_or_workflow_step}}` | {{created_state_or_reference}} |

## Creation Details

| Created Memory | Input / Source | Stored As | Required | Rule |
| --- | --- | --- | --- | --- |
| `{{memory_object_or_context}}` | `{{input_name_or_workflow_output}}` | `{{field|section|node|relationship|metadata}}` | `{{yes|no}}` | {{normalization_validation_default_or_evidence_rule}} |

## Creation Rules

- Idempotency: {{fails_if_exists|updates_existing|appends_new|creates_duplicate|unknown|none}}
- Mutability: {{updates_current|append_only|immutable_after_create|none|unknown}}
- Mutability: {{mutable|immutable_after_create|append_only_until_finish|immutable_after_finish|none|unknown}}
- Evidence requirement: {{required|inherited|not_required|unknown}}
- Missing input behavior: {{block|ask_user|use_unknown|skip|warn|unknown}}
- Stale memory behavior: {{reject|regenerate|warn|ignore|unknown|none}}

## Uses Memory

| Memory Dependency | Status | Contract / Owner | Command / Access | Required | Purpose | Missing / Stale Behavior |
| --- | --- | --- | --- | --- | --- | --- |
| `{{memory_object_or_context}}` | `{{current|planned|proposed}}` | `{{contract_ref_or_owner}}` | `{{command_or_access_pattern}}` | `{{yes|no}}` | {{why_it_is_used}} | {{block|warn|skip|regenerate|unknown}} |

## Non-Owned Boundaries

- {{memory_this_unit_reads_but_must_not_create_or_modify}}
- {{memory_schema_defined_elsewhere_and_not_repeated_here}}
- {{forbidden_memory_command_or_write}}

## Returned Memory References

| Output Field | Reference Type | Source Memory | Meaning |
| --- | --- | --- | --- |
| `{{output_field}}` | `{{id|kind|count|none}}` | `{{memory_object_or_context}}` | {{meaning; id values are UUIDs when returned}} |

## Invariants

- {{unit_scoped_memory_invariant}}

## Gaps

| Gap | Affects | Status | Source | Notes |
| --- | --- | --- | --- | --- |
| {{gap_or_none}} | `{{creates|uses|boundaries|outputs|rules|None}}` | `{{planned|proposed|None}}` | `{{source_ref_or_none}}` | {{notes_or_none}} |
