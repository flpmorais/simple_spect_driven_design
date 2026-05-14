---
workflow: bmad-deferred
id: DW-0013
status: done
source: Deferred from: code review of 1-3-sign-in-page-application-shell (2026-05-07)
createdAt: 2026-05-12-1350
updatedAt: 2026-05-12-1350
---

# Deferred Work Plan: DW-0013 Duplicate-email IntegrityError Crash

## Raw Item

`get_or_create_user` crashes on duplicate-email IntegrityError from a different `google_id` — the `except IntegrityError` handler re-selects by `google_id` which doesn't exist, causing unhandled `NoResultFound`. Pre-existing from story 1-2.

## Understanding

`users.email` and `users.google_id` are both unique. When a sign-in arrives with an email that already exists under a different Google ID, the insert can fail on the email constraint. The current retry handler assumes the failure was caused by another process creating the same `google_id`, so it re-selects by `google_id` and calls `scalar_one()`. For a duplicate-email/different-Google-ID conflict, no row exists for the new `google_id`, so the handler can raise an unhandled exception and return a 500.

## Decision

Approved plan-work. Fix duplicate-email handling so auth fails predictably instead of crashing.

## Plan

### Tasks

#### 1. Add regression coverage for duplicate email with different Google ID

- Objective: Reproduce the crash scenario before changing behavior.
- Likely files / areas:
  - `thagid/tests/test_auth.py`
  - `thagid/tests/test_middleware.py` if covering through `/api/auth/callback`.
- Subtasks:
  - Seed an existing user with `email="same@example.com"` and `google_id="existing-google-id"`.
  - Attempt `get_or_create_user()` or auth callback with the same email and a different `google_id`.
  - Assert a controlled domain/auth failure instead of `NoResultFound` or a 500.
- Tests to update/add:
  - Add a service-level regression test; add route-level coverage if the chosen error mapping changes router behavior.
- Validation:
  - `pytest thagid/tests/test_auth.py`
  - `pytest thagid/tests/test_middleware.py` if route behavior is covered.
- Risks / notes:
  - Exact exception/status mapping should stay minimal and consistent with the current auth router unless DW-0010 is approved as a broader domain-exception refactor.

#### 2. Implement controlled duplicate-email handling

- Objective: Keep the concurrent same-`google_id` retry behavior while detecting email conflicts with a different Google ID.
- Likely files / areas:
  - `thagid/services/auth.py`
  - `thagid/routers/auth.py` only if a new exception type or message needs explicit HTTP mapping.
- Subtasks:
  - In the `IntegrityError` handler, after rollback, re-select by `google_id` using `scalar_one_or_none()` instead of assuming a match.
  - If no `google_id` match exists, check for an existing row by email and raise a controlled auth/domain error for the account-linking conflict.
  - Avoid a broad service exception architecture refactor unless DW-0010 is approved.
- Tests to update/add:
  - Ensure the new duplicate-email test fails before the fix and passes after it.
  - Keep DW-0011 retry-path coverage passing.
- Validation:
  - `pytest thagid/tests/test_auth.py thagid/tests/test_middleware.py`
- Risks / notes:
  - Be careful not to treat legitimate concurrent same-`google_id` insert races as duplicate-email account conflicts.

## Execution Record

- 2026-05-12: Implemented controlled duplicate-email handling in `get_or_create_user()` by preserving the same-`google_id` IntegrityError retry path, checking for email ownership conflicts, and raising `AccountConflictError` instead of leaking `NoResultFound`/500 behavior.
- 2026-05-12: Updated `/api/auth/callback` to map auth service errors from user creation to HTTP 401 responses.
- Files changed: `thagid/services/auth.py`, `thagid/routers/auth.py`, `thagid/tests/test_auth.py`, `thagid/tests/test_middleware.py`, `_bmad-output/implementation-artifacts/deferred-work-tracker.md`, `_bmad-output/implementation-artifacts/deferred/deferred-DW-0013-duplicate-email-integrityerror-crash.md`.
- Validation: `pytest thagid/tests/test_auth.py thagid/tests/test_middleware.py` — 20 passed.
- Commit: `484cfe2` (`Complete deferred work DW-0013`).
- Push: pushed `1_datapipeline` to upstream `origin/1_datapipeline`.
