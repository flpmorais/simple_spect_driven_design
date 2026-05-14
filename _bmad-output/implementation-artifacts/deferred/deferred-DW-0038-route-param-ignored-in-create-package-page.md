---
workflow: bmad-deferred
id: DW-0038
status: done
source: Deferred from: code review of 4-1-package-creation (2026-05-07)
createdAt: 2026-05-12-1453
updatedAt: 2026-05-12-1611
---

# Deferred Work Plan: DW-0038 Route Param Ignored in Create Package Page

## Raw Item

URL route param [id] ignored in favor of scope store — page at `/project/[id]/package/create` never reads URL param. Pre-existing architectural pattern. [+page.svelte:33]

## Understanding

The package creation page is routed under `/project/[id]/package/create`, but it currently uses `$scope.project?.id` when creating the package and building the return URL. Project context says URL params drive scope resolution, so route-level actions should use the URL project ID instead of relying solely on the scope store being initialized and current.

## Decision

Approved plan-work. Use the route project ID parameter for package creation while preserving current scope/store behavior elsewhere.

## Plan

### Tasks

#### 1. Use route project ID in package creation

- Objective: Make package creation derive `project_id` from the route parameter, avoiding stale or missing scope issues.
- Likely files / areas:
  - `web/src/routes/project/[id]/package/create/+page.svelte`
  - Existing frontend tests if suitable page tests exist.
- Subtasks:
  - Read the route project ID from SvelteKit page params.
  - Use that ID for `createPackage({ project_id })` and navigation targets.
  - Keep user feedback for genuinely missing route IDs, if needed.
  - Remove unused imports or scope reads only if this page no longer needs them.
- Tests to update/add:
  - Add/update a focused frontend test if page component testing exists.
  - Otherwise validate through Svelte check/build.
- Validation:
  - `npm run check` from `web/` if available.
  - `npm test -- --run` from `web/` or the repository's established Vitest command.
- Risks / notes:
  - Do not alter backend authorization; backend still verifies package/project access.

## Execution Record

- Status updated to `in-progress` before implementation.
- Implemented `web/src/routes/project/[id]/package/create/+page.svelte` to read the project ID from `page.params.id` and use it for package creation, success navigation, and cancel navigation.
- Removed the now-unused scope store import from the package creation page.
- No focused component test existed for this route, so validation used the established frontend checks.
- Validation passed: `npm run check` from `web/`.
- Validation passed: `npm run test:unit` from `web/`.

Files changed:

- `web/src/routes/project/[id]/package/create/+page.svelte`
- `_bmad-output/implementation-artifacts/deferred/deferred-DW-0038-route-param-ignored-in-create-package-page.md`
- `_bmad-output/implementation-artifacts/deferred-work-tracker.md`

Commit and push:

- Implementation commit: `e79aec4` (`Complete deferred work DW-0038`).
- Push result: pushed successfully to `origin/1_datapipeline`.
