# Story 4.1: Retrieve Brainstorm Session Results

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a package user,
I want completed brainstorm sessions to load their themes, ideas, metadata, and summary,
so that I can review previous ideation work after the session ends.

## Acceptance Criteria

1. Given a brainstorm session has concluded, when the frontend requests session results, then the backend returns session metadata, summary, themes, and ideas grouped by theme, and the response follows the existing API JSON conventions.
2. Given a user requests results for a package outside their organization or project scope, when the backend authorizes the request, then it returns the existing forbidden or not found response, and no graph data is exposed.
3. Given a concluded session has context chunks, when results are loaded, then the response can include source metadata needed by the UI, and raw unsupported file content is not exposed unnecessarily.

## Tasks / Subtasks

- [x] Add browser-facing brainstorm result schemas (AC: 1, 3)
  - [x] Add result response models in `thagid/schemas/brainstorm.py`; keep these separate from internal KG write schemas so browser responses do not expose storage-only fields or raw context content.
  - [x] Include session metadata: `session_id`, `package_id`, `project_id`, `technique`, `summary`, `created_at`, `concluded_at`, `theme_count`, `idea_count`, and `context_source_count`.
  - [x] Include `themes` as grouped data with `id`, `title`, `summary`, `position`, and `ideas` using existing browser-facing `BrainstormTheme`/`BrainstormIdea` shapes where practical.
  - [x] Include context source metadata only: `source_type`, `source_ref`, `summary`, and `content_hash` when available. Do not include `ContextChunk.content` in the browser-facing result response.
  - [x] Use snake_case JSON fields to match existing API conventions.
- [x] Implement KG result retrieval in `KnowledgeGraphService` (AC: 1, 3)
  - [x] Add a method such as `get_brainstorm_results(project_id: uuid.UUID, package_id: uuid.UUID)` to `thagid/services/knowledge_graph.py`.
  - [x] Reuse `graph_name_for_project`, `validate_graph_name`, `_setup_age`, and the parameterized AGE query pattern already used by `persist_brainstorm_output`.
  - [x] Match Session nodes by `package_id` and `project_id`; target concluded/persisted output using existing stored fields (`status`, `source_session_id`, `summary`, `technique`, `created_at`, `concluded_at`).
  - [x] Traverse `Session -[:HAS_THEME]-> Theme -[:CONTAINS_IDEA]-> Idea` and return ideas grouped under their theme.
  - [x] Traverse `Session -[:USES_CONTEXT]-> ContextChunk` and return source metadata without returning raw `content`.
  - [x] Sort themes by `position` when present, then title as a deterministic fallback. Sort ideas deterministically by title if the graph query does not provide stable idea ordering; do not change KG write schema just to add idea positions in this story.
  - [x] Raise a domain not-found error when no persisted brainstorm session exists for the package so the router can return 404.
- [x] Add authenticated browser-facing endpoint (AC: 1, 2, 3)
  - [x] Add `GET /api/packages/{package_id}/brainstorm/results` to `thagid/routers/brainstorm.py`.
  - [x] Reuse existing `verify_package_access(package_id, user, db)` before any KG service call.
  - [x] Return 422 for invalid package IDs, 404 for missing package/project or missing concluded brainstorm results, and 403 for cross-organization access using existing router behavior.
  - [x] Do not expose `/internal/kg/*` to browser clients and do not add a browser-facing raw KG endpoint.
- [x] Add frontend API client types without building Epic 4 UI yet (AC: 1)
  - [x] Add TypeScript result interfaces in `web/src/lib/types/brainstorm.ts` matching the backend response shape.
  - [x] Add `getBrainstormResults(packageId: string)` in `web/src/lib/api/brainstorm.ts` using the existing `apiFetch` wrapper.
  - [x] Do not add summary cards, detail pages, theme browsing UI, or route changes in this story; those belong to stories 4.3 and 4.4.
- [x] Preserve existing behavior and story boundaries (AC: 1, 2, 3)
  - [x] Preserve active brainstorm status and message behavior in `GET /brainstorm/status` and `POST /brainstorm/message`.
  - [x] Preserve internal KG persistence, node versioning, and async embedding behavior.
  - [x] Do not implement vector similarity search; Story 4.2 owns that work.
  - [x] Do not return raw AGE/graph node objects, graph names, Cypher results, embedding vectors, OpenAI metadata, or raw context file content to the browser.
  - [x] Do not introduce new libraries or storage tables.
- [x] Add focused tests and verification (AC: 1, 2, 3)
  - [x] Add KG service tests in `thagid/tests/test_kg.py` using the existing fake session pattern to assert AGE setup, parameterized query usage, `HAS_THEME`, `CONTAINS_IDEA`, `USES_CONTEXT`, and no raw context `content` in the mapped response.
  - [x] Add service tests for no-session/not-found behavior and deterministic theme/idea grouping.
  - [x] Add router tests in `thagid/tests/test_brainstorm.py` for success, unauthenticated access, invalid package ID, package not found, cross-org forbidden, no concluded results, and ensuring KG service is not called after authorization failure.
  - [x] Add schema/API client checks as appropriate for the TypeScript result shape.
  - [x] Run `rtk pytest thagid/tests/test_kg.py thagid/tests/test_brainstorm.py -q`.
  - [x] Run `rtk npm run check` from `web/` if TypeScript files are changed.

### Review Findings

- [x] [Review][Patch] Theme IDs expose KG internal node IDs [thagid/services/knowledge_graph.py:195]
- [x] [Review][Defer] Versioned KG nodes are not surfaced in retrieved results [thagid/services/knowledge_graph.py:191] — deferred, pre-existing

## Dev Notes

### Scope Boundaries

- This story creates the retrieval API foundation for Epic 4 review surfaces.
- This story is primarily backend retrieval plus a frontend API helper/type contract; it should not build dashboard cards, detail routes, or theme browsing UI.
- Retrieval is package-scoped for the MVP because the PRD and architecture define one brainstorm session per package.
- Use the persisted KG data created by Epic 3 as the source of truth. Do not reconstruct final results from chat messages or agent checkpoints.
- Returning 404 when no persisted/concluded brainstorm exists is acceptable and matches existing API not-found behavior.

### Current Codebase State

- `thagid/services/knowledge_graph.py` currently writes Session, Theme, Idea, and ContextChunk nodes through `persist_brainstorm_output`, but has no result retrieval method.
- `KnowledgeGraphService._write_session` stores `source_session_id`, `package_id`, `project_id`, `status`, `technique`, `summary`, `created_at`, and `concluded_at` on Session nodes.
- `KnowledgeGraphService._write_themes_and_ideas` stores Theme nodes with `source_id`, `title`, `summary`, and `position`, and Idea nodes with `category`, `title`, `concept`, and `novelty`.
- `KnowledgeGraphService._write_context_chunks` stores ContextChunk nodes with `source_type`, `source_ref`, `content`, `summary`, and `content_hash`. Browser-facing retrieval must not return `content`.
- `thagid/routers/brainstorm.py` already has `verify_package_access`, which checks package existence, project existence, and organization ownership before calling agent-facing services.
- `thagid/schemas/brainstorm.py` already contains browser-facing `BrainstormIdea`, `BrainstormTheme`, `BrainstormMessageResponse`, and `BrainstormStatusResponse`.
- `web/src/lib/api/brainstorm.ts` currently exposes `getBrainstormStatus`, `sendBrainstormMessage`, and `getBrainstormTechniques` through `apiFetch`.
- `web/src/lib/types/brainstorm.ts` currently has types for status/message responses, ideas, themes, attachments, and techniques, but no result response type.
- Existing backend tests use SQLite by default. AGE-specific behavior is tested with fake/mocked sessions in `thagid/tests/test_kg.py`; follow that pattern.

### Required Result Shape

Use a compact response shape aligned with existing API JSON conventions:

```json
{
  "session_id": "uuid",
  "package_id": "uuid",
  "project_id": "uuid",
  "technique": "SCAMPER Method",
  "summary": "Final session summary",
  "created_at": "2026-05-11T10:00:00Z",
  "concluded_at": "2026-05-11T10:00:00Z",
  "theme_count": 1,
  "idea_count": 2,
  "context_source_count": 1,
  "themes": [
    {
      "id": "theme-general",
      "title": "General",
      "summary": "2 ideas grouped under General.",
      "position": 0,
      "ideas": [
        {
          "category": "general",
          "title": "Interview Customers",
          "concept": "Run customer interviews",
          "novelty": "incremental"
        }
      ]
    }
  ],
  "context_sources": [
    {
      "source_type": "file",
      "source_ref": "brief.md",
      "summary": "Context summary",
      "content_hash": "abc123"
    }
  ]
}
```

### Architecture Guardrails

- Follow Router -> Service -> Model. Routers handle HTTP/auth/status mapping; `KnowledgeGraphService` owns AGE graph traversal and result mapping.
- Keep all browser-facing endpoints under `/api/packages/{package_id}/brainstorm/...` and JWT-authenticated through existing middleware.
- Keep internal KG endpoints under `/internal/kg/...` and `X-Agent-Key` authenticated only.
- Derive graph names only from the authorized project UUID using `project_{uuid_with_hyphens_replaced_by_underscores}`.
- Use AGE parameter payloads for package/project/session values. Never interpolate user-controlled values into Cypher.
- Do not expose graph names, raw Cypher, raw agtype payloads, internal node ids unless explicitly needed by UI, embedding vectors, or context chunk raw content to browser clients.
- Preserve project isolation by resolving graph namespace from the authorized package's project, not from user-provided query/body data.

### Previous Story Intelligence

- Story 3.2 implemented KG persistence and deliberately stored ContextChunk raw `content` for internal graph use. This story must avoid leaking that raw content through browser results.
- Story 3.3 added node versioning and validation, but story status is currently `review`; if review patches are pending, do not depend on unreviewed behavior beyond code that exists at implementation time.
- Story 3.4 added async idea embeddings after KG persistence. Retrieval by graph traversal must work whether or not embeddings exist.
- Story 3.5 concluded sessions and stores the final summary before KG write, so Session `summary` is the preferred source for result summary.
- Recent commits show the current pattern: keep changes minimal, add focused tests, and preserve browser-facing response compatibility.

### File Structure Requirements

- Likely backend updates: `thagid/schemas/brainstorm.py`, `thagid/services/knowledge_graph.py`, `thagid/routers/brainstorm.py`, `thagid/tests/test_kg.py`, and `thagid/tests/test_brainstorm.py`.
- Likely frontend updates: `web/src/lib/types/brainstorm.ts` and `web/src/lib/api/brainstorm.ts`.
- Avoid migrations, models, agent files, frontend routes/pages, and custom UI components in this story.

### Testing Requirements

- KG service tests should not require live AGE/PostgreSQL in the default suite.
- Router tests should verify authorization happens before graph retrieval.
- Regression tests should prove existing brainstorm status/message routes still pass and markdown responses remain optional.
- TypeScript changes should pass `rtk npm run check`.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story-4.1-Retrieve-Brainstorm-Session-Results]
- [Source: _bmad-output/planning-artifacts/prd.md#Knowledge-Graph-Retrieval]
- [Source: _bmad-output/planning-artifacts/prd.md#Journey-4-Reviewing-Brainstorm-Results]
- [Source: _bmad-output/planning-artifacts/architecture.md#Knowledge-Graph-API]
- [Source: _bmad-output/planning-artifacts/architecture.md#KG-Retrieval-FR28-FR30]
- [Source: _bmad-output/planning-artifacts/architecture.md#AGE-Cypher-Query-Pattern]
- [Source: _bmad-output/implementation-artifacts/3-2-knowledge-graph-domain-api-and-atomic-writes.md#Completion-Notes-List]
- [Source: _bmad-output/implementation-artifacts/3-4-async-embeddings-for-brainstorm-ideas.md#Completion-Notes-List]
- [Source: _bmad-output/implementation-artifacts/3-5-bmad-markdown-rendering-and-final-session-summary.md#Completion-Notes-List]
- [Source: thagid/services/knowledge_graph.py]
- [Source: thagid/routers/brainstorm.py]
- [Source: thagid/schemas/brainstorm.py]
- [Source: web/src/lib/api/brainstorm.ts]
- [Source: web/src/lib/types/brainstorm.ts]
- [Source: _bmad-output-old/1_datapipeline/project-context.md#Critical-Implementation-Rules]

## Project Structure Notes

- The architecture lists internal KG retrieval methods, but this story needs a browser-facing package-scoped results endpoint for review surfaces. Keep raw KG internals behind the service layer.
- Epic 4 stories build in layers: this story retrieves structured results, Story 4.2 adds vector search, Story 4.3 adds dashboard discovery, and Story 4.4 adds detail browsing UI.
- The current write model does not store explicit idea positions. Use deterministic fallback ordering for ideas rather than expanding persistence scope.

## Dev Agent Record

### Agent Model Used

openai/gpt-5.5

### Debug Log References

- Red phase: `rtk pytest thagid/tests/test_kg.py thagid/tests/test_brainstorm.py -q` failed with missing result schema/domain error imports before implementation.
- Focused backend verification: `rtk pytest thagid/tests/test_kg.py thagid/tests/test_brainstorm.py -q` passed, 85 tests.
- Frontend type verification: `rtk npm run check` from `web/` passed with 0 errors and 0 warnings.
- Full backend regression: `rtk pytest -q` passed, 266 tests.
- Frontend unit regression: `rtk npm run test:unit` from `web/` passed, 9 files and 39 tests.

### Completion Notes List

- Ultimate context engine analysis completed - comprehensive developer guide created.
- Added browser-facing brainstorm results schemas and TypeScript API contract without exposing raw context content.
- Added KG retrieval through parameterized AGE queries, deterministic theme/idea grouping, source metadata mapping, and domain not-found handling.
- Added authenticated package-scoped results endpoint that verifies package access before graph retrieval.
- Added focused KG and router tests covering success, authorization failures, missing results, grouping, and no raw context content exposure.

### File List

- `thagid/schemas/brainstorm.py`
- `thagid/services/knowledge_graph.py`
- `thagid/routers/brainstorm.py`
- `thagid/tests/test_kg.py`
- `thagid/tests/test_brainstorm.py`
- `web/src/lib/types/brainstorm.ts`
- `web/src/lib/api/brainstorm.ts`

### Change Log

- 2026-05-11: Implemented story 4.1 retrieve brainstorm session results and marked ready for review.
- 2026-05-11: BMad code review completed; patched browser-facing theme IDs to use source IDs and marked story done.
