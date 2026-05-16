# Brainstorm Recipe

Artifact: `brainstorm`
Owner: `ssd-brainstorming`
Memory adapter: `.opencode/scripts/ssd_brainstorming/memory.py`

## Browse

Use when the user asks to use/continue/resume a brainstorm without an ID. Do not ask for a UUID first; IDs are internal handles.

```text
python .opencode/scripts/ssd_brainstorming/memory.py list
```

Returns brainstorm summaries: `id`, `title`, `topic`, `goal`, `scope`, `target_ideas`, `mode`, `downstream_consumer`, `status`, `created_at`, `finished_at`.

Selection rules:

- If the user gives an ID, skip browse and load it.
- For continue/resume, prefer unfinished brainstorms (`status=active` or empty `finished_at`).
- If one unfinished candidate matches, load it and tell the user which was selected.
- Use topic/domain/description/latest to narrow in working context.
- If multiple candidates match, show concise numbered options and ask for number/title/topic; do not require UUID.
- If none match, say so and ask whether to continue without it or run brainstorming.

## Load

Use after selecting a brainstorm ID.

```text
python .opencode/scripts/ssd_brainstorming/memory.py get --brainstorm-id <brainstorm_id>
```

Alias:

```text
python .opencode/scripts/ssd_brainstorming/memory.py ideas --brainstorm-id <brainstorm_id>
```

Returns metadata and current non-superseded `ideas`. For continuation, use metadata, techniques, ideas, target count, and scope before asking new prompts.

Use returned `brainstorm.id` as `cited_brainstorm_ids`; use idea `id` values as `cited_idea_ids` when specific ideas inform downstream content.

## Delete

Use only when the user explicitly asks to delete a brainstorm.

```text
python .opencode/scripts/ssd_brainstorming/memory.py delete --brainstorm-id <brainstorm_id> --confirm <brainstorm_id>
```

Deletes the selected `Brainstorm`, its `BrainstormIdea` children, and attached relationships. Does not delete downstream artifacts that cited them. Requires exact `--confirm` match.
