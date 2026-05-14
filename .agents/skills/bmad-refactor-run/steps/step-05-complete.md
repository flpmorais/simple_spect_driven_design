# Step 5: Complete, Commit, And Push

## Rules

- Speak in `{communication_language}`.
- Commit only after all required validations pass.
- Commit all uncommitted files that belong to the refactor execution.
- Do not complete if any task checklist item is unchecked or lacks evidence.
- Do not complete if any `execution/task-*.md` is not `taskStatus: complete`.
- Do not complete if the main refactor objective is implemented only as unused scaffolding.
- Do not commit secrets or credentials.
- Do not amend commits.
- Do not skip hooks.
- Never force push.

## Final Artifact Update

Before committing, update the selected refactor bundle index `{refactor_dir}/refactor.md`:

- `executionStatus: complete`
- `executionCompletedAt: <YYYY-MM-DD-HHMM>`
- `executionLastUpdated: <YYYY-MM-DD-HHMM>`
- `executionBranch: <current git branch>`

Update bundle execution files:

- `execution/checklist.md`: all checklist boxes checked with evidence.
- `execution/files-changed.md`: all new, modified, or deleted files relative to repo root.
- `execution/validation.md`: final validation summary.
- `execution/commits.md`: pending commit.
- `refactor.md`: compact execution status summary and links to execution files.

Before setting `executionStatus: complete`, re-scan the bundle execution files and selected bundle index:

- No unchecked task checklist items remain.
- No checked item is missing source/test/command evidence.
- No required validation is marked skipped without a concrete reason.
- `execution/validation.md` explicitly states where the refactored behavior is used at runtime.

If any condition fails, set `executionStatus: blocked`, record the failed completion gate, and HALT.

## Commit

Inspect git status, git diff, and recent git log.

Stage refactor-related changes, including the refactor bundle. If unrelated dirty files exist, do not stage them unless they are clearly part of the refactor or the user explicitly instructed inclusion.

Use a concise commit message:

```text
Execute refactor plan <refactorName>
```

If commit hooks modify files, inspect the changes, run relevant validation if needed, then create a new commit that includes hook changes. Do not amend unless explicitly requested.

## Push

After commit succeeds:

- If the current branch has an upstream, run `git push`.
- If no upstream exists, run `git push -u origin <current-branch>`.
- Never force push.

Update `execution/commits.md` with:

- commit hash
- push target
- push result

If updating the bundle after commit/push creates new uncommitted changes, make a follow-up commit for the execution record update and push again.

## Completion Output

Report:

- refactor bundle path
- commit hash(es)
- push result
- validations run
- any residual risks or skipped validations
