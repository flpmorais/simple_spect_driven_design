# Story 4.3: Brainstorm Summary Card on Project Dashboard

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a project user,
I want concluded brainstorms summarized on the project dashboard,
so that I can discover and reopen useful ideation results quickly.

## Acceptance Criteria

1. Given a package has a concluded brainstorm session, when I view the project dashboard, then a BrainstormSummaryCard appears under or near the package row, and it shows session date, technique count, idea count, theme count, and theme pills.
2. Given more themes exist than fit in the summary card, when the card renders theme pills, then it shows the configured maximum number of theme pills, and displays a `+N more` indicator for hidden themes.
3. Given I click View Details on the summary card, when navigation completes, then I arrive at the brainstorm detail view for that package session, and focus moves to the main content heading.

## Tasks / Subtasks

- [x] Add a project-dashboard BrainstormSummaryCard component (AC: 1, 2, 3)
  - [x] Create `web/src/lib/components/custom/BrainstormSummaryCard.svelte` using the project-dashboard design-system spec.
  - [x] Accept a package id, project id, and `BrainstormResultsResponse`-compatible summary data; do not perform API calls inside the component.
  - [x] Render only concluded results data returned by `/api/packages/{package_id}/brainstorm/results`.
  - [x] Show date from `concluded_at` when present, otherwise `created_at`; format with browser-safe date formatting and avoid showing raw ISO strings.
  - [x] Show technique count, idea count, and theme count in one stats row. Current results expose one `technique` string; derive technique count as `1` when non-null and `0` when null unless the backend contract is explicitly extended.
  - [x] Render theme pills as `{Theme Title} ({idea count})`.
  - [x] Limit visible theme pills to 5 and render `+N more` for hidden themes.
  - [x] Render a real link/button for View Details to `/project/{projectId}/package/{packageId}/brainstorm`.
  - [x] Ensure the View Details action stops package-row navigation if the card is nested near a clickable package row.
- [x] Load concluded brainstorm summaries on the project dashboard (AC: 1)
  - [x] Update `web/src/routes/project/[id]/+page.svelte` after packages load to request brainstorm results for each visible package with existing `getBrainstormResults`.
  - [x] Treat `404 Brainstorm results not found` as an expected “no concluded brainstorm” state for that package; do not show an error toast for it.
  - [x] Preserve existing project brief loading, package list loading, empty state, GitHub links, and package-row navigation behavior.
  - [x] Avoid adding new backend endpoints unless the per-package results calls prove insufficient; the existing browser-facing results endpoint already enforces package authorization.
  - [x] Guard against stale async responses when the scoped project changes, matching the existing `stale` pattern in the page.
- [x] Add or update frontend types/API support only where needed (AC: 1, 2)
  - [x] Reuse `BrainstormResultsResponse`, `BrainstormTheme`, and `getBrainstormResults` from `web/src/lib/types/brainstorm.ts` and `web/src/lib/api/brainstorm.ts`.
  - [x] Add helper types only if they make the dashboard state clearer; avoid duplicating the backend response shape.
  - [x] Do not change `BrainstormResultsResponse` unless backend response fields are also intentionally changed and tested.
- [x] Prepare navigation target compatibility (AC: 3)
  - [x] Link to the planned detail route `/project/{projectId}/package/{packageId}/brainstorm` from the summary card.
  - [x] If the detail route is not implemented yet, keep this story scoped to producing the correct URL and accessible link; Story 4.4 owns detail page implementation.
  - [x] Add a focus-management requirement for Story 4.4 in dev notes if the route cannot yet move focus because it does not exist.
- [x] Add focused frontend tests (AC: 1, 2, 3)
  - [x] Add `web/src/lib/components/custom/BrainstormSummaryCard.test.ts` covering stats, date display, theme pill rendering, `+N more`, and View Details href.
  - [x] Add or update a project dashboard test if an existing route test harness exists; otherwise document why component-level coverage is the practical default.
  - [x] Verify packages without concluded results do not render cards and do not surface user-visible errors.
  - [x] Run `cd web && npx vitest run` or the narrow equivalent for changed frontend tests.

## Dev Notes

### Scope Boundaries

- This is a frontend dashboard discovery story. Build the summary card and wire it into the project dashboard; do not build the brainstorm detail page content, theme browsing page, vector search UI, or new KG write behavior.
- Use existing browser-facing package brainstorm results: `GET /api/packages/{package_id}/brainstorm/results`. It returns `404` when no concluded results exist; that is a normal hidden-card condition for this story.
- Do not add a browser-facing vector search endpoint or expose internal `/internal/kg/*` routes to the frontend.
- If a bulk dashboard summaries API becomes desirable for performance, stop and ask before adding it. The simplest MVP path is per-package calls using the existing authorized endpoint.

### Current Codebase State

- Project dashboard route: `web/src/routes/project/[id]/+page.svelte` loads the project brief and `listPackages(project.id)` inside a `$effect`, stores `packages`, and renders a clickable package row button that navigates to `/project/{projectId}/package/{pkgId}`.
- Package list rows are currently rendered inside `<div class="divide-y divide-slate-200">` with a full-width `<button>`. If a card is nested under each row, avoid invalid nested interactive controls; prefer a wrapper per package with a row button plus a sibling summary card.
- Existing brainstorm API client: `web/src/lib/api/brainstorm.ts` exports `getBrainstormResults(packageId)` for `/api/packages/{packageId}/brainstorm/results`.
- Existing brainstorm result type: `BrainstormResultsResponse` includes `session_id`, `package_id`, `project_id`, `technique`, `summary`, `created_at`, `concluded_at`, `theme_count`, `idea_count`, `context_source_count`, `themes`, and `context_sources`.
- Existing theme type: `BrainstormTheme` includes `id`, `title`, `summary`, `ideas`, and optional `position`.
- Existing backend results route in `thagid/routers/brainstorm.py` verifies package access, returns `BrainstormResultsResponse`, and maps `BrainstormResultsNotFoundError` to `404` with detail `Brainstorm results not found`.
- Existing backend tests in `thagid/tests/test_brainstorm.py` already prove results success, auth, cross-org forbidden, invalid package id, missing package, and no concluded results behavior.

### UI / Design-System Requirements

- Because this story edits UI, the developer must read and follow `design-system/thagid/MASTER.md` and `design-system/thagid/pages/project-dashboard.md` before coding.
- BrainstormSummaryCard spec: `bg-white border border-slate-200 rounded-xl p-5 mt-2`; header row with Lucide `lightbulb` icon, “Brainstorm”, and date; stats row `text-xs text-slate-500`; theme pills `text-xs font-medium px-2.5 py-1 rounded-full bg-slate-100 text-slate-600`; max 5 visible pills plus `+N more`; View Details is right-aligned `text-sm font-medium text-primary`.
- Use Lucide icons only. Do not use emoji icons from the design doc examples.
- Maintain desktop-only MVP behavior; no mobile-specific layout work is required.
- Ensure visible focus rings, keyboard-reachable View Details link, and WCAG AA contrast.

### Implementation Guidance

- Recommended dashboard state shape: `let brainstormResultsByPackageId = $state<Record<string, BrainstormResultsResponse>>({});` plus optional loading/error tracking only if needed for tests or skeletons.
- Recommended loading flow: after `listPackages` resolves, request results for each package. For each fulfilled result, store it by package id. For `404`, skip. For other errors, do not block package display; consider silent skip or a non-disruptive console-free handling consistent with existing API error patterns.
- Avoid using `Promise.all` in a way that fails all cards when one package has no results. Use per-package `try/catch` or `Promise.allSettled`.
- Preserve stale-response protection from the existing `$effect`: if the project changes while requests are in flight, do not update dashboard state.
- Do not call raw `fetch()` from Svelte components. All HTTP calls must go through `$lib/api/*` wrappers, using `getBrainstormResults`.
- Keep the component pure/presentational so it can be unit-tested without network mocking.
- Sorting: preserve package list order. Theme pills can use the response order, which should already reflect graph/theme ordering from Story 4.1.
- Date formatting should tolerate `null` dates. If both `concluded_at` and `created_at` are null, render a neutral label such as “Date unavailable” rather than crashing.

### Navigation and Focus Notes

- The target route for View Details is `/project/{projectId}/package/{packageId}/brainstorm` per the UX spec.
- Story 4.4 owns creating the brainstorm detail route and moving focus to the main heading after navigation. In this story, ensure the summary card uses a real link/button with an accessible name so the later route can satisfy focus movement.
- If implementing a temporary focus handoff is possible without creating the detail page, use a query/hash only if it does not conflict with SvelteKit routing. Do not create the full detail page here.

### Previous Story Intelligence

- Story 4.2 completed internal KG vector search and explicitly kept Epic 4 UI work out of scope. This story begins the UI side and should not modify vector search code.
- Story 4.2 reinforced project isolation and existing response-shape preservation. Dashboard cards must use package-scoped browser endpoints that already enforce user org/project/package authorization.
- Story 4.1 added `get_brainstorm_results` and browser-facing `/api/packages/{package_id}/brainstorm/results`. Reuse that contract; do not duplicate raw KG traversal in the frontend.
- Story 4.1 review patched browser results to expose stable source IDs and avoid raw context chunk content. This card should display only summary metadata and theme titles/counts; do not expose context source raw content or graph internals.
- Recent commits emphasize focused changes with tests: `fix vector search review findings`, `fix brainstorm results review findings`, `feat: add extraction validation and node versioning`, `feat: add brainstorm markdown finalization`, and `feat: add async idea embeddings`.

### File Structure Requirements

- Likely frontend updates:
  - `web/src/lib/components/custom/BrainstormSummaryCard.svelte` (new)
  - `web/src/lib/components/custom/BrainstormSummaryCard.test.ts` (new)
  - `web/src/routes/project/[id]/+page.svelte` (update)
- Possible frontend updates only if needed:
  - `web/src/lib/types/brainstorm.ts`
  - `web/src/lib/api/brainstorm.ts`
- Avoid backend files, migrations, agent files, KG service files, compose files, and detail-route implementation unless explicitly approved or the story scope is updated.

### Testing Requirements

- Component tests should cover the visible contract: date, technique count derivation, idea/theme counts, theme pills, overflow `+N more`, View Details link target, and accessible labels.
- Dashboard integration behavior should verify that a package with returned results renders a card and a package with 404/no results does not render a card. If route-level testing is not set up, keep component tests strong and note the gap.
- Run frontend tests with Vitest. If only narrow tests are practical, run the changed component test and any existing affected component tests.
- Backend tests are not required unless backend contracts are changed. If backend code is changed despite guidance, run `rtk pytest thagid/tests/test_brainstorm.py -q`.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story-4.3-Brainstorm-Summary-Card-on-Project-Dashboard]
- [Source: _bmad-output/planning-artifacts/prd.md#Frontend-Brainstorm-Dashboard]
- [Source: _bmad-output/planning-artifacts/architecture.md#Frontend-Dashboard]
- [Source: _bmad-output/planning-artifacts/architecture.md#API-Boundaries]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#BrainstormSummaryCard]
- [Source: design-system/thagid/MASTER.md#Component-Specs]
- [Source: design-system/thagid/pages/project-dashboard.md#Brainstorm-Summary-Card]
- [Source: design-system/thagid/pages/brainstorm-detail.md#Navigation]
- [Source: web/src/routes/project/[id]/+page.svelte]
- [Source: web/src/lib/api/brainstorm.ts]
- [Source: web/src/lib/types/brainstorm.ts]
- [Source: thagid/routers/brainstorm.py]
- [Source: thagid/schemas/brainstorm.py]
- [Source: _bmad-output/implementation-artifacts/4-2-vector-similarity-search-for-ideas.md#Previous-Story-Intelligence]
- [Source: _bmad-output-old/1_datapipeline/project-context.md#Critical-Implementation-Rules]

## Project Structure Notes

- This story extends the existing SvelteKit project dashboard and custom component library under `web/src/lib/components/custom/`.
- Use shadcn-svelte primitives where already present, but the summary card itself is a custom component per the design system.
- Keep API access layered: dashboard page calls `$lib/api/brainstorm.ts`, component renders props, no raw fetch in components.

## Dev Agent Record

### Agent Model Used

openai/gpt-5.5

### Debug Log References

- `cd web && npm run test:unit -- src/lib/components/custom/BrainstormSummaryCard.test.ts` initially failed because `BrainstormSummaryCard.svelte` did not exist, confirming the red phase.
- `cd web && npm run check` passed with 0 errors and 0 warnings.
- `cd web && npm run test:unit -- src/lib/components/custom/BrainstormSummaryCard.test.ts` passed: 3 tests.
- `cd web && npm run test:unit` passed: 10 files, 42 tests.

### Completion Notes List

- Ultimate context engine analysis completed - comprehensive developer guide created.
- Implemented a pure BrainstormSummaryCard that renders design-system styling, browser-safe dates, derived technique count, idea/theme stats, theme pills, overflow indicator, and an accessible View Details link.
- Wired the project dashboard to load per-package brainstorm results after packages load, skip the expected no-results 404 state, preserve stale-response guards, and render cards as siblings to package row buttons.
- Reused existing brainstorm API/type contracts without backend changes or new endpoints; route-level test harness does not exist, so dashboard integration coverage is documented as a manual/code-review gap and component tests cover the visible card contract.

### File List

- `_bmad-output/implementation-artifacts/4-3-brainstorm-summary-card-on-project-dashboard.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `web/src/lib/components/custom/BrainstormSummaryCard.svelte`
- `web/src/lib/components/custom/BrainstormSummaryCard.test.ts`
- `web/src/routes/project/[id]/+page.svelte`

### Change Log

- 2026-05-11: Added dashboard brainstorm summary card, per-package dashboard results loading, focused component tests, and moved story to review.
