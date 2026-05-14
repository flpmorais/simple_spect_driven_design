---
workflow: bmad-deferred
id: DW-0034
status: done
source: Deferred from: code review of 4-1-package-creation (2026-05-07)
createdAt: 2026-05-12-1428
updatedAt: 2026-05-12-1558
---

# Deferred Work Plan: DW-0034 Missing Accessibility Attributes on Validation Errors

## Raw Item

No accessibility attributes on validation errors — `<p>` error elements lack `aria-describedby`/`aria-invalid`. Pre-existing pattern across all forms. [+page.svelte:62-63,75-76]

## Understanding

Several Svelte forms render validation errors visually and change border styling, but inputs/textareas are not marked invalid and are not linked to the error text. This makes validation feedback less accessible to assistive technologies.

## Decision

Approved plan-work. Add minimal accessibility attributes to current validation-error patterns.

## Plan

### Tasks

#### 1. Add `aria-invalid` and `aria-describedby` to form validation fields

- Objective: Connect visible validation errors to their controls without changing form behavior.
- Likely files / areas:
  - `web/src/routes/project/[id]/package/create/+page.svelte`
  - `web/src/routes/org/create-project/+page.svelte`
  - `web/src/routes/project/[id]/settings/+page.svelte`
  - `web/src/routes/org/create/+page.svelte` if applying the same pattern to the single-error org creation form is straightforward.
- Subtasks:
  - Add stable IDs to error text elements.
  - Set `aria-invalid` based on the corresponding validation error state.
  - Set `aria-describedby` only when error text is present, or in a Svelte-safe equivalent pattern.
  - Preserve current visual styling and validation messages.
- Tests to update/add:
  - Add or update focused frontend tests if a suitable component/page test pattern exists.
  - Otherwise rely on Svelte check/build validation and document the lack of component-level tests.
- Validation:
  - `npm run check` from `web/` if available.
  - `npm test -- --run` from `web/` or the repository's established Vitest command.
- Risks / notes:
  - Do not refactor forms wholesale; keep the accessibility changes surgical.

## Execution Record

- Added conditional `aria-invalid` and `aria-describedby` attributes to validation fields on package creation, project creation, project settings, and organisation creation forms.
- Added stable IDs to rendered validation error text and preserved existing validation messages and visual styling.
- No component-level page test pattern exists for these route pages; validation used configured frontend check and unit test commands.
- Validation passed: `npm run check` from `web/`.
- Validation passed: `npm run test:unit` from `web/`.
- Commit: `0e22aa8` (`Complete deferred work DW-0034`).
- Push: `git push` to `origin/1_datapipeline` succeeded.
- Files changed:
  - `web/src/routes/project/[id]/package/create/+page.svelte`
  - `web/src/routes/org/create-project/+page.svelte`
  - `web/src/routes/project/[id]/settings/+page.svelte`
  - `web/src/routes/org/create/+page.svelte`
