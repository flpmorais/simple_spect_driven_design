# Story 3.4: Async Embeddings for Brainstorm Ideas

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a package user,
I want brainstorm ideas embedded after they are saved,
so that semantic retrieval can work later without slowing down finalization.

## Acceptance Criteria

1. Given an idea node is written to the knowledge graph, when the write succeeds, then the API response returns without waiting for embedding computation, and a background task computes the embedding asynchronously.
2. Given an embedding is computed, when it is stored, then it uses a `vector(1536)` pgvector column in a relational table linked to the graph node id, and the embedding index uses HNSW cosine search configuration.
3. Given embedding computation fails, when the background task handles the failure, then the graph node remains available for graph traversal, and the failure is logged without rolling back the node write.

## Tasks / Subtasks

- [x] Add relational idea embedding storage (AC: 2)
  - [x] Add `thagid/models/embeddings.py` with an `IdeaEmbedding` SQLAlchemy model mapped to `idea_embeddings`.
  - [x] Use `node_id` as the primary key linked to the KG Idea node id returned from `KnowledgeGraphService.persist_brainstorm_output`.
  - [x] Add `project_id` for project-scoped retrieval and indexing, because later Epic 4 vector search must not cross project boundaries.
  - [x] Add `embedding` as `Vector(1536)` from `pgvector.sqlalchemy`.
  - [x] Add lightweight metadata useful for operation and tests: `model` defaulting to `text-embedding-3-small` and `created_at`/`updated_at` timestamps.
  - [x] Import the model from `thagid/models/__init__.py` and `migrations/env.py` so Alembic metadata includes it.
  - [x] Do not add `chunk_embeddings` in this story; Story 3.4 covers brainstorm idea embeddings only.
- [x] Add migration for pgvector idea embeddings (AC: 2)
  - [x] Add migration `008_add_idea_embeddings_table.py` with down revision `007`.
  - [x] Ensure `CREATE EXTENSION IF NOT EXISTS vector` is present or harmlessly repeated before creating the table.
  - [x] Create `idea_embeddings` with `node_id`, `project_id`, `embedding vector(1536)`, `model`, `created_at`, and `updated_at`.
  - [x] Create a project scoping index such as `ix_idea_embeddings_project_id`.
  - [x] Create an HNSW cosine index on `embedding`, named `ix_idea_embeddings_embedding_hnsw`, using `vector_cosine_ops`.
  - [x] Keep migration downgrade complete: drop HNSW index, project index, then table. Do not drop the `vector` extension.
- [x] Add embedding configuration without introducing new libraries (AC: 1, 3)
  - [x] Add `OPENAI_API_KEY` to `thagid/config.py` and `.env.template`.
  - [x] Use the existing `httpx` dependency to call `POST https://api.openai.com/v1/embeddings`; do not add the `openai` package unless the user explicitly approves a new dependency.
  - [x] Use model `text-embedding-3-small` and store 1536 dimensions, matching the architecture decision and pgvector column size.
  - [x] Treat missing `OPENAI_API_KEY`, non-2xx OpenAI responses, malformed responses, and wrong vector dimensions as embedding failures that are logged and do not affect KG persistence.
- [x] Implement embedding computation and storage service (AC: 1, 2, 3)
  - [x] Add `thagid/services/embedding.py` with focused embedding behavior; keep KG graph writes in `KnowledgeGraphService`.
  - [x] Build deterministic idea text from the persisted idea fields, for example title, concept, category, and novelty. Do not embed theme or session text in this story.
  - [x] Call OpenAI with `encoding_format: "float"` and validate the returned vector length is exactly 1536.
  - [x] Upsert the embedding row by `node_id` so repeated confirmed KG persistence or retrying a background task does not create duplicates.
  - [x] Keep the background task isolated: open a fresh DB session inside the task, then instantiate services with that session. Do not pass the request-scoped `AsyncSession` into `BackgroundTasks`, because it will be closed after the response.
  - [x] Catch and log exceptions inside the background task; never re-raise errors that could make the original KG write appear failed.
- [x] Queue embeddings only after successful KG persistence (AC: 1, 3)
  - [x] Update `thagid/routers/kg.py` to accept FastAPI `BackgroundTasks` on `POST /internal/kg/projects/{project_id}/brainstorm-output`.
  - [x] Call `KnowledgeGraphService.persist_brainstorm_output` exactly as Story 3.2 does, preserving existing transaction/rollback behavior for graph writes.
  - [x] After the service returns `KGWriteResponse`, queue one background task for all idea embeddings or one task per idea; either is acceptable if the HTTP response is not blocked by embedding calls.
  - [x] Pass only serializable data to the background task: `project_id`, created `idea_node_ids`, and the source idea payload fields needed to build embedding text.
  - [x] Preserve the existing `KGWriteResponse` shape if possible. If adding embedding queue metadata, make it additive and update agent tests so `state["kg_node_ids"]` remains compatible.
  - [x] Do not queue embeddings if `persist_brainstorm_output` raises; failed KG writes must not produce orphan embedding rows.
- [x] Preserve Epic 3 behavior and boundaries (AC: 1, 2, 3)
  - [x] Preserve Story 3.2 idempotency: repeated confirmed KG persistence should still return stable KG node ids and must not duplicate embedding rows.
  - [x] Preserve Story 3.1 theme review and adjustment behavior; no frontend changes are expected for this story.
  - [x] Preserve browser-facing brainstorm response fields and agent container boundaries. The agent still calls `/internal/kg/...` over HTTP and never imports backend modules.
  - [x] Do not implement vector similarity search, brainstorm result retrieval, dashboard summary cards, detail pages, BMAD markdown rendering, chunk embeddings, retry queues, or embedding failure recovery UI.
  - [x] Story 3.3 is currently `ready-for-dev` in sprint status, not `done`; do not assume validation/versioning code exists unless the codebase contains it when implementing this story.
- [x] Add focused tests and verification (AC: 1, 2, 3)
  - [x] Add model/migration-oriented tests or assertions that `idea_embeddings.embedding` uses `Vector(1536)` and the migration defines an HNSW `vector_cosine_ops` index.
  - [x] Add embedding service tests using mocked `httpx.AsyncClient` or a mocked helper to cover success, missing API key, non-2xx response, malformed response, wrong dimensions, and database upsert behavior.
  - [x] Add KG router tests that patch the embedding queue helper and assert it is called only after successful KG persistence, with created idea node ids and source ideas.
  - [x] Add regression tests proving KG failures do not queue embeddings and still return existing error behavior.
  - [x] Add idempotency tests proving repeated persistence/upsert does not create duplicate embedding rows.
  - [x] Run `rtk pytest thagid/tests/test_kg.py -q`.
  - [x] Run `rtk pytest thagid/tests/test_brainstorm.py thagid/tests/test_agent_client.py -q` to catch brainstorm contract regressions.

### Review Findings

- [x] [Review][Patch] Embedding job construction can fail after KG commit [thagid/routers/kg.py:45; thagid/services/embedding.py:75]
- [x] [Review][Patch] Concurrent embedding upserts are not atomic [thagid/services/embedding.py:53]
- [x] [Review][Patch] Embedding response validation accepts non-numeric or non-finite vector values [thagid/services/embedding.py:49]

## Dev Notes

### Scope Boundaries

- This story adds asynchronous embedding computation for persisted brainstorm Idea nodes only.
- This story is backend-only unless tests expose a browser or agent contract regression.
- The KG write must remain the source of truth. If embedding fails, the Idea node remains usable through graph traversal.
- Do not introduce a worker queue, Celery, Redis, or retry strategy in this story. The architecture explicitly defers embedding failure handling.
- Do not add a new dependency for the OpenAI Python SDK. `httpx` already exists and is sufficient for the single embeddings API call.

### Current Codebase State

- `thagid/services/knowledge_graph.py` currently writes Session, Theme, Idea, and ContextChunk AGE nodes in one transaction and returns `KGWriteResponse` with `idea_node_ids`.
- `thagid/routers/kg.py` currently exposes `POST /internal/kg/projects/{project_id}/brainstorm-output`, protected by `X-Agent-Key`, and calls `KnowledgeGraphService.persist_brainstorm_output`.
- `thagid/schemas/kg.py` currently defines `KGWriteRequest`, `KGThemeWrite`, `KGIdeaWrite`, `KGContextChunkWrite`, and `KGWriteResponse`.
- `agent/main.py` stores `kg_response.json()` in checkpoint state as `kg_node_ids` after successful theme confirmation. Be careful if changing the KG response shape.
- `pyproject.toml` already includes `pgvector>=0.4.2` and `httpx>=0.28`.
- `postgres/Containerfile` installs pgvector `v0.8.2`; pgvector docs support HNSW indexes and `vector_cosine_ops` for cosine distance.
- `.env.template` and `thagid/config.py` do not currently define `OPENAI_API_KEY`.
- Default backend tests use SQLite; SQLite cannot execute pgvector-specific DDL. Tests should validate SQL/model/migration shape with mocks or focused assertions rather than requiring live PostgreSQL in the default suite.

### Required Implementation Behavior

- Queue embeddings only after graph writes commit successfully and `KGWriteResponse` has been produced.
- The HTTP response from `/internal/kg/projects/{project_id}/brainstorm-output` must not wait for OpenAI embedding calls.
- Background task payload must include enough idea data to embed each idea without re-querying AGE: at minimum `category`, `title`, `concept`, `novelty`, and the corresponding `idea_node_id`.
- Preserve `idea_node_ids` ordering from `KnowledgeGraphService.persist_brainstorm_output`: it currently flattens ideas in theme order. Pair each node id with the same flattened source idea.
- Store one embedding row per Idea node id. Re-running the same task should update the existing row, not insert a duplicate.
- Do not store embeddings in AGE node properties. Embeddings belong in relational pgvector tables.
- Do not roll back or mark KG persistence failed because an embedding task fails.
- Log failures with enough context to diagnose the node id and project id, but do not log API keys or full sensitive payloads.

### Architecture Guardrails

- Follow Router -> Service -> Model. Routers handle HTTP/auth/status mapping and background task queuing; services own embedding API calls and database writes.
- Services receive `AsyncSession` during normal request handling. For FastAPI background tasks, open a fresh session inside the task and then pass that session to the service; never reuse the request-scoped `db` after the response.
- Keep internal KG endpoints under `/internal/kg/...` and authenticated by `X-Agent-Key`.
- Keep browser-facing endpoints under `/api/packages/{package_id}/brainstorm/...`; no browser-facing embedding endpoint is needed.
- Keep agent/backend container boundaries intact. The agent does not compute embeddings and does not call OpenAI for embeddings in this story.
- Use project scoping on `idea_embeddings` so Epic 4 vector search can filter by `project_id` and avoid cross-project leakage.

### Latest Technical Notes

- OpenAI docs state `text-embedding-3-small` returns 1536 dimensions by default and accepts `encoding_format: "float"` for embeddings output.
- OpenAI docs recommend cosine similarity; pgvector supports cosine distance with the `<=>` operator and HNSW indexes using `vector_cosine_ops`.
- pgvector `v0.8.2` supports HNSW indexes; HNSW can be created before data exists and trades build/memory cost for faster approximate nearest-neighbor search.
- FastAPI `BackgroundTasks` run after the response is sent and are appropriate for small background work. FastAPI docs warn that heavier distributed processing should use a larger queue system, which is intentionally out of scope for this MVP story.

### Previous Story Intelligence

- Story 3.2 is done and implemented stable KG node ids, atomic graph writes, internal KG routing, and agent persistence over HTTP.
- Story 3.2 deliberately deferred embeddings and stated embeddings must not be placed in AGE node properties.
- Story 3.2 tests established `FakeSession` patterns in `thagid/tests/test_kg.py` for AGE SQL behavior because the default test suite cannot execute AGE/pgvector SQL.
- Story 3.1 established confirmed theme grouping; embeddings must not happen before groupings are confirmed and KG persistence succeeds.
- Story 2.3 established idea fields `category`, `title`, `concept`, and `novelty`; use those fields to create deterministic embedding text.
- Recent git history: `feat: add knowledge graph persistence`, `feat: add theme grouping review`, `feat: add URL context ingestion`, `feat: add text file context ingestion`, and `feat: add brainstorm idea management and summaries`.

### File Structure Requirements

- Likely new backend files: `thagid/models/embeddings.py`, `thagid/services/embedding.py`, and `migrations/versions/008_add_idea_embeddings_table.py`.
- Likely backend updates: `thagid/config.py`, `.env.template`, `thagid/models/__init__.py`, `migrations/env.py`, `thagid/routers/kg.py`, `thagid/services/knowledge_graph.py` only if a helper for flattened source ideas is needed, and `thagid/tests/test_kg.py`.
- Possible schema updates: `thagid/schemas/kg.py` only if adding an internal helper schema or additive response metadata; avoid changing existing required response fields.
- Avoid frontend files and `agent/` files unless existing KG response compatibility tests require an additive adjustment.

### Testing Requirements

- Use mocks/fakes for OpenAI and pgvector-specific SQL in the default test suite.
- Test the non-blocking contract by asserting the router queues background work after KG success rather than awaiting embedding computation inline.
- Test failure containment: OpenAI/config/vector/database errors inside the background task are logged and do not alter the KG response path.
- Test upsert/idempotency: duplicate `node_id` writes update one row.
- Test project scoping fields exist because Epic 4 vector search depends on project isolation.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story-3.4-Async-Embeddings-for-Brainstorm-Ideas]
- [Source: _bmad-output/planning-artifacts/prd.md#Brainstorm-Output]
- [Source: _bmad-output/planning-artifacts/prd.md#Performance]
- [Source: _bmad-output/planning-artifacts/architecture.md#Embedding-Pipeline]
- [Source: _bmad-output/planning-artifacts/architecture.md#Data-Architecture]
- [Source: _bmad-output/planning-artifacts/architecture.md#Embedding-Column-Convention]
- [Source: _bmad-output/planning-artifacts/architecture.md#Embedding-Failure-Pattern]
- [Source: _bmad-output/implementation-artifacts/3-2-knowledge-graph-domain-api-and-atomic-writes.md#Completion-Notes-List]
- [Source: _bmad-output/implementation-artifacts/3-3-extraction-validation-and-node-versioning.md#Scope-Boundaries]
- [Source: thagid/services/knowledge_graph.py]
- [Source: thagid/routers/kg.py]
- [Source: thagid/schemas/kg.py]
- [Source: thagid/tests/test_kg.py]
- [Source: postgres/Containerfile]
- [Source: https://platform.openai.com/docs/guides/embeddings]
- [Source: https://github.com/pgvector/pgvector#hnsw]
- [Source: https://fastapi.tiangolo.com/tutorial/background-tasks/]
- [Source: _bmad-output-old/main/project-context.md#Critical-Implementation-Rules]

## Project Structure Notes

- The architecture names both `idea_embeddings` and `chunk_embeddings`, but this story covers Idea embeddings only. Chunk embeddings should remain future work unless the user expands the scope.
- The architecture target describes a future broader vector search API, but Epic 4 owns retrieval/search. This story should stop at writing embeddings and the index needed for later search.
- The current prototype keeps KG persistence in a single `brainstorm-output` endpoint. Queue embeddings from that endpoint after successful KG persistence rather than introducing the full architecture's separate per-idea write endpoints.
- `BackgroundTasks` is acceptable for this MVP because failure retry strategy is deferred; do not overbuild with a queue service.

## Dev Agent Record

### Agent Model Used

openai/gpt-5.5

### Debug Log References

- `rtk pytest thagid/tests/test_kg.py -q` - 22 passed
- `rtk pytest thagid/tests/test_brainstorm.py thagid/tests/test_agent_client.py -q` - 49 passed
- `rtk pytest -q` - 239 passed

### Completion Notes List

- Ultimate context engine analysis completed - comprehensive developer guide created.
- Added relational `IdeaEmbedding` storage with `Vector(1536)`, project scoping, metadata timestamps, and Alembic metadata imports.
- Added migration `008_add_idea_embeddings_table.py` with pgvector extension creation, project index, HNSW cosine index, and complete downgrade.
- Added `EmbeddingService` using existing `httpx` to call OpenAI embeddings, validate 1536 dimensions, upsert by `node_id`, and isolate/log background failures.
- Updated internal KG persistence route to queue serializable brainstorm idea embedding jobs only after successful KG persistence while preserving `KGWriteResponse` shape.
- Added focused tests for model/migration shape, embedding success/failure modes, idempotent upsert, background failure containment, and KG queue/no-queue behavior.

### File List

- `.env.template`
- `_bmad-output/implementation-artifacts/3-4-async-embeddings-for-brainstorm-ideas.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `migrations/env.py`
- `migrations/versions/008_add_idea_embeddings_table.py`
- `thagid/config.py`
- `thagid/models/__init__.py`
- `thagid/models/embeddings.py`
- `thagid/routers/kg.py`
- `thagid/services/embedding.py`
- `thagid/tests/test_kg.py`

### Change Log

- 2026-05-11: Implemented async brainstorm idea embeddings and moved story to review.
