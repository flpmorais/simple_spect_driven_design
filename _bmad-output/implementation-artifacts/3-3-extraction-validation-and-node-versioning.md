# Story 3.3: Extraction Validation and Node Versioning

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a package user,
I want extracted brainstorm data validated and versioned,
so that final output is structurally complete and future changes have an audit trail.

## Acceptance Criteria

1. Given extraction produces themes and ideas, when validation runs, then it detects missing summaries, orphan ideas, empty themes, and missing required fields, and it auto-corrects issues that match the architecture validation pattern.
2. Given extraction has no meaningful ideas after correction, when validation fails fundamentally, then the workflow routes back to Facilitate with an explanation, and the retry loop is limited according to the architecture pattern.
3. Given an existing graph node must be changed, when the KG service updates it, then it creates a new version linked by VERSION_OF, and stores agent id, change description, and created timestamp metadata.

## Tasks / Subtasks

- [x] Add deterministic extraction validation before confirmed KG persistence (AC: 1, 2)
  - [x] Add a small validation helper in `agent/main.py` or a focused helper module if it keeps `agent/main.py` readable; do not migrate to the future `agent/brainstorm/nodes/validate.py` layout in this story.
  - [x] Validate current checkpoint `ideas` and `themes` during Extract-phase confirmation before calling `persist_brainstorm_output`.
  - [x] Detect and correct missing theme summaries by regenerating deterministic summaries in the existing Story 3.1 style.
  - [x] Detect and remove empty themes.
  - [x] Detect orphan structured ideas from `state["ideas"]` that are not present in any theme and add them to a `General` theme.
  - [x] Detect duplicate idea membership across themes and keep each idea exactly once using the first occurrence, preserving existing theme order.
  - [x] Detect missing required idea fields (`category`, `title`, `concept`, `novelty`) and theme fields (`id`, `title`, `summary`, `ideas`); auto-correct only when a safe deterministic value exists.
  - [x] Persist corrected themes back to checkpoint state before KG write so the browser-facing response and persisted KG payload match.
  - [x] Do not call an LLM for validation or correction.
- [x] Implement fundamental validation failure routing (AC: 2)
  - [x] If validation produces zero meaningful ideas or zero non-empty themes after correction, do not call `/internal/kg/...`.
  - [x] Set phase back to `facilitate`, preserve messages, active documents, technique, rolling summary, and existing ideas, and reply with the architecture-defined explanation: `I wasn't able to extract meaningful ideas. Let's continue brainstorming.` or equivalent.
  - [x] Track a bounded retry counter in checkpoint state, such as `validation_retry_count`, and limit the Extract -> Validate -> Facilitate retry loop to 2 retries.
  - [x] Reset or clear the retry counter after a successful validation and KG persistence.
  - [x] Keep failures recoverable; the user should be able to add ideas and say done again without losing previous session context.
- [x] Integrate validation with the existing confirmation/KG write flow (AC: 1, 2)
  - [x] Update the existing Extract-phase confirmation block in `agent/main.py` that currently calls `persist_brainstorm_output`.
  - [x] Run validation/correction before `_build_kg_write_payload` so the KG receives validated data only.
  - [x] If validation corrects themes, include the corrected `themes` in the response and checkpoint save.
  - [x] Preserve Story 3.2 idempotency: if `kg_write_completed is True` and `kg_node_ids` exists, repeated confirmation must not run validation in a way that mutates already-persisted data or call the backend again.
  - [x] Preserve Story 3.2 retry behavior: KG failure must leave `themes_confirmed` false or unset `kg_write_completed`, keep phase recoverable, and return the standard brainstorm error.
  - [x] Do not implement BMAD markdown rendering, phase conclusion, or embeddings in this story.
- [x] Extend KG schemas for node versioning (AC: 3)
  - [x] Add request/response schemas to `thagid/schemas/kg.py` for versioning an existing graph node.
  - [x] Include `node_label` as an allowlisted value (`Session`, `Theme`, `Idea`, `ContextChunk`), `properties` as a non-empty dict of updated properties, `agent_id`, and `change_description`.
  - [x] Validate `agent_id` and `change_description` as non-empty strings.
  - [x] Ensure arbitrary labels, relationship types, graph names, and raw Cypher are never accepted from request payloads.
  - [x] Return the new version node id and previous node id.
- [x] Implement `KnowledgeGraphService.update_node` with VERSION_OF (AC: 3)
  - [x] Add `update_node` to `thagid/services/knowledge_graph.py` using the existing graph namespace helper and AGE setup pattern.
  - [x] Match the existing node by id and allowlisted label.
  - [x] Create a new node with a generated UUID `id`, merged or explicitly provided updated properties, and audit metadata: `agent_id`, `change_description`, `created_at`.
  - [x] Link the new node to the previous node with `VERSION_OF` exactly.
  - [x] Use parameterized AGE value payloads; labels may be selected from allowlisted constant query templates only.
  - [x] Commit on success and rollback on failure, matching current `persist_brainstorm_output` service behavior.
  - [x] Return 404-style domain feedback when the target node does not exist if practical with AGE query results; otherwise document/test the current MVP behavior.
- [x] Add internal KG versioning endpoint protected by `X-Agent-Key` (AC: 3)
  - [x] Add `PATCH /internal/kg/projects/{project_id}/nodes/{node_id}` to `thagid/routers/kg.py`.
  - [x] Reuse `verify_agent_key` from `thagid/routers/internal.py`.
  - [x] Resolve project id through `get_project` before calling the KG service; the requester must not provide graph names.
  - [x] Map invalid payloads to 422, missing project or node to 404 where implemented, and unexpected AGE failures to the existing FastAPI error behavior.
  - [x] Do not expose this endpoint through browser-facing `/api/*` routes in this story.
- [x] Preserve existing story behavior and boundaries (AC: 1, 2, 3)
  - [x] Preserve Story 3.1 theme grouping, theme adjustment, and ThemeCard/browser response behavior.
  - [x] Preserve Story 3.2 confirmed KG persistence, `kg_write_completed`, `kg_node_ids`, and `active_documents` ContextChunk payload behavior.
  - [x] Preserve existing non-brainstorm package chat and browser-facing brainstorm fields.
  - [x] Do not add embeddings, pgvector tables, vector search, dashboard summary cards, brainstorm detail retrieval, or markdown rendering.
  - [x] Do not introduce new libraries.
- [x] Add focused tests and verification (AC: 1, 2, 3)
  - [x] Add agent tests for validation correcting missing summaries, removing empty themes, assigning orphan ideas to General, and removing duplicate idea memberships.
  - [x] Add agent tests for fundamental validation failure routing back to Facilitate with no KG call and bounded retry counter behavior.
  - [x] Add agent regression tests that successful validation still calls KG once and stores `kg_write_completed`/`kg_node_ids` as Story 3.2 expects.
  - [x] Add KG schema tests for node versioning validation and label allowlist rejection.
  - [x] Add KG service tests using the existing fake/mocked session pattern to prove `VERSION_OF`, audit metadata, rollback on failure, and parameterized properties.
  - [x] Add KG router tests for `PATCH /internal/kg/projects/{project_id}/nodes/{node_id}` auth, project validation, success, and invalid payloads.
  - [x] Run `rtk pytest agent/tests/test_brainstorm.py -q`.
  - [x] Run `rtk pytest thagid/tests/test_kg.py thagid/tests/test_internal.py -q` or the focused backend tests added for this story.
  - [x] Run `rtk pytest thagid/tests/test_brainstorm.py thagid/tests/test_agent_client.py -q` to catch brainstorm contract regressions.

## Dev Notes

### Scope Boundaries

- This story adds deterministic validation of extracted brainstorm data and KG node versioning.
- This story is backend/agent-only unless a test exposes a browser response regression.
- Validation must be deterministic Python code, not freeform LLM output.
- Node versioning is KG API functionality for future agents/clients. It does not require new frontend UI.
- Do not implement Story 3.4 embeddings or Story 3.5 BMAD markdown rendering.
- Do not migrate the prototype to the future LangGraph folder layout; current agent behavior is centralized in `agent/main.py`.

### Current Codebase State

- `agent/main.py` currently supports phases `initiate`, `facilitate`, `extract`, `validate`, `markdown`, and `concluded`, but Validate/Markdown behavior is not implemented yet.
- Story 3.1 added deterministic theme grouping and adjustment in Extract phase.
- Story 3.2 added `_build_kg_write_payload`, `persist_brainstorm_output`, `kg_write_completed`, and `kg_node_ids` on successful confirmation.
- Current Extract confirmation in `agent/main.py` calls KG persistence directly after confirming themes; this story should insert validation before payload building/KG write.
- `agent/backend_client.py` has `persist_brainstorm_output(project_id, payload)` posting to `/internal/kg/projects/{project_id}/brainstorm-output` with `X-Agent-Key`.
- `thagid/schemas/kg.py` currently has write schemas for KG brainstorm output and `KGWriteResponse`; it does not have node versioning schemas.
- `thagid/services/knowledge_graph.py` currently creates graph nodes and relationships for Session, Theme, Idea, and ContextChunk. It does not implement `update_node` or `VERSION_OF` yet.
- `thagid/routers/kg.py` currently exposes `POST /internal/kg/projects/{project_id}/brainstorm-output`, protected by `X-Agent-Key`.
- `thagid/tests/test_kg.py` uses a fake async session to test AGE SQL shape because the default backend tests use SQLite.
- The worktree currently includes Story 3.2 implementation changes in review. Do not revert or rewrite those changes outside the minimum needed for Story 3.3 context.

### Required Validation Behavior

- Use `state["ideas"]` as the canonical list of extracted structured ideas.
- Use `state["themes"]` as the review grouping selected by the user.
- Every canonical idea should appear exactly once across validated themes.
- If a canonical idea is absent from all themes, add it to `General`.
- If an idea appears in multiple themes, keep the first occurrence by theme order and remove later duplicates.
- If a theme has no ideas after correction, remove it.
- If a theme summary is missing or blank, generate a deterministic summary from its idea count and title.
- If theme IDs are missing but title exists, generate the existing `theme-{slug}` style ID.
- If an idea is missing a required field and cannot be normalized with existing `agent.ideas.normalize_idea` behavior, exclude it from validated output.
- If no meaningful ideas remain after correction, route back to Facilitate and do not write KG data.

### Required Versioning Behavior

- `update_node` must create a new node rather than mutating the existing graph node in place.
- The new node must link to the prior node with `VERSION_OF`.
- The previous node must remain available for audit/history traversal.
- The new version must include audit metadata: `agent_id`, `change_description`, and `created_at`.
- Node labels must be selected from an allowlist and inserted only through constant query templates; never accept a raw label or raw Cypher fragment.
- Updated properties should remain snake_case and JSON-serializable.
- Do not add pgvector embedding columns or embedding updates as part of versioning in this story.

### Architecture Guardrails

- Follow Router -> Service -> Model. Routers handle HTTP/auth/status mapping; services own business/database logic.
- Services receive `AsyncSession`; do not create new SQLAlchemy sessions inside services.
- Preserve container boundaries: the agent calls backend HTTP endpoints and never imports `thagid.*`.
- Internal KG endpoints remain under `/internal/kg/...` and require `X-Agent-Key`.
- Browser-facing endpoints remain under `/api/packages/{package_id}/brainstorm/...` and should not expose node versioning in this story.
- AGE graph names are derived from project UUID only: `project_{uuid_with_hyphens_replaced_by_underscores}`.
- AGE needs `LOAD 'age'` and `SET search_path = ag_catalog, "$user", public` on the active DB session/connection before Cypher operations.
- Use parameterized AGE values. The current service builds query templates internally; keep all user/session/theme/idea/context/update values in `params`, not string interpolation.
- Existing SQLite backend tests cannot execute AGE; use fake/mocked session tests for SQL shape and transaction behavior.

### Previous Story Intelligence

- Story 3.2 is in review and implemented KG write schemas, `KnowledgeGraphService`, `/internal/kg/projects/{project_id}/brainstorm-output`, and agent confirmation persistence.
- Story 3.2 stores KG write result metadata in checkpoint state as `kg_node_ids` and idempotency flag `kg_write_completed`.
- Story 3.2 tests established the fake session pattern in `thagid/tests/test_kg.py`; extend that pattern for VERSION_OF tests.
- Story 3.2 deliberately deferred validation retries, node versioning, embeddings, markdown rendering, and retrieval UI. This story owns validation and node versioning only.
- Story 3.1 adjustment can clear `themes_confirmed`; if this happens after a KG write, do not silently mutate persisted graph data in this story unless explicitly using node versioning behavior through the KG API.
- Story 2.5 and 2.6 established file/URL `active_documents`; validation must preserve them for KG ContextChunk writes.
- Recent committed history still ends at Story 3.1; Story 3.2 changes are currently uncommitted/in review in the worktree.

### File Structure Requirements

- Likely agent updates: `agent/main.py` and `agent/tests/test_brainstorm.py`.
- Possible agent helper: `agent/validation.py` only if it reduces `agent/main.py` complexity without over-abstraction.
- Likely backend updates: `thagid/schemas/kg.py`, `thagid/services/knowledge_graph.py`, `thagid/routers/kg.py`, and `thagid/tests/test_kg.py`.
- Do not modify frontend files unless existing browser-facing brainstorm contract tests require it.
- Do not add migrations or SQLAlchemy models for embeddings in this story.

### Testing Requirements

- Agent validation tests should assert both response payload and saved checkpoint state.
- KG write tests should assert no backend persistence call occurs on fundamental validation failure.
- Repeated confirmation tests should preserve Story 3.2 idempotency and avoid a second backend call.
- Node versioning service tests should assert `VERSION_OF` appears in the internally generated Cypher template and update values appear only in params.
- Router tests should cover missing/wrong `X-Agent-Key` and project-not-found behavior before service call.
- Prefer focused test commands first; run wider backend/agent tests if failures suggest shared contract regressions.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story-3.3-Extraction-Validation-and-Node-Versioning]
- [Source: _bmad-output/planning-artifacts/prd.md#Brainstorm-Output]
- [Source: _bmad-output/planning-artifacts/prd.md#Knowledge-Graph-Storage]
- [Source: _bmad-output/planning-artifacts/architecture.md#Data-Architecture]
- [Source: _bmad-output/planning-artifacts/architecture.md#Knowledge-Graph-API]
- [Source: _bmad-output/planning-artifacts/architecture.md#LangGraph-State-Machine]
- [Source: _bmad-output/planning-artifacts/architecture.md#Validation-Failure-Pattern]
- [Source: _bmad-output/planning-artifacts/architecture.md#AGE-Cypher-Query-Pattern]
- [Source: _bmad-output/implementation-artifacts/3-2-knowledge-graph-domain-api-and-atomic-writes.md#Completion-Notes-List]
- [Source: agent/main.py]
- [Source: agent/backend_client.py]
- [Source: thagid/schemas/kg.py]
- [Source: thagid/services/knowledge_graph.py]
- [Source: thagid/routers/kg.py]
- [Source: thagid/tests/test_kg.py]
- [Source: _bmad-output-old/main/project-context.md#Critical-Implementation-Rules]

## Project Structure Notes

- Architecture names a future `validate.py` LangGraph node, but the current prototype has not migrated to node-per-file agent structure. Implement validation in the current flow and keep future migration out of scope.
- Story 3.2 chose a single atomic `brainstorm-output` endpoint instead of the full list of architecture endpoints to avoid partial-write ambiguity. Story 3.3 can add the architecture-listed `PATCH /internal/kg/projects/{project_id}/nodes/{node_id}` endpoint for versioning without changing the write endpoint.
- Keep this story as a minimal bridge from confirmed extraction to validated persistence plus version history; markdown and embeddings remain later stories.

## Dev Agent Record

### Agent Model Used

openai/gpt-5.5

### Debug Log References

- `rtk pytest agent/tests/test_brainstorm.py -q` - 98 passed
- `rtk pytest thagid/tests/test_kg.py -q` - 28 passed
- `rtk pytest thagid/tests/test_kg.py thagid/tests/test_internal.py -q` - 34 passed
- `rtk pytest thagid/tests/test_brainstorm.py thagid/tests/test_agent_client.py -q` - 50 passed
- `rtk pytest -q` - 256 passed

### Completion Notes List

- Ultimate context engine analysis completed - comprehensive developer guide created.
- Implemented deterministic extract validation in `agent/main.py`, including safe normalization, missing summary/id correction, empty theme removal, duplicate membership removal, orphan assignment, and no-LLM correction before KG persistence.
- Added recoverable validation failure routing back to Facilitate with bounded `validation_retry_count`, preserved session context, and no KG call on fundamental validation failure.
- Added KG node versioning schemas, service behavior, and protected internal PATCH endpoint with allowlisted labels, parameterized AGE values, `VERSION_OF`, audit metadata, commit/rollback behavior, and 404 mapping where detectable.
- Added focused agent and backend tests for validation correction/failure, KG schema validation, service SQL/audit behavior, rollback, auth, project validation, and endpoint success.

### File List

- agent/main.py
- agent/tests/test_brainstorm.py
- thagid/schemas/kg.py
- thagid/services/knowledge_graph.py
- thagid/routers/kg.py
- thagid/tests/test_kg.py
- _bmad-output/implementation-artifacts/3-3-extraction-validation-and-node-versioning.md
- _bmad-output/implementation-artifacts/sprint-status.yaml

### Review Findings

- [x] [Review][Patch] Validation retry limit is counted but not enforced [agent/main.py:881]
- [x] [Review][Patch] Malformed/missing theme and idea fields can be rejected before validation can correct or remove them [agent/main.py:96]
- [x] [Review][Patch] Duplicate validated theme ids can make finalization fail during KG payload validation [agent/main.py:333]
- [x] [Review][Patch] Idempotency shortcut ignores required `kg_node_ids` metadata [agent/main.py:862]

### Change Log

- 2026-05-11: Implemented extraction validation, recoverable validation retry routing, KG node versioning, internal update endpoint, and focused regression coverage.
