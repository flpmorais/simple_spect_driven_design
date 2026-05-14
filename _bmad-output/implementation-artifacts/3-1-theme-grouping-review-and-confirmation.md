# Story 3.1: Theme Grouping Review and Confirmation

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a package user,
I want the agent to group my brainstorm ideas into reviewable themes before finalization,
so that I can shape the final structure before it is persisted.

## Acceptance Criteria

1. Given the session is in Facilitate phase with one or more ideas, when I indicate that brainstorming is done, then the session enters the Extract phase, and the agent presents ideas grouped into theme cards.
2. Given theme cards are shown, when I expand or collapse a theme, then the idea list toggles visibility, and the control exposes the correct `aria-expanded` state.
3. Given I request a theme adjustment, when the agent handles the adjustment, then it updates theme names or idea membership and presents the revised grouping, and no knowledge graph write occurs until I confirm the grouping.

## Tasks / Subtasks

- [x] Define the theme grouping state and API contract (AC: 1, 2, 3)
  - [x] Add a `BrainstormTheme` shape across agent/backend/frontend contracts with stable fields: `id`, `title`, `summary`, `ideas: list[BrainstormIdea]`, and optional `position` if useful for rendering order.
  - [x] Preserve existing brainstorm response fields: `message`, `session_id`, `phase`, `technique`, `idea_count`, `message_count`, and `ideas`.
  - [x] Add `themes` to `BrainstormMessageResponse` and `BrainstormStatusResponse` with default empty lists so existing callers remain compatible.
  - [x] Keep `state["themes"]` as the checkpoint source of truth for grouped themes.
  - [x] Add a checkpoint flag such as `themes_confirmed: bool` only if needed for Story 3.2 handoff; default missing value to `False` for old checkpoints.
  - [x] Do not add database tables, migrations, KG writes, embeddings, or markdown rendering in this story.
- [x] Implement deterministic Facilitate -> Extract transition on done intent (AC: 1)
  - [x] Detect conclusion intent only while `phase == "facilitate"`, using explicit phrases such as `done`, `looks complete`, `wrap up`, `finalize`, `finish brainstorming`, or `conclude session`.
  - [x] Require at least one structured idea before entering Extract. If no ideas exist, stay in Facilitate and ask for at least one idea; do not create empty themes.
  - [x] Generate initial themes deterministically from existing `state["ideas"]`, preferably grouping by idea `category` and creating readable theme titles from categories.
  - [x] Include all ideas exactly once across themes. If an idea lacks a usable category, assign it to a `General` theme.
  - [x] Store generated themes in `state["themes"]`, set `state["phase"] = "extract"`, preserve `ideas`, `active_documents`, `summary`, `technique`, message counters, and existing transcript messages.
  - [x] Return an assistant reply that says the ideas are grouped for review and instructs the user how to request adjustments or confirm.
- [x] Present theme cards in package chat (AC: 1, 2, UX-DR16, UX-DR17)
  - [x] Add `BrainstormTheme` to `web/src/lib/types/brainstorm.ts`.
  - [x] Add `themes` handling to `web/src/lib/api/brainstorm.ts`, `web/src/routes/project/[id]/package/[pkgId]/+page.svelte`, and `ChatInterface.svelte`.
  - [x] Create a custom `ThemeCard.svelte` under `web/src/lib/components/custom/` rather than editing shadcn-managed `ui/` components.
  - [x] `ThemeCard.svelte` should follow `design-system/thagid/MASTER.md`: white card, slate border, `rounded-xl`, `p-5`, Layers icon, title, idea count badge, collapsible idea list, and compact idea rows/cards.
  - [x] Theme card header must be a keyboard-operable button with `aria-expanded` reflecting state.
  - [x] Render theme cards in the chat flow when `brainstormPhase === "extract"` and themes exist. Do not remove the existing cumulative idea list unless it causes duplicate/confusing display; if both render, keep the theme review visually primary.
  - [x] Preserve chat `role="log"`, `aria-live="polite"`, auto-scroll, reduced-motion behavior, existing attachment controls, technique picker, phase badge, and message counts.
- [x] Support text-based theme adjustments while in Extract (AC: 3)
  - [x] In `agent/main.py` or a small helper such as `agent/theme_grouping.py`, handle adjustment messages only when `phase == "extract"` and themes exist.
  - [x] Support deterministic adjustment commands at minimum: `Rename theme {old} to {new}` and `Move idea {idea title} to {theme title}`.
  - [x] For `Move idea`, remove the idea from its current theme, create the destination theme if it does not exist, append the idea there, and remove any empty source theme.
  - [x] For `Rename theme`, update the theme title and keep its idea membership intact.
  - [x] After every successful adjustment, update checkpoint `themes`, preserve all ideas exactly once, and return the revised themes in the response.
  - [x] If the command cannot be parsed or references a missing idea/theme, keep the existing themes unchanged and reply with the supported adjustment formats.
  - [x] Do not write to KG, call internal KG endpoints, compute embeddings, or render markdown during adjustment.
- [x] Support grouping confirmation as a handoff to later Epic 3 stories (AC: 3)
  - [x] Detect confirmation phrases while in Extract, such as `confirm`, `looks good`, `approved`, `these themes are good`, or `finalize groupings`.
  - [x] On confirmation, preserve `state["themes"]`, set a durable confirmation marker such as `themes_confirmed = True`, and either keep `phase == "extract"` with a clear acknowledgement or transition to `phase == "validate"` as a routing marker for Story 3.2/3.3. Choose one behavior and test it explicitly.
  - [x] The assistant reply must make clear that groupings are confirmed and the next pipeline step can proceed later.
  - [x] Do not implement Story 3.2 KG writes, Story 3.3 validation, Story 3.4 embeddings, or Story 3.5 markdown rendering.
  - [x] Ensure no calls are made to `/internal/kg/...` in this story.
- [x] Preserve existing brainstorm and attachment behavior (AC: 1, 2, 3)
  - [x] Story 2.1 technique recommendation and initiate selection must still work.
  - [x] Story 2.2 technique picker and facilitate-phase swaps must still work and must not be allowed to rewrite confirmed themes unexpectedly.
  - [x] Story 2.3 idea extraction, duplicate reduction, contradiction handling, anti-bias pivoting, cumulative idea cards, and status/resume must still work.
  - [x] Story 2.4 rolling summary counters and checkpoint compaction must remain correct through the Extract transition.
  - [x] Story 2.5 file active documents and Story 2.6 URL active documents must remain preserved and available in checkpoint state.
  - [x] Existing non-brainstorm package chat must still send through `/api/packages/{package_id}/messages` and remain unaffected.
- [x] Add focused tests and verification (AC: 1, 2, 3)
  - [x] Add agent tests for done intent in Facilitate with ideas: phase becomes Extract, themes are generated, all ideas appear exactly once, and no KG call is made.
  - [x] Add agent test for done intent with zero ideas: phase remains Facilitate and no themes are created.
  - [x] Add agent tests for renaming a theme, moving an idea between themes, creating a destination theme on move, removing empty themes, and rejecting malformed adjustment commands without state mutation.
  - [x] Add agent test for confirmation behavior and explicit no-KG-write/no-markdown behavior.
  - [x] Add backend tests that `themes` from the agent response/status are validated and returned to the browser.
  - [x] Add frontend tests for `ThemeCard.svelte` expand/collapse `aria-expanded`, rendering theme titles/idea counts, and chat rendering of theme cards in Extract.
  - [x] Run `rtk pytest agent/tests/test_brainstorm.py`.
- [x] Run `rtk pytest thagid/tests/test_brainstorm.py thagid/tests/test_internal.py` or the full backend suite if practical.
- [x] Run `rtk npm run check` from `web/`; run `rtk npm run test:unit` if frontend tests are added.

### Review Findings

- [x] [Review][Patch] Validate checkpoint theme shape before returning or adjusting themes [agent/main.py:64]
- [x] [Review][Patch] Reject or regenerate empty Extract-phase themes before confirmation [agent/main.py:690]
- [x] [Review][Patch] Prevent confirmed themes from being mutated without clearing or requiring reconfirmation [agent/main.py:690]
- [x] [Review][Patch] Make theme adjustment commands unambiguous for duplicate names and titles containing `to` [agent/main.py:299]
- [x] [Review][Patch] Extract fallback should ask whether to adjust themes or return to brainstorming [agent/main.py:693]

## Dev Notes

### Scope Boundaries

- This story implements reviewable theme grouping and text-based grouping adjustment only.
- Do not implement KG persistence, validation retries, embeddings, BMAD markdown rendering, dashboard summary cards, brainstorm detail pages, or graph retrieval.
- Do not introduce the future `agent/brainstorm/` LangGraph folder layout unless the project has already migrated to it. The current prototype centralizes brainstorm behavior in `agent/main.py`; use a small helper only if it keeps theme logic clear.
- Do not add new libraries. Deterministic Python grouping and existing Svelte components are sufficient.
- Drag-and-drop theme adjustment is future scope. MVP adjustment is text-based.

### Current Codebase State

- `agent/main.py` owns `/internal/agent/brainstorm/message` and `/internal/agent/brainstorm/status` with `X-Agent-Key` auth.
- Active checkpoint validation allows `themes` as a list but does not validate theme shape yet.
- Existing new sessions initialize `themes: []`, `active_documents: []`, `summary: None`, `phase: "initiate"`, `status: "active"`, and summary counters.
- Existing Facilitate behavior appends user/assistant messages, extracts ideas from the user message plus successful file/URL context, reduces duplicates, builds bounded context, and saves checkpoint state.
- Existing response from `agent/main.py` already includes internal `themes`, but `thagid/services/brainstorm.py` and browser-facing schemas currently expose only `ideas`, not `themes`.
- `web/src/lib/types/brainstorm.ts` defines `BrainstormPhase`, `BrainstormIdea`, file and URL attachment types, message/status responses, and technique list types. It has no `BrainstormTheme` type yet.
- `ChatInterface.svelte` renders phase badge, technique picker, cumulative idea cards, file upload, URL sharing, textarea, and send button. It has no theme card rendering yet.
- `IdeaCard.svelte` exists and can be reused inside theme cards or copied into compact idea rows.
- `BrainstormPhaseBadge.svelte` already supports `extract`, `validate`, `markdown`, and `concluded` labels/colors.
- `agent/checkpoint.py` merges messages, ideas, active documents, and summary/counter fields. If themes can be concurrently adjusted, merge behavior may need focused tests or a simple last-write-wins rule documented in tests.

### Required Implementation Behavior

- The done intent is meaningful only in Facilitate with at least one structured idea.
- Extract phase is a review phase. It presents grouped ideas and accepts user adjustment/confirmation messages.
- Theme generation must be deterministic and testable. Do not call an LLM to group themes in this story.
- Every idea in `state["ideas"]` must appear exactly once across `state["themes"]` after generation and after each adjustment.
- Theme adjustment must not mutate the canonical idea objects except for changing their theme membership.
- Confirmation must not write to the knowledge graph. It should only preserve confirmed state for later stories.
- If a user sends a normal ideation message while in Extract and it is not an adjustment/confirmation command, the agent should ask whether they want to adjust themes or go back to brainstorming; do not silently add new ideas unless explicitly designed and tested.
- Existing active document chunks from file and URL ingestion should be preserved for future KG ContextChunk writes.

### UX Requirements

- Follow `design-system/thagid/MASTER.md` and `design-system/thagid/pages/package-chat.md` because this story edits chat UI.
- ThemeCard visual style: `bg-white`, `border border-slate-200`, `rounded-xl`, `p-5`, Layers icon, title, idea count, and collapsible ideas list.
- ThemeCard header must be a button, keyboard accessible, and expose `aria-expanded`.
- Expanded theme cards should show compact idea content: title, concept, category, and novelty if space allows.
- The phase badge should show `Extract` while theme grouping review is active.
- Preserve desktop-only layout, no horizontal scroll, visible focus rings, no emoji icons, and reduced-motion behavior.
- Do not add drag/drop interactions or modal-heavy review flows.

### Backend And Agent Contract Guardrails

- Browser traffic continues through FastAPI `/api/packages/{package_id}/brainstorm/...`; browser never calls `thagid-agent` directly.
- Internal backend/agent traffic continues using `X-Agent-Key`.
- Existing non-brainstorm chat endpoint remains unchanged.
- Existing browser-facing response fields remain stable; `themes` must be additive and default to `[]`.
- Do not import `thagid.*` backend services/models into `agent/`; keep container boundaries strict.
- Do not call `/internal/kg/...` or create `KnowledgeGraphService` usage in this story.

### Architecture And Product Context

- PRD FR4 requires the user to conclude a brainstorm by indicating completion.
- PRD FR17 requires the system to present all ideas grouped into themes before conclusion.
- PRD FR18 requires the user to review and adjust theme groupings before finalizing.
- UX-DR16 requires ThemeCard with collapsible header, idea count, idea list, and `aria-expanded` behavior.
- UX-DR17 requires a theme grouping review flow where the user says done, agent presents grouped theme cards, user can request adjustments, and user can confirm final groupings.
- Architecture defines the flow `facilitate -> extract -> validate -> markdown`, with validation failures potentially returning to Facilitate. This story starts that output pipeline by implementing the Extract review state only.
- Architecture defines future KG writes for Session, Theme, Idea, and ContextChunk nodes. Those writes begin in Story 3.2, not here.

### Previous Story Intelligence

- Story 2.6 is in review and implemented URL context ingestion with SSRF guardrails, URL active document chunks, URL chips, and URL tests. Preserve its `active_documents` behavior and URL UI.
- Story 2.5 is done and implemented JSON text file attachment contracts, file chips, file active document chunks, deterministic file summaries, duplicate suppression, and pending file retention on send failure.
- Story 2.4 is done and implemented deterministic rolling summary state with `message_count_total`, `summarized_message_count`, checkpoint message compaction, and bounded facilitation context.
- Story 2.3 is done and implemented deterministic structured idea extraction, cumulative idea state, `IdeaCard`, backend/frontend `ideas` response fields, duplicate reduction, contradiction handling, and anti-bias pivoting.
- Story 2.2 implemented technique picker and facilitate-phase technique swaps through the same brainstorm message path.
- Story 2.1 established `SCAMPER Method` fallback and exact technique matching for initiate-phase selection.
- Story 1.4 established displayed transcript persistence in `messages` and agent continuity in `agent_checkpoints`.
- Recent git history includes `feat: add text file context ingestion`, `feat: add brainstorm idea management and summaries`, `feat: add technique picker and swaps`, `feat: recommend brainstorm techniques`, and `fix: align brainstorm chat accessibility`.

### File Structure Requirements

- Likely agent updates: `agent/main.py`, `agent/tests/test_brainstorm.py`, and optionally new `agent/theme_grouping.py`.
- Likely backend updates: `thagid/schemas/brainstorm.py`, `thagid/services/brainstorm.py`, and `thagid/tests/test_brainstorm.py`.
- Likely frontend updates: `web/src/lib/types/brainstorm.ts`, `web/src/routes/project/[id]/package/[pkgId]/+page.svelte`, `web/src/lib/components/custom/ChatInterface.svelte`, new `web/src/lib/components/custom/ThemeCard.svelte`, and a focused component test.
- Possible checkpoint update: `agent/checkpoint.py` if concurrent theme adjustments need explicit preservation.
- Avoid modifying shadcn-managed files under `web/src/lib/components/ui/`.
- Avoid migrations and new database models.

### Testing Requirements

- Build agent tests in `agent/tests/test_brainstorm.py`, near existing phase and idea-management tests.
- Add a test where Facilitate with multiple categories and done intent creates Extract themes grouped by category.
- Add a test where done intent with zero ideas stays Facilitate.
- Add tests for theme rename, idea move, bad adjustment command, confirmation, and no KG/markdown behavior.
- Add backend tests proving `themes` response/status payloads pass through FastAPI schemas.
- Add frontend tests for `ThemeCard` expand/collapse and `ChatInterface` rendering themes during Extract.
- Run the verification commands listed in Tasks.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story-3.1-Theme-Grouping-Review-and-Confirmation]
- [Source: _bmad-output/planning-artifacts/prd.md#Brainstorm-Output]
- [Source: _bmad-output/planning-artifacts/prd.md#Migration-Mapping]
- [Source: _bmad-output/planning-artifacts/architecture.md#LangGraph-State-Machine]
- [Source: _bmad-output/planning-artifacts/architecture.md#Validation-Failure-Pattern]
- [Source: _bmad-output/planning-artifacts/architecture.md#Architectural-Boundaries]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Theme-Grouping-FR17-FR18]
- [Source: design-system/thagid/MASTER.md#Theme-Card]
- [Source: design-system/thagid/pages/package-chat.md#Theme-Grouping-Conclude-Phase]
- [Source: _bmad-output/implementation-artifacts/2-6-url-context-ingestion.md#Completion-Notes-List]

## Project Structure Notes

- The architecture target names this as the `extract` node, but the current implementation remains in `agent/main.py`. Implement the Extract review state in the current prototype without prematurely creating the full future LangGraph folder structure.
- Theme grouping is checkpoint state only in this story. Story 3.2 owns KG writes for Theme and Idea nodes.
- Deterministic grouping by existing idea categories is the smallest correct implementation and avoids introducing new LLM calls or prompt instability.
- Latest technical research was not required because this story uses existing Python/Svelte/FastAPI patterns and no new external APIs or dependencies.

## Dev Agent Record

### Agent Model Used

openai/gpt-5.5

### Debug Log References

- `rtk pytest agent/tests/test_brainstorm.py thagid/tests/test_brainstorm.py -q` - 128 passed
- `rtk npm run test:unit -- ThemeCard ChatInterface` - 16 passed
- `rtk npm run check` - 0 errors, 0 warnings
- `rtk pytest agent/tests/test_brainstorm.py` - 82 passed
- `rtk pytest thagid/tests/test_brainstorm.py thagid/tests/test_internal.py` - 52 passed
- `rtk npm run test:unit` - 36 passed
- `rtk pytest` - 208 passed

### Completion Notes List

- Ultimate context engine analysis completed - comprehensive developer guide created.
- Implemented additive `BrainstormTheme` contracts across agent, backend, and frontend while preserving existing brainstorm response fields.
- Implemented deterministic Facilitate to Extract transition on done intent, grouping ideas by category and preserving checkpoint ideas, active documents, summary, technique, counters, and transcript messages.
- Implemented Extract-phase text adjustments for theme rename and idea move, including destination theme creation, empty source theme removal, malformed-command no-op behavior, and `themes_confirmed` confirmation handoff.
- Added package chat theme review cards with accessible expand/collapse controls and focused agent, backend, and frontend tests.

### File List

- `_bmad-output/implementation-artifacts/3-1-theme-grouping-review-and-confirmation.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `agent/main.py`
- `agent/tests/test_brainstorm.py`
- `thagid/schemas/brainstorm.py`
- `thagid/services/brainstorm.py`
- `thagid/tests/test_brainstorm.py`
- `web/src/lib/components/custom/ChatInterface.svelte`
- `web/src/lib/components/custom/ChatInterface.test.ts`
- `web/src/lib/components/custom/ThemeCard.svelte`
- `web/src/lib/components/custom/ThemeCard.test.ts`
- `web/src/lib/types/brainstorm.ts`
- `web/src/routes/project/[id]/package/[pkgId]/+page.svelte`

### Change Log

- 2026-05-11: Implemented theme grouping review and confirmation flow for Story 3.1.
