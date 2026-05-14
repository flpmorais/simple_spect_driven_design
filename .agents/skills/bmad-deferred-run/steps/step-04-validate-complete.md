# Step 4: Validate, Complete, Commit, And Push

## Rules

- Speak in `{communication_language}` if available; otherwise English.
- Do not commit until validations pass.
- Commit deferred-work-related changes and push to remote.
- Do not commit secrets or unrelated user changes.
- Do not amend commits unless explicitly requested.
- Do not skip hooks.
- Never force push.

## Final Validation

Run:

- all validation commands from the deferred plan
- relevant unit/integration/e2e tests based on touched code
- lint/type/static checks when relevant and configured

If validations fail, fix and rerun. If blocked, mark plan and tracker `blocked`, record the blocker, and HALT.

## Mark Complete

Update the plan artifact:

- frontmatter `status: done`
- execution record with final validation log
- files changed

Update `{tracker_file}`:

- Status: `done`
- Notes: completion summary

## Commit

Inspect git status, git diff, and recent git log.

Stage only deferred-work-related changes, including tracker and plan artifact.

Use commit message:

```text
Complete deferred work <ID>
```

If hooks modify files, inspect changes, rerun relevant validation if needed, create a new commit for hook changes, and do not amend.

## Push

After commit succeeds:

- If current branch has upstream, run `git push`.
- Otherwise run `git push -u origin <current-branch>`.

Update the plan execution record with commit hash and push result. If this creates uncommitted artifact changes, create a follow-up commit and push again.

## Completion Output

Report:

- deferred item ID
- plan artifact path
- validations run
- commit hash(es)
- push result
- residual risks or skipped validations
