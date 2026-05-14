# Task 06: Implement Frontend Review And Confirmation Flow

## Implementation Contract

- Objective: Make the package chat UI visibly support theme review, adjustments, explicit confirmation, and final concluded locking without calling internal endpoints or relying on hidden state.
- Runtime entrypoint: Package chat page `web/src/routes/project/[id]/package/[pkgId]/+page.svelte` and `ChatInterface.svelte`.
- Old owner: Theme review cards render only when phase is `extract`, with no explicit confirm/adjust controls beyond freeform chat.
- New owner: Frontend page uses brainstorm API client; custom components render review state and controls; backend/agent remains authoritative for state changes.
- Forbidden implementation patterns: No raw `fetch()` in components; no browser calls to `/internal/kg/*` or `/internal/agent/*`; no client-side finalization without backend confirmation; no hardcoded internal assumptions outside typed API layer.
- Required implementation patterns: API wrapper functions in `$lib/api/brainstorm.ts`; typed phase/status data in `$lib/types/brainstorm.ts`; custom components for review controls; Svelte 5 runes style consistent with existing code; design system/shadcn components where available.
- Compatibility allowed: Keep text-command support for “looks good”, rename, move, and return to brainstorming; add explicit buttons that send those supported messages through the public brainstorm message endpoint.
- Compatibility forbidden: Locking chat at `extract`; hiding review themes; showing summary card before backend reports finalized results.
- Files allowed: `web/src/lib/api/brainstorm.ts`, `web/src/lib/types/brainstorm.ts`, `web/src/routes/project/[id]/package/[pkgId]/+page.svelte`, `web/src/lib/components/custom/ChatInterface.svelte`, `ThemeCard.svelte`, `IdeaCard.svelte`, related custom components/tests, Playwright e2e files if present/needed.
- Files forbidden: `web/src/lib/components/ui/**` shadcn-managed files; backend/agent source except tests/fakes in other tasks; stale `docs/**`.

## Work Items

- Likely files / areas:
  - `ChatInterface.svelte` phase badges, review cards, confirm/back-to-brainstorm/adjust UI, locked state.
  - `+page.svelte` state updates after brainstorm responses.
  - `web/src/lib/types/brainstorm.ts` if new phase/status fields are needed.
  - `ChatInterface.test.ts` and possible Playwright flow.
- Subtasks:
  - Render a clear “Review themes” section whenever backend returns review phase/themes.
  - Add explicit confirm finalization control that sends the approved confirmation message through `sendBrainstormMessage`.
  - Add explicit “continue brainstorming” or adjustment guidance/actions without bypassing backend state.
  - Ensure attachments remain allowed only during facilitation and disabled during review/finalization as specified.
  - Ensure chat is not locked during review; lock only for `markdown`/`concluded` or confirmed final terminal state.
  - Ensure markdown/concluded response displays final artifact and dashboard/detail results can be reached after backend result availability.
  - Add tests for review display, confirm button behavior, adjustment guidance, no premature lock, terminal lock, and attachment gating.

## Completion Checks

- Done when:
  - User can start brainstorm, reach review phase, see grouped themes, confirm finalization, and then see concluded/markdown state.
  - Review phase is interactive and not locked.
  - Frontend sends only public brainstorm API calls for confirmation/adjustment.
  - No raw `fetch()` or internal endpoint calls are introduced.
- Evidence required:
  - Vitest tests proving review controls and state transitions.
  - Source references showing API wrapper use.
  - Optional Playwright evidence for the full UI flow.
- Forbidden shortcuts:
  - Client-only finalization flags.
  - Hiding theme review in markdown content only.
  - Editing shadcn `ui/` components.
- Static checks:
  - Search web code for `/internal/kg` and `/internal/agent` yields no browser calls.
  - `npm run check` passes.
- Test commands:
  - `cd web && npm run check`
  - `cd web && npm run test:unit`
  - `cd web && npm run test:e2e` if Playwright flow is added/available.
- Runtime-path evidence:
  - Component test or e2e shows confirm action calls `onSend`/API with a confirmation message and updates to concluded only after backend response.
- Validation:
  - Vitest for components; Playwright for package chat brainstorm flow where practical.
- Risks / notes:
  - Keep controls simple and text-command-compatible; do not create a separate frontend-only theme editor unless backend supports corresponding commands.
