---
workflow: bmad-deferred
id: DW-0037
status: done
source: Deferred from: code review of 4-1-package-creation (2026-05-07)
createdAt: 2026-05-12-1453
updatedAt: 2026-05-12-1604
---

# Deferred Work Plan: DW-0037 Double Error Toast on 5xx Responses

## Raw Item

Double error toast on 5xx responses — `apiFetch` already toasts on 5xx (client.ts:30), page's catch block toasts again. Pre-existing pattern across all forms. [+page.svelte:41]

## Understanding

The shared frontend API client shows a generic toast for 5xx responses. Form pages also catch errors and show a toast, so a single server failure can produce duplicate notifications. This is a user-facing behavior issue and likely affects more than package creation.

## Decision

Approved plan-work. Prevent duplicate 5xx toasts with a minimal shared/client-side pattern while preserving useful form-level error messages for non-5xx errors.

## Plan

### Tasks

#### 1. Distinguish API-client-toasted server errors from form-displayable errors

- Objective: Avoid duplicate user-facing toasts when `apiFetch()` has already handled a 5xx response.
- Likely files / areas:
  - `web/src/lib/api/client.ts`
  - `web/src/routes/project/[id]/package/create/+page.svelte`
  - Potentially other form pages if the duplicate-toast pattern is shared and simple to update consistently.
- Subtasks:
  - Add a minimal error type or flag for 5xx errors that have already shown a global toast.
  - Update package creation catch handling to skip an extra toast for that error type.
  - Consider applying the same skip pattern to nearby create/update form pages if they share identical behavior and the change stays surgical.
  - Preserve current 401 and non-5xx behavior.
- Tests to update/add:
  - Add or update focused frontend unit tests for `apiFetch()` error behavior if a suitable pattern exists.
  - Add page/form tests only if existing infrastructure supports page component testing without broad setup changes.
- Validation:
  - `npm test -- --run` from `web/` or the repository's established Vitest command.
  - `npm run check` from `web/` if available.
- Risks / notes:
  - Avoid suppressing non-5xx validation errors; those should remain visible to users.

## Execution Record

- Added `ServerError` and `isServerError()` in `web/src/lib/api/client.ts` so 5xx responses remain globally toasted by `apiFetch()` and are distinguishable by callers.
- Updated create/update form catch handlers to skip local duplicate toasts or inline error display for `ServerError` while preserving 401 and non-5xx caller behavior.
- Added focused Vitest coverage in `web/src/lib/api/client.test.ts` for globally-toasted 5xx errors and non-5xx caller-displayable errors.
- Files changed:
  - `web/src/lib/api/client.ts`
  - `web/src/lib/api/client.test.ts`
  - `web/src/routes/project/[id]/package/create/+page.svelte`
  - `web/src/routes/org/create-project/+page.svelte`
  - `web/src/routes/org/create/+page.svelte`
  - `web/src/routes/project/[id]/settings/+page.svelte`
  - `web/src/routes/org/settings/+page.svelte`
- Validation:
  - `npm run test:unit -- src/lib/api/client.test.ts` from `web/` — passed (2 tests).
  - `npm run test:unit` from `web/` — passed (12 files, 49 tests).
  - `npm run check` from `web/` — passed with 0 errors and 0 warnings.
- Commit: `2a597d7da86678976fb4c2888343d76168509874` (`Complete deferred work DW-0037`).
- Push: `git push` to `origin/1_datapipeline` succeeded.
