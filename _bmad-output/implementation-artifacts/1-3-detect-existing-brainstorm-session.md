# Story 1.3: Detect Existing Brainstorm Session

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a returning package user,
I want the package chat to detect an existing brainstorm session,
so that I can continue work without guessing whether a session already exists.

## Acceptance Criteria

1. Given a package has an active brainstorm checkpoint, when I open the package chat, then the frontend can request brainstorm status for that package, and the response identifies the active session id, phase, technique if any, idea count, and message count.
2. Given no active brainstorm session exists, when I open the package chat, then the brainstorm status response indicates that no session is active, and the regular package chat remains usable.
3. Given the status request fails because the user lacks package access, when the backend validates the request, then it returns the existing authorization error format, and no agent request is sent.

## Tasks / Subtasks

- [x] Add browser-facing brainstorm status endpoint (AC: 1, 2, 3)
  - [x] Extend `thagid/schemas/brainstorm.py` with a `BrainstormStatusResponse` schema containing `active`, `session_id`, `phase`, `technique`, `idea_count`, and `message_count`.
  - [x] Add `GET /api/packages/{package_id}/brainstorm/status` to `thagid/routers/brainstorm.py`.
  - [x] Reuse existing package access verification before any agent call; invalid id remains 422, missing package remains 404, cross-org access remains 403, unauthenticated access remains 401.
  - [x] Ensure forbidden/not-found status requests do not call the agent.
- [x] Extend backend agent client for status lookup (AC: 1, 2)
  - [x] Add a status method to `thagid/services/agent_client.py` that calls an internal agent status endpoint with `X-Agent-Key` and the configured `AGENT_SERVICE_URL`.
  - [x] Backend must derive `project_id` server-side from the authorized package/project relationship; do not trust frontend-supplied project ids.
  - [x] Map missing active sessions to a normal `active: false` browser response, not an error.
  - [x] Map agent/internal failures to the existing brainstorm agent error detail without leaking internals.
- [x] Add agent-side status lookup (AC: 1, 2)
  - [x] Add an internal agent endpoint such as `GET /internal/agent/brainstorm/status`, protected by the existing `verify_agent_key` dependency.
  - [x] Lookup active brainstorm state by `package_id` and `project_id` in checkpoint storage prepared by Stories 1.1 and 1.2.
  - [x] Return `active: true` with session id, phase, technique if any, idea count, and message count when active state exists.
  - [x] Return `active: false` with null/zero metadata when no active brainstorm checkpoint exists.
  - [x] If Story 1.2's implementation does not yet provide a queryable package-to-session checkpoint index, add the smallest checkpoint-schema-backed metadata needed for status lookup; keep it under `agent_checkpoints`, not the application tables.
- [x] Wire frontend status loading on package open (AC: 1, 2)
  - [x] Add `getBrainstormStatus(packageId)` to `web/src/lib/api/brainstorm.ts` using `$lib/api/client.ts`.
  - [x] Add a `BrainstormStatusResponse` type to `web/src/lib/types/brainstorm.ts`.
  - [x] Update `web/src/routes/project/[id]/package/[pkgId]/+page.svelte` to request status after package load for the current `pkgId` and ignore stale responses when navigating between packages.
  - [x] If status is active, set `brainstormSessionId` and `brainstormPhase` from the response so the existing `ChatInterface` phase badge appears.
  - [x] If status is inactive, leave `brainstormPhase` and `brainstormSessionId` unset so regular package chat remains usable.
- [x] Preserve message and chat behavior (AC: 1, 2)
  - [x] Continue loading existing package messages through `listMessages`; do not replace chat history with checkpoint data in this story.
  - [x] Preserve regular chat send behavior when status is inactive.
  - [x] Preserve brainstorm send behavior when status is active, using the existing brainstorm message API path from Story 1.2.
  - [x] Preserve `role="log"`, `aria-live="polite"`, auto-scroll, Enter-to-send, and Shift+Enter newline behavior in `ChatInterface.svelte`.
- [x] Add tests and verification (AC: 1, 2, 3)
  - [x] Add backend tests for active status success, inactive status success, unauthenticated rejection, invalid package id, package not found, cross-org forbidden, agent not called on authorization failure, and agent error mapping.
  - [x] Add agent tests for missing/invalid `X-Agent-Key`, active checkpoint status, inactive checkpoint status, and correct counts for messages and ideas.
  - [x] Add or update frontend checks for inactive status preserving regular chat and active status setting phase/session metadata if the existing test setup supports it; otherwise run `cd web && npm run check`.
  - [x] Run `pytest`, agent tests, and `cd web && npm run check`.

### Review Findings

- [x] [Review][Patch] Concluded brainstorm checkpoints are still reported as active [agent/checkpoint.py:35]
- [x] [Review][Patch] Active status response accepts malformed checkpoint state as success [agent/main.py:61]
- [x] [Review][Patch] Backend status validation errors bypass agent error mapping [thagid/services/brainstorm.py:22]

## Dev Notes

### Scope Boundaries

- This story detects an existing brainstorm session when package chat opens. It does not implement full state resume, message-history hydration from checkpoint, or exact continuation behavior; that is Story 1.4.
- This story should only surface status metadata: active flag, session id, phase, technique, idea count, and message count.
- Do not implement technique recommendation, technique picker behavior, idea reducers, file upload, URL ingestion, rolling summary, KG writes, extraction, validation, markdown rendering, summary cards, or results detail views.
- Do not convert regular package chat into brainstorm mode when no active checkpoint exists.

### Required Detection Behavior

- Detection must be authoritative and backend-mediated. Do not infer active status from local `brainstormPhase`, existing message text, URL fragments, or whether a message starts with `/brainstorm`.
- The frontend calls `GET /api/packages/{package_id}/brainstorm/status`; FastAPI verifies package access; only then may FastAPI call the internal agent status endpoint.
- The browser must never call `thagid-agent` directly.
- A package with no active checkpoint is a valid state and must return a successful inactive status response.

### Current Codebase State

- `thagid/routers/brainstorm.py` currently exposes `POST /api/packages/{package_id}/brainstorm/message`, verifies package access locally, derives project id server-side, and maps `AgentError` to HTTP 502.
- `thagid/services/brainstorm.py` currently saves the user message, calls `agent_client.agent_brainstorm_message`, saves the assistant message, and returns `BrainstormMessageResponse` with message, session id, and phase.
- `thagid/schemas/brainstorm.py` currently defines `BrainstormMessageCreate` and `BrainstormMessageResponse`; no status response schema exists yet.
- `thagid/services/agent_client.py` currently has `agent_health()` and `agent_brainstorm_message()`; no status call exists yet.
- `agent/main.py` currently exposes `/internal/agent/health` and `/internal/agent/brainstorm/message`; no status endpoint exists yet.
- `agent/checkpoint.py` currently validates AGE/vector extensions and creates `agent_checkpoints`; it does not expose status lookup helpers.
- `web/src/lib/api/brainstorm.ts` currently exposes `sendBrainstormMessage()` only.
- `web/src/lib/types/brainstorm.ts` currently defines `BrainstormPhase` and `BrainstormMessageResponse` only.
- `web/src/routes/project/[id]/package/[pkgId]/+page.svelte` currently maintains `brainstormPhase` and `brainstormSessionId` in page-local state, but only sets them after a brainstorm send. Refresh/navigation loses these values until this story adds status detection.

### Previous Story Intelligence

- Story 1.2 is in review and implemented the brainstorm message path with backend router, backend orchestration service, agent client, agent internal endpoint, frontend API/types, phase badge, and package-chat state wiring.
- Story 1.2 backend tests mock `thagid.services.brainstorm.agent_client.agent_brainstorm_message`; follow the same mocking style for status tests.
- Story 1.2 agent tests patch `ensure_schema` and mutate `settings.AGENT_KEY`; reuse that pattern for status endpoint tests.
- Story 1.2 found that `httpx.Response.raise_for_status()` and `.json()` are synchronous methods in tests; use `MagicMock` for those methods, not `AsyncMock`.
- Story 1.2 currently sends brainstorm messages after `/brainstorm` prefix or when `brainstormPhase` is already set. Story 1.3 should set `brainstormPhase` from status so subsequent sends use the brainstorm path.

### Architecture Requirements

- Brainstorm session detection endpoint is `GET /api/packages/{package_id}/brainstorm/status`; when active, UI shows brainstorm mode with technique and idea count metadata. [Source: _bmad-output/planning-artifacts/architecture.md#Frontend-Integration]
- Existing chat must be preserved: regular `POST /api/packages/{package_id}/messages` continues for non-brainstorm chat. [Source: _bmad-output/planning-artifacts/architecture.md#Frontend-Integration]
- Session checkpointing stores state in PostgreSQL under `agent_checkpoints`; first message creates checkpoint, every turn updates checkpoint, and user return loads from checkpoint. [Source: _bmad-output/planning-artifacts/architecture.md#Session-Persistence-Checkpointing]
- Agent/FastAPI communication uses `X-Agent-Key`, synchronous HTTP, and standard agent error mapping. [Source: _bmad-output/planning-artifacts/architecture.md#Communication-Patterns]
- Frontend traffic never calls the agent container directly; FastAPI is the gateway. [Source: _bmad-output/planning-artifacts/architecture.md#Architectural-Boundaries]

### API Contract Guidance

- Browser response should use snake_case JSON fields:
  - `active: boolean`
  - `session_id: string | null`
  - `phase: BrainstormPhase | null`
  - `technique: string | null`
  - `idea_count: number`
  - `message_count: number`
- Internal agent status response may use the same shape to reduce mapping errors.
- If active is false, `session_id`, `phase`, and `technique` should be null and counts should be zero.
- If checkpoint data is malformed or unreadable, treat that as an agent/internal failure, not inactive status; inactive status is only for a clean no-session result.

### Checkpoint Lookup Guidance

- The status endpoint needs package-level lookup, not session-id lookup, because returning users may not have a session id in frontend memory.
- If using LangGraph checkpoint APIs, store enough metadata/configurable keys to find the latest active checkpoint by `package_id` and `project_id`.
- If the current minimal checkpoint setup is not sufficient, add a small helper/index in `agent_checkpoints` that records active package sessions with `project_id`, `package_id`, `session_id`, `phase`, `technique`, `idea_count`, `message_count`, and status. Keep this implementation narrowly scoped to session detection.
- Do not add application-domain session tables under public schema unless explicitly required later; the architecture places brainstorm state persistence in agent checkpoint storage.

### Frontend UX Requirements

- On package open with active status, the chat header shows `BrainstormPhaseBadge` between package title/status area and the package status badge. [Source: design-system/thagid/pages/package-chat.md#Chat-Header]
- On package open with no active status, regular chat remains usable and does not show a phase badge. [Source: _bmad-output/planning-artifacts/epics.md#Story-1.3-Detect-Existing-Brainstorm-Session]
- The user should not see a save/resume prompt in this story. UX guidance says resumed sessions are invisible/no-prompt; this story only sets the visible phase/status metadata. [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Journey-4-Session-Abandoned-and-Resumed]
- Preserve the message area `role="log"` and `aria-live="polite"`. [Source: design-system/thagid/pages/package-chat.md#Message-Area]

### File Structure Requirements

- Backend likely updates: `thagid/schemas/brainstorm.py`, `thagid/routers/brainstorm.py`, `thagid/services/agent_client.py`, optional `thagid/services/brainstorm.py`, and `thagid/tests/test_brainstorm.py` or a focused status test file.
- Agent likely updates: `agent/main.py`, `agent/checkpoint.py` or a new focused checkpoint/status helper, and `agent/tests/test_brainstorm.py` or a focused status test file.
- Frontend likely updates: `web/src/lib/api/brainstorm.ts`, `web/src/lib/types/brainstorm.ts`, and `web/src/routes/project/[id]/package/[pkgId]/+page.svelte`.
- Avoid changes to `web/src/lib/components/ui/`; those are shadcn-managed.
- Avoid broad refactors of package access verification unless needed; if deduplicating `verify_package_access`, keep behavior and status codes identical.

### Testing Requirements

- Backend tests use pytest, pytest-asyncio, SQLite in-memory sessions, and httpx ASGI clients.
- Agent tests use FastAPI `TestClient`, patched startup schema checks, and mutable `settings.AGENT_KEY`.
- Mock backend agent HTTP calls for normal `pytest`; do not require a running agent container for backend unit tests.
- Required backend checks:
  - Active status returns active true with session id, phase, technique, idea_count, and message_count.
  - Inactive status returns active false and keeps regular chat usable.
  - Invalid id, not found, unauthenticated, and forbidden responses match existing authorization/error formats.
  - Agent status is not called when authorization fails.
  - Agent/internal errors map to the standard brainstorm agent error detail.
- Required agent checks:
  - Missing/invalid `X-Agent-Key` rejected.
  - No checkpoint returns inactive response.
  - Active checkpoint returns the expected metadata and counts.
- Required frontend verification: run `cd web && npm run check`; add unit tests only if they fit existing project patterns.

### Regression Risks

- Calling agent status before package authorization would leak package existence or cross-org data.
- Treating agent failures as inactive status would hide runtime problems and make users unknowingly use regular chat.
- Forgetting to clear stale `brainstormPhase` and `brainstormSessionId` on package navigation could show a previous package's phase badge.
- Continuing to rely only on page-local state would fail the core returning-user requirement after refresh.
- Adding full resume/history hydration here would overlap Story 1.4 and increase risk.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story-1.3-Detect-Existing-Brainstorm-Session]
- [Source: _bmad-output/planning-artifacts/prd.md#Brainstorm-Session-Management]
- [Source: _bmad-output/planning-artifacts/architecture.md#Frontend-Integration]
- [Source: _bmad-output/planning-artifacts/architecture.md#Session-Persistence-Checkpointing]
- [Source: _bmad-output/planning-artifacts/architecture.md#Communication-Patterns]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Journey-4-Session-Abandoned-and-Resumed]
- [Source: design-system/thagid/pages/package-chat.md]
- [Source: _bmad-output/implementation-artifacts/1-2-start-brainstorm-from-package-chat.md#Dev-Agent-Record]

## Project Structure Notes

- This story should be additive to the current brainstorm message path. Keep the existing `sendBrainstormMessage` behavior and add status detection beside it.
- The existing frontend phase badge component can be reused as-is if the status response sets `brainstormPhase` correctly.
- The current frontend state is package-page-local. When adding status loading, reset `brainstormPhase` and `brainstormSessionId` at the start of each package-load effect to avoid stale package state.

## Dev Agent Record

### Agent Model Used

glm-5.1

### Debug Log References

### Completion Notes List

- Ultimate context engine analysis completed - comprehensive developer guide created.
- Implemented brainstorm status detection across full stack: agent checkpoint lookup, agent status endpoint, backend agent client status call, backend brainstorm service status function, backend router status endpoint, frontend API function, frontend type, and frontend page wiring.
- Added `get_active_brainstorm_state()` to `agent/checkpoint.py` for querying brainstorm_states by package_id/project_id.
- Added `GET /internal/agent/brainstorm/status` to agent with `verify_agent_key` protection.
- Added `agent_brainstorm_status()` to `thagid/services/agent_client.py` and `get_brainstorm_status()` to `thagid/services/brainstorm.py`.
- Added `BrainstormStatusResponse` schema and `GET /api/packages/{package_id}/brainstorm/status` router endpoint reusing `verify_package_access`.
- Frontend loads brainstorm status on package open and sets `brainstormPhase`/`brainstormSessionId` from response if active.
- Status loading uses stale guard to prevent race conditions on package navigation.
- `brainstormPhase` and `brainstormSessionId` are reset to `undefined` at start of each package-load effect to avoid stale state.
- All 103 tests pass (21 brainstorm tests including 10 new status tests, 11 agent tests including 4 new status tests).
- Frontend `npm run check` passes with 0 errors and 0 warnings.

### File List

- `thagid/schemas/brainstorm.py` (modified - added BrainstormStatusResponse)
- `thagid/routers/brainstorm.py` (modified - added GET status endpoint, imports)
- `thagid/services/agent_client.py` (modified - added agent_brainstorm_status)
- `thagid/services/brainstorm.py` (modified - added get_brainstorm_status, import)
- `agent/checkpoint.py` (modified - added get_active_brainstorm_state)
- `agent/main.py` (modified - added GET status endpoint, import)
- `web/src/lib/api/brainstorm.ts` (modified - added getBrainstormStatus)
- `web/src/lib/types/brainstorm.ts` (modified - added BrainstormStatusResponse)
- `web/src/routes/project/[id]/package/[pkgId]/+page.svelte` (modified - added status loading)
- `thagid/tests/test_brainstorm.py` (modified - added 10 status tests)
- `agent/tests/test_brainstorm.py` (modified - added 4 status tests, updated fixture)

### Change Log

- 2026-05-09: Story 1.3 implementation complete - brainstorm session status detection across agent, backend, and frontend layers.
