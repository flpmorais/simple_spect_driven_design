---
workflow: bmad-deferred
id: DW-0010
status: done
source: Deferred from: code review of 1-2-backend-infrastructure-user-authentication (2026-05-07)
createdAt: 2026-05-12-1353
updatedAt: 2026-05-12-0000
---

# Deferred Work Plan: DW-0010 ValueError Domain Exception Pattern

## Raw Item

`ValueError` used as domain exception instead of custom exception types — refactor when error handling grows.

## Understanding

The auth service currently uses generic `ValueError` for user/auth domain failures such as invalid Google tokens, audience mismatch, incomplete token data, and missing JWT subject claims. The project context says services should raise domain exceptions and routers should map them to HTTP status. Generic `ValueError` works today but makes auth failures harder to distinguish from programmer errors and from future account-linking conflicts.

## Decision

Approved plan-work. Implement a small auth-focused domain exception refactor, not a broad cross-service error architecture cleanup.

## Plan

### Tasks

#### 1. Introduce auth-specific domain exceptions

- Objective: Replace generic auth `ValueError` cases with explicit exception types while preserving current HTTP behavior.
- Likely files / areas:
  - `thagid/services/auth.py`
  - `thagid/routers/auth.py`
  - `thagid/tests/test_auth.py`
  - `thagid/tests/test_middleware.py`
- Subtasks:
  - Add minimal auth exception classes near the auth service, such as a base `AuthError` plus specific exceptions only where they clarify behavior.
  - Update `verify_google_token()` and `decode_jwt()` auth-domain failures to raise auth-specific exceptions instead of `ValueError`.
  - Update `auth_callback()` to catch the auth-specific exception family and keep returning the same intentional HTTP status/details for existing cases.
  - Avoid refactoring unrelated service modules in this deferred item.
- Tests to update/add:
  - Update existing service tests that currently expect `ValueError` to expect the new auth exception type.
  - Keep auth callback integration tests passing with the same response status/details.
- Validation:
  - `pytest thagid/tests/test_auth.py thagid/tests/test_middleware.py`
- Risks / notes:
  - Coordinate with DW-0013 because duplicate-email handling may add or reuse an auth/account conflict exception.

## Execution Record

- Implemented `AuthError`, `GoogleTokenError`, and `JwtSubjectError` in `thagid/services/auth.py`.
- Updated Google token and JWT subject domain failures to raise auth-specific exceptions.
- Updated auth router and middleware mappings to preserve existing HTTP behavior.
- Updated tests to assert auth-specific service exceptions and added missing incomplete-token/missing-subject coverage.
- Files changed: `thagid/services/auth.py`, `thagid/routers/auth.py`, `thagid/middleware/auth.py`, `thagid/tests/test_auth.py`, `_bmad-output/implementation-artifacts/deferred-work-tracker.md`, `_bmad-output/implementation-artifacts/deferred/deferred-DW-0010-valueerror-domain-exception-pattern.md`.
- Validation: `pytest thagid/tests/test_auth.py thagid/tests/test_middleware.py` — passed (17 tests).
- Commit: `983b01e`.
- Push: pushed to `origin/1_datapipeline`.
