# Refactor Completion Checklist

Use this checklist during final validation before `executionStatus: complete`.

## Task Execution Files

- [x] `execution/task-01-align-binding-specs.md` — complete with PRD/architecture read-only and no-diff evidence.
- [x] `execution/task-02-harden-agent-contracts.md` — complete with internal response/payload and targeted agent validation evidence.
- [x] `execution/task-03-refactor-graph-lifecycle.md` — complete with review-pause/runtime lifecycle evidence.
- [x] `execution/task-04-atomic-kg-finalization.md` — complete with aggregate KG finalization and rollback/error evidence.
- [x] `execution/task-05-backend-contract-error-bridge.md` — complete with backend public/internal contract validation evidence.
- [x] `execution/task-06-frontend-review-confirmation.md` — complete with frontend check/unit/static audit evidence.
- [x] `execution/task-07-regression-test-suite.md` — complete with D1-D4 regression mapping evidence.
- [x] `execution/task-08-final-validation-and-drift-audit.md` — complete with full validation and static audit evidence.

## Task Evidence

- [x] Every `tasks/task-*.md` file has a corresponding `execution/task-*.md` file. Evidence: execution directory contains task 01 through task 08 files.
- [x] Every `execution/task-*.md` file has frontmatter `taskStatus: complete` before final validation. Evidence: task files updated with complete frontmatter.
- [x] Every task checklist item is checked. Evidence: task execution files contain checked acceptance items.
- [x] Every checked item includes concrete evidence. Evidence: task execution files name source paths, test names, commands, and static audits.
- [x] Evidence names source references, tests, commands, or manual checks specific enough for another agent to verify. Evidence: `execution/validation.md` summarizes exact commands and source paths.
- [x] No task is marked complete solely because files were added or tests were written. Evidence: runtime-path tests and static audits verify behavior wiring.

## Production Integration

- [x] The main refactor objective is implemented in the production/runtime path named by the plan. Evidence: `/internal/agent/brainstorm/message`, graph routing, backend KG aggregate route, and frontend review tests all passed.
- [x] Runtime entry points affected by the refactor call the new/refactored implementation. Evidence: `agent/main.py:invoke_brainstorm_graph`, `agent/brainstorm/graph.py`, and `agent/backend_client.py:persist_brainstorm_output` are exercised by tests.
- [x] Old production ownership paths named for removal or replacement are removed, bypassed, or explicitly retained by the approved plan. Evidence: `agent/brainstorm/nodes/extract.py` no longer performs KG writes; aggregate KG finalization is used.
- [x] Newly added scaffolding is either used by production code or explicitly listed as an approved extension point/non-goal. Evidence: static/source audit found no unused KG write path in extract; helpers are exercised by tests.

## Tests And Validation

- [x] Task-level validations passed after the related implementation changes. Evidence: targeted agent/backend/frontend commands passed.
- [x] Cross-boundary validations from the plan passed, or skipped validations have concrete environment/scope reasons. Evidence: `pytest`, frontend check/unit passed; Playwright e2e documented webServer timeout.
- [x] Tests were not weakened to fit an incomplete implementation. Evidence: graph test now asserts review pause rather than immediate markdown.
- [x] Any test rewrites preserve behavior coverage or document intentional behavior changes from the approved plan. Evidence: execution task files map rewrites to D1-D4 accepted decisions.

## Completion Gate

- [x] `execution/validation.md` states where the refactored behavior is used at runtime. Evidence: final validation summary names runtime entry points.
- [x] `execution/validation.md` lists residual risks and skipped validations. Evidence: Playwright webServer timeout recorded as residual validation blocker.
- [x] `refactor.md` frontmatter is not set to `executionStatus: complete` until all checks above pass. Evidence: checklist completed before final frontmatter update.
