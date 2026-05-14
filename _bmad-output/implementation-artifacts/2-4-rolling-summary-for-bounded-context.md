# Story 2.4: Rolling Summary for Bounded Context

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a package user,
I want long brainstorm sessions to stay coherent without loading the full conversation every turn,
so that responses remain timely and context-aware.

## Acceptance Criteria

1. Given a brainstorm session reaches the configured summary threshold of approximately 20 messages, when the next agent turn is processed, then the agent updates the rolling summary, and preserves key decisions, active technique, documents, and important ideas.
2. Given the rolling summary exists, when the facilitator prepares a response, then it uses the summary instead of relying on the full conversation history, and token overhead remains within the documented target range.
3. Given summary generation fails, when the agent handles the turn, then the user still receives a response if possible, and the failure is logged for diagnosis.

## Tasks / Subtasks

- [x] Define rolling summary checkpoint fields and constants (AC: 1, 2)
  - [x] Add `SUMMARY_TRIGGER_MESSAGE_COUNT = 20` and `SUMMARY_RECENT_MESSAGE_WINDOW = 8` in the agent layer.
  - [x] Keep `state["summary"]` as `str | None` for compatibility with existing checkpoints and `agent/main.py` return shape.
  - [x] Add `state["message_count_total"]` as the authoritative total brainstorm message count after checkpoint compaction.
  - [x] Add `state["summarized_message_count"]` as the total count included in the latest rolling summary.
  - [x] Initialize new checkpoints with `message_count_total = len(state["messages"])` after the initiation assistant reply is appended, usually `2`, and `summarized_message_count = 0`.
  - [x] Existing checkpoints without the new counters must continue to resume by deriving totals from `len(state["messages"])`.
  - [x] Normalize missing counters before trigger checks, status responses, and checkpoint saves so old checkpoints cannot produce off-by-threshold behavior.
- [x] Implement deterministic rolling summary generation (AC: 1, 3)
  - [x] Add the smallest helper needed, preferably `agent/summary.py`, rather than bloating `agent/main.py`.
  - [x] Generate summary deterministically from previous summary, messages being compacted, active technique, structured ideas, active documents, and current phase.
  - [x] Summary must preserve key decisions, active technique, important idea titles/concepts, document/source refs, and unresolved tensions from Story 2.3 contradiction handling.
  - [x] Keep the summary compact and bounded with a defined max length, for example `SUMMARY_MAX_CHARS = 2_000`.
  - [x] Do not introduce an LLM/API call for summarization in this story. Deterministic Python summarization is sufficient for the prototype and avoids new failure modes.
  - [x] If summary helper raises unexpectedly, catch it in `agent/main.py`, log with `logger.exception`, keep the session response flowing, and do not corrupt the existing summary.
- [x] Compact checkpoint messages after summary updates (AC: 1, 2)
  - [x] Trigger summary after a facilitate turn when `message_count_total - summarized_message_count >= SUMMARY_TRIGGER_MESSAGE_COUNT`.
  - [x] Append the current user and assistant messages first, then summarize older messages while keeping only the latest `SUMMARY_RECENT_MESSAGE_WINDOW` messages in `state["messages"]`.
  - [x] Do not compact during `initiate` before a technique is selected.
  - [x] Preserve `ideas`, `themes`, `active_documents`, `summary`, `technique`, `phase`, and `status` when compacting.
  - [x] Ensure `message_count_total` continues increasing by two for each normal brainstorm turn even after `state["messages"]` is compacted.
  - [x] Do not lose displayed transcript history; the browser transcript remains stored in the backend `messages` table.
- [x] Use bounded context for facilitation behavior (AC: 2)
  - [x] Add a small context-building helper that returns summary + recent messages + active technique + structured ideas + active documents.
  - [x] Normal facilitate replies and future prompt construction must use this bounded context helper, not the entire checkpoint `messages` list.
  - [x] Add a focused regression test that seeds a summary, recent window, and older unique message content, then proves facilitation context contains summary + recent messages + structured state but not compacted-away old messages.
  - [x] Keep Story 2.3 idea extraction/reduction running against the current user message and existing ideas.
  - [x] Keep Story 2.3 anti-bias pivoting based on structured ideas, not full transcript history.
  - [x] Do not expose rolling summary in chat UI unless needed for debugging; it is agent state, not user-facing content for this story.
- [x] Update status/message count behavior without UI regressions (AC: 1, 2)
  - [x] Update `agent/main.py` status and message responses so `message_count` uses `message_count_total` when present, falling back to `len(messages)` for older checkpoints.
  - [x] Stop returning rolling summary through the internal response `markdown` field during facilitate/initiate. `markdown` must remain `None` until Epic 3 BMAD markdown rendering.
  - [x] Update `thagid/services/brainstorm.py` only if validation needs to tolerate new response fields; keep browser-facing `BrainstormMessageResponse` and `BrainstormStatusResponse` backward-compatible.
  - [x] Do not add a frontend display for `summary`; existing chat header message count must remain accurate after compaction.
  - [x] Do not change regular non-brainstorm `/api/packages/{package_id}/messages` behavior.
- [x] Preserve checkpoint merge safety (AC: 1, 2, 3)
  - [x] Update `agent/checkpoint.py` merge behavior if needed so concurrent saves preserve `summary`, `message_count_total`, `summarized_message_count`, and compacted messages safely.
  - [x] If one concurrent save has a more advanced summary/counter state, preserve the more advanced counters and avoid expanding compacted messages incorrectly.
  - [x] Handle compacted-vs-stale-full-history safely: if current persisted state has compacted recent `messages` plus higher counters and a stale save still contains old full `messages`, keep the compacted recent window, preserve the advanced summary/counters, and still merge concurrent structured ideas.
  - [x] Continue preserving Story 2.3 concurrent structured idea additions via `reduce_ideas`.
  - [x] Do not let summary failure roll back successful user/assistant message persistence unless the checkpoint save itself fails.
- [x] Preserve prior and future story boundaries (AC: 1, 2, 3)
  - [x] Story 2.1 recommendations and initiate-phase selection still work.
  - [x] Story 2.2 technique picker and facilitate-phase swaps still work and preserve summary/counters.
  - [x] Story 2.3 structured idea extraction, duplicate reduction, contradiction handling, anti-bias pivoting, cumulative idea cards, and status/resume still work.
  - [x] Story 2.5 file/context ingestion remains out of scope for implementation here; if `active_documents` exists from future/current work, include document refs in summary without requiring file upload UI.
  - [x] Do not implement conclusion, theme grouping, KG writes, embeddings, markdown rendering, file upload, or URL ingestion in this story.
- [x] Add focused tests and verification (AC: 1, 2, 3)
  - [x] Add agent tests for summary trigger at 20 messages, compacting to recent window, preserving total message count, preserving active technique, ideas, active documents, and phase.
  - [x] Add agent tests proving facilitate response still succeeds when summary helper raises, and the failure is logged or observable through monkeypatched logger assertions.
  - [x] Add agent tests proving status response uses `message_count_total` after compaction.
  - [x] Add checkpoint merge tests for concurrent summary/counter state and concurrent idea preservation.
  - [x] Add backend tests only if response validation changes.
  - [x] Run `rtk pytest agent/tests/test_brainstorm.py`.
  - [x] Run `rtk pytest thagid/tests/test_brainstorm.py thagid/tests/test_internal.py` if backend contracts change.
  - [x] Run `rtk npm run check` from `web/` only if frontend files are touched; frontend edits should not be necessary for this story.

### Review Findings

- [x] [Review][Patch] Concurrent compacted-vs-stale save drops a successful turn [agent/checkpoint.py:33]
- [x] [Review][Patch] Concurrent idea additions can be lost during normal checkpoint merge [agent/checkpoint.py:41]
- [x] [Review][Patch] Concurrent summaries with equal counters overwrite one summary path [agent/checkpoint.py:81]
- [x] [Review][Patch] Summary truncation can drop newly compacted or required preserved content [agent/summary.py:57]
- [x] [Review][Patch] Summary idea preservation ignores important later tensions [agent/summary.py:62]
- [x] [Review][Patch] Bounded context helper does not enforce the recent-message window [agent/summary.py:23]

## Dev Notes

### Scope Boundaries

- This story is agent/checkpoint bounded-context work. It should not add chat UI, new user-facing summary cards, file upload, URL sharing, theme grouping, KG writes, embeddings, or markdown rendering.
- Do not introduce new libraries or LLM calls for summarization. Deterministic Python summarization is the minimal correct prototype approach.
- Do not create the future `agent/brainstorm/` LangGraph folder layout. The current prototype centralizes brainstorm behavior in `agent/main.py`; add a helper module only if it keeps code clearer.
- Do not prune the backend `messages` table. It is the displayed transcript source established by earlier stories.

### Current Codebase State

- `agent/main.py` implements `/internal/agent/brainstorm/message` and `/internal/agent/brainstorm/status` with `X-Agent-Key` auth.
- Active checkpoint validation currently allows `summary` but does not validate its type and returns it as the `markdown` field in the internal agent response.
- New sessions initialize `summary: None`, `messages` with the initial user message and recommendation reply, empty `ideas`, empty `themes`, empty `active_documents`, `phase: "initiate"`, and `status: "active"`.
- Existing status response uses `len(messages)` for `message_count`; this will become wrong if checkpoint `messages` is compacted unless `message_count_total` is introduced and used.
- Existing facilitate behavior appends user and assistant messages, runs Story 2.3 idea extraction/reduction, then saves the whole checkpoint.
- `agent/checkpoint.py` currently merges concurrent message appends and preserves concurrent structured ideas through `reduce_ideas`.
- `thagid/services/brainstorm.py` validates `message_count` as an integer and forwards it to the browser. It does not know about summary state.
- `web/src/routes/project/[id]/package/[pkgId]/+page.svelte` displays `message_count` from brainstorm status/message responses in the chat header.
- `agent/main.py` currently returns `markdown: summary` in existing-session responses. This story must correct that leak so rolling context is not mistaken for final BMAD markdown.

### Required Implementation Behavior

- Keep the visible transcript intact through the backend `messages` table; checkpoint compaction only affects agent continuity state.
- After summary exists, facilitation context should be constructed from `summary`, the most recent checkpoint messages, active technique, structured ideas, and active documents.
- `message_count_total` must count all brainstorm checkpoint messages, not only recent retained messages.
- `summarized_message_count` must prevent repeated summarization on every turn after the threshold.
- For old checkpoints, missing `message_count_total` means `len(messages)` and missing `summarized_message_count` means `0` until the first normalized save.
- Summary trigger should be checked after a turn has produced the assistant reply so the turn can be included in the summary/compaction decision.
- Summary generation failure should be non-fatal. The user should still receive the normal facilitate response if checkpoint save succeeds.
- If checkpoint save fails, preserve existing behavior: return the standard brainstorm error and do not persist partial backend transcript.
- Keep response `state_change` unchanged for normal facilitate flow.
- Keep `summary` internal for this story. Do not display it in chat and do not rename it to `markdown` in public types.
- Facilitate/initiate responses must keep `markdown: None`; rolling summary is context, not a markdown artifact.

### Summary Content Requirements

- Include active technique by exact display name.
- Include important idea titles and concise concept details from structured ideas.
- Include active document source refs and summaries if `active_documents` contains future Story 2.5 chunks.
- Include decisions and tensions visible in compacted messages or idea concepts, especially Story 2.3 `Tension:` text.
- Include enough recent user intent to make future facilitation coherent.
- Keep output deterministic and bounded; trim older details before exceeding `SUMMARY_MAX_CHARS`.

### Backend And Agent Contract Guardrails

- Browser traffic continues through FastAPI `/api/packages/{package_id}/brainstorm/...`; browser never calls `thagid-agent` directly.
- Internal backend/agent traffic continues using `X-Agent-Key`.
- Existing non-brainstorm chat endpoint remains unchanged.
- Existing browser-facing response fields remain stable: `message`, `session_id`, `phase`, `technique`, `idea_count`, `message_count`, and `ideas`.
- Do not import `thagid.*` backend services/models into `agent/`; keep container boundaries strict.
- If extra internal response fields are added for debugging, backend Pydantic schemas should ignore or safely tolerate them. Prefer not adding user-facing fields.

### Architecture And Product Context

- PRD FR16 requires a rolling summary to keep context bounded.
- NFR1 targets facilitator token overhead around 3.5K-7.7K tokens; bounded summary + recent messages + ideas + documents is the architecture mechanism.
- NFR4 says summarization triggers around every 20 messages and must not disrupt the facilitation loop.
- NFR5 requires LLM/API failures to be handled; this story avoids new LLM calls, but summary helper failures still need standard non-fatal handling.
- Architecture defines `summary: str | None` in `BrainstormState`, with rolling summary in the Facilitate node.
- Architecture says LangGraph state should load only technique + ideas + summary per turn for NFR1. Current prototype should approximate this through a bounded context helper and checkpoint message compaction.

### Previous Story Intelligence

- Story 2.3 is in review and implemented deterministic structured idea extraction, idea reduction, contradiction handling, anti-bias pivot prompting, cumulative idea response fields, and `IdeaCard` rendering.
- Story 2.3 explicitly left `summary` unchanged; this story is the first to mutate `state["summary"]`.
- Story 2.3 checkpoint merge now preserves concurrent structured idea additions. Do not regress it when adding summary counters.
- Story 2.2 implemented technique picker and facilitate-phase technique swaps; swaps preserve `ideas`, `themes`, `active_documents`, `summary`, messages, and phase.
- Story 2.1 established `SCAMPER Method` fallback and exact technique matching for initiate-phase selection.
- Story 1.4 established displayed transcript persistence in `messages` and agent continuity in `agent_checkpoints`.
- Recent git history includes `feat: add technique picker and swaps`, `feat: recommend brainstorm techniques`, `fix: align brainstorm chat accessibility`, `fix: harden brainstorm resume checkpoints`, and `feat: detect existing brainstorm sessions`.

### File Structure Requirements

- Likely agent updates: `agent/main.py`, `agent/checkpoint.py`, `agent/tests/test_brainstorm.py`, and optionally new `agent/summary.py`.
- Likely no frontend updates. If frontend files are touched, preserve `ChatInterface.svelte` idea rendering and header counters.
- Likely no backend updates unless `thagid/services/brainstorm.py` validation must tolerate new internal fields.
- Avoid migrations, new database models, and shadcn-managed UI files.

### Testing Requirements

- Build agent tests in `agent/tests/test_brainstorm.py`, which already covers initiation, status, resume, checkpoint failures, technique swaps, idea extraction, and checkpoint merge behavior.
- Add a test with 18 existing messages in facilitate; after one user/assistant turn, summary updates, `messages` is compacted to the recent window, and `message_count_total` is 20.
- Add a test with an existing summary and `summarized_message_count` where fewer than 20 new messages have accumulated; summary must not update again.
- Add a test where summary helper raises; response still returns 200, messages/ideas still save, and previous summary remains unchanged.
- Add a status test where compacted checkpoint has 8 recent messages and `message_count_total: 24`; response `message_count` must be 24.
- Add a checkpoint merge test where one save has more advanced summary counters and another save adds ideas; merged state preserves both.
- Add a checkpoint merge test for compacted current state versus stale full-history save; merged state must keep compacted recent messages, advanced summary/counters, and concurrent ideas.
- Add a context-helper test proving compacted-away old message content is not included when summary plus recent window exists.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story-2.4-Rolling-Summary-for-Bounded-Context]
- [Source: _bmad-output/planning-artifacts/prd.md#Brainstorm-Ideation]
- [Source: _bmad-output/planning-artifacts/prd.md#Non-Functional-Requirements]
- [Source: _bmad-output/planning-artifacts/architecture.md#LangGraph-State-Machine]
- [Source: _bmad-output/planning-artifacts/architecture.md#Non-Functional-Requirements-Coverage]
- [Source: _bmad-output/planning-artifacts/architecture.md#Agent-Backend-HTTP-Contract]
- [Source: _bmad-output/implementation-artifacts/2-3-facilitation-loop-with-real-time-idea-management.md#Completion-Notes-List]

## Project Structure Notes

- The current prototype is simpler than the architecture target. Implement bounded context in the current `agent/main.py` flow instead of introducing LangGraph nodes prematurely.
- Checkpoint compaction is safe only because the backend `messages` table remains the full visible transcript. Do not use compacted checkpoint messages as the UI transcript source.
- Latest technical research was not required because this story uses existing Python state helpers and does not add new external APIs or dependencies.

## Dev Agent Record

### Agent Model Used

gpt-5.5 (openai/gpt-5.5)

### Debug Log References

- `rtk pytest agent/tests/test_brainstorm.py` - 54 passed
- `rtk pytest agent/tests/test_brainstorm.py` - 63 passed after code review fixes

### Completion Notes List

- Ultimate context engine analysis completed - comprehensive developer guide created.
- Implemented deterministic rolling summary state with `message_count_total`, `summarized_message_count`, threshold compaction, and bounded recent-message retention.
- Kept rolling summary internal by returning `markdown: None` from active brainstorm message responses.
- Hardened checkpoint merges so advanced compacted summary/counter state wins over stale full-history saves while preserving concurrent structured ideas.
- Added focused agent regressions for summary trigger, no re-trigger before threshold, non-fatal summary failure, status message counts, bounded context, and merge safety.

### File List

- `_bmad-output/implementation-artifacts/2-4-rolling-summary-for-bounded-context.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `agent/checkpoint.py`
- `agent/main.py`
- `agent/summary.py`
- `agent/tests/test_brainstorm.py`

### Change Log

- 2026-05-11: Implemented Story 2.4 rolling summary and bounded checkpoint context; targeted agent tests pass.
- 2026-05-11: Code review findings addressed and story moved to done.
