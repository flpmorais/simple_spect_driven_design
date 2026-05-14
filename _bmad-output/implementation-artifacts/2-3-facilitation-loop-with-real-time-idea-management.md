# Story 2.3: Facilitation Loop With Real-Time Idea Management

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a package user,
I want the facilitator to build on my input and maintain ideas in real time,
so that the brainstorm feels productive and accumulates structured output.

## Acceptance Criteria

1. Given the session is in Facilitate phase, when I send an ideation message, then the agent responds using the active technique, and any new ideas are added to brainstorm state with category, title, concept, and novelty.
2. Given a new idea duplicates or contradicts an existing idea, when the idea reducer processes it, then it merges, updates, or preserves the idea consistently, and the resulting idea list contains no avoidable duplicates.
3. Given several similar ideas are accumulating, when the facilitator continues ideation, then it applies anti-bias domain pivoting when appropriate, and prompts the user toward a different angle without discarding prior ideas.

## Tasks / Subtasks

- [x] Define and validate the brainstorm idea shape (AC: 1, 2)
  - [x] Use the existing checkpoint `state["ideas"]` list as the source of truth; do not introduce a separate idea store for this story.
  - [x] Represent each idea as an object with `category`, `title`, `concept`, and `novelty` string fields.
  - [x] Extend agent checkpoint validation in `agent/main.py` only enough to reject malformed non-list idea state and tolerate old empty-list checkpoints.
  - [x] Treat legacy simple-string ideas from existing tests/checkpoints as legacy input only. Do not expose strings to browser-facing structured idea responses; normalize, preserve internally, or ignore them deliberately in tested code paths.
  - [x] Keep `themes`, `active_documents`, and `summary` unchanged in this story.
- [x] Add facilitate-phase idea extraction and response generation in the agent (AC: 1)
  - [x] Extend the current `phase == "facilitate"` branch in `agent/main.py`; do not create the future `agent/brainstorm/` LangGraph folder layout yet.
  - [x] Preserve Story 2.2 technique swap handling before normal ideation handling, so `Use {technique}` and natural-language swaps still work.
  - [x] Use the active `state["technique"]` in the facilitator reply text so users can see the response is technique-aware.
  - [x] Extract one or more structured ideas from the user's ideation message when it contains actionable content.
  - [x] Return updated `ideas`, `idea_count`, `message_count`, `technique`, `themes`, `active_documents`, and `markdown` using the existing agent response shape.
  - [x] Persist the assistant reply and updated ideas to the checkpoint in the same save operation.
- [x] Implement deterministic idea reduction for duplicates and contradictions (AC: 2)
  - [x] Add the smallest helper needed in `agent/main.py` or a focused `agent/ideas.py` if `main.py` becomes unclear.
  - [x] Match duplicates by normalized title and obvious title similarity; avoid fuzzy matching that can merge unrelated ideas.
  - [x] When a new idea duplicates an existing idea, preserve the existing idea identity/order and merge useful concept/novelty detail rather than appending a duplicate.
  - [x] When a new idea contradicts an existing idea, update or preserve the idea consistently and include enough wording in `concept` to make the tension explicit.
  - [x] Never discard existing ideas during technique swaps, invalid swap requests, normal ideation, or pivot prompts.
- [x] Preserve concurrent checkpoint idea changes (AC: 1, 2)
  - [x] Update `agent/checkpoint.py` merge behavior so concurrent message saves do not overwrite newly added ideas from another request.
  - [x] Preserve existing idea order and append or merge concurrent structured ideas through the same deterministic reducer used by normal facilitate handling.
  - [x] Add a focused checkpoint merge test proving concurrent additions from two saves both survive.
- [x] Add anti-bias domain pivoting during facilitation (AC: 3)
  - [x] Track enough lightweight state to detect repeated categories or semantically similar idea titles in the current `ideas` list.
  - [x] Trigger a pivot prompt when similar ideas are accumulating, using the BMAD source guidance of domain pivoting to prevent semantic clustering.
  - [x] Keep the phase as `facilitate` and preserve all prior ideas when pivoting.
  - [x] Include the pivot in the assistant reply as a prompt toward a different angle, not as a destructive reset or automatic technique swap.
- [x] Surface structured ideas to the browser without breaking existing clients (AC: 1)
  - [x] Extend `thagid/schemas/brainstorm.py`, `thagid/services/brainstorm.py`, and `web/src/lib/types/brainstorm.ts` to include optional `ideas` in brainstorm message/status responses if needed for rendering.
  - [x] Keep existing response fields backward-compatible: `message`, `session_id`, `phase`, `technique`, `idea_count`, and `message_count`.
  - [x] Continue persisting the user/assistant transcript in `messages`; the checkpoint remains the source of structured idea state.
  - [x] If ideas are exposed to the browser, expose the cumulative current idea list for the session, not per-message idea metadata.
- [x] Render idea cards in package chat if structured ideas are returned (AC: 1, UX-DR15)
  - [x] Prefer a small `IdeaCard.svelte` under `web/src/lib/components/custom/` if rendering structured ideas separately from assistant markdown.
  - [x] Render the cumulative ideas list once in chat UI state, such as a latest-ideas area near the assistant response or header region; do not duplicate the full idea list under every historical assistant message.
  - [x] On refresh/resume, use status or the next message response to repopulate the cumulative list; the persisted transcript alone is not enough to reconstruct structured idea cards.
  - [x] Follow `design-system/thagid/MASTER.md#Idea-Card` and `design-system/thagid/pages/package-chat.md#Chat-Bubbles`.
  - [x] Show title, concept/description, category tag, and novelty indicator using Lucide `lightbulb` and existing design tokens.
  - [x] Preserve `role="log"`, `aria-live="polite"`, visible focus states, reduced-motion behavior, auto-scroll, technique picker, phase badge, and message count display.
  - [x] Do not parse fragile freeform assistant markdown to infer idea cards; use structured response data or keep ideas as readable assistant text if structured UI wiring is too large.
- [x] Preserve Story 2.1 and Story 2.2 behavior (AC: 1, 2, 3)
  - [x] New-session recommendations and fallback `SCAMPER Method` behavior still work.
  - [x] Initiate-phase selection via exact `Use {technique}` still transitions to `facilitate`.
  - [x] Facilitate-phase picker and natural-language swaps still preserve ideas, themes, documents, summary, messages, and phase.
  - [x] Active-session status, resume by session id, terminal-checkpoint restart, checkpoint error handling, and regular non-brainstorm chat still work.
- [x] Add focused tests and verification (AC: 1, 2, 3)
  - [x] Add agent tests for facilitate-phase idea extraction adding structured ideas with category/title/concept/novelty.
  - [x] Add agent tests for duplicate idea merging, contradiction handling, preserving existing ideas, and anti-bias pivot prompting.
  - [x] Add agent regression tests proving technique swaps still preserve accumulated ideas after this story.
  - [x] Add backend tests if response schemas are extended to include structured ideas.
  - [x] Add frontend tests for `IdeaCard` rendering if a component is introduced; otherwise cover the existing package page state update if practical.
  - [x] Run `rtk pytest agent/tests/test_brainstorm.py`.
  - [x] Run relevant backend tests, including `rtk pytest thagid/tests/test_brainstorm.py thagid/tests/test_internal.py` if response contracts change.
  - [x] Run `rtk npm run check` from `web/`; run `rtk npm run test:unit` if frontend tests are added.

### Review Findings

- [x] [Review][Patch] Actionable question-form and multipart messages can drop all ideas [agent/ideas.py:48]
- [x] [Review][Patch] Non-idea chatter is captured as structured ideas [agent/ideas.py:108]
- [x] [Review][Patch] Newline-separated ideas are collapsed into one idea before splitting [agent/ideas.py:49]
- [x] [Review][Patch] Short generic titles can merge unrelated ideas [agent/ideas.py:145]
- [x] [Review][Patch] Malformed checkpoint idea entries are silently discarded [agent/main.py:300]
- [x] [Review][Patch] Initial status response can overwrite newer brainstorm state [web/src/routes/project/[id]/package/[pkgId]/+page.svelte:62]
- [x] [Review][Patch] Duplicate Svelte keys can break idea rendering [web/src/lib/components/custom/ChatInterface.svelte:188]
- [x] [Review][Patch] Story 2.5 status change is out of Story 2.3 scope [_bmad-output/implementation-artifacts/sprint-status.yaml:76]
- [x] [Review][Patch] Frontend unit test is not co-located [web/tests-unit/idea-card.test.ts:1]

## Dev Notes

### Scope Boundaries

- This story adds productive facilitate-phase behavior: technique-aware replies, structured idea accumulation, duplicate/contradiction reduction, and anti-bias pivot prompting.
- Do not implement Story 2.4 scope: rolling summary thresholding or summary replacement of long conversation history.
- Do not implement Story 2.5 or 2.6 scope: file upload, URL ingestion, attachment chips, document/context chunks, or URL fetching.
- Do not implement Epic 3 scope: theme grouping, conclusion flow, extraction/validation/markdown phases, KG writes, embeddings, or BMAD markdown rendering.
- Do not introduce new libraries. Use existing FastAPI, Pydantic, SvelteKit, current Svelte 5 patterns, shadcn-svelte primitives, and lucide-svelte.
- Keep the current prototype structure. The architecture shows a future LangGraph package layout, but the implemented runtime currently centralizes behavior in `agent/main.py` with checkpoint JSON persistence.

### Current Codebase State

- `agent/main.py` implements `/internal/agent/brainstorm/message` and `/internal/agent/brainstorm/status` with `X-Agent-Key` auth.
- `agent/main.py` currently validates active checkpoint state as `session_id`, `phase`, optional `technique`, list `messages`, list `ideas`, list `themes`, list `active_documents`, and optional `summary`.
- New sessions initialize `ideas: []`, `themes: []`, `active_documents: []`, `summary: None`, `technique: None`, `phase: "initiate"`, and `status: "active"`.
- Initiate-phase behavior recommends techniques from package context, stores `recommended_techniques`, and transitions to `facilitate` only after exact technique selection.
- Facilitate-phase behavior currently supports technique swap intent and otherwise returns the generic reply `Let's continue the brainstorm session. Share your next thought or idea.` without adding ideas.
- `agent/checkpoint.py` persists JSONB state in `agent_checkpoints.brainstorm_states` and merges concurrent message appends. Its merge logic currently preserves advanced phase/technique, but it does not special-case concurrent idea list changes.
- `thagid/services/brainstorm.py` validates agent `ideas` only as a list and uses `len(ideas)` for `idea_count`; it does not expose the actual ideas to the browser response today.
- `thagid/schemas/brainstorm.py` and `web/src/lib/types/brainstorm.ts` expose `phase`, `technique`, `idea_count`, and `message_count`, but not structured ideas.
- `web/src/routes/project/[id]/package/[pkgId]/+page.svelte` updates brainstorm phase/session/technique/idea count/message count after each brainstorm response and rolls back optimistic user messages on failure.
- `ChatInterface.svelte` shows the technique picker trigger, active technique pill, idea count, message count, phase badge, message log, and chat input.
- `ChatBubble.svelte` renders sanitized minimal assistant markdown for bold, inline code, and line breaks only. It does not render structured idea cards.
- No `IdeaCard.svelte` exists yet.
- Frontend state currently has no `brainstormIdeas` or equivalent cumulative structured idea list; adding idea cards requires explicit page/component state, not deriving cards from historical `Message[]`.

### Required Implementation Behavior

- In `facilitate`, normal ideation should be the fallback path after technique swap detection fails or no swap intent exists.
- The active technique must influence the assistant reply wording. The implementation can be deterministic for MVP, but the user must not receive another generic continuation response when providing ideation input.
- Ideas must be stored as dictionaries shaped like `{"category": str, "title": str, "concept": str, "novelty": str}`.
- The idea reducer must be deterministic and testable. Avoid LLM-only reduction that cannot be asserted in unit tests.
- For duplicate handling, stable output matters more than cleverness. Use normalized title matching and simple token overlap before considering more complex semantics.
- For contradiction handling, preserve the prior idea and record the tension in the updated idea concept unless the new message clearly supersedes it.
- Anti-bias pivoting should be a prompt-level intervention. It should not change the user's selected technique and should not clear existing ideas.
- If the user sends a message that contains no extractable idea, keep existing ideas and reply with a technique-aware facilitation prompt.
- The response `state_change` must remain `facilitate` throughout this story.
- Checkpoint saves must preserve old checkpoints with `ideas: []` and checkpoints from Story 2.2 where ideas may be simple test strings. Tests should migrate expectations to structured idea objects where this story creates new ideas.
- Structured browser responses must contain only valid idea objects. Legacy strings may remain inside old checkpoint state for compatibility, but they must not be rendered as `IdeaCard` data unless normalized to the required object shape.
- Concurrent brainstorm sends are in scope because `agent/checkpoint.py` already merges concurrent message appends. Extending idea accumulation without preserving concurrent ideas would regress checkpoint safety.

### UX Requirements

- Follow `design-system/thagid/MASTER.md` and `design-system/thagid/pages/package-chat.md` if editing chat UI.
- Idea card visual spec: white surface, slate border, rounded-lg, `p-4`, title row with `lightbulb`, `text-sm font-semibold`, concept text in `text-sm text-slate-600`, footer category pill and novelty indicator.
- Chat rendering must remain desktop-only and preserve `max-w-[70%]` assistant bubble width.
- If structured ideas are displayed in chat, they should appear inside or adjacent to assistant brainstorm content without replacing the persisted assistant message text.
- Preserve the existing streaming/typing indicator, auto-scroll, and `prefers-reduced-motion` behavior.
- Do not introduce emojis as icons; use lucide-svelte.

### Backend And Agent Contract Guardrails

- Browser traffic continues through FastAPI `/api/packages/{package_id}/brainstorm/...`; the browser must never call `thagid-agent` directly.
- Internal backend/agent traffic continues using `X-Agent-Key`.
- Existing non-brainstorm chat endpoint `/api/packages/{package_id}/messages` must remain unchanged.
- Agent response fields must remain compatible with `thagid/services/brainstorm.py`: `reply`, `session_id`, `state_change`, `ideas`, `idea_count`, `themes`, `active_documents`, `technique`, `message_count`, and `markdown`.
- If adding `ideas` to browser-facing Pydantic schemas, make it optional or defaulted so existing frontend callers and tests remain stable.
- Do not import `thagid.*` backend services/models into `agent/`; keep the container boundary.

### Architecture And Product Context

- PRD migration source defines idea format as category, mnemonic title, concept description, and novelty.
- PRD requires anti-bias domain pivoting during ideation to prevent semantic clustering.
- Architecture defines `BrainstormState.ideas` with a reducer pattern and NFR1 token overhead constraints; this story should keep state compact and not load or generate monolithic documents.
- Architecture's full LangGraph topology is the target direction, but current implementation should extend the prototype unless explicitly refactoring is requested.
- Architecture requires agent responses to stay within standard LLM response time and avoid additional processing bottlenecks.

### Previous Story Intelligence

- Story 2.2 is in review and implemented package-scoped technique browsing, the `TechniquePicker` modal, and facilitate-phase technique swaps.
- Story 2.2 established that picker confirmation sends a normal brainstorm message `Use {technique_name}` through `POST /api/packages/{package_id}/brainstorm/message`.
- Story 2.2 established that facilitate-phase swaps must preserve `ideas`, `themes`, `active_documents`, `summary`, messages, and `phase`.
- Story 2.2 documented the technique source mismatch: planning docs say 62 techniques, but current persisted CSV rows are 61. Do not fake the count.
- Story 2.1 established `SCAMPER Method` as safe fallback and exact technique matching for initiate-phase selection.
- Story 1.4 established that displayed transcript is persisted in `messages`, while agent continuity is persisted in `agent_checkpoints`.
- Story 1.5 established focus, reduced-motion, phase badge, and chat-shell accessibility requirements.
- Recent git history includes `feat: recommend brainstorm techniques`, `fix: align brainstorm chat accessibility`, `fix: harden brainstorm resume checkpoints`, `feat: detect existing brainstorm sessions`, and `feat: start brainstorm sessions from package chat`.

### File Structure Requirements

- Likely agent updates: `agent/main.py` and `agent/tests/test_brainstorm.py`; optionally a small `agent/ideas.py` only if it keeps reducer logic clearer and well-tested.
- Likely backend updates if structured ideas are exposed to the browser: `thagid/schemas/brainstorm.py`, `thagid/services/brainstorm.py`, and `thagid/tests/test_brainstorm.py`.
- Likely frontend updates if rendering ideas: `web/src/lib/types/brainstorm.ts`, `web/src/routes/project/[id]/package/[pkgId]/+page.svelte`, `web/src/lib/components/custom/ChatInterface.svelte`, `web/src/lib/components/custom/ChatBubble.svelte`, and new `web/src/lib/components/custom/IdeaCard.svelte`.
- Avoid modifying shadcn-managed files under `web/src/lib/components/ui/`.
- Avoid migrations; this story's structured ideas live in agent checkpoint state only until Epic 3 KG persistence.

### Testing Requirements

- Agent tests should build on `agent/tests/test_brainstorm.py`, which already covers initiation, fallback, selection, status, resume, terminal checkpoint restart, checkpoint failures, message merge behavior, and Story 2.2 swap behavior.
- Add a test where facilitate state has an active technique and no ideas, user sends an ideation message, response stays `facilitate`, and one structured idea is saved and returned.
- Add a test where an incoming similar idea merges into an existing structured idea without increasing `idea_count`.
- Add a test where an incoming contradictory idea updates the existing idea concept or preserves it with explicit tension, without appending an avoidable duplicate.
- Add a test where repeated category/title similarity triggers a pivot prompt while preserving all ideas.
- Add a regression test where `Use Mind Mapping` during facilitate still swaps technique and preserves structured ideas.
- Add a checkpoint merge test where two concurrent saves add different structured ideas and both survive after `_merge_state_messages`/save behavior runs.
- If browser-facing responses include `ideas`, add schema/service tests for valid idea objects and invalid agent `ideas` shapes.
- If `IdeaCard.svelte` is added, add focused Vitest/Svelte Testing Library coverage for title, concept, category, novelty, and accessible article semantics.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story-2.3-Facilitation-Loop-With-Real-Time-Idea-Management]
- [Source: _bmad-output/planning-artifacts/prd.md#Migration-Source-BMAD-Brainstorming-Skill]
- [Source: _bmad-output/planning-artifacts/prd.md#Brainstorm-Ideation]
- [Source: _bmad-output/planning-artifacts/prd.md#Non-Functional-Requirements]
- [Source: _bmad-output/planning-artifacts/architecture.md#LangGraph-State-Machine]
- [Source: _bmad-output/planning-artifacts/architecture.md#LangGraph-State-Reducer-Pattern]
- [Source: _bmad-output/planning-artifacts/architecture.md#Frontend-Integration]
- [Source: design-system/thagid/MASTER.md#Idea-Card]
- [Source: design-system/thagid/pages/package-chat.md#Chat-Bubbles]
- [Source: _bmad-output/implementation-artifacts/2-2-technique-picker-and-mid-session-swap.md#Previous-Story-Intelligence]

## Project Structure Notes

- The implemented prototype is intentionally simpler than the architecture target. For this story, extending `agent/main.py` is less risky than creating the full future LangGraph directory structure.
- The checkpoint `ideas` list is the only persistence layer needed for this story. KG Session/Theme/Idea/ContextChunk nodes arrive in Epic 3.
- If frontend structured rendering proves too large, keep UI changes minimal and still ensure `idea_count` and assistant text reflect accumulated ideas.
- Latest technical research was not required for this story because it introduces no new framework/library/API surface; use the versions and patterns already documented in project artifacts.

## Dev Agent Record

### Agent Model Used

openai/gpt-5.5

### Debug Log References

- `rtk pytest agent/tests/test_brainstorm.py` - 47 passed
- `rtk pytest thagid/tests/test_brainstorm.py thagid/tests/test_internal.py` - 41 passed
- `rtk npm run check` - 0 errors, 0 warnings
- `rtk npm run test:unit` - 20 passed
- `rtk pytest` - 162 passed

### Completion Notes List

- Ultimate context engine analysis completed - comprehensive developer guide created.
- Implemented deterministic structured idea extraction, normalization, reduction, contradiction handling, and anti-bias pivot prompting for facilitate-phase brainstorm messages.
- Preserved Story 2.2 technique selection/swap behavior while returning cumulative structured ideas and keeping themes, active documents, and summaries unchanged.
- Extended checkpoint merge behavior to preserve concurrent structured idea additions through the same reducer.
- Exposed cumulative structured ideas through agent, backend, and frontend brainstorm status/message contracts.
- Added cumulative idea card rendering in package chat using structured response data, plus focused agent, backend, and frontend tests.

### File List

- agent/checkpoint.py
- agent/ideas.py
- agent/main.py
- agent/tests/test_brainstorm.py
- thagid/schemas/brainstorm.py
- thagid/services/brainstorm.py
- thagid/tests/test_brainstorm.py
- web/src/lib/components/custom/ChatInterface.svelte
- web/src/lib/components/custom/IdeaCard.svelte
- web/src/lib/types/brainstorm.ts
- web/src/routes/project/[id]/package/[pkgId]/+page.svelte
- web/tests-unit/idea-card.test.ts

### Change Log

- 2026-05-11: Implemented Story 2.3 facilitation loop with real-time structured idea management and moved story to review.
- 2026-05-11: Code review findings addressed and story moved to done.
