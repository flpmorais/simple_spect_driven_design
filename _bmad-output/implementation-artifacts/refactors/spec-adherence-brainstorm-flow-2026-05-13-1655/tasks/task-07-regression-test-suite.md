# Task 07: Build Specification Regression Test Suite

## Implementation Contract

- Objective: Add and update automated tests that prove the refactor matches PRD, architecture, and project context, preventing future drift and rejecting scaffolding-only changes.
- Runtime entrypoint: Test suites under `agent/tests/`, `thagid/tests/`, and `web/src/**/*.test.ts`; Playwright where applicable.
- Old owner: Existing tests cover many parts but some encode simplified immediate-finalization behavior.
- New owner: Tests encode the approved lifecycle, boundary, persistence, and UI contracts.
- Forbidden implementation patterns: Do not delete failing tests without replacement; do not lower assertions to match drift; do not rely on external LLM/OpenAI calls; do not skip tests; do not add brittle sleeps/timeouts.
- Required implementation patterns: Use explicit fakes/mocks for PydanticAI, backend agent client, KG service errors, and frontend API responses; include negative tests for forbidden shortcuts.
- Compatibility allowed: Refactor existing tests when their old expectations conflict with accepted decisions.
- Compatibility forbidden: Leaving graph tests that expect conclude → markdown in one turn; accepting swallowed KG failures; accepting frontend locked review state.
- Files allowed: `agent/tests/**`, `thagid/tests/**`, `web/src/**/*.test.ts`, `web/e2e/**` or existing e2e location, test fakes/helpers.
- Files forbidden: Production source except where earlier tasks require; stale `docs/**`.

## Work Items

- Likely files / areas:
  - `agent/tests/test_brainstorm_graph.py`, `test_brainstorm.py`, `test_brainstorm_nodes.py`, `test_architecture_boundaries.py`.
  - `thagid/tests/test_brainstorm.py`, `thagid/tests/test_kg.py`.
  - `web/src/lib/components/custom/ChatInterface.test.ts`, summary/detail tests, Playwright e2e.
- Subtasks:
  - Update graph tests to require review pause after conclusion intent and finalization only after confirmation.
  - Add full fake-runner lifecycle test: initiate → select technique → facilitate with ideas/context → conclude → review → adjust → confirm → KG finalization → markdown/concluded.
  - Add resume tests for active `facilitate`, review, validation retry, and terminal checkpoints.
  - Add KG tests for aggregate successful write, rollback on failure, no embedding queue on failure, and result retrieval after success.
  - Add backend tests for internal-to-public contract bridge, review-phase response, finalization error propagation, and malformed response rejection.
  - Add frontend unit tests for review controls, confirmation, no premature lock, attachment gating, and concluded display.
  - Add architecture-boundary tests for no browser internal endpoints, no agent `thagid` imports, no forbidden LangChain APIs, and no KG writes in unconfirmed extract.
  - Add or update Playwright e2e flow if existing harness supports it.

## Completion Checks

- Done when:
  - Tests fail against old immediate-finalization/silent-failure behavior and pass against the refactored behavior.
  - Every accepted decision D1-D4 has at least one automated regression test.
  - Boundary tests protect project-context rules.
  - Frontend tests prove review and confirmation UX.
- Evidence required:
  - Test command outputs or recorded pass/fail notes.
  - List of tests added/updated mapped to D1-D4.
- Forbidden shortcuts:
  - Marking tests skipped or xfail.
  - Testing helper functions only while missing runtime entrypoint tests.
  - Replacing integration tests with snapshot-only checks.
- Static checks:
  - Test files contain no external network dependency for LLM/OpenAI.
  - Boundary tests search relevant source paths.
- Test commands:
  - `pytest agent/tests/test_brainstorm.py agent/tests/test_brainstorm_graph.py agent/tests/test_brainstorm_nodes.py agent/tests/test_architecture_boundaries.py`
  - `pytest thagid/tests/test_brainstorm.py thagid/tests/test_kg.py`
  - `cd web && npm run test:unit`
- Runtime-path evidence:
  - Lifecycle tests exercise `/internal/agent/brainstorm/message` or graph invocation, not only isolated helpers.
  - Backend tests exercise public API service/router bridge with mocked agent client.
- Validation:
  - Full `pytest` and frontend unit checks before final execution completion.
- Risks / notes:
  - If e2e environment is incomplete, document limitation and keep Playwright task focused on available harness without weakening unit/integration coverage.
