---
workflow: bmad-deferred
id: DW-0011
status: done
source: Deferred from: code review of 1-2-backend-infrastructure-user-authentication (2026-05-07)
createdAt: 2026-05-12-1350
updatedAt: 2026-05-12-0000
---

# Deferred Work Plan: DW-0011 IntegrityError Retry Path Untested

## Raw Item

IntegrityError retry path untested — concurrent-insert edge case for `get_or_create_user`.

## Understanding

`get_or_create_user()` first selects by `google_id`, inserts if missing, and catches `IntegrityError` from `db.commit()` to handle a concurrent insert. The catch branch rolls back, re-selects by `google_id`, and returns the existing user. Existing tests cover normal create/find behavior but not this race-handling branch.

## Decision

Approved plan-work. Add focused coverage for the retry branch without broad auth refactoring.

## Plan

### Tasks

#### 1. Add retry-path coverage for `get_or_create_user`

- Objective: Prove the `IntegrityError` branch rolls back, re-selects by `google_id`, and returns the existing user for a concurrent insert race.
- Likely files / areas:
  - `thagid/tests/test_auth.py`
  - `thagid/services/auth.py` only if the test exposes a real defect.
- Subtasks:
  - Add a focused async test that simulates an `IntegrityError` on commit after the initial lookup returns no user.
  - Assert rollback is called before the second lookup returns the existing user.
  - Keep the test scoped to the concurrent same-`google_id` retry path, not duplicate email with a different Google ID.
- Tests to update/add:
  - Add one pytest async test in `thagid/tests/test_auth.py`.
- Validation:
  - `pytest thagid/tests/test_auth.py`
  - If service code changes, run the relevant auth/middleware tests.
- Risks / notes:
  - Coordinate with DW-0013 during execution because both touch `get_or_create_user()`, but the behaviors are distinct.

## Execution Record

- 2026-05-12: Execution started by `bmad-deferred-run`.
- 2026-05-12: Added focused async coverage for the `get_or_create_user()` `IntegrityError` retry branch. The test simulates the initial miss, commit failure, rollback, and successful second lookup for the same `google_id`.
- Files changed:
  - `thagid/tests/test_auth.py`
  - `_bmad-output/implementation-artifacts/deferred-work-tracker.md`
  - `_bmad-output/implementation-artifacts/deferred/deferred-DW-0011-integrityerror-retry-path-untested.md`
- Final validation:
  - `pytest thagid/tests/test_auth.py` — passed (12 passed)
- Commit: `255343a` (`Complete deferred work DW-0011`)
- Push: pushed to upstream branch `origin/1_datapipeline`
