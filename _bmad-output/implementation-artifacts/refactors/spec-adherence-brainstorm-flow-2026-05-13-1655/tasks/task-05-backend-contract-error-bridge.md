# Task 05: Align Backend Brainstorm Contract And Error Bridge

## Implementation Contract

- Objective: Ensure FastAPI public brainstorm routes correctly bridge the internal agent contract, preserve user auth/package access, and surface finalization failures without corrupting message history.
- Runtime entrypoint: `POST /api/packages/{package_id}/brainstorm/message`, `GET /api/packages/{package_id}/brainstorm/status`, and `GET /api/packages/{package_id}/brainstorm/results`.
- Old owner: Backend service validates a simplified agent response and maps broad failures to `AgentError`.
- New owner: `thagid/services/brainstorm.py` owns public/internal contract bridge; routers stay HTTP-only; schemas document public response shape.
- Forbidden implementation patterns: No business logic in routers; no raw agent response leakage; no SQLAlchemy model leakage; no browser/internal route exposure; no successful assistant message commit when finalization fails.
- Required implementation patterns: Pydantic validation for internal agent response; explicit mapping from internal `state_change` to public `phase`; transactional message persistence behavior; generic safe user-facing error details for internal failures.
- Compatibility allowed: Public response can remain `BrainstormMessageResponse` with `message`, `phase`, counts, ideas, themes, markdown if explicitly tested as a wrapper around internal agent contract.
- Compatibility forbidden: Public route returning raw internal response without `message`; losing user messages inconsistently on agent failures without an intentional tested policy; storing malformed themes/ideas.
- Files allowed: `thagid/services/brainstorm.py`, `thagid/routers/brainstorm.py`, `thagid/schemas/brainstorm.py`, `thagid/services/agent_client.py`, `thagid/tests/test_brainstorm.py`, possibly `agent/main.py` only for contract compatibility tests in earlier/later tasks.
- Files forbidden: Agent graph internals except through tests/fakes in this task; frontend except later UI task; stale `docs/**`.

## Work Items

- Likely files / areas:
  - `thagid/services/brainstorm.py` response validation, error mapping, message commit/rollback.
  - `thagid/schemas/brainstorm.py` phase and response schemas.
  - `thagid/services/agent_client.py` timeout/client behavior.
  - `thagid/tests/test_brainstorm.py` contract and error tests.
- Subtasks:
  - Add or tighten an internal agent response schema for FastAPI service validation.
  - Explicitly map `state_change` to public `phase` and reject unknown phases.
  - Ensure review phase responses with themes are saved/displayed but not treated as concluded.
  - Ensure finalization errors from agent produce appropriate HTTP error and do not save a misleading assistant success/markdown message.
  - Preserve existing auth/package access checks and brainstorm technique listing.
  - Add tests for review response, confirmation success, confirmation failure, malformed agent response, and status/result behavior.

## Completion Checks

- Done when:
  - Backend tests prove internal agent contract bridges to public response shape.
  - Agent finalization failure returns an error and does not create a false concluded assistant markdown message.
  - Review-phase response with themes remains active and visible to frontend.
  - Existing JWT/package access tests still pass.
- Evidence required:
  - Test names/references for success, review, finalization failure, malformed response, and access control.
  - Source references to internal response schema or validation helper.
- Forbidden shortcuts:
  - Letting `dict` access throw `KeyError` as validation.
  - Saving all assistant responses before phase/error validation.
  - Changing route prefixes or auth requirements.
- Static checks:
  - Routes remain under `/api/packages/{package_id}/brainstorm/...`.
  - Routers do not contain business logic beyond dependency/HTTP mapping.
- Test commands:
  - `pytest thagid/tests/test_brainstorm.py thagid/tests/test_messages.py thagid/tests/test_packages.py`
- Runtime-path evidence:
  - Mocked agent review response produces public `phase: extract` with themes and no markdown.
  - Mocked agent failure during confirmation produces safe error response.
- Validation:
  - Backend unit/router tests with mocked `agent_client` responses.
- Risks / notes:
  - Be explicit about rollback policy for the user message on agent failure; preserve current expected behavior unless spec requires otherwise.
