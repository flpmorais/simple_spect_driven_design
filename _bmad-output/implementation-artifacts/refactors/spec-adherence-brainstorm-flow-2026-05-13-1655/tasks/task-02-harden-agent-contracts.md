# Task 02: Harden Agent Contracts And PydanticAI Execution

## Implementation Contract

- Objective: Make required agent execution explicit, typed, retry-aware, and non-silent; define stable internal data contracts for phases, themes, ideas, context chunks, and finalization payloads.
- Runtime entrypoint: `POST /internal/agent/brainstorm/message` in `agent/main.py`, which invokes the LangGraph graph.
- Old owner: Mixed fallback behavior in `agent/brainstorm/agents.py` and ad hoc dictionaries across nodes.
- New owner: Agent schemas/helpers under `agent/brainstorm/` own internal typed contracts; PydanticAI runners own phase outputs; tests inject fake runners deliberately.
- Forbidden implementation patterns: No silent fallback that appears successful for required phases; no freeform unvalidated dicts crossing node boundaries when a typed model is required; no `thagid` imports; no LangChain application APIs; no direct KG/database writes from agent except checkpointing.
- Required implementation patterns: Pydantic models for phase outputs and finalization payload assembly; explicit exceptions for required PydanticAI failures after retry behavior; deterministic helper functions for theme/source ID normalization; fake runners in tests.
- Compatibility allowed: Retain optional additive internal response fields (`technique`, counts, `active_documents`) if public/backend bridge tests explicitly cover them.
- Compatibility forbidden: Returning `# Brainstorm Summary` or default recommendations as successful final output after a required phase failure; swallowing runner creation/runtime errors for finalization-critical phases.
- Files allowed: `agent/brainstorm/agents.py`, `agent/brainstorm/state.py`, `agent/brainstorm/nodes/*.py`, `agent/main.py`, `agent/backend_client.py`, `agent/ideas.py`, `agent/summary.py`, agent tests.
- Files forbidden: `thagid/**` except tests that fake agent responses in later tasks; `web/**`; stale `docs/**`.

## Work Items

- Likely files / areas:
  - `agent/brainstorm/agents.py` for runner creation, typed execution, and explicit error behavior.
  - `agent/brainstorm/state.py` for response/phase/state helpers.
  - `agent/brainstorm/nodes/*.py` for typed result contracts.
  - `agent/tests/test_brainstorm_nodes.py`, `agent/tests/test_brainstorm.py` for fake runner behavior.
- Subtasks:
  - Define an agent-specific exception type for required phase execution failure that can propagate to FastAPI as the standard brainstorm error.
  - Split required vs optional agent execution behavior. Required phases include initiate recommendation, facilitate response when no deterministic response is available, extract/theme preparation, validate, and final markdown/finalization inputs.
  - Remove or constrain fallback behavior so it is only used in tests via injected fake runners or in non-final, explicitly degraded responses that cannot persist or conclude.
  - Ensure phase output models require fields needed downstream: theme IDs/source IDs, summaries, ideas, markdown, validation status, retry reason.
  - Normalize theme payload shape in one helper so downstream KG finalization always receives `source_id`, `title`, `summary`, `position`, and non-empty ideas.
  - Ensure `build_internal_response` returns the required internal shape and only documented additive fields.
  - Update tests to prove failures are surfaced and fake runners are explicit.

## Completion Checks

- Done when:
  - Required PydanticAI phase failures cannot produce a success-like concluded/finalized response.
  - Tests use explicit fake runners and do not depend on silent fallback paths.
  - Internal response shape includes at least `reply`, `session_id`, `state_change`, `ideas`, `themes`, `markdown` and any additive fields are covered by tests.
  - Theme/finalization payload normalization is centralized and tested.
- Evidence required:
  - Source references to the new error path and typed output helpers.
  - Test references proving required phase failure propagation and fake runner success paths.
- Forbidden shortcuts:
  - Catching `Exception` and returning fallback success.
  - Marking sessions `concluded` when markdown/finalization inputs are invalid.
  - Adding new LLM libraries or bypassing PydanticAI for required agent execution.
- Static checks:
  - `agent/tests/test_architecture_boundaries.py` still proves no `thagid` imports and no forbidden LangChain APIs.
  - Search confirms no new `from thagid` imports under `agent/`.
- Test commands:
  - `pytest agent/tests/test_brainstorm_nodes.py agent/tests/test_brainstorm.py agent/tests/test_architecture_boundaries.py`
- Runtime-path evidence:
  - A failing required runner reaches `/internal/agent/brainstorm/message` as an error response, not a concluded markdown response.
- Validation:
  - Unit tests for runner success, runner failure, malformed typed output, and finalization payload shape.
- Risks / notes:
  - Make test fakes explicit and small. Do not create a parallel fake production agent framework.
