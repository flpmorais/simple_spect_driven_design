# Story 2.1: Technique Recommendation at Session Initiation

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a package user,
I want the brainstorm agent to recommend relevant techniques when a session begins,
so that I can start ideating with useful guidance instead of choosing blindly.

## Acceptance Criteria

1. Given a brainstorm session enters the initiate phase, when the agent reads the package context available to it, then it recommends one or more techniques with concise reasons, and the recommendation appears in the first brainstorm response.
2. Given recommended techniques are shown in chat, when I choose a recommendation, then the selected technique is stored in brainstorm state, and the session can move into the facilitate phase.
3. Given the recommendation cannot be generated, when the agent handles the initiation, then it falls back to a safe default technique, and explains that the user can change it.

## Tasks / Subtasks

- [x] Add brainstorm technique reference persistence (AC: 1, 3)
  - [x] Add the next Alembic migration after `006_add_messages_table.py` for a `brainstorm_techniques` reference table.
  - [x] Add a SQLAlchemy model under `thagid/models/` and export it from `thagid/models/__init__.py`.
  - [x] Seed all rows from `.agents/skills/bmad-brainstorming/brain-methods.csv` using `category`, `technique_name`, and `description`.
  - [x] Do not store techniques in the knowledge graph; this is a relational reference table.
  - [x] Resolve or explicitly document the current source-count mismatch: planning docs say 62 techniques, but the CSV currently parses as 61 records.
- [x] Expose package context and technique data to the agent without breaking container boundaries (AC: 1, 3)
  - [x] Reuse FastAPI as the gateway; the agent must not import backend services or models directly.
  - [x] Add the smallest internal backend endpoint/service needed for the agent to read package title/description and candidate techniques over HTTP with `X-Agent-Key`.
  - [x] Keep browser-facing endpoints JWT-authenticated and keep internal endpoints protected by `X-Agent-Key`.
  - [x] Reuse existing package access and project/package identifiers already passed through the brainstorm request path.
- [x] Recommend techniques when a new brainstorm session is initiated (AC: 1, 3)
  - [x] Update `agent/main.py` new-session path so the first assistant reply includes one or more recommended technique names and concise reasons based on package context.
  - [x] Persist recommended techniques in checkpoint state if needed for later selection validation; do not remove existing state fields.
  - [x] Set a safe default technique if package context or recommendation generation fails.
  - [x] Keep `phase` as `initiate` until the user chooses a recommendation.
  - [x] Keep `ideas`, `themes`, `active_documents`, `summary`, and `messages` initialized as in Stories 1.2-1.4.
- [x] Allow choosing a recommended technique through the existing brainstorm flow (AC: 2)
  - [x] Use the existing `POST /api/packages/{package_id}/brainstorm/message` flow unless a minimal request/response extension is unavoidable.
  - [x] On selection, validate the technique against the reference list or session recommendations.
  - [x] Store the selected technique in checkpoint state as `technique`.
  - [x] Move the session to `facilitate` after successful selection and return `state_change`/`phase` as `facilitate`.
  - [x] Preserve existing resume behavior by session ID and active package checkpoint.
- [x] Render recommendations in package chat with a minimal UX (AC: 1, 2)
  - [x] Show recommendations in the first brainstorm assistant response as readable text at minimum.
  - [x] If adding inline cards/buttons, keep them inside existing assistant chat bubble patterns and wire `Use this` to the existing brainstorm message flow.
  - [x] Do not implement the full `TechniquePickerModal`, browse-all path, search/filter, or mid-session swap; those belong to Story 2.2.
  - [x] Preserve the chat header, phase badge, regular chat endpoint, and package navigation behavior from Story 1.5.
- [x] Add focused tests and verification (AC: 1, 2, 3)
  - [x] Add/adjust agent tests for first-response recommendations, fallback default, selected technique persistence, and transition to `facilitate`.
  - [x] Add backend tests for any internal context/technique endpoint and for `X-Agent-Key` protection.
  - [x] Add migration/model tests if the project has an established pattern for migration/reference data checks.
  - [x] Run relevant Python tests, including `pytest agent/tests/test_brainstorm.py`.
  - [x] If frontend files are touched, run `cd web && npm run check` and relevant Vitest tests.

## Dev Notes

### Scope Boundaries

- This story is only technique recommendation at session initiation plus accepting one recommendation.
- Do not implement Story 2.2 scope: full technique picker modal, browse/search/filter across all techniques, or mid-session technique swap.
- Do not implement Story 2.3+ scope: real-time idea extraction/reducer, anti-bias domain pivoting during facilitation, rolling summary, uploads, URLs, theme grouping, KG writes, embeddings, markdown rendering, summary cards, or detail pages.
- Do not introduce a new frontend framework, backend architecture component, or external library. Use existing FastAPI, SQLAlchemy/Alembic, async HTTP, SvelteKit, and current shadcn-svelte patterns.
- Keep changes surgical. Extend current files and contracts rather than replacing the prototype brainstorm runtime.

### Current Codebase State

- `agent/main.py` currently implements `/internal/agent/brainstorm/message` and `/internal/agent/brainstorm/status` with `X-Agent-Key` auth.
- New brainstorm sessions currently create checkpoint state with `technique: None`, `phase: "initiate"`, empty `ideas`, `themes`, `active_documents`, `summary: None`, and an opening generic facilitator reply.
- Existing session messages currently append the user message, return a generic continuation reply, preserve the existing phase, and save the checkpoint.
- `agent/checkpoint.py` persists state JSON under `agent_checkpoints.brainstorm_states` and merges concurrent message appends.
- `thagid/routers/brainstorm.py` exposes browser endpoints under `/api/packages/{package_id}/brainstorm/...`, verifies package access, and delegates to `thagid/services/brainstorm.py`.
- `thagid/services/brainstorm.py` persists displayed chat transcript to the existing `messages` table and validates agent response fields: `reply`, `session_id`, `state_change`, `technique`, `ideas`, and `message_count`.
- `thagid/services/agent_client.py` is the backend HTTP client to the agent and injects `X-Agent-Key`.
- `thagid/schemas/brainstorm.py` and `web/src/lib/types/brainstorm.ts` currently expose `phase`, optional `technique`, `idea_count`, and `message_count` only.
- `web/src/routes/project/[id]/package/[pkgId]/+page.svelte` loads package/messages/status, clears stale brainstorm state on package navigation, starts brainstorm via `sendBrainstormMessage`, and preserves regular chat through `/messages` when brainstorm mode is inactive.
- `web/src/lib/components/custom/ChatInterface.svelte` renders the existing package chat shell, brainstorm start CTA, phase badge, technique pill, idea/message counts, chat log, and input.
- `web/src/lib/components/custom/ChatBubble.svelte` is the existing assistant/user message renderer; use it or extend it minimally if rendering inline recommendation cards.

### Required Implementation Behavior

- Initiation must read package context available to the agent. The architecture describes package description from KG, but the current prototype has package title/description in relational tables; use the current package model through a backend internal API until KG package context exists.
- The first brainstorm assistant reply must include recommendation content in the persisted `messages` transcript so reload/resume still shows what was recommended.
- Technique selection can be implemented by the user sending a normal message such as `Use SCAMPER Method` through the existing brainstorm message endpoint. If a button is added, it should submit that same message path rather than adding a separate browser endpoint.
- On technique selection, checkpoint state must store the selected technique in `technique` and change `phase` to `facilitate`.
- Status responses must continue to show the active session and selected technique using the existing `GET /api/packages/{package_id}/brainstorm/status` contract.
- Fallback behavior must still produce a usable first response, choose a safe default technique, and tell the user they can change it later. A reasonable default from the CSV is `SCAMPER Method` because it is structured, general-purpose, and already appears in package-chat design examples.
- Do not fail session creation just because package context retrieval or recommendation ranking fails. Log the failure, fall back, save a valid checkpoint, and return the standard brainstorm response shape.

### Technique Reference Requirements

- Source CSV: `.agents/skills/bmad-brainstorming/brain-methods.csv` with columns `category`, `technique_name`, `description`.
- PRD and architecture state that there are 62 techniques and that they should be stored as a database reference table, not in KG.
- The current CSV parses as 61 records. Do not silently hard-code either count. Seed every CSV row and add a test or migration note that makes the discrepancy visible for product follow-up.
- Use stable technique names from the CSV for display and persisted state. Do not invent slug names unless the table needs a separate unique slug for constraints.
- Keep descriptions available for recommendation reasons and future Story 2.2 picker/search work.

### Backend And Agent Contract Guardrails

- Browser must continue calling only FastAPI `/api/...` endpoints; it must not call `thagid-agent` directly.
- Internal agent/backend traffic must continue using `X-Agent-Key`.
- Existing regular chat endpoint `/api/packages/{package_id}/messages` must remain unchanged for non-brainstorm chat.
- Existing brainstorm request/response fields must remain backward-compatible for Stories 1.2-1.5: `message`, `session_id`, `phase`, `technique`, `idea_count`, and `message_count`.
- If adding recommendation metadata to agent/backend/frontend responses, make it optional so existing callers/tests still pass and persisted text remains the source for reload readability.
- Preserve checkpoint validation rules in `agent/main.py`; if new state fields are added, existing checkpoints without them must still resume.
- Do not bypass FastAPI by importing `thagid.services.*` from the agent container. Architecture explicitly marks that as an anti-pattern.

### UX Requirements

- Follow `design-system/thagid/MASTER.md` and `design-system/thagid/pages/package-chat.md` if editing UI.
- Recommended techniques appear in the first brainstorm assistant message.
- Technique recommendation cards, if implemented in this story, should be compact content inside assistant bubbles with technique name, short description/reason, and a `Use this` ghost button.
- The `Use this` action should update button text/state to selected if practical, and should trigger the same brainstorm flow that stores technique and transitions to `facilitate`.
- Keep `BrainstormPhaseBadge` labels and phase values unchanged: `initiate`, `facilitate`, `extract`, `validate`, `markdown`, `concluded`.
- Preserve `role="log"` and `aria-live="polite"` on the chat message area.
- Preserve reduced-motion handling added in Story 1.5.

### Testing Requirements

- Existing agent tests in `agent/tests/test_brainstorm.py` assert first-message behavior, initial state shape, status behavior, resume by session ID, active package resume, rejected wrong package/project, checkpoint failures, terminal checkpoint restart, and message merge behavior. Update expectations deliberately where the opening reply now includes recommendations and/or default technique behavior.
- Add tests that prove new-session initiation saves recommendation text in `state["messages"]` and returns it as `reply`.
- Add tests that prove fallback recommendation still saves a valid checkpoint and returns `state_change == "initiate"` unless the user has selected a technique.
- Add tests that prove selecting a recommended technique stores `state["technique"]`, appends both user and assistant messages, and returns `state_change == "facilitate"`.
- Add tests that prove status reports selected technique and phase after selection.
- Add tests for any internal package-context/technique endpoint covering valid `X-Agent-Key`, missing/invalid key, package lookup success, and missing package behavior.
- If frontend recommendation cards/buttons are added, add focused component or unit tests only where current Svelte/Vitest setup supports them; otherwise document manual verification.

### Previous Story Intelligence

- Story 1.5 completed frontend shell alignment and explicitly deferred technique recommendation, technique picker, technique swapping, file upload, URL sharing, idea cards, and rolling summary.
- Story 1.5 preserved brainstorm API contracts from Stories 1.2-1.4 and did not change backend/agent behavior.
- Story 1.4 established that displayed chat transcript uses the `messages` table, while agent continuity uses `agent_checkpoints` state.
- Story 1.4 established frontend status/resume wiring: package open loads status, sets `brainstormSessionId`/`brainstormPhase`, sends `session_id` on brainstorm messages, and clears stale session data on navigation.
- Story 1.3 added active brainstorm detection through the status endpoint.
- Story 1.2 added brainstorm start CTA, phase badge, streaming indicator, and brainstorm message path.
- Recent git history includes `fix: harden brainstorm resume checkpoints`, `feat: detect existing brainstorm sessions`, `feat: start brainstorm sessions from package chat`, and `feat: add brainstorm runtime foundation`; do not regress those behaviors.

### File Structure Requirements

- Likely backend/model updates: `migrations/versions/007_add_brainstorm_techniques_table.py`, `thagid/models/technique.py`, `thagid/models/__init__.py`, possibly `thagid/schemas/technique.py` or additions to `thagid/schemas/brainstorm.py`.
- Likely backend service/router updates: a small internal backend route/service for package context and techniques, plus registration wherever routers are included.
- Likely agent updates: `agent/main.py` for initiation, selection handling, fallback, and response shape; possibly a small helper module under `agent/` if keeping the logic in `main.py` becomes unclear.
- Likely frontend updates only if rendering cards/buttons: `web/src/lib/types/brainstorm.ts`, `web/src/lib/api/brainstorm.ts`, `web/src/lib/components/custom/ChatBubble.svelte`, `web/src/lib/components/custom/ChatInterface.svelte`, and package page wiring.
- Avoid creating the full architecture skeleton from planning docs (`agent/brainstorm/graph.py`, node folders, tools) unless this story truly requires it; the current prototype has working endpoints in `agent/main.py`.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story-2.1-Technique-Recommendation-at-Session-Initiation]
- [Source: _bmad-output/planning-artifacts/prd.md#Migration-Source-BMAD-Brainstorming-Skill]
- [Source: _bmad-output/planning-artifacts/prd.md#Migration-Mapping]
- [Source: _bmad-output/planning-artifacts/prd.md#Brainstorm-Ideation]
- [Source: _bmad-output/planning-artifacts/architecture.md#Agent-State-Machine]
- [Source: _bmad-output/planning-artifacts/architecture.md#Frontend-Integration]
- [Source: _bmad-output/planning-artifacts/architecture.md#Pattern-Examples]
- [Source: _bmad-output/planning-artifacts/architecture.md#Project-Structure-Boundaries]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Technique-Selection-FR6-FR9]
- [Source: design-system/thagid/pages/package-chat.md#Brainstorm-Specific-Interactions]
- [Source: .agents/skills/bmad-brainstorming/brain-methods.csv]
- [Source: _bmad-output/implementation-artifacts/1-5-brainstorm-chat-shell-ux-alignment.md#Previous-Story-Intelligence]

## Project Structure Notes

- The architecture document shows a future LangGraph package layout, but the implemented prototype currently centralizes brainstorm behavior in `agent/main.py`. For this story, extend the prototype unless a small helper is needed for clarity.
- The model/migration naming should follow the current numeric migration sequence and simple SQLAlchemy model style.
- Keep reference data relational because future Story 2.2 needs searchable/filterable technique data and architecture says not to store techniques in KG.

## Dev Agent Record

### Agent Model Used

gpt-5.5

### Debug Log References

### Completion Notes List

- Ultimate context engine analysis completed - comprehensive developer guide created.
- Added migration 007 with brainstorm_techniques table seeded with all 61 CSV rows; documented PRD count discrepancy (62 vs 61).
- Added internal backend endpoint `GET /internal/backend/packages/{id}/context` returning package title, description, and techniques, protected by X-Agent-Key.
- Updated agent new-session path to fetch package context, generate keyword-based technique recommendations, and include them in the first reply. Falls back to SCAMPER Method on failure.
- Added technique selection via "Use X" message pattern during initiate phase. Validates against session recommendations, stores technique, transitions to facilitate.
- Updated ChatBubble to render basic markdown (bold, code, line breaks) in assistant messages for readable recommendation text.
- All 138 tests pass (32 agent + 106 backend). Frontend svelte-check passes with 0 errors.

### Change Log

- 2026-05-10: Implemented technique recommendation at session initiation, technique selection, and internal context endpoint.

### File List

- `migrations/versions/007_add_brainstorm_techniques_table.py` (new)
- `thagid/models/technique.py` (new)
- `thagid/models/__init__.py` (modified)
- `thagid/schemas/technique.py` (new)
- `thagid/services/technique.py` (new)
- `thagid/routers/internal.py` (new)
- `thagid/main.py` (modified)
- `thagid/config.py` (unchanged, already has AGENT_KEY)
- `migrations/env.py` (modified)
- `agent/main.py` (modified)
- `agent/config.py` (modified)
- `agent/backend_client.py` (new)
- `compose.yml` (modified)
- `agent/tests/test_brainstorm.py` (modified)
- `thagid/tests/test_internal.py` (new)
- `web/src/lib/components/custom/ChatBubble.svelte` (modified)
- `web/src/lib/components/custom/ChatInterface.svelte` (modified)

### Review Findings

- [x] [Review][Patch] Fallback should auto-store SCAMPER while remaining in initiate — Decision: store SCAMPER as the fallback technique, keep `phase` as `initiate`, and tell the user they can change or confirm it. [agent/main.py:326]
- [x] [Review][Patch] Concurrent initiate replies can overwrite a selected technique [agent/checkpoint.py:29]
- [x] [Review][Patch] Empty or whitespace-only input selects the first recommendation [agent/main.py:154]
- [x] [Review][Patch] Partial substring matching can persist an unintended technique [agent/main.py:161]
- [x] [Review][Patch] Initiate sessions without valid saved recommendations can get stuck or crash [agent/main.py:261]
- [x] [Review][Patch] Internal package context lookup does not verify the request project_id [agent/main.py:320]
- [x] [Review][Patch] Recommendation prompt advertises unsupported custom approaches [agent/main.py:150]
- [x] [Review][Patch] Backend context fetch can stall fallback for up to 30 seconds [agent/backend_client.py:14]
