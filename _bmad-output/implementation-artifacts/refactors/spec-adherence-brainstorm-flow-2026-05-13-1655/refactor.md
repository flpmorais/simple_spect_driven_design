---
workflow: bmad-refactor-plan
status: complete
phase: complete
phasesCompleted: [context, exploration, analysis, plan]
refactorName: "spec-adherence-brainstorm-flow"
createdAt: "2026-05-13-1655"
lastUpdated: "2026-05-13-1655"
decisions:
  - id: D1
    decision: "Use an explicit review/confirmation approval pause before KG writes; extract prepares themes only, user confirms, then final persistence and markdown occur."
  - id: D2
    decision: "Use the aggregate transactional brainstorm-output KG endpoint for confirmed finalization; keep granular endpoints for lower-level/internal operations."
  - id: D3
    decision: "Do not edit PRD or architecture during execution; treat them as read-only source-of-truth references and fix implementation/tests to conform to the PRD-required review/confirmation gate where architecture wording is ambiguous."
  - id: D4
    decision: "Remove silent fallbacks for required PydanticAI phases and surface errors through FastAPI after configured retries; tests use explicit fake runners."
blockedIssues: []
executionStatus: complete
executionStartedAt: "2026-05-13-1801"
executionCompletedAt: "2026-05-13-1820"
executionLastUpdated: "2026-05-13-1820"
executionBranch: "1_datapipeline"
sourceBranch: "1_datapipeline"
bundlePath: "_bmad-output/implementation-artifacts/refactors/spec-adherence-brainstorm-flow-2026-05-13-1655"
tasksDir: tasks
---

# Refactor Plan: Spec Adherence Brainstorm Flow

## Context

### Objective

Bring the brainstorm data-pipeline implementation into full adherence with the PRD, architecture decision document, and project context. The refactor must close the identified drift in the brainstorm lifecycle, agent orchestration, KG persistence behavior, rolling summarization, API contract/documented behavior, and UI review flow.

### Motivation

The current implementation has the main structural components in place, but the core behavior has drifted from the specification. In particular, it can skip user-confirmed theme review, silently swallow KG write failures, and run a simplified/fallback-oriented agent flow. The user explicitly wants these issues fixed thoroughly, with no new drift and no simplifications.

### Scope

- Agent brainstorm flow under `agent/`, especially LangGraph topology, node responsibilities, checkpoint state, PydanticAI node execution, theme review/confirmation, extraction, validation, markdown generation, and KG persistence.
- Backend brainstorm and KG integration under `thagid/`, especially internal KG routes, agent proxy behavior, error propagation, KG write/read semantics, and API schema contracts.
- Frontend brainstorm chat/dashboard under `web/src/`, especially active brainstorm status, technique selection, theme review/adjustment, finalization, attachment behavior, and result display.
- Tests across agent, backend, and frontend to lock specification adherence and prevent regressions.
- Read-only planning-artifact conformance checks against `_bmad-output/planning-artifacts/prd.md`, `_bmad-output/planning-artifacts/architecture.md`, and `_bmad-output/project-context.md`.

### Non-Goals

- Do not change or rely on stale `docs/` content.
- Do not introduce a new architecture, framework, library, persistence model, or frontend framework.
- Do not weaken the separate-container boundary between `agent` and `thagid`.
- Do not bypass Router → Service → Model, API client layers, LangGraph/PydanticAI ownership rules, or KG service ownership.
- Do not implement post-MVP features such as multiple brainstorm sessions per package unless required by the current MVP specification.
- Do not make speculative improvements outside the documented drift.

### Constraints

- `_bmad-output/project-context.md` is binding and is the golden source of technical rules.
- PRD and architecture are binding specifications; implementation must conform rather than simplify.
- Agent must remain a separate FastAPI container/package and must communicate with backend over internal HTTP using `X-Agent-Key`.
- LangGraph owns workflow/conversation state; PydanticAI owns individual agent execution; DB/KG owns business/audit records.
- Agent code must not import from `thagid`.
- Application code must not use forbidden LangChain application APIs/classes.
- AGE graph access must remain owned by `KnowledgeGraphService`; Cypher must be parameterized through the project pattern.
- Browser traffic must not call internal KG or agent endpoints directly.
- Existing user-facing routes must remain under `/api/packages/{package_id}/brainstorm/...` with JWT auth.

### Desired Behavior

- Starting a brainstorm reads package context, recommends techniques in the opening message, and persists/resumes state through LangGraph checkpointing.
- Facilitation uses PydanticAI node execution with the specified tool pattern while preserving deterministic guardrails where appropriate and specification-compliant.
- Ideas accumulate in real time with deduplication/contradiction handling and anti-bias domain pivoting.
- Rolling summarization triggers around every 20 messages without disrupting facilitation.
- Text file and URL context ingestion adds `ContextChunk`-compatible active documents and participates in ideation and final persistence.
- When the user indicates completion, the facilitator presents grouped themes for review instead of immediately finalizing.
- The user can adjust groupings and must explicitly confirm before final KG writes and markdown finalization.
- KG write failures during extraction/finalization propagate as errors and do not falsely report completion.
- Finalized sessions write Session, Theme, Idea, and ContextChunk nodes, queue async embeddings, render BMAD-compatible markdown from structured data, and expose dashboard/detail results.
- Agent/backend/frontend contracts are explicit, tested, and aligned with PRD/architecture/project context without editing PRD or architecture.

### Project Context Boundaries

- Backend changes must preserve Router → Service → Model separation.
- Frontend pages must use API client functions; components must not bypass API/state rules.
- Agent code must keep one LangGraph node function per file and preserve the separate service boundary.
- KG operations must stay in `KnowledgeGraphService`; agents must use internal backend HTTP, not direct database/KG imports.
- Tests must cover agent, backend, frontend, and architecture-boundary rules relevant to the refactor.
- Changes must be surgical to the drift areas and avoid unrelated cleanup.

### Known Risks

- LangGraph phase/routing changes can break checkpoint compatibility or active-session resume behavior.
- Enforcing theme review may require schema/status additions that affect frontend and backend assumptions.
- Fixing KG error propagation may reveal existing failures that were previously hidden.
- True PydanticAI execution with retries and typed outputs may require careful test fakes to avoid external LLM calls.
- Maintaining exact architecture boundaries while moving orchestration helpers out of `agent/main.py` may require multiple coordinated changes.
- Existing tests may encode simplified behavior and need updates to match the specification rather than current drift.

### Success Criteria

- Every major drift item identified in the analysis is mapped to explicit implementation tasks and completion checks.
- Automated tests prove theme review/adjustment/confirmation gates finalization and KG writes.
- Automated tests prove KG write failures surface as errors and do not mark sessions concluded.
- Automated tests prove initiate uses package context and technique recommendations as specified.
- Automated tests prove rolling summary behavior is wired into runtime execution.
- Automated tests prove frontend supports the intended review and finalization flow.
- Architecture-boundary tests continue to pass, including agent/backend separation and LangChain ban.
- Backend, agent, and frontend test suites pass after execution of the eventual refactor plan.

## Exploration

### Exploration Scope

Read-only exploration covered the implementation areas named in the confirmed context: `agent/` brainstorm orchestration and checkpointing, `thagid/` brainstorm/KG proxy and persistence services, `web/src/` brainstorm chat/review/results UI, tests, container/config boundaries, and binding planning artifacts. Stale `docs/` content was intentionally ignored.

### Impact Mapper Findings

- The refactor affects the full brainstorm path: agent LangGraph lifecycle, PydanticAI node execution, KG persistence/error propagation, rolling summary wiring, backend proxy/contracts, frontend review/finalization UX, tests, and read-only planning artifact conformance.
- Agent graph topology is a primary change point. Current routing sends `facilitate -> extract` when `conclusion_requested` is set, then `extract -> validate -> markdown -> END`, which conflicts with a mandatory user review/confirmation pause (`agent/brainstorm/graph.py:26-37`, `agent/brainstorm/graph.py:58-62`).
- Agent state/response contracts are central. The state includes phases, themes, documents, summary, validation counters, and response fields beyond the documented internal core contract (`agent/brainstorm/state.py:13-43`, `agent/brainstorm/state.py:74-88`).
- PydanticAI execution needs attention because `run_typed_agent` silently falls back on creation/runtime failures instead of making retry/failure behavior explicit (`agent/brainstorm/agents.py:26-35`).
- Node responsibilities are drift points:
  - `initiate_node` validates preexisting recommendations but does not fetch package context or generate recommendations itself (`agent/brainstorm/nodes/initiate.py:6-21`).
  - `facilitate_node` uses string/regex tool heuristics and does not clearly wire real-time idea extraction, reducers, or anti-bias pivot behavior (`agent/brainstorm/nodes/facilitate.py:11-40`).
  - `extract_node` writes KG output before confirmation and swallows all persistence errors (`agent/brainstorm/nodes/extract.py:16-30`).
  - `validate_node` performs simplified validation/retry behavior (`agent/brainstorm/nodes/validate.py:6-21`).
  - `markdown_node` can fall back to `# Brainstorm Summary` and marks sessions concluded (`agent/brainstorm/nodes/markdown.py:6-15`).
- `agent/main.py` contains richer lifecycle helpers for done intent, theme confirmation, KG payload building, markdown finalization, theme adjustment, file/url ingestion, and rolling summary, but many are not clearly wired into the production graph path (`agent/main.py:128-145`, `agent/main.py:405-543`, `agent/main.py:750-781`).
- KG persistence has two surfaces: granular internal routes and an aggregate `brainstorm-output` route. The aggregate path is transactional (`thagid/services/knowledge_graph.py:127-160`), while granular writes commit independently (`thagid/services/knowledge_graph.py:184-316`). The agent currently uses granular calls (`agent/backend_client.py:58-104`).
- Backend brainstorm proxy routes and schemas are affected: user-facing routes live under `/api/packages/{package_id}/brainstorm/...` (`thagid/routers/brainstorm.py:38-111`), and the service validates agent responses then saves assistant messages (`thagid/services/brainstorm.py:45-123`).
- Frontend impact points include the brainstorm API wrapper (`web/src/lib/api/brainstorm.ts:11-49`), shared types (`web/src/lib/types/brainstorm.ts:1-84`), package chat page (`web/src/routes/project/[id]/package/[pkgId]/+page.svelte:76-130`), and `ChatInterface` review/lock behavior (`web/src/lib/components/custom/ChatInterface.svelte:65-72`, `web/src/lib/components/custom/ChatInterface.svelte:339-350`).
- Binding planning references are `_bmad-output/project-context.md:125-139`, `_bmad-output/planning-artifacts/prd.md:201-271`, and `_bmad-output/planning-artifacts/architecture.md:333-394`, `_bmad-output/planning-artifacts/architecture.md:525-552`.

### Risk Hunter Findings

- Critical: KG persistence can be reported as successful while failing silently because `extract_node` catches all exceptions and passes (`agent/brainstorm/nodes/extract.py:16-30`), conflicting with the requirement that KG write failures surface through FastAPI (`_bmad-output/project-context.md:139`).
- Critical: Agent-side granular KG writes are not atomic. Session, theme, idea, and context endpoints each commit independently, so partial graph persistence is possible (`agent/backend_client.py:58-104`, `thagid/services/knowledge_graph.py:201-224`, `thagid/services/knowledge_graph.py:232-263`, `thagid/services/knowledge_graph.py:269-300`, `thagid/services/knowledge_graph.py:308-315`).
- High: The required user review/confirmation gate can be skipped because the graph can advance from conclusion request through extract, validate, markdown, and END in one invocation (`agent/brainstorm/graph.py:26-37`, `agent/brainstorm/graph.py:58-62`).
- High: Resume routing does not explicitly route active `facilitate` checkpoints back to `facilitate`, risking unintended restart through `initiate` (`agent/brainstorm/graph.py:13-23`).
- High: LangGraph state may not persist all required conversation data if runtime nodes do not append messages/reduce ideas/update summaries as specified (`agent/main.py:753-765`, `agent/brainstorm/state.py:50-57`).
- High: Agent KG payload shape is fragile: `extract_node` passes `result.themes`, while `agent/backend_client.py` expects `theme["source_id"]`; generated themes may use `id`, causing runtime failures that are currently swallowed (`agent/brainstorm/nodes/extract.py:20-27`, `agent/backend_client.py:73-91`, `thagid/schemas/kg.py:16-21`).
- High: Normal brainstorm writes use `MERGE`/`SET` and may overwrite current KG nodes without creating `VERSION_OF` audit history except through `update_node` (`thagid/services/knowledge_graph.py:584-594`, `thagid/services/knowledge_graph.py:629-637`, `thagid/services/knowledge_graph.py:670-678`, `thagid/services/knowledge_graph.py:43-107`).
- High: Initiation does not clearly read package context in the production graph path, despite package context helper availability (`agent/main.py:12`, `agent/main.py:753-765`, `agent/brainstorm/nodes/initiate.py:7-21`).
- High: Frontend review UI may never appear because it renders only for `phase === 'extract'`, while the backend can return `concluded` immediately after a done/conclude message (`web/src/lib/components/custom/ChatInterface.svelte:65-72`, `web/src/lib/components/custom/ChatInterface.svelte:339-350`).
- Medium: Rolling summarization helpers exist but appear disconnected from graph execution, risking NFR4 drift (`agent/summary.py:35-78`, `agent/main.py:128-144`, `agent/main.py:750-765`).
- Medium: PydanticAI failures silently degrade to fallback outputs, masking configuration/LLM/runtime failures and obscuring retry semantics (`agent/brainstorm/agents.py:19-39`, `agent/brainstorm/agents.py:66-82`).
- Medium: Relational chat messages and LangGraph checkpoint messages are coupled indirectly; the frontend can show chat history while agent internal message state may not match (`thagid/services/brainstorm.py:54-61`, `thagid/services/brainstorm.py:102-110`, `web/src/routes/project/[id]/package/[pkgId]/+page.svelte:63-75`, `_bmad-output/project-context.md:130`).

### Test Mapper Findings

- Existing agent coverage is substantial but may encode drift. `agent/tests/test_brainstorm_graph.py` currently expects conclusion to run extract/validate/markdown in one invoke, which must change for mandatory review gating.
- Existing agent tests cover many lifecycle and KG-write behaviors in `agent/tests/test_brainstorm.py`, including auth/session/resume/technique/attachment/finalization areas, but need explicit end-to-end tests through the real graph for initiate → technique select → facilitate → conclude → review → confirm → KG write → markdown.
- Existing KG tests cover graph naming, parameterized writes, deterministic IDs, idempotency, rollback, retrieval, and embeddings in `thagid/tests/test_kg.py`, but need focused coverage for atomic final brainstorm persistence and no partial writes on finalization failure.
- Existing backend tests in `thagid/tests/test_brainstorm.py` cover proxy/status/message contract behavior and should be updated to prove agent errors from finalization surface correctly and user messages/assistant messages are handled consistently.
- Existing frontend Vitest coverage in `web/src/lib/components/custom/ChatInterface.test.ts` covers attachment UX, extract/theme review, concluded markdown, and locked states. It needs stricter tests for explicit review controls, theme confirmation, and not locking before confirmation.
- Existing frontend summary/detail component tests cover results display but not full user flow. Add Playwright coverage for package chat brainstorm start/resume, technique select, phase-based attachments, theme review display, confirmation, summary card, and detail navigation.
- Recommended validation commands after execution: `pytest`; targeted `pytest agent/tests/test_brainstorm.py agent/tests/test_brainstorm_graph.py agent/tests/test_brainstorm_nodes.py agent/tests/test_architecture_boundaries.py thagid/tests/test_brainstorm.py thagid/tests/test_kg.py`; `cd web && npm run check`; `cd web && npm run test:unit`; and `cd web && npm run test:e2e` once UI flow changes land.

### Project Context Auditor Findings

- Binding rules require preserving backend Router → Service → Model layering (`_bmad-output/project-context.md:42`), frontend API-client layering (`_bmad-output/project-context.md:43`, `_bmad-output/project-context.md:81`), and separate agent/backend service boundaries (`_bmad-output/project-context.md:44`, `_bmad-output/project-context.md:162`).
- LangGraph/PydanticAI ownership is mandatory: LangGraph owns workflow/conversation state and checkpointing, PydanticAI owns LLM calls, tools, typed outputs, validation, retries, and structured parsing (`_bmad-output/project-context.md:45-47`, `_bmad-output/project-context.md:130-134`).
- KG access must remain owned by `KnowledgeGraphService`; agents must use internal HTTP, not direct `thagid` imports or raw graph access (`_bmad-output/project-context.md:47`, `_bmad-output/project-context.md:94-98`, `_bmad-output/project-context.md:162-167`).
- User-facing brainstorm routes must remain under `/api/packages/{package_id}/brainstorm/...`; internal KG routes must remain `/internal/kg/projects/{project_id}/...`; browser-to-internal/agent access remains forbidden (`_bmad-output/project-context.md:68-70`, `_bmad-output/project-context.md:127`, `_bmad-output/project-context.md:168`).
- Project context requires agent responses in the agreed internal shape: `reply`, `session_id`, `state_change`, `ideas`, `themes`, `markdown` (`_bmad-output/project-context.md:129`). Public FastAPI responses may wrap this, but the boundary must be explicit and tested.
- Validation behavior is specified: orphan ideas to `General`, empty themes removed, missing summaries generated, no meaningful ideas/themes routes back to facilitation, retry loop capped at 2 (`_bmad-output/project-context.md:136-137`).
- Embeddings remain async/fire-and-forget after successful KG writes, with failures logged and graph nodes preserved (`_bmad-output/project-context.md:138`).
- Potential specification tension: PRD/UX require presenting themes for review/adjustment before finalizing (`_bmad-output/planning-artifacts/prd.md:225-227`), while the architecture says `extract` writes KG nodes (`_bmad-output/planning-artifacts/architecture.md:345-349`). The implementation plan must reconcile this without simplifying the user-confirmation requirement.

### Exploration Limitations

- Exploration was read-only and did not run tests or inspect runtime behavior in a live container.
- Findings are based on static inspection and specialized read-only subagent reports.
- `docs/` was intentionally excluded because the user identified it as stale.

## Analysis

### Required Changes

- Introduce a specification-compliant brainstorm lifecycle gate: conclusion intent must produce theme grouping for review and must not persist KG output or render final markdown until the user explicitly confirms the grouping.
- Rework LangGraph routing so active phases resume correctly, especially `facilitate` and the theme-review/confirmation phase, while preserving checkpointed state across turns.
- Reassign agent node responsibilities to match the architecture and product behavior: initiate reads package context and recommends techniques; facilitate accumulates ideas/documents and detects completion intent; extract prepares themes only; validate enforces structural correctness; finalization persists confirmed output and renders BMAD markdown.
- Replace silent KG persistence failures with surfaced errors that propagate through agent → FastAPI → user-facing backend response.
- Use transactional aggregate KG finalization for confirmed brainstorm output to avoid partial Session/Theme/Idea/ContextChunk writes.
- Wire rolling summary and message compaction into the actual runtime path so LangGraph state persists messages, ideas, themes, active documents, summary, technique, package_id, and session_id.
- Make PydanticAI execution explicit for required phases: no silent success-like fallback; failures surface after configured retry behavior. Tests must use fake runners rather than relying on fallback behavior.
- Align public and internal brainstorm contracts with the specification. The internal agent contract remains `reply`, `session_id`, `state_change`, `ideas`, `themes`, `markdown`; public FastAPI may wrap it as `message`, `phase`, counts, etc., but that bridge must be documented and tested.
- Update frontend chat/review behavior so the user can see themes, adjust via chat or explicit controls, confirm finalization, and only lock once the session is truly concluded.
- Keep PRD and architecture read-only, and fix implementation/tests to follow the accepted interpretation: PRD-required review/confirmation gates KG persistence and markdown finalization where architecture wording is ambiguous.

### Likely Files And Areas

- Agent graph and state: `agent/brainstorm/graph.py`, `agent/brainstorm/state.py`, `agent/checkpoint.py`.
- Agent nodes: `agent/brainstorm/nodes/initiate.py`, `facilitate.py`, `extract.py`, `validate.py`, `markdown.py`, plus a finalization responsibility either in `markdown.py` or a new node only if it preserves the one-node-per-file rule and graph clarity.
- Agent runtime/API boundary: `agent/main.py`, `agent/backend_client.py`, `agent/brainstorm/agents.py`, `agent/summary.py`, `agent/ideas.py`, `agent/markdown_renderer.py`, `agent/brainstorm/tools/*`.
- Backend KG and brainstorm proxy: `thagid/routers/kg.py`, `thagid/services/knowledge_graph.py`, `thagid/schemas/kg.py`, `thagid/routers/brainstorm.py`, `thagid/services/brainstorm.py`, `thagid/schemas/brainstorm.py`, `thagid/services/agent_client.py`.
- Frontend API/types/UI: `web/src/lib/api/brainstorm.ts`, `web/src/lib/types/brainstorm.ts`, `web/src/routes/project/[id]/package/[pkgId]/+page.svelte`, `web/src/lib/components/custom/ChatInterface.svelte`, `TechniquePicker.svelte`, `BrainstormSummaryCard.svelte`, `BrainstormDetailView.svelte`, and related tests.
- Tests: `agent/tests/test_brainstorm.py`, `agent/tests/test_brainstorm_graph.py`, `agent/tests/test_brainstorm_nodes.py`, `agent/tests/test_architecture_boundaries.py`, `thagid/tests/test_brainstorm.py`, `thagid/tests/test_kg.py`, `web/src/lib/components/custom/ChatInterface.test.ts`, summary/detail component tests, and Playwright e2e where available.
- Binding specs, read-only: `_bmad-output/planning-artifacts/prd.md`, `_bmad-output/planning-artifacts/architecture.md`, and `_bmad-output/project-context.md`.

### Behavior To Preserve

- Separate `thagid-agent` service boundary and internal HTTP communication with `X-Agent-Key`.
- User-facing brainstorm routes under `/api/packages/{package_id}/brainstorm/...` with JWT auth.
- Browser never calls internal KG or agent endpoints.
- Existing package chat behavior for non-brainstorm messages.
- Technique picker/browse behavior and one-session-per-package MVP assumption.
- File and URL attachment constraints for brainstorm facilitation.
- KG graph naming, labels, relationships, parameterized Cypher pattern, and relational embedding tables.
- Async/fire-and-forget embeddings after successful KG writes.
- BMAD-compatible markdown rendered by Python from structured data, not freeform LLM markdown.
- Dashboard/detail display of finalized brainstorm results.

### Project Context Constraints

- Backend must preserve Router → Service → Model; routers map HTTP, services own business logic, models/schemas define data shapes.
- Frontend pages must use API client functions; components must not use raw `fetch()` or call internal endpoints.
- Agent must not import `thagid`; KG operations happen through backend internal HTTP and `KnowledgeGraphService`.
- LangGraph owns workflow/conversation state, approval pauses, resume, retry loops, long-running state, and checkpoint history.
- PydanticAI owns LLM calls, tool registration, typed outputs, argument validation, agent-level retry, and structured parsing.
- Application code must not use forbidden LangChain APIs/classes.
- KG updates/versioning and final writes must not create hidden audit/data inconsistencies.
- Validation must auto-correct structural issues, route back to facilitation when no meaningful ideas/themes exist, and cap retry loops at 2.
- KG write failures during extraction/finalization must surface through FastAPI.

### Flagged Issues

#### Decision Needed

All decision-needed issues are resolved:

- D1: Use an explicit review/confirmation approval pause before KG writes.
- D2: Use aggregate transactional brainstorm-output finalization for confirmed output.
- D3: Do not edit PRD or architecture; fix implementation/tests against the accepted read-only interpretation.
- D4: Remove silent fallback success behavior for required PydanticAI phases; surface errors after retries and use fake runners in tests.

#### Risks

- Checkpoint compatibility risk: phase/routing changes can break active-session resume behavior. Mitigation: add migration-tolerant routing and tests for active `facilitate`, review, and concluded checkpoints.
- Persistence risk: switching finalization to aggregate endpoint may reveal schema mismatches in theme/source IDs or context chunks. Mitigation: normalize final payload in one place and test KG request construction.
- UX risk: review controls can become chat-only and ambiguous. Mitigation: provide explicit visible review/confirm affordances while still supporting text commands.
- LLM/test risk: removing silent fallback may make tests brittle. Mitigation: inject explicit fake runners and test error paths separately.
- Spec interpretation risk: architecture wording can be misread as allowing unconfirmed writes. Mitigation: add tests that enforce PRD review/confirmation gating without editing PRD or architecture.

#### Constraints

- No new architecture, framework, library, frontend framework, or persistence model.
- No reliance on stale `docs/`.
- No direct agent-to-KG or agent-to-`thagid` imports.
- No public exposure of `/internal/kg/*` or agent endpoints.
- No source changes outside the drift areas unless required by tests/spec alignment.

#### Deferred

- Multiple brainstorm sessions per package remains post-MVP and should not be implemented.
- Embedding retry/failure recovery beyond logging remains deferred per PRD/architecture.
- Visual file ingestion beyond supported text file handling remains deferred.
- Neo4j migration/context-aware re-embedding remains future work.

#### Out Of Scope

- Stale `docs/` cleanup.
- General UI redesign not needed for review/finalization adherence.
- Unrelated package/project/auth refactors.
- GitHub Projects webhook workflow changes.

### User Decisions

- D1=A accepted: implement review/confirmation pause before KG writes.
- D2=A accepted: use aggregate transactional finalization endpoint.
- D3 revised by user: PRD and architecture must not be changed by the runner; implementation/tests must be fixed to conform to the PRD-required review/confirmation gate.
- D4=A accepted: remove silent fallback success behavior for required PydanticAI phases.

## Task Index

### Planning Status

Planning is complete. Execution has not started.

### Execution Principles

- Execute tasks in order. The specification alignment task intentionally precedes source changes so future implementation has no ambiguous contract.
- Do not skip tests. Each task contains task-local validation and Task 08 is the final drift audit.
- Keep changes scoped to approved drift areas and accepted decisions D1-D4.
- Preserve separate agent/backend/frontend boundaries and project-context rules throughout.
- If implementation discovers a new conflict with project context, stop and ask rather than simplifying.

### Tasks

- `tasks/task-01-align-binding-specs.md` - Lock Specification Interpretation
- `tasks/task-02-harden-agent-contracts.md` - Harden Agent Contracts And PydanticAI Execution
- `tasks/task-03-refactor-graph-lifecycle.md` - Refactor LangGraph Lifecycle, Checkpointing, And Summary
- `tasks/task-04-atomic-kg-finalization.md` - Implement Atomic Confirmed KG Finalization
- `tasks/task-05-backend-contract-error-bridge.md` - Align Backend Brainstorm Contract And Error Bridge
- `tasks/task-06-frontend-review-confirmation.md` - Implement Frontend Review And Confirmation Flow
- `tasks/task-07-regression-test-suite.md` - Build Specification Regression Test Suite
- `tasks/task-08-final-validation-and-drift-audit.md` - Final Validation And Drift Audit

### Cross-Cutting Validation

- Agent/backend: `pytest` and targeted `pytest agent/tests/test_brainstorm.py agent/tests/test_brainstorm_graph.py agent/tests/test_brainstorm_nodes.py agent/tests/test_architecture_boundaries.py thagid/tests/test_brainstorm.py thagid/tests/test_kg.py`.
- Frontend: `cd web && npm run check`, `cd web && npm run test:unit`, and `cd web && npm run test:e2e` where environment supports it.
- Static audits: no `thagid` imports under `agent/`; no forbidden LangChain application APIs; no browser calls to `/internal/kg` or `/internal/agent`; no KG writes before confirmation; no swallowed finalization failures.
- Spec audit: implementation conforms to PRD/architecture/project context on review/confirmation gating, transactional finalization, and error propagation; PRD and architecture have no diff.

### Rollback / Safety Notes

- Perform read-only spec interpretation audit first and source changes second.
- Preserve existing route prefixes and internal service names to avoid deployment/config churn.
- Keep aggregate finalization changes isolated so granular KG routes can remain available for lower-level tests and operations.
- If checkpoint compatibility breaks, prefer conservative routing for old active phases and add tests rather than deleting old checkpoints.

### Non-Goals And Deferred Work

- Do not clean stale `docs/`.
- Do not add multiple brainstorm sessions per package.
- Do not implement embedding retry recovery, visual file ingestion, Neo4j migration, or context-aware re-embedding.
- Do not redesign unrelated package/project/auth flows.

### Remaining Blockers

None.

## Summary

Planning status: complete.

Execution status: complete.

## Blockers

None.

## Execution

### Execution Status

Complete.

- Status: Complete.
- Checklist: `execution/checklist.md`
- Validation: `execution/validation.md`
- Files changed: `execution/files-changed.md`
- Commits: `execution/commits.md`
