# Step 3: Review Proposed Changes

## Rules

- Speak in `{communication_language}`.
- Do not modify files until the user confirms the proposed changes.
- Conflicts require an explicit user decision.

## Present Proposed Changes

Show the proposed merge summary from Step 2.

Emphasize:

- Existing project-context rules not mentioned in `architecture.md` will be preserved.
- Replacements/removals require explicit architecture evidence.
- Local-only work-package details will not be added.
- Final project context must remain under 300 lines.

## Conflict Handling

If there are `conflict` items, present each conflict with options:

```text
Conflict: <summary>

[1] Keep existing project-context rule
[2] Replace with architecture rule
[3] Add a clarified combined rule
[4] Do not update project context now
```

HALT and wait for user decisions before continuing.

Record the user's decisions in the proposed merge plan.

## Approval Gate

Ask:

```text
Apply these approved project-context updates?

[1] Apply updates
[2] Revise proposed updates
[3] Stop without changes
```

HALT and wait for selection.

- If `[1]`, load `./step-04-merge-and-validate.md`.
- If `[2]`, revise the proposed merge summary and ask again.
- If `[3]`, STOP without modifying files.
