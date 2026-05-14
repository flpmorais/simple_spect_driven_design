---
workflow: bmad-deferred
id: DW-0030
status: done
source: Deferred from: code review of 3-3-project-dashboard-package-list (2026-05-07)
createdAt: 2026-05-12-1428
updatedAt: 2026-05-12-1549
---

# Deferred Work Plan: DW-0030 NotFoundError Pattern Fragility

## Raw Item

NotFoundError pattern fragility across services (bare Exception per module) — pre-existing architectural concern, defer to refactor cycle.

## Understanding

Several backend service modules define local exception classes with the same `NotFoundError` name. Routers avoid ambiguity by aliasing imports, but each class is a distinct exception type. This works today, yet it is fragile as service exceptions grow because catch behavior depends on the originating module and repeated local names make mistakes easier.

## Decision

Approved plan-work. Perform a narrow backend service exception cleanup for NotFoundError-style exceptions without changing HTTP behavior or broad service architecture.

## Plan

### Tasks

#### 1. Introduce shared service exceptions for not-found errors

- Objective: Replace repeated bare `NotFoundError` classes with a shared exception pattern that remains explicit in routers.
- Likely files / areas:
  - `thagid/services/exceptions.py` or similar focused service exception module
  - `thagid/services/project.py`
  - `thagid/services/package.py`
  - `thagid/services/brief.py`
  - `thagid/services/organisation.py`
  - Routers/tests importing service `NotFoundError` classes
- Subtasks:
  - Add a shared `ServiceError`/`NotFoundError` base or small set of resource-specific shared exceptions.
  - Update service modules to import/use the shared not-found exception type instead of redefining local bare classes.
  - Update router imports/catches while preserving existing status codes and response details.
  - Keep this change separate from auth-specific exception work in DW-0010 unless execution intentionally coordinates both.
- Tests to update/add:
  - Update imports in existing backend tests that refer to service-specific not-found classes.
  - Add a focused assertion only if needed to verify exception identity/import behavior.
- Validation:
  - `pytest thagid/tests/test_projects.py thagid/tests/test_packages.py thagid/tests/test_briefs.py thagid/tests/test_orgs.py`
  - Run any KG/brainstorm tests that mock project/package not-found exceptions if imports change.
- Risks / notes:
  - Avoid changing router HTTP responses; this is an exception organization refactor, not an API behavior change.

## Execution Record

Completed by `bmad-deferred-run` on 2026-05-12.

- Added `thagid/services/exceptions.py` with shared `ServiceError` and `NotFoundError` service exceptions.
- Updated project, package, brief, and organisation services to use the shared `NotFoundError` while preserving existing service-module import paths used by routers and tests.
- Added focused coverage that verifies service modules share the same not-found exception type.
- Files changed:
  - `thagid/services/exceptions.py`
  - `thagid/services/project.py`
  - `thagid/services/package.py`
  - `thagid/services/brief.py`
  - `thagid/services/organisation.py`
  - `thagid/tests/test_projects.py`
  - `_bmad-output/implementation-artifacts/deferred-work-tracker.md`
  - `_bmad-output/implementation-artifacts/deferred/deferred-DW-0030-notfounderror-pattern-fragility.md`
- Validations:
  - `pytest thagid/tests/test_projects.py thagid/tests/test_packages.py thagid/tests/test_briefs.py thagid/tests/test_orgs.py` — passed, 42 tests.
  - `pytest thagid/tests/test_kg.py thagid/tests/test_brainstorm.py` — passed, 92 tests.
- Commit: `c31f6b8` (`Complete deferred work DW-0030`).
- Push: pushed to upstream branch `origin/1_datapipeline`.
