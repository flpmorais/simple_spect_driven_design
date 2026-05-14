# Story 3.5: BMAD Markdown Rendering and Final Session Summary

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a package user,
I want a BMAD-compatible markdown artifact from my finalized brainstorm,
so that the session produces a usable output document without manual formatting.

## Acceptance Criteria

1. Given validated brainstorm data exists, when the markdown phase runs, then Python renders BMAD-compatible markdown from structured Session, Theme, Idea, and ContextChunk data, and the LLM does not freeform-generate the markdown document.
2. Given the session summary and key insights are generated, when markdown rendering completes, then the artifact includes session overview, techniques used, themes, ideas, and key insights, and the session phase becomes Concluded.
3. Given markdown rendering fails, when the agent handles the failure, then the structured KG data remains saved, and the user receives a clear error response that can be retried.

## Tasks / Subtasks

- [x] Add deterministic markdown rendering helpers (AC: 1, 2)
  - [x] Add a focused module such as `agent/markdown_renderer.py` instead of embedding the renderer directly in the large `agent/main.py` flow.
  - [x] Render from structured checkpoint data only: `session_id`, package/project ids if present, active technique, `themes`, `ideas`, `active_documents`, final summary, key insights, and finalized timestamp.
  - [x] Do not call an LLM for markdown generation. Python must produce the final markdown string deterministically.
  - [x] Escape or normalize user-provided markdown-sensitive text enough to keep headings/lists readable and prevent malformed tables; do not introduce a markdown library unless the user explicitly approves a new dependency.
  - [x] Include YAML frontmatter compatible with the existing BMAD brainstorm output shape where practical: `stepsCompleted`, `session_active`, `workflow_completed`, `session_topic`, `session_goals`, `selected_approach`, `techniques_used`, and `ideas_generated`.
  - [x] Include these sections at minimum: `# Brainstorming Session Results`, `Session Overview`, `Technique Selection`, `Idea Organization and Themes`, `Key Insights`, `Context Sources`, and `Session Summary and Next Steps`.
  - [x] Keep the output valid Markdown as plain text. The runtime does not need to write a filesystem artifact in this story.
- [x] Generate final summary and key insights from finalized brainstorm state (AC: 2)
  - [x] Add deterministic helper functions for `final_summary` and `key_insights`; use existing state fields instead of adding an LLM integration.
  - [x] Summary should mention idea count, theme count, technique used, context source count, and the dominant themes.
  - [x] Key insights should be derived from theme summaries and idea concepts, with stable ordering and a bounded count such as 3-5 insights.
  - [x] Preserve any existing rolling `summary` context by folding it into the final summary when useful, but do not overwrite important final facts with stale rolling-summary text.
  - [x] Store `final_summary`, `key_insights`, `markdown`, and `finalized_at` in checkpoint state after successful rendering.
- [x] Wire markdown rendering into the current Extract confirmation flow (AC: 1, 2, 3)
  - [x] Update the `phase == "extract"` confirmation branch in `agent/main.py` after successful theme confirmation and KG persistence.
  - [x] Before building the KG payload, compute and set the final summary in state so `KGWriteRequest.summary` stores the final session summary rather than only the rolling facilitation summary.
  - [x] Preserve Story 3.2/3.4 behavior: KG persistence still happens only after final grouping confirmation, remains idempotent with `kg_write_completed`, and still queues embeddings asynchronously on backend success.
  - [x] If `kg_write_completed is True` and `markdown` already exists in checkpoint state, return the existing markdown and do not call the backend KG endpoint again.
  - [x] If `kg_write_completed is True` but `markdown` is missing, render markdown from checkpoint state and conclude without re-writing KG nodes.
  - [x] If KG persistence fails, do not render markdown and preserve the existing recoverable Extract-phase error behavior.
  - [x] If markdown rendering fails after KG persistence succeeds, keep `kg_write_completed` and `kg_node_ids` intact, keep the session recoverable in `extract` or `markdown`, and return a clear retryable error.
  - [x] On successful rendering, set `state["phase"] = "concluded"` and `state["status"] = "concluded"` or the existing terminal status value used by checkpoint code.
- [x] Expose markdown through existing agent/backend/frontend contracts (AC: 1, 2)
  - [x] The agent already returns `markdown: None`; change successful conclusion responses to include the rendered markdown string.
  - [x] Update `thagid/schemas/brainstorm.py` to add optional `markdown: str | None = None` to `BrainstormMessageResponse`; add it to status only if concluded status needs to surface it before terminal hiding.
  - [x] Update `thagid/services/brainstorm.py` to parse optional `markdown` from agent responses and include it in the browser-facing response.
  - [x] Update `web/src/lib/types/brainstorm.ts` with optional `markdown` on message responses.
  - [x] Update `web/src/routes/project/[id]/package/[pkgId]/+page.svelte` and `ChatInterface.svelte` so the Markdown/Concluded response can display the markdown artifact.
  - [x] Persist the markdown content in the assistant chat message content or otherwise ensure a page reload still shows the final artifact through the existing message history. Do not rely only on transient component state for the final artifact.
  - [x] Do not add a markdown parser dependency. Display the artifact as escaped preformatted markdown or use the existing lightweight `ChatBubble` handling if that remains readable.
- [x] Apply concluded-session UX behavior without overbuilding (AC: 2)
  - [x] Show the phase badge as `Concluded` for the immediate response after finalization.
  - [x] Disable brainstorm file, URL, technique, and send controls while `brainstormPhase` is `markdown` or `concluded`, matching the UX spec.
  - [x] Keep the normal package chat history readable. On reload, `brainstorm/status` may return inactive for concluded sessions; message history must still show the final markdown response.
  - [x] Do not implement Epic 4 summary cards, detail pages, retrieval APIs, vector search, or dashboard entry points in this story.
- [x] Preserve boundaries and compatibility (AC: 1, 2, 3)
  - [x] Preserve existing non-brainstorm package chat behavior.
  - [x] Preserve Story 3.1 theme grouping and adjustment behavior before confirmation.
  - [x] Preserve Story 3.2 KG write metadata: `themes_confirmed`, `kg_write_completed`, and `kg_node_ids`.
  - [x] Preserve Story 3.4 async embeddings behavior in `thagid/routers/kg.py`; markdown rendering happens in the agent after KG response, not in the backend background embedding flow.
  - [x] Story 3.3 may still be `ready-for-dev` rather than done. If validation helpers are present in the codebase, reuse them; if not, add only the minimal pre-render checks needed to avoid rendering empty/invalid themes and do not take over node versioning scope.
  - [x] Do not migrate the prototype to the future `agent/brainstorm/nodes/markdown.py` layout unless that migration already exists when implementing.
- [x] Add focused tests and verification (AC: 1, 2, 3)
  - [x] Add renderer unit tests for frontmatter, required sections, theme/idea rendering, context source rendering, key insights, deterministic output ordering, and markdown-sensitive text escaping/normalization.
  - [x] Add agent tests for confirmed Extract flow: successful KG write computes final summary, renders markdown, stores `markdown`/`final_summary`/`key_insights`, sets phase/status concluded, and returns markdown.
  - [x] Add idempotency tests: repeated confirmation with existing `kg_write_completed` and `markdown` does not call KG again and returns the same markdown.
  - [x] Add recovery tests: KG failure does not render markdown; markdown failure after KG success preserves KG metadata and returns a retryable user-facing error.
  - [x] Add backend service/schema tests proving optional `markdown` passes through `send_brainstorm_message` without breaking existing responses.
  - [x] Add frontend tests proving markdown output renders in package chat and concluded/markdown phases disable send and attachment controls.
  - [x] Run `rtk pytest agent/tests/test_brainstorm.py -q`.
  - [x] Run `rtk pytest thagid/tests/test_brainstorm.py thagid/tests/test_agent_client.py -q`.
  - [x] Run `rtk npm run check` from `web/`; run focused Vitest tests if frontend tests are added.

### Review Findings

- [x] [Review][Patch] KG write idempotency can be bypassed after successful persistence [agent/main.py:790, agent/main.py:825]

## Dev Notes

### Scope Boundaries

- This story completes the Epic 3 output pipeline by rendering deterministic BMAD-compatible markdown and concluding the brainstorm session.
- This story should not add new LLM calls, new Python packages, new storage tables, or filesystem artifact writes.
- The final artifact should be available to the user through the existing package chat flow.
- Epic 4 owns dashboard summary cards, detail views, and retrieval APIs. Do not start those features here.
- Story 3.4 changes are currently in review in the worktree. Do not revert or rewrite those changes; preserve backend embedding queue behavior.

### Current Codebase State

- `agent/main.py` currently centralizes the brainstorm state machine. It supports phases `initiate`, `facilitate`, `extract`, `validate`, `markdown`, and terminal `concluded`, but `markdown` behavior is not implemented yet.
- `agent/main.py` currently returns `markdown: None` in brainstorm responses.
- Extract confirmation currently calls `persist_brainstorm_output`, stores `themes_confirmed`, `kg_write_completed`, and `kg_node_ids`, then replies `Theme groupings confirmed and persisted to the knowledge graph.`
- `_build_kg_write_payload` currently passes `state["summary"]` into KG persistence. In this story, compute final summary before payload building so the KG Session node receives the final user-facing summary.
- `agent/checkpoint.py` treats `concluded` as terminal and `brainstorm/status` returns inactive for terminal checkpoints.
- `thagid/services/brainstorm.py` currently ignores any `markdown` field from the agent and returns `BrainstormMessageResponse` without markdown.
- `web/src/lib/types/brainstorm.ts` currently has no `markdown` field on responses.
- `ChatInterface.svelte` currently renders theme cards during Extract and current ideas, but no final markdown artifact panel. File and URL controls are already disabled outside Facilitate; send remains enabled for concluded phases unless changed.
- `ChatBubble.svelte` has a minimal assistant renderer for bold, inline code, and newlines. It is not a full Markdown renderer.

### Required Markdown Shape

Use this stable structure unless implementation discovers a stronger existing pattern:

```markdown
---
stepsCompleted: [1, 2, 3, 4]
session_active: false
workflow_completed: true
session_topic: '<package title or brainstorm package scope>'
session_goals: '<derived from package description or final summary>'
selected_approach: 'package-brainstorm'
techniques_used: ['<technique>']
ideas_generated: ['<idea title>', ...]
---

# Brainstorming Session Results

**Facilitator:** Thagid Brainstorm Agent
**Date:** <ISO date or YYYY-MM-DD>

## Session Overview
...

## Technique Selection
...

## Idea Organization and Themes
...

## Key Insights
...

## Context Sources
...

## Session Summary and Next Steps
...
```

Do not copy the old BMAD brainstorming skill's interactive action-planning flow wholesale. This product flow already reviewed themes in Story 3.1 and persisted structured data in Story 3.2. The renderer should summarize finalized structured state, not restart prioritization with the user.

### Required Finalization Behavior

- Finalization starts from Extract phase after the user confirms theme groupings.
- If validation helpers from Story 3.3 exist, call them before KG persistence or rendering. If they do not exist, require at least one non-empty theme and at least one idea before rendering.
- Generate `final_summary` and `key_insights` deterministically before KG write.
- Persist KG data before returning the final markdown. If KG write fails, do not claim finalization succeeded.
- Render markdown after KG persistence succeeds.
- On success, append/save an assistant message containing the final markdown or a durable reference to it through the existing message persistence path.
- Set checkpoint `phase` and `status` to terminal values after successful rendering.
- Concluded checkpoints should no longer appear as active sessions through status, but their persisted chat messages should remain visible.

### Architecture Guardrails

- Follow the existing prototype structure. Architecture describes future `agent/brainstorm/nodes/markdown.py`, but current implementation remains in `agent/main.py` plus small helper modules.
- Agent code must continue calling backend KG endpoints over HTTP via `agent/backend_client.py`. Do not import `thagid.*` into `agent/`.
- Backend code must continue using Router -> Service -> Model. Browser-facing routes stay under `/api/packages/{package_id}/brainstorm/...`.
- Python renders markdown from structured data. The LLM must not freeform-generate the markdown document.
- Do not add raw Cypher, graph traversal retrieval, vector search, or additional KG writes for markdown.
- Do not add a Markdown parsing/rendering package for frontend display. A preformatted markdown artifact is enough for MVP.

### Previous Story Intelligence

- Story 3.4 is in review and added async idea embeddings after KG persistence. Markdown rendering should not wait for embeddings and should not alter the embedding background task path.
- Story 3.4 added `OPENAI_API_KEY` and `EmbeddingService`; this story should not add any new external API integration.
- Story 3.3 is still `ready-for-dev` in sprint status. Its story file specifies deterministic validation and versioning, but implementation may not exist yet. Reuse implementation only if it is present when developing this story.
- Story 3.2 is done and established KG persistence after theme confirmation, with stable `kg_write_completed` and `kg_node_ids` checkpoint metadata.
- Story 3.1 is done and established deterministic theme grouping and text-based theme adjustment; every final markdown theme should come from confirmed `state["themes"]`.
- Story 2.5 and 2.6 established `active_documents` entries for file and URL context. Render source refs and summaries in `Context Sources`; do not include full raw file or URL content in markdown by default.
- Recent git history: `feat: add knowledge graph persistence`, `feat: add theme grouping review`, `feat: add URL context ingestion`, `feat: add text file context ingestion`, and `feat: add brainstorm idea management and summaries`.

### File Structure Requirements

- Likely new agent file: `agent/markdown_renderer.py`.
- Likely agent updates: `agent/main.py` and `agent/tests/test_brainstorm.py`.
- Likely backend updates: `thagid/schemas/brainstorm.py`, `thagid/services/brainstorm.py`, and `thagid/tests/test_brainstorm.py`.
- Likely frontend updates: `web/src/lib/types/brainstorm.ts`, `web/src/routes/project/[id]/package/[pkgId]/+page.svelte`, `web/src/lib/components/custom/ChatInterface.svelte`, and a focused component test if markdown display changes are non-trivial.
- Avoid migrations, new models, KG schema changes, and backend KG service changes unless required by existing tests.

### Testing Requirements

- Renderer tests should not need FastAPI, PostgreSQL, AGE, pgvector, or OpenAI.
- Agent finalization tests should mock `persist_brainstorm_output` and checkpoint saves.
- Backend tests should mock `agent_client.agent_brainstorm_message` and assert `markdown` remains optional/backward-compatible.
- Frontend tests should verify both immediate markdown display and disabled controls for terminal phases.
- Preserve existing tests that assert earlier phases return `markdown is None`; update only tests for the finalization path.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story-3.5-BMAD-Markdown-Rendering-and-Final-Session-Summary]
- [Source: _bmad-output/planning-artifacts/prd.md#Brainstorm-Output]
- [Source: _bmad-output/planning-artifacts/architecture.md#LangGraph-State-Machine]
- [Source: _bmad-output/planning-artifacts/architecture.md#Agent-Backend-HTTP-Contract]
- [Source: _bmad-output/planning-artifacts/architecture.md#Project-Structure-and-Boundaries]
- [Source: .agents/skills/bmad-brainstorming/template.md]
- [Source: .agents/skills/bmad-brainstorming/steps/step-04-idea-organization.md]
- [Source: _bmad-output-old/main/brainstorming/brainstorming-session-2026-05-07-0930.md]
- [Source: _bmad-output/implementation-artifacts/3-4-async-embeddings-for-brainstorm-ideas.md#Completion-Notes-List]
- [Source: agent/main.py]
- [Source: agent/checkpoint.py]
- [Source: agent/backend_client.py]
- [Source: thagid/services/brainstorm.py]
- [Source: thagid/schemas/brainstorm.py]
- [Source: web/src/lib/components/custom/ChatInterface.svelte]
- [Source: web/src/lib/components/custom/ChatBubble.svelte]
- [Source: _bmad-output-old/main/project-context.md#Critical-Implementation-Rules]

## Project Structure Notes

- This story is the bridge between the current active brainstorm flow and Epic 4's later review surfaces. It should produce a durable markdown artifact in chat, then stop.
- The old BMAD brainstorm output files are useful formatting references, but current Thagid data is theme/idea/context structured state, not a freeform brainstorming transcript.
- A small renderer module is the minimum useful abstraction here because it can be unit-tested independently and keeps `agent/main.py` from growing further.

## Dev Agent Record

### Agent Model Used

openai/gpt-5.5

### Debug Log References

- `rtk pytest agent/tests/test_markdown_renderer.py agent/tests/test_brainstorm.py -q` - 96 passed
- `rtk pytest agent/tests/test_brainstorm.py -q` - 93 passed
- `rtk pytest thagid/tests/test_brainstorm.py thagid/tests/test_agent_client.py -q` - 50 passed
- `rtk npm run test:unit -- ChatInterface.test.ts` - 17 passed
- `rtk pytest -q` - 245 passed
- `rtk npm run check` - 0 errors, 0 warnings

### Completion Notes List

- Ultimate context engine analysis completed - comprehensive developer guide created.
- Added deterministic BMAD markdown rendering from structured brainstorm checkpoint data without LLM calls or new dependencies.
- Final extract confirmation now computes final summary/key insights before KG write, persists KG metadata, renders markdown, stores final fields, and concludes the checkpoint.
- Backend and frontend now pass through and persist the markdown artifact in assistant chat history; concluded/markdown phases lock brainstorm controls.
- Added renderer, agent, backend, and frontend tests for success, idempotency, recovery, pass-through, display, and disabled controls.

### File List

- `_bmad-output/implementation-artifacts/3-5-bmad-markdown-rendering-and-final-session-summary.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `agent/main.py`
- `agent/markdown_renderer.py`
- `agent/tests/test_brainstorm.py`
- `agent/tests/test_markdown_renderer.py`
- `thagid/schemas/brainstorm.py`
- `thagid/services/brainstorm.py`
- `thagid/tests/test_brainstorm.py`
- `web/src/lib/components/custom/ChatBubble.svelte`
- `web/src/lib/components/custom/ChatInterface.svelte`
- `web/src/lib/components/custom/ChatInterface.test.ts`
- `web/src/lib/types/brainstorm.ts`

### Change Log

- 2026-05-11: Implemented deterministic BMAD markdown rendering and final brainstorm conclusion flow.
