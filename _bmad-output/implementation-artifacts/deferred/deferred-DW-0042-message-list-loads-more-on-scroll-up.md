---
workflow: bmad-deferred
id: DW-0042
status: done
source: Deferred from: code review of 4-2-chat-interface-echo-service (2026-05-08)
createdAt: 2026-05-12-1459
updatedAt: 2026-05-12-1618
---

# Deferred Work Plan: DW-0042 Message List Loads More on Scroll Up

## Raw Item

No pagination on list endpoint — not in spec, prototype phase.

## Understanding

The package message list currently returns all messages for a package in ascending order. The approved behavior is to load the most recent 20 messages initially, then load older messages as the user scrolls upward in the chat history.

## Decision

Approved plan-work. Add message pagination and upward infinite-scroll behavior for package chat history.

## Plan

### Tasks

#### 1. Add backend pagination for package messages

- Objective: Allow clients to request the latest page of messages and older pages without returning the full history.
- Likely files / areas:
  - `thagid/routers/messages.py`
  - `thagid/services/message.py`
  - `thagid/schemas/message.py`
  - `thagid/tests/test_messages.py`
- Subtasks:
  - Add query parameters for message pagination, keeping a default limit of 20.
  - Support loading older messages in a stable order, likely using a cursor based on message `created_at`/`id` or a simple offset if cursor complexity is unnecessary for the prototype.
  - Return messages in display order after fetching the requested page.
  - Preserve existing authorization behavior through `verify_package_access()`.
- Tests to update/add:
  - Add backend tests for default latest-20 behavior.
  - Add backend tests for fetching older messages.
  - Keep existing ordering tests updated to match the paginated contract.
- Validation:
  - `pytest thagid/tests/test_messages.py`
- Risks / notes:
  - Prefer a simple implementation unless existing code strongly favors cursor-based pagination.

#### 2. Add frontend upward infinite-scroll loading

- Objective: Load the latest 20 chat messages first, then prepend older messages when the user scrolls near the top.
- Likely files / areas:
  - `web/src/lib/api/messages.ts`
  - `web/src/routes/project/[id]/package/[pkgId]/+page.svelte`
  - `web/src/lib/components/custom/ChatInterface.svelte`
  - Relevant frontend tests if a suitable pattern exists.
- Subtasks:
  - Update message API client to accept pagination parameters and return pagination metadata.
  - Track whether older messages are available and whether an older-page load is in progress.
  - Detect scroll-near-top in the chat container and request older messages.
  - Prepend older messages while preserving scroll position so the viewport does not jump.
  - Keep optimistic send behavior working with the latest loaded page.
- Tests to update/add:
  - Add or update focused frontend tests if existing component/page test setup supports the behavior.
  - Otherwise rely on Svelte check/build and document manual validation steps.
- Validation:
  - `npm run check` from `web/` if available.
  - `npm test -- --run` from `web/` or the established Vitest command.
  - Manual check: open a package with more than 20 messages, confirm latest messages appear first and older messages load when scrolling upward.
- Risks / notes:
  - Avoid broad chat UI redesign; implement only pagination and scroll-up loading.

## Execution Record

Executed by `bmad-deferred-run` on 2026-05-12.

- Added backend message pagination with default latest-20 behavior and offset-based older-page loading while preserving package access checks.
- Updated frontend message loading to request the latest page initially, then prepend older messages when the chat history is scrolled near the top while preserving scroll position.
- Added backend pagination coverage and focused ChatInterface scroll-up load coverage.

### Files changed

- `thagid/routers/messages.py`
- `thagid/services/message.py`
- `thagid/tests/test_messages.py`
- `web/src/lib/api/messages.ts`
- `web/src/routes/project/[id]/package/[pkgId]/+page.svelte`
- `web/src/lib/components/custom/ChatInterface.svelte`
- `web/src/lib/components/custom/ChatInterface.test.ts`
- `_bmad-output/implementation-artifacts/deferred/deferred-DW-0042-message-list-loads-more-on-scroll-up.md`
- `_bmad-output/implementation-artifacts/deferred-work-tracker.md`

### Validation log

- `pytest thagid/tests/test_messages.py` — passed (10 tests)
- `npm run check` from `web/` — passed (0 errors, 0 warnings)
- `npm run test:unit` from `web/` — passed (12 files, 50 tests)

### Commit and push

- Commit: `b1f92c1`
- Push: pushed to `origin/1_datapipeline`
