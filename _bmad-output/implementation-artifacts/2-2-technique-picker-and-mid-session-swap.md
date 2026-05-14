# Story 2.2: Technique Picker and Mid-Session Swap

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a package user,
I want to browse and swap brainstorming techniques during facilitation,
so that I can change ideation direction without losing existing ideas.

## Acceptance Criteria

1. Given I open the technique picker, when the modal loads, then I can search and filter the 62 available techniques, and selecting a technique shows its details before confirmation.
2. Given I select a technique from the picker, when I confirm selection, then the modal closes, the active technique updates, and the agent acknowledges the change, and existing ideas remain in state.
3. Given I ask to swap techniques in natural language during facilitation, when the agent handles the request, then it can call the swap technique tool, and the phase remains Facilitate.

## Tasks / Subtasks

- [x] Expose technique list to the browser through FastAPI (AC: 1)
  - [x] Add a JWT-protected browser endpoint under the existing brainstorm/package API boundary, preferably `GET /api/packages/{package_id}/brainstorm/techniques`.
  - [x] Reuse `verify_package_access` from `thagid/routers/brainstorm.py` so users can only browse techniques from packages they can access.
  - [x] Reuse `thagid.services.technique` and `TechniqueItem`; do not duplicate CSV parsing in the frontend or agent.
  - [x] Return all rows from `brainstorm_techniques`, ordered predictably by category and technique name.
  - [x] Do not expose the internal `/internal/backend/...` endpoint to the browser.
- [x] Add frontend technique API/types (AC: 1)
  - [x] Add `TechniqueItem` or equivalent TypeScript type with `technique_name`, `category`, and `description`.
  - [x] Add a frontend API helper in `web/src/lib/api/brainstorm.ts` for the new browser endpoint.
  - [x] Keep existing `BrainstormMessageResponse` and `BrainstormStatusResponse` fields backward-compatible.
- [x] Build `TechniquePicker` modal (AC: 1, 2)
  - [x] Add `web/src/lib/components/custom/TechniquePicker.svelte` using existing shadcn `Dialog`, existing `Input`, and custom list/detail layout.
  - [x] Do not add a new library for `Command`; the repo does not currently have shadcn command components.
  - [x] Implement search by technique name, category, and description.
  - [x] Implement category filter chips with an all/default option.
  - [x] Show a two-column layout on desktop: scrollable list left, selected technique detail right.
  - [x] Show technique name, category badge, description, and a primary full-width `Select Technique` button.
  - [x] Ensure keyboard users can open the modal, search/filter, choose a technique, confirm, and close it.
- [x] Wire picker triggers in package chat (AC: 1, 2)
  - [x] Add a `wand-sparkles` icon button in `ChatInterface.svelte` header when brainstorm mode is active.
  - [x] Add an accessible name such as `Browse brainstorming techniques` and visible focus ring.
  - [x] Keep the existing technique pill, idea count, message count, phase badge, and package status badge.
  - [x] Optionally add a text affordance for `Browse all techniques` in recommendation content only if it can be done without brittle markdown parsing.
- [x] Confirm picker selection through existing brainstorm message flow (AC: 2)
  - [x] On confirmation, close the modal and send a normal brainstorm message such as `Use {technique_name}` through the existing `POST /api/packages/{package_id}/brainstorm/message` path.
  - [x] Update active technique from the existing response `technique` field.
  - [x] Preserve existing optimistic user-message behavior and rollback on send failure.
  - [x] Do not add a separate browser-to-agent endpoint for selection.
- [x] Support mid-session natural-language technique swap in the agent (AC: 2, 3)
  - [x] Extend `agent/main.py` existing-session path for `phase == "facilitate"` to detect natural-language swap intent.
  - [x] Accept direct picker messages like `Use Mind Mapping` and common natural-language variants like `switch to Mind Mapping`, `swap to Mind Mapping`, or `let's try Mind Mapping`.
  - [x] Validate the requested technique against the reference technique list fetched through `agent.backend_client.fetch_package_context`.
  - [x] Update `state["technique"]` to the selected technique and preserve `state["ideas"]`, `state["themes"]`, `state["active_documents"]`, `state["summary"]`, and messages.
  - [x] Return `state_change` as `facilitate`; phase must remain Facilitate after a swap.
  - [x] Reply with confirmation text matching the design intent: `Switching to [technique]. Your existing ideas will be kept.`
  - [x] If the technique is unknown, keep the current technique/phase and ask the user to choose a valid technique without losing state.
- [x] Preserve current Story 2.1 initiation behavior (AC: 1, 2, 3)
  - [x] Keep recommendation generation, fallback default, `recommended_techniques`, and initiate-phase selection behavior working.
  - [x] Do not regress active-session detection, session-id resume, terminal-checkpoint restart, or checkpoint error handling.
  - [x] Do not change regular non-brainstorm chat behavior.
- [x] Add focused tests and verification (AC: 1, 2, 3)
  - [x] Add backend tests for the browser-facing technique list endpoint: authenticated success, unauthenticated rejection, cross-org forbidden, invalid package id, and package not found.
  - [x] Add agent tests for picker-style `Use {technique}` during facilitate, natural-language swap during facilitate, invalid technique during facilitate, and preserving existing ideas.
  - [x] Add frontend tests for the picker modal search/filter/detail/confirm flow if current Svelte Testing Library setup supports it.
  - [x] Run `pytest agent/tests/test_brainstorm.py`.
  - [x] Run relevant backend tests, including `pytest thagid/tests/test_brainstorm.py thagid/tests/test_internal.py` or the full backend test set if practical.
  - [x] Run `cd web && npm run check`; run `cd web && npm run test:unit` if frontend tests are added.

### Review Findings

- [x] [Review][Patch] Picker rejects valid non-recommended techniques during initiate [web/src/lib/components/custom/ChatInterface.svelte:107]
- [x] [Review][Patch] Facilitate messages beginning with `Use ...` are over-classified as technique swaps [agent/main.py:176]
- [x] [Review][Patch] No-result filters can still confirm a hidden fallback technique [web/src/lib/components/custom/TechniquePicker.svelte:41]

## Dev Notes

### Scope Boundaries

- This story adds browse/search/filter technique selection and mid-session technique swap.
- Do not implement Story 2.3 scope: real-time idea extraction, idea reducer, anti-bias domain pivoting prompts, or facilitation quality improvements beyond acknowledging the selected technique.
- Do not implement Story 2.4+ scope: rolling summary, file upload, URL ingestion, theme grouping, KG writes, embeddings, markdown rendering, dashboard summaries, or detail views.
- Do not introduce new libraries. Use existing FastAPI, SQLAlchemy, SvelteKit, shadcn-svelte Dialog/Input/Button/Badge patterns, and lucide icons.
- Do not create a separate browser-to-agent communication path. Browser calls FastAPI only.

### Current Codebase State

- Story 2.1 is in review and implemented the technique reference foundation.
- `migrations/versions/007_add_brainstorm_techniques_table.py` seeds `brainstorm_techniques` from `.agents/skills/bmad-brainstorming/brain-methods.csv`.
- `thagid/models/technique.py`, `thagid/schemas/technique.py`, and `thagid/services/technique.py` exist and expose `TechniqueItem` plus package context with techniques.
- `thagid/routers/internal.py` exposes `GET /internal/backend/packages/{package_id}/context` for agent use only, protected by `X-Agent-Key`.
- `agent/backend_client.py` fetches package context/techniques from the backend over HTTP with `X-Agent-Key`.
- `agent/main.py` currently recommends techniques on new session, stores `recommended_techniques`, and supports selection during `initiate` using exact/partial matching against those recommendations.
- During `facilitate`, `agent/main.py` currently returns the generic continuation reply and does not yet handle technique swap.
- `thagid/routers/brainstorm.py` currently exposes only browser-facing brainstorm status and message endpoints and already has `verify_package_access`.
- `thagid/services/brainstorm.py` persists user/assistant message pairs to the `messages` table and validates the agent response shape.
- `web/src/lib/api/brainstorm.ts` currently has only `getBrainstormStatus` and `sendBrainstormMessage`.
- `web/src/lib/types/brainstorm.ts` currently has only `BrainstormPhase`, `BrainstormMessageResponse`, and `BrainstormStatusResponse`.
- `ChatInterface.svelte` already imports `WandSparkles` for the active technique pill but does not expose a picker button.
- `ChatBubble.svelte` renders basic assistant markdown for the Story 2.1 recommendation text; it does not render structured technique cards.

### Required Implementation Behavior

- The picker must load the technique list from the backend reference table, not from the CSV in the browser.
- The acceptance criteria say 62 techniques, but the current CSV/reference data has 61 rows. Do not fake a 62nd row. Show all available DB rows and keep the mismatch visible in tests or implementation notes.
- The picker must support both initial selection after recommendations and later swapping during facilitate.
- Picker confirmation should send through the existing brainstorm message endpoint so the transcript records the user's selection and the agent acknowledgement.
- The active technique pill in the chat header must update using the existing response `technique` field.
- Existing ideas must remain untouched during swaps. Treat `state["ideas"]` as append/preserve-only for this story.
- Natural language swaps during `facilitate` should not require the frontend modal. The agent should detect swap intent and validate the requested technique against all available techniques.
- Unknown or ambiguous swap requests should preserve the current technique and phase, then ask the user to choose a valid technique.

### UX Requirements

- Follow `design-system/thagid/MASTER.md` and `design-system/thagid/pages/package-chat.md` because this story edits UI.
- Technique picker trigger: `wand-sparkles` icon button in chat header, visible only during brainstorm.
- Modal width: `max-w-2xl`.
- Modal layout: two-column, with scrollable list left and selected technique detail right.
- Search bar: standard input with search icon prefix, rounded-lg, placeholder `Search...`, and optional clear button.
- Filter chips: horizontal category chips, active `bg-primary text-white`, inactive `bg-slate-100 text-slate-600 hover:bg-slate-200`.
- Technique list item: `p-3 rounded-lg cursor-pointer hover:bg-slate-50`; selected item should use `bg-primary/5 border-l-2 border-primary`.
- Detail panel: technique name, category badge, description, and primary full-width `Select Technique` button.
- Selection UX: modal closes, agent confirms, active technique updates, phase badge stays `Facilitate` for mid-session swaps.
- Preserve reduced-motion behavior and visible focus states from Story 1.5.
- Preserve `role="log"` and `aria-live="polite"` on the chat message area.

### Backend And Agent Contract Guardrails

- Browser-facing technique list endpoint must be JWT-authenticated and must verify package ownership.
- Internal agent/backend endpoint must remain `X-Agent-Key` protected and not be used by the browser.
- Existing brainstorm response fields must remain stable: `message`, `session_id`, `phase`, `technique`, `idea_count`, `message_count`.
- If adding optional technique metadata to responses, keep it optional and do not require frontend callers to consume it for existing flows.
- `agent/main.py` checkpoint validation currently tolerates additional state fields. Preserve this so old checkpoints without new fields resume.
- Do not import backend services/models into the agent. The agent must fetch technique data through `agent.backend_client`.
- Do not mutate `ideas`, `themes`, `active_documents`, or `summary` when swapping techniques.

### Testing Requirements

- Agent tests should build on `agent/tests/test_brainstorm.py`, which already covers initiation recommendations, fallback, initiate-phase selection, status, resume, errors, and message merge behavior.
- Add an agent test where facilitate state has existing `ideas` and `technique`, user sends `Use Mind Mapping`, response stays `facilitate`, state technique changes, and ideas are unchanged.
- Add an agent test for natural language such as `let's try Mind Mapping` or `switch to Mind Mapping`.
- Add an agent test for unknown technique during facilitate that preserves current technique and ideas.
- Backend tests should build on `thagid/tests/test_brainstorm.py` for authenticated package routes and `thagid/tests/test_internal.py` for technique/context helpers.
- Frontend tests can follow `web/tests-unit/brainstorm-phase-badge.test.ts` with Svelte Testing Library if component interaction is practical.
- If frontend picker tests are too brittle, still run `cd web && npm run check` and document manual verification in the Dev Agent Record.

### Previous Story Intelligence

- Story 2.1 implemented reference technique persistence and documented the 62-vs-61 technique count discrepancy.
- Story 2.1 established `SCAMPER Method` as safe fallback and kept `phase == "initiate"` until a technique is selected.
- Story 2.1 established normal message text (`Use {technique}`) as the selection command. Reuse that pattern for picker confirmation.
- Story 2.1 explicitly deferred full picker modal, browse-all path, search/filter, and mid-session swap to this story.
- Story 1.5 established focus, reduced-motion, phase badge, and chat-shell requirements; keep those intact.
- Story 1.4 established that displayed transcript is persisted in `messages`, while agent continuity is persisted in `agent_checkpoints`.
- Recent git history includes `fix: align brainstorm chat accessibility`, `fix: harden brainstorm resume checkpoints`, `feat: detect existing brainstorm sessions`, `feat: start brainstorm sessions from package chat`, and `feat: add brainstorm runtime foundation`; do not regress those contracts.

### File Structure Requirements

- Likely backend updates: `thagid/routers/brainstorm.py`, `thagid/services/technique.py`, `thagid/schemas/technique.py`, and backend tests under `thagid/tests/`.
- Likely agent updates: `agent/main.py` and `agent/tests/test_brainstorm.py`; possibly `agent/backend_client.py` only if a clearer helper is needed.
- Likely frontend updates: `web/src/lib/types/brainstorm.ts`, `web/src/lib/api/brainstorm.ts`, `web/src/lib/components/custom/TechniquePicker.svelte`, `web/src/lib/components/custom/ChatInterface.svelte`, and `web/src/routes/project/[id]/package/[pkgId]/+page.svelte`.
- Avoid modifying shadcn-managed files under `web/src/lib/components/ui/`.
- Avoid new migrations unless the Story 2.1 technique table is missing required columns; it should already have name/category/description.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story-2.2-Technique-Picker-and-Mid-Session-Swap]
- [Source: _bmad-output/planning-artifacts/prd.md#Migration-Source-BMAD-Brainstorming-Skill]
- [Source: _bmad-output/planning-artifacts/prd.md#Migration-Mapping]
- [Source: _bmad-output/planning-artifacts/prd.md#Brainstorm-Ideation]
- [Source: _bmad-output/planning-artifacts/architecture.md#Agent-State-Machine]
- [Source: _bmad-output/planning-artifacts/architecture.md#Frontend-Integration]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Technique-Selection-FR6-FR9]
- [Source: design-system/thagid/MASTER.md#Technique-Picker-Modal]
- [Source: design-system/thagid/pages/package-chat.md#Technique-Picker-In-Chat]
- [Source: design-system/thagid/pages/package-chat.md#Technique-Swap-Mid-Session]
- [Source: _bmad-output/implementation-artifacts/2-1-technique-recommendation-at-session-initiation.md#Completion-Notes-List]

## Project Structure Notes

- The implemented prototype still centralizes brainstorm behavior in `agent/main.py`; extend it for swap handling rather than creating the future LangGraph folder structure.
- The browser needs a package-scoped technique list endpoint because the existing context endpoint is internal agent-only.
- The frontend does not currently have shadcn `Command`; implement search/filter with existing Svelte state and `Input`.

## Dev Agent Record

### Agent Model Used

gpt-5.5

### Implementation Plan

- Added a package-scoped browser endpoint for technique browsing that reuses package access checks and the existing technique service/schema layer.
- Added frontend technique types/API helper, on-demand loading from the package page, and a custom shadcn Dialog/Input-based picker that sends `Use {technique}` through the existing brainstorm message flow.
- Extended the agent facilitate-phase path to detect explicit swap intents, validate against backend package context techniques, preserve existing state, and keep phase as `facilitate`.

### Debug Log References

- `rtk pytest thagid/tests/test_brainstorm.py` initially failed for the missing browser technique endpoint, then passed after implementation.
- `rtk pytest agent/tests/test_brainstorm.py` initially failed for missing facilitate swap handling, then passed after implementation.
- `rtk npm run test:unit -- --runInBand` failed because Vitest does not support `--runInBand`; reran the repo command successfully.
- `rtk pytest agent/tests/test_brainstorm.py` passed: 39 tests.
- `rtk pytest thagid/tests/test_brainstorm.py thagid/tests/test_internal.py` passed: 38 tests.
- `rtk npm run check` passed with 0 errors and 0 warnings.
- `rtk npm run test:unit` passed: 6 files, 18 tests.
- `rtk pytest` passed: 151 tests.
- Code review patches applied for initiate picker selection, facilitate `Use ...` ambiguity, and no-result picker selection.
- `rtk pytest agent/tests/test_brainstorm.py` passed: 41 tests.
- `rtk pytest thagid/tests/test_brainstorm.py thagid/tests/test_internal.py` passed: 38 tests.
- `rtk npm run check` passed with 0 errors and 0 warnings.
- `rtk npm run test:unit` passed: 6 files, 19 tests.

### Completion Notes List

- Ultimate context engine analysis completed - comprehensive developer guide created.
- Implemented the JWT-protected browser-facing technique list endpoint returning all persisted techniques ordered by category and name.
- Implemented the TechniquePicker modal with search, category filters, selected detail panel, and confirmation through the existing brainstorm message endpoint.
- Implemented facilitate-phase technique swaps for picker-style and natural-language requests while preserving ideas, themes, active documents, summary, messages, and phase.
- Resolved code review findings so picker-selected non-recommended techniques work during initiation, regular facilitate messages starting with `Use ...` are not misclassified, and no-result filters cannot confirm hidden techniques.
- Left the optional recommendation-content `Browse all techniques` affordance out to avoid brittle markdown parsing, per the story constraint.
- Added backend, agent, and frontend unit coverage for the endpoint, swap behavior, and picker search/filter/detail/confirm flow.

### File List

- `_bmad-output/implementation-artifacts/2-2-technique-picker-and-mid-session-swap.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `agent/main.py`
- `agent/tests/test_brainstorm.py`
- `thagid/routers/brainstorm.py`
- `thagid/schemas/technique.py`
- `thagid/services/technique.py`
- `thagid/tests/test_brainstorm.py`
- `web/src/lib/api/brainstorm.ts`
- `web/src/lib/components/custom/ChatInterface.svelte`
- `web/src/lib/components/custom/TechniquePicker.svelte`
- `web/src/lib/types/brainstorm.ts`
- `web/src/routes/project/[id]/package/[pkgId]/+page.svelte`
- `web/tests-unit/technique-picker.test.ts`

### Change Log

- 2026-05-11: Implemented browser technique browsing, package chat picker integration, facilitate-phase technique swaps, and focused regression coverage.
- 2026-05-11: Resolved code review findings and marked story complete.
