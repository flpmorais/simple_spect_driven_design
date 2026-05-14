---
workflow: bmad-deferred
id: DW-0051
status: done
source: Deferred from: code review of 1-1-brainstorm-runtime-foundation (2026-05-09)
createdAt: 2026-05-12-1507
updatedAt: 2026-05-12-1515
---

# Deferred Work Plan: DW-0051 DATABASE_URL Is Not URL-encoded

## Raw Item

`DATABASE_URL` not URL-encoded — special chars in password break connection string. Same pre-existing pattern in `thagid/config.py`. [agent/config.py:15-16]

## Understanding

Both backend and agent settings build PostgreSQL connection strings by interpolating raw user/password/database values into URLs. If credentials contain reserved URL characters such as `@`, `:`, `/`, or `#`, the generated connection URL can be parsed incorrectly. This is a configuration robustness issue across both services.

## Decision

Approved plan-work. Encode database URL components in backend and agent config while preserving existing defaults and connection behavior.

## Plan

### Tasks

#### 1. URL-encode database connection components

- Objective: Build valid database URLs even when credentials or database names contain URL-reserved characters.
- Likely files / areas:
  - `agent/config.py`
  - `thagid/config.py`
  - Existing config tests, or new focused tests if none exist.
- Subtasks:
  - Use Python standard-library URL quoting for username, password, and database components.
  - Preserve existing URL schemes: backend `postgresql+asyncpg://`, agent `postgresql://`.
  - Keep host/port behavior unchanged.
  - Avoid introducing new dependencies.
- Tests to update/add:
  - Add focused tests asserting default URLs remain unchanged.
  - Add focused tests asserting special characters in credentials are percent-encoded.
  - Cover both backend `Settings.DATABASE_URL` and agent `AgentSettings.DATABASE_URL`.
- Validation:
  - `pytest thagid/tests` focused config test if added.
  - `pytest agent/tests` focused config test if added.
- Risks / notes:
  - Ensure tests instantiate settings objects directly rather than mutating global settings where possible.

## Execution Record

- Implemented URL encoding with Python standard-library `urllib.parse.quote` for PostgreSQL username, password, and database components in both backend and agent settings.
- Preserved existing backend `postgresql+asyncpg://` and agent `postgresql://` URL schemes plus host/port behavior.
- Added focused backend and agent config tests covering unchanged default URLs and percent-encoding of reserved characters.

### Files Changed

- `agent/config.py`
- `agent/tests/test_config.py`
- `thagid/config.py`
- `thagid/tests/test_config.py`
- `_bmad-output/implementation-artifacts/deferred-work-tracker.md`
- `_bmad-output/implementation-artifacts/deferred/deferred-DW-0051-database-url-not-url-encoded.md`

### Validation Log

- `pytest thagid/tests/test_config.py` — passed
- `pytest agent/tests/test_config.py` — passed

### Commit And Push

- Commit: `4074623`
- Push: `git push` to `origin/1_datapipeline` — succeeded
