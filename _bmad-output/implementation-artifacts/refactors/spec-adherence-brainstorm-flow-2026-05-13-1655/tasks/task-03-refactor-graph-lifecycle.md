# Task 03: Refactor LangGraph Lifecycle, Checkpointing, And Summary

## Implementation Contract

- Objective: Rework brainstorm graph routing and runtime state so the lifecycle follows initiate → facilitate → extract review → user adjustment/confirmation → validate/finalize/markdown, with checkpointed approval pauses and rolling summaries.
- Runtime entrypoint: `invoke_brainstorm_graph()` in `agent/main.py` and `build_brainstorm_graph()` in `agent/brainstorm/graph.py`.
- Old owner: Graph routing advances from conclusion directly to extraction/validation/markdown; state helpers exist but are partly disconnected.
- New owner: LangGraph graph and node functions own phase transitions, approval pauses, resume routing, message/idea/document/summary state, and retry loops.
- Forbidden implementation patterns: No immediate finalization on “done”; no KG writes in unconfirmed extract; no storing business records only in checkpoint state; no routing active facilitate checkpoints through initiate; no hidden in-memory state outside checkpoint.
- Required implementation patterns: LangGraph approval pause represented by persisted phase/state; resume routes based on checkpoint phase; messages appended each turn; ideas reduced/deduped; rolling summary triggered around 20 messages; retry count capped at 2.
- Compatibility allowed: Existing phase label `extract` may represent “theme review pending” if public/backend/frontend contracts remain clear and tested.
- Compatibility forbidden: Adding post-MVP multiple sessions; introducing new persistence outside PostgreSQL checkpointing; direct frontend-to-agent changes.
- Files allowed: `agent/brainstorm/graph.py`, `agent/brainstorm/state.py`, `agent/brainstorm/nodes/*.py`, `agent/main.py`, `agent/checkpoint.py`, `agent/summary.py`, `agent/ideas.py`, agent tests.
- Files forbidden: Backend KG implementation except via later tasks; frontend except via later task; stale `docs/**`.

## Work Items

- Likely files / areas:
  - `agent/brainstorm/graph.py` route functions and conditional edges.
  - `agent/brainstorm/nodes/initiate.py`, `facilitate.py`, `extract.py`, `validate.py`, `markdown.py`.
  - `agent/main.py` request preparation, checkpoint load/save, rolling summary invocation, response construction.
  - `agent/checkpoint.py` active session metadata compatibility.
- Subtasks:
  - Add explicit route handling for active `facilitate`, pending review (`extract` or approved equivalent), `validate`, `markdown`, and `concluded` states.
  - Ensure first message creates session/checkpoint and initiate reads package context through backend HTTP, recommends techniques, and responds without losing state.
  - Ensure technique selection transitions to facilitation and preserves recommendation/technique data.
  - In facilitation, append user/assistant messages, ingest file/url context, reduce new ideas, apply duplicate/contradiction handling, and include anti-bias pivot prompt when triggered.
  - On completion intent, route to extract/theme-preparation and return grouped themes for review with `awaiting_user_input` true; do not validate/finalize/write KG yet.
  - Support review-turn behavior: rename theme, move idea, return to brainstorming, or confirm groupings.
  - On explicit confirmation only, proceed to validation/finalization/markdown.
  - Wire rolling summary update/compaction into runtime after each facilitation/review turn as specified.
  - Preserve completed checkpoints as terminal and ensure status endpoint reports no active session for terminal checkpoints.

## Completion Checks

- Done when:
  - “Done/conclude” returns theme review and does not call KG finalization or produce final markdown.
  - “Looks good/confirm/finalize groupings” from review phase triggers validation/finalization/markdown.
  - Review adjustments persist across checkpoint resume.
  - Active `facilitate` checkpoint resumes at facilitate, not initiate.
  - Rolling summary updates after threshold and compacts messages while preserving total count.
- Evidence required:
  - Graph tests showing route transitions and no immediate finalization.
  - Agent lifecycle tests covering resume from facilitate and review phases.
  - Summary tests showing runtime invocation, not just helper behavior.
- Forbidden shortcuts:
  - Hardcoding response strings without updating graph state.
  - Using only frontend UI state for approval pause.
  - Writing KG in `extract_node` before confirmation.
- Static checks:
  - `extract_node` contains no KG persistence call before confirmation.
  - `route_start` or equivalent handles all active phases including `facilitate`.
- Test commands:
  - `pytest agent/tests/test_brainstorm_graph.py agent/tests/test_brainstorm.py agent/tests/test_brainstorm_nodes.py`
- Runtime-path evidence:
  - A full fake-runner flow demonstrates initiate → facilitate → extract review → confirm → concluded.
- Validation:
  - Include tests for invalid/no-ideas validation path returning to facilitation with retry cap.
- Risks / notes:
  - If existing checkpoints have old phases, route them conservatively and test compatibility.
