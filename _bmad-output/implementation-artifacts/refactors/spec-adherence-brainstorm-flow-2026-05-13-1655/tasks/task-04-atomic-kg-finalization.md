# Task 04: Implement Atomic Confirmed KG Finalization

## Implementation Contract

- Objective: Persist confirmed brainstorm output atomically through the backend aggregate KG finalization route, queue embeddings only after successful writes, and surface persistence failures.
- Runtime entrypoint: Agent finalization path after user confirmation; internal backend route `POST /internal/kg/projects/{project_id}/brainstorm-output`.
- Old owner: Agent `backend_client.persist_brainstorm_output()` performs granular multi-call writes; `extract_node` swallows exceptions.
- New owner: Agent finalization builds one validated aggregate payload; backend `KnowledgeGraphService.persist_brainstorm_output()` owns atomic KG write; FastAPI background tasks own embeddings after success.
- Forbidden implementation patterns: No granular multi-call finalization for confirmed output; no catch-and-pass around persistence; no marking checkpoint/session concluded before KG write and markdown render both succeed; no direct agent DB/KG access.
- Required implementation patterns: One aggregate HTTP call with `X-Agent-Key`; Pydantic/KG schema validation; single backend transaction; rollback on failure; logged embedding failures only after successful KG writes.
- Compatibility allowed: Keep granular KG endpoints for lower-level operations and existing tests if still useful.
- Compatibility forbidden: Partial Session/Theme/Idea/ContextChunk final persistence; embedding tasks queued for failed writes; browser-visible internal route exposure.
- Files allowed: `agent/backend_client.py`, finalization node/helper files under `agent/brainstorm/`, `agent/main.py`, `thagid/routers/kg.py`, `thagid/services/knowledge_graph.py`, `thagid/schemas/kg.py`, `thagid/services/embedding.py`, agent and backend KG tests.
- Files forbidden: Frontend UI except tests faking backend later; stale `docs/**`; migrations unless schema changes are truly required and approved by existing architecture.

## Work Items

- Likely files / areas:
  - `agent/backend_client.py` aggregate finalization client.
  - `agent/brainstorm/nodes/markdown.py` or finalization helper for confirmed flow.
  - `thagid/routers/kg.py` aggregate route behavior and error mapping.
  - `thagid/services/knowledge_graph.py` aggregate transaction, idempotency, status, result retrieval, versioning implications.
  - `thagid/tests/test_kg.py`, `agent/tests/test_brainstorm.py`.
- Subtasks:
  - Replace finalization payload sending with one aggregate `/brainstorm-output` call.
  - Remove KG persistence from unconfirmed extract.
  - Ensure aggregate payload includes `session_id`, `package_id`, `project_id`, `technique`, final summary, finalized themes with `source_id`, ideas, context chunks, and finalized timestamp.
  - Ensure backend validates package/project access for the aggregate route and returns 404/422/500 consistently.
  - Ensure `KnowledgeGraphService.persist_brainstorm_output()` rolls back all graph writes on failure.
  - Ensure embedding jobs are queued only after successful aggregate persistence.
  - Decide implementation of repeat finalization/idempotency: either idempotent same payload success or explicit no-op if already finalized, but never duplicate inconsistent nodes.
  - Add tests for partial failure rollback and no false concluded state on failure.

## Completion Checks

- Done when:
  - Confirmed finalization uses exactly one aggregate internal KG call from agent.
  - KG write failure propagates to agent/backend and the session is not reported as concluded.
  - Aggregate KG write is transactional and tests prove rollback on mid-write failure.
  - Embedding tasks are queued after successful persistence and not on failure.
  - Dashboard results can retrieve finalized Session/Theme/Idea/ContextChunk data.
- Evidence required:
  - Test references for successful aggregate finalization, rollback, and error propagation.
  - Source references showing finalization no longer uses granular multi-call sequence.
- Forbidden shortcuts:
  - Keeping granular finalization but wrapping in try/except.
  - Adding client-side retries that hide backend failure.
  - Persisting a final markdown message before KG persistence succeeds.
- Static checks:
  - Search for `pass` in KG persistence error paths confirms no swallowed finalization failure.
  - Agent code still imports no `thagid` modules.
- Test commands:
  - `pytest agent/tests/test_brainstorm.py thagid/tests/test_kg.py thagid/tests/test_brainstorm.py`
- Runtime-path evidence:
  - Fake backend failure causes `/internal/agent/brainstorm/message` confirmation request to fail instead of returning `concluded`.
- Validation:
  - Backend KG route tests and agent finalization integration tests.
- Risks / notes:
  - AGE transaction behavior must be tested with existing fakes/mocks and, if possible, integration DB tests.
