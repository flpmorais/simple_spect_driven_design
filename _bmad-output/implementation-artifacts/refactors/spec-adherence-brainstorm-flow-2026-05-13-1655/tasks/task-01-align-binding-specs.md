# Task 01: Lock Specification Interpretation

## Implementation Contract

- Objective: Establish a read-only implementation interpretation of PRD, architecture, and project context before source changes. The runner must not edit PRD or architecture; it must fix code/tests to conform to the accepted interpretation.
- Runtime entrypoint: N/A; this task is a pre-implementation audit gate.
- Old owner: Ambiguous split between PRD review requirements and architecture `extract` write description.
- New owner: The implementation plan and tests encode the accepted interpretation: PRD-required review/confirmation gates KG persistence, and architecture wording about `extract` is implemented as theme preparation until explicit confirmation.
- Forbidden implementation patterns: Do not edit `_bmad-output/planning-artifacts/prd.md`; do not edit `_bmad-output/planning-artifacts/architecture.md`; do not edit stale `docs/`; do not weaken requirements to match current code; do not add post-MVP features; do not introduce new frameworks/components.
- Required implementation patterns: Treat PRD review/confirmation requirements as controlling where architecture wording is ambiguous; keep PRD and architecture read-only; record any interpretation in implementation tests and runner summary, not by editing source-of-truth planning docs.
- Compatibility allowed: Additive clarification to internal agent response fields if current public wrapping remains; explicit note that public FastAPI response may wrap the internal agent contract.
- Compatibility forbidden: Any spec text allowing unconfirmed KG writes, swallowed KG errors, direct browser/internal calls, direct agent KG imports, or silent fallback success behavior for required phases.
- Files allowed: No source or planning document edits in this task. The runner may only read `_bmad-output/planning-artifacts/prd.md`, `_bmad-output/planning-artifacts/architecture.md`, and `_bmad-output/project-context.md`.
- Files forbidden: `_bmad-output/planning-artifacts/prd.md`, `_bmad-output/planning-artifacts/architecture.md`, `_bmad-output/project-context.md`, `docs/**`, source code, tests, migrations, generated assets, design-system files.

## Work Items

- Likely files / areas:
  - Read-only: `_bmad-output/planning-artifacts/prd.md` FR17-FR22 and relevant success criteria.
  - Read-only: `_bmad-output/planning-artifacts/architecture.md` orchestration topology, node responsibilities, KG endpoint, validation/finalization behavior, and implementation handoff.
  - Read-only: `_bmad-output/project-context.md` brainstorm agent/KG rules and API response shape rules.
- Subtasks:
  - Read PRD FR17-FR22 and record in the runner summary that FR17/FR18 gate FR21/FR22 for implementation purposes.
  - Read architecture `extract`/validation/markdown sections and record that implementation must satisfy them without violating PRD review/confirmation requirements.
  - Treat aggregate transactional KG finalization as an implementation detail needed to satisfy atomicity and no partial writes, without editing architecture.
  - Record that KG write failures during confirmed finalization must propagate through agent and FastAPI and must not mark a session concluded.
  - Record that required PydanticAI phases must not silently return success-like fallbacks; retries/errors are explicit, tests use fakes.
  - Confirm the internal agent response shape and public FastAPI wrapper distinction by tests in later tasks.

## Completion Checks

- Done when:
  - Runner has read PRD, architecture, and project context before code changes.
  - Runner summary states the controlling interpretation: user-confirmed theme review gates KG persistence and markdown finalization.
  - Runner summary states that PRD and architecture were not edited.
  - Later tasks implement this interpretation in code and tests rather than changing PRD/architecture.
- Evidence required:
  - Manual notes in the runner summary with file references read.
  - Git diff showing no changes to `_bmad-output/planning-artifacts/prd.md` or `_bmad-output/planning-artifacts/architecture.md`.
- Forbidden shortcuts:
  - Editing PRD or architecture.
  - Editing stale `docs/` to appear aligned.
  - Proceeding with code changes while treating architecture wording as permission to bypass PRD review/confirmation.
- Static checks:
  - Confirm no files changed in this task except normal runner execution metadata if the runner workflow maintains it.
  - Confirm PRD and architecture paths have no diff.
- Test commands:
  - No automated tests required for this read-only audit gate; subsequent tasks must include architecture-boundary and lifecycle tests for these rules.
- Runtime-path evidence:
  - N/A for this task.
- Validation:
  - Manual review against accepted decisions D1, D2, and D4, plus revised D3: PRD/architecture are read-only during execution.
- Risks / notes:
  - If implementation cannot satisfy PRD and architecture simultaneously without editing PRD/architecture, stop and report a blocker instead of changing those files.
