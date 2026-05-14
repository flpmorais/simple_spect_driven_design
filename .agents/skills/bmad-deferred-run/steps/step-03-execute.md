# Step 3: Execute Plan

## Rules

- Speak in `{communication_language}` if available; otherwise English.
- Implement tasks in the approved plan order.
- Keep changes minimal and directly traceable to the deferred item.
- Update tests with the implementation.
- Do not mark a task complete until relevant validation passes.

## Execution Loop

For each planned task:

1. Read relevant files before editing.
2. Implement the smallest correct change.
3. Update/add/remove tests as needed.
4. Run targeted validations for that task.
5. Fix failures and rerun until passing.
6. Append notes to the plan `## Execution Record`.

STOP and ask the user if:

- implementation requires material deviation from the plan
- project context says X and implementation would require Y
- a new dependency/framework/component/pattern is needed but not approved
- tests reveal ambiguous intended behavior
- validation cannot be made to pass after three attempts

When all tasks are complete, load `./step-04-validate-complete.md`.
