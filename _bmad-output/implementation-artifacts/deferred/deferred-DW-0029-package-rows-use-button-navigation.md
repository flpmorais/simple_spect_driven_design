---
workflow: bmad-deferred
id: DW-0029
status: done
source: Deferred from: code review of 3-3-project-dashboard-package-list (2026-05-07)
createdAt: 2026-05-12-1422
updatedAt: 2026-05-12-1543
---

# Deferred Work Plan: DW-0029 Package Rows Use Button Navigation

## Raw Item

Package rows use `<button>` + `goto()` instead of `<a href>` — pre-existing accessibility pattern, not introduced by this change.

## Understanding

The project dashboard renders each package row as a button and navigates with `goto()`. Since the row is a navigation target, link semantics are more appropriate for accessibility, browser affordances, and expected keyboard/context-menu behavior.

## Decision

Approved plan-work. Replace package row button navigation with link semantics while preserving visual styling and behavior.

## Plan

### Tasks

#### 1. Convert package row navigation to link semantics

- Objective: Make package rows navigational links instead of buttons that imperatively call `goto()`.
- Likely files / areas:
  - `web/src/routes/project/[id]/+page.svelte`
  - Existing or new co-located frontend tests if a suitable route/component test pattern exists.
- Subtasks:
  - Replace the package row `<button>` with an `<a href="/project/{projectId}/package/{pkg.id}">` or equivalent link-capable project component.
  - Preserve row layout, hover styling, status badge display, and keyboard focus visibility.
  - Remove now-unused `goto` import only if this change makes it unused in the file.
  - Avoid changing unrelated package/dashboard behavior.
- Tests to update/add:
  - Add or update a focused frontend test if a suitable pattern exists.
  - At minimum, rely on Svelte check/build validation if no established page component test exists.
- Validation:
  - `npm run check` from `web/` if available.
  - `npm test -- --run` from `web/` or the repository's established Vitest command.
- Risks / notes:
  - Ensure nested interactive content is not introduced inside the anchor.

## Execution Record

- 2026-05-12: Converted project dashboard package rows from `<button>` plus imperative `goto()` navigation to anchor links with matching layout, hover styling, and visible focus ring styling.
- Tests: No co-located page/component test pattern exists for route pages, so no focused component test was added.
- Validations passed:
  - `npm run check` from `web/`
  - `npm run test:unit` from `web/`
  - `npm run build` from `web/` (passed with pre-existing CSS `@import` ordering warnings in generated optimization output)
- Files changed:
  - `web/src/routes/project/[id]/+page.svelte`
  - `_bmad-output/implementation-artifacts/deferred-work-tracker.md`
  - `_bmad-output/implementation-artifacts/deferred/deferred-DW-0029-package-rows-use-button-navigation.md`
- Commit: `3c667c51191f259badf33143228feb70af64e581`
- Push: `git push` completed successfully to upstream branch `origin/1_datapipeline`.
