# Refactor Completion Checklist

Use this checklist during final validation before `executionStatus: complete`.

## Task Evidence

- [ ] Every `tasks/task-*.md` file has a corresponding `execution/task-*.md` file.
- [ ] Every `execution/task-*.md` file has frontmatter `taskStatus: complete` before final validation.
- [ ] Every task checklist item is checked.
- [ ] Every checked item includes concrete evidence.
- [ ] Evidence names source references, tests, commands, or manual checks specific enough for another agent to verify.
- [ ] No task is marked complete solely because files were added or tests were written.

## Production Integration

- [ ] The main refactor objective is implemented in the production/runtime path named by the plan.
- [ ] Runtime entry points affected by the refactor call the new/refactored implementation.
- [ ] Old production ownership paths named for removal or replacement are removed, bypassed, or explicitly retained by the approved plan.
- [ ] Newly added scaffolding is either used by production code or explicitly listed as an approved extension point/non-goal.

## Tests And Validation

- [ ] Task-level validations passed after the related implementation changes.
- [ ] Cross-boundary validations from the plan passed, or skipped validations have concrete environment/scope reasons.
- [ ] Tests were not weakened to fit an incomplete implementation.
- [ ] Any test rewrites preserve behavior coverage or document intentional behavior changes from the approved plan.

## Completion Gate

- [ ] `execution/validation.md` states where the refactored behavior is used at runtime.
- [ ] `execution/validation.md` lists residual risks and skipped validations.
- [ ] `refactor.md` frontmatter is not set to `executionStatus: complete` until all checks above pass.
