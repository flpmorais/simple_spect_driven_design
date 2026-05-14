---
workflow: bmad-deferred
id: DW-0012
status: done
source: Deferred from: code review of 1-2-backend-infrastructure-user-authentication (2026-05-07)
createdAt: 2026-05-12-1350
updatedAt: 2026-05-12-0000
---

# Deferred Work Plan: DW-0012 Cookie Attributes Not Asserted

## Raw Item

Cookie attributes (`httponly`, `secure`, `samesite`, `max_age`) not asserted in integration tests.

## Understanding

`auth_callback()` sets the `thagid_session` cookie with `httponly=True`, `secure=True`, `samesite="lax"`, and `max_age=604800`. Existing integration coverage checks that the cookie exists, but does not assert the security attributes.

## Decision

Approved plan-work. Extend auth callback integration coverage for cookie security attributes.

## Plan

### Tasks

#### 1. Assert session cookie security attributes

- Objective: Ensure auth callback tests fail if HTTP-only, secure, SameSite, or max-age attributes regress.
- Likely files / areas:
  - `thagid/tests/test_middleware.py` or `thagid/tests/test_auth.py`
  - `thagid/routers/auth.py` only if the test exposes a regression.
- Subtasks:
  - Extend the existing `test_auth_callback_success` integration test or add a focused test for `Set-Cookie` attributes.
  - Assert the raw `set-cookie` header contains `HttpOnly`, `Secure`, `SameSite=lax`, and `Max-Age=604800`.
  - Keep signout behavior separate unless existing assertions need minor alignment.
- Tests to update/add:
  - Update/add one auth callback integration test.
- Validation:
  - `pytest thagid/tests/test_middleware.py`
  - Optionally `pytest thagid/tests/test_auth.py` if the test is placed there.
- Risks / notes:
  - Header casing may vary by framework; use case-insensitive checks where appropriate while preserving exact semantic assertions.

## Execution Record

- 2026-05-12: Execution started by `bmad-deferred-run`.
- 2026-05-12: Extended `test_auth_callback_success` to assert the `thagid_session` `Set-Cookie` header includes `HttpOnly`, `Secure`, `SameSite=lax`, and `Max-Age=604800`.
- 2026-05-12: Validation passed: `pytest thagid/tests/test_middleware.py` (6 passed).
- 2026-05-12: Committed implementation as `0802072` and pushed to `origin/1_datapipeline`.

## Files Changed

- `thagid/tests/test_middleware.py`
- `_bmad-output/implementation-artifacts/deferred/deferred-DW-0012-cookie-attributes-not-asserted.md`
- `_bmad-output/implementation-artifacts/deferred-work-tracker.md`
