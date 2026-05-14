# Step 2: Understand Selected Batch

## Rules

- Speak in `{communication_language}` if available; otherwise English.
- Do not modify source code.
- Use read-only exploration to determine whether the item is still true.

## Read Context

For each selected batch item:

- Read source files referenced by the item when paths are present.
- Search current code for the relevant symbols, routes, services, tests, or components.
- Read nearby tests when the item references coverage gaps.
- Read `_bmad-output/project-context.md` for applicable technical rules.

## Determine Current State

For each batch item, determine:

- What the item means in plain language.
- Why it was deferred originally, based on raw text and source heading.
- Whether it still appears true in the current code.
- Whether later work seems to have fixed or superseded it.
- Whether it overlaps another tracker item.
- What project-context rules are relevant.

Keep this analysis concise. Do not dump raw tracker sections or the full deferred-work file into the user response.

Then load `./step-03-classify.md`.
