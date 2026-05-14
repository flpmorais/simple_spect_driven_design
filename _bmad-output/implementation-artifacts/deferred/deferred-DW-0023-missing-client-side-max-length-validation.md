---
workflow: bmad-deferred
id: DW-0023
status: done
source: Deferred from: code review of 3-1-project-crud-github-configuration (2026-05-07)
createdAt: 2026-05-12-1401
updatedAt: 2026-05-12-1538
---

# Deferred Work Plan: DW-0023 Missing Client-side max_length Validation

## Raw Item

No client-side max_length validation — backend returns 422 handled by generic toast. Not required by spec. [both form pages]

## Understanding

Project create/settings forms validate only required fields. Backend schemas enforce `name` max length 255 and GitHub URL max length 500. The user approved adding client-side max-length checks for better UX while preserving backend validation as the source of truth.

## Decision

Approved plan-work. Add minimal client-side max-length validation to project create and settings forms.

## Plan

### Tasks

#### 1. Add max-length validation to project forms

- Objective: Show immediate form errors when project fields exceed backend limits.
- Likely files / areas:
  - `web/src/routes/org/create-project/+page.svelte`
  - `web/src/routes/project/[id]/settings/+page.svelte`
  - Existing or new co-located Vitest tests if component/form tests are present.
- Subtasks:
  - Add client validation for `name` length <= 255.
  - Add client validation for `githubProjectUrl` and `githubRepoUrl` length <= 500.
  - Avoid changing backend schema behavior or adding new libraries.
  - Keep existing required-field messages and submit flow intact.
- Tests to update/add:
  - Add or update focused frontend unit tests for over-limit validation if the project has a suitable existing pattern for Svelte page tests.
  - If no suitable component test pattern exists, validate with frontend type/test commands and document the limitation in the execution record.
- Validation:
  - `npm test -- --run` from `web/` or the repository's established Vitest command.
  - `npm run check` from `web/` if available.
- Risks / notes:
  - Do not introduce schema-validation libraries; keep the change surgical.

## Execution Record

- Status updated to in-progress and tracker DW-0023 marked in-progress before implementation.
- Added client-side max-length checks to the create-project and project-settings forms for project name (255 characters) and GitHub project/repo URLs (500 characters), preserving existing required-field validation and submit flow.
- No page/component test pattern exists for Svelte route form validation in this project; no new component test was added.
- Files changed:
  - `web/src/routes/org/create-project/+page.svelte`
  - `web/src/routes/project/[id]/settings/+page.svelte`
  - `_bmad-output/implementation-artifacts/deferred-work-tracker.md`
  - `_bmad-output/implementation-artifacts/deferred/deferred-DW-0023-missing-client-side-max-length-validation.md`
- Final validation:
  - `npm run test:unit` from `web/`: passed, 11 files / 47 tests.
  - `npm run check` from `web/`: passed, 0 errors / 0 warnings.
- Commit: `10b3477` (`Complete deferred work DW-0023`).
- Push: `git push` to `origin/1_datapipeline` succeeded.
