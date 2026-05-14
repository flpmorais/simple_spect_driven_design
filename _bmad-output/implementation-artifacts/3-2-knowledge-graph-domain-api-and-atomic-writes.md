# Story 3.2: Knowledge Graph Domain API and Atomic Writes

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a package user,
I want confirmed brainstorm results stored as structured knowledge,
so that future agents and views can retrieve specific ideas and themes.

## Acceptance Criteria

1. Given I confirm the final theme grouping, when extraction writes brainstorm data, then the backend creates Session, Theme, Idea, and ContextChunk graph nodes as needed, and relationships use HAS_THEME, CONTAINS_IDEA, and USES_CONTEXT edge types.
2. Given graph data is written for a project, when the KG service resolves the graph namespace, then it uses the `project_{normalized_project_id}` graph naming pattern, and enforces organization and project scoping through the backend service layer.
3. Given the agent needs KG operations, when it persists brainstorm output, then it calls the FastAPI internal KG endpoints over HTTP with `X-Agent-Key`, and it never imports or directly calls backend service classes.

## Tasks / Subtasks

- [x] Define internal KG schemas and response contracts (AC: 1, 2, 3)
  - [x] Add `thagid/schemas/kg.py` with Pydantic schemas for Session, Theme, Idea, ContextChunk write payloads and write responses.
  - [x] Keep KG schemas internal/backend-facing; do not reuse browser-facing response models if that would expose implementation-only fields.
  - [x] Represent graph node IDs as UUID strings in stored node properties. Do not store existing UI/checkpoint theme IDs like `theme-general` as KG node UUIDs.
  - [x] Include source/reference fields needed for idempotency and traceability, such as brainstorm `session_id`, checkpoint theme id/title/position, idea title/concept, and context document `source_type`/`source_ref`.
  - [x] Validate that themes contain ideas and context chunks have supported `source_type` values from existing `active_documents` (`file`, `url`).
- [x] Implement `KnowledgeGraphService` for AGE graph writes (AC: 1, 2)
  - [x] Add `thagid/services/knowledge_graph.py` following existing Router -> Service -> Model layering.
  - [x] Add graph namespace helper that accepts a project UUID and returns `project_{uuid_with_hyphens_replaced_by_underscores}`.
  - [x] Validate graph names with an allowlist before using them in AGE calls; never build graph names from arbitrary strings.
  - [x] Ensure AGE setup runs on the active DB session/connection before AGE operations: `LOAD 'age'` and `SET search_path = ag_catalog, "$user", public`.
  - [x] Create the project graph if it does not already exist, and make graph creation visible to subsequent writes in the same request.
  - [x] Write Session, Theme, Idea, and ContextChunk nodes with labels exactly `Session`, `Theme`, `Idea`, and `ContextChunk`.
  - [x] Write relationships exactly `HAS_THEME` from Session to Theme, `CONTAINS_IDEA` from Theme to Idea, and `USES_CONTEXT` from Session to ContextChunk.
  - [x] Use parameterized AGE Cypher calls through `cypher(:graph, $$ ... $$, :params::agtype)` or an equivalent parameterized pattern. Do not interpolate values into Cypher strings.
  - [x] Keep writes in one backend transaction for one brainstorm-output persist operation where practical; on failure, do not leave partially persisted theme/idea/context output for that call.
  - [x] Return created node IDs to the caller so the agent can store handoff metadata in checkpoint state.
- [x] Add internal KG router endpoints protected by `X-Agent-Key` (AC: 2, 3)
  - [x] Add `thagid/routers/kg.py` with prefix `/internal/kg` and reuse the existing `verify_agent_key` pattern from `thagid/routers/internal.py`.
  - [x] Register the router in `thagid/main.py`.
  - [x] Add a domain-specific persist endpoint for confirmed brainstorm output under `/internal/kg/projects/{project_id}/...`, or implement the architecture-listed write endpoints only if the agent can persist the output without partial-write ambiguity.
  - [x] Verify project existence and package/project consistency through backend service-layer checks before writing graph data.
  - [x] Enforce organization/project graph scoping in backend code; the agent must only provide `project_id`/`package_id`, not a raw graph name.
  - [x] Return 401 for missing/invalid `X-Agent-Key`, 404 for missing package/project, 422 for invalid payloads, and standard 500 errors for KG write failures.
- [x] Add agent-side KG client call on confirmed themes (AC: 1, 3)
  - [x] Extend `agent/backend_client.py` with an HTTP function that posts confirmed brainstorm output to the backend internal KG endpoint using the existing `_client()` and `X-Agent-Key` header.
  - [x] Update `agent/main.py` confirmation handling in Extract phase: when themes are confirmed and not already persisted, call the backend KG endpoint over HTTP.
  - [x] Send the current checkpoint data needed for persistence: `session_id`, `package_id`, `project_id`, `technique`, `themes`, `ideas`, `active_documents`, summary if available, and finalization metadata.
  - [x] After a successful KG write, store returned node IDs and a durable flag such as `kg_write_completed: True` in checkpoint state.
  - [x] Repeated confirmation after a successful KG write must not create duplicate nodes; it should return an acknowledgement using stored checkpoint metadata.
  - [x] If the KG write fails, keep `themes_confirmed` false or unset `kg_write_completed`, keep phase recoverable, and return a standard retryable brainstorm error rather than pretending persistence succeeded.
  - [x] Do not import `thagid.*` modules into `agent/`; preserve the container boundary.
- [x] Preserve existing brainstorm behavior and story boundaries (AC: 1, 2, 3)
  - [x] Preserve Story 3.1 theme review behavior: deterministic theme grouping, text-based theme adjustment, `aria-expanded` theme cards, and no KG write before confirmation.
  - [x] Preserve `active_documents` from Story 2.5/2.6 and write them as ContextChunk nodes only after confirmation.
  - [x] Preserve existing browser-facing brainstorm response fields: `message`, `session_id`, `phase`, `technique`, `idea_count`, `message_count`, `ideas`, and `themes`.
  - [x] Do not add embeddings, pgvector tables, HNSW indexes, vector search, validation retry routing, BMAD markdown rendering, dashboard summary cards, or brainstorm detail retrieval in this story.
  - [x] Do not migrate the prototype to the future `agent/brainstorm/nodes/` LangGraph folder layout in this story.
- [x] Add focused tests and verification (AC: 1, 2, 3)
  - [x] Add service tests for graph name normalization, invalid graph name rejection, AGE setup execution, parameterized Cypher usage, node labels, edge labels, and transaction rollback behavior using a fake or mocked async DB session where SQLite cannot execute AGE.
  - [x] Add router tests in `thagid/tests/test_internal.py` or `thagid/tests/test_kg.py` for `X-Agent-Key`, package/project validation, success payload, and error responses.
  - [x] Add agent tests in `agent/tests/test_brainstorm.py` for confirmation calling the backend KG endpoint, storing returned node IDs, avoiding duplicate writes on repeated confirmation, and surfacing retryable errors on KG failure.
  - [x] Add a regression test that non-confirmation Extract messages still adjust or reject theme changes without KG calls.
  - [x] Run `rtk pytest thagid/tests/test_kg.py thagid/tests/test_internal.py -q` if `test_kg.py` is added.
  - [x] Run `rtk pytest agent/tests/test_brainstorm.py -q`.
  - [x] Run `rtk pytest thagid/tests/test_brainstorm.py thagid/tests/test_agent_client.py -q`.

### Review Findings

- [x] [Review][Patch] Backend KG idempotency across post-commit retry/save-failure boundaries [`thagid/services/knowledge_graph.py:26`]
- [x] [Review][Patch] AGE relationship writes fail because SQLAlchemy parses edge labels as bind params [`thagid/services/knowledge_graph.py:64`]
- [x] [Review][Patch] Revised themes after a successful KG write are skipped because adjustment does not clear KG persistence flags [`agent/main.py:782`]
- [x] [Review][Patch] Session nodes omit the specified `created_at` property [`thagid/services/knowledge_graph.py:72`]
- [x] [Review][Patch] Duplicate KG theme `source_id` values collapse response metadata [`thagid/schemas/kg.py:31`]

## Dev Notes

### Scope Boundaries

- This story starts persistence of confirmed brainstorm output into the knowledge graph.
- This story is backend/agent-only unless tests reveal a browser response regression. No planned frontend UI changes.
- Do not implement Story 3.3 validation/versioning, Story 3.4 embeddings/vector tables, Story 3.5 markdown rendering, or Epic 4 retrieval/dashboard UI.
- Do not add new libraries. Required KG-related dependencies already exist in `pyproject.toml`: `langgraph`, `langgraph-checkpoint-postgres`, and `pgvector`.
- Keep the current prototype structure. The architecture target has a future `agent/brainstorm/nodes/` layout, but current behavior is centralized in `agent/main.py`; avoid a migration unless explicitly requested.

### Current Codebase State

- `agent/main.py` owns `/internal/agent/brainstorm/message` and `/internal/agent/brainstorm/status`, validates `X-Agent-Key`, manages phase transitions, and stores checkpoint state.
- Story 3.1 confirmation currently sets `themes_confirmed = True` in Extract phase and replies that the next pipeline step can proceed later; it does not write KG data yet.
- `agent/backend_client.py` already provides a backend HTTP client with `BACKEND_SERVICE_URL`, `X-Agent-Key`, and a package context call. Extend this instead of creating another client pattern.
- `thagid/routers/internal.py` has the current internal backend prefix `/internal/backend` and a `verify_agent_key` dependency. Reuse the auth pattern for `/internal/kg`.
- `thagid/main.py` currently registers `brainstorm` and `internal` routers. New KG router registration belongs there.
- `thagid/services/brainstorm.py` proxies browser-facing brainstorm messages to the agent and writes normal chat messages to the existing `messages` table. KG writes should remain behind internal KG endpoints, not browser-facing brainstorm endpoints.
- `thagid/schemas/brainstorm.py` has browser-facing `BrainstormIdea` and `BrainstormTheme` shapes. These are useful references, but KG schemas should be explicit about stored node data.
- Current backend tests use SQLite via `thagid/tests/conftest.py`; SQLite cannot execute AGE or pgvector-specific SQL. Unit-test SQL construction with mocks/fakes or isolate real PostgreSQL integration tests from the default test suite.
- There is no existing `KnowledgeGraphService`, `thagid/routers/kg.py`, `thagid/schemas/kg.py`, or embedding model/table.

### Required Implementation Behavior

- KG writes start only after final theme grouping confirmation in Extract phase.
- The agent must call FastAPI over HTTP for KG operations. Never import backend service classes into `agent/`.
- Browser traffic never calls `/internal/kg/...` directly; internal KG endpoints are authenticated only by `X-Agent-Key`.
- The backend must resolve and validate graph namespace from `project_id`; the agent must not send graph names.
- Session, Theme, Idea, and ContextChunk nodes must be separate atomic graph nodes, not one serialized JSON blob on a Session node.
- Relationships must be typed exactly as documented: `HAS_THEME`, `CONTAINS_IDEA`, `USES_CONTEXT`.
- Store node properties in snake_case and preserve source traceability from checkpoint data.
- Use UUID string node IDs in KG properties. If the checkpoint has non-UUID theme ids, map them to backend-generated UUID node IDs and keep the source id separately.
- Treat repeated confirmation as idempotent after a successful checkpoint save. Do not create duplicate nodes when `kg_write_completed` and returned node IDs are already present.
- If a KG write fails, the session must remain recoverable in Extract phase with existing themes intact.

### Architecture Guardrails

- Follow Router -> Service -> Model. Routers handle HTTP/auth/status mapping; `KnowledgeGraphService` owns AGE graph operations.
- Services receive `AsyncSession`; do not create their own SQLAlchemy sessions.
- Parameterize AGE Cypher values. Never use f-strings, `.format()`, or string concatenation to insert user/project/session/theme/idea/context values into Cypher.
- AGE graph names are not user input. Normalize from UUID project id only and validate with an allowlist before use.
- AGE requires `LOAD 'age'` and `SET search_path = ag_catalog, "$user", public` per DB session/connection before Cypher calls.
- Apache AGE DDL-like graph creation is transactional; make sure graph creation and subsequent writes are visible in the intended transaction/session.
- Use the existing PostgreSQL 16 + AGE + pgvector container. Do not add Neo4j or another graph database.
- Do not put embeddings in AGE node properties. Embeddings are Story 3.4 and belong in relational pgvector tables later.

### Data Shape Guidance

- Session node properties should include at minimum: `id`, `package_id`, `project_id`, `status`, `technique`, `created_at`, and `concluded_at` or persisted timestamp.
- Theme node properties should include at minimum: `id`, `source_id`, `title`, `summary`, and `position`.
- Idea node properties should include at minimum: `id`, `category`, `title`, `concept`, and `novelty`.
- ContextChunk node properties should include at minimum: `id`, `source_type`, `source_ref`, `content`, `summary` if available, and `content_hash` if available.
- The persisted graph should allow Epic 4 retrieval by traversing Session -> Theme -> Idea and Session -> ContextChunk.

### Previous Story Intelligence

- Story 3.1 added `BrainstormTheme`, deterministic grouping by idea category, Extract-phase theme adjustment, confirmation handoff, `ThemeCard.svelte`, and tests. Preserve those contracts.
- Story 3.1 deliberately avoided KG writes. This story removes that boundary only for confirmed groupings.
- Story 2.6 added URL context ingestion with `active_documents` entries using `source_type = "url"`, canonical `source_ref`, `content`, `summary`, and `content_hash`. Persist these as ContextChunk nodes after confirmation.
- Story 2.5 added file context ingestion with `active_documents` entries using `source_type = "file"`, filename `source_ref`, `content`, and `summary`. Persist these as ContextChunk nodes after confirmation.
- Story 2.4 added rolling summary fields and checkpoint compaction. Preserve summary state and message counters during KG write attempts.
- Story 2.3 established deterministic structured ideas with fields `category`, `title`, `concept`, and `novelty`; ideas do not currently have stable UUID ids.
- Recent git history shows the established pattern: keep prototype logic in `agent/main.py`, add focused tests, and preserve browser-facing response compatibility.

### Latest Technical Notes

- Apache AGE currently supports PostgreSQL 16, and this repo builds AGE from the `PG16/v1.6.0-rc0` branch in `postgres/Containerfile`.
- AGE must be loaded per connection with `LOAD 'age'` and search path set to `ag_catalog, "$user", public` before Cypher calls.
- AGE graph/label creation is transactional for non-autocommit clients; commit or keep setup and writes in a transaction where visibility is guaranteed.
- pgvector `0.8.2` is installed in the custom PostgreSQL image, but this story must not add vector columns or HNSW indexes. Story 3.4 owns that work.
- `pgvector-python` supports SQLAlchemy and asyncpg, but no pgvector Python integration is needed for this story.

### File Structure Requirements

- Likely new backend files: `thagid/schemas/kg.py`, `thagid/services/knowledge_graph.py`, `thagid/routers/kg.py`, and `thagid/tests/test_kg.py`.
- Likely backend updates: `thagid/main.py`, and possibly `thagid/tests/test_internal.py` if internal router test helpers are reused.
- Likely agent updates: `agent/backend_client.py`, `agent/main.py`, and `agent/tests/test_brainstorm.py`.
- Possible backend test updates: `thagid/tests/test_agent_client.py` if KG client behavior is added to existing backend agent client code, but the primary KG call is agent -> backend and belongs in `agent/backend_client.py`.
- Avoid migrations and new SQLAlchemy models in this story unless a minimal relational helper table becomes unavoidable; AGE graph persistence should not require a migration for embeddings.
- Avoid frontend changes unless browser-facing brainstorm responses regress.

### Testing Requirements

- Test KG service behavior without relying on SQLite executing AGE SQL.
- Test that Cypher value payloads are passed as parameters and not interpolated into query strings.
- Test graph name normalization with a real UUID and rejection of malformed graph names/helpers.
- Test internal KG endpoint auth with missing, wrong, and correct `X-Agent-Key`.
- Test package/project mismatch rejects writes before KG service calls.
- Test agent confirmation calls backend KG exactly once for a successful confirmed grouping and stores returned KG metadata.
- Test repeated confirmation after `kg_write_completed` avoids another backend call.
- Test KG failure leaves existing themes available for retry and does not mark the brainstorm as persisted.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story-3.2-Knowledge-Graph-Domain-API-and-Atomic-Writes]
- [Source: _bmad-output/planning-artifacts/prd.md#Knowledge-Graph-Storage]
- [Source: _bmad-output/planning-artifacts/prd.md#Technical-Success]
- [Source: _bmad-output/planning-artifacts/architecture.md#Data-Architecture]
- [Source: _bmad-output/planning-artifacts/architecture.md#Knowledge-Graph-API]
- [Source: _bmad-output/planning-artifacts/architecture.md#Agent-Backend-Communication]
- [Source: _bmad-output/planning-artifacts/architecture.md#AGE-Cypher-Query-Pattern]
- [Source: _bmad-output/planning-artifacts/architecture.md#Architectural-Boundaries]
- [Source: _bmad-output/implementation-artifacts/3-1-theme-grouping-review-and-confirmation.md#Completion-Notes-List]
- [Source: agent/main.py]
- [Source: agent/backend_client.py]
- [Source: thagid/routers/internal.py]
- [Source: thagid/services/brainstorm.py]
- [Source: thagid/tests/conftest.py]
- [Source: postgres/Containerfile]
- [Source: https://github.com/apache/age#post-installation]
- [Source: https://github.com/pgvector/pgvector#hnsw]

## Project Structure Notes

- The architecture target describes a fuller future agent package layout and multiple KG endpoint methods. The current codebase is still a prototype with centralized agent flow, so this story should implement the smallest correct KG persistence path while keeping API names and service boundaries aligned with the architecture.
- The default backend test database is SQLite, so any AGE-specific test that executes real SQL must either be mocked/faked or deliberately separated from default `rtk pytest` execution.
- This story should leave the system working end-to-end through confirmation: confirmed themes persist to KG, chat remains usable, and later stories can continue validation, embeddings, and markdown rendering.

## Dev Agent Record

### Agent Model Used

openai/gpt-5.5

### Debug Log References

- 2026-05-11: Started implementation for story 3.2; set sprint status to in-progress.
- 2026-05-11: Added internal KG schemas, AGE-backed service, `/internal/kg` router, and focused backend tests.
- 2026-05-11: Added agent KG HTTP client integration, confirmation idempotency, retryable KG failure handling, and full pytest verification.

### Completion Notes List

- Ultimate context engine analysis completed - comprehensive developer guide created.
- Implemented internal KG payload/response contracts, graph namespace normalization, AGE setup, parameterized node/edge writes, transaction rollback, and internal KG endpoint validation.
- Implemented agent-side confirmed-theme persistence over HTTP with checkpointed `kg_write_completed` and returned KG node metadata.
- Verified no KG write occurs before theme confirmation and existing theme adjustment/browser-facing brainstorm behavior remains covered by regression tests.

### Change Log

- 2026-05-11: Implemented KG domain API, AGE write service, internal router, agent confirmation persistence, idempotent checkpoint handling, and focused tests.

### File List

- `_bmad-output/implementation-artifacts/3-2-knowledge-graph-domain-api-and-atomic-writes.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `agent/backend_client.py`
- `agent/main.py`
- `agent/tests/test_brainstorm.py`
- `thagid/main.py`
- `thagid/routers/kg.py`
- `thagid/schemas/kg.py`
- `thagid/services/knowledge_graph.py`
- `thagid/tests/test_kg.py`
