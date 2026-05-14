# Story 1.2: Start Brainstorm From Package Chat

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a package user,
I want to start a brainstorm session from package chat,
so that I can begin ideating without leaving the scoped package workspace.

## Acceptance Criteria

1. Given I am viewing an authenticated package chat, when I send a message that starts a brainstorm session, then the frontend calls `/api/packages/{package_id}/brainstorm/message`, and the backend verifies package access before forwarding to the agent.
2. Given no active brainstorm session exists for the package, when the agent receives the first brainstorm message, then it creates a new brainstorm state with package id, messages, empty ideas, empty documents, and no active technique, and the response includes a session id and current phase.
3. Given a brainstorm session has started, when the chat renders the agent response, then the package chat shows brainstorm mode with the correct phase badge, and the message log remains accessible with `role="log"` and `aria-live="polite"`.

## Tasks / Subtasks

- [x] Add backend brainstorm proxy endpoint (AC: 1)
  - [x] Create `thagid/schemas/brainstorm.py` with request/response schemas for browser-facing brainstorm messages.
  - [x] Create `thagid/routers/brainstorm.py` with `POST /api/packages/{package_id}/brainstorm/message`, JWT auth, package access verification, and agent forwarding.
  - [x] Include the new router in `thagid/main.py`.
  - [x] Preserve `POST /api/packages/{package_id}/messages` as the regular non-brainstorm echo path.
- [x] Extend backend agent client for brainstorm messages (AC: 1, 2)
  - [x] Extend `thagid/services/agent_client.py` beyond health checks to call the agent message endpoint using configured `AGENT_SERVICE_URL` and `X-Agent-Key`.
  - [x] Backend must derive `project_id` from the authorized package/project relationship, not trust a frontend-supplied project id.
  - [x] Forward the internal request shape documented in architecture: `message`, `package_id`, `project_id`, `session_id`, and `context` with technique, idea_count, and message_count.
  - [x] Map agent failures to `{"detail": "Brainstorm agent encountered an error. Please try again."}` without leaking internal errors to the browser.
- [x] Persist brainstorm chat messages through the existing message table (AC: 1, 3)
  - [x] Save the user's brainstorm-start message as a `Message` with role `user`.
  - [x] Save the agent reply as a `Message` with role `assistant`.
  - [x] Return the assistant message plus brainstorm metadata needed by the frontend; do not return SQLAlchemy models directly.
  - [x] Keep existing message ordering and regular message tests passing.
- [x] Add minimal agent-side brainstorm start endpoint (AC: 2)
  - [x] Add an internal agent endpoint, for example `POST /internal/agent/brainstorm/message`, protected by the existing `X-Agent-Key` dependency.
  - [x] On first message with `session_id: null`, create a UUID session id and initial state containing `package_id`, message history including the user message, empty `ideas`, empty `themes`, empty `active_documents`, `summary: null`, `technique: null`, and current phase `initiate`.
  - [x] Persist the initial state using the checkpoint storage prepared in Story 1.1.
  - [x] Return a deterministic starter reply, `session_id`, and current phase. Do not implement technique recommendation, technique picker behavior, idea reducers, KG writes, extraction, validation, markdown rendering, file upload, or URL ingestion in this story.
- [x] Add frontend brainstorm API and types (AC: 1, 3)
  - [x] Add `web/src/lib/types/brainstorm.ts` for phase and response types.
  - [x] Add `web/src/lib/api/brainstorm.ts` using `$lib/api/client.ts`; do not call `fetch()` directly from Svelte components.
  - [x] Ensure the browser-facing response uses snake_case fields from the backend and maps safely into TypeScript types.
- [x] Update package chat UI for started brainstorm sessions (AC: 1, 3)
  - [x] Update `web/src/routes/project/[id]/package/[pkgId]/+page.svelte` so brainstorm sends call the new brainstorm API path while regular chat still uses `sendMessage`.
  - [x] Update `ChatInterface.svelte` to accept optional brainstorm phase/session metadata and render a phase badge only when brainstorm mode is active.
  - [x] Add `BrainstormPhaseBadge.svelte` under `$lib/components/custom/` or extend existing badge patterns without modifying shadcn-managed `ui/` components.
  - [x] Add a minimal `StreamingIndicator.svelte` or equivalent in `ChatInterface.svelte` so brainstorm sends show an assistant-side loading state while waiting for the agent response.
  - [x] Preserve the message area `role="log"` and `aria-live="polite"`, Enter-to-send, Shift+Enter newline, auto-scroll, and optimistic user message behavior.
- [x] Add tests and verification (AC: 1, 2, 3)
  - [x] Add backend tests for authenticated brainstorm start success, unauthenticated rejection, package-not-found, invalid package id, and cross-org forbidden access.
  - [x] Add backend tests proving agent calls include `X-Agent-Key`, use the configured agent URL, and map agent errors to the standard user-facing detail.
  - [x] Add agent tests for missing/invalid `X-Agent-Key`, first-message state creation, returned `session_id`, returned phase, and empty initial ideas/documents/technique.
  - [x] Add frontend unit tests if existing test patterns make that practical; otherwise at minimum run `cd web && npm run check`.
  - [x] Run `pytest`, agent tests, and `cd web && npm run check`.

### Review Findings

- [x] [Review][Patch] Agent endpoint does not create or persist the required initial brainstorm state [agent/main.py:51]
- [x] [Review][Patch] Agent response omits required initial state fields such as active documents and technique [agent/main.py:58]
- [x] [Review][Patch] Follow-up brainstorm messages never send the stored session id back to the backend or agent [web/src/routes/project/[id]/package/[pkgId]/+page.svelte:65]
- [x] [Review][Patch] Frontend starts brainstorms via message content command detection instead of a brainstorm-specific affordance/state [web/src/routes/project/[id]/package/[pkgId]/+page.svelte:65]
- [x] [Review][Patch] Brainstorm mode/session state is not reset when the package route changes [web/src/routes/project/[id]/package/[pkgId]/+page.svelte:20]
- [x] [Review][Patch] Malformed successful agent responses are not mapped to the standard agent error path [thagid/services/brainstorm.py:39]
- [x] [Review][Patch] Backend accepts any phase string while the frontend assumes a fixed phase union [thagid/schemas/brainstorm.py:21]
- [x] [Review][Patch] Tests do not prove the agent client uses configured URL and `X-Agent-Key` headers [thagid/tests/test_brainstorm.py:204]

## Dev Notes

### Scope Boundaries

- This story starts a brainstorm session from package chat. It does not detect existing brainstorm sessions on page load; that is Story 1.3.
- This story creates the first brainstorm state and phase metadata. It does not resume prior checkpoints; that is Story 1.4.
- This story may display a phase badge and streaming/loading state. Broader shell alignment, breadcrumb/sidebar polish, focus-order cleanup, and reduced-motion hardening belong to Story 1.5 unless directly required to keep this story working.
- Do not implement Epic 2 features here: technique recommendation, technique selection, technique swapping, idea management, file upload, URL sharing, rolling summary, or anti-bias pivots.
- Do not implement Epic 3 or Epic 4 features: theme grouping, KG writes, validation, embeddings, markdown rendering, summary cards, or results detail views.

### Required Start Behavior

- The start path must be deterministic. Do not use fragile keyword detection inside the backend such as checking if a normal message contains "brainstorm".
- The frontend should call the brainstorm API only from a brainstorm-specific UI path/state. If a trigger is needed, use the package-chat brainstorm welcome/start affordance from the design spec rather than replacing all regular package chat sends.
- Regular package messages must continue using `$lib/api/messages.ts` and `/api/packages/{package_id}/messages`.

### Current Codebase State

- `web/src/routes/project/[id]/package/[pkgId]/+page.svelte` currently loads package details and messages, optimistically appends a user message, then calls `sendMessage` from `$lib/api/messages` and appends the returned assistant message.
- `ChatInterface.svelte` currently renders package title/description, `StatusBadge`, message log with `role="log"` and `aria-live="polite"`, an auto-growing textarea, Enter-to-send, Shift+Enter newline, and a send button.
- `ChatBubble.svelte` currently supports only simple `Message` text for `user` and `assistant` roles.
- `web/src/lib/api/messages.ts` uses `apiFetch`; maintain this API-client pattern for brainstorm.
- `thagid/routers/messages.py` currently verifies package access in a router-local helper, saves echo messages through `thagid/services/message.py`, and returns only the assistant message for POST.
- `thagid/services/message.py` currently persists both user and assistant rows for regular echo chat; list ordering is ascending by `created_at` then `id`.
- `thagid/services/agent_client.py` currently only exposes `agent_health()` using `settings.AGENT_SERVICE_URL` and `X-Agent-Key`.
- `agent/main.py` currently has only `/internal/agent/health` protected by `verify_agent_key`.

### Previous Story Intelligence

- Story 1.1 is in review and completed the runtime foundation: custom PostgreSQL image with AGE and pgvector, `thagid-agent` FastAPI service, `agent_checkpoints` schema, `thagid/services/agent_client.py`, and tests.
- Story 1.1 verified missing/invalid agent keys return 401 and valid keys return 200 on `/internal/agent/health`; reuse `verify_agent_key` for the new agent brainstorm endpoint.
- Story 1.1 notes that host curl can fail due to Podman pasta networking, but in-container agent verification works. For this story, prefer ASGI/httpx tests for unit coverage and compose/internal network checks only when feasible.
- Story 1.1 added approved dependencies including LangGraph checkpointing; use the existing dependency set and do not introduce new runtime libraries without approval.

### Architecture Requirements

- Browser-facing brainstorm chat endpoint is `POST /api/packages/{package_id}/brainstorm/message`, JWT-authenticated and proxied through FastAPI. [Source: _bmad-output/planning-artifacts/architecture.md#Frontend-Integration]
- Frontend traffic must never call `thagid-agent` directly; FastAPI is the gateway/proxy. [Source: _bmad-output/planning-artifacts/architecture.md#Architectural-Boundaries]
- FastAPI authenticates the user, verifies package ownership, forwards to `thagid-agent`, saves the message pair to the existing `Message` model, and returns the response. [Source: _bmad-output/planning-artifacts/architecture.md#Frontend-Integration]
- Agent-backend internal requests use `X-Agent-Key` and synchronous HTTP. [Source: _bmad-output/planning-artifacts/architecture.md#Communication-Patterns]
- The internal request to the agent should carry `message`, `package_id`, `project_id`, `session_id`, and `context` with current technique, idea_count, and message_count. [Source: _bmad-output/planning-artifacts/architecture.md#Agent-Backend-HTTP-Contract]
- The internal agent response should include reply text, `session_id`, current state/phase, and empty lists/null values for fields not yet implemented. [Source: _bmad-output/planning-artifacts/architecture.md#Agent-Backend-HTTP-Contract]
- Initial LangGraph state shape includes `package_id`, `technique`, `messages`, `ideas`, `themes`, `active_documents`, `summary`, and `session_id`. [Source: _bmad-output/planning-artifacts/architecture.md#LangGraph-State-Machine]

### API Contract Guidance

- Browser request: `{"content": "..."}` is sufficient for this story unless the frontend needs to send an explicit `session_id` after the first response.
- Browser response should include at least `message`, `session_id`, and `phase`, where `message` is the saved assistant message using the existing message response shape.
- Use phase value `initiate` for the first created brainstorm state. If using architecture's `state_change` field internally, map it to browser-facing `phase` consistently.
- Backend should save the browser user's content before or atomically with the assistant reply. If the agent call fails after saving the user message, either roll back both rows or document and test the chosen behavior; do not silently create half-conversations unintentionally.
- Use existing API error conventions: validation errors remain 422, auth remains 401, forbidden package access remains 403, not found remains 404, and agent/internal failures become a 500-level standard detail.

### Frontend UX Requirements

- Package chat remains the defining workspace with sticky chat header, scrollable message log, sticky bottom textarea, send button, and auto-scroll to latest message. [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Component-Strategy]
- `BrainstormPhaseBadge` variants must support at least `initiate`, with later-compatible variants for `facilitate`, `extract`, `validate`, `markdown`, and `concluded`. [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Component-Strategy]
- Chat bubbles must preserve user right-aligned primary bubbles and assistant left-aligned neutral bubbles. [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Component-Strategy]
- Streaming/loading state for brainstorm responses should use the assistant bubble visual language with dot pulse or simple equivalent. [Source: design-system/thagid/pages/package-chat.md#Streaming-Indicator]
- Empty/no-active brainstorm wording from the design spec: "I'm your brainstorm facilitator. I can help you generate and organize ideas for this package. Want to start a brainstorm session?" [Source: design-system/thagid/pages/package-chat.md#Empty-Chat-State]
- Preserve `role="log"` and `aria-live="polite"` on the message area. [Source: design-system/thagid/pages/package-chat.md#Message-Area]

### File Structure Requirements

- Backend new/update files likely include `thagid/routers/brainstorm.py`, `thagid/schemas/brainstorm.py`, `thagid/services/agent_client.py`, `thagid/services/message.py`, `thagid/main.py`, and `thagid/tests/test_brainstorm.py`.
- Agent updates likely include `agent/main.py` and new tests under `agent/tests/`.
- Frontend new/update files likely include `web/src/lib/api/brainstorm.ts`, `web/src/lib/types/brainstorm.ts`, `web/src/lib/components/custom/BrainstormPhaseBadge.svelte`, optional `web/src/lib/components/custom/StreamingIndicator.svelte`, `web/src/lib/components/custom/ChatInterface.svelte`, and `web/src/routes/project/[id]/package/[pkgId]/+page.svelte`.
- Do not modify shadcn-managed files under `web/src/lib/components/ui/`.
- Do not add new database tables for sessions in this story unless required by checkpoint persistence; the initial brainstorm state belongs in checkpoint storage, and chat transcript rows belong in the existing `messages` table.

### Testing Requirements

- Existing backend tests use pytest, pytest-asyncio, SQLite in-memory sessions, and httpx ASGI clients. Follow that style.
- Existing agent tests use FastAPI `TestClient` and mutate `agent.config.settings.AGENT_KEY`; reuse that style where possible.
- Mock the backend agent HTTP call in router/service tests rather than requiring the agent container for standard `pytest`.
- Add coverage that regular `/api/packages/{package_id}/messages` still echoes and persists two rows.
- Add coverage that `/api/packages/{package_id}/brainstorm/message` uses package authorization and does not forward to the agent when access is invalid.
- Add coverage for blank content validation matching existing message behavior.
- Frontend verification should include `cd web && npm run check`; add focused unit tests only if they fit existing project test patterns.

### Regression Risks

- Replacing the regular chat send path wholesale would break the existing echo chat behavior and tests.
- Trusting `project_id` from the browser could cross project/org boundaries; derive it server-side from the authorized package.
- Returning only a raw agent response would bypass existing message persistence and make refresh lose the conversation.
- Adding direct frontend calls to `thagid-agent` would violate the container and security boundary.
- Implementing technique recommendations in this story would overlap Story 2.1 and create unclear acceptance boundaries.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story-1.2-Start-Brainstorm-From-Package-Chat]
- [Source: _bmad-output/planning-artifacts/prd.md#Brainstorm-Session-Management]
- [Source: _bmad-output/planning-artifacts/prd.md#Frontend-Chat-Interface]
- [Source: _bmad-output/planning-artifacts/architecture.md#Frontend-Integration]
- [Source: _bmad-output/planning-artifacts/architecture.md#Agent-Backend-HTTP-Contract]
- [Source: _bmad-output/planning-artifacts/architecture.md#LangGraph-State-Machine]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Journey-3-First-Brainstorm-Session]
- [Source: design-system/thagid/pages/package-chat.md]
- [Source: _bmad-output/implementation-artifacts/1-1-brainstorm-runtime-foundation.md#Dev-Agent-Record]

## Project Structure Notes

- This story should extend existing chat files instead of replacing them. The safest path is additive: new brainstorm API/types/router/schema, small additions to the package chat page, and optional small custom phase/loading components.
- The existing `Message` type has only `id`, `content`, `role`, `package_id`, and `created_at`; brainstorm metadata should live in brainstorm response types, not be forced into the generic `Message` shape unless the data model is intentionally expanded.
- Existing design-system docs now use navy primary `#0A3B85`; if older project-context references cyan, follow the current design system and package-chat page docs.

## Dev Agent Record

### Agent Model Used

glm-5.1

### Debug Log References

- Mock for `response.raise_for_status()` and `response.json()` needed to use `MagicMock` (sync) not `AsyncMock` since httpx.Response methods are synchronous.

### Completion Notes List

- Ultimate context engine analysis completed - comprehensive developer guide created.
- Created `thagid/schemas/brainstorm.py` with `BrainstormMessageCreate` and `BrainstormMessageResponse` schemas following existing message schema patterns.
- Created `thagid/routers/brainstorm.py` with `POST /api/packages/{package_id}/brainstorm/message` endpoint reusing `verify_package_access` pattern. Derives `project_id` server-side from authorized package/project relationship.
- Extended `thagid/services/agent_client.py` with `agent_brainstorm_message()` forwarding the architecture-defined request shape including `message`, `package_id`, `project_id`, `session_id`, and `context`. Timeout increased to 120s for LLM calls.
- Created `thagid/services/brainstorm.py` orchestrating user message save, agent call, assistant message save with rollback on agent failure, and Pydantic response mapping.
- Added brainstorm router to `thagid/main.py`. Regular messages router preserved unchanged.
- Added `POST /internal/agent/brainstorm/message` to `agent/main.py` with Pydantic request model. Creates UUID session_id on first message, returns deterministic starter reply with `state_change: "initiate"`, empty ideas/themes/markdown.
- Created `web/src/lib/types/brainstorm.ts` with `BrainstormPhase` type and `BrainstormMessageResponse` interface.
- Created `web/src/lib/api/brainstorm.ts` using `apiFetch` wrapper pattern.
- Created `BrainstormPhaseBadge.svelte` with phase-to-color mapping for all 6 phases.
- Updated `ChatInterface.svelte` with optional brainstorm phase/session props, phase badge rendering, and dot-pulse streaming indicator. Preserved `role="log"`, `aria-live="polite"`, Enter-to-send, Shift+Enter newline, auto-scroll, optimistic user message.
- Updated package chat page to call brainstorm API when brainstorm is active or triggered via `/brainstorm` prefix, while regular chat continues using `sendMessage`.
- Backend tests: 10 tests covering success flow, message persistence, auth rejection, 404, invalid ID, cross-org forbidden, empty content, agent error mapping, agent call verification, and regular message regression.
- Agent tests: 6 tests covering missing key, invalid key, first message session creation, session_id format, existing session_id preservation, and empty initial state.
- All 75 backend tests pass, 11 agent tests pass, `npm run check` passes with 0 errors.

### File List

New files:
- thagid/schemas/brainstorm.py
- thagid/routers/brainstorm.py
- thagid/services/brainstorm.py
- thagid/tests/test_brainstorm.py
- agent/tests/test_brainstorm.py
- web/src/lib/types/brainstorm.ts
- web/src/lib/api/brainstorm.ts
- web/src/lib/components/custom/BrainstormPhaseBadge.svelte

Modified files:
- thagid/services/agent_client.py
- thagid/main.py
- agent/main.py
- web/src/lib/components/custom/ChatInterface.svelte
- web/src/routes/project/[id]/package/[pkgId]/+page.svelte
