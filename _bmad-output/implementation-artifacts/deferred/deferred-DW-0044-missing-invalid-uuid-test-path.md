---
workflow: bmad-deferred
id: DW-0044
status: done
source: Deferred from: code review of 4-2-chat-interface-echo-service (2026-05-08)
createdAt: 2026-05-12-1459
updatedAt: 2026-05-12
---

# Deferred Work Plan: DW-0044 Missing invalid-UUID Test Path

## Raw Item

No test for invalid-UUID 422 path — verify_package_access returns 422 on ValueError but all tests use valid UUIDs. [test_messages.py]

## Understanding

`verify_package_access()` catches `ValueError` from package ID parsing and returns a 422 HTTP error. Existing message endpoint tests cover success, empty content validation, package not found, authorization, and auth-required behavior, but not malformed package IDs.

## Decision

Approved plan-work. Add focused backend tests for malformed package IDs on message endpoints.

## Plan

### Tasks

#### 1. Cover invalid package UUID behavior in message endpoint tests

- Objective: Ensure malformed package IDs return 422 for message list/create paths.
- Likely files / areas:
  - `thagid/tests/test_messages.py`
  - `thagid/routers/messages.py` only if the test reveals a mismatch.
- Subtasks:
  - Add a test for `GET /api/packages/not-a-uuid/messages` with auth cookies expecting 422.
  - Add a test for `POST /api/packages/not-a-uuid/messages` with auth cookies expecting 422.
  - Keep existing not-found tests using valid UUIDs.
- Tests to update/add:
  - Add one or two focused pytest async tests in `thagid/tests/test_messages.py`.
- Validation:
  - `pytest thagid/tests/test_messages.py`
- Risks / notes:
  - Coordinate with DW-0042 if message route signatures change for pagination.

## Execution Record

- Implemented by `bmad-deferred-run` on 2026-05-12.
- Files changed:
  - `thagid/tests/test_messages.py`
  - `_bmad-output/implementation-artifacts/deferred-work-tracker.md`
  - `_bmad-output/implementation-artifacts/deferred/deferred-DW-0044-missing-invalid-uuid-test-path.md`
- Validation:
  - `pytest thagid/tests/test_messages.py` — passed (12 tests).
- Commit: `0ab879b` (`Complete deferred work DW-0044`).
- Push: pushed to upstream branch `origin/1_datapipeline`.
