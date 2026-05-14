# Story 4.2: Vector Similarity Search for Ideas

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a future agent or authorized client,
I want to retrieve brainstorm ideas by vector similarity,
so that relevant ideas can be reused without scanning whole documents.

## Acceptance Criteria

1. Given idea embeddings exist for a project, when an authorized vector search request is made with an embedding and limit, then the KG API returns the closest matching ideas for that project, and results do not cross project graph boundaries.
2. Given some ideas do not yet have embeddings, when vector search runs, then it skips non-embedded ideas without failing the whole request, and graph traversal retrieval remains available separately.
3. Given a caller requests an invalid limit or malformed embedding, when the endpoint validates input, then it returns the existing validation error format, and no query is executed.

## Tasks / Subtasks

- [x] Add KG vector search request/response schemas (AC: 1, 3)
  - [x] Add schemas in `thagid/schemas/kg.py` for a vector search request containing `embedding` and `limit`.
  - [x] Validate `embedding` as exactly 1536 finite numeric values to match `text-embedding-3-small` and `IdeaEmbedding.embedding` dimensions.
  - [x] Validate `limit` with a small bounded range, recommended `ge=1` and `le=50`, defaulting to 10.
  - [x] Add response item fields that are useful to agents without exposing storage internals unnecessarily: `node_id`, `distance`, `category`, `title`, `concept`, and `novelty`.
  - [x] Do not include the raw query embedding, stored embedding vectors, graph names, Cypher/agtype payloads, or OpenAI metadata in the response.
- [x] Implement `KnowledgeGraphService.search_ideas_by_vector` (AC: 1, 2)
  - [x] Query `IdeaEmbedding` rows filtered by the authorized `project_id`, ordered by cosine distance against the request embedding, limited by the validated limit.
  - [x] Use the existing `idea_embeddings` relational table; do not add migrations, tables, or new libraries.
  - [x] Skip ideas without embeddings naturally by searching only rows present in `idea_embeddings`.
  - [x] Resolve the graph namespace only from the authorized project UUID using `graph_name_for_project` and `validate_graph_name`.
  - [x] Use `_setup_age` and a parameterized AGE query to load Idea node properties for the matched node ids; never interpolate node ids or user-provided values into Cypher.
  - [x] Preserve vector ranking order from pgvector when combining embedding distances with graph Idea properties.
  - [x] If an embedding row points to a missing/stale graph Idea node, skip that row rather than failing the whole search.
  - [x] Return an empty result list when the project has no embedded ideas.
- [x] Add authorized internal KG endpoint (AC: 1, 3)
  - [x] Add `POST /internal/kg/projects/{project_id}/ideas/search` to `thagid/routers/kg.py`.
  - [x] Require `X-Agent-Key` using the same `dependencies=[Depends(verify_agent_key)]` pattern as existing internal KG endpoints.
  - [x] Validate the project exists before creating/calling `KnowledgeGraphService`; return the existing 404 style for missing projects.
  - [x] Let Pydantic/FastAPI produce the existing 422 validation error format for invalid limit or malformed embedding, with no service query executed.
  - [x] Do not add a browser-facing `/api/*` vector search endpoint in this story.
- [x] Preserve existing retrieval and persistence behavior (AC: 1, 2)
  - [x] Do not change `persist_brainstorm_output`, async embedding writes, node versioning, or `get_brainstorm_results` response shapes.
  - [x] Do not make vector search a dependency of graph traversal retrieval; Story 4.1 results must still load when embeddings are missing.
  - [x] Maintain project isolation by filtering relational embeddings by `IdeaEmbedding.project_id` and fetching graph ideas from the same project graph only.
- [x] Add focused tests and verification (AC: 1, 2, 3)
  - [x] Add schema tests for embedding length, non-finite values, and invalid limits in `thagid/tests/test_kg.py`.
  - [x] Add service tests using the existing fake session pattern for project-scoped relational vector ranking, parameterized AGE lookup, order preservation, missing embedding behavior, stale graph-node skipping, and empty result behavior.
  - [x] Add router tests for success, missing `X-Agent-Key`, project not found, malformed embedding, invalid limit, and ensuring the service is not called after validation/auth/project failures.
  - [x] Run `rtk pytest thagid/tests/test_kg.py -q`.
  - [x] Run `rtk pytest thagid/tests/test_brainstorm.py -q` if any shared brainstorm retrieval behavior is touched.

### Review Findings

- [x] [Review][Patch] Invalid-limit router verification missing [`thagid/tests/test_kg.py`] — added endpoint-level validation coverage proving invalid `limit` returns 422 before project lookup or service execution.

## Dev Notes

### Scope Boundaries

- This story adds vector similarity retrieval for stored brainstorm Idea nodes. It is not a UI story and must not build dashboard cards, detail pages, browser API clients, or package routes.
- The architecture lists vector search as KG API functionality. For this story, implement it as an internal KG endpoint under `/internal/kg/...` protected by `X-Agent-Key`, consistent with the agent-facing KG API surface.
- Do not introduce a new embedding model or embedding computation path. Story 3.4 already writes idea embeddings asynchronously using OpenAI `text-embedding-3-small` with 1536 dimensions.
- Do not backfill missing embeddings or fail when embeddings are absent. Vector search should return only rows currently present in `idea_embeddings`; graph traversal retrieval remains the fallback path.

### Current Codebase State

- `thagid/models/embeddings.py` defines `IdeaEmbedding` with `node_id` primary key, `project_id` foreign key/index, `embedding = Vector(1536)`, and `model = "text-embedding-3-small"`.
- `thagid/services/embedding.py` uses `EMBEDDING_MODEL = "text-embedding-3-small"` and `EMBEDDING_DIMENSIONS = 1536`, validates OpenAI embedding responses as finite numeric lists, and upserts `IdeaEmbedding` rows by `node_id`.
- `thagid/services/knowledge_graph.py` already imports `BrainstormIdea` and has `_setup_age`, `_execute_cypher_returning`, `_cypher_values`, `graph_name_for_project`, and `validate_graph_name` helpers that should be reused.
- `KnowledgeGraphService.persist_brainstorm_output` returns stable `idea_node_ids`; `thagid/routers/kg.py` queues background embedding jobs from those node ids after KG persistence succeeds.
- `KnowledgeGraphService.get_brainstorm_results` retrieves Session/Theme/Idea/ContextChunk data by graph traversal and intentionally does not depend on embeddings.
- `thagid/routers/kg.py` currently exposes `POST /internal/kg/projects/{project_id}/brainstorm-output` and `PATCH /internal/kg/projects/{project_id}/nodes/{node_id}`, both protected by `verify_agent_key`.
- `thagid/schemas/kg.py` currently contains write and node update schemas only; vector search schemas belong there to keep internal KG contracts together.
- Existing KG tests in `thagid/tests/test_kg.py` use fake sessions for AGE query assertions and SQLite-backed app tests for router behavior. Follow those patterns instead of requiring a live AGE/PostgreSQL server in the default suite.

### Suggested API Contract

Request:

```json
{
  "embedding": [0.01, -0.02, 0.03],
  "limit": 10
}
```

Implementation requirement: the actual `embedding` must contain exactly 1536 finite numeric values. The abbreviated example above is illustrative only.

Response:

```json
{
  "items": [
    {
      "node_id": "idea-node-uuid",
      "distance": 0.1234,
      "category": "general",
      "title": "Interview Customers",
      "concept": "Run customer interviews before release planning.",
      "novelty": "incremental"
    }
  ],
  "total": 1
}
```

### Implementation Guidance

- Use pgvector/SQLAlchemy cosine distance on `IdeaEmbedding.embedding` because the migration and architecture use HNSW cosine indexing (`vector_cosine_ops`). The pgvector Python documentation supports SQLAlchemy `embedding.cosine_distance([...])` ordering.
- Compute vector nearest-neighbor candidates from the relational table first, because embeddings live outside AGE graph properties. Then fetch the matching Idea node properties from AGE by node id.
- Keep ranking deterministic: maintain the order returned by the vector distance query; do not re-sort alphabetically after fetching graph properties.
- Recommended service flow:
  1. Validate graph name for `project_id`.
  2. Query `IdeaEmbedding` where `project_id == project_id`, ordered by cosine distance, limited by `limit`; collect `(node_id, distance)`.
  3. If no rows, return an empty response without an AGE lookup unless existing helpers make setup unavoidable.
  4. Run a parameterized AGE query for Idea nodes with ids in `node_ids`.
  5. Merge graph properties into vector result order and skip node ids that no longer have an Idea node.
- Ensure all Cypher uses AGE parameters, e.g. `WHERE i.id IN $node_ids`, with `node_ids` supplied through the existing JSON `params` argument.
- Avoid returning graph names, raw node labels, internal Cypher output, or embedding vectors. `node_id` is acceptable here because future agents may need to reference an Idea node for graph operations.

### Architecture Guardrails

- Follow Router -> Service -> Model. Router owns HTTP/auth/status mapping; `KnowledgeGraphService` owns graph/vector retrieval logic.
- Keep all agent-called KG endpoints under `/internal/kg/` and `X-Agent-Key` authenticated.
- Keep browser-facing endpoints under `/api/packages/{package_id}/brainstorm/...`; do not add one for vector search now.
- Use `project_{normalized_uuid}` graph naming through `KnowledgeGraphService.graph_name_for_project` only.
- Parameterize all AGE Cypher queries. No f-strings or `.format()` with user-controlled values in AGE/Cypher statements.
- Preserve container boundaries: the agent calls FastAPI KG endpoints over HTTP and never imports backend services directly.
- Preserve API JSON conventions: snake_case fields, list responses as `{ "items": [...], "total": N }`, errors as `{ "detail": ... }`.

### Previous Story Intelligence

- Story 4.1 added `get_brainstorm_results` and a browser-facing package-scoped results endpoint. Do not change that endpoint or its response shape.
- Story 4.1 review patched theme IDs to expose stable source IDs instead of KG-internal node IDs for browser results. Vector search is different: returning `node_id` is acceptable for agent/KG use, but do not leak graph names or raw AGE payloads.
- Story 4.1 established that raw context chunk content must not be exposed in browser results. This story should not touch context chunks at all.
- Story 3.4 established that embeddings are async and failure leaves graph nodes available without embeddings. This story must skip non-embedded ideas and keep graph traversal retrieval independent.
- Recent commits emphasize minimal, focused changes with tests: `fix brainstorm results review findings`, `feat: add extraction validation and node versioning`, `feat: add async idea embeddings`, and `feat: add knowledge graph persistence`.

### File Structure Requirements

- Likely backend updates: `thagid/schemas/kg.py`, `thagid/services/knowledge_graph.py`, `thagid/routers/kg.py`, and `thagid/tests/test_kg.py`.
- Avoid frontend files, agent files, migrations, compose files, and browser-facing brainstorm routes unless the implementation proves absolutely necessary and the story scope is updated first.

### Testing Requirements

- Default tests must not require a live AGE/PostgreSQL instance.
- Service tests should prove SQL/Cypher parameterization and project scoping rather than relying on real vector indexes.
- Router tests should prove `verify_agent_key` and project validation happen before service execution.
- Regression tests should prove Story 4.1 graph traversal retrieval still works without embeddings.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story-4.2-Vector-Similarity-Search-for-Ideas]
- [Source: _bmad-output/planning-artifacts/prd.md#Knowledge-Graph-Retrieval]
- [Source: _bmad-output/planning-artifacts/architecture.md#Knowledge-Graph-API]
- [Source: _bmad-output/planning-artifacts/architecture.md#Embedding-Pipeline]
- [Source: _bmad-output/planning-artifacts/architecture.md#Embedding-Column-Convention]
- [Source: _bmad-output/planning-artifacts/architecture.md#AGE-Cypher-Query-Pattern]
- [Source: _bmad-output/implementation-artifacts/4-1-retrieve-brainstorm-session-results.md#Previous-Story-Intelligence]
- [Source: thagid/models/embeddings.py]
- [Source: thagid/services/embedding.py]
- [Source: thagid/services/knowledge_graph.py]
- [Source: thagid/routers/kg.py]
- [Source: thagid/schemas/kg.py]
- [Source: _bmad-output-old/1_datapipeline/project-context.md#Critical-Implementation-Rules]
- [Source: pgvector-python README#SQLAlchemy]

## Project Structure Notes

- This story extends the backend KG retrieval layer only. Epic 4 UI discovery and browsing remain assigned to Stories 4.3 and 4.4.
- The architecture originally listed `POST /internal/kg/projects/{project_id}/ideas/search`; use that route unless existing router naming conventions strongly require a clearer equivalent.
- The existing `idea_embeddings` table is the authoritative vector index. AGE remains the authoritative source for Idea properties.

## Dev Agent Record

### Agent Model Used

openai/gpt-5.5

### Debug Log References

- `rtk pytest thagid/tests/test_kg.py -q` — 38 passed
- `rtk pytest -q` — 273 passed

### Completion Notes List

- Ultimate context engine analysis completed - comprehensive developer guide created.
- Added internal KG vector search schemas with 1536-dimension finite embedding validation, bounded limits, and agent-safe result fields.
- Implemented project-scoped pgvector cosine ranking merged with parameterized AGE Idea lookups while preserving vector order and skipping stale graph nodes.
- Added `POST /internal/kg/projects/{project_id}/ideas/search` protected by `X-Agent-Key` and project validation.
- Added focused schema, service, and router tests for validation, authorization, project isolation, order preservation, empty results, and stale graph-node handling.

### File List

- `_bmad-output/implementation-artifacts/4-2-vector-similarity-search-for-ideas.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `thagid/routers/kg.py`
- `thagid/schemas/kg.py`
- `thagid/services/knowledge_graph.py`
- `thagid/tests/test_kg.py`

### Change Log

- 2026-05-11: Implemented internal KG vector similarity search for embedded ideas and marked story ready for review.
- 2026-05-11: Reviewed vector similarity search, added invalid-limit router validation coverage, and marked story done.
