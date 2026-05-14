# Story 1.4: Resume Persisted Brainstorm State

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a returning package user,
I want an interrupted brainstorm session to resume exactly where it left off,
so that I do not lose ideation context when I leave and return later.

## Acceptance Criteria

1. Given I have an active brainstorm session with messages, ideas, active technique, documents, and summary state, when I leave and later reopen the package, then the agent loads the latest checkpoint for that package session, and the chat reflects the persisted phase, message history, active technique, and idea count.
2. Given a brainstorm message is processed, when the agent response completes, then the updated LangGraph state is checkpointed to PostgreSQL, and persistence happens without requiring a visible save button.
3. Given checkpoint loading fails unexpectedly, when the backend handles the brainstorm request, then the user receives the standard error response, and the failure is logged without corrupting existing checkpoints.

## Tasks / Subtasks

- [x] Preserve and build on Story 1.3 status contract (AC: 1)
  - [x] Ensure `GET /api/packages/{package_id}/brainstorm/status` exists before implementing resume behavior.
  - [x] Ensure status returns `active`, `session_id`, `phase`, `technique`, `idea_count`, and `message_count` from checkpoint-backed state.
  - [x] Keep package access verification before any agent call; unauthorized status/message requests must not reach the agent.
  - [x] If Story 1.3 is not yet implemented in the worktree, implement its status contract first without changing the public response shape defined in Story 1.3.
- [x] Extend browser brainstorm message request with session continuity (AC: 1, 2)
  - [x] Extend `BrainstormMessageCreate` and frontend `sendBrainstormMessage` to optionally send `session_id` after status detection or after first brainstorm response.
  - [x] Backend must still derive `project_id` server-side and must verify that any supplied `session_id` belongs to the authorized package/project through the agent/checkpoint lookup.
  - [x] Continue saving user and assistant chat rows in the existing `messages` table.
  - [x] Preserve regular `/api/packages/{package_id}/messages` behavior for non-brainstorm chat.
- [x] Implement agent checkpoint load and update helpers (AC: 1, 2, 3)
  - [x] Add focused checkpoint helpers under `agent/checkpoint.py` or a new agent module for loading active session state by package/project and loading specific session state by `session_id`.
  - [x] Add checkpoint update helper that persists current state after each successful brainstorm turn.
  - [x] Store and retrieve at least `package_id`, `project_id`, `session_id`, `phase`, `messages`, `ideas`, `active_documents`, `summary`, `technique`, and status.
  - [x] Use `agent_checkpoints` schema for checkpoint/session metadata; do not add public application tables for brainstorm state.
  - [x] Ensure writes are atomic enough that a failed update does not partially corrupt the latest valid checkpoint.
- [x] Resume state in the agent message endpoint (AC: 1, 2, 3)
  - [x] Update `POST /internal/agent/brainstorm/message` to load existing state when `session_id` is provided.
  - [x] When `session_id` is absent, load the active package session if one exists; otherwise create a new session as Story 1.2 does.
  - [x] Append the new user message to the persisted state, generate the deterministic starter/continuation response currently supported by the agent, append the assistant message, and persist updated state.
  - [x] Return current `session_id`, `state_change`/phase, `technique`, `ideas`, `themes`, and `markdown` using existing internal response conventions.
  - [x] Do not implement real technique recommendation, real facilitation, idea reducers, file/URL ingestion, extraction, validation, or markdown rendering in this story.
- [x] Reflect resumed metadata in package chat (AC: 1)
  - [x] On package open, use the Story 1.3 status response to set `brainstormSessionId`, `brainstormPhase`, active technique display state if present, and idea count display state if present.
  - [x] Continue loading chat transcript from `listMessages(packageId)` so message history survives refresh through the existing message persistence.
  - [x] When sending a brainstorm message, pass the current `brainstormSessionId` to the brainstorm message API.
  - [x] After a successful brainstorm response, update `brainstormSessionId`, `brainstormPhase`, technique, and idea count from the response/status metadata.
  - [x] Keep regular chat usable when no active brainstorm status exists.
- [x] Add error handling for checkpoint failures (AC: 3)
  - [x] Log checkpoint load/update failures in the agent or backend without exposing internal details to the browser.
  - [x] Map checkpoint load/update failures to `{"detail": "Brainstorm agent encountered an error. Please try again."}` through existing `AgentError` handling.
  - [x] Ensure a failed checkpoint load/update rolls back request-local database work where applicable and leaves the previous checkpoint intact.
- [x] Add tests and verification (AC: 1, 2, 3)
  - [x] Backend tests: resumed brainstorm send includes session id, unauthorized users cannot resume another package's session, agent failures map to the standard error detail, regular messages still work.
  - [x] Agent tests: existing session id loads persisted state, no session id resumes active package session, every successful message updates checkpoint metadata/counts, checkpoint load failure returns a controlled error, previous checkpoint remains valid after update failure.
  - [x] Frontend verification: status-loaded session id is passed to subsequent brainstorm sends, stale session id is cleared on package navigation, and inactive status preserves regular chat.
  - [x] Run `pytest`, agent tests, and `cd web && npm run check`.

### Review Findings

- [x] [Review][Patch] Unknown supplied session IDs create new checkpoints instead of failing or resuming verified state [agent/main.py:110]
- [x] [Review][Patch] Resume path does not validate persisted `messages` before appending [agent/main.py:136]
- [x] [Review][Patch] Resume path does not validate persisted `session_id` before UUID parsing [agent/main.py:128]
- [x] [Review][Patch] Resumed metadata is not exposed through the public brainstorm message response [thagid/services/brainstorm.py:84]
- [x] [Review][Patch] Package chat does not display persisted technique or idea count [web/src/routes/project/[id]/package/[pkgId]/+page.svelte:51]
- [x] [Review][Patch] New checkpoint state omits required `status` metadata [agent/main.py:160]
- [x] [Review][Patch] Active-package resume can continue terminal checkpoints [agent/main.py:120]
- [x] [Review][Patch] Concurrent resume messages can overwrite each other with stale checkpoint state [agent/checkpoint.py:96]

## Dev Notes

### Scope Boundaries

- This story completes resume mechanics for the minimal brainstorm state established by Stories 1.2 and 1.3.
- This story should not implement actual LLM facilitation or Epic 2 ideation features. Continue using deterministic responses if that is all the current agent supports.
- This story should not add knowledge graph writes, embeddings, extraction, validation, markdown rendering, summary cards, or result detail views.
- This story should not introduce visible save buttons, confirmation dialogs, or a "resume session?" prompt. Resume is invisible.

### Dependency On Story 1.3

- Sprint status currently shows Story 1.3 as `ready-for-dev`, not done. If Story 1.3 has not been implemented before this story is developed, implement the Story 1.3 status contract first or treat it as a prerequisite branch dependency.
- Do not change the Story 1.3 public status response shape while adding resume behavior; Story 1.4 depends on it.
- Story 1.4 extends status from "detect active session" to "use the detected session for subsequent brainstorm messages".

### Current Codebase State

- `thagid/routers/brainstorm.py` currently has `POST /api/packages/{package_id}/brainstorm/message`, package access verification, server-side project id derivation, and `AgentError` mapping.
- `thagid/services/brainstorm.py` currently saves a user message, calls `agent_client.agent_brainstorm_message`, saves an assistant message, and returns message/session/phase metadata.
- `thagid/schemas/brainstorm.py` currently has `BrainstormMessageCreate` with `content` only and `BrainstormMessageResponse` with `message`, `session_id`, and `phase`.
- `thagid/services/agent_client.py` currently sends `session_id` internally if provided, but current browser request and service orchestration do not expose/pass it from the frontend.
- `agent/main.py` currently creates or preserves a session id in `/internal/agent/brainstorm/message` but does not load or persist full state.
- `agent/checkpoint.py` currently ensures extensions and creates `agent_checkpoints`; it has no load/save helpers for brainstorm state.
- `web/src/routes/project/[id]/package/[pkgId]/+page.svelte` currently stores `brainstormSessionId` in page-local state after a brainstorm response but does not pass it back to `sendBrainstormMessage`.
- `web/src/lib/api/brainstorm.ts` currently sends only `{ content }` to the backend.

### Previous Story Intelligence

- Story 1.2 implemented the first brainstorm message path and tests. It found that `httpx.Response.raise_for_status()` and `.json()` are synchronous methods in tests; use `MagicMock`, not `AsyncMock`, for those methods.
- Story 1.2 created the frontend `BrainstormPhaseBadge` and page-local `brainstormPhase`/`brainstormSessionId` state. Reuse these rather than introducing a new global store unless necessary.
- Story 1.3 story file defines the status contract and warns that stale `brainstormPhase`/`brainstormSessionId` must be reset on package navigation. Preserve that guardrail.
- Story 1.1 added the agent service, checkpoint schema foundation, `X-Agent-Key` auth, and approved dependencies. Do not introduce new runtime libraries without approval.

### Architecture Requirements

- LangGraph state shape includes `package_id`, `technique`, `messages`, `ideas`, `themes`, `active_documents`, `summary`, and `session_id`. [Source: _bmad-output/planning-artifacts/architecture.md#LangGraph-State-Machine]
- Checkpointing stores LangGraph state in PostgreSQL under `agent_checkpoints`; first message creates checkpoint, every turn updates checkpoint, and returning users load the checkpoint. [Source: _bmad-output/planning-artifacts/architecture.md#Session-Persistence-Checkpointing]
- FastAPI remains the gateway/proxy. Frontend traffic must not call `thagid-agent` directly. [Source: _bmad-output/planning-artifacts/architecture.md#Frontend-Integration]
- Existing regular chat endpoint remains separate and preserved for non-brainstorm chat. [Source: _bmad-output/planning-artifacts/architecture.md#Frontend-Integration]
- Agent/FastAPI communication uses `X-Agent-Key`; errors from the agent boundary map to a standard user-facing detail. [Source: _bmad-output/planning-artifacts/architecture.md#Communication-Patterns]

### State And API Contract Guidance

- Browser brainstorm message request should become `{"content": "...", "session_id": "uuid or null"}` or equivalent while keeping `content` validation from existing message schemas.
- Browser brainstorm response may stay compatible with Story 1.2 (`message`, `session_id`, `phase`) but should include or support `technique`, `idea_count`, and `message_count` if needed to reflect resumed state without an extra status call.
- Internal agent response should preserve `reply`, `session_id`, `state_change`, `ideas`, `themes`, and `markdown`. Add `technique`, `message_count`, and/or `active_documents` only if useful and documented in the backend schema mapping.
- Message history shown in chat should continue to come from the existing `messages` table. Agent checkpoint `messages` are for agent state, not a replacement for browser chat transcript unless explicitly implemented later.
- Active technique can be null in the current minimal flow. The UI should handle null without rendering misleading technique text.
- Idea count can be zero in the current minimal flow. The UI should handle zero without implying ideas were lost.

### Checkpoint Implementation Guidance

- Use package/project scoped lookup for active sessions because the frontend may not have a session id after refresh.
- Use session-id scoped lookup when a valid session id is provided by the browser/backend.
- Verify session/package/project consistency before resuming to prevent cross-package or cross-project session reuse.
- Store the latest state in a way that supports status lookup and future Story 2 state growth. A narrow metadata table/helper in `agent_checkpoints` is acceptable if LangGraph checkpoint APIs alone are not enough for package-level lookup.
- Keep old checkpoint/state intact until the new state is successfully written.
- Avoid public-schema application tables for brainstorm runtime state unless a later architecture change explicitly requires them.

### Frontend UX Requirements

- Returning to a package with an active brainstorm should show chat history, phase badge, and current status without prompting the user. [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Journey-4-Session-Abandoned-and-Resumed]
- No save indicator is required; persistence is invisible. [Source: _bmad-output/planning-artifacts/epics.md#Story-1.4-Resume-Persisted-Brainstorm-State]
- Preserve `role="log"`, `aria-live="polite"`, auto-scroll, Enter-to-send, and Shift+Enter newline behavior from the existing chat shell.
- If the status endpoint reports active session metadata before messages finish loading, avoid flicker or stale package state by guarding all async effects with the existing stale flag pattern.

### File Structure Requirements

- Backend likely updates: `thagid/schemas/brainstorm.py`, `thagid/services/brainstorm.py`, `thagid/services/agent_client.py`, `thagid/routers/brainstorm.py`, and brainstorm tests.
- Agent likely updates: `agent/main.py`, `agent/checkpoint.py` or a new focused state/checkpoint module, and agent brainstorm tests.
- Frontend likely updates: `web/src/lib/api/brainstorm.ts`, `web/src/lib/types/brainstorm.ts`, and `web/src/routes/project/[id]/package/[pkgId]/+page.svelte`.
- Avoid changes to `web/src/lib/components/ui/`; those are shadcn-managed.
- Avoid broad component refactors unless directly needed to pass session id/status metadata through the existing chat path.

### Testing Requirements

- Backend tests use pytest, pytest-asyncio, SQLite in-memory sessions, and httpx ASGI clients. Mock agent HTTP calls in backend tests.
- Agent tests use FastAPI `TestClient`, patched startup schema checks, and mutable `settings.AGENT_KEY`.
- Required backend checks:
  - Browser can send a brainstorm message with `session_id` and backend forwards it to the agent.
  - Backend rejects unauthorized/cross-org access before resume/agent call.
  - Agent checkpoint/load failures map to `Brainstorm agent encountered an error. Please try again.`
  - Existing regular message endpoint still works.
- Required agent checks:
  - Existing session id resumes persisted state.
  - Missing session id resumes active package session when one exists.
  - Successful turn updates message_count and preserves session id.
  - Checkpoint load/update failure returns controlled error and does not corrupt prior state.
- Required frontend verification:
  - `brainstormSessionId` from status/first response is included in subsequent brainstorm sends.
  - Switching packages clears stale session id and phase before new status resolves.
  - `cd web && npm run check` passes.

### Regression Risks

- Resuming by session id without verifying package/project ownership could allow cross-package state access through a guessed UUID.
- Treating checkpoint load failures as inactive status would silently route users into regular chat and hide data loss risk.
- Persisting chat transcript only in checkpoint and not `messages` would make the UI lose history on refresh.
- Passing stale page-local `brainstormSessionId` after route changes could append messages to the wrong session.
- Updating checkpoint before the agent response is finalized could leave a half-turn as the latest state.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story-1.4-Resume-Persisted-Brainstorm-State]
- [Source: _bmad-output/planning-artifacts/prd.md#Journey-2-Session-Abandoned-and-Resumed]
- [Source: _bmad-output/planning-artifacts/architecture.md#LangGraph-State-Machine]
- [Source: _bmad-output/planning-artifacts/architecture.md#Session-Persistence-Checkpointing]
- [Source: _bmad-output/planning-artifacts/architecture.md#Frontend-Integration]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Journey-4-Session-Abandoned-and-Resumed]
- [Source: _bmad-output/implementation-artifacts/1-3-detect-existing-brainstorm-session.md]
- [Source: _bmad-output/implementation-artifacts/1-2-start-brainstorm-from-package-chat.md#Dev-Agent-Record]

## Project Structure Notes

- This story is mostly backend/agent state plumbing plus small frontend request-shape changes.
- Keep resume behavior layered: frontend calls backend, backend verifies package access, backend calls agent, agent loads/checkpoints state.
- The existing message table remains the source for displayed chat transcript; checkpoint state is the source for agent continuity and metadata.

## Dev Agent Record

### Agent Model Used

glm-5.1 (zai-coding-plan/glm-5.1)

### Debug Log References

### Completion Notes List

- Ultimate context engine analysis completed - comprehensive developer guide created.
- Task 1: Story 1.3 status contract verified - endpoint, schema, and package access all in place from previous story.
- Task 2: Session continuity already wired through Stories 1.2/1.3 - BrainstormMessageCreate has session_id, frontend sends it, backend forwards it. Agent now verifies package/project ownership of resumed sessions.
- Task 3: Added get_brainstorm_state_by_session() helper to agent/checkpoint.py with CheckpointError exception class for controlled failure handling.
- Task 4: Rewrote brainstorm_message endpoint to load existing state by session_id or active package session, append user+assistant messages, persist updated state, and return full metadata. Ownership verification prevents cross-package session reuse.
- Task 5: Frontend already handles resume via Story 1.3 status loading (sets brainstormSessionId/brainstormPhase), passes session_id to sends, clears on navigation.
- Task 6: All checkpoint functions wrapped with CheckpointError handling. Agent endpoint catches CheckpointError and returns controlled 500 with standard error detail. Failed saves do not corrupt prior state (upsert only writes on success).
- Task 7: Added 8 agent tests (resume by session, resume by active package, wrong package/project rejection, checkpoint load/save/active-package failure, new session save failure) and 5 backend tests (session_id forwarding, cross-org resume blocked, agent error mapping, regular messages preserved, message persistence). All 119 tests pass (26 agent + 93 backend) and npm run check clean.

### File List

- agent/checkpoint.py (modified: added CheckpointError, get_brainstorm_state_by_session, wrapped all functions with error handling)
- agent/main.py (modified: rewrote brainstorm_message with resume logic, ownership verification, error handling, added CheckpointError import)
- agent/tests/test_brainstorm.py (modified: added get_brainstorm_state_by_session fake to fixture, updated test_brainstorm_first_message_persists_initial_state for new state shape, added 8 new tests)
- thagid/tests/test_brainstorm.py (modified: added 5 new tests for resume behavior)
