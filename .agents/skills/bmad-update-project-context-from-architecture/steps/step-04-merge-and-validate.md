# Step 4: Merge And Validate Project Context

## Rules

- Speak in `{communication_language}`.
- Only modify `_bmad-output/project-context.md`.
- Keep the final file under 300 lines.
- Preserve useful existing rules unless explicitly replaced or removed.

## Merge Rules

Apply the approved changes to `_bmad-output/project-context.md`:

- Add concise durable rules in the most relevant existing section.
- Merge related rules instead of adding duplicates.
- Replace existing rules only when approved and backed by explicit architecture evidence or user decision.
- Remove existing rules only when approved and backed by explicit architecture evidence or user decision.
- Preserve existing stack/rule mentions when `architecture.md` is silent about them.
- Keep wording specific, actionable, and optimized for agents.

## Frontmatter Updates

Update frontmatter:

- `date` to current date.
- `status: 'complete'`.
- `optimized_for_llm: true`.
- `rule_count` to the current number of rule bullets, best effort.
- Add or update `architecture_sources` with an entry for `_bmad-output/planning-artifacts/architecture.md` and current date.

Use compact YAML. Do not let metadata bloat the file.

## Compression Pass

After merging, read the complete file and compress if needed:

- Remove duplicated rules.
- Combine overlapping bullets.
- Prefer dense bullets over verbose paragraphs.
- Keep section hierarchy simple.
- Keep usage guidance short.

If the file remains over 300 lines and further compression would remove meaningful rules, STOP and ask the user what to compress or remove.

## Final Validation

Validate:

- File is <= 300 lines.
- No duplicate rules were introduced.
- No existing rule was removed without explicit replacement/removal evidence or user decision.
- New rules are durable architecture rules, not local implementation notes.
- Existing rules absent from `architecture.md` were preserved.

## Completion Output

Report:

- project context path
- final line count
- number of added/replaced/removed rules
- conflicts resolved, if any
- any local-only architecture details intentionally ignored
