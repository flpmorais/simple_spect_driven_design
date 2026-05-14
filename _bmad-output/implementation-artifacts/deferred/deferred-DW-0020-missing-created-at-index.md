---
workflow: bmad-deferred
id: DW-0020
status: done
source: Deferred from: code review of 2-2-org-dashboard-project-cards (2026-05-07)
createdAt: 2026-05-12-1401
updatedAt: 2026-05-12-1401
---

# Deferred Work Plan: DW-0020 Missing created_at Index for Ordering

## Raw Item

No index on created_at used in ORDER BY — premature optimization for prototype. [thagid/services/project.py:35]

## Understanding

`list_projects_by_org()` queries projects by `org_id` and orders by `Project.created_at.desc()`. The model currently indexes `org_id`, but there is no index that directly supports the ordering column. At small prototype scale this is not a correctness issue, but the user approved fixing it.

## Decision

Approved plan-work. Add a minimal index for project list ordering without changing endpoint behavior.

## Plan

### Tasks

#### 1. Add project ordering index

- Objective: Add database support for listing projects ordered by creation time.
- Likely files / areas:
  - `thagid/models/project.py`
  - `migrations/versions/`
  - `thagid/tests/` if migration/model shape tests exist or are straightforward.
- Subtasks:
  - Determine the next Alembic migration revision and add an index on `projects.created_at`, or a composite index on `(org_id, created_at)` if that better matches the current query shape.
  - Keep the service query behavior unchanged.
  - Reflect the index in the SQLAlchemy model if the project convention keeps model indexes declared there.
- Tests to update/add:
  - Add or update a focused test that verifies the model/migration defines the intended index, following existing migration-shape test patterns.
- Validation:
  - `pytest thagid/tests/test_projects.py`
  - Run any focused migration/model test file updated by the change.
- Risks / notes:
  - Avoid broad performance refactors; this deferred item is only about the index.

## Execution Record

- Added `ix_projects_org_id_created_at` as a composite SQLAlchemy model index on `(org_id, created_at)` to support the existing organisation-scoped descending creation-time project list query.
- Added Alembic revision `009_add_projects_org_created_at_index.py` to create and drop the matching database index.
- Added focused model-shape coverage in `thagid/tests/test_projects.py` for the composite index definition.
- Validations run:
  - `pytest thagid/tests/test_projects.py` — 13 passed.
  - `python -m py_compile migrations/versions/009_add_projects_org_created_at_index.py` — passed.
- Files changed:
  - `thagid/models/project.py`
  - `migrations/versions/009_add_projects_org_created_at_index.py`
  - `thagid/tests/test_projects.py`
  - `_bmad-output/implementation-artifacts/deferred-work-tracker.md`
  - `_bmad-output/implementation-artifacts/deferred/deferred-DW-0020-missing-created-at-index.md`
- Commit: `cd36b1f` (`Complete deferred work DW-0020`).
- Push result: pushed to `origin/1_datapipeline`.
