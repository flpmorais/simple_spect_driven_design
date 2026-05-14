# Task 08: Final Validation And Drift Audit

## Implementation Contract

- Objective: Run full validations, audit implementation against read-only PRD/architecture/project context, and prove no new drift or forbidden shortcut remains.
- Runtime entrypoint: Repository validation commands and static/code review checks after implementation tasks complete.
- Old owner: No single final drift gate.
- New owner: Executor performs explicit cross-cutting validation and records evidence before completion.
- Forbidden implementation patterns: Do not skip failing validations; do not ignore spec mismatches; do not commit/push until all required checks pass or blockers are explicitly reported; do not start a different BMad workflow.
- Required implementation patterns: Run targeted and full tests; inspect changed files against allowed scope; verify source-level rules; document any unrun command with reason.
- Compatibility allowed: If Playwright/e2e cannot run due environment, record exact failure and ensure unit/integration coverage still passes.
- Compatibility forbidden: Calling implementation complete with known failing backend/agent/frontend tests related to this refactor.
- Files allowed: Test evidence notes in commit/output only; source/test/spec files already modified by earlier tasks; no additional source changes except fixing validation failures within scope.
- Files forbidden: Stale `docs/**`, unrelated cleanup, unrelated config changes, ignored files/secrets.

## Work Items

- Likely files / areas:
  - Whole repository test suite.
  - Changed files from Tasks 01-07.
  - Binding specs and project context, read-only.
- Subtasks:
  - Run targeted agent/backend/frontend tests from prior tasks.
  - Run full `pytest` from repository root.
  - Run `cd web && npm run check` and `cd web && npm run test:unit`.
  - Run `cd web && npm run test:e2e` if environment supports it; otherwise record exact blocker.
  - Perform static audits: no `from thagid` under `agent/`; no forbidden LangChain APIs in application code; no browser calls to `/internal/kg` or `/internal/agent`; no KG writes in unconfirmed extract; no catch-and-pass finalization failures.
  - Verify implementation conforms to PRD/architecture/project-context on review pause, aggregate finalization, and error behavior without editing PRD or architecture.
  - Verify `_bmad-output/planning-artifacts/prd.md` and `_bmad-output/planning-artifacts/architecture.md` have no diff.
  - Verify git diff touches only approved source/spec/test areas and no secrets.
  - If the runner workflow requires commit/push, commit only after all validations pass and use a message reflecting spec adherence.

## Completion Checks

- Done when:
  - All required targeted tests pass.
  - Full backend/agent pytest pass.
  - Frontend check and unit tests pass.
  - E2E is either passing or has a documented environment blocker unrelated to implementation.
  - Static drift audit confirms no forbidden shortcuts and no PRD/architecture edits.
  - Final implementation summary maps completed work to D1-D4 and success criteria.
- Evidence required:
  - Command outputs for each validation.
  - Static audit notes with searches/checks performed, including no PRD/architecture diff.
  - Final changed-file summary grouped by spec/source/test.
- Forbidden shortcuts:
  - Treating partial targeted tests as enough without full validation.
  - Hiding unrun commands.
  - Committing ignored/secrets files.
- Static checks:
  - Search `agent/` for `from thagid` and forbidden LangChain imports.
  - Search `web/src` for `/internal/kg` and `/internal/agent`.
  - Search finalization paths for broad swallowed exceptions.
- Test commands:
  - `pytest`
  - `pytest agent/tests/test_brainstorm.py agent/tests/test_brainstorm_graph.py agent/tests/test_brainstorm_nodes.py agent/tests/test_architecture_boundaries.py thagid/tests/test_brainstorm.py thagid/tests/test_kg.py`
  - `cd web && npm run check`
  - `cd web && npm run test:unit`
  - `cd web && npm run test:e2e`
- Runtime-path evidence:
  - Full fake-runner lifecycle test and frontend review test are passing.
  - KG finalization failure test proves no false concluded state.
- Validation:
  - This task is the final validation gate for the refactor execution workflow.
- Risks / notes:
  - If validation uncovers new drift, fix within the relevant prior task scope and re-run all affected checks.
